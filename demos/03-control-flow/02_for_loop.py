"""
for 循环 (For Loop)
===============================
Python for 循环: 遍历各种可迭代对象、range、enumerate、zip、
break/continue、for-else、嵌套循环。
参考: https://www.runoob.com/python3/python3-loop.html
"""

def demo_basic_for():
    """演示 1: for 循环遍历基本数据类型"""
    print("=" * 50)
    print("演示 1: for 循环遍历各种类型")
    print("=" * 50)

    # 遍历列表
    fruits = ["苹果", "香蕉", "橙子", "葡萄"]
    print("  遍历列表:", end=" ")
    for fruit in fruits:
        print(fruit, end=" ")
    print()

    # 遍历元组
    colors = ("红", "绿", "蓝")
    print("  遍历元组:", end=" ")
    for color in colors:
        print(color, end=" ")
    print()

    # 遍历字符串（逐个字符）
    text = "Python"
    print("  遍历字符串:", end=" ")
    for ch in text:
        print(ch, end=" ")
    print()

    # 遍历字典的键（默认）
    student = {"name": "张三", "age": 20, "grade": "A"}
    print("  遍历字典的键:", end=" ")
    for key in student:
        print(key, end=" ")
    print()

    # 遍历字典的值
    print("  遍历字典的值:", end=" ")
    for value in student.values():
        print(value, end=" ")
    print()

    # 同时遍历字典的键和值
    print("  遍历字典的键值对:", end=" ")
    for k, v in student.items():
        print(f"({k}:{v})", end=" ")
    print()

    # 遍历集合（无序）
    nums_set = {3, 1, 4, 1, 5, 9}
    print("  遍历集合:", end=" ")
    for num in nums_set:
        print(num, end=" ")
    print()


def demo_range():
    """演示 2: range() 函数"""
    print("\n" + "=" * 50)
    print("演示 2: range() 函数")
    print("=" * 50)

    # range(stop) — 从0开始到stop-1
    print("  range(5):", list(range(5)))

    # range(start, stop)
    print("  range(2, 7):", list(range(2, 7)))

    # range(start, stop, step)
    print("  range(0, 10, 2):", list(range(0, 10, 2)))

    # 倒序
    print("  range(10, 0, -1):", list(range(10, 0, -1)))

    # range 是惰性求值，不会生成完整列表，节省内存
    r = range(1000000)
    print(f"  range(1000000) 占用内存: {r.__sizeof__()} bytes (列表需要约 8000000 bytes)")


def demo_enumerate_and_zip():
    """演示 3: enumerate() 和 zip()"""
    print("\n" + "=" * 50)
    print("演示 3: enumerate() 和 zip()")
    print("=" * 50)

    # enumerate — 同时获取索引和值
    fruits = ["苹果", "香蕉", "橙子"]
    print("  enumerate 示例:")
    for index, fruit in enumerate(fruits):
        print(f"    第{index}个水果: {fruit}")

    # enumerate 可以指定起始索引
    print("  enumerate(..., start=1):")
    for index, fruit in enumerate(fruits, start=1):
        print(f"    第{index}个水果: {fruit}")

    # zip — 并行遍历多个可迭代对象
    names = ["张三", "李四", "王五"]
    ages = [20, 22, 21]
    cities = ["北京", "上海", "广州"]
    print("\n  zip 并行遍历:")
    for name, age, city in zip(names, ages, cities):
        print(f"    {name}, 年龄{age}, 来自{city}")

    # zip 严格模式 (Python 3.10+) — 长度不匹配时抛异常
    # for a, b in zip([1,2,3], [4,5], strict=True):  # ValueError


def demo_break_continue_else():
    """演示 4: break、continue 和 for-else"""
    print("\n" + "=" * 50)
    print("演示 4: break、continue 和 for-else")
    print("=" * 50)

    # break — 提前终止循环
    print("  break 示例: 找到第一个偶数就停止")
    nums = [1, 3, 7, 8, 9, 10]
    for num in nums:
        if num % 2 == 0:
            print(f"    找到第一个偶数: {num}, 停止循环")
            break
        print(f"    检查 {num}... (奇数，继续)")

    # continue — 跳过当前迭代
    print("\n  continue 示例: 只打印偶数")
    for num in range(1, 11):
        if num % 2 != 0:
            continue  # 奇数跳过
        print(f"    {num} ", end="")
    print()

    # for-else — 循环正常结束(没有break)时执行 else 块
    print("\n  for-else 示例 1: 正常结束")
    for num in range(3):
        print(f"    迭代 {num}")
    else:
        print("    [OK] 循环正常结束，执行 else 块")

    print("\n  for-else 示例 2: break 中断")
    for num in range(5):
        print(f"    迭代 {num}")
        if num == 2:
            print("    触发 break!")
            break
    else:
        print("    这行不会执行 (因为 break 中断了循环)")

    # 实用场景：查找元素
    print("\n  for-else 实用场景: 查找素数")
    target = 17
    for divisor in range(2, int(target ** 0.5) + 1):
        if target % divisor == 0:
            print(f"    {target} 不是素数，可被 {divisor} 整除")
            break
    else:
        print(f"    {target} 是素数!")


def demo_nested_loop():
    """演示 5: 嵌套循环"""
    print("\n" + "=" * 50)
    print("演示 5: 嵌套循环")
    print("=" * 50)

    # 九九乘法表
    print("  九九乘法表:")
    for i in range(1, 10):
        for j in range(1, i + 1):
            print(f"  {j}×{i}={i*j:2d}", end="")
        print()

    # 嵌套循环中的 break 只跳出内层循环
    print("\n  break 只跳出内层循环:")
    for i in range(3):
        for j in range(3):
            if j == 1:
                break  # 只跳出内层 for j
            print(f"    i={i}, j={j}", end=" | ")
        print()


# ========== 主程序入口 ==========
if __name__ == "__main__":
    demo_basic_for()
    demo_range()
    demo_enumerate_and_zip()
    demo_break_continue_else()
    demo_nested_loop()
    print("\n[OK] 所有 for 循环演示完成！")
