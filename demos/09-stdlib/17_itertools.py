"""
itertools模块 - Python标准库高效迭代器
涵盖内容:
  1. 无限迭代器: count(), cycle(), repeat()
  2. 累积/压缩: accumulate()
  3. 连接函数: chain(), chain.from_iterable()
  4. 过滤函数: compress(), dropwhile(), filterfalse(), takewhile()
  5. 分组与切片: groupby(), islice(), tee()
  6. 星图映射: starmap()
  7. 填充合并: zip_longest()
  8. 组合排列: product(), permutations(), combinations(), combinations_with_replacement()
  9. 实用组合: 滑动窗口、分组处理、嵌套循环替代、排列组合场景

参考: https://docs.python.org/zh-cn/3/library/itertools.html
"""

import operator
from itertools import (
    accumulate, chain, combinations, combinations_with_replacement,
    compress, count, cycle, dropwhile, filterfalse, groupby,
    islice, permutations, product, repeat, starmap,
    takewhile, tee, zip_longest,
)


def sliding_window(iterable, n):
    """返回长度为 n 的滑动窗口 (使用 tee 实现)"""
    iters = tee(iterable, n)
    for i, it in enumerate(iters):
        for _ in range(i):
            next(it, None)
    return zip(*iters)


def grouper(iterable, n, fillvalue=None):
    """将可迭代对象按每组 n 个元素分组 (使用 zip_longest 实现)"""
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def main():
    # ============================================================
    # 1. 无限迭代器: count(), cycle(), repeat()
    # ============================================================
    print("=" * 50)
    print("1. 无限迭代器: count() / cycle() / repeat()")
    print("=" * 50)

    # count(start, step) - 无限计数
    print("count(10, 2) 从10开始步长2:")
    gen = count(10, 2)
    print(f"  {[next(gen) for _ in range(5)]}  # 前5个: 10,12,14,16,18")

    # cycle(iterable) - 无限循环
    print("\ncycle('ABC') 无限循环:")
    cyc = cycle("ABC")
    print(f"  {[next(cyc) for _ in range(8)]}  # 前8个: A B C A B C A B")

    # repeat(elem, n) - 重复元素 n 次
    print("\nrepeat('Hi', 3) 重复3次:")
    print(f"  {list(repeat('Hi', 3))}  # ['Hi', 'Hi', 'Hi']")

    # repeat 配合 map 模拟乘法表
    print("\nrepeat('=', 12) 结合 map 快速生成分隔线:")
    print(f"  {''.join(repeat('=', 12))}  # ============")

    # ============================================================
    # 2. 累积运算: accumulate()
    # ============================================================
    print("\n" + "=" * 50)
    print("2. 累积运算: accumulate()")
    print("=" * 50)

    nums = [1, 2, 3, 4, 5]
    print(f"数据: {nums}")
    print(f"  累加求和   = {list(accumulate(nums))}              # 前缀和")
    print(f"  累乘求积   = {list(accumulate(nums, operator.mul))} # 前缀积")
    print(f"  取最大值   = {list(accumulate([3,1,4,2,5], max))}   # 前缀最大值")

    # ============================================================
    # 3. 连接函数: chain() / chain.from_iterable()
    # ============================================================
    print("\n" + "=" * 50)
    print("3. 连接函数: chain() / chain.from_iterable()")
    print("=" * 50)

    # chain(*iterables) - 串联多个可迭代对象
    print(f"chain('ABC', 'DEF') 串联字符串:  {list(chain('ABC', 'DEF'))}")

    a, b, c = [1, 2], [3, 4], [5, 6]
    print(f"chain([1,2], [3,4], [5,6]) 串联列表:  {list(chain(a, b, c))}")

    # chain.from_iterable() - 展平一层嵌套
    nested = [[1, 2], [3, 4], [5, 6]]
    print(f"chain.from_iterable({nested}) 展平嵌套:  {list(chain.from_iterable(nested))}")

    # ============================================================
    # 4. 过滤函数: compress() / dropwhile() / filterfalse() / takewhile()
    # ============================================================
    print("\n" + "=" * 50)
    print("4. 过滤函数: compress / dropwhile / filterfalse / takewhile")
    print("=" * 50)

    # compress(data, selectors) - 按布尔掩码过滤
    data = ["A", "B", "C", "D", "E"]
    selectors = [1, 0, 1, 0, 1]
    print(f"compress({data}, {selectors}) => {list(compress(data, selectors))}")

    # dropwhile(pred, iterable) - 跳过满足条件的开头部分
    print(f"\ndropwhile(lambda x: x<3, [1,2,3,4,1,2])=> {list(dropwhile(lambda x: x < 3, [1, 2, 3, 4, 1, 2]))}")
    print("  跳过头部所有<3的元素, 直到遇到 >=3")

    # takewhile(pred, iterable) - 取满足条件的开头部分
    print(f"takewhile(lambda x: x<3, [1,2,3,4,1,2])=> {list(takewhile(lambda x: x < 3, [1, 2, 3, 4, 1, 2]))}")
    print("  取头部所有<3的元素, 遇到 >=3 停止")

    # filterfalse(pred, iterable) - 保留不满足条件的元素
    nums = range(1, 11)
    print(f"\nfilterfalse(lambda x: x%2, 1..10)=> {list(filterfalse(lambda x: x % 2, nums))}")
    print("  保留 predicate 为 False 的元素 (此处: 偶数)")

    # ============================================================
    # 5. 分组与切片: groupby() / islice() / tee()
    # ============================================================
    print("\n" + "=" * 50)
    print("5. 分组与切片: groupby() / islice() / tee()")
    print("=" * 50)

    # groupby(iterable, key) - 按连续相同 key 分组
    data = "AAABBBCCDAAA"
    print(f"groupby('{data}'):")
    for key, group in groupby(data):
        print(f"  '{key}': {list(group)}")

    # islice(iterable, start, stop, step) - 迭代器切片
    print(f"\nislice(range(100), 5, 15, 2) => {list(islice(range(100), 5, 15, 2))}")
    print("  取索引5开始, 步长为2, 到索引15停止")

    # tee(iterable, n) - 复制 n 份迭代器
    it = iter([1, 2, 3])
    a, b = tee(it, 2)
    print(f"\ntee([1,2,3], 2) 复制两份:")
    print(f"  copy1: {list(a)}")
    print(f"  copy2: {list(b)}")

    # ============================================================
    # 6. 星图映射: starmap()
    # ============================================================
    print("\n" + "=" * 50)
    print("6. 星图映射: starmap()")
    print("=" * 50)

    # starmap(func, iterable) - 对每个元素解包后调用 func
    pairs = [(2, 5), (3, 4), (10, 3)]
    print(f"starmap(pow, {pairs}) => {list(starmap(pow, pairs))}")
    print("  等价于 [pow(2,5), pow(3,4), pow(10,3)]")

    # 坐标距离计算
    points = [((0, 0), (3, 4)), ((0, 0), (5, 12))]
    dist = starmap(lambda p1, p2: ((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2) ** 0.5, points)
    print(f"starmap 计算两点距离: {list(dist)}")

    # ============================================================
    # 7. 填充合并: zip_longest()
    # ============================================================
    print("\n" + "=" * 50)
    print("7. 填充合并: zip_longest()")
    print("=" * 50)

    short = [1, 2, 3]
    long = "ABCDE"
    print(f"zip_longest({short}, 'ABCDE') 不等长合并:")
    print(f"  fillvalue='-' => {list(zip_longest(short, long, fillvalue='-'))}")
    print(f"  (默认 fillvalue=None) => {list(zip_longest(short, long))}")

    # ============================================================
    # 8. 组合排列: product / permutations / combinations / combinations_with_replacement
    # ============================================================
    print("\n" + "=" * 50)
    print("8. 组合排列")
    print("=" * 50)

    chars = "ABC"

    # product(*iterables, repeat=1) - 笛卡尔积
    print(f"product('ABC', repeat=2) 有放回排列 (笛卡尔积):")
    print(f"  {list(product(chars, repeat=2))}")

    # permutations(iterable, r) - 排列 (顺序重要, 不重复)
    print(f"\npermutations('ABC', 2) 排列 (有顺序, 不重复):")
    print(f"  {list(permutations(chars, 2))}")

    # combinations(iterable, r) - 组合 (顺序无关, 不重复)
    print(f"\ncombinations('ABC', 2) 组合 (无顺序, 不重复):")
    print(f"  {list(combinations(chars, 2))}")

    # combinations_with_replacement - 有放回组合 (元素可重复)
    print(f"\ncombinations_with_replacement('ABC', 2) 有放回组合:")
    print(f"  {list(combinations_with_replacement(chars, 2))}")

    # product 多迭代器笛卡尔积 (替代嵌套循环)
    print("\nproduct 多列表笛卡尔积 (替代嵌套循环):")
    colors, sizes = ["红", "蓝"], ["S", "M", "L"]
    print(f"  colors={colors}, sizes={sizes}")
    print(f"  => {list(product(colors, sizes))}")

    # ============================================================
    # 9. 实用组合: 滑动窗口 / 分组处理 / 实战场景
    # ============================================================
    print("\n" + "=" * 50)
    print("9. 实用组合示例")
    print("=" * 50)

    # 滑动窗口
    print("滑动窗口 (基于 tee+zip):")
    seq = [1, 2, 3, 4, 5]
    print(f"  序列: {seq}")
    print(f"  窗口大小 2: {list(sliding_window(seq, 2))}")
    print(f"  窗口大小 3: {list(sliding_window(seq, 3))}")

    # 分组处理 (grouper)
    print("\n分组处理 (基于 zip_longest):")
    print(f"  grouper([1..9], 3) 每组3个 => {list(grouper(range(1, 10), 3))}")
    print(f"  grouper([1..5], 3, fillvalue='?') => {list(grouper(range(1, 6), 3, fillvalue='?'))}")

    # 实战: 嵌套循环替代
    print("\n实战场景 - 嵌套循环-> product:")
    print("  旧式: for r in rows: for c in cols: ...")
    print(f"  新式: product([1,2], ['A','B']) = {list(product([1, 2], ['A', 'B']))}")

    # 实战: 密码穷举组合
    print("\n实战场景 - 6位数字密码穷举 (取前5个):")
    digits = "0123456789"
    combos = product(digits, repeat=6)
    for i, combo in enumerate(combos):
        if i >= 5:
            break
        print(f"  #{i+1}: {''.join(combo)}")


if __name__ == "__main__":
    main()
