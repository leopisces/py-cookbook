"""
模块 - Python 模块化编程

学习目标：
  - import / from...import / as 的用法
  - 模块搜索路径 sys.path
  - 包的概念与 __init__.py
  - 相对导入与绝对导入
  - __all__ 控制导出内容
"""

import sys
import os
import tempfile
import importlib
import shutil


def main():
    # 注: 本函数中的 import 语句均为教学演示，
    # 展示 Python 导入机制的各种用法，并非 PEP 8 违规。
    # ========== 1. import 的多种方式 ==========
    print("=== 1. import 的多种方式 ===")

    # 方式一：import 模块名 —— 使用模块名.函数名() 调用
    import math
    print(f"import math -> math.sqrt(16) = {math.sqrt(16)}")

    # 方式二：from 模块 import 特定内容 —— 直接使用函数名
    from math import pi, sin
    print(f"from math import pi, sin -> pi = {pi}, sin(0) = {sin(0)}")

    # 方式三：import 模块 as 别名 —— 简化模块名
    import json as j
    data = j.dumps({"name": "Python", "version": 3.12})
    print(f"import json as j -> {data}")

    # 方式四：from 模块 import * —— 导入全部（不推荐，会污染命名空间）
    # from math import *  # 通常不推荐

    # 方式五：import 多个模块
    import os, sys, datetime
    now = datetime.datetime.now()
    print(f"当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}")

    # ========== 2. 模块搜索路径 sys.path ==========
    print("\n=== 2. 模块搜索路径 sys.path ===")

    print("Python 按以下顺序搜索模块:")
    for i, p in enumerate(sys.path[:5], 1):
        desc = ""
        if i == 1:
            desc = "（当前目录）"
        elif "site-packages" in p:
            desc = "（第三方包目录）"
        elif "python" in p.lower():
            desc = "（标准库目录）"
        print(f"  {i}. {p} {desc}")
    if len(sys.path) > 5:
        print(f"  ... 共 {len(sys.path)} 个路径")

    # ========== 3. 查看模块信息 ==========
    print("\n=== 3. 查看模块信息 ===")

    # dir() 查看模块导出的所有名称
    import re
    re_names = [n for n in dir(re) if not n.startswith("_")]
    print(f"re 模块公开的名称（前10个）: {re_names[:10]}")

    # 查看模块文件位置
    print(f"re 模块文件: {re.__file__}")

    # 查看模块文档字符串
    print(f"re 模块描述: {re.__doc__[:50].strip()}...")

    # ========== 4. 包与 __init__.py 概念 ==========
    print("\n=== 4. 包与 __init__.py 概念 ===")
    print("包（Package）是一个包含 __init__.py 的目录。")
    print("Python 3.3+ 支持隐式命名空间包（Namespace Package），")
    print("但传统包仍需 __init__.py。")

    # 演示：临时创建一个包结构
    tmp_dir = tempfile.mkdtemp(prefix="py_demo_pkg_")
    try:
        pkg_dir = os.path.join(tmp_dir, "mypackage")
        os.makedirs(pkg_dir)

        # 创建 __init__.py
        with open(os.path.join(pkg_dir, "__init__.py"), "w", encoding="utf-8") as f:
            f.write('''"""
演示包: mypackage
__init__.py 在包导入时自动执行
"""

# __all__ 控制 from package import * 导出的内容
__all__ = ["hello", "PI"]

PI = 3.14159

def hello(name="World"):
    """包级别的函数"""
    return f"Hello, {name} from mypackage!"

print("[mypackage 已初始化]")  # 导入包时会打印这行
''')

        # 创建子模块
        with open(os.path.join(pkg_dir, "utils.py"), "w", encoding="utf-8") as f:
            f.write('''
"""mypackage.utils 子模块"""

def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

# 模块级别的代码在首次 import 时执行
print("  [utils 子模块已加载]")
''')

        # 添加到 sys.path 以便导入
        if tmp_dir not in sys.path:
            sys.path.insert(0, tmp_dir)

        # 导入包
        import mypackage
        print(f"PI = {mypackage.PI}")
        print(f"hello() = {mypackage.hello('Python')}")

        # 导入子模块
        from mypackage import utils
        print(f"utils.add(3, 4) = {utils.add(3, 4)}")
        print(f"utils.multiply(5, 6) = {utils.multiply(5, 6)}")

        # __all__ 的作用
        print(f"__all__ 控制导出: {mypackage.__all__}")

    finally:
        # 清理临时文件和 sys.path
        if tmp_dir in sys.path:
            sys.path.remove(tmp_dir)
        if "mypackage" in sys.modules:
            del sys.modules["mypackage"]
        if "mypackage.utils" in sys.modules:
            del sys.modules["mypackage.utils"]
        shutil.rmtree(tmp_dir, ignore_errors=True)

    # ========== 5. 绝对导入 vs 相对导入 ==========
    print("\n=== 5. 绝对导入 vs 相对导入 ===")

    print("绝对导入（Absolute Import）：")
    print("  从项目根目录开始的完整路径")
    print("  from mypackage.utils import add")
    print("  import os.path  # 标准库也是绝对导入")
    print()
    print("相对导入（Relative Import）：")
    print("  使用 . 表示当前包，.. 表示上级包")
    print("  from . import sibling_module   # 同包内导入")
    print("  from ..parent_pkg import func  # 上级包导入")
    print()
    print("注意：相对导入只能用在包内部，不能直接在顶层脚本中使用。")

    # 实际演示：os.path 的导入链
    print(f"os.path 是一个模块: {type(os.path).__name__}")
    print(f"os.path.join('a', 'b') = {os.path.join('a', 'b')}")

    # ========== 6. 模块缓存与重载 ==========
    print("\n=== 6. 模块缓存与重载 ===")

    # 模块只导入一次，缓存在 sys.modules 中
    print(f"已加载的模块数量: {len(sys.modules)}")
    # 查看几个已加载的模块
    loaded = list(sys.modules.keys())
    common = [m for m in loaded if m in ("os", "sys", "math", "json", "re")]
    print(f"已缓存的常用模块: {common}")

    # 如需重新加载模块（开发调试时常用）
    import json
    importlib.reload(json)  # 强制重新加载
    print("已使用 importlib.reload(json) 重新加载 json 模块")

    # ========== 7. 模块搜索路径的动态修改 ==========
    print("\n=== 7. 动态添加搜索路径 ===")
    # PYTHONPATH 环境变量的作用
    pythonpath = os.environ.get("PYTHONPATH", "(未设置)")
    print(f"PYTHONPATH 环境变量: {pythonpath}")
    print("可以通过以下方式添加搜索路径：")
    print("  1. sys.path.append('/your/path')")
    print("  2. 设置 PYTHONPATH 环境变量")
    print("  3. 将模块放在 site-packages 目录")


if __name__ == "__main__":
    main()
