"""
Python 字典 (Dictionary)

学习目标：
  - 字典的创建与初始化
  - 访问、修改、删除键值对
  - 常用方法: keys, values, items, get, update, pop, setdefault
  - 字典推导式
  - 字典的遍历与嵌套
"""

def main():
    # ========== 1. 字典的创建 ==========
    print("=== 1. 字典的创建 ===")

    # 多种创建方式
    d1 = {}                                 # 空字典
    d2 = {"name": "张三", "age": 25}        # 标准字面量
    d3 = dict(name="李四", age=30)          # dict() + 关键字参数
    d4 = dict([("name", "王五"), ("age", 28)])  # 键值对序列
    d5 = dict(zip(["a", "b", "c"], [1, 2, 3]))  # zip 创建

    print(f"空字典: {d1}")
    print(f"字面量: {d2}")
    print(f"关键字: {d3}")
    print(f"序列: {d4}")
    print(f"zip: {d5}")

    # ========== 2. 访问与修改 ==========
    print("\n=== 2. 访问与修改 ===")

    student = {
        "name": "小明",
        "age": 20,
        "scores": {"语文": 90, "数学": 95, "英语": 88}
    }

    # 访问
    print(f"姓名: {student['name']}")                       # 直接访问
    print(f"年龄: {student['age']}")

    # get() — 安全访问（键不存在也不会报错）
    print(f"手机号 (get): {student.get('phone', '未设置')}")
    print(f"姓名 (get): {student.get('name', '未知')}")

    # 修改
    student["age"] = 21                                     # 修改已有键
    student["grade"] = "大三"                                # 添加新键
    print(f"修改后: {student}")

    # 删除
    removed = student.pop("grade")                          # 删除并返回值
    print(f"pop('grade') 返回值: '{removed}'")
    del student["scores"]                                   # 直接删除
    print(f"删除后: {student}")

    # ========== 3. 常用方法 ==========
    print("\n=== 3. 常用方法 ===")

    info = {"name": "Alice", "age": 25, "city": "北京"}
    print(f"字典: {info}")

    # keys(), values(), items()
    print(f"keys(): {list(info.keys())}")
    print(f"values(): {list(info.values())}")
    print(f"items(): {list(info.items())}")

    # get() — 安全获取（已在上方演示）
    print(f'get("name"): {info.get("name")}')
    print(f'get("country", "中国"): {info.get("country", "中国")}')

    # update() — 合并字典
    info.update({"age": 26, "hobby": "编程"})  # 更新已有键，添加新键
    print(f"update() 后: {info}")

    # pop() — 删除并返回
    age = info.pop("age")
    print(f'pop("age") = {age}, 剩余: {info}')

    # popitem() — 删除并返回最后一个键值对 (Python 3.7+)
    pair = info.popitem()
    print(f'popitem() = {pair}, 剩余: {info}')

    # setdefault() — 键存在则返回值，不存在则设置默认值
    name = info.setdefault("name", "未知")       # 键存在 → 返回值
    country = info.setdefault("country", "中国") # 键不存在 → 设置并返回
    print(f"setdefault('name'): '{name}'")
    print(f"setdefault('country', '中国'): '{country}'")
    print(f"最终字典: {info}")

    # ========== 4. 字典推导式 ==========
    print("\n=== 4. 字典推导式 ===")

    # 平方字典
    squares = {x: x**2 for x in range(1, 6)}
    print(f"平方字典: {squares}")

    # 带条件的推导
    even_squares = {x: x**2 for x in range(10) if x % 2 == 0}
    print(f"偶数平方: {even_squares}")

    # 反转键值对
    original = {"a": 1, "b": 2, "c": 3}
    reversed_dict = {v: k for k, v in original.items()}
    print(f"原字典: {original}")
    print(f"键值反转: {reversed_dict}")

    # 从列表创建字典（元素作为键）
    fruits = ["apple", "banana", "orange"]
    fruit_len = {f: len(f) for f in fruits}
    print(f"水果名→长度: {fruit_len}")

    # ========== 5. 遍历字典 ==========
    print("\n=== 5. 遍历字典 ===")

    grades = {"语文": 90, "数学": 95, "英语": 88, "物理": 92}

    # 遍历键
    print("遍历键:")
    for subject in grades:
        print(f"  {subject}", end=" ")
    print()

    # 遍历值
    print("遍历值:", end=" ")
    for score in grades.values():
        print(score, end=" ")
    print()

    # 遍历键值对
    print("遍历键值对:")
    for subject, score in grades.items():
        status = "优秀" if score >= 90 else "良好"
        print(f"  {subject}: {score} 分 ({status})")

    # 统计
    total = sum(grades.values())
    avg = total / len(grades)
    print(f"总成绩: {total}, 平均分: {avg:.1f}")

    # ========== 6. 字典嵌套 ==========
    print("\n=== 6. 字典嵌套 ===")

    # 嵌套字典 — 模拟学生管理系统
    school = {
        "一班": {
            "张三": {"语文": 85, "数学": 90},
            "李四": {"语文": 92, "数学": 88},
        },
        "二班": {
            "王五": {"语文": 78, "数学": 85},
            "赵六": {"语文": 95, "数学": 93},
        }
    }

    print("学生成绩系统:")
    for class_name, students in school.items():
        print(f"\n{class_name}:")
        for name, scores in students.items():
            avg = sum(scores.values()) / len(scores)
            print(f"  {name}: {scores}, 平均分: {avg:.1f}")


if __name__ == "__main__":
    main()
