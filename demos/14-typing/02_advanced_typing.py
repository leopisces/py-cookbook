"""
高级类型系统 — Python Typing 深度进阶
========================================
Python 高级类型特性：TypeVar 泛型、Protocol 结构化子类型、
ParamSpec 泛型可调用对象、TypeGuard/TypeIs 类型窄化、
@overload 重载、cast/TYPE_CHECKING、自定义泛型容器。

学习目标：
  - 掌握 TypeVar 与 Generic 编写泛型类和函数
  - 理解 Protocol 如何实现结构化子类型（鸭子类型）
  - 学会 ParamSpec 精确注解装饰器和高阶函数
  - 掌握 TypeGuard/TypeIs 实现类型窄化
  - 熟悉 @overload 为函数提供多个类型签名
  - 理解 cast 与 TYPE_CHECKING 的运行时/检查时差异
  - 能够编写自定义泛型容器
  - 了解 reveal_type 等 mypy 调试技巧
  - 总结实际项目中的 typing 最佳实践

参考: https://docs.python.org/zh-cn/3/library/typing.html
"""

from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Generic,
    Protocol,
    TypeVar,
    cast,
    overload,
    runtime_checkable,
)

# 尝试导入 Python 3.12+ 的特性，不存在则优雅降级
try:
    from typing import TypeAliasType
except ImportError:
    TypeAliasType = None  # type: ignore[assignment]

try:
    from typing import TypeGuard
except ImportError:
    TypeGuard = None  # type: ignore[assignment]


# ========== 演示 1: TypeVar 与泛型函数/类 ==========
def demo_typevar_generic():
    """演示 1: TypeVar 定义泛型函数和泛型类"""
    print("=" * 50)
    print("演示 1: TypeVar 与泛型 (Generic)")
    print("=" * 50)

    # TypeVar — 定义类型变量（泛型参数）
    T = TypeVar("T")

    # 泛型函数：类型变量 T 在调用时确定具体类型
    def first_item(items: list[T]) -> T:
        """返回列表的第一个元素，保持元素类型"""
        return items[0]

    # 类型检查器会根据传入的 list 类型推断 T
    nums: list[int] = [1, 2, 3, 4, 5]
    words: list[str] = ["hello", "world", "python"]
    mixed: list[int | str] = [1, "two", 3]

    print(f"  first_item({nums})  = {first_item(nums)}   → T = int")
    print(f"  first_item({words})  = '{first_item(words)}'  → T = str")
    print(f"  first_item({mixed})  = {first_item(mixed)}   → T = int|str")

    # 泛型函数 — 获取字典的键列表（保持类型）
    def get_keys(d: dict[T, object]) -> list[T]:
        """获取字典的所有键"""
        return list(d.keys())

    scores: dict[str, int] = {"Alice": 95, "Bob": 88}
    ids: dict[int, str] = {1: "Alice", 2: "Bob"}
    print(f"\n  get_keys({scores}) = {get_keys(scores)}  → list[str]")
    print(f"  get_keys({ids})    = {get_keys(ids)}     → list[int]")

    # 泛型类 — 使用 Generic[T] 创建类型安全的容器
    K = TypeVar("K")
    V = TypeVar("V")

    class Pair(Generic[K, V]):
        """一个键值对泛型容器"""
        def __init__(self, key: K, value: V) -> None:
            self.key = key
            self.value = value

        def __repr__(self) -> str:
            return f"Pair(key={self.key!r}, value={self.value!r})"

        def swap(self) -> Pair[V, K]:
            """交换键值（返回新 Pair，类型也交换）"""
            return Pair(self.value, self.key)

    p1 = Pair("name", "Alice")           # Pair[str, str]
    p2 = Pair(1, 3.14)                   # Pair[int, float]
    p3 = Pair("user_id", 42)             # Pair[str, int]

    print(f"\n  {p1}")
    print(f"  {p2}")
    print(f"  {p3}")
    swapped = p3.swap()                  # Pair[int, str]
    print(f"  p3.swap() = {swapped}")

    print()


# ========== 演示 2: 多 TypeVar 与约束/上界 ==========
def demo_typevar_constraints():
    """演示 2: TypeVar 的 bound（上界）与 constraints（约束）"""
    print("=" * 50)
    print("演示 2: TypeVar 的上界 (bound) 与约束 (constraints)")
    print("=" * 50)

    # bound — 类型变量必须是某个类型的子类型（上界）
    T_num = TypeVar("T_num", bound=int | float)

    def double(value: T_num) -> T_num:
        """将数值翻倍，保持原类型"""
        return value * 2  # type: ignore[return-value]

    print("  【bound 上界示例】")
    print(f"    double(5)     = {double(5)}       (T_num = int)")
    print(f"    double(3.14)  = {double(3.14)}    (T_num = float)")
    print("    double('hello') → mypy 会报错，因为 str 不是 int|float")

    # 对比：有 bound 的 TypeVar 只接受该类型及其子类型
    T_comparable = TypeVar("T_comparable", bound="SupportsLessThan")

    # Python 中任何支持 < 的类型都可以
    class SupportsLessThan(Protocol):
        def __lt__(self, other: object) -> bool: ...

    def minimum(a: T_comparable, b: T_comparable) -> T_comparable:
        """返回两个值中较小的那个"""
        return a if a < b else b

    print(f"\n    minimum(10, 20)   = {minimum(10, 20)}")
    print(f"    minimum('a', 'z') = {minimum('a', 'z')}")
    print(f"    minimum(3.14, 2.71)= {minimum(3.14, 2.71)}")

    # constraints — 类型变量仅限于指定的几个类型（不常用）
    T_str_bytes = TypeVar("T_str_bytes", str, bytes)

    def concat(a: T_str_bytes, b: T_str_bytes) -> T_str_bytes:
        """连接两个同类型的字符串或字节序列"""
        return a + b

    print("\n  【constraints 约束示例】")
    print(f"    concat('hello', 'world') = {concat('hello', 'world')}")
    print(f"    concat(b'ab', b'cd')     = {concat(b'ab', b'cd')}")
    # concat('hello', b'world') → mypy 报错，str 和 bytes 不能混用

    print()


# ========== 演示 3: Protocol 与结构化子类型 ==========
def demo_protocol():
    """演示 3: Protocol — 结构化子类型（鸭子类型的静态版本）"""
    print("=" * 50)
    print("演示 3: Protocol 结构化子类型")
    print("=" * 50)

    # Protocol 允许基于结构（有哪些方法/属性）而非继承关系来确定类型兼容性
    # 这就是"如果你走路像鸭子，叫起来像鸭子，那你就是鸭子"

    # 定义一个 Protocol — 可飞行的事物
    class Flyable(Protocol):
        """任何有 fly() 方法的对象都符合此协议"""
        def fly(self) -> str: ...

    class Bird:
        """鸟 — 明确实现了 Flyable 协议"""
        def fly(self) -> str:
            return "鸟儿展翅高飞!"

    class Airplane:
        """飞机 — 没有继承 Flyable，但结构上满足协议"""
        def fly(self) -> str:
            return "飞机引擎轰鸣起飞!"

    class Superman:
        """超人 — 也有 fly 方法"""
        def fly(self) -> str:
            return "超人一飞冲天!"

        def laser_eyes(self) -> str:
            return "热视线!"

    # 接受任何满足 Flyable 协议的对象
    def take_off(flyer: Flyable) -> str:
        """起飞！（接受任何实现了 fly() 方法的对象）"""
        return flyer.fly()

    bird = Bird()
    plane = Airplane()
    clark = Superman()

    print(f"  take_off(bird):   {take_off(bird)}")
    print(f"  take_off(plane):  {take_off(plane)}")
    print(f"  take_off(superman): {take_off(clark)}")

    # Protocol vs ABC 的区别
    print("\n  Protocol vs ABC 对比:")
    print("    ABC:    需要显式继承或 register，强调'是什么'")
    print("    Protocol: 只看结构（方法/属性），强调'能做什么'")
    print("    Protocol 更符合 Python 的鸭子类型哲学")

    # 组合多个 Protocol
    class Drawable(Protocol):
        def draw(self) -> str: ...

    class Clickable(Protocol):
        def click(self) -> str: ...

    class Button:  # 不需要显式继承任何 Protocol
        def draw(self) -> str:
            return "绘制按钮"

        def click(self) -> str:
            return "按钮被点击"

    # 函数接受同时满足两个协议的对象
    def render_ui(widget: Flyable | Drawable) -> str:
        """渲染 UI 组件"""
        if hasattr(widget, "fly"):
            return widget.fly()  # type: ignore[union-attr]
        return widget.draw()  # type: ignore[union-attr]

    btn = Button()
    print(f"\n  render_ui(Button): {render_ui(btn)}")

    # @runtime_checkable — 让 Protocol 可以在运行时用 isinstance 检查
    @runtime_checkable
    class Named(Protocol):
        name: str

    class Person:
        def __init__(self, name: str) -> None:
            self.name = name

    p = Person("Alice")
    print(f"\n  isinstance(Person('Alice'), Named) = {isinstance(p, Named)}")

    print()


# ========== 演示 4: ParamSpec 与 Callable 泛型 ==========
def demo_paramspec():
    """演示 4: ParamSpec — 精确捕获可调用对象的参数签名"""
    print("=" * 50)
    print("演示 4: ParamSpec 泛型可调用对象")
    print("=" * 50)

    # ParamSpec (Python 3.10+): 精准捕获被装饰函数的参数类型
    # 让装饰器的返回函数和原函数有完全一致的参数签名

    # 没有 ParamSpec 时的痛点 — 我们只能知道是个 Callable
    # 有 ParamSpec 时 — 参数签名被完整保留

    print("  【ParamSpec 的核心价值】")
    print("    - 装饰器是最常见的 ParamSpec 使用场景")
    print("    - 保留了被装饰函数的完整参数类型签名")
    print("    - IDE 可以准确提示参数、类型检查器可以准确检查")

    # 模拟一个带类型注解的 ParamSpec 装饰器模式
    # 注意：由于 ParamSpec 主要用于类型检查层面，
    # 这里展示其概念和使用模式

    # 传统装饰器：丢失了参数类型信息
    def logging_decorator_simple(func: Callable[..., object]) -> Callable[..., object]:
        """简单装饰器 — 丢失了被装饰函数的参数类型信息"""
        def wrapper(*args: object, **kwargs: object) -> object:
            print(f"      调用 {func.__name__}(...)", end="")
            result = func(*args, **kwargs)
            print(f" → {result}")
            return result
        return wrapper

    @logging_decorator_simple
    def add_with_log(a: int, b: int) -> int:
        return a + b

    @logging_decorator_simple
    def greet_with_log(name: str, greeting: str = "Hello") -> str:
        return f"{greeting}, {name}!"

    print(f"\n    add_with_log(3, 5) = {add_with_log(3, 5)}")
    print(f"    greet_with_log('World') = {greet_with_log('World')}")

    # 如果要保留参数类型信息，在 Python 3.10+ 中应使用 ParamSpec：
    # from typing import ParamSpec
    # P = ParamSpec("P")
    # def typed_decorator(func: Callable[P, R]) -> Callable[P, R]:
    #     @functools.wraps(func)
    #     def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
    #         ...
    #         return func(*args, **kwargs)
    #     return wrapper
    print("\n  【ParamSpec 语法示例 (注释)】")
    print("    P = ParamSpec('P')")
    print("    def decorator(func: Callable[P, R]) -> Callable[P, R]:")
    print("        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:")
    print("            ...")
    print("            return func(*args, **kwargs)")
    print("        return wrapper")

    # ParamSpec 实战 — 计时装饰器（概念展示）
    import time as _time
    import functools

    def timer(func: Callable[..., object]) -> Callable[..., object]:
        """计时装饰器 — 测量函数执行时间"""
        @functools.wraps(func)
        def wrapper(*args: object, **kwargs: object) -> object:
            start = _time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = _time.perf_counter() - start
            print(f"      [{func.__name__}] 耗时: {elapsed:.6f}s")
            return result
        return wrapper

    @timer
    def slow_add(a: int, b: int) -> int:
        _time.sleep(0.001)  # 模拟耗时操作
        return a + b

    print(f"\n    slow_add(10, 20) = {slow_add(10, 20)}")

    print()


# ========== 演示 5: TypeGuard / TypeIs 类型窄化 ==========
def demo_typeguard():
    """演示 5: TypeGuard 与 TypeIs — 类型窄化（type narrowing）"""
    print("=" * 50)
    print("演示 5: TypeGuard / TypeIs 类型窄化")
    print("=" * 50)

    # TypeGuard (Python 3.10+): 告诉类型检查器 "如果返回 True，参数就一定是某类型"
    # TypeIs   (Python 3.13+): 更精确的版本，也处理返回 False 的情况

    print("  【类型窄化的意义】")
    print("    在 if isinstance(x, str) 这种检查后")
    print("    类型检查器自动将 x 的类型从 X 窄化为 str")
    print("    TypeGuard/TypeIs 让自定义函数也能实现同样的效果")

    # Python 内置的 isinstance 已经实现了类型窄化
    def process(value: int | str) -> int:
        """处理数值或字符串 — isinstance 自动窄化类型"""
        if isinstance(value, str):
            # 这里类型检查器知道 value 是 str
            return len(value)
        else:
            # 这里类型检查器知道 value 是 int
            return value

    print(f"  process('hello')  = {process('hello')}  (str → len)")
    print(f"  process(42)       = {process(42)}       (int → 直接返回)")

    # 自定义类型守卫 — 模式演示
    # 注意：TypeGuard 在 Python 3.10 typing 中存在，
    # 但在某些旧版本 mypy 中可能不支持
    # 这里用注释演示概念

    print("\n  【TypeGuard 概念演示 (注释)】")
    print("    from typing import TypeGuard")
    print("")
    print("    def is_string_list(values: list[object]) -> TypeGuard[list[str]]:")
    print("        '''检查列表中的所有元素都是字符串'''")
    print("        return all(isinstance(v, str) for v in values)")
    print("")
    print("    def process_list(data: list[int | str]):")
    print("        if is_string_list(data):")
    print("            # data 的类型被窄化为 list[str]")
    print("            return ','.join(data)  # 安全!")
    print("        else:")
    print("            # data 的类型被窄化为 list[int]")
    print("            return sum(data)  # 安全!")

    # 实际实现 is_string_list (不依赖 TypeGuard 也能运行)
    def is_string_list(values: list[object]) -> bool:
        """运行时检查是否全是字符串"""
        return all(isinstance(v, str) for v in values)

    def process_list(data: list[int | str]) -> str:
        """处理混合类型列表"""
        if is_string_list(data):
            return ",".join(data)  # type: ignore[arg-type]
        else:
            return f"总和: {sum(data)}"  # type: ignore[arg-type]

    print(f"\n    process_list(['a','b','c']) = {process_list(['a', 'b', 'c'])}")
    print(f"    process_list([1, 2, 3])      = {process_list([1, 2, 3])}")

    # TypeIs (Python 3.13+): 更精确的二元窄化
    # TypeGuard 只告诉我们 True 时的情况
    # TypeIs 告诉类型检查器 True 和 False 两种情况的类型
    print("\n  【TypeIs (Python 3.13+) 对比】")
    print("    TypeGuard[T]: True 时窄化为 T，False 时不做窄化")
    print("    TypeIs[T]:    True 时窄化为 T，False 时排除 T")

    print()


# ========== 演示 6: @overload 装饰器 ==========
def demo_overload():
    """演示 6: @overload — 为函数提供多个类型签名"""
    print("=" * 50)
    print("演示 6: @overload 函数重载")
    print("=" * 50)

    # @overload 让你为同一个函数提供多个类型签名
    # 这在函数根据参数类型返回不同类型时特别有用

    # 使用 @overload 定义多个签名
    @overload
    def double_value(value: int) -> int: ...
    @overload
    def double_value(value: str) -> str: ...
    @overload
    def double_value(value: list[int]) -> list[int]: ...

    # 实际实现只有一个
    def double_value(value: int | str | list[int]) -> int | str | list[int]:
        """根据输入类型执行不同的"翻倍"操作"""
        if isinstance(value, int):
            return value * 2
        elif isinstance(value, str):
            return value * 2  # 字符串重复
        elif isinstance(value, list):
            return [x * 2 for x in value]
        else:
            raise TypeError(f"不支持的类型: {type(value)}")

    print(f"  double_value(5)        = {double_value(5)}        → int")
    print(f"  double_value('hi')     = {double_value('hi')}      → str")
    print(f"  double_value([1,2,3])  = {double_value([1, 2, 3])}  → list[int]")

    # @overload 的另一个典型场景：同一个函数可以有不同数量的参数
    @overload
    def format_date(timestamp: float) -> str: ...
    @overload
    def format_date(year: int, month: int, day: int) -> str: ...

    def format_date(
        timestamp_or_year: float | int,
        month: int | None = None,
        day: int | None = None,
    ) -> str:
        """格式化日期（支持时间戳或年月日）"""
        if month is not None and day is not None:
            return f"{timestamp_or_year}-{month:02d}-{day:02d}"
        else:
            import datetime
            dt = datetime.datetime.fromtimestamp(float(timestamp_or_year))
            return dt.strftime("%Y-%m-%d")

    print(f"\n  format_date(2024, 1, 15)    = {format_date(2024, 1, 15)}")
    import time as _time2
    print(f"  format_date({_time2.time():.0f}) = {format_date(_time2.time())}")

    # @overload 也常用于类的 __init__
    print("\n  【@overload 在其他场景】")
    print("    - 类的 __init__ 可以有多种构造方式")
    print("    - 函数返回类型依赖于输入参数类型时")
    print("    - 库 API 设计时提供精确的类型签名")
    print("    注意: @overload 仅有类型检查意义，不影响运行时行为")

    print()


# ========== 演示 7: cast 与 TYPE_CHECKING ==========
def demo_cast_typechecking():
    """演示 7: cast() 类型强制与 TYPE_CHECKING 条件导入"""
    print("=" * 50)
    print("演示 7: cast() 与 TYPE_CHECKING")
    print("=" * 50)

    # cast(目标类型, 值) — 告诉类型检查器"相信我，这个值就是这个类型"
    # cast 在运行时什么都不做，完全不影响性能

    # 场景 1: 你知道类型比类型检查器推断的更精确
    def get_config_value(key: str) -> object:
        """从配置中获取任意值"""
        config = {"timeout": 30, "host": "localhost", "port": 8080}
        return config.get(key)

    # 类型检查器只知道返回值是 object，但你知道它是 int
    raw_timeout = get_config_value("timeout")  # → object
    timeout = cast(int, raw_timeout)            # → int（告诉类型检查器）
    print(f"  cast(int, get_config_value('timeout')) = {timeout}")
    print(f"  type(timeout) = {type(timeout).__name__}")
    print("  cast() 在运行时就是恒等函数，不改变值也不检查类型")

    # 场景 2: 复杂的类型推断
    def parse_json(data: str) -> object:
        """解析 JSON 返回任意对象"""
        import json
        return json.loads(data)

    raw = parse_json('{"name": "Alice", "age": 30}')
    # 我们知道这是一个 dict[str, object]
    typed = cast(dict[str, object], raw)
    print(f"\n  cast 后可以安全访问: name={typed['name']}, age={typed['age']}")

    # 注意：cast 不进行运行时检查，如果类型推断错误会在运行时崩溃
    print("\n  [警告] cast() 不做运行时检查")
    print("    如果类型推断错误，会在运行时产生 AttributeError/TypeError")
    print("    因此 cast 应谨慎使用，只在确信类型正确时使用")

    # TYPE_CHECKING — 只在类型检查时导入的模块
    # 用于避免循环导入问题
    print("\n  【TYPE_CHECKING 用途】")
    print(f"    TYPE_CHECKING = {TYPE_CHECKING}")
    print("    TYPE_CHECKING 在运行时为 False")
    print("    在 mypy/pyright 静态检查时为 True")
    print("")
    print("    典型用法:")
    print("    if TYPE_CHECKING:")
    print("        from my_module import MyClass  # 只为类型检查导入")
    print("")
    print("    这避免了循环导入问题，同时保留了类型信息")

    print()


# ========== 演示 8: reveal_type 与调试技巧 ==========
def demo_reveal_type():
    """演示 8: reveal_type 与 mypy 类型调试技巧"""
    print("=" * 50)
    print("演示 8: reveal_type 与类型调试技巧")
    print("=" * 50)

    # reveal_type 是 mypy 的特殊函数，用于查看变量的推断类型
    # 它不是一个真正的 Python 函数，只在 mypy 分析时有效
    # 但在运行时我们通过注释来展示它的用法

    print("  【reveal_type — 查看 mypy 推断的类型】")
    print("    在代码中添加 reveal_type(x)，然后运行 mypy")
    print("    mypy 会输出变量 x 的推断类型")

    # 模拟 reveal_type 的效果
    def show_mypy_type(name: str, value: object) -> None:
        """模拟 mypy 的 reveal_type 输出效果"""
        print(f"    reveal_type({name}) → {type(value).__name__}")

    x = 42
    y: str = "hello"
    z = [1, 2, 3]
    w: dict[str, int] = {"a": 1}

    show_mypy_type("x", x)
    show_mypy_type("y", y)
    show_mypy_type("z", z)
    show_mypy_type("w", w)
    print()

    # 调试技巧列表
    print("  【mypy 类型调试技巧】")
    tips = [
        ("reveal_type(var)", "查看变量在当前位置的类型推断结果"),
        ("reveal_locals()", "查看当前作用域所有变量的类型"),
        ("--strict 模式", "启用所有可选检查，发现潜在类型问题"),
        ("--show-error-codes", "显示错误码，方便针对性配置"),
        ("# type: ignore[error-code]", "精确忽略特定类型的错误"),
        ("pyproject.toml 配置", "项目级别统一 mypy 配置"),
        ("mypy --html-report", "生成 HTML 类型检查报告"),
    ]
    for cmd, desc in tips:
        print(f"    {cmd:30s} — {desc}")

    # 常见类型错误的处理
    print("\n  【常见 mypy 错误与处理】")
    common_issues = [
        ('error: Incompatible types', '参数或赋值类型不匹配 → 检查类型注解'),
        ('error: Missing return statement', '函数缺少 return → 添加返回值或注解为 None'),
        ('error: Item "None" has no attribute', 'Optional 值需要先判断 is not None'),
        ('error: Module has no attribute', '导入的模块未安装或路径错误'),
        ('note: Revealed type is', '提示信息，告诉你类型推断的结果'),
    ]
    for error, fix in common_issues:
        print(f"    {error:45s} → {fix}")

    print()


# ========== 演示 9: 自定义泛型容器 ==========
def demo_custom_generic_container():
    """演示 9: 自定义泛型容器 — 实现一个类型安全的 Stack"""
    print("=" * 50)
    print("演示 9: 自定义泛型容器")
    print("=" * 50)

    T = TypeVar("T")

    class Stack(Generic[T]):
        """泛型栈容器 — 类型安全的后进先出数据结构

        使用 Generic[T] 后:
          Stack[int]  — 只能 push/pop int
          Stack[str]  — 只能 push/pop str
          类型检查器会在编译时验证类型安全
        """
        def __init__(self) -> None:
            self._items: list[T] = []

        def push(self, item: T) -> None:
            """压入一个元素"""
            self._items.append(item)

        def pop(self) -> T:
            """弹出栈顶元素"""
            if not self._items:
                raise IndexError("从空栈中弹出")
            return self._items.pop()

        def peek(self) -> T:
            """查看栈顶元素（不弹出）"""
            if not self._items:
                raise IndexError("空栈无法查看")
            return self._items[-1]

        def is_empty(self) -> bool:
            """检查栈是否为空"""
            return len(self._items) == 0

        def __len__(self) -> int:
            return len(self._items)

        def __repr__(self) -> str:
            return f"Stack({self._items})"

    # 使用泛型栈 — 不同类型安全的栈
    int_stack: Stack[int] = Stack()
    int_stack.push(10)
    int_stack.push(20)
    int_stack.push(30)
    print(f"  int_stack: {int_stack}")
    print(f"  int_stack.pop()  = {int_stack.pop()}")
    print(f"  int_stack.peek() = {int_stack.peek()}")
    print(f"  int_stack len    = {len(int_stack)}")

    str_stack: Stack[str] = Stack()
    str_stack.push("hello")
    str_stack.push("world")
    print(f"\n  str_stack: {str_stack}")
    print(f"  str_stack.pop() = {str_stack.pop()}")

    # 泛型函数操作泛型容器
    def pop_all(stack: Stack[T]) -> list[T]:
        """弹出栈中所有元素"""
        items: list[T] = []
        while not stack.is_empty():
            items.append(stack.pop())
        return items

    int_stack.push(1)
    int_stack.push(2)
    int_stack.push(3)
    popped = pop_all(int_stack)
    print(f"\n  pop_all(int_stack) = {popped}")
    print(f"  int_stack.is_empty() = {int_stack.is_empty()}")

    # 复合泛型容器
    class Cache(Generic[T]):
        """泛型缓存容器 — 带过期机制的键值存储"""
        def __init__(self) -> None:
            self._data: dict[str, tuple[T, float]] = {}
            import time
            self._time = time

        def set(self, key: str, value: T, ttl: float = 60.0) -> None:
            """设置缓存，TTL 单位秒"""
            expire_at = self._time.time() + ttl
            self._data[key] = (value, expire_at)

        def get(self, key: str) -> T | None:
            """获取缓存（过期返回 None）"""
            entry = self._data.get(key)
            if entry is None:
                return None
            value, expire_at = entry
            if self._time.time() > expire_at:
                del self._data[key]
                return None
            return value

        def __repr__(self) -> str:
            return f"Cache({ {k: v[0] for k, v in self._data.items()} })"

    num_cache: Cache[int] = Cache()
    num_cache.set("score", 95)
    num_cache.set("level", 42)
    print(f"\n  num_cache: {num_cache}")
    print(f"  num_cache.get('score') = {num_cache.get('score')}")
    print(f"  num_cache.get('missing') = {num_cache.get('missing')}")

    print()


# ========== 演示 10: 实际项目中的 typing 最佳实践 ==========
def demo_best_practices():
    """演示 10: 实际项目中的 typing 最佳实践总结"""
    print("=" * 50)
    print("演示 10: 实际项目中的 typing 最佳实践")
    print("=" * 50)

    practices: list[tuple[str, str]] = [
        # 基础原则
        ("1. 公共 API 必须注解",
         "所有公开的函数/类方法都应该有完整的类型注解"),
        ("2. 返回值永远注解",
         "即使返回 None 也要明确写 -> None"),
        ("3. Any 要慎用",
         "Any 会关闭类型检查，只在确实需要动态类型时使用"),
        ("4. 优先使用新语法",
         "Python 3.10+: X | Y 代替 Union, list[X] 代替 List[X]"),

        # 类型安全
        ("5. Optional 先判空",
         "处理 X | None 时先 if x is not None 再使用 x"),
        ("6. cast 作为最后手段",
         "优先改进类型推断，cast 只在确信类型时使用"),
        ("7. TypeVar 命名有含义",
         "T, K, V 标准命名；有场景的用 T_User 等"),

        # 项目配置
        ("8. 渐进式采用类型注解",
         "旧项目可以配置 mypy 逐步增加检查严格度"),
        ("9. pyproject.toml 统一配置",
         "mypy/pyright 配置放在 pyproject.toml 中版本控制"),
        ("10. CI 集成类型检查",
         "在 CI/CD 中运行 mypy --strict 阻止类型错误合入"),

        # 进阶技巧
        ("11. @overload 提升 API",
         "当函数参数类型决定返回类型时使用 @overload"),
        ("12. Protocol 替代 ABC",
         "结构化子类型比名义子类型更灵活，更 Pythonic"),
        ("13. Final 标记常量",
         "不可变配置/常量用 Final 标注，防止意外修改"),
        ("14. TYPE_CHECKING 破循环",
         "解决模块间循环导入的类型注解问题"),

        # 工具链
        ("15. mypy 作为日常工具",
         "提交前运行 mypy src/ 发现潜在类型问题"),
        ("16. pyright/pylance 实时",
         "VSCode 中 Pylance 提供即时类型检查和补全"),
        ("17. stub 文件处理第三方",
         "无类型注解的第三方库使用 .pyi stub 文件补充类型"),
    ]

    for title, desc in practices:
        print(f"  {title}")
        print(f"    {desc}")
        print()

    # 一个综合示例：展示了大部分最佳实践
    print("  " + "-" * 46)
    print("  【综合示例：规范的类型注解项目代码】")
    print("  " + "-" * 46)

    from dataclasses import dataclass

    @dataclass
    class User:
        """用户数据类 — 展示规范的注解"""
        id: int
        name: str
        email: str
        age: int | None = None
        tags: list[str] | None = None

    class UserService:
        """用户服务 — 展示规范的函数注解"""

        def find_by_id(self, user_id: int) -> User | None:
            """根据 ID 查找用户"""
            # 模拟数据库查询
            if user_id == 1:
                return User(
                    id=1, name="Alice", email="alice@example.com",
                    age=30, tags=["python", "django"]
                )
            return None

        def get_user_name(self, user_id: int) -> str:
            """获取用户名（找不到返回默认值）"""
            user = self.find_by_id(user_id)
            if user is not None:
                return user.name
            return "未知用户"

        def search_users(
            self,
            keyword: str,
            limit: int = 10,
            offset: int = 0,
        ) -> list[User]:
            """搜索用户"""
            return []  # 简化实现

    service = UserService()
    user = service.find_by_id(1)
    print(f"\n    service.find_by_id(1): {user}")
    print(f"    service.get_user_name(1): {service.get_user_name(1)}")
    print(f"    service.get_user_name(99): {service.get_user_name(99)}")

    print()


# ========== 主入口 ==========
def main():
    """运行所有高级类型系统演示"""
    demo_typevar_generic()
    demo_typevar_constraints()
    demo_protocol()
    demo_paramspec()
    demo_typeguard()
    demo_overload()
    demo_cast_typechecking()
    demo_reveal_type()
    demo_custom_generic_container()
    demo_best_practices()
    print("=== 所有高级类型系统演示完成! ===")


if __name__ == "__main__":
    main()


# ============================================================
# 相关主题:
#   - 14-typing/01_type_annotations.py     → 类型注解基础 (基本类型/容器/Optional/Literal/Final)
#   - 05-oop/02_inheritance.py             → ABC 抽象基类 (名义子类型 vs Protocol 结构化子类型)
#   - 04-functions/03_decorator.py         → 装饰器与 ParamSpec
#   - 05-oop/01_class.py                   → Generic 泛型类与普通类的对比
#   - Python 官方 typing 文档: https://docs.python.org/zh-cn/3/library/typing.html
#   - mypy 文档: https://mypy.readthedocs.io/
#   - PEP 484 (类型提示): https://peps.python.org/pep-0484/
#   - PEP 544 (Protocol): https://peps.python.org/pep-0544/
#   - PEP 612 (ParamSpec): https://peps.python.org/pep-0612/
#   - PEP 647 (TypeGuard): https://peps.python.org/pep-0647/
#   - python/typeshed (第三方 stub): https://github.com/python/typeshed
# ============================================================
