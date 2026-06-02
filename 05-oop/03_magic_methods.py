"""
魔术方法与类型注解 - 面向对象编程高级特性

学习目标：
  - 魔术方法：__call__ / __len__ / __getitem__ / __iter__
  - 比较运算：__eq__ / __lt__
  - 算术运算：__add__
  - 上下文管理：__enter__ / __exit__
  - 类型注解基础：变量注解 / 函数注解 / typing 模块常用类型
"""

from typing import List, Dict, Optional, Union, Tuple, Callable


def main():
    # ========== 1. __call__ 让实例像函数一样调用 ==========
    print("=== 1. __call__ 可调用对象 ===")

    class Multiplier:
        """可调用对象：实例可以像函数一样被调用"""
        def __init__(self, factor):
            self.factor = factor

        def __call__(self, x):
            return x * self.factor

    double = Multiplier(2)
    triple = Multiplier(3)
    print(f"double(5)  = {double(5)}")   # 实例像函数一样被调用
    print(f"triple(5)  = {triple(5)}")
    print(f"double 是可调用的: {callable(double)}")

    # ========== 2. __len__ / __getitem__ 容器模拟 ==========
    print("\n=== 2. 容器模拟：__len__ / __getitem__ ===")

    class Playlist:
        """模拟一个播放列表，支持 len() 和索引访问"""
        def __init__(self, songs):
            self._songs = list(songs)

        def __len__(self):
            # len(obj) 会调用此方法
            return len(self._songs)

        def __getitem__(self, index):
            # obj[index] 会调用此方法
            return self._songs[index]

        def __contains__(self, song):
            # in 运算符会调用此方法
            return song in self._songs

    pl = Playlist(["晴天", "七里香", "夜曲", "稻香"])
    print(f"歌单长度: {len(pl)}")
    print(f"第一首歌: {pl[0]}")
    print(f"最后一首: {pl[-1]}")
    print(f"'夜曲' 在歌单中: {'夜曲' in pl}")
    print(f"切片 [1:3]: {pl[1:3]}")

    # ========== 3. __iter__ 迭代器协议 ==========
    print("\n=== 3. __iter__ 可迭代对象 ===")

    class Countdown:
        """倒计时迭代器"""
        def __init__(self, start):
            self.start = start

        def __iter__(self):
            # 返回一个迭代器
            self.current = self.start
            return self

        def __next__(self):
            # 每次迭代调用，直到 StopIteration
            if self.current < 0:
                raise StopIteration
            value = self.current
            self.current -= 1
            return value

    print("倒计时:", end=" ")
    for n in Countdown(3):
        print(n, end=" ")
    print()

    # ========== 4. 比较运算：__eq__ / __lt__ ==========
    print("\n=== 4. 比较运算：__eq__ / __lt__ ===")

    class Money:
        """带比较运算的钱包类"""
        def __init__(self, amount):
            self.amount = amount

        def __eq__(self, other):
            # == 运算符
            if isinstance(other, Money):
                return self.amount == other.amount
            return NotImplemented

        def __lt__(self, other):
            # < 运算符
            if isinstance(other, Money):
                return self.amount < other.amount
            return NotImplemented

        def __le__(self, other):
            # <= 运算符
            return self.__lt__(other) or self.__eq__(other)

        def __repr__(self):
            return f"Money({self.amount})"

    a = Money(100)
    b = Money(200)
    c = Money(100)
    print(f"{a} == {b}: {a == b}")
    print(f"{a} == {c}: {a == c}")
    print(f"{a} < {b}:  {a < b}")
    print(f"{a} <= {c}: {a <= c}")

    # ========== 5. 算术运算：__add__ ==========
    print("\n=== 5. 算术运算：__add__ ===")

    class Vector:
        """二维向量，支持加法运算"""
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def __add__(self, other):
            # + 运算符
            if isinstance(other, Vector):
                return Vector(self.x + other.x, self.y + other.y)
            return NotImplemented

        def __mul__(self, scalar):
            # * 运算符（标量乘法）
            return Vector(self.x * scalar, self.y * scalar)

        def __repr__(self):
            return f"Vector({self.x}, {self.y})"

    v1 = Vector(1, 2)
    v2 = Vector(3, 4)
    print(f"{v1} + {v2} = {v1 + v2}")
    print(f"{v1} * 3 = {v1 * 3}")

    # ========== 6. 上下文管理器：__enter__ / __exit__ ==========
    print("\n=== 6. 上下文管理器：__enter__ / __exit__ ===")

    class DatabaseConnection:
        """模拟数据库连接，支持 with 语句"""
        def __init__(self, db_name):
            self.db_name = db_name
            self.connected = False

        def __enter__(self):
            # with 进入时调用
            self.connected = True
            print(f"  [连接数据库: {self.db_name}]")
            return self  # 返回值赋给 as 后的变量

        def __exit__(self, exc_type, exc_val, exc_tb):
            # with 退出时调用（即使发生异常也会执行）
            self.connected = False
            print(f"  [断开数据库: {self.db_name}]")
            # 返回 True 会抑制异常，返回 False（或 None）会让异常继续传播
            return False

        def query(self, sql):
            if not self.connected:
                raise RuntimeError("数据库未连接")
            return f"执行查询: {sql} -> 结果集"

    with DatabaseConnection("test_db") as db:
        result = db.query("SELECT * FROM users")
        print(f"  {result}")

    # ========== 7. 类型注解基础 ==========
    print("\n=== 7. 类型注解基础 ===")

    # 变量注解（Python 3.6+）
    name: str = "Python"
    version: float = 3.12
    is_active: bool = True
    print(f"name: {name} (type: {type(name).__name__})")
    print(f"version: {version} (type: {type(version).__name__})")

    # 函数注解
    def greet(person: str, times: int = 1) -> str:
        """带类型注解的函数"""
        return f"你好, {person}! " * times

    print(greet("小明", 2))

    # typing 模块常用类型
    def process_data(
        items: List[str],                # 字符串列表
        mapping: Dict[str, int],         # 字符串到整数的字典
        callback: Optional[Callable] = None,  # 可选的可调用对象
    ) -> Union[Tuple[int, str], None]:  # 返回元组或 None
        """演示 typing 模块的类型注解"""
        count = len(items)
        total = sum(mapping.values())
        result: Tuple[int, str] = (count, f"处理了 {count} 项, 总值: {total}")
        return result

    data = process_data(
        items=["a", "b", "c"],
        mapping={"x": 10, "y": 20}
    )
    print(f"process_data 返回: {data}")

    # 注意：类型注解在运行时不会强制检查，它们是给 IDE 和类型检查器（mypy）用的
    print("（类型注解是提示性质，运行时不会强制校验）")


if __name__ == "__main__":
    main()
