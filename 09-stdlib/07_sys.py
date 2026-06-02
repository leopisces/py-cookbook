#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sys模块 - Python标准库系统相关功能

涵盖内容:
  1. sys.argv - 命令行参数
  2. sys.path - 模块搜索路径
  3. sys.exit - 程序退出
  4. sys.stdin / stdout / stderr - 标准输入输出
  5. sys.platform / sys.version - 平台与版本信息
  6. sys.getsizeof / sys.getrecursionlimit - 内省信息

参考: https://www.runoob.com/python3/python3-sys.html
"""

import sys


# ============================================================
# 1. sys.argv - 命令行参数
# ============================================================
print("=" * 60)
print("1. sys.argv - 命令行参数")
print("=" * 60)

print(f"脚本名称: {sys.argv[0]}")
print(f"全部参数: {sys.argv}")
print(f"参数个数: {len(sys.argv)}")

# 模拟带参数运行
print("\n用法示例:")
print("  python 07_sys.py arg1 arg2 arg3")
print("  # 则 sys.argv = ['07_sys.py', 'arg1', 'arg2', 'arg3']")

# ============================================================
# 2. sys.path - 模块搜索路径
# ============================================================
print("\n" + "=" * 60)
print("2. sys.path - 模块搜索路径 (仅显示前5条)")
print("=" * 60)

for i, p in enumerate(sys.path[:5]):
    print(f"  [{i}] {p}")
print(f"  ... 共 {len(sys.path)} 条路径")

# sys.path 是一个列表, 可以动态修改
print("\n说明: sys.path 决定 import 时从哪里查找模块")
print("  sys.path.insert(0, '/my/modules')  # 插入自定义路径")

# ============================================================
# 3. sys.exit - 程序退出
# ============================================================
print("\n" + "=" * 60)
print("3. sys.exit() - 程序退出")
print("=" * 60)

print("演示 sys.exit() 的行为:")
print("  sys.exit(0)     # 正常退出")
print("  sys.exit(1)     # 异常退出 (错误码)")
print("  sys.exit('错误信息')  # 打印消息后退出(返回码1)")

# 捕获 SystemExit 可以阻止程序退出
print("\n模拟捕获 SystemExit:")
try:
    sys.exit(0)
except SystemExit as e:
    print(f"  捕获到 SystemExit, 退出码: {e.code}")
    print(f"  程序未退出, 继续执行...")

# ============================================================
# 4. sys.stdin / sys.stdout / sys.stderr
# ============================================================
print("\n" + "=" * 60)
print("4. sys.stdin / stdout / stderr - 标准流")
print("=" * 60)

# stdout 写入 (等价于 print)
sys.stdout.write("这是通过 sys.stdout.write() 输出的文本\n")

# stderr 写入 (错误输出, 通常是红色/单独管道)
sys.stderr.write("这是通过 sys.stderr.write() 输出的错误文本\n")

# stdin 读取 (这里展示对象的类型, 实际运行需交互)
print(f"\nsys.stdin  类型: {type(sys.stdin).__name__}")
print(f"sys.stdout 类型: {type(sys.stdout).__name__}")
print(f"sys.stderr 类型: {type(sys.stderr).__name__}")

print("\nsys.stdin 常用方法:")
print("  sys.stdin.read()    # 读取所有输入")
print("  sys.stdin.readline()  # 读取一行")
print("  sys.stdin.readlines() # 读取所有行到列表")

# ============================================================
# 5. 平台与版本信息
# ============================================================
print("\n" + "=" * 60)
print("5. 平台与版本信息")
print("=" * 60)

print(f"Python 版本:  {sys.version}")
print(f"版本号:       {sys.version_info}")
print(f"平台标识:     {sys.platform}")

# 判断操作系统
print("\n操作系统判断:")
if sys.platform.startswith('win'):
    print(f"  [OK] Windows 系统 (完整标识: {sys.platform})")
elif sys.platform.startswith('linux'):
    print(f"  [OK] Linux 系统")
elif sys.platform == 'darwin':
    print(f"  [OK] macOS 系统")

# Python 实现
print(f"\n解释器实现:  {sys.implementation}")
print(f"最大整数值:  {sys.maxsize}")
print(f"编码:        {sys.getdefaultencoding()}")

# ============================================================
# 6. 内省与运行时信息
# ============================================================
print("\n" + "=" * 60)
print("6. 内省与运行时信息")
print("=" * 60)

# getsizeof - 获取对象内存占用 (字节)
print("sys.getsizeof() - 对象内存大小:")
test_objects = {
    "整数 42": 42,
    "空字符串": "",
    "短字符串 'hello'": "hello",
    "空列表 []": [],
    "列表 [1,2,3]": [1, 2, 3],
    "空字典 {}": {},
    "字典 {a:1,b:2}": {"a": 1, "b": 2},
    "空元组 ()": (),
    "None": None,
    "True": True,
}
for name, obj in test_objects.items():
    size = sys.getsizeof(obj)
    print(f"  {name:<22} → {size:>4} 字节")

# 递归深度限制
rec_limit = sys.getrecursionlimit()
print(f"\n递归深度限制: {rec_limit}")

# 演示如何修改 (仅展示, 不实际修改)
print("修改方法: sys.setrecursionlimit(5000)")

# ============================================================
# 7. 其他实用属性
# ============================================================
print("\n" + "=" * 60)
print("7. 其他实用属性")
print("=" * 60)

# 已加载的模块
print(f"已加载模块数量: {len(sys.modules)}")
print("部分已加载模块:")
for name in list(sys.modules.keys())[:8]:
    print(f"  - {name}")

# 引用计数 (仅 CPython)
print(f"\ngetrefcount 演示:")
# sys.getrefcount 查看对象引用计数 (CPython)
a = []
print(f"  空列表引用计数: {sys.getrefcount(a)} (含getrefcount自身)")
b = a
print(f"  增加引用后:     {sys.getrefcount(a)}")

# 字节序
print(f"\n字节序: {sys.byteorder}")

# 模块搜索
print(f"\nexecutable: {sys.executable}")  # Python 解释器路径
print(f"prefix:     {sys.prefix}")        # Python 安装目录
