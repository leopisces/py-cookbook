"""
while 循环 (While Loop)
===============================
Python while 循环: 基本用法、死循环与break、
while-else、嵌套循环、while 与 for 的选择。
参考: https://www.runoob.com/python3/python3-loop.html
"""

def demo_basic_while():
    """演示 1: while 循环基本用法"""
    print("=" * 50)
    print("演示 1: while 循环基本用法")
    print("=" * 50)

    # 基本 while — 条件为 True 时不断执行
    count = 1
    print("  基本 while 循环:")
    while count <= 5:
        print(f"    第 {count} 次循环")
        count += 1  # 别忘了递增条件变量，否则会死循环！

    # while 结合列表
    print("\n  用 while 遍历列表:")
    fruits = ["苹果", "香蕉", "橙子"]
    i = 0
    while i < len(fruits):
        print(f"    fruits[{i}] = {fruits[i]}")
        i += 1

    # while 循环计算累加和
    print("\n  计算 1+2+...+100:")
    total = 0
    n = 1
    while n <= 100:
        total += n
        n += 1
    print(f"    累加和(1~100) = {total}")


def demo_infinite_and_break():
    """演示 2: 死循环与 break 退出"""
    print("\n" + "=" * 50)
    print("演示 2: 死循环与 break")
    print("=" * 50)

    # while True — 常与 break 配合
    print("  死循环 + break 示例:")
    attempts = 0
    while True:
        attempts += 1
        print(f"    尝试第 {attempts} 次...", end=" ")
        # 模拟某些条件达成后退出
        if attempts >= 3:
            print("条件达成，退出循环！")
            break
        print("条件未达成，继续")

    # 实用场景：用户输入验证的模拟
    print("\n  模拟输入验证 (用 break 退出):")
    valid_options = ["y", "yes"]
    attempts = 0
    while True:
        attempts += 1
        # 模拟用户输入
        simulated_input = "yes" if attempts > 1 else "n"
        print(f"    第{attempts}次尝试: 用户输入 '{simulated_input}'")
        if simulated_input in valid_options:
            print(f"    [OK] 输入有效，退出循环")
            break
        if attempts >= 3:
            print(f"    [X] 尝试次数过多，退出")
            break
        print(f"    [!] 输入无效，请重试")


def demo_while_else():
    """演示 3: while-else 语句"""
    print("\n" + "=" * 50)
    print("演示 3: while-else 语句")
    print("=" * 50)

    # while-else: 当条件变为 False 正常退出时执行 else
    print("  示例 1: 正常退出 -> else 执行")
    count = 3
    while count > 0:
        print(f"    倒计时: {count}")
        count -= 1
    else:
        print("    >> 发射! (条件自然变为 False，else 执行)")

    # break 退出时 else 不执行
    print("\n  示例 2: break 退出 -> else 不执行")
    count = 3
    while count > 0:
        print(f"    倒计时: {count}")
        count -= 1
        if count == 1:
            print("    [STOP] 紧急中止!")
            break
    else:
        print("    (这行不会执行)")

    # 实用场景：密码重试
    print("\n  实用场景: 密码重试模拟")
    max_retries = 3
    retry_count = 0
    while retry_count < max_retries:
        retry_count += 1
        # 模拟密码输入
        input_password = "123456" if retry_count >= 3 else "wrong"
        print(f"    第{retry_count}次输入: '{input_password}'")
        if input_password == "123456":
            print(f"    [OK] 登录成功!")
            break
        print(f"    密码错误，剩余尝试次数: {max_retries - retry_count}")
    else:
        print(f"    [X] 超过最大重试次数({max_retries})，账户锁定!")


def demo_nested_while():
    """演示 4: 嵌套 while 循环"""
    print("\n" + "=" * 50)
    print("演示 4: 嵌套 while 循环")
    print("=" * 50)

    # 用 while 打印九九乘法表
    print("  九九乘法表 (用 while):")
    i = 1
    while i <= 9:
        j = 1
        while j <= i:
            print(f"  {j}×{i}={i*j:2d}", end="")
            j += 1
        print()
        i += 1

    # 嵌套 break 只退出内层
    print("\n  嵌套 break 示例:")
    outer = 1
    while outer <= 3:
        inner = 1
        while inner <= 3:
            if inner == 2:
                print(f"    内层 break at outer={outer}, inner={inner}")
                break  # 只退出内层 while
            print(f"    outer={outer}, inner={inner}")
            inner += 1
        outer += 1


def demo_while_vs_for():
    """演示 5: while 与 for 的选择"""
    print("\n" + "=" * 50)
    print("演示 5: while 与 for 的选择")
    print("=" * 50)

    print("  选择指南:")
    print("    循环次数确定 -> 用 for")
    print("    循环次数不确定 -> 用 while")
    print()

    # 场景 1: 循环次数确定 -> for 更优
    print("  场景 1: 打印 1~5 -> for 更合适")
    for i in range(1, 6):
        print(f"    {i}", end=" ")
    print()

    # 场景 2: 循环次数不确定 -> while 更合适
    print("\n  场景 2: 数字每次减半直到小于1 -> while 更合适")
    num = 100
    while num > 1:
        print(f"    {num}", end=" -> ")
        num //= 2
    print(f"{num}")

    # 场景 3: 迭代算法 (如二分查找) -> while
    print("\n  场景 3: 二分查找模拟 -> while 合适")
    target = 67
    low, high = 1, 100
    steps = 0
    while low <= high:
        steps += 1
        mid = (low + high) // 2
        print(f"    范围 [{low}, {high}], 猜 {mid}", end="")
        if mid == target:
            print(f" -> 找到了! 共 {steps} 步")
            break
        elif mid < target:
            print(" -> 太小")
            low = mid + 1
        else:
            print(" -> 太大")
            high = mid - 1

    # 场景 4: 遍历序列 -> for 更简洁
    print("\n  场景 4: 遍历列表 -> for 更简洁")
    # for 方式
    items = [10, 20, 30, 40, 50]
    for item in items:
        print(f"    {item}", end=" ")
    print("← for 遍历比 while+索引 更 Pythonic")


# ========== 主程序入口 ==========
if __name__ == "__main__":
    demo_basic_while()
    demo_infinite_and_break()
    demo_while_else()
    demo_nested_while()
    demo_while_vs_for()
    print("\n[OK] 所有 while 循环演示完成！")
