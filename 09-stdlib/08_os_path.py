#!/usr/bin/env python3
"""
os.path模块 - Python标准库路径操作

涵盖内容:
  1. join - 拼接路径
  2. split / splitext - 分割路径
  3. basename / dirname - 文件名与目录名
  4. exists / isfile / isdir - 路径检测
  5. getsize / getmtime / abspath - 文件属性
  6. 路径操作实战

参考: https://www.runoob.com/python3/python3-os-path.html
"""

import os
import os.path
import tempfile
from pathlib import Path  # 顺带介绍 pathlib (Python 3.4+ 推荐方式)


# ============================================================
# 1. join - 路径拼接
# ============================================================
print("=" * 60)
print("1. os.path.join() - 跨平台路径拼接")
print("=" * 60)

# 跨平台路径拼接, 自动使用正确的分隔符
paths = [
    os.path.join("home", "user", "docs"),
    os.path.join("C:\\", "Users", "Admin", "Desktop"),
    os.path.join("folder", "file.txt"),
    os.path.join("/", "var", "log", "app.log"),
]

for p in paths:
    print(f"  {p}")

print(f"\n当前系统分隔符: '{os.sep}'")
print(f"说明: Windows用 '\\', Linux/macOS用 '/'")

# ============================================================
# 2. split / splitext - 分割路径
# ============================================================
print("\n" + "=" * 60)
print("2. split() / splitext() - 分割路径")
print("=" * 60)

# split - 分割成 (目录, 文件名)
test_paths = [
    "/home/user/document.txt",
    "C:\\Users\\Admin\\Desktop\\report.pdf",
    "folder/subfolder/data.csv",
    "just_a_file.py",
]

print("split() 分割结果:")
for p in test_paths:
    head, tail = os.path.split(p)
    print(f"  原始:   {p}")
    print(f"  目录:   {head}")
    print(f"  文件名: {tail}")
    print()

# splitext - 分割扩展名
print("splitext() 分割结果:")
files = ["report.pdf", "data.csv", "image.tar.gz", "README", ".gitignore"]
for f in files:
    name, ext = os.path.splitext(f)
    print(f"  '{f}' → 名称='{name}', 扩展名='{ext}'")

# ============================================================
# 3. basename / dirname - 简化操作
# ============================================================
print("\n" + "=" * 60)
print("3. basename / dirname - 文件名与目录名")
print("=" * 60)

p = "/home/user/projects/python/script.py"
print(f"完整路径:    {p}")
print(f"dirname:     {os.path.dirname(p)}")
print(f"basename:    {os.path.basename(p)}")

# 组合验证
print(f"\n组合验证: dirname + basename == 原路径?")
restored = os.path.join(os.path.dirname(p), os.path.basename(p))
print(f"  {restored}")
print(f"  是否等价: {os.path.normpath(restored) == os.path.normpath(p)}")

# ============================================================
# 4. exists / isfile / isdir - 路径检测
# ============================================================
print("\n" + "=" * 60)
print("4. exists / isfile / isdir - 路径检测")
print("=" * 60)

# 检测当前脚本文件
this_file = __file__
print(f"当前脚本: {this_file}")
print(f"  exists:   {os.path.exists(this_file)}")
print(f"  isfile:   {os.path.isfile(this_file)}")
print(f"  isdir:    {os.path.isdir(this_file)}")
print(f"  isabs:    {os.path.isabs(this_file)} (是否为绝对路径)")

# 检测所在目录
this_dir = os.path.dirname(this_file)
print(f"\n脚本目录: {this_dir}")
print(f"  exists:   {os.path.exists(this_dir)}")
print(f"  isfile:   {os.path.isfile(this_dir)}")
print(f"  isdir:    {os.path.isdir(this_dir)}")

# 检测不存在的东西
fake = os.path.join(this_dir, "不存在的文件.txt")
print(f"\n不存在的路径: {fake}")
print(f"  exists:   {os.path.exists(fake)}")

# ============================================================
# 5. 文件属性
# ============================================================
print("\n" + "=" * 60)
print("5. 文件属性 (大小/时间)")
print("=" * 60)

# getsize - 文件大小
size = os.path.getsize(this_file)
print(f"当前脚本大小: {size} 字节 ({size / 1024:.1f} KB)")

# getmtime / getatime / getctime
mtime = os.path.getmtime(this_file)  # 最后修改时间
atime = os.path.getatime(this_file)  # 最后访问时间
ctime = os.path.getctime(this_file)  # 创建时间 (Windows) / 元数据变更 (Unix)

from datetime import datetime
print(f"最后修改: {datetime.fromtimestamp(mtime)}")
print(f"最后访问: {datetime.fromtimestamp(atime)}")
print(f"创建时间: {datetime.fromtimestamp(ctime)}")

# abspath / realpath
print(f"\nabspath (当前脚本):  {os.path.abspath(this_file)}")
print(f"realpath (解析链接):  {os.path.realpath(this_file)}")
print(f"normpath (规范化):    {os.path.normpath(this_file)}")

# ============================================================
# 6. 路径操作实战
# ============================================================
print("\n" + "=" * 60)
print("6. 路径操作实战 - 遍历目录收集文件信息")
print("=" * 60)

# 以当前脚本目录为参考
base_dir = os.path.dirname(os.path.abspath(this_file))
print(f"工作目录: {base_dir}\n")

# 列出目录中的 .py 文件
py_files = [f for f in os.listdir(base_dir) if f.endswith('.py')]
print(f"本目录下的 .py 文件 ({len(py_files)}个):")
for fname in sorted(py_files):
    full_path = os.path.join(base_dir, fname)
    size = os.path.getsize(full_path)
    mtime = datetime.fromtimestamp(os.path.getmtime(full_path))
    print(f"  {fname:<25} {size:>5}字节  修改: {mtime.strftime('%Y-%m-%d')}")

# 路径规范化工具
print("\n路径规范化示例:")
messy = "folder//sub/./../sub/file.txt"
print(f"  原始:     {messy}")
print(f"  normpath: {os.path.normpath(messy)}")
print(f"  realpath: {os.path.realpath(messy)}")

# commonpath / commonprefix
print(f"\n共同路径: {os.path.commonpath(['/a/b/c', '/a/b/d', '/a/b/e'])}")

# ============================================================
# 7. pathlib 简介 (Python 3.4+ 推荐)
# ============================================================
print("\n" + "=" * 60)
print("7. pathlib 简介 (Python 3.4+ 推荐的新方式)")
print("=" * 60)

# Path 对象是跨平台的面向对象路径管理
p = Path(this_file)
print(f"Path 对象: {p}")
print(f"  name:      {p.name}")
print(f"  stem:      {p.stem}")
print(f"  suffix:    {p.suffix}")
print(f"  parent:    {p.parent}")
print(f"  exists():  {p.exists()}")
print(f"  is_file(): {p.is_file()}")
print(f"  stat().st_size: {p.stat().st_size} 字节")

# 链式操作
print(f"\n链式操作: {p.parent / 'subdir' / 'file.txt'}")
print(f"读取自身: Path(__file__).read_text()  # 一行读取")

print("\n总结: Python 3.4+ 推荐使用 pathlib.Path 代替 os.path")
print("  os.path [>>] 传统方式, 字符串操作")
print("  pathlib [*] 现代方式, 面向对象, 更直观")
