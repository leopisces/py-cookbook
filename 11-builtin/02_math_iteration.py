"""
内置函数 — 数学与迭代相关 (Math / Iteration)
==================================================
演示与数学运算、迭代处理相关的 Python 内置函数：
abs, round, divmod, pow, min, max, sum,
len, range, enumerate, zip, map, filter,
sorted, reversed, all, any, iter, next

参考: https://www.runoob.com/python3/python3-built-in-functions.html
"""


# ========== 演示 1: 数学相关函数 ==========
def demo_math_functions():
    """abs / round / divmod / pow / min / max / sum"""
    print("=" * 50)
    print("演示 1: 数学相关函数")
    print("=" * 50)

    # --- abs(): 绝对值 ---
    print("--- abs() 绝对值 ---")
    print(f"  abs(-10)          = {abs(-10)}")
    print(f"  abs(-3.14)        = {abs(-3.14)}")
    print(f"  abs(complex(3, 4))= {abs(complex(3, 4))}  # 复数的模")

    # --- round(): 四舍五入 ---
    print("\n--- round() 四舍五入 ---")
    print(f"  round(3.14159, 2) = {round(3.14159, 2)}")
    print(f"  round(3.14159)    = {round(3.14159)}     # 默认0位小数")
    print(f"  round(2.5)        = {round(2.5)}         # 银行家舍入(偶数优先)")

    # --- divmod(): 同时返回商和余数 ---
    print("\n--- divmod() 商和余数 ---")
    q, r = divmod(17, 5)
    print(f"  divmod(17, 5)     = ({q}, {r})")
    q2, r2 = divmod(100, 7)
    print(f"  divmod(100, 7)    = ({q2}, {r2})  # 验证: {q2}*7+{r2}={q2*7+r2}")

    # --- pow(): 幂运算 (可加取模) ---
    print("\n--- pow() 幂运算 ---")
    print(f"  pow(2, 3)        = {pow(2, 3)}        # 2的3次方")
    print(f"  pow(2, 10)       = {pow(2, 10)}       # 2的10次方")
    print(f"  pow(2, 3, 5)     = {pow(2, 3, 5)}    # (2的3次方) % 5 (高效取模)")

    # --- min() / max(): 最小/最大值 ---
    print("\n--- min() / max() ---")
    nums = [5, 2, 9, 1, 7, 3]
    print(f"  数据: {nums}")
    print(f"  min(nums)        = {min(nums)}")
    print(f"  max(nums)        = {max(nums)}")
    print(f"  min('a', 'z', 'm') = {min('a', 'z', 'm')}")
    # key 参数: 按自定义规则比较
    words = ["apple", "banana", "kiwi", "grape"]
    print(f"  单词: {words}")
    print(f"  min(按长度)      = {min(words, key=len)}")
    print(f"  max(按长度)      = {max(words, key=len)}")

    # --- sum(): 求和 ---
    print("\n--- sum() 求和 ---")
    print(f"  sum([1, 2, 3, 4, 5])     = {sum([1, 2, 3, 4, 5])}")
    print(f"  sum([1, 2, 3], start=10)  = {sum([1, 2, 3], start=10)}")
    # 生成器求和
    print(f"  sum(i*i for i in range(1,6)) = {sum(i * i for i in range(1, 6))}")

    print()


# ========== 演示 2: 迭代相关函数 ==========
def demo_iteration_functions():
    """len / range / enumerate / zip / map / filter / sorted / reversed / all / any / iter / next"""
    print("=" * 50)
    print("演示 2: 迭代相关函数")
    print("=" * 50)

    # --- len(): 获取长度 ---
    print("--- len() ---")
    print(f"  len('Python')      = {len('Python')}")
    print(f"  len([1, 2, 3])     = {len([1, 2, 3])}")
    sample_dict = {'a': 1, 'b': 2}
    print(f"  len({sample_dict}) = {len(sample_dict)}")

    # --- range(): 生成整数序列 ---
    print("\n--- range() ---")
    print(f"  list(range(5))     = {list(range(5))}        # 0到4")
    print(f"  list(range(2, 7))  = {list(range(2, 7))}     # 2到6")
    print(f"  list(range(0, 10, 3)) = {list(range(0, 10, 3))}  # 步长3")
    print(f"  list(range(10, 0, -1)) = {list(range(10, 0, -1))}  # 递减")

    # --- enumerate(): 带索引的迭代 ---
    print("\n--- enumerate() ---")
    fruits = ["苹果", "香蕉", "橙子"]
    print(f"  水果列表: {fruits}")
    print("  带索引遍历:")
    for i, fruit in enumerate(fruits):
        print(f"    [{i}] {fruit}")
    print(f"  enumerate start=1: {list(enumerate(fruits, start=1))}")

    # --- zip(): 并行迭代多个可迭代对象 ---
    print("\n--- zip() ---")
    names = ["张三", "李四", "王五"]
    scores = [85, 92, 78]
    ages = [20, 21, 22]
    print(f"  姓名: {names}")
    print(f"  成绩: {scores}")
    print(f"  年龄: {ages}")
    print("  zip 并行迭代:")
    for name, score, age in zip(names, scores, ages):
        print(f"    {name}: 成绩{score}, 年龄{age}")
    # 创建字典的便捷方式
    print(f"  dict(zip(names, scores)) = {dict(zip(names, scores))}")

    # --- map(): 对每个元素应用函数 ---
    print("\n--- map() ---")
    nums = [1, 2, 3, 4, 5]
    print(f"  数据: {nums}")
    squared = list(map(lambda x: x * x, nums))
    print(f"  map(平方): {squared}")
    # 多个可迭代对象
    a, b = [1, 2, 3], [4, 5, 6]
    print(f"  map(add, {a}, {b}) = {list(map(lambda x, y: x + y, a, b))}")

    # --- filter(): 过滤元素 ---
    print("\n--- filter() ---")
    print(f"  数据: {nums}")
    even = list(filter(lambda x: x % 2 == 0, nums))
    print(f"  filter(偶数): {even}")
    # 当第一个参数为 None 时，过滤掉 falsy 值
    mixed = [0, 1, "", "hello", [], [1, 2], None, False]
    print(f"  filter(None, {mixed}) = {list(filter(None, mixed))}")

    # --- sorted(): 排序 ---
    print("\n--- sorted() ---")
    nums2 = [3, 1, 4, 1, 5, 9, 2]
    print(f"  数据: {nums2}")
    print(f"  sorted()            = {sorted(nums2)}")
    print(f"  sorted(reverse=True)= {sorted(nums2, reverse=True)}")
    # key 参数自定义排序
    words = ["banana", "apple", "kiwi", "grape"]
    print(f"  sorted(按长度)      = {sorted(words, key=len)}")
    print(f"  sorted(按末尾字母)  = {sorted(words, key=lambda w: w[-1])}")

    # --- reversed(): 反向迭代 ---
    print("\n--- reversed() ---")
    print(f"  数据: {nums}")
    print(f"  list(reversed(nums)) = {list(reversed(nums))}")
    # reversed 返回迭代器，不是列表
    r = reversed(nums)
    print(f"  reversed 对象: {r}")

    # --- all() / any(): 全真/任一真 ---
    print("\n--- all() / any() ---")
    print(f"  all([True, True, False])  = {all([True, True, False])}")
    print(f"  all([1, 2, 3])            = {all([1, 2, 3])}")
    print(f"  all([1, 0, 3])            = {all([1, 0, 3])}")
    print(f"  any([False, False, True]) = {any([False, False, True])}")
    print(f"  any([0, '', None])        = {any([0, '', None])}")
    # 实用: 检查是否所有元素满足条件
    print(f"  所有 > 0? {all(n > 0 for n in [1, 2, 3, 4])}")
    print(f"  存在 > 2? {any(n > 2 for n in [1, 2, 3, 4])}")

    # --- iter() / next(): 迭代器 ---
    print("\n--- iter() / next() ---")
    it = iter([10, 20, 30])
    print(f"  next(it) = {next(it)}")
    print(f"  next(it) = {next(it)}")
    print(f"  next(it) = {next(it)}")
    print(f"  next(it, '默认值') = {next(it, '默认值')}  # 耗尽后返回默认值")

    print()


# ========== 主程序入口 ==========
if __name__ == "__main__":
    demo_math_functions()
    demo_iteration_functions()
