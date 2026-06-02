"""
Python 列表 (List)

学习目标：
  - 列表的创建与初始化
  - 索引、切片操作
  - 增删改查方法 (append, extend, insert, remove, pop)
  - 排序与反转 (sort, reverse, sorted)
  - 列表嵌套与多维操作
  - 列表复制 (浅拷贝与深拷贝)
"""

def main():
    # ========== 1. 列表的创建 ==========
    print("=== 1. 列表的创建 ===")

    # 多种创建方式
    empty = []                              # 空列表
    nums = [1, 2, 3, 4, 5]                # 整数列表
    mixed = [1, "hello", 3.14, True]      # 混合类型列表
    nested = [[1, 2], [3, 4], [5, 6]]     # 嵌套列表

    print(f"空列表: {empty}")
    print(f"整数列表: {nums}")
    print(f"混合类型: {mixed}")
    print(f"嵌套列表: {nested}")

    # 使用 list() 构造函数
    chars = list("abcde")                   # 从字符串创建
    from_range = list(range(1, 6))          # 从 range 创建
    print(f"从字符串: {chars}")
    print(f"从 range: {from_range}")

    # 列表推导式创建
    squares = [x ** 2 for x in range(6)]
    evens = [x for x in range(10) if x % 2 == 0]
    print(f"平方列表: {squares}")
    print(f"偶数列表: {evens}")

    # ========== 2. 索引与切片 ==========
    print("\n=== 2. 索引与切片 ===")

    fruits = ["苹果", "香蕉", "橘子", "葡萄", "西瓜"]
    print(f"原始列表: {fruits}")

    # 索引
    print(f"索引 0: {fruits[0]}")
    print(f"索引 -1 (最后一个): {fruits[-1]}")
    print(f"索引 -2 (倒数第二): {fruits[-2]}")

    # 切片
    print(f"fruits[1:4]  = {fruits[1:4]}")     # 索引 1-3
    print(f"fruits[:3]   = {fruits[:3]}")      # 前 3 个
    print(f"fruits[2:]   = {fruits[2:]}")      # 从索引 2 到末尾
    print(f"fruits[::2]  = {fruits[::2]}")     # 每隔一个取
    print(f"fruits[::-1] = {fruits[::-1]}")    # 反转列表

    # ========== 3. 增删改查 ==========
    print("\n=== 3. 增删改查 ===")

    todo = ["学习Python", "写代码"]

    # --- 增加 ---
    print(f"初始: {todo}")

    todo.append("跑步")            # 末尾追加
    print(f"append('跑步'): {todo}")

    todo.insert(1, "吃饭")         # 在索引 1 处插入
    print(f"insert(1, '吃饭'): {todo}")

    todo.extend(["睡觉", "阅读"])  # 扩展列表
    print(f"extend(['睡觉', '阅读']): {todo}")

    # --- 修改 ---
    todo[0] = "学习Python高级特性"
    print(f"修改索引0: {todo}")

    # --- 查找 ---
    if "睡觉" in todo:
        idx = todo.index("睡觉")
        print(f"'睡觉' 在索引 {idx} 处")
    print(f"'玩游戏' 在列表中吗? {'玩游戏' in todo}")

    # --- 删除 ---
    removed = todo.pop()               # 弹出最后一个
    print(f"pop() → '{removed}', 剩余: {todo}")

    removed2 = todo.pop(1)             # 弹出索引 1
    print(f"pop(1) → '{removed2}', 剩余: {todo}")

    todo.remove("跑步")                # 删除第一个匹配的值
    print(f"remove('跑步'): {todo}")

    del todo[0]                        # del 删除指定索引
    print(f"del todo[0]: {todo}")

    # ========== 4. 排序与反转 ==========
    print("\n=== 4. 排序与反转 ===")

    numbers = [3, 1, 4, 1, 5, 9, 2, 6]
    print(f"原始: {numbers}")

    # sort() — 原地排序
    numbers.sort()
    print(f"sort() 升序: {numbers}")

    numbers.sort(reverse=True)
    print(f"sort(reverse=True) 降序: {numbers}")

    # sorted() — 返回新列表（不改变原列表）
    original = [5, 2, 8, 1, 9]
    sorted_list = sorted(original)
    print(f"sorted() 返回新列表: {sorted_list}, 原列表不变: {original}")

    # 自定义排序: 按字符串长度
    words = ["apple", "kiwi", "banana", "pear", "grape"]
    words.sort(key=len)
    print(f"按长度排序: {words}")

    # reverse() — 原地反转
    nums = [1, 2, 3, 4, 5]
    nums.reverse()
    print(f"reverse(): {nums}")

    # ========== 5. 常用方法 ==========
    print("\n=== 5. 常用方法 ===")

    data = [10, 20, 30, 40, 50]

    print(f"列表: {data}")
    print(f"len(): 长度 = {len(data)}")
    print(f"count(20): 出现次数 = {data.count(20)}")
    print(f"max(): 最大值 = {max(data)}")
    print(f"min(): 最小值 = {min(data)}")
    print(f"sum(): 总和 = {sum(data)}")

    # copy() — 浅拷贝
    copy_list = data.copy()
    print(f"copy(): {copy_list}")

    # clear() — 清空列表
    temp = [1, 2, 3]
    temp.clear()
    print(f"clear(): {temp}")

    # ========== 6. 列表嵌套 ==========
    print("\n=== 6. 列表嵌套（二维列表）===")

    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]

    print("二维矩阵:")
    for row in matrix:
        print(f"  {row}")

    # 访问嵌套元素
    print(f"matrix[0][0] = {matrix[0][0]}")     # 第一行第一列
    print(f"matrix[1][2] = {matrix[1][2]}")     # 第二行第三列
    print(f"matrix[2][1] = {matrix[2][1]}")     # 第三行第二列

    # 修改嵌套元素
    matrix[1][1] = 99
    print(f"修改后 matrix[1][1] = 99:")
    for row in matrix:
        print(f"  {row}")

    # 浅拷贝与深拷贝的区别
    print("\n--- 浅拷贝 vs 深拷贝 ---")
    import copy

    nested_list = [[1, 2], [3, 4]]
    shallow_copy = nested_list.copy()         # 浅拷贝
    deep_copy = copy.deepcopy(nested_list)    # 深拷贝

    nested_list[0][0] = 999
    print(f"原列表修改后: {nested_list}")
    print(f"浅拷贝 (受影响): {shallow_copy}")
    print(f"深拷贝 (不受影响): {deep_copy}")


if __name__ == "__main__":
    main()
