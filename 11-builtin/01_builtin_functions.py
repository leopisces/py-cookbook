"""
内置函数大全 (Built-in Functions)
=====================================
Python 内置函数分类演示：类型相关、数学相关、迭代相关、对象相关、其他。

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


# ========== 演示 2: 数学相关函数 ==========
def demo_math_functions():
    """abs / round / divmod / pow / min / max / sum"""
    print("=" * 50)
    print("演示 2: 数学相关函数")
    print("=" * 50)

    # --- abs(): 绝对值 ---
    print("--- abs() 绝对值 ---")
    print(f"  abs(-10)          = {abs(-10)}")
    print(f"  abs(-3.14)        = {abs(-3.14)}")
    print(f"  abs(complex(3, 4))= {abs(complex(3, 4))}  # 复数的模")

    # --- round(): 四舍五入 ---
    print("\n--- round() 四舍五入 ---")
    print(f"  round(3.14159, 2) = {round(3.14159, 2)}")
    print(f"  round(3.14159)    = {round(3.14159)}     # 默认0位小数")
    print(f"  round(2.5)        = {round(2.5)}         # 银行家舍入(偶数优先)")

    # --- divmod(): 同时返回商和余数 ---
    print("\n--- divmod() 商和余数 ---")
    q, r = divmod(17, 5)
    print(f"  divmod(17, 5)     = ({q}, {r})")
    q2, r2 = divmod(100, 7)
    print(f"  divmod(100, 7)    = ({q2}, {r2})  # 验证: {q2}*7+{r2}={q2*7+r2}")

    # --- pow(): 幂运算 (可加取模) ---
    print("\n--- pow() 幂运算 ---")
    print(f"  pow(2, 3)        = {pow(2, 3)}        # 2的3次方")
    print(f"  pow(2, 10)       = {pow(2, 10)}       # 2的10次方")
    print(f"  pow(2, 3, 5)     = {pow(2, 3, 5)}    # (2的3次方) % 5 (高效取模)")

    # --- min() / max(): 最小/最大值 ---
    print("\n--- min() / max() ---")
    nums = [5, 2, 9, 1, 7, 3]
    print(f"  数据: {nums}")
    print(f"  min(nums)        = {min(nums)}")
    print(f"  max(nums)        = {max(nums)}")
    print(f"  min('a', 'z', 'm') = {min('a', 'z', 'm')}")
    # key 参数: 按自定义规则比较
    words = ["apple", "banana", "kiwi", "grape"]
    print(f"  单词: {words}")
    print(f"  min(按长度)      = {min(words, key=len)}")
    print(f"  max(按长度)      = {max(words, key=len)}")

    # --- sum(): 求和 ---
    print("\n--- sum() 求和 ---")
    print(f"  sum([1, 2, 3, 4, 5])     = {sum([1, 2, 3, 4, 5])}")
    print(f"  sum([1, 2, 3], start=10)  = {sum([1, 2, 3], start=10)}")
    # 生成器求和
    print(f"  sum(i*i for i in range(1,6)) = {sum(i * i for i in range(1, 6))}")

    print()


# ========== 演示 3: 迭代相关函数 ==========
def demo_iteration_functions():
    """len / range / enumerate / zip / map / filter / sorted / reversed / all / any / iter / next"""
    print("=" * 50)
    print("演示 3: 迭代相关函数")
    print("=" * 50)

    # --- len(): 获取长度 ---
    print("--- len() ---")
    print(f"  len('Python')      = {len('Python')}")
    print(f"  len([1, 2, 3])     = {len([1, 2, 3])}")
    sample_dict = {'a': 1, 'b': 2}
    print(f"  len({sample_dict}) = {len(sample_dict)}")

    # --- range(): 生成整数序列 ---
    print("\n--- range() ---")
    print(f"  list(range(5))     = {list(range(5))}        # 0到4")
    print(f"  list(range(2, 7))  = {list(range(2, 7))}     # 2到6")
    print(f"  list(range(0, 10, 3)) = {list(range(0, 10, 3))}  # 步长3")
    print(f"  list(range(10, 0, -1)) = {list(range(10, 0, -1))}  # 递减")

    # --- enumerate(): 带索引的迭代 ---
    print("\n--- enumerate() ---")
    fruits = ["苹果", "香蕉", "橙子"]
    print(f"  水果列表: {fruits}")
    print("  带索引遍历:")
    for i, fruit in enumerate(fruits):
        print(f"    [{i}] {fruit}")
    print(f"  enumerate start=1: {list(enumerate(fruits, start=1))}")

    # --- zip(): 并行迭代多个可迭代对象 ---
    print("\n--- zip() ---")
    names = ["张三", "李四", "王五"]
    scores = [85, 92, 78]
    ages = [20, 21, 22]
    print(f"  姓名: {names}")
    print(f"  成绩: {scores}")
    print(f"  年龄: {ages}")
    print("  zip 并行迭代:")
    for name, score, age in zip(names, scores, ages):
        print(f"    {name}: 成绩{score}, 年龄{age}")
    # 创建字典的便捷方式
    print(f"  dict(zip(names, scores)) = {dict(zip(names, scores))}")

    # --- map(): 对每个元素应用函数 ---
    print("\n--- map() ---")
    nums = [1, 2, 3, 4, 5]
    print(f"  数据: {nums}")
    squared = list(map(lambda x: x * x, nums))
    print(f"  map(平方): {squared}")
    # 多个可迭代对象
    a, b = [1, 2, 3], [4, 5, 6]
    print(f"  map(add, {a}, {b}) = {list(map(lambda x, y: x + y, a, b))}")

    # --- filter(): 过滤元素 ---
    print("\n--- filter() ---")
    print(f"  数据: {nums}")
    even = list(filter(lambda x: x % 2 == 0, nums))
    print(f"  filter(偶数): {even}")
    # 当第一个参数为 None 时，过滤掉 falsy 值
    mixed = [0, 1, "", "hello", [], [1, 2], None, False]
    print(f"  filter(None, {mixed}) = {list(filter(None, mixed))}")

    # --- sorted(): 排序 ---
    print("\n--- sorted() ---")
    nums2 = [3, 1, 4, 1, 5, 9, 2]
    print(f"  数据: {nums2}")
    print(f"  sorted()            = {sorted(nums2)}")
    print(f"  sorted(reverse=True)= {sorted(nums2, reverse=True)}")
    # key 参数自定义排序
    words = ["banana", "apple", "kiwi", "grape"]
    print(f"  sorted(按长度)      = {sorted(words, key=len)}")
    print(f"  sorted(按末尾字母)  = {sorted(words, key=lambda w: w[-1])}")

    # --- reversed(): 反向迭代 ---
    print("\n--- reversed() ---")
    print(f"  数据: {nums}")
    print(f"  list(reversed(nums)) = {list(reversed(nums))}")
    # reversed 返回迭代器，不是列表
    r = reversed(nums)
    print(f"  reversed 对象: {r}")

    # --- all() / any(): 全真/任一真 ---
    print("\n--- all() / any() ---")
    print(f"  all([True, True, False])  = {all([True, True, False])}")
    print(f"  all([1, 2, 3])            = {all([1, 2, 3])}")
    print(f"  all([1, 0, 3])            = {all([1, 0, 3])}")
    print(f"  any([False, False, True]) = {any([False, False, True])}")
    print(f"  any([0, '', None])        = {any([0, '', None])}")
    # 实用: 检查是否所有元素满足条件
    print(f"  所有 > 0? {all(n > 0 for n in [1, 2, 3, 4])}")
    print(f"  存在 > 2? {any(n > 2 for n in [1, 2, 3, 4])}")

    # --- iter() / next(): 迭代器 ---
    print("\n--- iter() / next() ---")
    it = iter([10, 20, 30])
    print(f"  next(it) = {next(it)}")
    print(f"  next(it) = {next(it)}")
    print(f"  next(it) = {next(it)}")
    print(f"  next(it, '默认值') = {next(it, '默认值')}  # 耗尽后返回默认值")

    print()


# ========== 演示 4: 对象相关函数 ==========
def demo_object_functions():
    """id / dir / vars / getattr / setattr / hasattr / callable / super"""
    print("=" * 50)
    print("演示 4: 对象相关函数")
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


# ========== 演示 5: 其他常用内置函数 ==========
def demo_other_functions():
    """eval / exec / open / hash / memoryview / chr / ord / hex / oct / bin / format"""
    print("=" * 50)
    print("演示 5: 其他常用内置函数")
    print("=" * 50)

    # --- eval(): 执行表达式字符串并返回值 ---
    print("--- eval() ---")
    print(f"  eval('2 + 3 * 4')  = {eval('2 + 3 * 4')}")
    print(f"  eval('[1,2,3]')    = {eval('[1,2,3]')}")
    x_val = 10
    print(f"  eval('x_val * 2')   = {eval('x_val * 2')}")
    # 安全: 可以限制可用命名空间
    print(f"  eval('min([1,2,3])', {{'min': min}}) = {eval('min([1,2,3])', {'min': min})}")

    # --- exec(): 执行代码块（无返回值） ---
    print("\n--- exec() ---")
    code = """
result = 0
for i in range(1, 6):
    result += i
"""
    local_ns = {}
    exec(code, {}, local_ns)
    print(f"  exec('1到5求和') → result = {local_ns['result']}")

    # --- open(): 文件操作 ---
    print("\n--- open() ---")
    import tempfile, os
    fd, tmp_path = tempfile.mkstemp(suffix=".txt", prefix="builtin_demo_")
    os.close(fd)
    # 写入
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write("Hello, Python!\n内置函数演示。\n")
    # 读取
    with open(tmp_path, "r", encoding="utf-8") as f:
        content = f.read()
    print(f"  文件内容: {content.strip().split(chr(10))}")
    os.unlink(tmp_path)

    # --- hash(): 获取哈希值 ---
    print("\n--- hash() ---")
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

    # --- compile(): 编译代码为可执行对象 ---
    print("\n--- compile() ---")
    compiled = compile("a + b", "<test>", "eval")
    result = eval(compiled, {"a": 3, "b": 4})
    print(f"  compile + eval: 3 + 4 = {result}")

    # --- globals() / locals(): 查看当前作用域变量 ---
    print("\n--- globals() / locals() ---")
    test_var = "I am local"
    print(f"  'test_var' in locals(): {'test_var' in locals()}")
    print(f"  '__name__' in globals(): {'__name__' in globals()}")
    print()


# ========== 演示 6: 实用组合案例 ==========
def demo_practical_combos():
    """展示几个内置函数组合使用的实用案例"""
    print("=" * 50)
    print("演示 6: 实用组合案例")
    print("=" * 50)

    # 案例1: 学生成绩统计
    print("--- 案例1: 成绩统计 ---")
    students = [
        {"name": "张三", "score": 85},
        {"name": "李四", "score": 92},
        {"name": "王五", "score": 78},
        {"name": "赵六", "score": 95},
        {"name": "钱七", "score": 60},
    ]
    # 平均分
    avg = sum(s["score"] for s in students) / len(students)
    print(f"  平均分: {avg:.1f}")
    # 最高分和最低分
    best = max(students, key=lambda s: s["score"])
    worst = min(students, key=lambda s: s["score"])
    print(f"  最高分: {best['name']} ({best['score']})")
    print(f"  最低分: {worst['name']} ({worst['score']})")
    # 及格人数
    passed = sum(1 for s in students if s["score"] >= 60)
    print(f"  及格人数: {passed}/{len(students)}")
    # 按分数排序
    ranked = sorted(students, key=lambda s: s["score"], reverse=True)
    names_ranked = [s["name"] for s in ranked]
    print(f"  排名: {names_ranked}")

    # 案例2: 字符串处理组合
    print("\n--- 案例2: 字符串处理 ---")
    text = "  Hello, Python World! 123  "
    # strip + filter + map 组合
    chars = list(filter(str.isalpha, text.strip()))
    print(f"  提取字母: {chars}")
    # 转换为大写并去重
    upper_unique = sorted(set(ch.upper() for ch in chars))
    print(f"  大写去重排序: {''.join(upper_unique)}")

    # 案例3: 数据验证
    print("\n--- 案例3: 数据验证 ---")
    values = [1, 2, "3", None, 5, "abc"]
    # 过滤并转换为整数
    ints = []
    for v in values:
        if isinstance(v, (int, str)):
            try:
                ints.append(int(v))
            except (ValueError, TypeError):
                pass
    print(f"  有效整数: {ints}")
    print(f"  总和: {sum(ints)}")
    print(f"  全部为正? {all(n > 0 for n in ints)}")

    # 案例4: 动态对象操作
    print("\n--- 案例4: 动态对象操作 ---")

    class Config:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

        def __repr__(self):
            attrs = [f"{k}={v!r}" for k, v in vars(self).items()]
            return f"Config({', '.join(attrs)})"

    cfg = Config(host="localhost", port=8080, debug=True)
    print(f"  配置: {cfg}")
    print(f"  属性列表: {list(vars(cfg).keys())}")
    for attr_name in sorted(dir(cfg)):
        if not attr_name.startswith("_"):
            val = getattr(cfg, attr_name)
            print(f"    cfg.{attr_name} = {val}")

    print()


# ========== 主程序入口 ==========
if __name__ == "__main__":
    demo_type_functions()
    demo_math_functions()
    demo_iteration_functions()
    demo_object_functions()
    demo_other_functions()
    demo_practical_combos()
    print("\n=== 所有内置函数演示完成! ===")
