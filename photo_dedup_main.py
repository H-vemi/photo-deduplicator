#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 智能清理重复照片 - 主程序
使用感知哈希算法自动检测并清理重复图片
"""

import os
import sys
import argparse
import logging
from pathlib import Path
from typing import List, Dict, Set, Tuple
from collections import defaultdict
import hashlib
from PIL import Image
import imagehash

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PhotoDeduplicator:
    """照片去重工具类"""
    
    def __init__(self, hash_size: int = 8, threshold: int = 5):
        """
        初始化去重工具
        
        Args:
            hash_size: 感知哈希大小（8x8 或 16x16）
            threshold: 哈希距离阈值（0-64），越小越严格
        """
        self.hash_size = hash_size
        self.threshold = threshold
        self.hashes: Dict[str, str] = {}  # 文件路径 -> 哈希值
        self.duplicates: Dict[str, List[str]] = defaultdict(list)  # 哈希值 -> 重复文件列表
        
    def get_image_hash(self, image_path: str) -> str:
        """
        计算图片的感知哈希值
        
        Args:
            image_path: 图片文件路径
            
        Returns:
            哈希值字符串
        """
        try:
            img = Image.open(image_path)
            # 使用感知哈希（Perceptual Hash）
            phash = imagehash.phash(img, hash_size=self.hash_size)
            return str(phash)
        except Exception as e:
            logger.warning(f"无法处理图片 {image_path}: {e}")
            return None
    
    def hamming_distance(self, hash1: str, hash2: str) -> int:
        """
        计算两个哈希值的汉明距离
        
        Args:
            hash1: 第一个哈希值
            hash2: 第二个哈希值
            
        Returns:
            汉明距离
        """
        return sum(c1 != c2 for c1, c2 in zip(hash1, hash2))
    
    def find_duplicates(self, image_dir: str) -> Dict[str, List[str]]:
        """
        扫描目录并找出重复照片
        
        Args:
            image_dir: 图片目录路径
            
        Returns:
            重复照片分组字典
        """
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
        image_dir = Path(image_dir)
        
        if not image_dir.exists():
            logger.error(f"目录不存在: {image_dir}")
            return {}
        
        logger.info(f"开始扫描目录: {image_dir}")
        
        # 第一步：计算所有图片的哈希值
        for image_file in image_dir.rglob('*'):
            if image_file.suffix.lower() in image_extensions:
                image_hash = self.get_image_hash(str(image_file))
                if image_hash:
                    self.hashes[str(image_file)] = image_hash
                    logger.debug(f"已处理: {image_file.name} -> {image_hash}")
        
        logger.info(f"共处理 {len(self.hashes)} 张图片")
        
        # 第二步：比较哈希值，找出相似图片
        processed = set()
        for file1, hash1 in self.hashes.items():
            if file1 in processed:
                continue
            
            group = [file1]
            for file2, hash2 in self.hashes.items():
                if file1 != file2 and file2 not in processed:
                    distance = self.hamming_distance(hash1, hash2)
                    if distance <= self.threshold:
                        group.append(file2)
                        processed.add(file2)
            
            if len(group) > 1:
                self.duplicates[hash1] = group
                logger.info(f"找到 {len(group)} 张相似图片（距离 <= {self.threshold}）")
        
        return self.duplicates
    
    def get_file_size(self, file_path: str) -> int:
        """获取文件大小（字节）"""
        try:
            return os.path.getsize(file_path)
        except:
            return 0
    
    def select_duplicates_to_delete(self) -> List[str]:
        """
        选择要删除的重复文件（保留最大的，删除其他）
        
        Returns:
            要删除的文件列表
        """
        to_delete = []
        
        for hash_val, files in self.duplicates.items():
            if len(files) > 1:
                # 按文件大小排序，保留最大的
                sorted_files = sorted(files, key=self.get_file_size, reverse=True)
                keep_file = sorted_files[0]
                delete_files = sorted_files[1:]
                
                logger.info(f"保留: {keep_file} ({self.get_file_size(keep_file)} bytes)")
                for f in delete_files:
                    logger.info(f"  删除: {f} ({self.get_file_size(f)} bytes)")
                    to_delete.append(f)
        
        return to_delete
    
    def delete_duplicates(self, dry_run: bool = True) -> Tuple[int, int]:
        """
        删除重复文件
        
        Args:
            dry_run: 是否为模拟运行（不真正删除）
            
        Returns:
            (删除文件数, 释放空间字节数)
        """
        to_delete = self.select_duplicates_to_delete()
        deleted_count = 0
        freed_space = 0
        
        for file_path in to_delete:
            file_size = self.get_file_size(file_path)
            freed_space += file_size
            
            if dry_run:
                logger.info(f"[模拟] 删除: {file_path}")
            else:
                try:
                    os.remove(file_path)
                    logger.info(f"✅ 已删除: {file_path}")
                    deleted_count += 1
                except Exception as e:
                    logger.error(f"删除失败 {file_path}: {e}")
        
        return deleted_count, freed_space
    
    def generate_report(self) -> str:
        """生成去重报告"""
        report = []
        report.append("=" * 60)
        report.append("📸 AI 智能照片去重报告")
        report.append("=" * 60)
        report.append(f"扫描图片总数: {len(self.hashes)}")
        report.append(f"发现重复组数: {len(self.duplicates)}")
        
        total_duplicates = sum(len(files) - 1 for files in self.duplicates.values())
        report.append(f"重复图片总数: {total_duplicates}")
        
        to_delete = self.select_duplicates_to_delete()
        freed_space = sum(self.get_file_size(f) for f in to_delete)
        
        report.append(f"可删除文件数: {len(to_delete)}")
        report.append(f"可释放空间: {freed_space / (1024*1024):.2f} MB")
        report.append("=" * 60)
        
        return "\n".join(report)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="🤖 AI 智能清理重复照片"
    )
    parser.add_argument(
        "image_dir",
        help="图片目录路径"
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=5,
        help="哈希距离阈值（0-64），默认 5"
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="真正删除重复文件（默认为模拟运行）"
    )
    parser.add_argument(
        "--hash-size",
        type=int,
        default=8,
        help="感知哈希大小（8 或 16），默认 8"
    )
    
    args = parser.parse_args()
    
    # 创建去重工具实例
    dedup = PhotoDeduplicator(
        hash_size=args.hash_size,
        threshold=args.threshold
    )
    
    # 扫描并找出重复照片
    dedup.find_duplicates(args.image_dir)
    
    # 生成报告
    report = dedup.generate_report()
    print(report)
    
    # 删除重复文件
    deleted, freed = dedup.delete_duplicates(dry_run=not args.delete)
    
    if args.delete:
        print(f"\n✅ 已删除 {deleted} 个文件，释放 {freed / (1024*1024):.2f} MB 空间")
    else:
        print(f"\n📋 模拟运行：将删除 {len(dedup.select_duplicates_to_delete())} 个文件")
        print("   使用 --delete 参数真正执行删除")


if __name__ == "__main__":
    main()
