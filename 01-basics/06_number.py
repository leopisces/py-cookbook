"""
Python 数字类型

学习目标：
  - int 整数（无限制大小）
  - float 浮点数（双精度 IEEE 754）
  - complex 复数
  - 数字运算与进制转换
  - math 模块常用函数
"""

import math

def main():
    # ========== 1. int 整数类型 ==========
    print("=== 1. int 整数类型 ===")

    # Python 3 的 int 可以表示任意大的整数（无溢出）
    normal = 42
    big = 2 ** 100  # 远超 64 位整数范围
    negative = -123

    print(f"普通整数: {normal}")
    print(f"大整数 2^100 = {big}")
    print(f"大整数的位数: {len(str(big))} 位")
    print(f"负整数: {negative}")

    # 不同进制表示
    print(f"十进制 255 = 二进制 {bin(255)} = 八进制 {oct(255)} = 十六进制 {hex(255)}")
    print(f"二进制 0b1010 = {0b1010}")
    print(f"八进制 0o77 = {0o77}")
    print(f"十六进制 0xFF = {0xFF}")

    # ========== 2. float 浮点数类型 ==========
    print("\n=== 2. float 浮点数类型 ===")

    pi = 3.141592653589793
    sci = 1.5e-3  # 科学计数法

    print(f"π 的近似值: {pi}")
    print(f"科学计数法 1.5e-3 = {sci}")
    print(f"浮点数精度: 0.1 + 0.2 = {0.1 + 0.2}")  # 浮点数精度问题
    print(f"注意: 0.1 + 0.2 不完全等于 0.3!")

    # ========== 3. complex 复数类型 ==========
    print("\n=== 3. complex 复数类型 ===")

    # 使用 j 或 J 表示虚部
    c1 = 3 + 4j
    c2 = complex(1, 2)  # 另一种创建方式

    print(f"复数 c1 = {c1}")
    print(f"复数 c2 = {c2}")
    print(f"实部: real = {c1.real}")
    print(f"虚部: imag = {c1.imag}")
    print(f"共轭: conjugate() = {c1.conjugate()}")
    print(f"加法: c1 + c2 = {c1 + c2}")
    print(f"乘法: c1 * c2 = {c1 * c2}")
    print(f"模 (绝对值): abs(c1) = {abs(c1)}")

    # ========== 4. 常用数学运算 ==========
    print("\n=== 4. 常用数学运算 ===")

    print(f"abs(-5) = {abs(-5)}")                    # 绝对值
    print(f"round(3.14159, 2) = {round(3.14159, 2)}") # 四舍五入
    print(f"pow(2, 10) = {pow(2, 10)}")              # 幂运算（等价于 2**10）
    print(f"divmod(17, 5) = {divmod(17, 5)}")        # 返回 (商, 余数) → (3, 2)
    print(f"max(1, 5, 3, 9) = {max(1, 5, 3, 9)}")    # 最大值
    print(f"min(1, 5, 3, 9) = {min(1, 5, 3, 9)}")    # 最小值
    print(f"sum([1, 2, 3, 4]) = {sum([1, 2, 3, 4])}") # 求和

    # ========== 5. math 模块常用函数 ==========
    print("\n=== 5. math 模块常用函数 ===")

    print(f"math.pi = {math.pi}")                     # 圆周率 π
    print(f"math.e = {math.e}")                       # 自然常数 e
    print(f"math.tau = {math.tau}")                   # 2π
    print(f"math.inf = {math.inf}")                   # 无穷大
    print(f"math.nan = {math.nan}")                   # 非数字

    # 取整相关
    print(f"\n--- 取整相关 ---")
    print(f"math.ceil(3.14) = {math.ceil(3.14)}")     # 向上取整 → 4
    print(f"math.floor(3.14) = {math.floor(3.14)}")   # 向下取整 → 3
    print(f"math.trunc(-3.14) = {math.trunc(-3.14)}") # 截断小数 → -3

    # 指数与对数
    print(f"\n--- 指数与对数 ---")
    print(f"math.sqrt(16) = {math.sqrt(16)}")         # 平方根 → 4.0
    print(f"math.pow(2, 10) = {math.pow(2, 10)}")     # 幂运算 → 1024.0
    print(f"math.exp(1) = {math.exp(1)}")             # e^1
    print(f"math.log(math.e) = {math.log(math.e)}")   # 自然对数 ln(e) → 1.0
    print(f"math.log2(8) = {math.log2(8)}")           # 以2为底 log2(8) → 3.0
    print(f"math.log10(100) = {math.log10(100)}")     # 以10为底 log10(100) → 2.0

    # 三角函数
    print(f"\n--- 三角函数 ---")
    print(f"math.sin(math.pi / 2) = {math.sin(math.pi / 2)}")  # sin(90°) ≈ 1
    print(f"math.cos(0) = {math.cos(0)}")                       # cos(0) = 1
    print(f"math.degrees(math.pi) = {math.degrees(math.pi)}")   # 弧度转角度 → 180
    print(f"math.radians(180) = {math.radians(180)}")           # 角度转弧度 → π

    # 其他常用函数
    print(f"\n--- 其他 ---")
    print(f"math.factorial(5) = {math.factorial(5)}")   # 阶乘 5! = 120
    print(f"math.gcd(48, 18) = {math.gcd(48, 18)}")     # 最大公约数 → 6
    print(f"math.isclose(0.1+0.2, 0.3) = {math.isclose(0.1+0.2, 0.3)}")  # 浮点数近似比较


if __name__ == "__main__":
    main()
