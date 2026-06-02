"""
Python 数据类型转换

学习目标：
  - int() 整数转换
  - float() 浮点数转换
  - str() 字符串转换
  - bool() 布尔转换
  - list(), tuple(), set(), dict() 等容器类型转换
  - 类型转换的注意事项与陷阱
"""

def main():
    # ========== 1. 整数转换 int() ==========
    print("=== 1. int() 整数转换 ===")

    # 浮点数 → 整数（直接截断，不四舍五入）
    print(f"int(3.14) = {int(3.14)}")
    print(f"int(9.99) = {int(9.99)}")
    print(f"int(-3.14) = {int(-3.14)}")

    # 字符串 → 整数
    print(f'int("42") = {int("42")}')
    print(f'int("-100") = {int("-100")}')

    # 指定进制的字符串转换
    print(f'int("1010", 2) = {int("1010", 2)}')    # 二进制 → 10
    print(f'int("FF", 16) = {int("FF", 16)}')       # 十六进制 → 255
    print(f'int("77", 8) = {int("77", 8)}')         # 八进制 → 63

    # bool → int
    print(f"int(True) = {int(True)}, int(False) = {int(False)}")

    # ========== 2. 浮点数转换 float() ==========
    print("\n=== 2. float() 浮点数转换 ===")

    print(f"float(10) = {float(10)}")
    print(f'float("3.14") = {float("3.14")}')
    print(f'float("-2.5") = {float("-2.5")}')
    print(f'float("1e3") = {float("1e3")}')         # 科学计数法

    # ========== 3. 字符串转换 str() ==========
    print("\n=== 3. str() 字符串转换 ===")

    print(f'str(42) = "{str(42)}"')
    print(f'str(3.14) = "{str(3.14)}"')
    print(f'str(True) = "{str(True)}"')
    print(f'str(None) = "{str(None)}"')
    print(f'str([1, 2, 3]) = "{str([1, 2, 3])}"')

    # ========== 4. 布尔转换 bool() ==========
    print("\n=== 4. bool() 布尔转换 ===")

    # Falsy 值（转换为 False）
    print(f"bool(0) = {bool(0)}")            # 零值 → False
    print(f"bool(0.0) = {bool(0.0)}")        # 零浮点 → False
    print(f"bool('') = {bool('')}")          # 空字符串 → False
    print(f"bool([]) = {bool([])}")          # 空列表 → False
    print(f"bool(()) = {bool(())}")          # 空元组 → False
    print(f"bool({{}}) = {bool({})}")        # 空字典 → False
    print(f"bool(set()) = {bool(set())}")    # 空集合 → False
    print(f"bool(None) = {bool(None)}")      # None → False

    # Truthy 值（转换为 True）
    print(f"bool(42) = {bool(42)}")          # 非零值 → True
    print(f"bool(-1) = {bool(-1)}")          # 负数 → True
    print(f"bool('hello') = {bool('hello')}") # 非空字符串 → True

    # ========== 5. 容器类型转换 ==========
    print("\n=== 5. 容器类型转换 ===")

    # list() — 转换为列表
    tup = (1, 2, 3)
    print(f"tuple → list: list({tup}) = {list(tup)}")
    print(f"str → list: list('abc') = {list('abc')}")     # 每个字符一个元素
    print(f"range → list: list(range(5)) = {list(range(5))}")

    # tuple() — 转换为元组
    lst = [4, 5, 6]
    print(f"list → tuple: tuple({lst}) = {tuple(lst)}")

    # set() — 转换为集合（自动去重）
    dup_list = [1, 2, 2, 3, 3, 3]
    print(f"list → set (去重): set({dup_list}) = {set(dup_list)}")
    print(f"str → set: set('hello') = {set('hello')}")     # 字符去重

    # dict() — 转换为字典
    # 从键值对列表创建
    pairs = [("name", "Alice"), ("age", 25)]
    print(f"键值对列表→字典: dict({pairs}) = {dict(pairs)}")
    # 从关键字参数创建
    print(f"关键字→字典: dict(a=1, b=2) = {dict(a=1, b=2)}")

    # ========== 6. 综合转换示例 ==========
    print("\n=== 6. 综合转换示例 ===")

    # 从用户输入到计算（模拟）
    user_input = "3.14"
    # 字符串 → 浮点数 → 计算
    radius = float(user_input)
    area = 3.14159 * radius ** 2
    # 浮点数 → 字符串 → 格式化显示
    result = f"半径为 {user_input} 的圆面积约为 {area:.2f}"
    print(result)

    # 类型检查
    val = 42
    print(f"\nval = {val}, 类型: {type(val).__name__}")
    print(f"isinstance(val, int): {isinstance(val, int)}")
    print(f"isinstance(val, (int, float)): {isinstance(val, (int, float))}")

    print("\n注意: 类型转换可能失败，如 int('abc') 会抛 ValueError")


if __name__ == "__main__":
    main()
