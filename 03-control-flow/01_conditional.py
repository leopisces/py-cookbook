"""
条件控制 (Conditional Control)
===============================
Python 条件控制: if / elif / else 语句、嵌套条件、三元表达式、条件中常见陷阱。
参考: https://www.runoob.com/python3/python3-conditional-statements.html
"""

def demo_if_elif_else():
    """演示 1: if / elif / else 基本用法"""
    print("=" * 50)
    print("演示 1: if / elif / else 基本用法")
    print("=" * 50)

    score = 85

    if score >= 90:
        grade = "优秀"
    elif score >= 80:
        grade = "良好"
    elif score >= 70:
        grade = "中等"
    elif score >= 60:
        grade = "及格"
    else:
        grade = "不及格"

    print(f"成绩: {score}, 等级: {grade}")

    # Python 用缩进表示代码块，冒号后缩进的一致层级为一组
    x = 10
    if x > 5:
        print("  x > 5 成立")
        print("  这两行在同一个 if 块内")
    else:
        print("  x <= 5 成立")
    print("  这一行已经不在 if-else 块内了（缩进层级回到了外面）")


def demo_nested_if():
    """演示 2: 嵌套条件"""
    print("\n" + "=" * 50)
    print("演示 2: 嵌套 if 语句")
    print("=" * 50)

    age = 25
    has_license = True

    # 嵌套条件：外层判断年龄，内层判断是否有驾照
    if age >= 18:
        print(f"年龄 {age} 岁，已成年")
        if has_license:
            print("  有驾照，可以开车")
        else:
            print("  无驾照，不能开车")
    else:
        print(f"年龄 {age} 岁，未成年，不能考驾照")

    # 多层嵌套示例（实际开发中避免过深的嵌套，建议重构）
    is_weekend = False
    weather_is_good = True
    have_time = True

    if is_weekend:
        if weather_is_good:
            if have_time:
                print("去郊游！")
            else:
                print("在家休息")
        else:
            print("去看电影")
    else:
        print("上班/上学")


def demo_ternary():
    """演示 3: 三元表达式 (条件表达式)"""
    print("\n" + "=" * 50)
    print("演示 3: 三元表达式")
    print("=" * 50)

    # 语法: value_if_true if condition else value_if_false
    age = 20
    status = "成年" if age >= 18 else "未成年"
    print(f"年龄 {age}: {status}")

    # 与传统 if-else 对比
    num = 7
    parity = "偶数" if num % 2 == 0 else "奇数"
    print(f"{num} 是{parity}")

    # 嵌套三元表达式（可读性差，不推荐）
    score = 75
    result = "优秀" if score >= 90 else ("良好" if score >= 80 else ("中等" if score >= 70 else "加油"))
    print(f"成绩 {score}: {result}")

    # 三元表达式可以用于任何需要值的场景
    a, b = 10, 20
    max_val = a if a > b else b
    print(f"a={a}, b={b}, 较大值: {max_val}")


def demo_truthy_falsy():
    """演示 4: 条件中的真值判断与常见陷阱"""
    print("\n" + "=" * 50)
    print("演示 4: 条件中的真值判断与常见陷阱")
    print("=" * 50)

    # Python 中以下值被视为 False:
    # None, False, 0, 0.0, 空字符串"", 空列表[], 空元组(), 空字典{}, 空集合set()
    # 其他一切皆为 True

    falsy_values = [
        ("None", None),
        ("False", False),
        ("0", 0),
        ("0.0", 0.0),
        ("空字符串 ''", ""),
        ("空列表 []", []),
        ("空元组 ()", ()),
        ("空字典 {}", {}),
        ("空集合 set()", set()),
    ]

    for name, val in falsy_values:
        result = "True" if val else "False (falsy)"
        print(f"  {name:20s} -> {result}")

    # 陷阱 1: 不要用 == 判断 None，应该用 is
    value = None
    if value is None:  # [OK] 推荐
        print("\n  [OK] 正确判断 None: 使用 'is None'")
    # if value == None:  # [X] 不推荐，None 是单例对象

    # 陷阱 2: 布尔运算符短路 (and / or)
    # and: 第一个 falsy 值或最后一个值
    # or:  第一个 truthy 值或最后一个值
    print("\n  布尔运算符短路特性:")
    print(f"    0 and 5 = {0 and 5}        (0 是 falsy，短路返回 0)")
    print(f"    3 and 5 = {3 and 5}        (3 是 truthy，继续计算返回 5)")
    print(f"    0 or 5  = {0 or 5}         (0 是 falsy，继续计算返回 5)")
    print(f"    3 or 5  = {3 or 5}         (3 是 truthy，短路返回 3)")

    # 陷阱 3: 比较运算符可以链式使用
    x = 5
    result = 1 < x < 10  # 等价于 1 < x and x < 10
    print(f"\n  链式比较: 1 < {x} < 10 -> {result}")

    # 陷阱 4: 成员测试 in / not in
    fruits = ["apple", "banana", "orange"]
    print(f"  'apple' in fruits  -> {'apple' in fruits}")
    print(f"  'grape' not in fruits -> {'grape' not in fruits}")

    # 陷阱 5: 空容器在条件中的用法
    items = []
    if not items:
        print("\n  陷阱 5: 空列表条件判断正确用法 - if not items: (而不是 if len(items) == 0)")


def demo_multiple_conditions():
    """演示 5: 多条件组合与 match-case (Python 3.10+)"""
    print("\n" + "=" * 50)
    print("演示 5: 多条件组合")
    print("=" * 50)

    # and / or / not 组合
    age = 22
    is_student = True

    if age < 30 and is_student:
        print(f"  年龄 {age}, 是学生 -> 享受学生优惠")
    elif age >= 60 or age < 12:
        print(f"  年龄 {age} -> 享受老人/儿童优惠")
    else:
        print(f"  年龄 {age} -> 全价票")


# ========== 主程序入口 ==========
if __name__ == "__main__":
    demo_if_elif_else()
    demo_nested_if()
    demo_ternary()
    demo_truthy_falsy()
    demo_multiple_conditions()
    print("\n[OK] 所有条件控制演示完成！")
