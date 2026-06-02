"""
Python 运算符

学习目标：
  - 算术运算符 (+, -, *, /, //, %, **)
  - 比较运算符 (==, !=, >, <, >=, <=)
  - 赋值运算符 (=, +=, -=, *=, /= 等)
  - 逻辑运算符 (and, or, not)
  - 位运算符 (&, |, ^, ~, <<, >>)
  - 成员运算符 (in, not in)
  - 身份运算符 (is, is not)
  - 运算符优先级
"""

def main():
    # ========== 1. 算术运算符 ==========
    print("=== 1. 算术运算符 ===")
    a, b = 10, 3

    print(f"a = {a}, b = {b}")
    print(f"加法 a + b = {a + b}")       # 13
    print(f"减法 a - b = {a - b}")       # 7
    print(f"乘法 a * b = {a * b}")       # 30
    print(f"除法 a / b = {a / b}")       # 3.333... (浮点数)
    print(f"整除 a // b = {a // b}")     # 3 (向下取整)
    print(f"取余 a % b = {a % b}")       # 1
    print(f"幂运算 a ** b = {a ** b}")   # 1000
    # Python 没有 ++ 和 -- 运算符
    a += 1
    print(f"自增(用+=) a += 1 → a = {a}")

    # ========== 2. 比较运算符 ==========
    print("\n=== 2. 比较运算符 ===")
    x, y = 5, 10

    print(f"x = {x}, y = {y}")
    print(f"x == y: {x == y}")     # 等于
    print(f"x != y: {x != y}")     # 不等于
    print(f"x > y: {x > y}")       # 大于
    print(f"x < y: {x < y}")       # 小于
    print(f"x >= y: {x >= y}")     # 大于等于
    print(f"x <= y: {x <= y}")     # 小于等于
    # 链式比较（Python 独有特性）
    print(f"1 < x < 10: {1 < x < 10}")  # x 在 1 到 10 之间

    # ========== 3. 赋值运算符 ==========
    print("\n=== 3. 赋值运算符 ===")
    n = 10
    print(f"初始值 n = {n}")

    n += 5  # 等价于 n = n + 5
    print(f"n += 5  → n = {n}")

    n -= 3  # 等价于 n = n - 3
    print(f"n -= 3  → n = {n}")

    n *= 2  # 等价于 n = n * 2
    print(f"n *= 2  → n = {n}")

    n //= 4  # 等价于 n = n // 4
    print(f"n //= 4 → n = {n}")

    # 海象运算符 := (Python 3.8+) - 在表达式中赋值
    if (length := len("hello")) > 3:
        print(f"海象运算符: 字符串长度={length} > 3")

    # ========== 4. 逻辑运算符 ==========
    print("\n=== 4. 逻辑运算符 ===")
    p, q = True, False

    print(f"p = {p}, q = {q}")
    print(f"p and q = {p and q}")  # 逻辑与：都为真才为真
    print(f"p or q  = {p or q}")   # 逻辑或：有一个为真即为真
    print(f"not p   = {not p}")     # 逻辑非：取反
    print(f"not q   = {not q}")

    # 短路求值
    print("True or 报错" + " ← 不会报错（or 短路）")
    result = 0 and (1 / 0)  # 不会执行 1/0，因为 and 短路
    print(f"0 and (会报错的表达式) = {result}（短路求值）")

    # ========== 5. 位运算符 ==========
    print("\n=== 5. 位运算符 ===")
    # 位运算操作整数的二进制位
    a, b = 60, 13  # 60=0b111100, 13=0b001101

    print(f"a = {a} (二进制: {bin(a)})")
    print(f"b = {b} (二进制: {bin(b)})")
    print(f"按位与 a & b   = {a & b}   (二进制: {bin(a & b)})")
    print(f"按位或 a | b   = {a | b}  (二进制: {bin(a | b)})")
    print(f"按位异或 a ^ b  = {a ^ b}   (二进制: {bin(a ^ b)})")
    print(f"按位取反 ~a     = {~a} (补码表示)")
    print(f"左移 a << 2     = {a << 2}  (二进制: {bin(a << 2)})")
    print(f"右移 a >> 2     = {a >> 2}   (二进制: {bin(a >> 2)})")

    # ========== 6. 成员运算符 ==========
    print("\n=== 6. 成员运算符 ===")
    fruits = ["苹果", "香蕉", "橘子"]

    print(f"列表: {fruits}")
    print(f"'苹果' 在列表中吗? {'苹果' in fruits}")
    print(f"'西瓜' 在列表中吗? {'西瓜' in fruits}")
    print(f"'西瓜' 不在列表中吗? {'西瓜' not in fruits}")

    text = "Hello Python"
    print(f"\n字符串: \"{text}\"")
    print(f"\"Py\" 在字符串中吗? {'Py' in text}")
    print(f"\"py\" 在字符串中吗? {'py' in text}")  # 区分大小写

    # ========== 7. 身份运算符 ==========
    print("\n=== 7. 身份运算符 ===")
    # is 判断两个变量是否引用同一个对象（内存地址相同）
    # == 判断两个变量的值是否相等

    list1 = [1, 2, 3]
    list2 = [1, 2, 3]
    list3 = list1

    print(f"list1 = {list1}, list2 = {list2}, list3 = list1")
    print(f"list1 == list2: {list1 == list2}")  # 值相等 → True
    print(f"list1 is list2: {list1 is list2}")  # 不是同一对象 → False
    print(f"list1 is list3: {list1 is list3}")  # 同一对象 → True

    # None 始终用 is 判断
    val = None
    print(f"val is None: {val is None}")  # 推荐写法
    print(f"val == None: {val == None}")  # 不推荐

    # ========== 8. 运算符优先级 ==========
    print("\n=== 8. 运算符优先级 ===")
    # 从高到低: ** → * / // % → + - → 比较 → not → and → or
    # 不确定时用括号明确优先级！

    result1 = 2 + 3 * 4       # 先乘后加: 2 + 12 = 14
    result2 = (2 + 3) * 4     # 括号优先: 5 * 4 = 20
    result3 = 2 ** 3 * 2      # 先幂后乘: 8 * 2 = 16
    result4 = not True or False  # 先 not 后 or

    print(f"2 + 3 * 4 = {result1}     （先乘法）")
    print(f"(2 + 3) * 4 = {result2}   （括号优先）")
    print(f"2 ** 3 * 2 = {result3}     （先幂后乘）")
    print(f"not True or False = {result4}")
    print("\n建议: 不确定优先级时，使用括号明确意图!")


if __name__ == "__main__":
    main()
