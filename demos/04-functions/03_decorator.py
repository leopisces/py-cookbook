"""
装饰器 (Decorator)
===============================
Python 装饰器: 函数装饰器、带参数装饰器、functools.wraps、
类装饰器、多个装饰器叠加、常用装饰器模式(计时/日志/权限)。
参考: https://www.runoob.com/w3cnote/python-func-decorators.html
"""

import functools
import time


# ==============================
# 演示 1: 基本函数装饰器
# ==============================
def demo_basic_decorator():
    """演示 1: 函数装饰器基本原理"""
    print("=" * 50)
    print("演示 1: 函数装饰器基本原理")
    print("=" * 50)

    # 装饰器本质上是一个函数，接受一个函数作为参数，返回一个新函数
    def my_decorator(func):
        def wrapper():
            print(f"    在 {func.__name__} 之前执行")
            result = func()
            print(f"    在 {func.__name__} 之后执行")
            return result
        return wrapper

    # 使用装饰器语法糖 @
    @my_decorator
    def say_hello():
        print("    Hello!")

    print("  调用装饰后的函数:")
    say_hello()

    # 等价于: say_hello = my_decorator(say_hello)
    print("\n  装饰器本质:")
    print("    @my_decorator")
    print("    def say_hello(): ...")
    print("    ")
    print("    等价于 -> say_hello = my_decorator(say_hello)")

    # 装饰带参数的函数
    def logging_decorator(func):
        def wrapper(*args, **kwargs):
            print(f"    调用 {func.__name__}({args}, {kwargs})")
            result = func(*args, **kwargs)
            print(f"    {func.__name__} 返回: {result}")
            return result
        return wrapper

    @logging_decorator
    def add(a, b):
        return a + b

    print(f"\n  装饰带参数的函数: add(3, 5) = {add(3, 5)}")


# ==============================
# 演示 2: functools.wraps 与保留元数据
# ==============================
def demo_functools_wraps():
    """演示 2: functools.wraps 保留函数元数据"""
    print("\n" + "=" * 50)
    print("演示 2: functools.wraps 保留函数元数据")
    print("=" * 50)

    # 不使用 @wraps 的问题
    def bad_decorator(func):
        def wrapper(*args, **kwargs):
            """wrapper 的文档"""
            return func(*args, **kwargs)
        return wrapper

    @bad_decorator
    def greet_bad(name):
        """打招呼的函数"""
        return f"你好, {name}!"

    print("  不使用 @wraps:")
    print(f"    函数名: {greet_bad.__name__}")
    print(f"    文档: {greet_bad.__doc__}")

    # 使用 @wraps 的正确方式
    def good_decorator(func):
        @functools.wraps(func)  # 保留原函数的元数据
        def wrapper(*args, **kwargs):
            """wrapper 的文档"""
            return func(*args, **kwargs)
        return wrapper

    @good_decorator
    def greet_good(name):
        """打招呼的函数"""
        return f"你好, {name}!"

    print("\n  使用 @wraps:")
    print(f"    函数名: {greet_good.__name__}")
    print(f"    文档: {greet_good.__doc__}")
    print(f"    调用: {greet_good('张三')}")

    # 始终使用 @functools.wraps(func) 保留:
    # __name__, __doc__, __module__, __qualname__, __dict__, __wrapped__


# ==============================
# 演示 3: 带参数的装饰器
# ==============================
def demo_decorator_with_args():
    """演示 3: 带参数的装饰器"""
    print("\n" + "=" * 50)
    print("演示 3: 带参数的装饰器")
    print("=" * 50)

    # 带参数的装饰器需要三层嵌套:
    # 第一层: 接收装饰器参数
    # 第二层: 接收被装饰的函数
    # 第三层: 实际的包装函数

    def repeat(times):
        """让函数重复执行指定次数"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                results = []
                for i in range(times):
                    results.append(func(*args, **kwargs))
                return results
            return wrapper
        return decorator

    @repeat(times=3)
    def say(name):
        return f"你好, {name}!"

    print(f"  @repeat(times=3): {say('张三')}")

    # 另一个例子: 延迟执行装饰器
    def delay(seconds):
        """模拟延迟执行的装饰器"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                print(f"    等待 {seconds} 秒...", end=" ")
                time.sleep(0.1)  # 实际用0.1秒演示
                print("完成!")
                return func(*args, **kwargs)
            return wrapper
        return decorator

    @delay(seconds=0.5)
    def heavy_computation():
        return "计算结果"

    print(f"\n  @delay(seconds=0.5): {heavy_computation()}")

    # 无条件装饰器: 即使没有参数也可以使用 @decorator 或 @decorator()
    def optional_args_decorator(func=None, *, prefix="[LOG]"):
        """既能 @deco 也能 @deco(prefix='...') 使用的装饰器"""
        def decorator(f):
            @functools.wraps(f)
            def wrapper(*args, **kwargs):
                print(f"    {prefix} 调用 {f.__name__}")
                return f(*args, **kwargs)
            return wrapper
        if func is None:
            return decorator  # 带参数调用
        return decorator(func)  # 不带参数调用

    @optional_args_decorator
    def func1():
        return "func1"

    @optional_args_decorator(prefix="[DEBUG]")
    def func2():
        return "func2"

    print(f"\n  可选参数装饰器: {func1()}, {func2()}")


# ==============================
# 演示 4: 类装饰器与多个装饰器叠加
# ==============================
def demo_class_decorator_and_stacking():
    """演示 4: 类装饰器与多个装饰器叠加"""
    print("\n" + "=" * 50)
    print("演示 4: 类装饰器与多个装饰器叠加")
    print("=" * 50)

    # 类装饰器: 使用 __call__ 使类实例可调用
    class CountCalls:
        """统计函数调用次数的类装饰器"""
        def __init__(self, func):
            self.func = func
            self.count = 0

        def __call__(self, *args, **kwargs):
            self.count += 1
            print(f"    第 {self.count} 次调用 {self.func.__name__}")
            return self.func(*args, **kwargs)

    @CountCalls
    def greet_cls(name):
        return f"你好, {name}!"

    print(f"  类装饰器示例:")
    greet_cls("张三")
    greet_cls("李四")
    print(f"    总调用次数: {greet_cls.count}")

    # 多个装饰器叠加 — 从下往上执行 (洋葱模型)
    print("\n  多个装饰器叠加 (洋葱模型):")

    def deco_a(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print("    [A 进入]")
            result = func(*args, **kwargs)
            print("    [A 退出]")
            return result
        return wrapper

    def deco_b(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print("    [B 进入]")
            result = func(*args, **kwargs)
            print("    [B 退出]")
            return result
        return wrapper

    @deco_a
    @deco_b
    def sandwich():
        print("    [核心函数]")

    print(f"  调用 @deco_a @deco_b 装饰的函数:")
    sandwich()
    print(f"  执行顺序: A进入 -> B进入 -> 核心 -> B退出 -> A退出")


# ==============================
# 演示 5: 常用装饰器模式
# ==============================
def demo_common_patterns():
    """演示 5: 常用装饰器模式 (计时、日志、缓存、权限)"""
    print("\n" + "=" * 50)
    print("演示 5: 常用装饰器模式")
    print("=" * 50)

    # 模式 1: 计时器
    def timer(func):
        """测量函数执行时间的装饰器"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            print(f"    {func.__name__} 耗时: {elapsed:.6f} 秒")
            return result
        return wrapper

    @timer
    def slow_function():
        # 模拟耗时操作
        total = sum(range(100000))
        return total

    result = slow_function()
    print(f"    结果: {result}")

    # 模式 2: 缓存 (简易 memoize)
    def memoize(func):
        """缓存函数结果的装饰器 (避免重复计算)"""
        cache = {}
        @functools.wraps(func)
        def wrapper(*args):
            if args not in cache:
                print(f"      计算 fibonacci({args[0]})...")
                cache[args] = func(*args)
            else:
                print(f"      从缓存获取 fibonacci({args[0]})")
            return cache[args]
        return wrapper

    @memoize
    def fibonacci(n):
        if n <= 1:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)

    print(f"\n  模式 2: 缓存 (memoize):")
    print(f"    fibonacci(10) = {fibonacci(10)}")
    print(f"    再次调用 fibonacci(10)(从缓存) = {fibonacci(10)}")

    # 模式 3: 访问控制 / 权限检查
    def require_role(role):
        """权限检查装饰器"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(user_role, *args, **kwargs):
                if user_role == role:
                    return func(user_role, *args, **kwargs)
                else:
                    return f"权限不足! 需要 {role} 角色，当前为 {user_role}"
            return wrapper
        return decorator

    @require_role("admin")
    def delete_user(user_role, username):
        return f"用户 {username} 已被删除"

    @require_role("admin")
    def view_dashboard(user_role):
        return f"显示管理面板"

    print(f"\n  模式 3: 权限检查:")
    print(f"    管理员访问: {delete_user('admin', '张三')}")
    print(f"    普通用户访问: {delete_user('user', '张三')}")


# ========== 主程序入口 ==========
if __name__ == "__main__":
    demo_basic_decorator()
    demo_functools_wraps()
    demo_decorator_with_args()
    demo_class_decorator_and_stacking()
    demo_common_patterns()
    print("\n[OK] 所有装饰器演示完成！")

# ============================================================
# 相关主题:
#   - 09-stdlib/19_functools.py  → wraps/lru_cache 等装饰器工具
# ============================================================
