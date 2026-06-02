"""
functools模块 - Python标准库高阶函数工具
涵盖内容:
  1. partial - 偏函数（固定部分参数）
  2. reduce - 累积计算
  3. lru_cache - 缓存装饰器（斐波那契性能对比）
  4. total_ordering - 自动补全比较方法
  5. wraps - 保留原函数元信息（与装饰器章节呼应）
  6. singledispatch - 根据参数类型分发不同实现

参考: https://docs.python.org/zh-cn/3/library/functools.html
"""

import time
import functools
from functools import partial, reduce, lru_cache, total_ordering, wraps, singledispatch


# ============================================================
# 辅助函数
# ============================================================

def power(base, exp):
    """计算幂"""
    return base ** exp


def multiply(x, y, z=1):
    """乘法运算"""
    return x * y * z


# total_ordering 演示用
@total_ordering
class Version:
    """版本号类 - 只定义 __eq__ 和 __lt__, total_ordering 自动补全其余比较方法"""

    def __init__(self, major, minor, patch=0):
        self.major = major
        self.minor = minor
        self.patch = patch

    def __eq__(self, other):
        return (self.major, self.minor, self.patch) == (other.major, other.minor, other.patch)

    def __lt__(self, other):
        return (self.major, self.minor, self.patch) < (other.major, other.minor, other.patch)

    def __repr__(self):
        return f"v{self.major}.{self.minor}.{self.patch}"


# singledispatch 演示用
@singledispatch
def describe(obj):
    """根据参数类型分发描述"""
    return f"未知类型 {type(obj).__name__}: {obj}"


@describe.register
def _(obj: str):
    return f"字符串 (len={len(obj)}): '{obj}'"


@describe.register
def _(obj: int):
    return f"整数: {obj} (十六进制: {hex(obj)})"


@describe.register
def _(obj: list):
    return f"列表 (len={len(obj)}): {obj[:3]}{'...' if len(obj) > 3 else ''}"


@describe.register
def _(obj: dict):
    return f"字典 (keys={len(obj)}): {list(obj.keys())[:3]}"


def main():
    # ============================================================
    # 1. partial - 偏函数（固定部分参数）
    # ============================================================
    print("=" * 50)
    print("1. functools.partial() - 偏函数（固定部分参数）")
    print("=" * 50)

    # 固定 base 参数: 创建平方、立方函数
    square = partial(power, exp=2)
    cube = partial(power, exp=3)

    print("原始函数: power(base, exp) -> base ** exp")
    print(f"  power(2, 3) = {power(2, 3)}")
    print("\n创建偏函数:")
    print(f"  square = partial(power, exp=2)")
    print(f"  cube   = partial(power, exp=3)")
    print(f"\n  square(5)  = {square(5)}   (5**2)")
    print(f"  square(10) = {square(10)}  (10**2)")
    print(f"  cube(3)    = {cube(3)}     (3**3)")

    # 固定位置参数
    double = partial(multiply, 2)
    triple = partial(multiply, 3)

    print(f"\n固定位置参数:")
    print(f"  multiply(x, y, z=1) -> x * y * z")
    print(f"  double = partial(multiply, 2)   # 固定 x=2")
    print(f"  double(5)    = {double(5)}       (2*5*1)")
    print(f"  double(5, z=10) = {double(5, z=10)}  (2*5*10)")
    print(f"  triple(4)    = {triple(4)}       (3*4*1)")

    # 与 lambda 对比: partial 可序列化, 调试时显示函数名
    print(f"\npartial 的优势:")
    print(f"  square (str): {square}     # 保留函数名便于调试")
    print(f"  lambda对比:   <lambda>      # 匿名函数难以调试")
    print(f"  partial 是C实现的, 比 lambda 更高效")

    # ============================================================
    # 2. reduce - 累积计算
    # ============================================================
    print("\n" + "=" * 50)
    print("2. functools.reduce() - 累积计算")
    print("=" * 50)

    # 列表求和
    nums = [1, 2, 3, 4, 5]
    total = reduce(lambda a, b: a + b, nums)
    print(f"列表: {nums}")
    print(f"  reduce(lambda a,b: a+b, nums) = {total}")
    print(f"  builtin sum(nums)              = {sum(nums)}  (等价, 但更快)")

    # 求最大值
    max_val = reduce(lambda a, b: a if a > b else b, nums)
    print(f"\n  reduce(lambda a,b: a if a>b else b, nums) = {max_val}")
    print(f"  builtin max(nums)                          = {max(nums)}  (等价)")

    # 阶乘 —— 内置函数无法替代的场景
    factorial = reduce(lambda a, b: a * b, range(1, 6))
    print(f"\n  阶乘 5! = reduce(lambda a,b: a*b, range(1,6)) = {factorial}")

    # 字符串拼接
    words = ["Python", "标准库", "functools"]
    joined = reduce(lambda a, b: a + " -> " + b, words)
    print(f"\n  字符串累积: reduce(..., {words})")
    print(f"    结果: {joined}")

    # 带初始值
    seq = [1, 2, 3]
    result = reduce(lambda a, b: a + b, seq, 10)
    print(f"\n  带初始值: reduce(lambda a,b: a+b, {seq}, 10) = {result}")
    print(f"    等价于: (((10+1)+2)+3)")

    # ============================================================
    # 3. lru_cache - 缓存装饰器（斐波那契性能对比）
    # ============================================================
    print("\n" + "=" * 50)
    print("3. functools.lru_cache - 缓存装饰器")
    print("=" * 50)

    # 无缓存的斐波那契（仅用于对比, 不实际计算大值）
    def fib_no_cache(n):
        if n < 2:
            return n
        return fib_no_cache(n - 1) + fib_no_cache(n - 2)

    # 有缓存的斐波那契
    @lru_cache(maxsize=None)
    def fib(n):
        if n < 2:
            return n
        return fib(n - 1) + fib(n - 2)

    # 性能对比: 无缓存版本仅测试小值, 避免耗时过长
    n_small = 10
    start = time.perf_counter()
    result_no = fib_no_cache(n_small)
    time_no = time.perf_counter() - start

    start = time.perf_counter()
    result_cached = fib(n_small)
    time_cached = time.perf_counter() - start

    print(f"斐波那契 fib({n_small}):")
    print(f"  无缓存: fib(10)={result_no},  耗时: {time_no:.6f}s  (指数复杂度 O(2^n))")
    print(f"  有缓存: fib(10)={result_cached},  耗时: {time_cached:.6f}s  (线性复杂度 O(n))")

    # 大值测试（仅缓存版本, 无缓存版本会极慢）
    fib.cache_clear()
    n_big = 35
    start = time.perf_counter()
    result = fib(n_big)
    elapsed = time.perf_counter() - start
    print(f"\n  缓存版 fib({n_big}) = {result}, 耗时: {elapsed:.6f}s")

    # cache_info 查看缓存统计
    info = fib.cache_info()
    print(f"\n  cache_info():")
    print(f"    hits={info.hits}    (命中次数)")
    print(f"    misses={info.misses}  (未命中次数)")
    print(f"    maxsize={info.maxsize} (最大缓存大小)")
    print(f"    currsize={info.currsize} (当前缓存条目)")

    # maxsize 参数限制
    @lru_cache(maxsize=3)
    def compute(x):
        print(f"    [计算] compute({x})")  # 仅在缓存未命中时打印
        return x * x

    print(f"\n  maxsize 限制演示 (maxsize=3):")
    print(f"    compute(1) = {compute(1)}")
    print(f"    compute(1) = {compute(1)}  # 缓存命中")
    print(f"    compute(2) = {compute(2)}")
    print(f"    compute(3) = {compute(3)}")
    print(f"    compute(4) = {compute(4)}  # 满, 淘汰最早的1")
    print(f"    compute(1) = {compute(1)}  # 已淘汰, 重新计算")

    # ============================================================
    # 4. total_ordering - 自动补全比较方法
    # ============================================================
    print("\n" + "=" * 50)
    print("4. functools.total_ordering - 自动补全比较方法")
    print("=" * 50)

    v1 = Version(1, 0)
    v2 = Version(1, 2, 3)
    v3 = Version(2, 0)
    v4 = Version(1, 2, 3)  # 与 v2 相等

    print("只需定义 __eq__ 和 __lt__, total_ordering 自动补全:")
    print("  __le__, __gt__, __ge__")
    print(f"\n版本实例: v1={v1}, v2={v2}, v3={v3}, v4={v4}")

    comparisons = [
        ("==", lambda: v1 == v2, f"v1 == v2"),
        ("!=", lambda: v1 != v2, f"v1 != v2"),
        ("<",  lambda: v1 < v2,  f"v1 < v2"),
        ("<=", lambda: v1 <= v2, f"v1 <= v2"),
        (">",  lambda: v1 > v2,  f"v1 > v2"),
        (">=", lambda: v1 >= v2, f"v1 >= v2"),
    ]

    print(f"\n  {v1} 与 {v2} 比较:")
    for op_name, op_fn, expr in comparisons:
        print(f"    {expr:<10} = {op_fn()}")

    print(f"\n  {v2} 与 {v4} (相等) 比较:")
    print(f"    v2 == v4   = {v2 == v4}")
    print(f"    v2 != v4   = {v2 != v4}")
    print(f"    v2 < v4    = {v2 < v4}")
    print(f"    v2 <= v4   = {v2 <= v4}")
    print(f"    v2 > v4    = {v2 > v4}")
    print(f"    v2 >= v4   = {v2 >= v4}")

    # 排序演示
    versions = [v3, v1, v2, v4]
    sorted_versions = sorted(versions)
    print(f"\n  排序: {versions}")
    print(f"    结果: {sorted_versions}")

    # ============================================================
    # 5. wraps - 保留原函数元信息
    # ============================================================
    print("\n" + "=" * 50)
    print("5. functools.wraps - 保留原函数元信息")
    print("=" * 50)

    # 无 wraps 的装饰器
    def decorator_no_wraps(fn):
        def wrapper(*args, **kwargs):
            """wrapper的内部文档"""
            return fn(*args, **kwargs)
        return wrapper

    # 有 wraps 的装饰器
    def decorator_with_wraps(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            """wrapper的内部文档"""
            return fn(*args, **kwargs)
        return wrapper

    # 应用装饰器
    def original():
        """原始函数的文档: 执行重要操作"""
        return "result"

    wrapped_no = decorator_no_wraps(original)
    wrapped_yes = decorator_with_wraps(original)

    print("装饰器对函数元信息的影响:")
    print(f"  原始函数:  __name__='{original.__name__}', __doc__='{original.__doc__}'")
    print(f"  无 wraps:  __name__='{wrapped_no.__name__}', __doc__='{wrapped_no.__doc__}'")
    print(f"  有 wraps:  __name__='{wrapped_yes.__name__}', __doc__='{wrapped_yes.__doc__}'")
    print(f"\n 结论: @wraps 让装饰后的函数保留原函数的 name/doc/module 等元信息")
    print(f" 详细讲解见: 04-functions/03_decorator.py")

    # ============================================================
    # 6. singledispatch - 根据参数类型分发
    # ============================================================
    print("\n" + "=" * 50)
    print("6. functools.singledispatch - 根据参数类型分发")
    print("=" * 50)

    print("@singledispatch 根据第一个参数类型调用不同实现:\n")

    test_cases = [
        "Hello World",
        42,
        [1, 2, 3, 4, 5],
        {"name": "张三", "age": 30, "city": "北京"},
        3.14,
    ]

    for val in test_cases:
        print(f"  describe({repr(val)}) -> {describe(val)}")

    print(f"\n  dispatch 注册表: {describe.registry.keys()}")
    print(f"  注意: singledispatch 仅根据第一个参数的类型分发")


if __name__ == "__main__":
    main()

# ============================================================
# 相关主题:
#   - 04-functions/03_decorator.py  → wraps 保留函数元信息的实际应用
# ============================================================
