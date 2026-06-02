"""
函数 (Function)
===============================
Python 函数: 定义与调用、参数类型(位置/关键字/默认/可变)、
返回值、文档字符串、作用域(LEGB)、闭包。
参考: https://www.runoob.com/python3/python3-function.html
"""


# ==============================
# 演示 1: 函数定义与调用
# ==============================
def demo_define_and_call():
    """演示 1: 函数定义与基本调用"""
    print("=" * 50)
    print("演示 1: 函数定义与基本调用")
    print("=" * 50)

    # 最简单的函数：无参数，无返回值
    def greet():
        """打印问候语"""  # 文档字符串 (docstring)
        print("  你好，世界！")

    # 调用函数
    greet()

    # 带参数和返回值的函数
    def add(a, b):
        """返回两个数的和"""
        return a + b

    result = add(3, 5)
    print(f"  add(3, 5) = {result}")

    # 查看函数的文档字符串
    print(f"\n  函数文档字符串:")
    print(f"    greet.__doc__  = {greet.__doc__}")
    print(f"    add.__doc__    = {add.__doc__}")

    # Python 中函数是一等公民：可以赋值给变量
    my_add = add
    print(f"\n  函数作为变量: my_add(10, 20) = {my_add(10, 20)}")


# ==============================
# 演示 2: 参数类型
# ==============================
def demo_parameters():
    """演示 2: 各种参数类型"""
    print("\n" + "=" * 50)
    print("演示 2: 参数类型详解")
    print("=" * 50)

    # 位置参数（必需参数）
    def power(base, exp):
        return base ** exp

    print(f"  位置参数: power(2, 3) = {power(2, 3)}")
    print(f"  位置参数: power(exp=4, base=2) = {power(exp=4, base=2)}  (关键字指定)")

    # 默认参数（可选参数）
    def greet(name, greeting="你好"):
        return f"{greeting}, {name}!"

    print(f"\n  默认参数: greet('张三') = {greet('张三')}")
    print(f"  默认参数: greet('John', 'Hello') = {greet('John', 'Hello')}")

    # 可变位置参数 *args — 接收任意数量的位置参数为元组
    def my_sum(*args):
        total = 0
        for num in args:
            total += num
        return total

    print(f"\n  *args: my_sum(1, 2, 3) = {my_sum(1, 2, 3)}")
    print(f"  *args: my_sum(1, 2, 3, 4, 5) = {my_sum(1, 2, 3, 4, 5)}")

    # 可变关键字参数 **kwargs — 接收任意数量的关键字参数为字典
    def print_info(**kwargs):
        for key, value in kwargs.items():
            print(f"    {key}: {value}")

    print(f"\n  **kwargs 示例:")
    print_info(name="张三", age=20, city="北京")

    # 参数组合 (顺序: 位置 -> *args -> 关键字 -> **kwargs)
    def full_func(a, b, *args, c=10, **kwargs):
        print(f"    位置参数 a={a}, b={b}")
        print(f"    *args={args}")
        print(f"    默认参数 c={c}")
        print(f"    **kwargs={kwargs}")

    print(f"\n  参数组合示例:")
    full_func(1, 2, 3, 4, 5, c=20, name="test", value=99)


# ==============================
# 演示 3: 返回值
# ==============================
def demo_return_values():
    """演示 3: 函数返回值"""
    print("\n" + "=" * 50)
    print("演示 3: 函数返回值")
    print("=" * 50)

    # 单个返回值
    def square(x):
        return x ** 2

    print(f"  square(6) = {square(6)}")

    # 返回多个值 (实际上是返回元组)
    def min_max(numbers):
        return min(numbers), max(numbers)

    result = min_max([3, 1, 4, 1, 5, 9])
    print(f"  min_max([3,1,4,1,5,9]) = {result}, 类型: {type(result)}")

    # 元组解包
    smallest, largest = min_max([3, 1, 4, 1, 5, 9])
    print(f"  解包: smallest={smallest}, largest={largest}")

    # 无显式 return 时返回 None
    def no_return():
        x = 1 + 1  # 没有 return

    result = no_return()
    print(f"\n  无 return 函数返回: {result} (类型: {type(result).__name__})")

    # 提前返回 (early return)
    def safe_divide(a, b):
        if b == 0:
            return None, "除数不能为零"
        return a / b, None

    val, err = safe_divide(10, 2)
    print(f"\n  safe_divide(10, 2) = {val}, error={err}")
    val, err = safe_divide(10, 0)
    print(f"  safe_divide(10, 0) = {val}, error={err}")


# ==============================
# 演示 4: 作用域 (LEGB)
# ==============================

# 全局变量 — 用于演示 global 关键字
_global_counter = 0

def demo_scope():
    """演示 4: 变量作用域 LEGB 规则"""
    print("\n" + "=" * 50)
    print("演示 4: 作用域 LEGB 规则")
    print("=" * 50)

    # LEGB: Local → Enclosing → Global → Built-in

    # 全局变量
    x = "global_x"

    def outer():
        # 闭包变量 (Enclosing)
        x = "enclosing_x"

        def inner():
            # 局部变量 (Local)
            x = "local_x"
            print(f"    在 inner() 中: x = '{x}'")

        inner()
        print(f"    在 outer() 中: x = '{x}'")

    outer()
    print(f"    在全局: x = '{x}'")

    # global 关键字 — 在函数内修改模块级全局变量
    def increment():
        global _global_counter
        _global_counter += 1
        print(f"    计数: {_global_counter}")

    print(f"\n  global 关键字示例:")
    # _global_counter 在模块顶层定义
    increment()
    increment()
    print(f"    最终计数: {_global_counter}")

    # nonlocal 关键字 — 在嵌套函数中修改外层函数变量
    def make_counter():
        count = 0

        def counter_func():
            nonlocal count  # 声明要修改的是外层函数的变量
            count += 1
            return count

        return counter_func

    print(f"\n  nonlocal 关键字示例 (闭包计数器):")
    my_counter = make_counter()
    print(f"    第1次: {my_counter()}")
    print(f"    第2次: {my_counter()}")
    print(f"    第3次: {my_counter()}")


# ==============================
# 演示 5: 闭包
# ==============================
def demo_closure():
    """演示 5: 闭包 (Closure)"""
    print("\n" + "=" * 50)
    print("演示 5: 闭包 (Closure)")
    print("=" * 50)

    # 闭包: 函数内部定义函数，内部函数引用外部函数的变量
    def make_multiplier(n):
        """返回一个函数，该函数将其参数乘以 n"""
        def multiplier(x):
            return x * n  # n 来自外层作用域

        return multiplier

    double = make_multiplier(2)
    triple = make_multiplier(3)

    print(f"  double(5) = {double(5)}")
    print(f"  triple(5) = {triple(5)}")

    # 查看闭包中保存的自由变量
    print(f"\n  闭包内部属性:")
    print(f"    double.__closure__[0].cell_contents = {double.__closure__[0].cell_contents}")
    print(f"    triple.__closure__[0].cell_contents = {triple.__closure__[0].cell_contents}")

    # 闭包实用场景: 创建一系列函数
    def make_power_function(exponent):
        def power(base):
            return base ** exponent
        return power

    square_func = make_power_function(2)
    cube_func = make_power_function(3)

    print(f"\n  实用场景 - 幂函数工厂:")
    print(f"    平方: square_func(5) = {square_func(5)}")
    print(f"    立方: cube_func(5) = {cube_func(5)}")
    print(f"    10次方: make_power_function(10)(2) = {make_power_function(10)(2)}")

    # 闭包陷阱: 循环中创建闭包（延迟绑定）
    print(f"\n  闭包陷阱: 循环中的延迟绑定")
    funcs = []
    for i in range(3):
        def func():
            return i  # i 是外部变量引用，不是值拷贝
        funcs.append(func)

    print(f"    [func() for func in funcs] = {[func() for func in funcs]}")
    print(f"    [!] 都是 2！因为所有闭包引用的是同一个 i (最终值)")

    # 解决方案: 使用默认参数立即绑定值
    funcs_fixed = []
    for i in range(3):
        def func(i=i):  # 默认参数在定义时求值
            return i
        funcs_fixed.append(func)

    print(f"    [func() for func in funcs_fixed] = {[func() for func in funcs_fixed]}")
    print(f"    [OK] 正确! 每个函数保存了自己的 i 值")


# ========== 主程序入口 ==========
if __name__ == "__main__":
    demo_define_and_call()
    demo_parameters()
    demo_return_values()
    demo_scope()
    demo_closure()
    print("\n[OK] 所有函数演示完成！")
