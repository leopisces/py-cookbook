"""
匿名函数 (Lambda)
===============================
Python lambda 函数: 定义与使用、与 map/filter/sorted 结合、
lambda 与 def 的对比、适用场景。
参考: https://www.runoob.com/python3/python3-function.html
"""


def demo_lambda_basic():
    """演示 1: lambda 基本定义与使用"""
    print("=" * 50)
    print("演示 1: lambda 基本定义与使用")
    print("=" * 50)

    # lambda 语法: lambda 参数: 表达式
    # lambda 是单行表达式函数，自动返回表达式的结果

    # 最简单的 lambda
    square = lambda x: x ** 2
    print(f"  平方: lambda x: x**2  -> square(5) = {square(5)}")

    # 多个参数
    add = lambda a, b: a + b
    print(f"  加法: lambda a,b: a+b -> add(3,4) = {add(3, 4)}")

    # 无参数
    get_pi = lambda: 3.14159
    print(f"  无参: lambda: 3.14159  -> get_pi() = {get_pi()}")

    # 条件表达式 (三元运算符)
    max_val = lambda a, b: a if a > b else b
    print(f"  最大值: max_val(10, 20) = {max_val(10, 20)}")

    # lambda 作为参数直接传递给其他函数
    numbers = [5, 2, 8, 1, 9, 3]
    sorted_nums = sorted(numbers, key=lambda x: x)  # 按值排序
    print(f"\n  sorted 配合 lambda: {sorted_nums}")

    # lambda 也可以返回元组等复合值
    swap = lambda x, y: (y, x)
    print(f"  交换: swap(1, 2) = {swap(1, 2)}")


def demo_lambda_with_map():
    """演示 2: lambda 与 map() 配合"""
    print("\n" + "=" * 50)
    print("演示 2: lambda 与 map() 配合")
    print("=" * 50)

    # map(函数, 可迭代对象) — 对每个元素应用函数
    numbers = [1, 2, 3, 4, 5]

    # 平方
    squared = list(map(lambda x: x ** 2, numbers))
    print(f"  平方: {squared}")

    # 多个可迭代对象
    list1 = [1, 2, 3]
    list2 = [10, 20, 30]
    summed = list(map(lambda a, b: a + b, list1, list2))
    print(f"  两列表相加: {summed}")

    # 类型转换
    str_nums = ["1", "2", "3", "4"]
    int_nums = list(map(lambda s: int(s), str_nums))
    print(f"  字符串列表转整数: {int_nums}")

    # 等价写法: map(int, str_nums) 也可以
    int_nums2 = list(map(int, str_nums))
    print(f"  直接用 int: {int_nums2}")

    # 字符串格式化
    names = ["alice", "bob", "charlie"]
    capitalized = list(map(lambda name: name.capitalize(), names))
    print(f"  首字母大写: {capitalized}")


def demo_lambda_with_filter():
    """演示 3: lambda 与 filter() 配合"""
    print("\n" + "=" * 50)
    print("演示 3: lambda 与 filter() 配合")
    print("=" * 50)

    # filter(函数, 可迭代对象) — 保留函数返回 True 的元素
    numbers = list(range(1, 21))

    # 筛选偶数
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    print(f"  偶数: {evens}")

    # 筛选能被3整除的数
    div_by_3 = list(filter(lambda x: x % 3 == 0, numbers))
    print(f"  能被3整除: {div_by_3}")

    # 筛选非空字符串
    words = ["hello", "", "world", "", "python", ""]
    non_empty = list(filter(lambda w: w != "", words))
    print(f"  非空字符串: {non_empty}")

    # 筛选长度>3的单词
    words = ["hi", "hello", "ok", "python", "a", "world"]
    long_words = list(filter(lambda w: len(w) > 3, words))
    print(f"  长度>3的单词: {long_words}")

    # filter 返回 None / falsy 值时元素被过滤
    values = [0, 1, "", "hello", None, 42, [], [1, 2]]
    truthy = list(filter(None, values))  # filter(None, ...) 过滤掉 falsy 值
    print(f"  过滤 falsy 值: {truthy}")


def demo_lambda_with_sorted():
    """演示 4: lambda 与 sorted() / max() / min() 配合"""
    print("\n" + "=" * 50)
    print("演示 4: lambda 与 sorted/max/min 配合")
    print("=" * 50)

    # sorted(key=...) — 按指定规则排序

    # 按字符串长度排序
    words = ["banana", "apple", "kiwi", "cherry", "date"]
    by_length = sorted(words, key=lambda w: len(w))
    print(f"  按长度排序: {by_length}")

    # 按最后一个字符排序
    by_last_char = sorted(words, key=lambda w: w[-1])
    print(f"  按最后字符排序: {by_last_char}")

    # 对元组列表排序（按第二个元素）
    students = [("张三", 85), ("李四", 92), ("王五", 78)]
    by_score = sorted(students, key=lambda s: s[1], reverse=True)
    print(f"  按成绩降序: {by_score}")

    # 对字典列表排序
    people = [
        {"name": "张三", "age": 25},
        {"name": "李四", "age": 20},
        {"name": "王五", "age": 30},
    ]
    by_age = sorted(people, key=lambda p: p["age"])
    print(f"  按年龄排序: {[p['name'] for p in by_age]}")

    # 多级排序：先按长度，再按字母顺序
    words = ["apple", "bat", "cherry", "dog", "ant"]
    multi_sort = sorted(words, key=lambda w: (len(w), w))
    print(f"  多级排序(长度+字母): {multi_sort}")

    # max / min 配合 lambda
    words = ["hello", "world", "python", "AI"]
    longest = max(words, key=lambda w: len(w))
    shortest = min(words, key=lambda w: len(w))
    print(f"\n  最长单词: {longest}, 最短单词: {shortest}")


def demo_lambda_vs_def():
    """演示 5: lambda 与 def 对比，以及 lambda 的局限性"""
    print("\n" + "=" * 50)
    print("演示 5: lambda 与 def 对比")
    print("=" * 50)

    # 等价写法对比
    print("  等价写法对比:")

    # lambda 版本
    double_lambda = lambda x: x * 2
    # def 版本
    def double_def(x):
        return x * 2

    print(f"    lambda: double_lambda(5) = {double_lambda(5)}")
    print(f"    def:    double_def(5)    = {double_def(5)}")
    print(f"    类型:   {type(double_lambda).__name__} vs {type(double_def).__name__}")

    # lambda 适用场景
    print("\n  [OK] lambda 适用场景:")

    # 1. 作为一次性回调/参数
    pairs = [(1, 'one'), (2, 'two'), (3, 'three'), (4, 'four')]
    pairs.sort(key=lambda pair: pair[1])
    print(f"    1. 排序回调: {pairs}")

    # 2. GUI 事件处理 (简化示例)
    actions = []
    for i in range(3):
        actions.append(lambda i=i: f"按钮 {i} 被点击")  # 注意 i=i 绑定当前值
    print(f"    2. 事件回调: {[a() for a in actions]}")

    # 3. 短小的转换操作
    data = [1.5, 2.7, 3.1, 4.9]
    rounded = list(map(lambda x: round(x), data))
    print(f"    3. 数据转换: {rounded}")

    print("\n  [X] lambda 局限性:")

    # 1. 只能包含一个表达式（不能有语句）
    lambda_square = lambda x: x ** 2  # [OK] 表达式
    # lambda x: print(x); return x  # [X] 不能包含语句

    # 2. 不能包含类型注解
    # lambda x: int = x * 2  # [X] 语法错误

    # 3. 不能包含文档字符串
    # lambda x: "docstring" or (x * 2)  # hack，不推荐

    # 4. 复杂逻辑应该用 def
    print("    1. lambda 只能包含一个表达式，不能有语句")
    print("    2. lambda 不能包含类型注解")
    print("    3. lambda 不能包含文档字符串")
    print("    4. 复杂逻辑应该用 def 提高可读性")

    # 经验法则
    print("\n  [*] 经验法则:")
    print("    用 lambda: 一行能写完的简单表达式，作为参数传递")
    print("    用 def:    多行逻辑、需要复用、需要文档、需要递归")


# ========== 主程序入口 ==========
if __name__ == "__main__":
    demo_lambda_basic()
    demo_lambda_with_map()
    demo_lambda_with_filter()
    demo_lambda_with_sorted()
    demo_lambda_vs_def()
    print("\n[OK] 所有 lambda 演示完成！")
