#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 智能清理重复照片 - GUI 版本
提供图形界面用于照片去重
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import threading
from photo_dedup_main import PhotoDeduplicator


class PhotoDeduplicatorGUI:
    """照片去重 GUI 应用"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 AI 智能清理重复照片")
        self.root.geometry("600x500")
        self.dedup = None
        self.selected_dir = tk.StringVar()
        
        self.setup_ui()
    
    def setup_ui(self):
        """设置用户界面"""
        # 标题
        title = tk.Label(
            self.root,
            text="🤖 AI 智能清理重复照片",
            font=("Arial", 16, "bold")
        )
        title.pack(pady=10)
        
        # 目录选择
        dir_frame = tk.Frame(self.root)
        dir_frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(dir_frame, text="选择图片目录:").pack(side=tk.LEFT)
        tk.Entry(dir_frame, textvariable=self.selected_dir, width=40).pack(side=tk.LEFT, padx=5)
        tk.Button(dir_frame, text="浏览", command=self.select_directory).pack(side=tk.LEFT)
        
        # 参数设置
        param_frame = tk.LabelFrame(self.root, text="参数设置", padx=10, pady=10)
        param_frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(param_frame, text="相似度阈值 (0-64):").pack()
        self.threshold_var = tk.IntVar(value=5)
        tk.Scale(
            param_frame,
            from_=0,
            to=64,
            orient=tk.HORIZONTAL,
            variable=self.threshold_var
        ).pack(fill=tk.X)
        
        # 进度条
        self.progress = ttk.Progressbar(self.root, mode='indeterminate')
        self.progress.pack(pady=10, padx=10, fill=tk.X)
        
        # 结果显示
        self.result_text = tk.Text(self.root, height=10, width=70)
        self.result_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # 按钮
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="扫描", command=self.scan).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="删除", command=self.delete).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="清空", command=self.clear).pack(side=tk.LEFT, padx=5)
    
    def select_directory(self):
        """选择目录"""
        directory = filedialog.askdirectory(title="选择图片目录")
        if directory:
            self.selected_dir.set(directory)
    
    def scan(self):
        """扫描目录"""
        if not self.selected_dir.get():
            messagebox.showwarning("警告", "请先选择图片目录")
            return
        
        self.progress.start()
        thread = threading.Thread(target=self._scan_thread)
        thread.start()
    
    def _scan_thread(self):
        """扫描线程"""
        try:
            self.dedup = PhotoDeduplicator(threshold=self.threshold_var.get())
            self.dedup.find_duplicates(self.selected_dir.get())
            
            report = self.dedup.generate_report()
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, report)
        except Exception as e:
            messagebox.showerror("错误", str(e))
        finally:
            self.progress.stop()
    
    def delete(self):
        """删除重复文件"""
        if not self.dedup:
            messagebox.showwarning("警告", "请先扫描目录")
            return
        
        if messagebox.askyesno("确认", "确定要删除重复文件吗？"):
            self.progress.start()
            thread = threading.Thread(target=self._delete_thread)
            thread.start()
    
    def _delete_thread(self):
        """删除线程"""
        try:
            deleted, freed = self.dedup.delete_duplicates(dry_run=False)
            messagebox.showinfo(
                "完成",
                f"已删除 {deleted} 个文件\n释放空间: {freed / (1024*1024):.2f} MB"
            )
        except Exception as e:
            messagebox.showerror("错误", str(e))
        finally:
            self.progress.stop()
    
    def clear(self):
        """清空结果"""
        self.result_text.delete(1.0, tk.END)


def main():
    root = tk.Tk()
    app = PhotoDeduplicatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
