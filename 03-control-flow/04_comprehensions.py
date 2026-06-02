"""
推导式 (Comprehensions)
===============================
Python 推导式: 列表推导式、字典推导式、集合推导式、
生成器表达式、嵌套推导式、条件推导式。
参考: https://www.runoob.com/python3/python-comprehensions.html
"""

import sys


def demo_list_comprehension():
    """演示 1: 列表推导式 (List Comprehension)"""
    print("=" * 50)
    print("演示 1: 列表推导式")
    print("=" * 50)

    # 基本语法: [表达式 for 变量 in 可迭代对象]

    # 传统 for 循环方式
    squares_traditional = []
    for x in range(1, 6):
        squares_traditional.append(x ** 2)
    print(f"  传统方式: {squares_traditional}")

    # 列表推导式 — 一行搞定
    squares = [x ** 2 for x in range(1, 6)]
    print(f"  推导式:   {squares}")

    # 对字符串操作
    words = ["hello", "world", "python"]
    upper_words = [w.upper() for w in words]
    print(f"  转大写:    {upper_words}")

    # 数学运算
    doubles = [n * 2 for n in range(1, 6)]
    print(f"  翻倍:      {doubles}")

    # 类型转换
    str_nums = [str(n) for n in range(1, 6)]
    print(f"  转字符串:  {str_nums}")


def demo_comprehension_with_condition():
    """演示 2: 带条件的推导式"""
    print("\n" + "=" * 50)
    print("演示 2: 带条件的推导式")
    print("=" * 50)

    # 带 if 过滤: [表达式 for 变量 in 可迭代对象 if 条件]
    evens = [x for x in range(1, 11) if x % 2 == 0]
    print(f"  1~10 中的偶数:    {evens}")

    # 带 if-else 的三元: [表达式1 if 条件 else 表达式2 for 变量 in 可迭代对象]
    # 注意: if-else 在 for 前面，if 过滤在 for 后面
    parity = ["偶数" if x % 2 == 0 else "奇数" for x in range(1, 6)]
    print(f"  奇偶判断:         {parity}")

    # 多个 if 条件 (等价于 and)
    nums = [x for x in range(1, 31) if x % 2 == 0 if x % 3 == 0]
    print(f"  1~30 中能被 2 和 3 整除的数: {nums}")

    # 字符串过滤
    words = ["apple", "banana", "cherry", "date", "elderberry"]
    long_words = [w for w in words if len(w) > 5]
    print(f"  长度>5的单词:     {long_words}")

    # 条件过滤的同时做转换
    squared_evens = [x ** 2 for x in range(1, 11) if x % 2 == 0]
    print(f"  偶数的平方:       {squared_evens}")


def demo_dict_and_set_comprehension():
    """演示 3: 字典推导式与集合推导式"""
    print("\n" + "=" * 50)
    print("演示 3: 字典推导式与集合推导式")
    print("=" * 50)

    # 字典推导式: {键表达式: 值表达式 for 变量 in 可迭代对象}
    # 创建数字 -> 平方的映射
    square_map = {x: x ** 2 for x in range(1, 6)}
    print(f"  数字->平方:  {square_map}")

    # 创建字符串->长度的映射
    words = ["apple", "banana", "cherry"]
    word_len = {w: len(w) for w in words}
    print(f"  单词->长度:  {word_len}")

    # 反转字典的键值对
    original = {"a": 1, "b": 2, "c": 3}
    reversed_dict = {v: k for k, v in original.items()}
    print(f"  反转字典:   {reversed_dict}")

    # 带条件的字典推导式
    even_squares = {x: x ** 2 for x in range(1, 11) if x % 2 == 0}
    print(f"  偶数的平方字典: {even_squares}")

    # 集合推导式: {表达式 for 变量 in 可迭代对象 if 条件}
    # 创建平方数集合 (自动去重)
    squares_set = {x ** 2 for x in range(-5, 6)}
    print(f"\n  平方数集合(自动去重): {sorted(squares_set)}")

    # 字符串去重、转小写
    text = "Hello World"
    unique_chars = {c.lower() for c in text if c.isalpha()}
    print(f"  字符串字符去重: {sorted(unique_chars)}")

    # 找出列表中所有不同长度的单词
    words = ["hi", "hello", "hey", "hi", "world", "hello"]
    unique_lengths = {len(w) for w in words}
    print(f"  单词唯一长度集合: {unique_lengths}")


def demo_generator_expression():
    """演示 4: 生成器表达式"""
    print("\n" + "=" * 50)
    print("演示 4: 生成器表达式")
    print("=" * 50)

    # 生成器表达式: (表达式 for 变量 in 可迭代对象)
    # 使用圆括号，惰性求值，节省内存

    # 列表推导式 — 立即生成完整列表
    squares_list = [x ** 2 for x in range(10)]
    print(f"  列表推导式结果: {squares_list}")
    print(f"  列表推导式类型: {type(squares_list)}")

    # 生成器表达式 — 惰性求值
    squares_gen = (x ** 2 for x in range(10))
    print(f"\n  生成器表达式类型: {type(squares_gen)}")
    print(f"  逐个获取生成器值:", end=" ")
    for val in squares_gen:
        print(val, end=" ")
    print()

    # 生成器表达式只能迭代一次
    squares_gen = (x ** 2 for x in range(3))
    print(f"\n  第一次遍历:", list(squares_gen))
    print(f"  第二次遍历(空了): {list(squares_gen)}")

    # 生成器表达式可以直接作为函数参数（单参数时省略外层括号）
    total = sum(x ** 2 for x in range(1, 11))
    print(f"\n  sum(x**2 for x in range(1,11)) = {total}")

    # 内存对比
    list_comp = [x for x in range(1000000)]
    gen_expr = (x for x in range(1000000))
    print(f"\n  内存占用对比:")
    print(f"    列表推导式: ~{sys.getsizeof(list_comp):,} bytes")
    print(f"    生成器表达式: ~{sys.getsizeof(gen_expr):,} bytes")


def demo_nested_comprehension():
    """演示 5: 嵌套推导式"""
    print("\n" + "=" * 50)
    print("演示 5: 嵌套推导式")
    print("=" * 50)

    # 嵌套列表推导式: 展开二维列表 (flatten)
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    # 传统方式
    flat_traditional = []
    for row in matrix:
        for item in row:
            flat_traditional.append(item)
    print(f"  传统展开: {flat_traditional}")

    # 推导式: for 从左到右对应从外到内
    flat = [item for row in matrix for item in row]
    print(f"  推导式展开: {flat}")

    # 矩阵转置
    print(f"\n  原始矩阵:")
    for row in matrix:
        print(f"    {row}")
    transposed = [[row[i] for row in matrix] for i in range(3)]
    print(f"  转置矩阵:")
    for row in transposed:
        print(f"    {row}")

    # 嵌套字典推导式
    print(f"\n  嵌套字典推导: 创建二维映射")
    coord_map = {(x, y): x * y for x in range(1, 4) for y in range(1, 4)}
    for k, v in sorted(coord_map.items()):
        print(f"    坐标{k} = {v}")

    # 带条件的嵌套推导
    print(f"\n  带条件的嵌套推导: 只取偶数值")
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    flat_evens = [item for row in matrix for item in row if item % 2 == 0]
    print(f"    二维矩阵中的偶数: {flat_evens}")


# ========== 主程序入口 ==========
if __name__ == "__main__":
    demo_list_comprehension()
    demo_comprehension_with_condition()
    demo_dict_and_set_comprehension()
    demo_generator_expression()
    demo_nested_comprehension()
    print("\n[OK] 所有推导式演示完成！")

# ============================================================
# 相关主题:
#   - 04-functions/04_iterator_generator.py  → 生成器表达式与惰性求值
# ============================================================
