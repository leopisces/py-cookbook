"""
迭代器与生成器 (Iterator & Generator)
===============================
Python 迭代器与生成器: 可迭代对象与迭代器协议、
iter()/next()、生成器函数(yield)、生成器表达式、
yield from、生成器管道。
参考: https://www.runoob.com/python3/python3-iterator-generator.html
"""

from collections.abc import Iterable, Iterator
import sys


def demo_iterable_and_iterator():
    """演示 1: 可迭代对象与迭代器协议"""
    print("=" * 50)
    print("演示 1: 可迭代对象与迭代器")
    print("=" * 50)

    # 可迭代对象 (Iterable): 实现了 __iter__() 方法，返回迭代器
    # 迭代器 (Iterator): 实现了 __iter__() 和 __next__() 方法

    # 列表是可迭代对象
    my_list = [1, 2, 3]
    print(f"  my_list = {my_list}")
    print(f"  isinstance(my_list, Iterable) = {isinstance(my_list, Iterable)}")
    print(f"  isinstance(my_list, Iterator) = {isinstance(my_list, Iterator)}")

    # 通过 iter() 获取迭代器
    list_iter = iter(my_list)
    print(f"\n  list_iter = iter(my_list)")
    print(f"  isinstance(list_iter, Iterator) = {isinstance(list_iter, Iterator)}")

    # 使用 next() 逐个获取元素
    print(f"\n  逐个获取迭代器元素:")
    print(f"    next(list_iter) = {next(list_iter)}")
    print(f"    next(list_iter) = {next(list_iter)}")
    print(f"    next(list_iter) = {next(list_iter)}")

    # 迭代器到达末尾后抛出 StopIteration
    try:
        next(list_iter)
    except StopIteration:
        print("    next(list_iter) -> StopIteration (迭代器已耗尽)")

    # for 循环本质上是 iter() + next() 的语法糖
    print(f"\n  for 循环本质:")
    print(f"    for item in iterable:")
    print(f"        # 等价于:")
    print(f"        # iterator = iter(iterable)")
    print(f"        # while True:")
    print(f"        #     try: item = next(iterator)")
    print(f"        #     except StopIteration: break")

    # 自定义可迭代对象
    class CountDown:
        """自定义倒计时迭代器"""
        def __init__(self, start):
            self.start = start

        def __iter__(self):
            return self

        def __next__(self):
            if self.start <= 0:
                raise StopIteration
            self.start -= 1
            return self.start + 1

    print(f"\n  自定义迭代器 (CountDown(3)):")
    for num in CountDown(3):
        print(f"    倒计时: {num}")


def demo_generator_function():
    """演示 2: 生成器函数 — yield"""
    print("\n" + "=" * 50)
    print("演示 2: 生成器函数 (yield)")
    print("=" * 50)

    # 生成器函数: 使用 yield 而不是 return
    # 调用生成器函数返回生成器对象（一个迭代器）

    def simple_generator():
        """最简单的生成器"""
        print("    生成器开始执行")
        yield 1
        print("    恢复执行")
        yield 2
        print("    恢复执行")
        yield 3
        print("    生成器结束")

    gen = simple_generator()
    print(f"  创建生成器: {type(gen).__name__}")

    print(f"\n  逐次获取值:")
    print(f"    next(gen) -> {next(gen)}")
    print(f"    next(gen) -> {next(gen)}")
    print(f"    next(gen) -> {next(gen)}")

    # yield 与 return 的区别
    print(f"\n  yield vs return:")
    print(f"    yield:  暂停函数，保存状态，可多次产生值")
    print(f"    return: 结束函数，返回一个值")

    # 实用示例: 斐波那契数列生成器
    def fibonacci_generator(n):
        """生成前 n 个斐波那契数"""
        a, b = 0, 1
        for _ in range(n):
            yield a
            a, b = b, a + b

    print(f"\n  斐波那契数列生成器 (前10个):")
    fib = list(fibonacci_generator(10))
    print(f"    {fib}")

    # 无限生成器 (惰性求值，不会占用大量内存)
    def infinite_counter(start=0):
        """无限计数器生成器"""
        while True:
            yield start
            start += 1

    print(f"\n  无限生成器 (取前5个):")
    counter = infinite_counter(1)
    first_five = [next(counter) for _ in range(5)]
    print(f"    {first_five}")

    # 生成器也支持 send() 方法 (双向通信)
    def echo_generator():
        """接收发送值的生成器"""
        received = yield "准备好了，发送一个值吧"
        yield f"收到: {received}"

    echo = echo_generator()
    print(f"\n  生成器 send() 双向通信:")
    initial = next(echo)  # 启动生成器，运行到第一个 yield
    print(f"    生成器说: {initial}")
    try:
        response = echo.send("你好")
        print(f"    发送 '你好' 后生成器说: {response}")
    except StopIteration:
        pass


def demo_generator_expression():
    """演示 3: 生成器表达式"""
    print("\n" + "=" * 50)
    print("演示 3: 生成器表达式")
    print("=" * 50)

    # 生成器表达式: (表达式 for 变量 in 可迭代对象 if 条件)
    # 与列表推导式类似，但使用圆括号，惰性求值

    # 对比: 列表推导式 vs 生成器表达式
    squares_list = [x ** 2 for x in range(10)]
    squares_gen = (x ** 2 for x in range(10))

    print(f"  列表推导式: {squares_list}")
    print(f"  生成器表达式: {type(squares_gen).__name__}")
    print(f"  生成器表达式内容: {list(squares_gen)}")

    # 内存效率对比
    big_list = [x for x in range(100000)]
    big_gen = (x for x in range(100000))
    print(f"\n  内存占用 (range(100000)):")
    print(f"    列表推导式: {sys.getsizeof(big_list):,} bytes")
    print(f"    生成器表达式: {sys.getsizeof(big_gen):,} bytes")
    print(f"    差距: 约 {sys.getsizeof(big_list) // sys.getsizeof(big_gen)}x")

    # 生成器表达式可以直接传给接受可迭代对象的函数
    total = sum(x ** 2 for x in range(1, 101))
    print(f"\n  sum(x**2 for x in range(1,101)) = {total}")

    # 当生成器表达式是函数的唯一参数时，可以省略外层括号
    print(f"  max(x for x in range(10)) = {max(x for x in range(10))}")
    print(f"  min(x for x in range(1, 100)) = {min(x for x in range(1, 100))}")


def demo_yield_from():
    """演示 4: yield from — 委托生成器"""
    print("\n" + "=" * 50)
    print("演示 4: yield from 委托生成器")
    print("=" * 50)

    # yield from iterable: 将迭代委托给另一个迭代器/生成器

    # 传统方式: 手动迭代子生成器
    def chain_generators_manual(*iterables):
        """传统方式串联多个可迭代对象"""
        for it in iterables:
            for item in it:
                yield item

    # 使用 yield from: 更简洁
    def chain_generators(*iterables):
        """使用 yield from 串联多个可迭代对象"""
        for it in iterables:
            yield from it

    result1 = list(chain_generators_manual([1, 2], "AB", (10, 20)))
    result2 = list(chain_generators([1, 2], "AB", (10, 20)))
    print(f"  传统方式: {result1}")
    print(f"  yield from: {result2}")

    # yield from 还可以处理 send/throw/close
    def sub_generator():
        """子生成器"""
        received = yield 1
        yield received * 2

    def delegating_generator():
        """委托生成器"""
        result = yield from sub_generator()
        yield result + 100

    dg = delegating_generator()
    print(f"\n  委托生成器示例:")
    print(f"    next() -> {next(dg)}")
    try:
        print(f"    send(5) -> {dg.send(5)}")
    except StopIteration:
        pass

    # yield from 用于展平嵌套结构
    def flatten(nested_list):
        """展平嵌套列表 (一层)"""
        for sublist in nested_list:
            yield from sublist

    nested = [[1, 2], [3, 4, 5], [6]]
    print(f"\n  展平嵌套列表: {list(flatten(nested))}")

    # 递归展平任意深度
    def deep_flatten(nested):
        """递归展平任意深度的嵌套结构"""
        for item in nested:
            if isinstance(item, (list, tuple)):
                yield from deep_flatten(item)
            else:
                yield item

    deep = [1, [2, [3, 4], 5], [6, [7, [8]]]]
    print(f"  递归展平: {list(deep_flatten(deep))}")


def demo_generator_pipeline():
    """演示 5: 生成器管道 (Generator Pipeline)"""
    print("\n" + "=" * 50)
    print("演示 5: 生成器管道")
    print("=" * 50)

    # 生成器管道: 多个生成器串联，数据流经每个阶段处理
    # 惰性求值: 每个元素被逐个处理完成整个管道，而不是一次处理一批

    # 管道阶段 1: 读取数据 (模拟)
    def read_data():
        """生成 1~20 的数字"""
        for i in range(1, 21):
            yield i

    # 管道阶段 2: 过滤偶数
    def filter_even(numbers):
        """保留偶数"""
        for n in numbers:
            if n % 2 == 0:
                yield n

    # 管道阶段 3: 平方
    def square(numbers):
        """计算平方"""
        for n in numbers:
            yield n ** 2

    # 管道阶段 4: 限制数量
    def take(numbers, count):
        """取前 count 个"""
        for i, n in enumerate(numbers):
            if i >= count:
                break
            yield n

    # 组合管道
    print("  生成器管道: 数据 -> 过滤偶数 -> 平方 -> 取前5个")
    pipeline = take(square(filter_even(read_data())), 5)
    print(f"  结果: {list(pipeline)}")

    # 显示管道中每一步的数据流
    print(f"\n  逐步展示管道执行过程:")
    print(f"  read_data()  -> {list(read_data())[:5]}... (1~20)")
    print(f"  filter_even -> {list(filter_even(read_data()))}  (只保留偶数)")
    print(f"  square      -> {list(square(filter_even(read_data())))}  (平方)")
    print(f"  take(5)     -> {list(take(square(filter_even(read_data())), 5))}  (取前5个)")

    # 管道模式的好处
    print(f"\n  生成器管道的优点:")
    print(f"    1. 惰性求值 — 不会一次性加载全部数据到内存")
    print(f"    2. 可组合性 — 每个阶段独立开发测试")
    print(f"    3. 可读性 — 数据处理流程清晰")
    print(f"    4. 内存高效 — 适合处理大型数据集")


# ========== 主程序入口 ==========
if __name__ == "__main__":
    demo_iterable_and_iterator()
    demo_generator_function()
    demo_generator_expression()
    demo_yield_from()
    demo_generator_pipeline()
    print("\n[OK] 所有迭代器与生成器演示完成！")

# ============================================================
# 相关主题:
#   - 03-control-flow/04_comprehensions.py  → 推导式与生成器表达式的对比
# ============================================================
