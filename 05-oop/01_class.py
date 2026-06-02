"""
类与对象 - 面向对象编程基础

学习目标：
  - 定义类与创建实例
  - __init__ 构造方法
  - 实例属性与类属性
  - 实例方法、类方法 (@classmethod)、静态方法 (@staticmethod)
  - __str__ 与 __repr__ 的区别
"""


def main():
    # ========== 1. 定义类与创建实例 ==========
    print("=== 1. 定义类与创建实例 ===")

    class Dog:
        """一个简单的狗类"""

        # 类属性：所有实例共享
        species = "犬科"

        # __init__ 构造方法：创建实例时自动调用
        def __init__(self, name, age):
            # 实例属性：每个实例独有
            self.name = name
            self.age = age

        # 实例方法：第一个参数必须是 self，代表实例本身
        def bark(self):
            return f"{self.name} 在叫：汪汪！"

        def info(self):
            return f"{self.name}，{self.age}岁，属于{self.species}"

    # 创建实例（对象）
    dog1 = Dog("旺财", 3)
    dog2 = Dog("小黑", 1)

    print(f"dog1: {dog1.name}, {dog1.age}岁")
    print(f"dog2: {dog2.name}, {dog2.age}岁")
    print(dog1.bark())
    print(dog2.bark())

    # ========== 2. 实例属性 vs 类属性 ==========
    print("\n=== 2. 实例属性 vs 类属性 ===")

    print(f"dog1.species = {dog1.species}")  # 访问类属性
    print(f"dog2.species = {dog2.species}")
    print(f"Dog.species = {Dog.species}")    # 通过类名访问

    # 修改类属性会影响所有实例（未覆盖的情况下）
    Dog.species = "哺乳纲犬科"
    print(f"修改类属性后: dog1.species = {dog1.species}")
    print(f"修改类属性后: dog2.species = {dog2.species}")

    # 实例属性可以动态添加（仅影响当前实例）
    dog1.color = "黄色"
    print(f"dog1 动态添加 color 属性: {dog1.color}")
    # dog2 没有 color 属性，访问会报错

    # ========== 3. 实例方法 / 类方法 / 静态方法 ==========
    print("\n=== 3. 实例方法 / 类方法 / 静态方法 ===")

    class MathTool:
        """演示三种方法类型"""
        factor = 10  # 类属性

        def __init__(self, value):
            self.value = value

        # 实例方法：可以访问实例属性和类属性
        def instance_method(self):
            return f"实例方法: value={self.value}, factor={MathTool.factor}"

        # 类方法：第一个参数是 cls（类本身），可以修改类属性
        @classmethod
        def class_method(cls):
            return f"类方法: factor={cls.factor}"

        @classmethod
        def set_factor(cls, new_factor):
            cls.factor = new_factor
            return f"已将 factor 修改为 {cls.factor}"

        # 静态方法：不需要 self 或 cls，与普通函数类似
        @staticmethod
        def static_method(x, y):
            return f"静态方法: {x} + {y} = {x + y}"

    tool = MathTool(5)
    print(tool.instance_method())        # 通过实例调用
    print(MathTool.class_method())       # 通过类名调用类方法
    print(MathTool.set_factor(100))
    print(MathTool.static_method(3, 7))  # 静态方法不需要实例

    # ========== 4. __str__ 与 __repr__ ==========
    print("\n=== 4. __str__ 与 __repr__ ===")

    class Point:
        """__str__: 给用户看的友好字符串（print() 调用）"""
        """__repr__: 给开发者看的详细字符串（调试用，交互环境显示）"""

        def __init__(self, x, y):
            self.x = x
            self.y = y

        def __str__(self):
            # print() 和 str() 会调用此方法
            return f"Point({self.x}, {self.y})"

        def __repr__(self):
            # repr() 和交互式环境会调用此方法
            return f"Point(x={self.x}, y={self.y})"

    p = Point(3, 4)
    print(f"str(p)  -> {str(p)}")       # 调用 __str__
    print(f"repr(p) -> {repr(p)}")      # 调用 __repr__
    print(f"直接 print -> {p}")          # print 默认调 __str__

    # 如果没有定义 __str__，print 会回退到 __repr__
    class OnlyRepr:
        def __repr__(self):
            return "<OnlyRepr 实例>"

    o = OnlyRepr()
    print(f"只有 __repr__ 时 print: {o}")

    # ========== 5. 私有属性和 property ==========
    print("\n=== 5. 私有属性与 @property ===")

    class BankAccount:
        """使用 @property 实现属性的 getter/setter"""

        def __init__(self, owner, balance=0):
            self.owner = owner
            self._balance = balance  # 单下划线约定为"受保护"属性

        # @property 将方法变为"只读属性"
        @property
        def balance(self):
            return self._balance

        # @xxx.setter 定义属性的设置方法
        @balance.setter
        def balance(self, amount):
            if amount < 0:
                raise ValueError("余额不能为负数")
            self._balance = amount
            print(f"  [余额已更新为 {amount}]")

        def deposit(self, amount):
            self.balance = self._balance + amount
            return f"存入 {amount} 元，余额: {self.balance}"

    account = BankAccount("张三", 1000)
    print(f"账户: {account.owner}, 余额: {account.balance}")
    print(account.deposit(500))
    # account.balance = -100  # 这会触发 ValueError


if __name__ == "__main__":
    main()
