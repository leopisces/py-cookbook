"""
__name__ 属性 - 模块运行模式判断

学习目标：
  - __name__ 的作用与含义
  - if __name__ == "__main__" 判断
  - 模块测试代码的编写方式
  - 实际应用场景
"""

import sys
import os


# ========== 0. __name__ 属性说明（写在函数外以便展示） ==========
# 当脚本直接运行时，__name__ = "__main__"
# 当脚本被 import 时，__name__ = 模块文件名（不含 .py）


def demo_function():
    """一个普通函数，供测试代码调用"""
    return "demo_function 被调用了"


def main():
    # ========== 1. __name__ 的值取决于运行方式 ==========
    print("=== 1. __name__ 的值 ===")
    print(f"当前 __name__ 的值: '{__name__}'")
    print("如果直接运行此文件: __name__ == '__main__'")
    print("如果被 import 导入:   __name__ == '模块名'")

    # ========== 2. __main__ 判断的作用 ==========
    print("\n=== 2. if __name__ == '__main__' 的作用 ===")
    print("这个判断用来区分：直接运行 还是 被导入")
    print()
    print("当脚本被 import 时：")
    print("  模块顶层的代码会执行（定义函数、类等）")
    print("  但 __name__ != '__main__'，测试代码不会执行")
    print()
    print("当脚本直接运行时：")
    print("  __name__ == '__main__'，测试/演示代码会执行")

    # ========== 3. 模块测试代码模式 ==========
    print("\n=== 3. 模块测试代码的典型模式 ===")

    # 演示：这个模块也可以被导入使用
    print(f"调用 demo_function(): {demo_function()}")
    print("如果本文件被其他脚本 import，上面的代码在 main() 里不会执行")

    # ========== 4. 模拟：查看被导入时的行为 ==========
    print("\n=== 4. 模拟被导入时的行为 ===")

    # 使用 importlib 导入自己，观察 __name__ 的变化
    # 注: 此处导入用于演示模块自我导入行为与 __name__ 属性
    import importlib.util

    # 获取当前文件路径
    current_file = os.path.abspath(__file__)

    # 创建一个规格并加载为模块
    spec = importlib.util.spec_from_file_location(
        "demo_imported_module", current_file
    )
    if spec is not None:
        imported_module = importlib.util.module_from_spec(spec)
        # 模拟被导入时的 __name__ 值
        print(f"被导入前临时模块的 __name__: {imported_module.__name__}")
        print("注意：被导入时 __name__ 是 'demo_imported_module'（模块名），")
        print("而不是 '__main__'，因此 if 判断中的代码不会执行。")

    # ========== 5. 实际应用场景 ==========
    print("\n=== 5. 实际应用场景 ===")

    print("场景 1：编写可复用库")
    print("  将核心逻辑放在函数/类中，测试代码放在 if __name__ 块里")
    print()
    print("场景 2：命令行入口脚本")
    print("  if __name__ == '__main__':")
    print("      sys.exit(main())")
    print()
    print("场景 3：单元测试（简单方式）")
    print("  if __name__ == '__main__':")
    print("      test_function1()")
    print("      test_function2()")
    print("      print('所有测试通过')")

    # ========== 6. 传递命令行参数 ==========
    print("\n=== 6. 在 __main__ 中处理命令行参数 ===")
    print(f"命令行参数列表: {sys.argv}")
    if len(sys.argv) > 1:
        print(f"接收到的参数: {sys.argv[1:]}")
    else:
        print("没有额外的命令行参数（可以试试 python 02_name_main.py arg1 arg2）")

    # ========== 7. 查看标准库中的 __main__ 用法 ==========
    print("\n=== 7. 标准库中的 __main__ 用法示例 ===")
    print("很多标准库模块都可以直接运行，例如：")
    print("  python -m http.server    # 启动 HTTP 服务器")
    print("  python -m json.tool      # JSON 格式化工具")
    print("  python -m calendar 2026  # 显示日历")


# 模块顶层代码（无论直接运行还是被导入都会执行）
print(f"[模块加载] 02_name_main.py 的 __name__ = '{__name__}'")


if __name__ == "__main__":
    main()
