# 🤖 AI 智能清理重复照片

[English](./README_EN.md) | 中文

使用**感知哈希算法**（Perceptual Hash）自动检测并清理重复或相似照片的 AI 工具。

![Python Version](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows/Mac/Linux-lightgrey)

## ✨ 功能特性

- 🔍 **智能检测** - 使用感知哈希算法检测视觉上相似的图片
- ⚡ **高速扫描** - 支持批量处理数千张照片
- 🎯 **灵活配置** - 可调整相似度阈值
- 🗑️ **安全删除** - 默认模拟运行，确认后真正删除
- 📊 **详细报告** - 生成去重统计报告
- 🖼️ **GUI 版本** - 提供图形界面版本（可选）

## 📦 安装

```bash
# 克隆仓库
git clone https://github.com/H-vemi/photo-deduplicator.git
cd photo-deduplicator

# 安装依赖
pip install -r requirements.txt
```

## 🚀 使用方法

### 命令行版本

```bash
# 扫描目录（模拟运行）
python photo_dedup_main.py /path/to/photos

# 扫描并显示详细信息
python photo_dedup_main.py /path/to/photos --threshold 3

# 真正删除重复文件
python photo_dedup_main.py /path/to/photos --delete
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `image_dir` | 图片目录路径 | 必填 |
| `--threshold` | 哈希距离阈值（0-64），越小越严格 | 5 |
| `--hash-size` | 感知哈希大小（8 或 16） | 8 |
| `--delete` | 真正删除文件（默认模拟运行） | False |

### 阈值参考

| 阈值 | 效果 |
|------|------|
| 0-2 | 几乎完全相同 |
| 3-5 | 非常相似（推荐） |
| 6-10 | 相似但可能有差异 |
| 10+ | 较宽松的匹配 |

## 📊 使用示例

```bash
$ python photo_dedup_main.py ./my_photos

============================================================
📸 AI 智能照片去重报告
============================================================
扫描图片总数: 150
发现重复组数: 12
重复图片总数: 28
可删除文件数: 16
可释放空间: 245.67 MB
============================================================

📋 模拟运行：将删除 16 个文件
   使用 --delete 参数真正执行删除
```

## 🖼️ GUI 版本

```bash
# 启动图形界面
python photo_dedup_gui.py
```

GUI 版本提供：
- 📁 文件夹选择
- 📊 实时进度显示
- 🖼️ 缩略图预览
- 🎚️ 阈值滑块调节
- ✅ 批量确认删除

## 🧠 技术原理

### 感知哈希算法

```
1. 缩放图片 → 8x8 像素
2. 转换为灰度图
3. 计算 DCT 变换
4. 取左上角低频部分
5. 计算均值并生成哈希
```

### 汉明距离

比较两个哈希值的差异程度：
- 距离 ≤ 5：视觉上几乎相同
- 距离 > 30：完全不同的图片

## 📁 项目结构

```
photo-deduplicator/
├── photo_dedup_main.py    # 主程序（CLI）
├── photo_dedup_gui.py     # GUI 版本
├── requirements.txt       # Python 依赖
├── README.md              # 中文说明
├── README_EN.md           # English
├── setup.py               # 安装脚本
└── examples/
    └── sample_usage.py    # 使用示例
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📝 许可证

MIT License - 自由使用、修改、分发

---

Made with ❤️ by OpenClaw AI Agent
