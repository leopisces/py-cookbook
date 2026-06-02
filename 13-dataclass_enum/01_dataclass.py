"""
dataclass 数据类 - Python 3.7+ 的数据容器利器

学习目标：
  - 基本 @dataclass 定义与使用
  - 字段类型、默认值、default_factory
  - dataclass 参数: frozen, eq, order, repr, init, slots
  - __post_init__ 初始化后处理
  - 继承 dataclass (字段顺序与覆盖)
  - 与普通 class 的对比
  - dataclass 与 typing 结合 (Optional/Union/List/ClassVar)
  - asdict / astuple 转换
"""
from dataclasses import dataclass, field, asdict, astuple, fields, is_dataclass, MISSING
from typing import Optional, List, ClassVar, Any
import math


# ==============================
# 演示 1: 基本数据类定义
# ==============================
def demo_basic_dataclass():
    """演示 1: 最简单 @dataclass 定义与使用"""
    print("=" * 50)
    print("演示 1: 基本数据类定义")
    print("=" * 50)

    @dataclass
    class Point:
        """一个 2D 坐标点 —— 三行代码就定义好了！"""
        x: float
        y: float

    # 自动生成了 __init__ / __repr__ / __eq__
    p1 = Point(3.0, 4.0)
    p2 = Point(3.0, 4.0)
    p3 = Point(1.0, 2.0)

    print(f"  p1 = {p1}")                 # 自动 __repr__
    print(f"  p1.x={p1.x}, p1.y={p1.y}")  # 属性访问正常
    print(f"  p1 == p2: {p1 == p2}")      # 自动 __eq__
    print(f"  p1 == p3: {p1 == p3}")

    # 与手动定义类的对比
    class PointManual:
        """dataclass 替我们写完了 init/repr/eq"""
        def __init__(self, x, y):
            self.x = x
            self.y = y
        def __repr__(self):
            return f"PointManual(x={self.x}, y={self.y})"
        def __eq__(self, other):
            if not isinstance(other, PointManual):
                return NotImplemented
            return self.x == other.x and self.y == other.y

    pm = PointManual(3.0, 4.0)
    print(f"\n  手动类效果: {pm}")


# ==============================
# 演示 2: 字段类型与默认值
# ==============================
def demo_fields_and_defaults():
    """演示 2: 字段类型、默认值、field() 和 default_factory"""
    print("\n" + "=" * 50)
    print("演示 2: 字段类型与默认值")
    print("=" * 50)

    @dataclass
    class User:
        """
        普通默认值 vs default_factory:
        - 不可变默认值 (int/str/float) 可以直接赋值
        - 可变默认值 (list/dict/set) 必须用 default_factory，否则所有实例共享同一个对象！
        """
        name: str                           # 必填字段（没有默认值）
        age: int = 18                       # 简单默认值
        email: str = ""                     # 字符串默认值
        tags: List[str] = field(default_factory=list)   # 可变类型必须用 default_factory
        metadata: dict = field(default_factory=dict)    # 同理 dict 也必须
        is_active: bool = True

        # field() 完整参数说明:
        # - default           : 默认值 (与 default_factory 互斥)
        # - default_factory   : 零参可调用对象，每次实例化时调用
        # - init              : 是否出现在 __init__ 中 (默认 True)
        # - repr              : 是否出现在 __repr__ 中 (默认 True)
        # - compare           : 是否参与比较 (默认 True)
        # - hash              : 是否参与哈希 (默认 None，由 frozen 决定)
        # - metadata          : 用户自定义元数据 (不影响行为)
        internal_id: str = field(default="", repr=False, compare=False)

    # 基本创建
    u1 = User(name="张三")
    u2 = User(name="李四", age=25, tags=["Python", "Go"], metadata={"role": "admin"})

    print(f"  默认值示例: {u1}")
    print(f"  完整传参:   {u2}")
    print(f"  u2.tags = {u2.tags}")
    print(f"  u2.metadata = {u2.metadata}")

    # 验证 default_factory 每次都新建 list
    u3 = User(name="王五")
    u3.tags.append("Java")
    u4 = User(name="赵六")
    print(f"\n  [!] default_factory 验证: 每个实例拥有独立的 list")
    print(f"  u3.tags = {u3.tags}")
    print(f"  u4.tags = {u4.tags}  (没有 'Java'，各自独立)")

    # 错误演示：可变默认值的坑
    print(f"\n  [警告] 如果用 field(default=[]) 而不是 default_factory=list:")
    print(f"         所有实例会共享同一个 list 对象，修改一个会影响所有！")
    print(f"         因此 dataclass 会直接抛出 ValueError 阻止你这样做。")

    # 隐藏字段 internal_id 不在 __repr__ 中
    print(f"\n  internal_id 设置了 repr=False，不出现在打印中")


# ==============================
# 演示 3: dataclass 参数
# ==============================
def demo_dataclass_params():
    """演示 3: @dataclass 的各种参数配置"""
    print("\n" + "=" * 50)
    print("演示 3:  @dataclass 参数")
    print("=" * 50)

    # ---------- frozen=True: 不可变数据类 ----------
    print("  参数 1: frozen=True (不可变数据类)")
    @dataclass(frozen=True)
    class FrozenPoint:
        x: int
        y: int

    fp = FrozenPoint(3, 4)
    print(f"    fp = {fp}")
    print(f"    frozen 数据类可哈希: hash(fp) = {hash(fp)}")
    print(f"    可以作为 dict 的 key 或放入 set: { {fp: 'point'} }")
    # fp.x = 5  # dataclasses.FrozenInstanceError!

    # ---------- order=True: 自动排序 ----------
    print("\n  参数 2: order=True (自动生成排序方法)")
    @dataclass(order=True)
    class Student:
        score: int
        name: str = ""

    s1 = Student(95, "张三")
    s2 = Student(88, "李四")
    s3 = Student(95, "王五")

    print(f"    s1={s1}, s2={s2}, s3={s3}")
    print(f"    s1 > s2  (按 score): {s1 > s2}")
    # order=True 时按字段顺序比较 (类似 tuple)
    print(f"    s1 > s3  (score 相同比 name): {s1 > s3}")

    sorted_students = sorted([s1, s2, s3])
    print(f"    排序后: {sorted_students}")

    # ---------- 禁用自动方法: init=False / repr=False ----------
    print("\n  参数 3: init=False / repr=False (禁用自动生成)")
    @dataclass(init=False, repr=False)
    class ManualInit:
        value: int

        def __init__(self, raw: str):
            self.value = len(raw)

    mi = ManualInit("hello")
    print(f"    ManualInit('hello').value = {mi.value}")
    print(f"    repr: {repr(mi)}  (未自动生成 repr)")

    # ---------- slots=True (Python 3.10+) ----------
    print("\n  参数 4: slots=True (内存优化，Python 3.10+)")
    @dataclass(slots=True)
    class SlottedPoint:
        x: float
        y: float

    sp = SlottedPoint(1.0, 2.0)
    print(f"    sp = {sp}")
    print(f"    __slots__ = {SlottedPoint.__slots__}")
    # slots 数据类没有 __dict__，属性访问更快，内存占用更少
    # 但无法动态添加属性


# ==============================
# 演示 4: __post_init__ 初始化后处理
# ==============================
def demo_post_init():
    """演示 4: __post_init__ 后处理钩子"""
    print("\n" + "=" * 50)
    print("演示 4:  __post_init__ 初始化后处理")
    print("=" * 50)

    @dataclass
    class Rectangle:
        width: float
        height: float
        area: float = field(init=False)      # init=False: 不接受此参数
        diagonal: float = field(init=False)

        def __post_init__(self):
            """__init__ 执行完成后自动调用，用于派生字段的计算"""
            self.area = self.width * self.height
            self.diagonal = math.sqrt(self.width ** 2 + self.height ** 2)

    r = Rectangle(3, 4)
    print(f"  矩形: width={r.width}, height={r.height}")
    print(f"  自动计算 area = {r.area}")
    print(f"  自动计算 diagonal = {r.diagonal:.4f}")

    # __post_init__ 中做数据校验
    @dataclass
    class PositiveNumber:
        value: float

        def __post_init__(self):
            if self.value <= 0:
                raise ValueError(f"value 必须为正数，实际为 {self.value}")

    try:
        PositiveNumber(-5)
    except ValueError as e:
        print(f"\n  [校验示例] PositiveNumber(-5) 抛出异常: {e}")

    pn = PositiveNumber(42)
    print(f"  PositiveNumber(42).value = {pn.value}")

    # frozen + __post_init__ 的特殊处理: object.__setattr__
    print(f"\n  frozen=True 时在 __post_init__ 中修改字段: 使用 object.__setattr__")

    @dataclass(frozen=True)
    class ImmutableCircle:
        radius: float
        area: float = field(init=False)

        def __post_init__(self):
            # frozen 时 self.area = ... 会报错，需要用 object.__setattr__
            object.__setattr__(self, 'area', math.pi * self.radius ** 2)

    c = ImmutableCircle(5)
    print(f"  ImmutableCircle(5).area = {c.area:.2f}")


# ==============================
# 演示 5: 继承 dataclass
# ==============================
def demo_inheritance():
    """演示 5: dataclass 的继承机制"""
    print("\n" + "=" * 50)
    print("演示 5:  继承 dataclass")
    print("=" * 50)

    @dataclass
    class Person:
        name: str
        age: int

    @dataclass
    class Employee(Person):
        """子类字段追加到父类字段后面"""
        employee_id: str
        department: str = "General"

    emp = Employee(name="张三", age=30, employee_id="E001", department="研发部")
    print(f"  Employee: {emp}")
    print(f"  emp.name={emp.name}, emp.employee_id={emp.employee_id}")

    # 字段顺序: 父类字段在前，子类字段在后
    print(f"\n  字段顺序 (__init__ 参数顺序也是这个):")
    for f in fields(Employee):
        type_name = getattr(f.type, '__name__', str(f.type))
        print(f"    {f.name}: {type_name}")

    # 子类覆盖父类字段的默认值
    print(f"\n  子类覆盖父类字段默认值:")
    @dataclass
    class Admin(Employee):
        department: str = "管理部"       # 覆盖 Employee 的 department 默认值
        permissions: List[str] = field(default_factory=list)

    admin = Admin(name="管理员", age=30, employee_id="A001")
    print(f"  Admin (默认值): {admin}")

    # 注意: 如果父类有默认值字段，子类新增的必填字段必须放在有默认值字段前面！
    # 这是 Python dataclass 继承的一个重要约束
    print(f"\n  [规则] 子类新增无默认值字段 → 必须放在所有有默认值字段之前")
    print(f"        否则: TypeError: non-default argument follows default argument")


# ==============================
# 演示 6: 与普通 class 对比
# ==============================
def demo_comparison_with_class():
    """演示 6: dataclass vs 普通 class 的对比"""
    print("\n" + "=" * 50)
    print("演示 6:  dataclass 与普通 class 对比")
    print("=" * 50)

    # ---------- 普通 class ----------
    class RegularBook:
        def __init__(self, title, author, pages, price=0.0):
            self.title = title
            self.author = author
            self.pages = pages
            self.price = price

        def __repr__(self):
            return f"RegularBook(title='{self.title}', author='{self.author}', pages={self.pages}, price={self.price})"

        def __eq__(self, other):
            if not isinstance(other, RegularBook):
                return NotImplemented
            return (self.title == other.title and
                    self.author == other.author and
                    self.pages == other.pages and
                    self.price == other.price)

    # ---------- dataclass (等效代码) ----------
    @dataclass
    class DataBook:
        title: str
        author: str
        pages: int
        price: float = 0.0

    rb1 = RegularBook("Python入门", "张三", 300)
    rb2 = RegularBook("Python入门", "张三", 300)
    db1 = DataBook("Python入门", "张三", 300)
    db2 = DataBook("Python入门", "张三", 300)

    print(f"  普通 class 代码行数: ~18 行 (带 init/repr/eq)")
    print(f"  dataclass 代码行数:     ~5 行")
    print(f"")
    print(f"  普通 class 比较: rb1 == rb2 → {rb1 == rb2}")
    print(f"  dataclass 比较:  db1 == db2 → {db1 == db2}")
    print(f"  普通 class repr:  {repr(rb1)}")
    print(f"  dataclass repr:   {repr(db1)}")

    # 自动生成方法的完整性
    print(f"\n  dataclass 自动生成的所有方法:")
    print(f"    __init__   : {'__init__' in DataBook.__dict__}")
    print(f"    __repr__   : {'__repr__' in DataBook.__dict__}")
    print(f"    __eq__     : {'__eq__' in DataBook.__dict__}")
    print(f"    __hash__   : {'__hash__' in DataBook.__dict__}")
    print(f"  is_dataclass(db1): {is_dataclass(db1)}")
    print(f"  is_dataclass(rb1): {is_dataclass(rb1)}")


# ==============================
# 演示 7: typing 结合
# ==============================
def demo_typing():
    """演示 7: dataclass 与 typing 模块结合"""
    print("\n" + "=" * 50)
    print("演示 7:  dataclass + typing (类型注解)")
    print("=" * 50)

    @dataclass
    class Order:
        """订单数据类 —— 演示各种 typing 类型注解"""
        order_id: int
        customer_name: str
        items: List[str]                       # 字符串列表
        quantities: List[int]                  # 整数列表
        # Optional[X] 等于 Union[X, None]
        discount_code: Optional[str] = None    # 可选字段
        # Union[float, None] 等同于 Optional[float]
        shipping_fee: Optional[float] = None   # 另一种写法
        # ClassVar 是类变量(类级别共享)，不是实例字段
        tax_rate: ClassVar[float] = 0.13       # 不会出现在 __init__ 中
        notes: str = ""

    o = Order(
        order_id=1001,
        customer_name="张三",
        items=["Python书", "机械键盘"],
        quantities=[1, 2],
        discount_code="SAVE10",
    )
    print(f"  Order: {o}")
    print(f"  discount_code: {o.discount_code}")
    print(f"  shipping_fee:  {o.shipping_fee}")
    print(f"  tax_rate (ClassVar): {Order.tax_rate}")

    # ClassVar 不在 __init__ 参数中，不在字段列表里
    print(f"\n  ClassVar 验证: tax_rate 不出现在 fields() 中")
    field_names = {f.name for f in fields(Order)}
    print(f"  'tax_rate' in fields()? {'tax_rate' in field_names}")
    print(f"  但可通过实例访问 (解析为类属性): o.tax_rate = {o.tax_rate}")
    print(f"  Order.tax_rate: {Order.tax_rate}")

    # 嵌套 dataclass
    @dataclass
    class Address:
        city: str
        street: str
        zip_code: str = ""

    @dataclass
    class Customer:
        name: str
        address: Address                     # 嵌套数据类

    customer = Customer(
        name="李四",
        address=Address(city="北京", street="长安街")
    )
    print(f"\n  嵌套 dataclass:")
    print(f"  {customer}")
    print(f"  customer.address.city = {customer.address.city}")


# ==============================
# 演示 8: asdict / astuple 转换
# ==============================
def demo_asdict_astuple():
    """演示 8: asdict() 与 astuple() 转换"""
    print("\n" + "=" * 50)
    print("演示 8:  asdict 与 astuple 转换")
    print("=" * 50)

    @dataclass
    class Address:
        city: str
        street: str

    @dataclass
    class Person:
        name: str
        age: int
        address: Address
        hobbies: List[str] = field(default_factory=list)

    p = Person(
        name="张三",
        age=25,
        address=Address("上海", "南京路"),
        hobbies=["编程", "读书"]
    )

    # asdict: 递归转换为字典
    d = asdict(p)
    print(f"  asdict(p):")
    print(f"    {d}")
    print(f"    d['name'] = {d['name']}")
    print(f"    d['address']['city'] = {d['address']['city']}")

    # astuple: 递归转换为元组
    t = astuple(p)
    print(f"\n  astuple(p):")
    print(f"    {t}")
    print(f"    t[0] = {t[0]}, t[2][0] = {t[2][0]}")

    # 使用 asdict 序列化为 JSON
    import json
    json_str = json.dumps(d, ensure_ascii=False)
    print(f"\n  序列化为 JSON:")
    print(f"    {json_str}")

    # 浅拷贝 vs 深拷贝注意
    print(f"\n  [注意] asdict/astuple 执行的是深拷贝 (递归)")
    print(f"         修改返回的 dict 不会影响原始 dataclass 实例")

    # fields() 获取字段元数据
    print(f"\n  fields() 获取字段信息:")
    for f in fields(Person):
        if f.default is not MISSING:
            default = repr(f.default)
        elif f.default_factory is not MISSING:
            default = f"<factory: {f.default_factory}>"
        else:
            default = "<必填>"
        type_name = getattr(f.type, '__name__', str(f.type))
        print(f"    {f.name}: type={type_name}, default={default}")


# ==============================
# 主程序入口
# ==============================
if __name__ == "__main__":
    demo_basic_dataclass()
    demo_fields_and_defaults()
    demo_dataclass_params()
    demo_post_init()
    demo_inheritance()
    demo_comparison_with_class()
    demo_typing()
    demo_asdict_astuple()
    print("\n[OK] 所有 dataclass 演示完成！")

# ============================================================
# 相关主题:
#   - 13-dataclass_enum/02_enum.py   -> Python 枚举类型详解
#   - 05-oop/01_class.py             -> 面向对象基础 (class 定义)
#   - 05-oop/03_magic_methods.py     -> 魔术方法与类型注解
#   - 04-functions/03_decorator.py   -> 装饰器 (@dataclass 本身也是装饰器)
# ============================================================
