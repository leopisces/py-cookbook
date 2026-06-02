"""
内置函数 — 类型与对象相关 (Type / Object / Inspection)
==========================================================
演示与类型转换、类型检查、对象属性操作相关的 Python 内置函数：
type, isinstance, issubclass, str, repr, bool, int, float,
list, dict, tuple, set, frozenset, bytes, bytearray, memoryview,
id, dir, vars, getattr, setattr, hasattr, callable, super,
hash, chr, ord, hex, oct, bin, format, slice

参考: https://www.runoob.com/python3/python3-built-in-functions.html
"""


# ========== 演示 1: 类型相关函数 ==========
def demo_type_functions():
    """
    type / isinstance / issubclass / str / repr / bool /
    int / float / list / dict / tuple / set / frozenset
    """
    print("=" * 50)
    print("演示 1: 类型相关函数")
    print("=" * 50)

    # --- type(): 获取对象的类型 ---
    print("--- type() ---")
    print(f"  type(42)       = {type(42)}")
    print(f"  type(3.14)     = {type(3.14)}")
    print(f"  type('hello')  = {type('hello')}")
    print(f"  type([])       = {type([])}")
    print(f"  type(type)     = {type(type)}      # type 本身的类型")
    # type 还可以动态创建类
    MyClass = type("MyClass", (), {"x": 100})
    print(f"  type 动态创建类: {MyClass}, x={MyClass.x}")

    # --- isinstance(): 检查对象是否是某个类型的实例 ---
    print("\n--- isinstance() ---")
    print(f"  isinstance(42, int)         = {isinstance(42, int)}")
    print(f"  isinstance(42, float)       = {isinstance(42, float)}")
    print(f"  isinstance(True, int)       = {isinstance(True, int)}  # bool 是 int 的子类")
    print(f"  isinstance([1,2], (list, tuple)) = {isinstance([1, 2], (list, tuple))}  # 多个类型")

    # --- issubclass(): 检查类之间的继承关系 ---
    print("\n--- issubclass() ---")
    print(f"  issubclass(bool, int)  = {issubclass(bool, int)}")
    print(f"  issubclass(int, object) = {issubclass(int, object)}")
    print(f"  issubclass(str, int)   = {issubclass(str, int)}")

    # --- str() 和 repr(): 转换为字符串 ---
    print("\n--- str() vs repr() ---")
    print(f"  str(123)       = {str(123)}")
    print(f"  repr(123)      = {repr(123)}     # repr 力求精确/可求值")
    s = "Hello\nWorld"
    print(f"  str(s)         = {str(s)}        # str 友好显示")
    print(f"  repr(s)        = {repr(s)}       # repr 显示转义字符")

    # --- bool(): 转换为布尔值 ---
    print("\n--- bool() ---")
    print(f"  bool(1)        = {bool(1)}")
    print(f"  bool(0)        = {bool(0)}")
    print(f"  bool('')       = {bool('')}      # 空字符串 → False")
    print(f"  bool('hi')     = {bool('hi')}")
    print(f"  bool([])       = {bool([])}      # 空列表 → False")
    print(f"  bool(None)     = {bool(None)}")

    # --- int(), float(): 类型转换 ---
    print("\n--- int() / float() ---")
    print(f"  int(3.14)            = {int(3.14)}          # 截断小数")
    print(f"  float(42)            = {float(42)}")
    print(f"  int('1010', 2)       = {int('1010', 2)}     # 二进制字符串转整数")
    print(f"  int('FF', 16)        = {int('FF', 16)}      # 十六进制字符串转整数")
    print(f"  float('3.14')        = {float('3.14')}")

    # --- list(), dict(), tuple(), set(), frozenset() ---
    print("\n--- 容器类型转换 ---")
    print(f"  list('abc')          = {list('abc')}        # 字符串转列表")
    print(f"  tuple([1, 2, 3])     = {tuple([1, 2, 3])}  # 列表转元组")
    print(f"  set([1, 2, 2, 3])    = {set([1, 2, 2, 3])} # 列表转集合(去重)")
    print(f"  dict([('a',1),('b',2)]) = {dict([('a', 1), ('b', 2)])}")
    fs = frozenset([1, 2, 3])  # 不可变集合
    print(f"  frozenset([1,2,3])   = {fs}")

    # --- bytes() / bytearray() ---
    print("\n--- bytes / bytearray ---")
    print(f"  bytes([65, 66, 67])  = {bytes([65, 66, 67])}")
    print(f"  bytes('ABC', 'utf-8')= {bytes('ABC', 'utf-8')}")
    ba = bytearray(b"hello")
    ba[0] = 72  # 改成 'H'
    print(f"  bytearray 可变: {ba}")

    print()


# ========== 演示 2: 对象相关函数 ==========
def demo_object_functions():
    """id / dir / vars / getattr / setattr / hasattr / callable / super"""
    print("=" * 50)
    print("演示 2: 对象相关函数")
    print("=" * 50)

    # --- id(): 获取对象的内存地址 ---
    print("--- id() ---")
    x = 42
    y = x
    z = 43
    print(f"  id(42) = {id(x)}")
    print(f"  id(y)  = {id(y)}    (y=x, 相同对象)")
    print(f"  id(z)  = {id(z)}    (不同对象)")

    # --- dir(): 列出属性和方法 ---
    print("\n--- dir() ---")
    print(f"  dir([]) 前5个: {dir([])[:5]}...")  # 列出列表的所有方法
    print(f"  'append' in dir([]): {'append' in dir([])}")

    # --- vars(): 获取对象的 __dict__ ---
    print("\n--- vars() ---")

    class Person:
        def __init__(self, name, age):
            self.name = name
            self.age = age

    p = Person("小明", 20)
    print(f"  vars(p) = {vars(p)}")
    # 无参数 vars() 等价于 locals()
    local_x = "test"
    print(f"  vars() 包含 'local_x': {'local_x' in vars()}")

    # --- getattr / setattr / hasattr ---
    print("\n--- getattr / setattr / hasattr ---")
    print(f"  hasattr(p, 'name')    = {hasattr(p, 'name')}")
    print(f"  hasattr(p, 'email')   = {hasattr(p, 'email')}")
    print(f"  getattr(p, 'name')    = {getattr(p, 'name')}")
    print(f"  getattr(p, 'email', '无') = {getattr(p, 'email', '无')}  # 默认值")
    setattr(p, "email", "xiaoming@test.com")  # 动态设置属性
    print(f"  设置 email 后: {p.email}")

    # --- callable(): 判断是否可调用 ---
    print("\n--- callable() ---")
    print(f"  callable(print)    = {callable(print)}")
    print(f"  callable(len)      = {callable(len)}")
    print(f"  callable(42)       = {callable(42)}")
    print(f"  callable(lambda x: x) = {callable(lambda x: x)}")

    # --- super(): 调用父类方法 ---
    print("\n--- super() ---")

    class Animal:
        def speak(self):
            return "动物叫声"

    class Dog(Animal):
        def speak(self):
            parent_sound = super().speak()  # 调用父类方法
            return f"{parent_sound} → 汪汪"

    d = Dog()
    print(f"  Dog().speak() = {d.speak()}")

    print()


# ========== 演示 3: 其他类型相关函数 ==========
def demo_other_type_functions():
    """hash / memoryview / chr / ord / hex / oct / bin / format / slice"""
    print("=" * 50)
    print("演示 3: 其他类型相关函数")
    print("=" * 50)

    # --- hash(): 获取哈希值 ---
    print("--- hash() ---")
    print(f"  hash('hello')      = {hash('hello')}")
    print(f"  hash(42)           = {hash(42)}")
    print(f"  hash((1, 2, 3))    = {hash((1, 2, 3))}")
    # 可变类型不可哈希
    print(f"  hash([1,2,3]) 不可哈希 (会抛 TypeError)")
    # 相同值的对象哈希相同
    print(f"  hash('hello') 重复: {hash('hello')} (相同)")

    # --- memoryview(): 内存视图（不复制数据） ---
    print("\n--- memoryview() ---")
    data = bytearray(b"ABCDEFGH")
    mv = memoryview(data)
    print(f"  mv[0]   = {chr(mv[0])}")
    print(f"  mv[0:3].tobytes() = {mv[0:3].tobytes()}")  # 切片返回 bytes
    # 修改 memoryview 会影响原数据
    mv[0] = 90  # 'Z'
    print(f"  修改后 data = {data}")

    # --- chr() / ord(): 字符与编码互转 ---
    print("\n--- chr() / ord() ---")
    print(f"  chr(65)      = '{chr(65)}'")
    print(f"  chr(97)      = '{chr(97)}'")
    print(f"  chr(20013)   = '{chr(20013)}'  # Unicode 中文字符")
    print(f"  ord('A')     = {ord('A')}")
    print(f"  ord('中')    = {ord('中')}")

    # --- hex() / oct() / bin(): 进制转换 ---
    print("\n--- hex() / oct() / bin() ---")
    n = 255
    print(f"  {n} 十进制")
    print(f"  hex({n}) = {hex(n)}    # 十六进制")
    print(f"  oct({n}) = {oct(n)}    # 八进制")
    print(f"  bin({n}) = {bin(n)}    # 二进制")
    # 去掉前缀
    print(f"  format({n}, 'x') = {format(n, 'x')}")
    print(f"  format({n}, 'b') = {format(n, 'b')}")
    print(f"  format({n}, '#x') = {format(n, '#x')}")

    # --- format(): 格式化 ---
    print("\n--- format() ---")
    print(f"  format(3.14159, '.2f')  = {format(3.14159, '.2f')}")
    print(f"  format(255, '08b')      = {format(255, '08b')}    # 8位二进制")
    print(f"  format(255, '#04x')     = {format(255, '#04x')}   # 带0x前缀")
    print(f"  format('hello', '>10s') = '{format('hello', '>10s')}'  # 右对齐")
    print(f"  format('hello', '<10s') = '{format('hello', '<10s')}'  # 左对齐")
    print(f"  format('hello', '^10s') = '{format('hello', '^10s')}'  # 居中")

    # --- slice(): 创建切片对象 ---
    print("\n--- slice() ---")
    items = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    s = slice(2, 8, 2)  # 等价于 [2:8:2]
    print(f"  items[slice(2,8,2)] = {items[s]}")

    print()


# ========== 主程序入口 ==========
if __name__ == "__main__":
    demo_type_functions()
    demo_object_functions()
    demo_other_type_functions()
