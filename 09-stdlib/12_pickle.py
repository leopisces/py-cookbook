#!/usr/bin/env python3
"""
pickle模块 - Python标准库对象序列化

涵盖内容:
  1. dumps / loads - 对象 <-> 字节流
  2. dump / load - 文件序列化与反序列化
  3. 序列化自定义对象
  4. 协议版本说明
  5. [!] Pickle 安全警告

参考: https://docs.python.org/zh-cn/3/library/pickle.html
"""

import pickle
import os
import tempfile
from datetime import datetime


# ============================================================
# 1. dumps / loads - 对象 <-> 字节流
# ============================================================
print("=" * 60)
print("1. dumps() / loads() - 对象 <-> 字节流")
print("=" * 60)

# pickle 可以序列化几乎任意 Python 对象
original = {
    "name": "张三",
    "age": 25,
    "scores": [90, 85, 92],
    "address": {"city": "北京", "district": "海淀"},
    "is_active": True,
    "birthday": datetime(1999, 5, 15),
}

# dumps - 序列化为字节
data_bytes = pickle.dumps(original)
print(f"序列化结果: {len(data_bytes)} 字节")
print(f"前32字节 (hex): {data_bytes[:32].hex()}")

# loads - 反序列化回 Python 对象
restored = pickle.loads(data_bytes)
print(f"\n反序列化结果:")
print(f"  类型:       {type(restored).__name__}")
print(f"  name:       {restored['name']}")
print(f"  age:        {restored['age']}")
print(f"  scores:     {restored['scores']}")
print(f"  birthday:   {restored['birthday']}")
print(f"  完全一致:   {original == restored}")

# ============================================================
# 2. dump / load - 文件序列化
# ============================================================
print("\n" + "=" * 60)
print("2. dump() / load() - 文件序列化")
print("=" * 60)

# 使用临时文件
tmp_path = os.path.join(tempfile.gettempdir(), "py_cookbook_pickle.pkl")

data_to_save = {
    "version": "1.0",
    "created_at": datetime.now().isoformat(),
    "items": list(range(100)),
}

try:
    # dump - 写入文件 (必须以二进制模式打开)
    with open(tmp_path, 'wb') as f:
        pickle.dump(data_to_save, f)
    print(f"已写入: {tmp_path}")

    # 查看文件大小
    file_size = os.path.getsize(tmp_path)
    print(f"文件大小: {file_size} 字节")

    # load - 从文件读取
    with open(tmp_path, 'rb') as f:
        loaded_data = pickle.load(f)
    print(f"\n从文件读取:")
    print(f"  version: {loaded_data['version']}")
    print(f"  items数: {len(loaded_data['items'])}")
    print(f"  首5项:   {loaded_data['items'][:5]}")

finally:
    os.unlink(tmp_path)
    print(f"\n已删除临时文件: {tmp_path}")

# ============================================================
# 3. 序列化自定义对象
# ============================================================
print("\n" + "=" * 60)
print("3. 序列化自定义对象")
print("=" * 60)


class Person:
    """示例自定义类"""

    def __init__(self, name, age, hobbies=None):
        self.name = name
        self.age = age
        self.hobbies = hobbies or []
        self._created = datetime.now()

    def greet(self):
        return f"你好, 我是{self.name}, {self.age}岁"

    def __repr__(self):
        return f"Person(name='{self.name}', age={self.age})"

    def __eq__(self, other):
        if not isinstance(other, Person):
            return False
        return (self.name == other.name and
                self.age == other.age and
                self.hobbies == other.hobbies)


# 创建对象
person = Person("李四", 30, ["编程", "读书", "跑步"])
print(f"原始对象: {person}")
print(f"问候: {person.greet()}")

# 序列化
person_bytes = pickle.dumps(person)
print(f"序列化大小: {len(person_bytes)} 字节")

# 反序列化
person_restored = pickle.loads(person_bytes)
print(f"\n反序列化后:")
print(f"  对象:   {person_restored}")
print(f"  问候:   {person_restored.greet()}")
print(f"  相等:   {person == person_restored}")

# 序列化多个对象到一个文件
tmp_path2 = os.path.join(tempfile.gettempdir(), "py_cookbook_persons.pkl")
try:
    people = [
        Person("Alice", 25, ["音乐", "旅行"]),
        Person("Bob", 32, ["摄影", "烹饪"]),
        Person("Charlie", 28, ["篮球", "游戏"]),
    ]

    with open(tmp_path2, 'wb') as f:
        pickle.dump(people, f)

    with open(tmp_path2, 'rb') as f:
        loaded_people = pickle.load(f)

    print(f"\n序列化对象列表: {len(loaded_people)}人")
    for p in loaded_people:
        print(f"  {p} → {p.greet()}")

finally:
    if os.path.exists(tmp_path2):
        os.unlink(tmp_path2)

# ============================================================
# 4. 协议版本
# ============================================================
print("\n" + "=" * 60)
print("4. Pickle 协议版本")
print("=" * 60)

protocols = [
    (pickle.HIGHEST_PROTOCOL, "最高协议 (当前推荐)"),
    (pickle.DEFAULT_PROTOCOL, "默认协议"),
]

for proto, desc in protocols:
    data_bytes = pickle.dumps({"test": 42}, protocol=proto)
    print(f"  协议 {proto} ({desc}): {len(data_bytes)} 字节")

print(f"\n协议说明:")
print(f"  0: ASCII 文本协议 (Python 0.x, 兼容性最好)")
print(f"  1: 旧版二进制 (Python 1.x)")
print(f"  2: Python 2.3+ 引入 (高效序列化 new-style class)")
print(f"  3: Python 3.0+ 引入 (bytes 支持)")
print(f"  4: Python 3.4+ 引入 (大对象支持, pickle 优化)")
print(f"  5: Python 3.8+ 引入 (带外数据, 字节码优化)")

# 对比不同协议的效率
data = list(range(10000))
for proto in range(min(6, pickle.HIGHEST_PROTOCOL + 1)):
    try:
        size = len(pickle.dumps(data, protocol=proto))
        print(f"  协议{proto} 序列化10000个整数: {size:>6} 字节")
    except Exception:
        pass

# ============================================================
# 5. [!] Pickle 安全警告
# ============================================================
print("\n" + "=" * 60)
print("5. [!] Pickle 安全警告!")
print("=" * 60)

print("""
[!]  NEVER unpickle data from untrusted sources!

危险原因:
  1. pickle 可以执行任意代码 (通过 __reduce__)
  2. 攻击者可以构造恶意 pickle 数据来执行系统命令
  3. 反序列化时无任何安全检查

[XX] 永远不要这样做:
  1. 反序列化来自网络的数据
  2. 反序列化用户上传的文件
  3. 反序列化不可信来源的任何数据

[OK] 安全替代方案:
  - 纯数据:   使用 json 模块
  - 配置/数据: 使用 YAML (PyYAML safe_load)
  - 二进制:    使用 msgpack, protobuf
  - 密码/密钥: 使用 secrets, hashlib, bcrypt

[OK] 仅在以下场景安全使用 pickle:
  - 本地缓存 (自己创建的, 自己读取)
  - IPC 通信 (可信的本地进程间)
  - 模型保存 (机器学习 model checkpoint)
  - 不可信场景: 可考虑 hmac + pickle (验证完整性)
""")

# 演示: 查看协议信息
print(f"当前 pickle 最高协议版本: {pickle.HIGHEST_PROTOCOL}")
print(f"当前 Python 版本信息: {pickle.DEFAULT_PROTOCOL=} (默认协议)")
