#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
statistics模块 - Python标准库统计计算

涵盖内容:
  1. mean / fmean - 平均值
  2. median / median_low / median_high - 中位数
  3. mode / multimode - 众数
  4. stdev / variance - 标准差与方差
  5. 数据统计综合示例

参考: https://docs.python.org/zh-cn/3/library/statistics.html
"""

import statistics


# ============================================================
# 1. mean / fmean - 平均数
# ============================================================
print("=" * 60)
print("1. mean / fmean - 平均数")
print("=" * 60)

data = [85, 92, 78, 90, 88, 95, 82, 89, 91, 87]

# mean - 算术平均值 (返回 float)
avg = statistics.mean(data)
print(f"成绩数据: {data}")
print(f"  算术平均值 (mean):      {avg:.2f}")

# fmean - 快速浮点平均值 (Python 3.8+, 专为浮点优化)
f_avg = statistics.fmean(data)
print(f"  快速均值 (fmean):       {f_avg:.2f}")

# 加权平均值示例
weights = [1, 1, 1, 2, 1, 2, 1, 1, 1, 1]  # 某些成绩权重更高
print(f"\n加权数据: 成绩={data}")
print(f"          权重={weights}")
weighted_avg = sum(x * w for x, w in zip(data, weights)) / sum(weights)
print(f"  加权平均值: {weighted_avg:.2f}")

# ============================================================
# 2. median - 中位数
# ============================================================
print("\n" + "=" * 60)
print("2. median - 中位数 (及变体)")
print("=" * 60)

# 奇数个数据
odd_data = [1, 3, 5, 7, 9]
print(f"奇数数据: {sorted(odd_data)}")
print(f"  median (中位数):      {statistics.median(odd_data)}")
print(f"  median_low (低中位):  {statistics.median_low(odd_data)}")
print(f"  median_high (高中位): {statistics.median_high(odd_data)}")

# 偶数个数据
even_data = [1, 3, 5, 7, 9, 11]
print(f"\n偶数数据: {sorted(even_data)}")
print(f"  median (中位数):      {statistics.median(even_data)}")  # 5和7的平均
print(f"  median_low (低中位):  {statistics.median_low(even_data)}")  # 5
print(f"  median_high (高中位): {statistics.median_high(even_data)}") # 7

# ============================================================
# 3. mode / multimode - 众数
# ============================================================
print("\n" + "=" * 60)
print("3. mode / multimode - 众数")
print("=" * 60)

# 单一众数
mode_data = [1, 2, 2, 3, 4, 4, 4, 5, 5]
print(f"数据: {sorted(mode_data)}")
print(f"  mode (众数):      {statistics.mode(mode_data)}")

# 多众数 (multimode, Python 3.8+)
multi_mode_data = [1, 1, 2, 2, 3, 4, 5]
print(f"\n数据 (多众数): {sorted(multi_mode_data)}")
print(f"  multimode: {statistics.multimode(multi_mode_data)}")

# mode 是字符串也可以
words = ["apple", "banana", "apple", "orange", "banana", "apple"]
print(f"\n字符串数据: {words}")
print(f"  mode: {statistics.mode(words)}")

# ============================================================
# 4. stdev / variance - 标准差与方差
# ============================================================
print("\n" + "=" * 60)
print("4. 标准差与方差")
print("=" * 60)

scores = [85, 92, 78, 90, 88, 95, 82, 89, 91, 87]

# pstdev / pvariance - 总体标准差/方差
# stdev / variance  - 样本标准差/方差
p_var = statistics.pvariance(scores)   # 总体方差 (除以 N)
s_var = statistics.variance(scores)    # 样本方差 (除以 N-1)
p_std = statistics.pstdev(scores)      # 总体标准差
s_std = statistics.stdev(scores)       # 样本标准差

print(f"成绩数据: {scores}")
print(f"  总体方差 (pvariance): {p_var:.2f}")
print(f"  样本方差 (variance):  {s_var:.2f}")
print(f"  总体标准差 (pstdev):  {p_std:.2f}")
print(f"  样本标准差 (stdev):   {s_std:.2f}")

print(f"\n说明:")
print(f"  总体: 用于描述整个数据集, 除以 N")
print(f"  样本: 用于从样本推断总体, 除以 N-1 (无偏估计)")

# 展示数据分布
print(f"\n数据分布特征:")
print(f"  最大值: {max(scores)}, 最小值: {min(scores)}")
print(f"  极差:   {max(scores) - min(scores)}")
print(f"  均值:   {avg:.1f}")
print(f"  68%数据落在 [{avg - s_std:.1f}, {avg + s_std:.1f}] 区间内 (正态分布假设)")
print(f"  95%数据落在 [{avg - 2 * s_std:.1f}, {avg + 2 * s_std:.1f}] 区间内")

# ============================================================
# 5. 综合统计示例
# ============================================================
print("\n" + "=" * 60)
print("5. 综合统计示例 - 数据分析报告")
print("=" * 60)


def analyze_data(name, data):
    """生成数据统计摘要"""
    n = len(data)
    total = sum(data)
    avg = statistics.mean(data)
    med = statistics.median(data)
    std = statistics.stdev(data) if n > 1 else 0
    try:
        mode_val = statistics.mode(data)
    except statistics.StatisticsError:
        mode_val = "无单一众数"

    print(f"\n[==] {name} 统计报告 (n={n})")
    print(f"  总和:     {total}")
    print(f"  均值:     {avg:.2f}")
    print(f"  中位数:   {med}")
    print(f"  众数:     {mode_val}")
    print(f"  标准差:   {std:.2f}")
    print(f"  最小值:   {min(data)}")
    print(f"  最大值:   {max(data)}")


# 示例1: 学生成绩
analyze_data("学生成绩", [85, 92, 78, 90, 88, 95, 82, 89, 91, 87, 76, 93, 84, 88, 90])

# 示例2: 网站日访问量
analyze_data("网站日访问量",
             [120, 135, 142, 128, 156, 134, 140, 138, 145, 132, 150, 148, 141])

# 示例3: 均匀分布
analyze_data("均匀分布", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# ============================================================
# 6. 其他统计函数
# ============================================================
print("\n" + "=" * 60)
print("6. 其他实用函数")
print("=" * 60)

data = [1, 2, 2, 3, 4, 5, 6, 7, 8, 9]

# quantiles - 分位数 (Python 3.8+)
quantiles = statistics.quantiles(data, n=4)
print(f"quantiles (四分位数): {quantiles}")
print(f"  即 Q1={quantiles[0]}, Q2={quantiles[1]}, Q3={quantiles[2]}")

# harmonic_mean - 调和平均数
print(f"\nharmonic_mean([40, 60]): {statistics.harmonic_mean([40, 60]):.2f}")
print(f"  适用场景: 速率/密度等")

# geometric_mean - 几何平均数 (Python 3.8+)
print(f"geometric_mean([2, 8]): {statistics.geometric_mean([2, 8])}")

# correlation / covariance (Python 3.10+)
x = [1, 2, 3, 4, 5]
y = [2, 4, 5, 4, 7]
print(f"\n相关性分析:")
print(f"  x: {x}")
print(f"  y: {y}")
try:
    corr = statistics.correlation(x, y)
    print(f"  correlation (皮尔逊相关系数): {corr:.4f}")
except AttributeError:
    print(f"  correlation 需要 Python 3.10+")
