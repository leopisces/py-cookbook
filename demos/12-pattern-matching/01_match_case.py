"""
结构模式匹配 (Structural Pattern Matching)
============================================
Python 3.10+ 引入的 match/case 语句，提供强大的结构化模式匹配能力。
支持字面量、序列、映射、类、OR、通配符、守卫条件、嵌套模式等多种匹配方式。

学习目标：
  - 字面量模式匹配（int, str, bool, None）
  - 序列模式（list/tuple 匹配与 [*rest] 解构）
  - 映射模式（dict 匹配与 **rest 捕获）
  - 类模式（类实例属性匹配）
  - OR 模式（多值匹配 case X | Y）
  - 通配符 _ 与变量绑定
  - 守卫条件（case X if condition）
  - 嵌套模式（组合多种模式）
  - as 模式（捕获子模式）
  - 实际应用（命令解析、HTTP 状态处理、数据验证）

参考: https://www.runoob.com/python3/python3-match-case.html
      https://docs.python.org/zh-cn/3/whatsnew/3.10.html
"""

from dataclasses import dataclass
from typing import Any


# ========== 演示 1: 基本字面量匹配 ==========
def demo_literal_patterns():
    """字面量模式: 匹配 int, str, bool, None 等基本值"""
    print("=" * 50)
    print("演示 1: 基本字面量匹配 (Literal Patterns)")
    print("=" * 50)

    def describe(value):
        """用 match/case 根据值的类型和内容进行匹配"""
        match value:
            case 0:
                return "零 (整数 0)"
            case 1:
                return "一 (整数 1)"
            case True:
                return "布尔值 True"
            case False:
                return "布尔值 False"
            case None:
                return "None (空值)"
            case "hello":
                return "英文字符串 'hello'"
            case "":
                return "空字符串"
            case _:
                return f"其他值: {value!r}"

    # 注意: True/False 在 Python 中也是 1/0 的子类，
    # 所以 case 1 会先于 case True 匹配！
    # 实际匹配顺序: 0 → 1 → True → False → None → str → _
    print(f"  describe(0)     → {describe(0)}")
    print(f"  describe(1)     → {describe(1)}")
    print(f"  describe(True)  → {describe(True)}")
    print(f"  describe(False) → {describe(False)}")
    print(f"  describe(None)  → {describe(None)}")
    print(f"  describe('hello') → {describe('hello')}")
    print(f"  describe('')    → {describe('')}")
    print(f"  describe(42)    → {describe(42)}")
    print(f"  describe('world') → {describe('world')}")

    # 正确做法: 将 bool 匹配放在 int 之前
    print("\n  --- 注意事项: bool 是 int 的子类 ---")
    print("  Python 中 True == 1 为 True, False == 0 为 True")
    print("  在 match 中, case 1 会拦截 True, 因为 True 也满足 case 1")
    print("  建议: 先匹配 bool 再匹配 int, 或使用守卫条件区分")

    print()


# ========== 演示 2: 序列模式 (Sequence Patterns) ==========
def demo_sequence_patterns():
    """序列模式: 匹配 list/tuple 的结构, 支持 [*rest] 解构"""
    print("=" * 50)
    print("演示 2: 序列模式 (Sequence Patterns)")
    print("=" * 50)

    def match_sequence(seq):
        """匹配不同长度和结构的序列"""
        match seq:
            case []:
                return "空列表"
            case [x]:
                return f"单元素列表: [{x}]"
            case [x, y]:
                return f"两元素列表: [{x}, {y}]"
            case [x, y, z]:
                return f"三元素列表: [{x}, {y}, {z}]"
            case [first, *rest]:
                return f"至少一个元素: 首={first!r}, 剩余={rest}"
            case _:
                return "不匹配"

    test_cases = [
        [],
        [42],
        [1, 2],
        [10, 20, 30],
        [1, 2, 3, 4, 5],
        "not a list",
    ]
    for tc in test_cases:
        print(f"  match_sequence({tc!r}) → {match_sequence(tc)}")

    # 用于解构元组
    print("\n  --- 元组解构 ---")

    def analyze_point(point):
        """匹配坐标元组"""
        match point:
            case (0, 0):
                return "原点"
            case (0, y):
                return f"Y轴上的点: (0, {y})"
            case (x, 0):
                return f"X轴上的点: ({x}, 0)"
            case (x, y):
                return f"普通点: ({x}, {y})"
            case _:
                return "无效坐标"

    print(f"  (0, 0)    → {analyze_point((0, 0))}")
    print(f"  (0, 5)    → {analyze_point((0, 5))}")
    print(f"  (3, 0)    → {analyze_point((3, 0))}")
    print(f"  (3, 4)    → {analyze_point((3, 4))}")

    # 使用 *rest 捕获剩余元素
    print("\n  --- [*rest] 解构列表 ---")

    def process_numbers(nums):
        """用序列模式处理数值列表"""
        match nums:
            case []:
                return "空列表, 无操作"
            case [int(x), int(y)]:
                return f"两个整数: {x} + {y} = {x + y}"
            case [int(first), *rest]:
                total = first + sum(rest)
                return f"首元素 {first} + 剩余 {rest} = {total}"
            case _:
                return "非数值列表"

    print(f"  process_numbers([])        → {process_numbers([])}")
    print(f"  process_numbers([3, 7])    → {process_numbers([3, 7])}")
    print(f"  process_numbers([1,2,3,4]) → {process_numbers([1, 2, 3, 4])}")
    print(f"  process_numbers(['a','b']) → {process_numbers(['a', 'b'])}")

    print()


# ========== 演示 3: 映射模式 (Mapping Patterns) ==========
def demo_mapping_patterns():
    """映射模式: 匹配 dict 的键值结构, 支持 **rest 捕获剩余键值对"""
    print("=" * 50)
    print("演示 3: 映射模式 (Mapping Patterns)")
    print("=" * 50)

    def match_dict(d):
        """匹配字典结构"""
        # 注意: case {} 会匹配任意字典(不限于空字典)!
        # 映射模式 {} 表示"无键约束", 因此匹配所有映射类型
        # 如需仅匹配空字典, 使用守卫条件: case {} if len(d) == 0
        match d:
            case {"name": str(name), "age": int(age)}:
                return f"用户: {name}, 年龄: {age}"
            case {"name": str(name)}:
                return f"仅姓名: {name}"
            case {"error": str(msg)}:
                return f"错误信息: {msg}"
            case {} if len(d) == 0:
                return "空字典"
            case _:
                return f"未知结构: {d}"

    print(f"  match_dict({{}})                         → {match_dict({})}")
    print(f"  match_dict({{'name': '小明', 'age': 20}}) → {match_dict({'name': '小明', 'age': 20})}")
    print(f"  match_dict({{'name': '小红'}})            → {match_dict({'name': '小红'})}")
    print(f"  match_dict({{'error': '连接失败'}})       → {match_dict({'error': '连接失败'})}")
    print(f"  match_dict({{'x': 1, 'y': 2}})            → {match_dict({'x': 1, 'y': 2})}")

    # **rest 捕获额外键值对
    print("\n  --- **rest 捕获额外键 ---")

    def parse_config(cfg):
        """解析配置字典, 支持额外字段"""
        match cfg:
            case {"host": str(host), "port": int(port), **extra}:
                extra_str = f", 额外配置={extra}" if extra else ""
                return f"服务配置: {host}:{port}{extra_str}"
            case {"host": str(host)}:
                return f"主机: {host} (端口未指定, 使用默认值)"
            case _:
                return "无效配置"

    print(f"  parse_config({{'host':'localhost','port':8080}})")
    print(f"    → {parse_config({'host': 'localhost', 'port': 8080})}")
    print(f"  parse_config({{'host':'localhost','port':9090,'debug':True}})")
    print(f"    → {parse_config({'host': 'localhost', 'port': 9090, 'debug': True})}")
    print(f"  parse_config({{'host':'0.0.0.0'}})")
    print(f"    → {parse_config({'host': '0.0.0.0'})}")

    # 请注意: 映射模式的匹配是 **子集匹配**, 即字典包含指定键即可
    # 如果字典有额外键而你没有用 **rest 捕获, 仍会匹配成功
    print("\n  --- 映射模式子集匹配特性 ---")

    def greet_user(user):
        match user:
            case {"name": str(name)}:
                return f"你好, {name}!"
            case _:
                return "未知用户"

    user_with_extra = {"name": "张三", "email": "zhang@example.com", "age": 30}
    print(f"  greet_user({user_with_extra})")
    print(f"    → {greet_user(user_with_extra)}")
    print(f"  说明: 尽管 user 有 email/age, 但匹配时只检查 'name' 键")

    print()


# ========== 演示 4: 类模式 (Class Patterns) ==========
def demo_class_patterns():
    """类模式: 匹配类实例的属性值"""
    print("=" * 50)
    print("演示 4: 类模式 (Class Patterns)")
    print("=" * 50)

    # 使用 dataclass 定义数据类 (自动生成 __init__, __repr__, __eq__)
    @dataclass
    class Point:
        x: int
        y: int

    @dataclass
    class Point3D:
        x: int
        y: int
        z: int

    @dataclass
    class Circle:
        center: Point
        radius: float

    def describe_shape(shape):
        """用类模式匹配不同的几何形状"""
        match shape:
            case Point(x=0, y=0):
                return "原点"
            case Point(x=0, y=int(y)):
                return f"Y轴上的点, y={y}"
            case Point(x=int(x), y=0):
                return f"X轴上的点, x={x}"
            case Point(x=int(x), y=int(y)):
                return f"二维点: ({x}, {y})"
            case Point3D(x=int(x), y=int(y), z=int(z)):
                return f"三维点: ({x}, {y}, {z})"
            case Circle(center=Point(x=int(cx), y=int(cy)), radius=float(r)):
                area = 3.14159 * r * r
                return f"圆: 圆心({cx},{cy}), 半径{r}, 面积≈{area:.2f}"
            case _:
                return "未知形状"

    print(f"  describe_shape(Point(0, 0))    → {describe_shape(Point(0, 0))}")
    print(f"  describe_shape(Point(0, 5))    → {describe_shape(Point(0, 5))}")
    print(f"  describe_shape(Point(3, 0))    → {describe_shape(Point(3, 0))}")
    print(f"  describe_shape(Point(3, 4))    → {describe_shape(Point(3, 4))}")
    print(f"  describe_shape(Point3D(1,2,3)) → {describe_shape(Point3D(1, 2, 3))}")
    print(f"  describe_shape(Circle(Point(0,0), 5.0))")
    print(f"    → {describe_shape(Circle(Point(0, 0), 5.0))}")

    # 类模式中可以使用位置参数 (需要定义 __match_args__)
    print("\n  --- 位置参数类模式 (__match_args__) ---")

    @dataclass
    class Person:
        name: str
        age: int
        __match_args__ = ("name", "age")  # 指定位置参数顺序

    def describe_person(p):
        match p:
            case Person("小明", age):
                return f"小明, 年龄{age}"
            case Person(name, 18):
                return f"{name}, 刚成年(18岁)"
            case Person(name, age) if age < 18:
                return f"{name}, 未成年({age}岁)"
            case Person(name, age):
                return f"{name}, {age}岁"

    print(f"  describe_person(Person('小明', 20)) → {describe_person(Person('小明', 20))}")
    print(f"  describe_person(Person('小红', 18)) → {describe_person(Person('小红', 18))}")
    print(f"  describe_person(Person('小刚', 15)) → {describe_person(Person('小刚', 15))}")
    print(f"  describe_person(Person('老王', 45)) → {describe_person(Person('老王', 45))}")

    print()


# ========== 演示 5: OR 模式 ==========
def demo_or_patterns():
    """OR 模式: 使用 | 匹配多个可选值"""
    print("=" * 50)
    print("演示 5: OR 模式 (OR Patterns)")
    print("=" * 50)

    def check_command(cmd):
        """匹配多个可选的命令"""
        match cmd:
            case "help" | "h" | "?":
                return "显示帮助信息"
            case "quit" | "exit" | "q":
                return "退出程序"
            case "start" | "run" | "go":
                return "启动/运行程序"
            case "stop" | "halt" | "pause":
                return "停止/暂停程序"
            case _:
                return f"未知命令: {cmd!r}"

    for cmd in ["help", "h", "exit", "start", "run", "stop", "something"]:
        print(f"  check_command({cmd!r:>9}) → {check_command(cmd)}")

    # OR 模式结合类型匹配
    print("\n  --- OR 模式 + 类型匹配 ---")

    def process_input(value):
        """OR 模式匹配不同类型"""
        match value:
            case int(x) | float(x):
                return f"数值: {x}, 类型: {type(x).__name__}"
            case str(s) | bytes(s):
                return f"文本/字节: {s!r}"
            case list(items) | tuple(items):
                return f"序列: 长度={len(items)}"
            case True | False:
                return f"布尔值: {value}"
            case None:
                return "空值 None"
            case _:
                return f"其他: {type(value).__name__}"

    for v in [42, 3.14, "hello", b"world", [1, 2, 3], (4, 5), True, None, {1, 2}]:
        print(f"  process_input({v!r}) → {process_input(v)}")

    print()


# ========== 演示 6: 通配符与变量绑定 ==========
def demo_wildcard_and_capture():
    """通配符 _ 忽略值, 变量名绑定捕获值"""
    print("=" * 50)
    print("演示 6: 通配符 _ 与变量绑定")
    print("=" * 50)

    def parse_point(point):
        """通配符 _ 表示 '我不关心这个值'"""
        match point:
            case (0, _):
                return "在 Y 轴上的某处"
            case (_, 0):
                return "在 X 轴上的某处"
            case (_, _):
                return "不在任何轴上"
            case _:
                return "无效"

    # _ 用作通配符: 匹配任意值但不绑定
    print(f"  parse_point((0, 5))  → {parse_point((0, 5))}")
    print(f"  parse_point((3, 0))  → {parse_point((3, 0))}")
    print(f"  parse_point((3, 4))  → {parse_point((3, 4))}")

    # 变量绑定: 给匹配的值取一个名字, 后续可以使用
    print("\n  --- 变量绑定 vs 通配符 ---")

    def classify_value(val):
        """展示变量绑定和通配符的区别"""
        match val:
            case 0:
                return "零"
            case int(n) if n > 0:     # n 绑定到 int 值
                return f"正整数: {n}"
            case int(n) if n < 0:     # n 绑定到 int 值
                return f"负整数: {n}"
            case float(f):            # f 绑定到 float 值
                return f"浮点数: {f}"
            case str(s):              # s 绑定到字符串
                return f"字符串(长度={len(s)}): {s!r}"
            case _:                   # _ 不绑定, 仅匹配
                return f"其他类型: {type(val).__name__}"

    for v in [0, 42, -7, 3.14, "Python", [1, 2]]:
        print(f"  classify_value({v!r}) → {classify_value(v)}")

    # 多个 _ 可以独立使用
    print("\n  --- 多个通配符 ---")

    def check_three_elements(seq):
        """匹配恰好三个元素的序列, 只关心首尾"""
        match seq:
            case [first, _, last]:
                return f"首={first!r}, 尾={last!r} (中间忽略)"
            case _:
                return "不是三元素序列"

    print(f"  check_three_elements([1, 2, 3]) → {check_three_elements([1, 2, 3])}")
    print(f"  check_three_elements(['a','b','c']) → {check_three_elements(['a', 'b', 'c'])}")
    print(f"  check_three_elements([1, 2]) → {check_three_elements([1, 2])}")

    print()


# ========== 演示 7: 守卫条件 (Guard Conditions) ==========
def demo_guard_conditions():
    """守卫条件: case 后跟 if 条件, 为 True 才执行该分支"""
    print("=" * 50)
    print("演示 7: 守卫条件 (Guard Conditions)")
    print("=" * 50)

    def classify_score(score):
        """使用守卫条件实现分数分级"""
        match score:
            case int(n) if n >= 90:
                return f"{n}分 -> 优秀 (A)"
            case int(n) if n >= 80:
                return f"{n}分 -> 良好 (B)"
            case int(n) if n >= 70:
                return f"{n}分 -> 中等 (C)"
            case int(n) if n >= 60:
                return f"{n}分 -> 及格 (D)"
            case int(n):
                return f"{n}分 -> 不及格 (F)"
            case _:
                return "无效分数"

    for s in [95, 83, 75, 62, 45, "abc"]:
        print(f"  classify_score({s!r}) → {classify_score(s)}")

    # 守卫条件 + 序列模式: 匹配特定结构的序列
    print("\n  --- 守卫条件 + 序列模式 ---")

    def analyze_list(lst):
        """根据列表内容做不同处理"""
        match lst:
            case [int(x), int(y)] if x == y:
                return f"两个相等的整数: {x} == {y}"
            case [int(x), int(y)] if x > y:
                return f"递减: {x} > {y}"
            case [int(x), int(y)]:
                return f"递增: {x} < {y}"
            case [int(x), *rest] if all(n > 0 for n in rest):
                return f"全是正数: {[x] + rest}"
            case [int(x), *rest]:
                return f"有非正数: {[x] + rest}"
            case _:
                return "不匹配"

    print(f"  analyze_list([5, 5])      → {analyze_list([5, 5])}")
    print(f"  analyze_list([7, 3])      → {analyze_list([7, 3])}")
    print(f"  analyze_list([2, 8])      → {analyze_list([2, 8])}")
    print(f"  analyze_list([1, 2, 3])   → {analyze_list([1, 2, 3])}")
    print(f"  analyze_list([1, -2, 3])  → {analyze_list([1, -2, 3])}")

    # 守卫条件过滤 bool vs int 问题
    print("\n  --- 守卫解决 bool 是 int 子类问题 ---")

    def safe_match(value):
        """使用守卫条件确保 bool 不会错误匹配 int"""
        match value:
            case bool(b):       # bool 必须先匹配
                return f"布尔值: {b}"
            case int(n):        # 然后才匹配 int
                return f"整数: {n}"
            case _:
                return f"其他: {value!r}"

    print(f"  safe_match(True)  → {safe_match(True)}")
    print(f"  safe_match(42)    → {safe_match(42)}")
    print(f"  safe_match(0)     → {safe_match(0)}")
    print(f"  safe_match(False) → {safe_match(False)}")

    print()


# ========== 演示 8: 嵌套模式 (Nested Patterns) ==========
def demo_nested_patterns():
    """嵌套模式: 在序列/映射/类模式中嵌套其他模式"""
    print("=" * 50)
    print("演示 8: 嵌套模式 (Nested Patterns)")
    print("=" * 50)

    # 定义数据类型
    @dataclass
    class Address:
        city: str
        country: str

    @dataclass
    class User:
        name: str
        age: int
        address: Address
        tags: list

    def describe_user(user):
        """嵌套匹配: 在类模式中嵌套序列模式和映射模式"""
        match user:
            case User(
                name=str(name),
                age=int(age),
                address=Address(city=str(city), country="中国"),
                tags=["vip", *rest]
            ) if age >= 18:
                return f"{name}({age}岁) 是来自{city}的VIP成年用户, 标签: vip, {rest}"
            case User(
                name=str(name),
                age=int(age),
                address=Address(city=str(city), country=str(country)),
                tags=list(tags)
            ):
                return f"{name}({age}岁) 来自 {country}-{city}, 标签: {tags}"
            case _:
                return "无效用户"

    u1 = User("张三", 25, Address("北京", "中国"), ["vip", "premium", "verified"])
    u2 = User("Alice", 30, Address("New York", "美国"), ["user", "email_verified"])
    u3 = User("李四", 16, Address("上海", "中国"), [])

    print(f"  describe_user(u1) → {describe_user(u1)}")
    print(f"  describe_user(u2) → {describe_user(u2)}")
    print(f"  describe_user(u3) → {describe_user(u3)}")

    # 嵌套列表模式
    print("\n  --- 嵌套列表匹配 ---")

    def analyze_matrix(m):
        """匹配嵌套列表结构"""
        match m:
            case []:
                return "空矩阵"
            case [[x]]:
                return f"1x1 矩阵: [[{x}]]"
            case [[a, b], [c, d]]:
                det = a * d - b * c
                return f"2x2 矩阵, 行列式={det}"
            case [first_row, *rest]:
                return f"{len(rest)+1} 行矩阵, 首行={first_row}"
            case _:
                return "不匹配"

    print(f"  analyze_matrix([[5]])         → {analyze_matrix([[5]])}")
    print(f"  analyze_matrix([[1,2],[3,4]]) → {analyze_matrix([[1, 2], [3, 4]])}")
    print(f"  analyze_matrix([[1,2],[3,4],[5,6]]) → {analyze_matrix([[1, 2], [3, 4], [5, 6]])}")

    # 嵌套字典 + 列表
    print("\n  --- 嵌套字典与列表 ---")

    def parse_api_response(resp):
        """匹配 API 响应中的嵌套结构"""
        match resp:
            case {"status": "ok", "data": {"users": [*users]}}:
                return f"成功: {len(users)} 个用户"
            case {"status": "ok", "data": {"count": int(n)}}:
                return f"成功: 共 {n} 条记录"
            case {"status": "error", "message": str(msg)}:
                return f"错误: {msg}"
            case _:
                return "未知响应格式"

    print(f"  parse_api_response({{'status':'ok','data':{{'users':['a','b','c']}}}})")
    print(f"    → {parse_api_response({'status': 'ok', 'data': {'users': ['a', 'b', 'c']}})}")
    print(f"  parse_api_response({{'status':'ok','data':{{'count':100}}}})")
    print(f"    → {parse_api_response({'status': 'ok', 'data': {'count': 100}})}")
    print(f"  parse_api_response({{'status':'error','message':'超时'}})")
    print(f"    → {parse_api_response({'status': 'error', 'message': '超时'})}")

    print()


# ========== 演示 9: as 模式 ==========
def demo_as_patterns():
    """as 模式: 捕获整个子模式或部分匹配结果"""
    print("=" * 50)
    print("演示 9: as 模式 (AS Patterns)")
    print("=" * 50)

    def process_with_as(data):
        """使用 as 捕获匹配的部分"""
        match data:
            # as 捕获整个列表用于后续处理
            case [int(x), int(y)] as point:
                return f"二维点 {point}: x={x}, y={y}"
            # as 捕获第一个元素
            case [(int(first) | str(first)) as head, *tail] as full:
                return f"首元素 {head!r}, 剩余 {tail}, 完整: {full}"
            # as 在映射模式中
            case {"name": str(name), "scores": [int(s1), int(s2)] as scores}:
                avg = sum(scores) / len(scores)
                return f"{name} 的成绩: {scores}, 平均={avg:.1f}"
            case _:
                return f"不匹配: {data!r}"

    print(f"  process_with_as([3, 4])")
    print(f"    → {process_with_as([3, 4])}")
    print(f"  process_with_as(['hello', 1, 2, 3])")
    print(f"    → {process_with_as(['hello', 1, 2, 3])}")
    print(f"  process_with_as({{'name':'小明','scores':[85,92]}})")
    print(f"    → {process_with_as({'name': '小明', 'scores': [85, 92]})}")

    # as 模式在复杂嵌套中非常有用
    print("\n  --- as 模式捕获嵌套子结构 ---")

    def parse_json_node(node):
        """as 模式捕获 JSON 树节点"""
        match node:
            case {"type": "text", "value": str(v) as text}:
                return f"文本节点: {text!r}"
            case {"type": "element", "tag": str(tag), "children": list(children) as kids}:
                return f"元素 <{tag}> 包含 {len(kids)} 个子节点"
            case {"type": "element", "tag": str(tag)}:
                return f"空元素 <{tag}/>"
            case _:
                return "未知节点"

    print(f"  parse_json_node({{'type':'text','value':'你好'}})")
    print(f"    → {parse_json_node({'type': 'text', 'value': '你好'})}")
    print(f"  parse_json_node({{'type':'element','tag':'div','children':[1,2,3]}})")
    print(f"    → {parse_json_node({'type': 'element', 'tag': 'div', 'children': [1, 2, 3]})}")
    print(f"  parse_json_node({{'type':'element','tag':'br'}})")
    print(f"    → {parse_json_node({'type': 'element', 'tag': 'br'})}")

    print()


# ========== 演示 10: 实际应用示例 ==========
def demo_practical_examples():
    """综合实际应用: 命令解析、HTTP 状态处理、数据验证"""
    print("=" * 50)
    print("演示 10: 实际应用示例")
    print("=" * 50)

    # ---------- 应用 1: 命令行解析 ----------
    print("--- 应用 1: 命令解析器 ---")

    def parse_command(input_str):
        """将用户输入字符串解析为命令和参数"""
        parts = input_str.strip().split()
        match parts:
            case []:
                return {"action": "noop", "msg": "空命令"}
            case ["help" | "h" | "?"]:
                return {"action": "help", "msg": "显示帮助"}
            case ["quit" | "exit" | "q"]:
                return {"action": "quit", "msg": "退出程序"}
            case ["add", str(a), str(b)] if a.lstrip('-').isdigit() and b.lstrip('-').isdigit():
                ai, bi = int(a), int(b)
                return {"action": "add", "result": ai + bi, "msg": f"{ai} + {bi} = {ai + bi}"}
            case ["mul", str(a), str(b)] if a.lstrip('-').isdigit() and b.lstrip('-').isdigit():
                ai, bi = int(a), int(b)
                return {"action": "mul", "result": ai * bi, "msg": f"{ai} * {bi} = {ai * bi}"}
            case ["greet", str(name)]:
                return {"action": "greet", "msg": f"你好, {name}!"}
            case ["set", str(key), str(value)]:
                return {"action": "set", "key": key, "value": value}
            case [str(cmd), *args]:
                return {"action": "unknown", "cmd": cmd, "args": args}
            case _:
                return {"action": "error", "msg": "解析失败"}

    test_commands = [
        "",
        "help",
        "quit",
        "add 3 5",
        "mul 4 7",
        "greet 小明",
        "set lang zh-CN",
        "unknown_cmd arg1 arg2",
    ]
    for cmd in test_commands:
        result = parse_command(cmd)
        print(f"  parse_command({cmd!r:>20}) → {result}")

    # ---------- 应用 2: HTTP 状态码处理 ----------
    print("\n  --- 应用 2: HTTP 状态码分类 ---")

    def handle_http_status(code):
        """根据 HTTP 状态码输出对应的处理逻辑"""
        match code:
            case int(c) if 100 <= c < 200:
                return f"{c} 信息响应 (Informational)"
            case 200 as c:
                return f"{c} 成功 (OK)"
            case 201 as c:
                return f"{c} 已创建 (Created)"
            case 204 as c:
                return f"{c} 无内容 (No Content)"
            case 301 | 302 | 307 | 308 as c:
                return f"{c} 重定向 (Redirect)"
            case 304 as c:
                return f"{c} 未修改 (Not Modified)"
            case 400 as c:
                return f"{c} 错误请求 (Bad Request)"
            case 401 | 403 as c:
                return f"{c} 认证/授权失败 (Unauthorized/Forbidden)"
            case 404 as c:
                return f"{c} 未找到 (Not Found)"
            case 405 as c:
                return f"{c} 方法不允许 (Method Not Allowed)"
            case int(c) if 400 <= c < 500:
                return f"{c} 客户端错误 (Client Error)"
            case 500 as c:
                return f"{c} 服务器内部错误 (Internal Server Error)"
            case 502 as c:
                return f"{c} 网关错误 (Bad Gateway)"
            case 503 as c:
                return f"{c} 服务不可用 (Service Unavailable)"
            case int(c) if 500 <= c < 600:
                return f"{c} 服务器错误 (Server Error)"
            case _:
                return f"{code} 未知状态码"

    for status in [200, 201, 301, 302, 400, 403, 404, 500, 502, 503, 520, 999]:
        print(f"  handle_http_status({status}) → {handle_http_status(status)}")

    # ---------- 应用 3: 数据验证与清洗 ----------
    print("\n  --- 应用 3: 数据验证与清洗 ---")

    def validate_and_normalize(record):
        """验证并标准化数据记录"""
        match record:
            # 验证用户数据
            case {
                "type": "user",
                "name": str(name),
                "email": str(email),
            } if "@" in email and len(name) >= 2:
                return {"valid": True, "kind": "user",
                        "data": {"name": name.strip(), "email": email.strip().lower()}}

            # 验证订单数据
            case {
                "type": "order",
                "order_id": str(oid),
                "amount": int(amt) | float(amt),
                "items": list(items),
            } if amt > 0 and len(items) > 0:
                return {"valid": True, "kind": "order",
                        "data": {"order_id": oid, "amount": amt, "item_count": len(items)}}

            # 验证日志
            case {"type": "log", "level": str(lvl), "message": str(msg)}:
                if lvl.upper() in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"):
                    return {"valid": True, "kind": "log",
                            "data": {"level": lvl.upper(), "message": msg}}
                return {"valid": False, "reason": f"无效日志级别: {lvl}"}

            # 未知类型
            case {"type": str(t)}:
                return {"valid": False, "reason": f"未知记录类型: {t}"}

            case _:
                return {"valid": False, "reason": "缺少 'type' 字段"}

    test_records = [
        {"type": "user", "name": "张三", "email": "ZHANG@EXAMPLE.COM"},
        {"type": "user", "name": "李", "email": "no-at-sign"},          # name 太短
        {"type": "order", "order_id": "ORD-001", "amount": 99.5, "items": ["A", "B"]},
        {"type": "order", "order_id": "ORD-002", "amount": 0, "items": []},  # amount=0
        {"type": "log", "level": "INFO", "message": "服务启动"},
        {"type": "log", "level": "FATAL", "message": "崩溃"},             # 无效级别
        {"type": "unknown", "data": 42},
        {"name": "无类型字段"},
    ]
    for rec in test_records:
        result = validate_and_normalize(rec)
        print(f"  validate({rec}) → {result}")

    print()


# ========== 主程序入口 ==========
if __name__ == "__main__":
    demo_literal_patterns()
    demo_sequence_patterns()
    demo_mapping_patterns()
    demo_class_patterns()
    demo_or_patterns()
    demo_wildcard_and_capture()
    demo_guard_conditions()
    demo_nested_patterns()
    demo_as_patterns()
    demo_practical_examples()
    print("\n=== 所有模式匹配演示完成! ===")

# ============================================================
# 相关主题:
#   - 03-control-flow/01_conditional.py  → 条件控制(if/elif/else)
#   - 03-control-flow/02_for_loop.py     → for 循环(迭代与解构)
#   - 04-functions/04_iterator_generator.py → 迭代器与生成器(yield/send)
#   - 05-oop/01_class.py                 → 类与对象(class/__init__)
#   - 05-oop/03_magic_methods.py         → 魔术方法(__match_args__等)
#   - 09-stdlib/04_re.py                 → 正则表达式(文本模式匹配)
#   - Python 3.10 更新日志               → https://docs.python.org/zh-cn/3/whatsnew/3.10.html
# ============================================================
