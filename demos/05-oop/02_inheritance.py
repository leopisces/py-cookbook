"""
继承与多态 - 面向对象编程进阶

学习目标：
  - 单继承与多继承
  - super() 调用父类方法
  - 方法重写（Override）
  - 多态（Polymorphism）
  - 抽象基类（ABC）
  - Mixin 模式
  - __mro__ 方法解析顺序
"""

from abc import ABC, abstractmethod
import pprint


# ========== 1. 单继承 ==========
class Animal:
    """动物基类"""

    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} 发出了声音"


# Cat 继承 Animal
class Cat(Animal):
    def speak(self):
        # 方法重写：覆盖父类的 speak 方法
        return f"{self.name} 在叫：喵喵！"

    def climb(self):
        return f"{self.name} 在爬树"


class Dog(Animal):
    def speak(self):
        return f"{self.name} 在叫：汪汪！"


# ========== 2. super() 调用父类方法 ==========
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        return f"我叫{self.name}，今年{self.age}岁"


class Student(Person):
    def __init__(self, name, age, grade):
        # super() 调用父类的 __init__
        super().__init__(name, age)
        self.grade = grade

    def introduce(self):
        # 在子类方法中扩展父类方法
        base = super().introduce()
        return f"{base}，在读{self.grade}年级"


# ========== 3. 多继承 ==========
class Flyable:
    def fly(self):
        return "可以飞"


class Swimmable:
    def swim(self):
        return "可以游泳"


# 多继承：同时继承多个父类
class Duck(Animal, Flyable, Swimmable):
    def speak(self):
        return f"{self.name} 在叫：嘎嘎！"


# ========== 5. 抽象基类 (ABC) ==========
class Shape(ABC):
    """抽象基类：不能直接实例化，子类必须实现抽象方法"""

    @abstractmethod
    def area(self):
        """计算面积 —— 子类必须实现"""
        pass

    @abstractmethod
    def perimeter(self):
        """计算周长 —— 子类必须实现"""
        pass

    def describe(self):
        # 普通方法可以被子类继承
        return f"面积: {self.area():.2f}, 周长: {self.perimeter():.2f}"


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2

    def perimeter(self):
        return 2 * 3.14159 * self.radius


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


# ========== 6. Mixin 模式 ==========
# Mixin：提供特定功能的类，不单独使用，用于"混入"其他类
class JsonMixin:
    """将对象序列化为 JSON 的 Mixin"""
    # 注: 在类体内导入是为了演示延迟导入模式
    import json

    def to_json(self):
        return self.json.dumps(self.__dict__, ensure_ascii=False)


class LogMixin:
    """添加日志功能的 Mixin"""
    def log(self, msg):
        print(f"[LOG] {self.__class__.__name__}: {msg}")


# 通过多继承"混入"功能
class Product(JsonMixin, LogMixin):
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.log(f"创建产品: {name}")


# ========== 7. __mro__ 方法解析顺序 ==========
# 钻石继承问题演示
class A:
    def method(self):
        return "A"


class B(A):
    def method(self):
        return "B"


class C(A):
    def method(self):
        return "C"


class D(B, C):
    pass


def main():
    # ========== 1. 单继承 ==========
    print("=== 1. 单继承 ===")

    cat = Cat("小花")
    print(cat.speak())
    print(cat.climb())
    print(f"Cat 是 Animal 的子类: {issubclass(Cat, Animal)}")
    print(f"cat 是 Cat 的实例: {isinstance(cat, Cat)}")
    print(f"cat 也是 Animal 的实例: {isinstance(cat, Animal)}")

    # ========== 2. super() 调用父类方法 ==========
    print("\n=== 2. super() 调用父类方法 ===")

    s = Student("小明", 10, 4)
    print(s.introduce())

    # ========== 3. 多继承 ==========
    print("\n=== 3. 多继承 ===")

    duck = Duck("唐老鸭")
    print(duck.speak())
    print(duck.fly())
    print(duck.swim())

    # ========== 4. 多态（Polymorphism） ==========
    print("\n=== 4. 多态 ===")

    # 多态：相同的方法名，不同的行为
    animals = [Cat("小橘"), Dog("大黄"), Duck("小鸭")]

    for animal in animals:
        # 都调用 speak()，但各自表现不同 —— 这就是多态
        print(animal.speak())

    # 函数接受任意 Animal 子类 —— 多态的实际应用
    def make_sound(animal: Animal):
        print(f"make_sound: {animal.speak()}")

    make_sound(Cat("咪咪"))
    make_sound(Dog("阿黄"))

    # ========== 5. 抽象基类 (ABC) ==========
    print("\n=== 5. 抽象基类 (ABC) ===")

    # Shape()  # 抽象类不能直接实例化，会报 TypeError
    circle = Circle(5)
    rect = Rectangle(4, 6)
    print(f"圆: {circle.describe()}")
    print(f"矩形: {rect.describe()}")

    # ========== 6. Mixin 模式 ==========
    print("\n=== 6. Mixin 模式 ===")

    product = Product("笔记本电脑", 5999)
    print(f"JSON 序列化: {product.to_json()}")

    # ========== 7. __mro__ 方法解析顺序 ==========
    print("\n=== 7. __mro__ 方法解析顺序 ===")

    # MRO 决定了多继承时方法查找的顺序（C3 线性化算法）
    print("Duck 类的 MRO（方法解析顺序）:")
    for cls in Duck.__mro__:
        print(f"  -> {cls.__name__}")

    d = D()
    print(f"\n钻石继承 D.method() = {d.method()}")  # B 的方法（B 在 C 前面）
    print("D 类的 MRO:")
    for cls in D.__mro__:
        print(f"  -> {cls.__name__}")


if __name__ == "__main__":
    main()
