#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 智能清理重复照片 - 安装脚本
"""

from setuptools import setup, find_packages

setup(
    name="photo-deduplicator",
    version="1.0.0",
    description="🤖 AI 智能清理重复照片 - 使用感知哈希算法自动检测并清理重复图片",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="H-vemi",
    author_email="H-vemi3445466162@qq.com",
    url="https://github.com/H-vemi/photo-deduplicator",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "Pillow>=10.0.0",
        "imagehash>=4.3.1",
    ],
    extras_require={
        "gui": [],
        "web": ["flask>=2.0.0", "werkzeug>=2.0.0"],
        "dev": ["pytest>=7.0.0", "pytest-cov>=4.0.0"],
    },
    entry_points={
        "console_scripts": [
            "photo-dedup=photo_dedup_main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Utilities",
    ],
)
