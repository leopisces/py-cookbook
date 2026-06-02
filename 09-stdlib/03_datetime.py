#!/usr/bin/env python3
"""
datetime模块 - Python标准库日期与时间处理

涵盖内容:
  1. date 对象 - 日期创建与属性
  2. time 对象 - 时间创建与属性
  3. datetime 对象 - 日期时间创建与操作
  4. strftime / strptime - 格式化与解析
  5. timedelta - 时间差与日期计算

参考: https://www.runoob.com/python3/python3-date-time.html
"""

from datetime import date, time, datetime, timedelta
from datetime import timezone, tzinfo


# ============================================================
# 1. date 对象 - 日期
# ============================================================
print("=" * 60)
print("1. date 对象 - 日期 (年/月/日)")
print("=" * 60)

# 创建日期
d = date.today()
print(f"今天日期:    {d}")
print(f"  指定日期:  {date(2024, 1, 1)}")
print(f"  最小日期:  {date.min}")
print(f"  最大日期:  {date.max}")

# 属性
print(f"\n年: {d.year}, 月: {d.month}, 日: {d.day}")
print(f"星期几 (0=周一, 6=周日): {d.weekday()} → {d.strftime('%A')}")
print(f"ISO格式星期 (1=周一):     {d.isoweekday()}")

# 替换属性
print(f"\n替换年份: {d.replace(year=2020)}")
print(f"ISO日历:   {d.isocalendar()}")  # (年份, 周数, 星期)

# ============================================================
# 2. time 对象 - 时间
# ============================================================
print("\n" + "=" * 60)
print("2. time 对象 - 时间 (时/分/秒/微秒)")
print("=" * 60)

t = time(14, 30, 45, 123456)
print(f"指定时间: {t}")
print(f"  小时: {t.hour}, 分钟: {t.minute}")
print(f"  秒:   {t.second}, 微秒: {t.microsecond}")

print(f"最小时间: {time.min}")
print(f"最大时间: {time.max}")

# ============================================================
# 3. datetime 对象 - 日期+时间
# ============================================================
print("\n" + "=" * 60)
print("3. datetime 对象 - 日期 + 时间")
print("=" * 60)

# 获取当前日期时间
now = datetime.now()
print(f"当前日期时间: {now}")

# 指定日期时间
dt = datetime(2024, 6, 1, 9, 30, 0)
print(f"指定日期时间: {dt}")

# 合并 date 和 time
combined = datetime.combine(date.today(), time(18, 0))
print(f"合并date+time: {combined}")

# 获取 UTC 时间
utc_now = datetime.now(timezone.utc)
print(f"UTC 时间:     {utc_now}")

# 常用属性
print(f"\n年={now.year} 月={now.month} 日={now.day}")
print(f"时={now.hour} 分={now.minute} 秒={now.second}")
print(f"weekday()={now.weekday()}  isoweekday()={now.isoweekday()}")

# timestamp - 时间戳
ts = now.timestamp()
print(f"\n时间戳 (秒): {ts}")
print(f"从时间戳恢复:  {datetime.fromtimestamp(ts)}")

# ============================================================
# 4. 格式化与解析
# ============================================================
print("\n" + "=" * 60)
print("4. strftime / strptime - 格式化与解析")
print("=" * 60)

now = datetime(2024, 6, 1, 14, 30, 45)

# strftime - datetime → 字符串
print("=== strftime: datetime → 字符串 ===")
formats = {
    "%Y-%m-%d":       "标准日期格式",
    "%Y/%m/%d %H:%M": "年月日 时分",
    "%Y年%m月%d日 %H时%M分%S秒": "中文格式",
    "%A, %B %d, %Y":  "星期, 月 日, 年",
    "%Y-%m-%d %I:%M %p": "12小时制",
}
for fmt, desc in formats.items():
    print(f"  {desc:>18}: {now.strftime(fmt)}")

# strptime - 字符串 → datetime
print("\n=== strptime: 字符串 → datetime ===")
s = "2024-06-01 14:30:45"
parsed = datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
print(f"解析 '{s}' → {parsed}")

# ============================================================
# 5. timedelta - 时间差计算
# ============================================================
print("\n" + "=" * 60)
print("5. timedelta - 时间差与日期计算")
print("=" * 60)

today = date.today()
print(f"今天: {today}")

# 时间差
one_day = timedelta(days=1)
one_week = timedelta(weeks=1)

print(f"  1天后:     {today + one_day}")
print(f"  7天后:     {today + one_week}")
print(f"  3天前:     {today - timedelta(days=3)}")
print(f"  30天前:    {today - timedelta(days=30)}")

# timedelta 运算
delta = timedelta(days=10, hours=5, minutes=30, seconds=15)
print(f"\n时间差: 10天5时30分15秒")
print(f"  总秒数:    {delta.total_seconds():.0f} 秒")
print(f"  总天数:    {delta.days} 天")
print(f"  秒部分:    {delta.seconds} 秒 (不含天数部分)")

# 两个日期之间的差值
new_year = date(2025, 1, 1)
diff = new_year - today
print(f"\n距离2025年元旦还有 {diff.days} 天")

# ============================================================
# 实用示例: 计算年龄
# ============================================================
print("\n" + "=" * 60)
print("实用示例: 计算年龄和纪念日")
print("=" * 60)

birthday = date(1995, 8, 15)
today = date.today()
age = today.year - birthday.year
# 如果今年生日还没到,减一岁
if (today.month, today.day) < (birthday.month, birthday.day):
    age -= 1
print(f"生日: {birthday}, 今年 {today.year} 年为 {age} 岁")

# 下周的同一天
print(f"今天是: {today} ({today.strftime('%A')})")
print(f"7天后:  {today + timedelta(days=7)} ({ (today + timedelta(days=7)).strftime('%A') })")
