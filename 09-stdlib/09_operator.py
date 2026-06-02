#!/usr/bin/env python3
"""
operator模块 - Python标准库函数式操作符

涵盖内容:
  1. itemgetter - 获取可迭代元素的指定项
  2. attrgetter - 获取对象属性
  3. methodcaller - 调用对象方法
  4. 比较运算符函数 (lt, le, eq, ne, gt, ge)
  5. 算术/位运算符函数
  6. 排序优化实战

参考: https://docs.python.org/zh-cn/3/library/operator.html
"""

import operator


# ============================================================
# 1. itemgetter - 从可迭代对象中获取元素
# ============================================================
print("=" * 60)
print("1. operator.itemgetter() - 获取可迭代元素")
print("=" * 60)

# 类似 lambda x: x[n] 但更高效
get_second = operator.itemgetter(1)
get_first_third = operator.itemgetter(0, 2)

data = [10, 20, 30, 40]
print(f"列表: {data}")
print(f"  itemgetter(1) → {get_second(data)}")         # 20
print(f"  itemgetter(0, 2) → {get_first_third(data)}")  # (10, 30)

# 用于字典
get_name = operator.itemgetter("name")
person = {"name": "张三", "age": 25, "city": "北京"}
print(f"\n字典: {person}")
print(f"  itemgetter('name') → {get_name(person)}")

# 组合多个字段
get_info = operator.itemgetter("name", "age")
print(f"  itemgetter('name','age') → {get_info(person)}")

# ============================================================
# 2. attrgetter - 获取对象属性
# ============================================================
print("\n" + "=" * 60)
print("2. operator.attrgetter() - 获取对象属性")
print("=" * 60)


class Student:
    def __init__(self, name, score, grade):
        self.name = name
        self.score = score
        self.grade = grade

    def __repr__(self):
        return f"Student(name='{self.name}', score={self.score}, grade='{self.grade}')"


students = [
    Student("Alice", 92, "A"),
    Student("Bob", 78, "B"),
    Student("Charlie", 85, "B"),
    Student("David", 65, "C"),
]

get_score = operator.attrgetter("score")
get_name_score = operator.attrgetter("name", "score")

print("学生列表:")
for s in students:
    print(f"  {s}")

# 按属性排序
sorted_by_score = sorted(students, key=get_score)
print(f"\n按 score 升序排序:")
for s in sorted_by_score:
    print(f"  {s}")

sorted_by_name = sorted(students, key=operator.attrgetter("name"))
print(f"\n按 name 排序:")
for s in sorted_by_name:
    print(f"  {s}")

# ============================================================
# 3. methodcaller - 调用对象方法
# ============================================================
print("\n" + "=" * 60)
print("3. operator.methodcaller() - 调用对象方法")
print("=" * 60)

# methodcaller('方法名', 参数...) → 可调用对象
upper = operator.methodcaller("upper")
replace = operator.methodcaller("replace", "World", "Python")

print(f"methodcaller('upper')('hello') → {upper('hello')}")
print(f"methodcaller('replace','World','Python')('Hello World') →")
print(f"  {replace('Hello World')}")

# 列表操作
fruits = ["apple", "  banana  ", "Orange", "  grape  "]
print(f"\n原始列表: {fruits}")

# 对列表中每个元素调用 strip() 和 upper()
strip_all = map(operator.methodcaller("strip"), fruits)
print(f"全部 strip: {list(strip_all)}")

upper_all = map(operator.methodcaller("upper"), ["hello", "world", "python"])
print(f"全部 upper: {list(upper_all)}")

# ============================================================
# 4. 比较运算符函数
# ============================================================
print("\n" + "=" * 60)
print("4. 比较运算符函数")
print("=" * 60)

a, b = 10, 20

comparisons = [
    ("lt (小于)",  operator.lt,  "a < b"),
    ("le (小于等于)", operator.le, "a <= b"),
    ("eq (等于)",    operator.eq, "a == b"),
    ("ne (不等于)",   operator.ne, "a != b"),
    ("gt (大于)",    operator.gt,  "a > b"),
    ("ge (大于等于)", operator.ge, "a >= b"),
]

print(f"a={a}, b={b}")
for name, op, expr in comparisons:
    result = op(a, b)
    print(f"  {name:<16} {expr:<8} = {result}")

# 字符串比较
print(f"\n字符串比较:")
print(f"  operator.eq('hello', 'hello') = {operator.eq('hello', 'hello')}")
print(f"  operator.lt('apple', 'banana') = {operator.lt('apple', 'banana')}")

# ============================================================
# 5. 算术/逻辑/位运算符
# ============================================================
print("\n" + "=" * 60)
print("5. 算术 / 逻辑 / 位运算符函数")
print("=" * 60)

# 算术
print("=== 算术 ===")
print(f"  add(3, 5)   加法 = {operator.add(3, 5)}")
print(f"  sub(10, 3)  减法 = {operator.sub(10, 3)}")
print(f"  mul(4, 7)   乘法 = {operator.mul(4, 7)}")
print(f"  truediv(10, 3) 真除法 = {operator.truediv(10, 3)}")
print(f"  floordiv(10, 3) 整除 = {operator.floordiv(10, 3)}")
print(f"  mod(10, 3)  取余 = {operator.mod(10, 3)}")
print(f"  pow(2, 10)  幂 = {operator.pow(2, 10)}")
print(f"  neg(-5)     取负 = {operator.neg(-5)}")

# 逻辑
print("\n=== 逻辑 ===")
print(f"  truth(0)    = {operator.truth(0)}")
print(f"  truth(42)   = {operator.truth(42)}")
print(f"  not_(True)  = {operator.not_(True)}")
print(f"  is_(None, None) = {operator.is_(None, None)}")
print(f"  is_not(1, 2)    = {operator.is_not(1, 2)}")

# 位运算
print("\n=== 位运算 ===")
a, b = 0b1100, 0b1010  # 12 和 10
print(f"  a={a}(0b{a:04b}), b={b}(0b{b:04b})")
print(f"  and_  = {operator.and_(a, b):>4} (0b{operator.and_(a, b):04b})")
print(f"  or_   = {operator.or_(a, b):>4} (0b{operator.or_(a, b):04b})")
print(f"  xor   = {operator.xor(a, b):>4} (0b{operator.xor(a, b):04b})")
print(f"  lshift(a,1) = {operator.lshift(a, 1)}")
print(f"  rshift(a,2) = {operator.rshift(a, 2)}")

# ============================================================
# 6. 排序优化实战
# ============================================================
print("\n" + "=" * 60)
print("6. 排序优化实战 - itemgetter / attrgetter 排序")
print("=" * 60)

# 多级排序: 先按成绩降序, 再按名字升序
print("多级排序 (先按成绩降序, 再按名字升序):")
sorted_students = sorted(students,
                         key=operator.attrgetter("score"),
                         reverse=True)
for s in sorted_students:
    print(f"  {s}")

# 多字段字典排序
records = [
    {"name": "产品A", "price": 99, "sales": 500},
    {"name": "产品B", "price": 199, "sales": 300},
    {"name": "产品C", "price": 99, "sales": 800},
    {"name": "产品D", "price": 299, "sales": 100},
]

print("\n字典列表多字段排序 (先price, 再sales):")
sorted_records = sorted(records, key=operator.itemgetter("price", "sales"))
for r in sorted_records:
    print(f"  {r['name']}: ${r['price']}, 销量{r['sales']}")

# 性能对比说明
print("\n性能说明:")
print("  operator.itemgetter(n) ≈ 比 lambda x: x[n] 快 10-30%")
print("  operator.attrgetter(n)  ≈ 比 lambda x: x.n 快 15-40%")
print("  关键点: C 实现的函数调用开销更低")

# reduce 用法 (functools, 但常与 operator 搭配)
from functools import reduce

nums = [1, 2, 3, 4, 5]
print(f"\nreduce + operator 示例:")
print(f"  reduce(add, [1,2,3,4,5]) = {reduce(operator.add, nums)}  (累加)")
print(f"  reduce(mul, [1,2,3,4,5]) = {reduce(operator.mul, nums)}  (累乘)")
