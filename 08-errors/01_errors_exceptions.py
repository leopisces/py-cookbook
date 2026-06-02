"""
错误与异常 - Python 异常处理机制

学习目标：
  - try / except / else / finally 完整异常处理
  - 常见异常类型及触发场景
  - 自定义异常类
  - 异常链（raise ... from ...）
  - assert 断言语句
"""

import traceback


def main():
    # ========== 1. try / except 基本用法 ==========
    print("=== 1. try / except 基本用法 ===")

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
        import nonexistent_module
    except ImportError as e:
        print(f"  导入失败: {e}")
        print(f"  异常类型: {type(e).__name__}")

    # ========== 2. else 和 finally 子句 ==========
    print("\n=== 2. else 和 finally 子句 ===")

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
    print("\n=== 3. 常见异常类型 ===")

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

    # ========== 4. 自定义异常 ==========
    print("\n=== 4. 自定义异常 ===")

    class ValidationError(Exception):
        """自定义验证异常"""
        def __init__(self, field, value, message="验证失败"):
            self.field = field
            self.value = value
            self.message = f"{message}: 字段 '{field}' 的值 '{value}' 不合法"
            super().__init__(self.message)

    class BusinessError(Exception):
        """自定义业务异常（带错误码）"""
        def __init__(self, code, message):
            self.code = code
            self.message = message
            super().__init__(f"[{code}] {message}")

    # 使用自定义异常
    def validate_age(age):
        if not isinstance(age, int):
            raise ValidationError("age", age, "类型错误")
        if age < 0 or age > 150:
            raise ValidationError("age", age, "范围错误")
        return age

    # 测试
    test_ages = [25, -5, "abc"]
    for age in test_ages:
        try:
            valid = validate_age(age)
            print(f"  年龄 {valid} 验证通过")
        except ValidationError as e:
            print(f"  {e}")

    # 业务异常
    def transfer_money(amount, balance):
        if amount <= 0:
            raise BusinessError("E001", "转账金额必须大于0")
        if amount > balance:
            raise BusinessError("E002", f"余额不足（余额: {balance}, 需要: {amount}）")
        return balance - amount

    print()
    try:
        transfer_money(500, 300)
    except BusinessError as e:
        print(f"  {e.message}")

    # ========== 5. 异常链：raise ... from ... ==========
    print("\n=== 5. 异常链：raise ... from ... ===")

    class DataError(Exception):
        """数据层异常"""
        pass

    class ServiceError(Exception):
        """服务层异常"""
        pass

    def load_data():
        """底层函数可能抛出原始异常"""
        raise DataError("数据库连接超时")

    def process_data():
        """上层函数捕获并转换为业务异常"""
        try:
            load_data()
        except DataError as e:
            # raise ... from ... 保留原始异常链
            raise ServiceError("数据处理失败") from e

    try:
        process_data()
    except ServiceError as e:
        print(f"  捕获到: {e}")
        print(f"  原始异常: {e.__cause__}")
        print(f"  异常链: {type(e).__name__} -> {type(e.__cause__).__name__}")

    # raise ... from None 可以切断异常链
    print("\n--- from None 切断异常链 ---")
    try:
        try:
            raise ValueError("内部错误")
        except ValueError:
            raise RuntimeError("外部错误") from None
    except RuntimeError as e:
        print(f"  捕获: {e}")
        print(f"  原始异常: {e.__cause__}")  # None

    # ========== 6. assert 断言 ==========
    print("\n=== 6. assert 断言 ===")

    # assert 用于调试，条件为 False 时抛出 AssertionError
    def divide(a, b):
        assert b != 0, "除数不能为0"
        return a / b

    print(f"  10 / 2 = {divide(10, 2)}")

    try:
        divide(10, 0)
    except AssertionError as e:
        print(f"  断言失败: {e}")

    # assert 可以在运行时通过 -O 参数禁用
    print("\n  提示: python -O script.py 可以禁用所有 assert 语句")
    print("  assert 只用于调试，不要用于业务逻辑的数据校验")

    # ========== 7. 异常处理最佳实践 ==========
    print("\n=== 7. 异常处理最佳实践 ===")

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
