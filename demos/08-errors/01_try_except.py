"""
Python 错误处理 - try/except 基础模式

学习目标：
  - try / except / else / finally 完整异常处理
  - 常见异常类型及触发场景
  - assert 断言语句
  - 异常处理最佳实践
"""


def divide(a, b):
    """安全除法，使用 assert 确保除数不为零"""
    assert b != 0, "除数不能为0"
    return a / b


def main():
    # ========== 1. try / except 基本用法 ==========
    print("=" * 50)
    print("1. try / except 基本用法")
    print("=" * 50)

    # 捕获特定异常
    print("--- 捕获特定异常 ---")
    try:
        result = 10 / 0
    except ZeroDivisionError:
        print("  错误：除数不能为零！")

    # 捕获多个异常类型
    print("\n--- 捕获多个异常 ---")
    test_cases = ["123", "abc", "0"]
    for s in test_cases:
        try:
            result = 100 / int(s)
            print(f"  100 / {s} = {result}")
        except ZeroDivisionError:
            print(f"  100 / {s} → 除数不能为零")
        except ValueError:
            print(f"  100 / '{s}' → 无法转换为数字")

    # 获取异常对象（as）
    print("\n--- 获取异常对象 ---")
    try:
        # 注: 此导入必然失败，用于演示 ImportError 异常捕获
        import nonexistent_module
    except ImportError as e:
        print(f"  导入失败: {e}")
        print(f"  异常类型: {type(e).__name__}")

    # ========== 2. else 和 finally 子句 ==========
    print("\n" + "=" * 50)
    print("2. else 和 finally 子句")
    print("=" * 50)

    # else：try 没有异常时执行
    print("--- else 子句 ---")
    try:
        result = 10 / 2
    except ZeroDivisionError:
        print("  捕获到异常")
    else:
        print(f"  计算成功，结果: {result}")

    # finally：无论是否异常都执行（清理资源）
    print("\n--- finally 子句 ---")
    print("  情况1：正常退出")
    try:
        print("    try 块执行")
    finally:
        print("    finally 块执行（清理）")

    print("  情况2：异常退出")
    try:
        try:
            print("    try 块执行")
            raise RuntimeError("测试异常")
        finally:
            print("    finally 块执行（即使发生异常）")
    except RuntimeError:
        print("    外部 except 捕获了异常")

    # ========== 3. 常见异常类型 ==========
    print("\n" + "=" * 50)
    print("3. 常见异常类型")
    print("=" * 50)

    common_exceptions = [
        ("IndexError",        "列表索引越界",            lambda: [1, 2, 3][10]),
        ("KeyError",          "字典键不存在",             lambda: {}["nonexistent"]),
        ("TypeError",         "类型错误",                 lambda: "hello" + 5),
        ("AttributeError",    "属性不存在",               lambda: "abc".nonexistent),
        ("FileNotFoundError", "文件不存在",               lambda: open("不存在的文件.txt")),
        ("NameError",         "变量未定义",               lambda: undefined_var),  # noqa: F821
    ]

    for name, desc, func in common_exceptions:
        try:
            func()
            print(f"  {name}: 无异常（意外）")
        except ZeroDivisionError:
            pass
        except Exception as e:
            print(f"  {name} ({desc}): {e}")

    # ========== 4. assert 断言 ==========
    print("\n" + "=" * 50)
    print("4. assert 断言")
    print("=" * 50)

    # assert 用于调试，条件为 False 时抛出 AssertionError
    print(f"  10 / 2 = {divide(10, 2)}")

    try:
        divide(10, 0)
    except AssertionError as e:
        print(f"  断言失败: {e}")

    # assert 可以在运行时通过 -O 参数禁用
    print("\n  提示: python -O script.py 可以禁用所有 assert 语句")
    print("  assert 只用于调试，不要用于业务逻辑的数据校验")

    # ========== 5. 异常处理最佳实践 ==========
    print("\n" + "=" * 50)
    print("5. 异常处理最佳实践")
    print("=" * 50)

    tips = [
        "只捕获你能处理的异常，避免裸 except:",
        "使用具体的异常类型，不要用 except Exception 一刀切",
        "finally 用于释放资源（文件、连接、锁等）",
        "else 子句让 try 块更精简（只放可能异常的代码）",
        "自定义异常让错误信息更有意义",
        "使用 raise ... from ... 保留完整的错误上下文",
    ]
    for i, tip in enumerate(tips, 1):
        print(f"  {i}. {tip}")


if __name__ == "__main__":
    main()
