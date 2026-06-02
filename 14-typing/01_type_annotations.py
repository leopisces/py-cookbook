"""
类型注解基础 — Python Typing 核心入门
========================================
Python 类型注解：基本类型、函数注解、容器类型、Optional/Union、
Any/NoReturn/Never、Callable、TypeAlias、Literal、Final。

学习目标：
  - 掌握所有基本类型注解语法
  - 理解类型注解在函数参数与返回值中的用法
  - 熟悉容器类型（list/dict/tuple/set）的泛型注解
  - 掌握 Optional、Union、Any、NoReturn 的区别与使用场景
  - 学会使用 TypeAlias、Literal、Final 提升代码可读性
  - 理解"类型注解不影响运行时性能"的本质

参考: https://docs.python.org/zh-cn/3/library/typing.html
"""

from __future__ import annotations

from typing import (
    Any,
    Callable,
    Final,
    Literal,
    NoReturn,
    TypeAlias,
)


# ========== 演示 1: 基本类型注解 ==========
def demo_basic_annotations():
    """演示 1: int、str、float、bool、None 等基本类型注解"""
    print("=" * 50)
    print("演示 1: 基本类型注解 (int / str / float / bool / None)")
    print("=" * 50)

    # 变量类型注解：在变量名后加冒号和类型
    name: str = "Python"
    version: float = 3.12
    count: int = 42
    is_active: bool = True
    nothing: None = None

    print(f"  name: {name}       → 类型: {type(name).__name__}")
    print(f"  version: {version}  → 类型: {type(version).__name__}")
    print(f"  count: {count}      → 类型: {type(count).__name__}")
    print(f"  is_active: {is_active}  → 类型: {type(is_active).__name__}")
    print(f"  nothing: {nothing}     → 类型: {type(nothing).__name__}")

    # 类型注解不强制类型检查 — 以下代码不会报 RuntimeError
    name = 123  # type checker 会警告，但运行时不报错
    print(f"\n  重新赋值为 int 后 name = {name}, 类型 = {type(name).__name__}")
    print("  (注意: 类型注解只是提示，运行时不会强制校验)")

    # 类型注解对 IDE 自动补全和 mypy 静态检查很有用
    scores: list[int] = [95, 88, 76, 92]
    print(f"  scores: {scores}")

    print()


# ========== 演示 2: 函数参数与返回值注解 ==========
def demo_function_annotations():
    """演示 2: 函数签名中的参数类型和返回值类型"""
    print("=" * 50)
    print("演示 2: 函数参数与返回值注解")
    print("=" * 50)

    # 参数注解：在参数名后加 :类型
    # 返回值注解：在函数签名末尾加 ->类型
    def greet(name: str, times: int = 1) -> str:
        """向某人打招呼，可指定次数"""
        return f"你好, {name}! " * times

    result = greet("小明", 3)
    print(f"  greet('小明', 3) = {result}")

    # 多参数、多类型
    def calculate(x: int, y: int, operation: str = "+") -> float:
        """基础计算器"""
        if operation == "+":
            return float(x + y)
        elif operation == "-":
            return float(x - y)
        elif operation == "*":
            return float(x * y)
        elif operation == "/":
            return float(x / y)
        else:
            raise ValueError(f"不支持的操作: {operation}")

    print(f"  calculate(10, 3, '*') = {calculate(10, 3, '*')}")
    print(f"  calculate(10, 3, '/') = {calculate(10, 3, '/'):.2f}")

    # 返回 None 的函数
    def log_message(msg: str, level: str = "INFO") -> None:
        """打印日志（无返回值）"""
        print(f"    [{level}] {msg}")

    log_message("函数注解演示完成")
    print(f"  log_message 返回: {log_message('test')}  (即 None)")

    # 类型注解可以很详细地帮助你理解函数契约
    def process_user(
        user_id: int,
        name: str,
        age: int,
        tags: list[str] | None = None,
    ) -> dict[str, object]:
        """处理用户数据并返回字典"""
        return {
            "id": user_id,
            "name": name.upper(),
            "age_group": "成年" if age >= 18 else "未成年",
            "tags": tags or [],
        }

    user = process_user(1, "张三", 15, tags=["student", "python"])
    print(f"  process_user(1, '张三', 15) = {user}")

    print()


# ========== 演示 3: 容器类型注解 ==========
def demo_container_annotations():
    """演示 3: list、dict、tuple、set 等容器的泛型注解 (Python 3.9+)"""
    print("=" * 50)
    print("演示 3: 容器类型注解 (list / dict / tuple / set / frozenset)")
    print("=" * 50)

    # Python 3.9+ 可以直接用 list[int] 而不是 typing.List[int]
    # Python 3.10+ 可以用 X | Y 而不是 Union[X, Y]

    # 列表：list[元素类型]
    names: list[str] = ["Alice", "Bob", "Charlie"]
    matrix: list[list[int]] = [[1, 2], [3, 4], [5, 6]]
    print(f"  names (list[str]):         {names}")
    print(f"  matrix (list[list[int]]):  {matrix}")

    # 字典：dict[键类型, 值类型]
    scores: dict[str, int] = {"Alice": 95, "Bob": 88}
    config: dict[str, str | int] = {"host": "localhost", "port": 8080}
    nested: dict[str, dict[str, int]] = {"math": {"Alice": 90}, "english": {"Bob": 85}}
    print(f"  scores (dict[str, int]):   {scores}")
    print(f"  config (dict[str, str|int]): {config}")

    # 元组：tuple[类型1, 类型2, ...] 或 tuple[类型, ...] 表示可变长度
    point: tuple[int, int] = (3, 4)                    # 定长：两个 int
    record: tuple[str, int, float] = ("Alice", 25, 68.5)  # 三个元素，类型固定
    numbers: tuple[int, ...] = (1, 2, 3, 4, 5)          # 不定长：都是 int
    print(f"  point (tuple[int, int]):     {point}")
    print(f"  record (tuple[str,int,float]):{record}")
    print(f"  numbers (tuple[int, ...]):   {numbers}")

    # 集合：set[元素类型]
    tags: set[str] = {"python", "typing", "tutorial"}
    integer_set: set[int] = {1, 2, 3, 4}
    print(f"  tags (set[str]):            {tags}")
    print(f"  integer_set (set[int]):     {integer_set}")

    # frozenset：不可变集合
    frozen_tags: frozenset[str] = frozenset(["A", "B", "C"])
    print(f"  frozen_tags (frozenset[str]): {frozen_tags}")

    # 嵌套容器实战
    def get_user_scores() -> dict[str, list[int]]:
        """返回每个用户的分数列表"""
        return {
            "Alice": [90, 95, 88],
            "Bob": [78, 82, 91],
            "Charlie": [85, 89, 93],
        }

    user_scores = get_user_scores()
    print(f"\n  get_user_scores() 返回: {user_scores}")
    print(f"  Alice 平均分: {sum(user_scores['Alice']) / len(user_scores['Alice']):.1f}")

    print()


# ========== 演示 4: Optional 与 Union ==========
def demo_optional_union():
    """演示 4: X | None (Optional) 与 X | Y (Union) — Python 3.10+ 语法"""
    print("=" * 50)
    print("演示 4: Optional (X | None) 与 Union (X | Y)")
    print("=" * 50)

    # Python 3.10+: 用 X | None 代替 Optional[X]
    # Python 3.10+: 用 X | Y 代替 Union[X, Y]

    # Optional — 值可以是某类型或 None
    def find_user(user_id: int) -> dict[str, str | int] | None:
        """查找用户，找不到返回 None"""
        users = {1: {"name": "Alice", "age": 30}, 2: {"name": "Bob", "age": 25}}
        return users.get(user_id)

    print(f"  find_user(1) = {find_user(1)}     → 找到用户")
    print(f"  find_user(99) = {find_user(99)}   → 返回 None")

    # Union — 值可以是多种类型之一
    def parse_id(raw_id: int | str) -> int:
        """接受 int 或 str，统一转为 int"""
        return int(raw_id)

    print(f"  parse_id(42) = {parse_id(42)}")
    print(f"  parse_id('42') = {parse_id('42')}")

    # 多类型联合
    def format_value(value: int | float | str | None) -> str:
        """格式化各种类型的值"""
        if value is None:
            return "N/A"
        if isinstance(value, float):
            return f"{value:.2f}"
        return str(value)

    print(f"  format_value(42)     = {format_value(42)}")
    print(f"  format_value(3.14159) = {format_value(3.14159)}")
    print(f"  format_value('hello') = {format_value('hello')}")
    print(f"  format_value(None)    = {format_value(None)}")

    # 对比：Optional 本质就是 Union
    # Optional[X] 等价于 Union[X, None] 等价于 X | None
    print("\n  语法对比:")
    print("    Optional[str]   (传统写法)")
    print("    X | None        (Python 3.10+, 推荐)")

    print()


# ========== 演示 5: Any、NoReturn、Never ==========
def demo_any_noreturn():
    """演示 5: Any（任意类型）、NoReturn（永不返回）、Never（3.11+）"""
    print("=" * 50)
    print("演示 5: Any / NoReturn / Never")
    print("=" * 50)

    # Any — 关闭类型检查，表示可以是任意类型
    def process_any(data: Any) -> Any:
        """接受任意类型，返回任意类型（相当于无类型注解）"""
        return data

    print(f"  process_any(42)      = {process_any(42)}")
    print(f"  process_any('hello')  = {process_any('hello')}")
    print(f"  process_any([1,2,3])  = {process_any([1, 2, 3])}")
    print("  注意: Any 会关闭类型检查器的检查，应谨慎使用")

    # NoReturn — 函数永远不会正常返回（总是抛异常或死循环）
    def raise_error(message: str) -> NoReturn:
        """此函数永远抛出异常，没有正常的返回值"""
        raise ValueError(message)

    # 演示 NoReturn 的特点
    try:
        raise_error("这是一个致命的错误")
    except ValueError as e:
        print(f"\n  捕获到异常: {e}")
    print("  NoReturn 表示函数永远不会有正常返回值（总是异常或死循环）")

    # NoReturn 也用于无限循环的函数
    def server_loop(port: int) -> NoReturn:
        """模拟服务器主循环（永远不会正常退出）"""
        raise SystemExit(f"服务器在端口 {port} 上退出")

    try:
        server_loop(8080)
    except SystemExit as se:
        print(f"  {se}")

    # Never (Python 3.11+): 比 NoReturn 更严格的"永不"概念
    # Never 是底部类型(bottom type)，是任何类型的子类型
    # NoReturn 在 3.11+ 被标记为 deprecated，建议使用 Never
    print("\n  Python 3.11+ 新增 typing.Never")
    print("    Never 是"底部类型"(bottom type)")
    print("    Never 是任何类型的子类型")
    print("    推荐在 Python 3.11+ 使用 Never 代替 NoReturn")

    print()


# ========== 演示 6: Callable 类型注解 ==========
def demo_callable_annotations():
    """演示 6: Callable[[参数类型], 返回值类型] 注解"""
    print("=" * 50)
    print("演示 6: Callable 类型注解")
    print("=" * 50)

    # Callable[[参数类型列表], 返回值类型]
    # 例如: Callable[[int, int], int] 表示接受两个 int 返回一个 int 的函数

    # 定义一个接受回调函数的函数
    def apply_operation(
        a: int,
        b: int,
        op: Callable[[int, int], int]
    ) -> int:
        """对两个数应用某个操作"""
        return op(a, b)

    # 定义不同的操作函数
    def add(x: int, y: int) -> int:
        return x + y

    def multiply(x: int, y: int) -> int:
        return x * y

    def max_of_two(x: int, y: int) -> int:
        return x if x > y else y

    print(f"  apply_operation(3, 5, add)      = {apply_operation(3, 5, add)}")
    print(f"  apply_operation(3, 5, multiply)  = {apply_operation(3, 5, multiply)}")
    print(f"  apply_operation(3, 5, max_of_two)= {apply_operation(3, 5, max_of_two)}")

    # 无参数、无返回值的 Callable
    def run_task(task: Callable[[], None]) -> None:
        """运行一个无参数的任务"""
        print("    开始执行任务...")
        task()
        print("    任务执行完毕")

    def say_hello() -> None:
        print("    Hello from callback!")

    run_task(say_hello)

    # lambda 也是 Callable
    result = apply_operation(10, 20, lambda x, y: x ** 2 + y ** 2)
    print(f"\n  apply_operation(10, 20, lambda) = {result}")

    # Callable 也可以注解可选参数
    # Callable[..., int] — 参数任意，返回 int
    def register_handler(handler: Callable[..., str]) -> None:
        """注册一个返回 str 的处理器，参数不限"""
        print(f"    注册处理器: {handler.__name__}")

    def handler_v1(x: int) -> str:
        return f"v1: {x}"

    def handler_v2(x: int, y: str) -> str:
        return f"v2: {x}, {y}"

    register_handler(handler_v1)
    register_handler(handler_v2)

    print()


# ========== 演示 7: 变量注解与类型别名 ==========
def demo_typealias():
    """演示 7: 变量类型注解与 TypeAlias 类型别名"""
    print("=" * 50)
    print("演示 7: 变量注解与 TypeAlias 类型别名")
    print("=" * 50)

    # TypeAlias — 为复杂类型创建可读的别名
    # 使用 TypeAlias 明确告诉类型检查器这是一个类型别名

    # 定义类型别名
    UserId: TypeAlias = int
    UserName: TypeAlias = str
    JsonDict: TypeAlias = dict[str, object]
    Vector: TypeAlias = tuple[float, float, float]
    Matrix: TypeAlias = list[list[float]]
    Callback: TypeAlias = Callable[[str], None]

    # 使用类型别名让代码更易读
    def get_user(uid: UserId) -> dict[str, object]:
        """根据用户 ID 获取用户"""
        return {"id": uid, "name": f"用户{uid}"}

    def apply_transform(points: list[Vector]) -> Matrix:
        """将向量列表转为矩阵"""
        return [list(v) for v in points]

    user = get_user(42)
    print(f"  get_user(42) = {user}")
    print(f"  JsonDict 别名: {JsonDict}")

    # 复杂嵌套类型的别名
    UserRecord: TypeAlias = dict[str, str | int | list[str]]
    Database: TypeAlias = dict[int, UserRecord]

    def query_db(db: Database, user_id: int) -> UserRecord | None:
        """从数据库查询用户"""
        return db.get(user_id)

    sample_db: Database = {
        1: {"name": "Alice", "age": 30, "tags": ["python", "django"]},
        2: {"name": "Bob", "age": 25, "tags": ["javascript", "react"]},
    }
    print(f"  query_db(sample_db, 1) = {query_db(sample_db, 1)}")
    print(f"  query_db(sample_db, 99) = {query_db(sample_db, 99)}")

    # Python 3.12+ 还提供了 TypeAliasType，支持泛型别名
    print("\n  Python 3.12+ 新增 TypeAliasType，支持泛型别名:")
    print("    type Point[T] = tuple[T, T]")

    print()


# ========== 演示 8: Literal 类型 ==========
def demo_literal():
    """演示 8: Literal — 限制值只能是特定的字面量"""
    print("=" * 50)
    print("演示 8: Literal 字面量类型")
    print("=" * 50)

    # Literal — 值必须是指定的常量之一
    def set_mode(mode: Literal["read", "write", "append"]) -> str:
        """设置文件模式"""
        if mode == "read":
            return "以只读模式打开"
        elif mode == "write":
            return "以写入模式打开"
        elif mode == "append":
            return "以追加模式打开"
        else:
            # 类型检查器应该知道这里永远不会执行
            raise ValueError(f"未知模式: {mode}")

    print(f"  set_mode('read')   = {set_mode('read')}")
    print(f"  set_mode('write')  = {set_mode('write')}")
    print(f"  set_mode('append') = {set_mode('append')}")

    # Literal 也支持数字和布尔值
    def http_status(code: Literal[200, 301, 404, 500]) -> str:
        """HTTP 状态码映射"""
        status_map = {
            200: "成功",
            301: "永久重定向",
            404: "未找到",
            500: "服务器错误",
        }
        return status_map.get(code, "未知状态")

    print(f"  http_status(200) = {http_status(200)}")
    print(f"  http_status(404) = {http_status(404)}")

    # Literal 结合 Union — 可选多个具体值
    def sort_items(
        items: list[int],
        order: Literal["asc", "desc"] = "asc"
    ) -> list[int]:
        """排序列表"""
        return sorted(items, reverse=(order == "desc"))

    data = [3, 1, 4, 1, 5, 9]
    print(f"\n  sort_items({data}, 'asc')  = {sort_items(data, 'asc')}")
    print(f"  sort_items({data}, 'desc')  = {sort_items(data, 'desc')}")

    # Literal 的实际应用：限制 API 参数
    def create_button(
        text: str,
        size: Literal["small", "medium", "large"],
        variant: Literal["primary", "secondary", "danger"],
    ) -> str:
        """创建按钮配置"""
        return f'<Button size="{size}" variant="{variant}">{text}</Button>'

    print(f"\n  {create_button('提交', 'medium', 'primary')}")

    print()


# ========== 演示 9: Final 与常量注解 ==========
def demo_final():
    """演示 9: Final — 标记不可重新赋值的常量"""
    print("=" * 50)
    print("演示 9: Final 常量注解")
    print("=" * 50)

    # Final — 标记某个变量不应该被重新赋值
    # 注意：Final 只在类型检查层面生效，运行时不会阻止重新赋值

    MAX_CONNECTIONS: Final[int] = 100
    API_BASE_URL: Final[str] = "https://api.example.com"
    DATABASE_NAME: Final = "production_db"  # 可以省略类型，自动推导

    print(f"  MAX_CONNECTIONS = {MAX_CONNECTIONS}")
    print(f"  API_BASE_URL    = {API_BASE_URL}")
    print(f"  DATABASE_NAME   = {DATABASE_NAME}")

    # Final 与类的结合
    class AppConfig:
        """应用配置类 — 使用 Final 标记常量"""
        VERSION: Final[str] = "1.0.0"
        DEBUG: Final[bool] = False
        MAX_RETRIES: Final[int] = 3

    config = AppConfig()
    print(f"\n  AppConfig.VERSION     = {config.VERSION}")
    print(f"  AppConfig.DEBUG       = {config.DEBUG}")
    print(f"  AppConfig.MAX_RETRIES = {config.MAX_RETRIES}")

    # Final 也可以用于防止方法被覆写 (Python 3.8+)
    # 但这里演示的是变量层面的 Final

    # 注意：虽然标记了 Final，运行时仍可重新赋值
    # 以下代码在运行时不会报错，但 mypy 会报告错误
    print("\n  注意: Final 只在类型检查层面生效")
    print("    - mypy/pyright 会报告 Final 变量被重新赋值")
    print("    - 但 Python 运行时不会阻止重新赋值")

    print()


# ========== 演示 10: 类型注解运行时的影响 ==========
def demo_runtime_impact():
    """演示 10: 类型注解在运行时的行为与影响"""
    print("=" * 50)
    print("演示 10: 类型注解运行时不影响性能")
    print("=" * 50)

    # 1. 类型注解存储在 __annotations__ 属性中
    def annotated_func(x: int, y: str) -> float:
        return float(x)

    print("  【类型注解的存储位置】")
    print(f"  annotated_func.__annotations__ = {annotated_func.__annotations__}")

    # 2. 使用 from __future__ import annotations 后，
    #    所有注解变成字符串，延迟求值（PEP 563）
    #    这在文件顶部已经启用了

    # 3. 运行时不会进行类型检查
    def takes_int(x: int) -> int:
        return x * 2

    result = takes_int("hello")  # type checker 会警告，但运行时通过
    print(f"\n  takes_int('hello') = '{result}'  (字符串被重复两次)")
    print("  即使签名说接受 int，传入 str 也不会报运行时错误")

    # 4. 类型注解的性能影响
    print("\n  【类型注解的性能影响】")
    print("    - 类型注解在运行时几乎零开销")
    print("    - 注解存储在 __annotations__ 字典中，仅在定义时计算")
    print("    - from __future__ import annotations 将注解变为惰性字符串")
    print("    - 类型检查由外部工具（mypy/pyright）在代码分析阶段完成")
    print("    - CPython 解释器完全忽略类型注解")

    # 5. 总结：类型注解的三层价值
    print("\n  【类型注解的价值】")
    print("    1. 文档价值 — 代码即文档，明确函数参数和返回值")
    print("    2. IDE 支持  — 自动补全、类型提示、重构支持")
    print("    3. 静态检查 — mypy/pyright 在运行前发现类型错误")

    print()


# ========== 主入口 ==========
def main():
    """运行所有类型注解基础演示"""
    demo_basic_annotations()
    demo_function_annotations()
    demo_container_annotations()
    demo_optional_union()
    demo_any_noreturn()
    demo_callable_annotations()
    demo_typealias()
    demo_literal()
    demo_final()
    demo_runtime_impact()
    print("=== 所有类型注解基础演示完成! ===")


if __name__ == "__main__":
    main()


# ============================================================
# 相关主题:
#   - 14-typing/02_advanced_typing.py → TypeVar/Generic/Protocol/ParamSpec 等高级类型
#   - 05-oop/03_magic_methods.py → 魔术方法中也有类型注解的简要示例
#   - Python 官方 typing 文档: https://docs.python.org/zh-cn/3/library/typing.html
#   - mypy 静态检查器: https://mypy.readthedocs.io/
#   - PEP 484 (类型提示): https://peps.python.org/pep-0484/
#   - PEP 604 (联合类型 X | Y): https://peps.python.org/pep-0604/
# ============================================================
