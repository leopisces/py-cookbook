"""
命名空间与作用域 (Namespace & Scope)
===============================
Python 命名空间与作用域: LEGB 规则详解、global/nonlocal、
locals()/globals()、闭包中的变量绑定、作用域陷阱。
参考: https://www.runoob.com/python3/python3-namespace-scope.html
"""


# ==============================
# 全局变量（用于演示）
# ==============================
global_x = "我是全局变量 global_x"
global_counter = 0


def demo_namespace_concept():
    """演示 1: 命名空间概念"""
    print("=" * 50)
    print("演示 1: 命名空间概念")
    print("=" * 50)

    # 命名空间 (Namespace): 名字到对象的映射，类似字典
    # Python 中命名空间以字典形式实现

    # 三种主要命名空间:
    # 1. 内置命名空间 (Built-in): Python 内置的名字，如 print, len, range
    # 2. 全局命名空间 (Global): 模块级别的名字
    # 3. 局部命名空间 (Local): 函数内部的局部名字

    print("  Python 的三种命名空间:")
    print("    1. 内置命名空间 (Built-in): Python 启动时创建，一直存在")
    print("    2. 全局命名空间 (Global): 模块导入时创建，模块结束时销毁")
    print("    3. 局部命名空间 (Local): 函数调用时创建，函数返回时销毁")

    # 使用 __builtins__ 查看内置命名空间
    builtin_names = dir(__builtins__)
    print(f"\n  内置命名空间中的名字 (前10个): {builtin_names[:10]}")

    # 不同命名空间可以有相同的名字（不冲突）
    # 比如全局和局部都可以有变量 x
    x = "全局的 x"  # 全局命名空间

    def show_x():
        x = "局部的 x"  # 局部命名空间（不覆盖全局的 x）
        print(f"    在函数内部: x = '{x}'")

    show_x()
    print(f"    在函数外部: x = '{x}'")

    # 命名空间的生命周期
    print(f"\n  命名空间生命周期:")
    print(f"    Built-in: Python 解释器启动 -> 解释器退出")
    print(f"    Global:   模块被导入 -> 解释器退出")
    print(f"    Local:    函数被调用 -> 函数返回/异常")


def demo_legb_rule():
    """演示 2: LEGB 规则详解"""
    print("\n" + "=" * 50)
    print("演示 2: LEGB 规则 (变量查找顺序)")
    print("=" * 50)

    # LEGB: Local -> Enclosing -> Global -> Built-in
    # 当访问一个变量时，Python 按此顺序搜索

    print("  变量查找顺序 LEGB:")
    print("    L (Local)        -> 函数/方法内部的变量")
    print("    E (Enclosing)    -> 外层函数的变量 (闭包)")
    print("    G (Global)       -> 模块级别的变量")
    print("    B (Built-in)     -> Python 内置的变量/函数")
    print()

    # 演示 LEGB 优先级
    x = "Global"  # G

    def outer():
        x = "Enclosing"  # E

        def inner():
            x = "Local"  # L
            print(f"    inner() 中的 x = '{x}' (Local 优先)")

        inner()
        print(f"    outer() 中的 x = '{x}' (Enclosing)")

    outer()
    print(f"    全局的 x = '{x}' (Global)")

    # 内置命名空间是最后一层
    print(f"\n  Built-in 示例:")
    print(f"    len('hello') = {len('hello')}  ← len 来自 Built-in")

    # 可以覆盖 Built-in (但不推荐!)
    # len = 5  # 这会覆盖内置的 len

    # 实际演示: 每层一个不同变量名
    built_in_example = "不要这样做"  # 仅为说明

    def demo_all_levels():
        # L: 局部变量
        local_var = "L"
        print(f"    Local 变量: {local_var}")

        # E: 闭包变量
        def enclosed():
            enclosed_var = "E"
            print(f"    Enclosing 变量: {enclosed_var}")
        enclosed()

        # G: 全局变量
        print(f"    Global 变量: {global_x}")

        # B: 内置变量
        print(f"    Built-in: type(42) = {type(42).__name__}")

    demo_all_levels()


def demo_global_and_nonlocal():
    """演示 3: global 和 nonlocal 关键字"""
    print("\n" + "=" * 50)
    print("演示 3: global 和 nonlocal 关键字")
    print("=" * 50)

    # global — 在函数内声明要使用/修改全局变量
    print("  global 关键字:")

    global_var = "初始值"

    def modify_global():
        global global_var  # 声明要修改全局变量
        global_var = "已修改"
        print(f"    函数内修改后: global_var = '{global_var}'")

    print(f"    调用前: global_var = '{global_var}'")
    modify_global()
    print(f"    调用后: global_var = '{global_var}'")

    # 没有 global 关键字的情况 (只读不报错)
    def read_global():
        print(f"    读取全局变量 (不需要 global): {global_var}")

    print(f"\n  读取全局变量不需要 global:")
    read_global()

    # 但是赋值会创建新的局部变量（不会修改全局变量）
    def try_modify_without_global():
        global_var = "局部值"  # 创建了一个新的局部变量!
        print(f"    函数内的 global_var = '{global_var}' (局部变量)")

    print(f"\n  没有 global 的赋值:")
    try_modify_without_global()
    print(f"    函数外的 global_var 仍然是 = '{global_var}'")

    # nonlocal — 在嵌套函数中修改外层函数的变量
    print(f"\n  nonlocal 关键字:")

    def outer_func():
        outer_var = "外层初始值"
        print(f"    outer_func 的 outer_var = '{outer_var}'")

        def inner_func():
            nonlocal outer_var  # 声明要修改外层函数的变量
            outer_var = "内层修改后的值"
            print(f"    inner_func 修改后: outer_var = '{outer_var}'")

        inner_func()
        print(f"    inner_func 返回后: outer_var = '{outer_var}'")

    outer_func()

    # nonlocal 作用范围
    print(f"\n  nonlocal 查找顺序: 从内向外找最近的 Enclosing")
    def outer1():
        x = "outer1 的 x"
        def outer2():
            x = "outer2 的 x"
            def inner():
                nonlocal x  # 找最近的外层 — outer2 的 x
                x = "inner 修改了 outer2 的 x"
                print(f"    inner 中: x = '{x}'")
            inner()
            print(f"    outer2 中: x = '{x}'")
        outer2()
        print(f"    outer1 中: x = '{x}'")
    outer1()


def demo_locals_globals():
    """演示 4: locals() 和 globals() 内置函数"""
    print("\n" + "=" * 50)
    print("演示 4: locals() 和 globals()")
    print("=" * 50)

    # globals() — 返回全局命名空间字典
    print("  globals() 返回的全局变量 (部分):")
    global_dict = globals()
    # 只显示我们定义的
    our_globals = {
        k: v for k, v in global_dict.items()
        if not k.startswith("_")
        and k in ["global_x", "global_counter"]
    }
    for k, v in our_globals.items():
        display = repr(v)[:50] + "..." if len(repr(v)) > 50 else repr(v)
        print(f"    {k}: {display}")

    # locals() — 返回局部命名空间字典
    def demo_local():
        local_a = 10
        local_b = "hello"
        local_dict = locals()
        print(f"\n  locals() 返回的局部变量:")
        for k, v in local_dict.items():
            if k in ["local_a", "local_b"]:
                print(f"    {k}: {v} = {repr(v)}")

        # 修改 locals() 字典在函数内部不保证生效 (CPython 中无效)
        locals()["local_a"] = 999
        print(f"    尝试通过 locals() 修改 local_a: {local_a} (未改变!)")

    demo_local()

    # 在模块顶层，locals() 等于 globals()
    print(f"\n  在模块顶层: locals() is globals() -> {locals() is globals()}")

    # globals() 可以用于动态创建/修改全局变量
    globals()["dynamic_global"] = "动态创建的全局变量"
    print(f"  通过 globals() 动态创建: dynamic_global = '{dynamic_global}'")

    # dir() — 返回当前作用域的名字列表
    print(f"\n  dir() 查看当前作用域 (前15个):")
    print(f"    {dir()[:15]}")

    # vars() — 返回对象的 __dict__ (如果存在)
    class Person:
        def __init__(self, name, age):
            self.name = name
            self.age = age

    p = Person("张三", 20)
    print(f"\n  vars(p) = {vars(p)}")
    # vars() 无参数时等同于 locals()


def demo_scope_traps():
    """演示 5: 作用域常见陷阱与最佳实践"""
    print("\n" + "=" * 50)
    print("演示 5: 作用域常见陷阱")
    print("=" * 50)

    # 陷阱 1: 在函数内赋值时自动创建局部变量
    print("  陷阱 1: 赋值即声明为局部变量")
    x = 100

    def trap1():
        # print(x)  # [X] UnboundLocalError! 因为后面的 x = 200 让 Python
        #           #    认为 x 是局部变量，但 print 时还没赋值
        x = 200  # 这里让 x 成为局部变量
        print(f"    函数内的 x = {x} (局部变量)")

    trap1()
    print(f"    函数外的 x = {x} (全局变量不受影响)")
    print(f"    解释: Python 在编译时确定变量作用域，赋值即声明为局部")

    # 陷阱 2: 可变对象的修改不需要 global
    print(f"\n  陷阱 2: 修改可变对象的内容不需要 global")
    my_list = [1, 2, 3]

    def modify_list():
        my_list.append(4)  # [OK] 修改内容，不需要 global
        # my_list = [5, 6, 7]  # [X] 重新赋值，会创建局部变量（需要 global）

    print(f"    修改前: {my_list}")
    modify_list()
    print(f"    修改后: {my_list}")
    print(f"    规则: 修改对象内部 (如 append) OK，重新赋值变量名 NO")

    # 陷阱 3: 闭包中的变量绑定 (延迟绑定)
    print(f"\n  陷阱 3: 闭包延迟绑定")

    # 错误示例
    closures_wrong = []
    for i in range(3):
        def inner_wrong():
            return i  # 引用的是循环变量 i (最终值)
        closures_wrong.append(inner_wrong)

    results_wrong = [f() for f in closures_wrong]
    print(f"    错误方式: {results_wrong} (都是 2)")

    # 正确方式 1: 使用默认参数绑定当前值
    closures_fixed1 = []
    for i in range(3):
        def inner_fixed(i=i):  # 默认参数在定义时求值
            return i
        closures_fixed1.append(inner_fixed)

    results_fixed1 = [f() for f in closures_fixed1]
    print(f"    修复方式1 (默认参数): {results_fixed1} [OK]")

    # 正确方式 2: 使用工厂函数
    def make_func(val):
        def inner():
            return val  # val 是工厂函数的参数，每次调用都是新的
        return inner

    closures_fixed2 = [make_func(i) for i in range(3)]
    results_fixed2 = [f() for f in closures_fixed2]
    print(f"    修复方式2 (工厂函数): {results_fixed2} [OK]")

    # 陷阱 4: 循环中的 lambda 同样存在延迟绑定
    print(f"\n  陷阱 4: lambda 循环中的延迟绑定")

    lambdas_wrong = [lambda: i for i in range(3)]
    print(f"    错误: {[l() for l in lambdas_wrong]}")

    lambdas_fixed = [lambda i=i: i for i in range(3)]
    print(f"    修复: {[l() for l in lambdas_fixed]}")

    # 陷阱 5: global 和 nonlocal 的作用域限制
    print(f"\n  陷阱 5: nonlocal 不能用在模块层级")
    print(f"    nonlocal 只能在函数内的函数中使用")
    print(f"    global 可以在任何函数中使用")


# ========== 主程序入口 ==========
if __name__ == "__main__":
    demo_namespace_concept()
    demo_legb_rule()
    demo_global_and_nonlocal()
    demo_locals_globals()
    demo_scope_traps()
    print("\n[OK] 所有命名空间与作用域演示完成！")
