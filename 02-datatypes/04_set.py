"""
Python 集合 (Set)

学习目标：
  - 集合的创建与基本操作
  - 元素的增加与删除
  - 集合运算: 交集、并集、差集、对称差集
  - 子集与超集判断
  - frozenset 不可变集合
  - 集合的应用场景（去重、关系测试）
"""

def main():
    # ========== 1. 集合的创建 ==========
    print("=== 1. 集合的创建 ===")

    # 多种创建方式
    s1 = {1, 2, 3, 4, 5}                     # 字面量创建
    s2 = set([1, 2, 2, 3, 3, 3])             # 从列表创建（自动去重）
    s3 = set("hello")                         # 从字符串创建（字符去重）
    s4 = set()                                # 空集合（不能用 {}，那是空字典）

    print(f"字面量: {s1}")
    print(f"从列表去重: {s2}")
    print(f"从字符串去重: {s3}")
    print(f"空集合: {s4}")
    print(f"注意: {{}} 创建的是 {type({}).__name__}，不是 set!")

    # ========== 2. 元素的增删 ==========
    print("\n=== 2. 元素的增删 ===")

    fruits = {"苹果", "香蕉", "橘子"}
    print(f"初始集合: {fruits}")

    # 增加
    fruits.add("葡萄")                        # 添加单个元素
    print(f"add('葡萄'): {fruits}")

    fruits.add("苹果")                        # 添加重复元素（无效，集合元素唯一）
    print(f"add('苹果') 重复: {fruits}")

    fruits.update(["西瓜", "草莓"])          # 批量添加
    print(f"update(...): {fruits}")

    # 删除
    fruits.remove("香蕉")                     # 删除元素（不存在则报错）
    print(f"remove('香蕉'): {fruits}")

    fruits.discard("芒果")                    # 删除元素（不存在也不报错）
    print(f"discard('芒果'): {fruits} (不报错)")

    popped = fruits.pop()                     # 随机删除并返回一个元素
    print(f"pop() -> '{popped}', 剩余: {fruits}")

    fruits.clear()                            # 清空集合
    print(f"clear(): {fruits}")

    # ========== 3. 集合运算 ==========
    print("\n=== 3. 集合运算 ===")

    A = {1, 2, 3, 4, 5}
    B = {4, 5, 6, 7, 8}
    print(f"集合 A: {A}")
    print(f"集合 B: {B}")

    # 交集 & — 两个集合都有的元素
    print(f"\n交集 A & B:              {A & B}")
    print(f"交集 A.intersection(B):   {A.intersection(B)}")

    # 并集 | — 两个集合的所有元素（去重）
    print(f"并集 A | B:              {A | B}")
    print(f"并集 A.union(B):         {A.union(B)}")

    # 差集 - — 在 A 中但不在 B 中
    print(f"差集 A - B:              {A - B}")
    print(f"差集 B - A:              {B - A}")
    print(f"差集 A.difference(B):     {A.difference(B)}")

    # 对称差集 ^ — 只在其中一个集合中的元素
    print(f"对称差 A ^ B:                      {A ^ B}")
    print(f"对称差 A.symmetric_difference(B):   {A.symmetric_difference(B)}")

    # ========== 4. 子集与超集判断 ==========
    print("\n=== 4. 子集与超集判断 ===")

    small = {1, 2}
    large = {1, 2, 3, 4}

    print(f"small = {small}, large = {large}")
    print(f"small.issubset(large):    {small.issubset(large)}")
    print(f"small <= large:           {small <= large}")
    print(f"large.issuperset(small):  {large.issuperset(small)}")
    print(f"large >= small:           {large >= small}")

    # 真子集与真超集（不包含相等的情况）
    equal = {1, 2}
    print(f"\nequal = {equal}")
    print(f"small <= equal:   {small <= equal}")         # 子集（包含相等） → True
    print(f"small < equal:    {small < equal}")          # 真子集（不包含相等） → False
    print(f"small.isdisjoint({3, 4}): {small.isdisjoint({3, 4})}")  # 是否无交集

    # ========== 5. frozenset 不可变集合 ==========
    print("\n=== 5. frozenset 不可变集合 ===")

    # frozenset 创建后不可修改
    fs = frozenset([1, 2, 3, 4])
    print(f"frozenset: {fs}")
    print(f"类型: {type(fs).__name__}")

    # frozenset 支持所有集合运算
    fs2 = frozenset([3, 4, 5, 6])
    print(f"fs & fs2: {fs & fs2}")

    # frozenset 可以作为字典的键或集合的元素（普通 set 不行）
    frozen_set_dict = {
        frozenset([1, 2]): "A组",
        frozenset([3, 4]): "B组",
    }
    print(f"frozenset 作为字典键: {frozen_set_dict}")

    # 普通 set 不能作为集合元素（因为 set 是可变的）
    # set_of_sets = {{1, 2}, {3, 4}}  # TypeError!
    set_of_frozensets = {frozenset([1, 2]), frozenset([3, 4])}
    print(f"frozenset 组成的集合: {set_of_frozensets}")

    # ========== 6. 应用场景 ==========
    print("\n=== 6. 集合应用场景 ===")

    # 场景1: 列表去重
    dup_list = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
    unique = list(set(dup_list))
    print(f"列表去重: {dup_list} -> {unique}")

    # 场景2: 找出两个列表中相同的元素（交集）
    list_a = [1, 2, 3, 4, 5, 6]
    list_b = [4, 5, 6, 7, 8, 9]
    common = list(set(list_a) & set(list_b))
    print(f"共同元素: {list_a} ∩ {list_b} = {common}")

    # 场景3: 集合推导式
    squares_set = {x**2 for x in range(10)}
    print(f"平方集合: {squares_set}")

    # 场景4: in 操作 — 集合的成员检查非常快（基于哈希表）
    large_set = set(range(10000))
    print(f"5000 在集合中? {5000 in large_set}")
    print("注意: 集合的 in 操作是 O(1)，而列表是 O(n)!")


if __name__ == "__main__":
    main()
