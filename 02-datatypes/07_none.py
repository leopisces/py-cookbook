"""
Python NoneType 与布尔值

学习目标：
  - None 的含义与使用场景
  - None 的比较方式 (is vs ==)
  - bool 类型与转换规则
  - truthy 与 falsy 值
  - 常见陷阱与最佳实践
"""

def main():
    # ========== 1. None 的基本概念 ==========
    print("=== 1. None 的基本概念 ===")

    # None 是 Python 的空值，表示"没有值"或"不存在"
    val = None
    print(f"None 的值: {val}")
    print(f"None 的类型: {type(val)}")
    print(f"None 的类型名: {type(val).__name__}")

    # None 是单例（singleton）— 全局只有一个 None 对象
    a = None
    b = None
    print(f"a is b: {a is b}")        # 同一个对象
    print(f"id(a) == id(b): {id(a) == id(b)}")

    # ========== 2. None 的比较 ==========
    print("\n=== 2. None 的比较 ===")

    # 【最佳实践】使用 is 比较 None（不要用 ==）
    x = None

    # ✅ 推荐写法
    if x is None:
        print("x is None (推荐写法)")

    # ✅ 也推荐
    if x is not None:
        pass

    # ⚠️ 可以但不推荐（== 可能被重载）
    if x == None:
        print("x == None (不推荐，== 可能被自定义类覆盖)")

    # ❌ 错误写法（赋值）
    # if x = None:  # SyntaxError!

    # ========== 3. None 的使用场景 ==========
    print("\n=== 3. None 的使用场景 ===")

    # 场景1: 函数默认参数（用 None 代替可变默认参数）
    def add_item(item, target=None):
        """安全地向列表添加元素"""
        if target is None:
            target = []            # 每次调用创建新列表
        target.append(item)
        return target

    list1 = add_item("a")
    list2 = add_item("b")
    print(f"list1: {list1}, list2: {list2} (互不影响)")

    # 场景2: 函数没有 return 语句时返回 None
    def no_return():
        print("  这个函数没有 return")

    result = no_return()
    print(f"无 return 函数的返回值: {result}")

    # 场景3: 字典中表示"键不存在"
    info = {"name": "Alice", "age": 25}
    print(f"get('phone'): {info.get('phone')}")
    print(f"get('phone', 'N/A'): {info.get('phone', 'N/A')}")

    # 场景4: 表示"未初始化"或"可选值"
    class Config:
        def __init__(self):
            self.debug_mode = None  # 尚未设置

    config = Config()
    if config.debug_mode is None:
        config.debug_mode = False   # 设置默认值
    print(f"debug_mode: {config.debug_mode}")

    # ========== 4. bool 类型 ==========
    print("\n=== 4. bool 类型 ===")

    # True 和 False 是 int 的子类
    print(f"True 的类型: {type(True)}")
    print(f"True == 1: {True == 1}")
    print(f"False == 0: {False == 0}")
    print(f"True + True: {True + True}")   # 2

    # bool 运算
    print(f"True and False: {True and False}")
    print(f"True or False: {True or False}")
    print(f"not True: {not True}")
    print(f"not False: {not False}")

    # ========== 5. truthy 与 falsy 值 ==========
    print("\n=== 5. truthy 与 falsy 值 ===")

    print("--- Falsy 值（转换为 False） ---")
    # 以下值在布尔上下文中被视为 False

    test_values = [
        ("None", None),
        ("False", False),
        ("0 (int)", 0),
        ("0.0 (float)", 0.0),
        ("0j (complex)", 0j),
        ("空字符串 ''", ""),
        ("空列表 []", []),
        ("空元组 ()", ()),
        ("空字典 {}", {}),
        ("空集合 set()", set()),
        ("空 range(0)", range(0)),
    ]

    for name, val in test_values:
        print(f"  bool({name:20s}) = {bool(val)}")

    print("\n--- Truthy 值（转换为 True） ---")
    # 除了上面的 falsy 值，其他所有值都是 truthy

    truthy_tests = [
        ("True", True),
        ("非零数字 42", 42),
        ("负数 -1", -1),
        ("非空字符串 '0'", "0"),
        ("非空列表 [0]", [0]),
        ("非空字典 {0: 0}", {0: 0}),
    ]

    for name, val in truthy_tests:
        print(f"  bool({name:18s}) = {bool(val)}")

    # ========== 6. 短路求值与实用性 ==========
    print("\n=== 6. 短路求值与实用性 ===")

    # or 运算符 — 返回第一个 truthy 值
    print("or 运算符 (取第一个真值):")
    print(f"  None or '默认值' = '{None or '默认值'}'")
    print(f"  0 or '' or 42 = {0 or '' or 42}")
    print(f"  '' or [] or 'hello' = '{'' or [] or 'hello'}'")

    # and 运算符 — 返回第一个 falsy 值或最后一个值
    print("\nand 运算符:")
    print(f"  True and 'result' = '{True and 'result'}'")
    print(f"  1 and 2 and 3 = {1 and 2 and 3}")
    print(f"  1 and 0 and 3 = {1 and 0 and 3}")

    # 实际应用: 设置默认值
    user_input = ""    # 模拟用户空输入
    name = user_input or "匿名用户"
    print(f"\n用户名: '{user_input}' -> 处理为: '{name}'")

    # 实际应用: 条件表达式简写
    enabled = True
    status = "开启" if enabled else "关闭"
    print(f"状态: {status}")

    # ========== 7. 常见陷阱 ==========
    print("\n=== 7. 常见陷阱 ===")

    # 陷阱1: None 与空容器的混淆
    def get_data_wrong():
        """错误示例: 不应该返回多种不同类型的'空'"""
        return None   # None ≠ []

    def get_data_right():
        """正确示例: 统一返回类型"""
        return []

    result = get_data_right()
    print(f"可以安全地 for 遍历: {[x for x in result]}")
    print("如果返回 None 会导致 TypeError: 'NoneType' is not iterable")

    # 陷阱2: 等价的 bool 值
    print(f"\nbool(0) == bool(0.0) == bool([]) == bool('') == bool(None) = "
          f"{bool(0) == bool(0.0) == bool([]) == bool('') == bool(None)}")
    print("它们的 bool 值相同，但各自的值不同！")

    # 陷阱3: is True / is False vs == True
    value = 1
    print(f"\n1 == True: {value == True}")    # True (类型转换后相等)
    print(f"1 is True: {value is True}")       # False (不是同一个对象)
    print("建议: 使用 == 比较布尔值，使用 is 比较 None")


if __name__ == "__main__":
    main()
