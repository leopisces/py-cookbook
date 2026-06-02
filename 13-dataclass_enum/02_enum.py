"""
enum 枚举 - Python 3.4+ 的类型安全常量方案

学习目标：
  - 基本 Enum 定义与成员访问
  - Enum vs IntEnum vs StrEnum vs Flag vs IntFlag
  - auto() 自动值生成
  - 枚举的遍历、比较与转换 (__members__, value, name)
  - 自定义枚举方法 (为枚举类添加方法)
  - @unique 装饰器实现唯一性约束
  - 枚举在实际项目中的应用 (状态码、配置常量)
"""
from enum import Enum, IntEnum, Flag, IntFlag, auto, unique


# ==============================
# 演示 1: 基本枚举定义
# ==============================
def demo_basic_enum():
    """演示 1: 基本 Enum 定义与成员访问"""
    print("=" * 50)
    print("演示 1: 基本枚举定义")
    print("=" * 50)

    # 定义枚举 —— 继承 Enum
    class Color(Enum):
        RED = 1
        GREEN = 2
        BLUE = 3

    print(f"  Color 类: {Color}")
    print(f"  Color 成员:")

    # 访问枚举成员的方式
    print(f"    按名称: Color.RED = {Color.RED}")
    print(f"    按值:   Color(1) = {Color(1)}")
    print(f"    字典式: Color['RED'] = {Color['RED']}")

    # 成员属性
    print(f"\n  成员属性:")
    print(f"    Color.RED.name  = {Color.RED.name}")    # 成员名称 (字符串)
    print(f"    Color.RED.value = {Color.RED.value}")   # 成员值
    print(f"    type(Color.RED) = {type(Color.RED)}")   # <enum 'Color'>

    # 枚举是不可变的
    # Color.RED = 5   # AttributeError: Cannot reassign members

    # 枚举成员是单例: 同一枚举中每个成员唯一
    print(f"\n  单例验证:")
    print(f"    Color.RED is Color.RED = {Color.RED is Color.RED}")
    print(f"    Color(1) is Color.RED = {Color(1) is Color.RED}")


# ==============================
# 演示 2: 枚举类型的变体
# ==============================
def demo_enum_variants():
    """演示 2: Enum vs IntEnum vs StrEnum vs Flag vs IntFlag"""
    print("\n" + "=" * 50)
    print("演示 2:  枚举类型的变体")
    print("=" * 50)

    # ---------- IntEnum: 同时是 int 子类 ----------
    print("  类型 1: IntEnum (整型枚举，可当 int 使用)")
    class Priority(IntEnum):
        LOW = 1
        MEDIUM = 2
        HIGH = 3

    print(f"    Priority.HIGH = {Priority.HIGH}")
    print(f"    isinstance(Priority.HIGH, int) = {isinstance(Priority.HIGH, int)}")
    print(f"    Priority.HIGH == 3 = {Priority.HIGH == 3}")
    print(f"    sorted([Priority.HIGH, Priority.LOW]) = {sorted([Priority.HIGH, Priority.LOW])}")

    # ---------- StrEnum (Python 3.11+): 同时是 str 子类 ----------
    # 使用 (str, Enum) 在所有版本下兼容；Python 3.11+ 有原生 StrEnum
    print("\n  类型 2: StrEnum (字符串枚举)")
    class PostStatus(str, Enum):
        DRAFT = "draft"
        PUBLISHED = "published"
        ARCHIVED = "archived"

    print(f"    PostStatus.PUBLISHED = {PostStatus.PUBLISHED}")
    print(f"    isinstance(PostStatus.DRAFT, str) = {isinstance(PostStatus.DRAFT, str)}")
    print(f"    PostStatus.ARCHIVED == 'archived' = {PostStatus.ARCHIVED == 'archived'}")
    print(f"    f-string: f'Post status: {PostStatus.PUBLISHED}' = 'Post status: {PostStatus.PUBLISHED}'")
    print(f"    [注] Python 3.11+ 可直接使用 `class X(StrEnum)` 原生写法")

    # ---------- Flag: 位标志枚举 (可组合) ----------
    print("\n  类型 3: Flag (位标志，支持按位运算组合)")
    class Permission(Flag):
        READ = 1      # 0b001
        WRITE = 2     # 0b010
        EXECUTE = 4   # 0b100

    # 组合多个权限
    rw = Permission.READ | Permission.WRITE
    print(f"    READ | WRITE = {rw}  (值: {rw.value})")
    print(f"    READ | WRITE | EXECUTE = {Permission.READ | Permission.WRITE | Permission.EXECUTE}")

    # 检查权限
    print(f"    Permission.READ in rw: {Permission.READ in rw}")
    print(f"    Permission.EXECUTE in rw: {Permission.EXECUTE in rw}")

    # ---------- IntFlag: 组合后仍为 int ----------
    print("\n  类型 4: IntFlag (整型位标志，组合后仍是 int)")
    class FilePerm(IntFlag):
        R = 4
        W = 2
        X = 1

    perms = FilePerm.R | FilePerm.W
    print(f"    FilePerm.R | FilePerm.W = {perms}  (值: {perms.value})")
    print(f"    isinstance(perms, int) = {isinstance(perms, int)}")
    print(f"    perms == 6: {perms == 6}")


# ==============================
# 演示 3: auto() 自动值生成
# ==============================
def demo_auto():
    """演示 3: auto() 自动值生成"""
    print("\n" + "=" * 50)
    print("演示 3:  auto() 自动值生成")
    print("=" * 50)

    # auto() 自动分配递增的整数值
    class Weekday(Enum):
        MONDAY = auto()      # 1
        TUESDAY = auto()     # 2
        WEDNESDAY = auto()   # 3
        THURSDAY = auto()    # 4
        FRIDAY = auto()      # 5

    for day in Weekday:
        print(f"    {day.name}: {day.value}")

    # auto() 也可以通过 _generate_next_value_ 自定义生成逻辑
    print(f"\n  自定义 auto() 生成逻辑:")
    class NamedAuto(Enum):
        @staticmethod
        def _generate_next_value_(name, start, count, last_values):
            """auto() 调用此方法生成下一个值"""
            return str(name).lower()  # 用成员名称的小写作为值

        FIRST = auto()
        SECOND = auto()
        THIRD = auto()

    for item in NamedAuto:
        print(f"    {item.name}: {item.value}")

    # auto() 在 Flag 中自动生成 2 的幂 (1, 2, 4, 8, ...)
    print(f"\n  auto() 在 Flag 中自动生成 2 的幂:")
    class AutoPerm(Flag):
        R = auto()    # 1
        W = auto()    # 2
        X = auto()    # 4

    for p in AutoPerm:
        print(f"    {p.name}: {p.value}  (二进制: {p.value:03b})")


# ==============================
# 演示 4: 枚举的遍历、比较与转换
# ==============================
def demo_iteration_and_comparison():
    """演示 4: 枚举的遍历、比较与转换"""
    print("\n" + "=" * 50)
    print("演示 4:  枚举的遍历、比较与转换")
    print("=" * 50)

    class Direction(Enum):
        NORTH = 0
        EAST = 90
        SOUTH = 180
        WEST = 270

    # ---------- 遍历 ----------
    print(f"  遍历所有成员:")
    for d in Direction:
        print(f"    {d.name} = {d.value}°")

    # __members__ 是一个有序字典
    print(f"\n  __members__ (有序字典):")
    print(f"    type: {type(Direction.__members__)}")
    for name, member in Direction.__members__.items():
        print(f"    {name} -> {member}")

    # ---------- 比较 ----------
    print(f"\n  比较操作:")
    print(f"    Direction.NORTH == Direction.NORTH: {Direction.NORTH == Direction.NORTH}")
    print(f"    Direction.NORTH == Direction.SOUTH: {Direction.NORTH == Direction.SOUTH}")
    print(f"    Direction.NORTH != Direction.SOUTH: {Direction.NORTH != Direction.SOUTH}")

    # 枚举成员之间不支持大小比较 (除非 IntEnum)
    print(f"    is 身份比较: Direction.NORTH is Direction.NORTH: {Direction.NORTH is Direction.NORTH}")
    # Direction.NORTH < Direction.SOUTH  # TypeError: '<' not supported

    # ---------- 转换 ----------
    print(f"\n  枚举值转成员:")
    print(f"    Direction(90) = {Direction(90)}")
    try:
        Direction(999)  # ValueError: 999 is not a valid Direction
    except ValueError as e:
        print(f"    Direction(999) 抛出 ValueError: {e}")

    # 安全取值
    print(f"\n  安全取值 (避免异常):")
    # 方式 1: try/except
    try:
        val = Direction(45)
    except ValueError:
        val = None
    print(f"    Direction(45) -> {val}")

    # 方式 2: 用 _missing_ 钩子 (注意: 必须返回一个枚举成员，不能返回 None)
    class SafeDirection(Enum):
        NORTH = 0
        EAST = 90
        SOUTH = 180
        WEST = 270
        UNKNOWN = -1  # 定义兜底成员

        @classmethod
        def _missing_(cls, value):
            """当 value 不在枚举中时调用 (Python 3.6+)"""
            return cls.UNKNOWN  # 返回 UNKNOWN 成员而不是抛出异常

    print(f"    SafeDirection(45) -> {SafeDirection(45)}")
    print(f"    SafeDirection(180) -> {SafeDirection(180)}")
    print(f"    [注] _missing_ 必须返回枚举成员，返回 None 仍会抛 ValueError")


# ==============================
# 演示 5: 自定义枚举方法
# ==============================
def demo_custom_methods():
    """演示 5: 为枚举类添加自定义方法"""
    print("\n" + "=" * 50)
    print("演示 5:  自定义枚举方法")
    print("=" * 50)

    class HTTPStatus(IntEnum):
        """HTTP 状态码枚举 —— 带自定义方法"""
        OK = 200
        CREATED = 201
        BAD_REQUEST = 400
        UNAUTHORIZED = 401
        FORBIDDEN = 403
        NOT_FOUND = 404
        INTERNAL_SERVER_ERROR = 500

        @property
        def is_success(self) -> bool:
            """判断是否为成功状态码 (2xx)"""
            return 200 <= self.value < 300

        @property
        def is_client_error(self) -> bool:
            """判断是否为客户端错误 (4xx)"""
            return 400 <= self.value < 500

        @property
        def is_server_error(self) -> bool:
            """判断是否为服务端错误 (5xx)"""
            return 500 <= self.value < 600

        @property
        def description(self) -> str:
            """获取状态码描述"""
            descriptions = {
                200: "请求成功",
                201: "已创建",
                400: "请求错误",
                401: "未授权",
                403: "禁止访问",
                404: "未找到",
                500: "服务器内部错误",
            }
            return descriptions.get(self.value, "未知状态")

        @classmethod
        def all_codes(cls):
            """类方法: 返回所有状态码的值列表"""
            return [m.value for m in cls]

    print(f"  状态码判断:")
    print(f"    HTTPStatus.OK.is_success:         {HTTPStatus.OK.is_success}")
    print(f"    HTTPStatus.NOT_FOUND.is_success:   {HTTPStatus.NOT_FOUND.is_success}")
    print(f"    HTTPStatus.FORBIDDEN.is_client_error: {HTTPStatus.FORBIDDEN.is_client_error}")
    print(f"    HTTPStatus.INTERNAL_SERVER_ERROR.is_server_error: {HTTPStatus.INTERNAL_SERVER_ERROR.is_server_error}")

    print(f"\n  状态码描述:")
    for code in [HTTPStatus.OK, HTTPStatus.NOT_FOUND, HTTPStatus.INTERNAL_SERVER_ERROR]:
        print(f"    {code.value}: {code.description}")

    print(f"\n  类方法:")
    print(f"    all_codes() = {HTTPStatus.all_codes()}")

    # 带字段的枚举 (enum 成员可以有多余的关联数据)
    print(f"\n  枚举成员带额外数据 (通过 __init__):")
    class Planet(Enum):
        """行星枚举 —— 每个成员有质量 (mass) 和半径 (radius)"""
        MERCURY = (3.303e23, 2.4397e6)
        VENUS   = (4.869e24, 6.0518e6)
        EARTH   = (5.976e24, 6.37814e6)

        def __init__(self, mass, radius):
            self.mass = mass       # 单位: kg
            self.radius = radius   # 单位: m

        @property
        def surface_gravity(self):
            """计算表面重力 (m/s^2)"""
            G = 6.67300e-11
            return G * self.mass / (self.radius * self.radius)

    print(f"    Planet.EARTH.name = {Planet.EARTH.name}")
    print(f"    Planet.EARTH.value = {Planet.EARTH.value}")
    print(f"    Planet.EARTH.mass = {Planet.EARTH.mass:.2e} kg")
    print(f"    Planet.EARTH.surface_gravity = {Planet.EARTH.surface_gravity:.2f} m/s^2")


# ==============================
# 演示 6: unique 装饰器
# ==============================
def demo_unique():
    """演示 6: @unique 装饰器确保枚举值唯一"""
    print("\n" + "=" * 50)
    print("演示 6:  @unique 唯一值装饰器")
    print("=" * 50)

    # 正常情况：所有值唯一
    @unique
    class UniqueColor(Enum):
        RED = 1
        GREEN = 2
        BLUE = 3

    print(f"  @unique 验证通过: UniqueColor")
    for c in UniqueColor:
        print(f"    {c.name} = {c.value}")

    # 如果没有 @unique，重复的值也不会报错
    print(f"\n  没有 @unique 时重复值不会报错:")
    class NonUniqueColor(Enum):
        RED = 1
        GREEN = 2
        BLUE = 1   # 与 RED 重复，但不会报错 —— 这成为 RED 的别名

    print(f"    NonUniqueColor.RED = {NonUniqueColor.RED}")
    print(f"    NonUniqueColor.BLUE = {NonUniqueColor.BLUE}")
    print(f"    RED is BLUE: {NonUniqueColor.RED is NonUniqueColor.BLUE}")

    # 遍历时别名默认跳过
    print(f"\n    遍历成员 (别名被跳过):")
    for c in NonUniqueColor:
        print(f"      {c.name} = {c.value}")

    # 使用 __members__ 可以看到别名
    print(f"\n    __members__ (包含别名):")
    for name, member in NonUniqueColor.__members__.items():
        print(f"      {name} -> {member}")

    # 违反 @unique 约束会报错
    print(f"\n  @unique 检测到重复值会抛出 ValueError:")
    try:
        @unique
        class BadEnum(Enum):
            A = 1
            B = 2
            C = 1   # 与 A 重复！
    except ValueError as e:
        print(f"    错误: {e}")


# ==============================
# 演示 7: 实际项目中的应用
# ==============================
def demo_real_world_usage():
    """演示 7: 枚举在实际项目中的应用"""
    print("\n" + "=" * 50)
    print("演示 7:  枚举在实际项目中的应用")
    print("=" * 50)

    # ---------- 场景 1: 订单状态机 ----------
    print("  场景 1: 订单状态管理")
    class OrderStatus(Enum):
        PENDING = "pending"             # 待处理
        CONFIRMED = "confirmed"         # 已确认
        PROCESSING = "processing"       # 处理中
        SHIPPED = "shipped"            # 已发货
        DELIVERED = "delivered"         # 已送达
        CANCELLED = "cancelled"         # 已取消
        REFUNDED = "refunded"           # 已退款

        @property
        def can_transition_to(self):
            """返回当前状态下允许转换到的状态列表"""
            transitions = {
                OrderStatus.PENDING: [OrderStatus.CONFIRMED, OrderStatus.CANCELLED],
                OrderStatus.CONFIRMED: [OrderStatus.PROCESSING, OrderStatus.CANCELLED],
                OrderStatus.PROCESSING: [OrderStatus.SHIPPED, OrderStatus.CANCELLED],
                OrderStatus.SHIPPED: [OrderStatus.DELIVERED],
                OrderStatus.DELIVERED: [OrderStatus.REFUNDED],
                OrderStatus.CANCELLED: [],
                OrderStatus.REFUNDED: [],
            }
            return transitions.get(self, [])

    status = OrderStatus.PENDING
    print(f"    当前状态: {status.value}")
    next_statuses = [s.value for s in status.can_transition_to]
    print(f"    可转换到: {next_statuses}")

    # 状态流转验证
    def transition(current: OrderStatus, target: OrderStatus) -> OrderStatus:
        if target in current.can_transition_to:
            print(f"    [OK] {current.value} -> {target.value} (允许)")
            return target
        print(f"    [X] {current.value} -> {target.value} (不允许!)")
        return current

    status = transition(status, OrderStatus.CONFIRMED)
    status = transition(status, OrderStatus.DELIVERED)  # 不允许

    # ---------- 场景 2: 应用配置常量 ----------
    print(f"\n  场景 2: 应用配置常量")
    class Config(str, Enum):
        """替代零散的字符串常量"""
        DB_HOST = "localhost"
        DB_PORT = "5432"
        DB_NAME = "myapp"
        CACHE_TTL = "3600"
        API_VERSION = "v1"

    print(f"    数据库配置:")
    print(f"      主机: {Config.DB_HOST.value}")
    print(f"      端口: {Config.DB_PORT.value}")
    print(f"    API 版本: {Config.API_VERSION.value}")
    print(f"    优势: IDE 自动补全、编译期检查、避免拼写错误")

    # ---------- 场景 3: API 响应码 ----------
    print(f"\n  场景 3: API 响应码统一管理")
    class APIResponse(IntEnum):
        SUCCESS = 0
        PARAM_ERROR = 1001
        AUTH_FAILED = 1002
        PERMISSION_DENIED = 1003
        NOT_FOUND = 1004
        RATE_LIMIT = 1005
        SERVER_ERROR = 5000

        @property
        def message(self) -> str:
            messages = {
                0: "操作成功",
                1001: "参数错误",
                1002: "认证失败",
                1003: "权限不足",
                1004: "资源不存在",
                1005: "请求过于频繁",
                5000: "服务器内部错误",
            }
            return messages.get(self.value, "未知错误")

    print(f"    响应码示例:")
    for code in [APIResponse.SUCCESS, APIResponse.AUTH_FAILED, APIResponse.PERMISSION_DENIED]:
        print(f"      code={code.value:5d}  msg='{code.message}'")

    # ---------- 场景 4: 枚举与 match 结合 (Python 3.10+) ----------
    print(f"\n  场景 4: enum + match/case 模式匹配")
    def handle_response(code: APIResponse):
        match code:
            case APIResponse.SUCCESS:
                print(f"      [OK] 操作成功")
            case APIResponse.PARAM_ERROR:
                print(f"      [!] 参数错误，请检查输入")
            case APIResponse.AUTH_FAILED | APIResponse.PERMISSION_DENIED:
                print(f"      [X] 认证或权限问题")
            case APIResponse.SERVER_ERROR:
                print(f"      [X] 服务器错误")
            case _:
                print(f"      [?] 未知响应码")

    handle_response(APIResponse.SUCCESS)
    handle_response(APIResponse.AUTH_FAILED)
    handle_response(APIResponse.PERMISSION_DENIED)


# ==============================
# 主程序入口
# ==============================
if __name__ == "__main__":
    demo_basic_enum()
    demo_enum_variants()
    demo_auto()
    demo_iteration_and_comparison()
    demo_custom_methods()
    demo_unique()
    demo_real_world_usage()
    print("\n[OK] 所有 enum 演示完成！")

# ============================================================
# 相关主题:
#   - 13-dataclass_enum/01_dataclass.py -> Python 数据类详解
#   - 05-oop/01_class.py                -> 面向对象基础 (class 定义)
#   - 05-oop/02_inheritance.py          -> 继承与多态 (ABC 抽象基类)
#   - 09-stdlib/01_math.py              -> Python 标准库中的枚举示例
# ============================================================
