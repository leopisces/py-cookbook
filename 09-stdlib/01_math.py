#!/usr/bin/env python3
"""
math模块 - Python标准库数学函数与常量

涵盖内容:
  1. 数学常量 (pi, e, tau, inf, nan)
  2. 取整函数 (ceil, floor, trunc)
  3. 幂与对数 (sqrt, pow, log, log10, log2, exp)
  4. 三角函数 (sin, cos, tan, asin, acos, atan, atan2)
  5. 角度与弧度转换 (degrees, radians)

参考: https://www.runoob.com/python3/python3-math.html
"""

import math


# ============================================================
# 1. 数学常量
# ============================================================
print("=" * 60)
print("1. 数学常量")
print("=" * 60)

print(f"圆周率 π  = {math.pi}")
print(f"自然常数 e = {math.e}")
print(f"tau (2π)  = {math.tau}")
print(f"正无穷大   = {math.inf}")
print(f"非数字     = {math.nan}")
print(f"-∞ 是否无穷? {math.isinf(-math.inf)}")
print(f"NaN 是否非数字? {math.isnan(math.nan)}")

# ============================================================
# 2. 取整函数
# ============================================================
print("\n" + "=" * 60)
print("2. 取整函数 (ceil / floor / trunc)")
print("=" * 60)

nums = [3.14, 3.78, -3.14, -3.78]

for n in nums:
    print(f"数值: {n:>6.2f}  |  "
          f"ceil={math.ceil(n):>3}  "
          f"floor={math.floor(n):>3}  "
          f"trunc={math.trunc(n):>3}")

print("\n说明: ceil=向上取整, floor=向下取整, trunc=向零取整")

# ============================================================
# 3. 幂与对数
# ============================================================
print("\n" + "=" * 60)
print("3. 幂与对数")
print("=" * 60)

x = 16
print(f"sqrt({x}) 开平方根  = {math.sqrt(x)}")
print(f"pow(2, 10) 2的10次方 = {math.pow(2, 10)}")
print(f"2 ** 10 (内置)       = {2 ** 10}")

print(f"\nlog({math.e}) 自然对数(底e) = {math.log(math.e)}")
print(f"log(100, 10) 底10        = {math.log(100, 10)}")
print(f"log10(1000) 常用对数       = {math.log10(1000)}")
print(f"log2(64) 底2              = {math.log2(64)}")
print(f"exp(2) e的2次方           = {math.exp(2)}")

# ============================================================
# 4. 三角函数
# ============================================================
print("\n" + "=" * 60)
print("4. 三角函数")
print("=" * 60)

# 使用弧度
angle_rad = math.pi / 4  # 45度
print(f"角度 45° = {angle_rad:.4f} 弧度")
print(f"sin(π/4)  = {math.sin(angle_rad):.4f}")
print(f"cos(π/4)  = {math.cos(angle_rad):.4f}")
print(f"tan(π/4)  = {math.tan(angle_rad):.4f}")

# 反三角函数
print(f"\nasin(0.707) = {math.asin(0.707):.4f} rad ≈ {math.degrees(math.asin(0.707)):.1f}°")
print(f"acos(0.707) = {math.acos(0.707):.4f} rad ≈ {math.degrees(math.acos(0.707)):.1f}°")
print(f"atan(1)     = {math.atan(1):.4f} rad ≈ {math.degrees(math.atan(1)):.1f}°")

# atan2(y, x) - 返回从 x 轴到点 (x,y) 的角度
print(f"atan2(1, 1) = {math.atan2(1, 1):.4f} rad ≈ {math.degrees(math.atan2(1, 1)):.1f}°")

# ============================================================
# 5. 角度与弧度转换
# ============================================================
print("\n" + "=" * 60)
print("5. 角度 <-> 弧度转换")
print("=" * 60)

angles_deg = [0, 30, 45, 60, 90, 180, 270, 360]
print(f"{'角度°':>6}  {'弧度':>10}")
print("-" * 22)
for deg in angles_deg:
    rad = math.radians(deg)
    print(f"{deg:>6}  {rad:>10.4f}")

# 演示转换的互逆关系
deg = 57.2958
rad = math.radians(deg)
back_deg = math.degrees(rad)
print(f"\n互逆测试: {deg}° → {rad:.4f} rad → {back_deg:.4f}°")
print("转换后几乎相同,误差在浮点精度范围内")

# ============================================================
# 其他实用函数
# ============================================================
print("\n" + "=" * 60)
print("其他实用函数")
print("=" * 60)
print(f"gcd(36, 48)  最大公约数 = {math.gcd(36, 48)}")
print(f"lcm(12, 18)  最小公倍数 = {math.lcm(12, 18)}")  # Python 3.9+
print(f"factorial(6) 阶乘       = {math.factorial(6)}")
print(f"comb(10, 3)  组合数 C(10,3) = {math.comb(10, 3)}")      # Python 3.8+
print(f"perm(5, 2)   排列数 P(5,2)  = {math.perm(5, 2)}")       # Python 3.8+
print(f"fabs(-3.14)  绝对值(浮点)  = {math.fabs(-3.14)}")
print(f"fmod(7.5, 2) 浮点取余      = {math.fmod(7.5, 2)}")
print(f"copysign(3.0, -1) 复制符号 = {math.copysign(3.0, -1)}")
