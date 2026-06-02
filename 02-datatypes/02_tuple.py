"""
Python 元组 (Tuple)

学习目标：
  - 元组的创建与基本操作
  - 不可变特性及其意义
  - 单元素元组的特殊语法
  - 元组解包（unpacking）
  - 元组与列表互转
  - 元组的应用场景
"""

from collections import namedtuple


def main():
    # ========== 1. 元组的创建 ==========
    print("=== 1. 元组的创建 ===")

    # 多种创建方式
    t1 = ()                         # 空元组
    t2 = (1, 2, 3)                 # 标准语法
    t3 = 4, 5, 6                   # 可以省略括号（打包）
    t4 = (7,)                      # 单元素元组（必须有逗号！）
    t5 = tuple([10, 20, 30])       # 从列表创建
    t6 = tuple("abc")              # 从字符串创建

    print(f"空元组: {t1}")
    print(f"标准创建: {t2}")
    print(f"省略括号: {t3}")
    print(f"单元素: {t4}")
    print(f"从列表创建: {t5}")
    print(f"从字符串创建: {t6}")

    # 单元素注意
    not_a_tuple = (42)             # 这只是一个带括号的整数！
    is_a_tuple = (42,)             # 这才是元组
    print(f"\n(42) 类型: {type(not_a_tuple).__name__}")    # int
    print(f"(42,) 类型: {type(is_a_tuple).__name__}")       # tuple

    # ========== 2. 索引与切片 ==========
    print("\n=== 2. 索引与切片 ===")

    fruits = ("苹果", "香蕉", "橘子", "葡萄", "西瓜")
    print(f"元组: {fruits}")
    print(f"长度: {len(fruits)}")

    # 索引操作（与列表一样）
    print(f"fruits[0]  = {fruits[0]}")
    print(f"fruits[-1] = {fruits[-1]}")
    print(f"fruits[1:4] = {fruits[1:4]}")
    print(f"fruits[::2] = {fruits[::2]}")

    # ========== 3. 不可变特性 ==========
    print("\n=== 3. 不可变特性 ===")

    t = (1, 2, [3, 4], "hello")

    # 元组本身不可变 — 不能增删改元素
    print(f"元组: {t}")

    # 以下操作会报错（已注释）：
    # t[0] = 10      # TypeError: 'tuple' object does not support item assignment
    # t.append(5)    # AttributeError: 'tuple' object has no attribute 'append'
    # del t[1]       # TypeError: 'tuple' object doesn't support item deletion

    # 但是！元组内可变元素的内部可以修改
    print(f"修改前 t[2] = {t[2]}")
    t[2].append(5)
    t[2][0] = 999
    print(f"修改后 t[2] = {t[2]}")
    print(f"元组不变，但内部列表变了: {t}")

    # 元组的优势：
    # 1. 更安全 — 防止意外修改
    # 2. 更高效 — 内存占用更小
    # 3. 可作为字典的键（列表不可以）

    # ========== 4. 元组解包 ==========
    print("\n=== 4. 元组解包 (unpacking) ===")

    # 基本解包
    point = (10, 20, 30)
    x, y, z = point
    print(f"解包 ({point}): x={x}, y={y}, z={z}")

    # 交换变量（元组打包与解包的妙用）
    a, b = 1, 2
    print(f"交换前: a={a}, b={b}")
    a, b = b, a    # 实际上是 (a, b) = (b, a)
    print(f"交换后: a={a}, b={b}")

    # 使用 * 收集剩余元素
    first, *middle, last = [10, 20, 30, 40, 50]
    print(f"first={first}, middle={middle}, last={last}")

    # 交换多个变量
    colors = ("红", "绿", "蓝")
    r, g, b = colors
    print(f"颜色: 红={r}, 绿={g}, 蓝={b}")

    # ========== 5. 元组常用操作 ==========
    print("\n=== 5. 元组常用操作 ===")

    t = (1, 2, 3, 2, 4, 2)

    # 计数与查找
    print(f"元组: {t}")
    print(f"count(2): 2 出现了 {t.count(2)} 次")
    print(f"index(3): 3 在索引 {t.index(3)} 处")

    # 成员检查
    print(f"2 in t: {2 in t}")
    print(f"99 in t: {99 in t}")

    # 连接与重复
    t1 = (1, 2)
    t2 = (3, 4)
    print(f"连接 t1 + t2 = {t1 + t2}")
    print(f"重复 t1 * 3 = {t1 * 3}")

    # 遍历
    print("遍历元组:", end=" ")
    for item in (10, 20, 30):
        print(item, end=" ")
    print()

    # ========== 6. 元组与列表互转 ==========
    print("\n=== 6. 元组与列表互转 ===")

    original_tuple = (1, 2, 3)
    print(f"原始元组: {original_tuple}")

    # 元组 → 列表 → 修改 → 元组
    temp_list = list(original_tuple)
    temp_list.append(4)
    new_tuple = tuple(temp_list)
    print(f"转换修改后: {new_tuple}")

    # 列表 → 元组 → 列表
    original_list = [5, 6, 7, 8]
    print(f"原始列表: {original_list}")
    temp_tuple = tuple(original_list)
    new_list = list(temp_tuple)
    print(f"转一圈回来: {new_list}")

    # ========== 7. 元组的应用场景 ==========
    print("\n=== 7. 元组的应用场景 ===")

    # 场景1: 函数返回多个值（实际上是返回一个元组）
    def get_min_max(numbers):
        return min(numbers), max(numbers)  # 返回元组

    result = get_min_max([3, 1, 4, 1, 5])
    print(f"返回多值: min={result[0]}, max={result[1]}")

    # 场景2: 作为字典的键
    locations = {
        (0, 0): "原点",
        (1, 0): "右侧",
        (0, 1): "上方",
    }
    print(f"坐标字典: {locations}")
    print(f"坐标 (1, 0) 是: {locations[(1, 0)]}")

    # 场景3: 命名元组（更可读的轻量数据结构）
    Student = namedtuple("Student", ["name", "age", "score"])
    alice = Student("Alice", 20, 95)
    print(f"\n命名元组: {alice}")
    print(f"姓名: {alice.name}, 年龄: {alice.age}, 成绩: {alice.score}")


if __name__ == "__main__":
    main()
