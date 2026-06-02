#!/usr/bin/env python3
"""
json模块 - Python标准库JSON数据序列化

涵盖内容:
  1. dumps - Python对象 → JSON字符串
  2. loads - JSON字符串 → Python对象
  3. dump / load - JSON文件读写
  4. 自定义JSON编码器 (JSONEncoder)
  5. JSON格式美化与中文处理

参考: https://www.runoob.com/python3/python3-json.html
"""

import json
import os
import tempfile


# ============================================================
# 1. dumps - Python 对象 → JSON 字符串
# ============================================================
print("=" * 60)
print("1. dumps() - Python对象 → JSON字符串")
print("=" * 60)

# Python → JSON 类型映射表
data = {
    "name": "张三",
    "age": 25,
    "score": 95.5,
    "is_active": True,
    "hobbies": ["编程", "读书", "跑步"],
    "address": None,
    "scores": {"语文": 90, "数学": 95, "英语": 88},
}

json_str = json.dumps(data)
print(f"默认紧凑格式:\n{json_str}")

# ============================================================
# 2. JSON格式美化与中文处理
# ============================================================
print("\n" + "=" * 60)
print("2. 格式化参数 (indent / sort_keys / ensure_ascii)")
print("=" * 60)

# indent - 缩进美化
print("美化缩进 (indent=2):")
print(json.dumps(data, indent=2))

# sort_keys - 键排序
print("\n键排序 (sort_keys=True):")
print(json.dumps(data, indent=2, sort_keys=True))

# ensure_ascii=False - 保留中文字符
print("\n保留中文 (ensure_ascii=False):")
print(json.dumps(data, indent=2, ensure_ascii=False))

# 对比 ASCII 编码
print(f"\nensure_ascii=True:  {json.dumps({'姓名': '张三'})}")
print(f"ensure_ascii=False: {json.dumps({'姓名': '张三'}, ensure_ascii=False)}")

# ============================================================
# 3. loads - JSON 字符串 → Python 对象
# ============================================================
print("\n" + "=" * 60)
print("3. loads() - JSON字符串 → Python对象")
print("=" * 60)

json_str = '''
{
    "name": "李四",
    "age": 30,
    "scores": [85, 92, 78],
    "meta": {"city": "北京", "job": "工程师"}
}
'''

obj = json.loads(json_str)
print(f"解析结果类型: {type(obj).__name__}")
print(f"  name:  {obj['name']}")
print(f"  age:   {obj['age']}")
print(f"  scores: {obj['scores']}")
print(f"  meta:   {obj['meta']}")

# JSON <-> Python 类型对应
print("\nJSON <-> Python 类型对应:")
type_demo = {
    "object → dict": json.loads('{"a": 1}'),
    "array  → list": json.loads('[1, 2, 3]'),
    "string → str":  json.loads('"hello"'),
    "number → int":  json.loads('42'),
    "number → float":json.loads('3.14'),
    "true   → bool": json.loads('true'),
    "null   → None": json.loads('null'),
}
for k, v in type_demo.items():
    print(f"  {k:<20} → {repr(v):<15} ({type(v).__name__})")

# ============================================================
# 4. dump / load - JSON文件读写
# ============================================================
print("\n" + "=" * 60)
print("4. dump() / load() - JSON文件读写")
print("=" * 60)

# 使用临时文件演示
tmpfile = tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json',
                                      encoding='utf-8')
tmpfile.close()  # 先关闭, 只使用其路径
tmp_path = tmpfile.name

try:
    # dump - 写入文件
    with open(tmp_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"已写入临时文件: {tmp_path}")

    # load - 从文件读取
    with open(tmp_path, 'r', encoding='utf-8') as f:
        loaded = json.load(f)
    print(f"从文件读取: name={loaded['name']}, age={loaded['age']}")
finally:
    # 清理临时文件
    os.unlink(tmp_path)
    print(f"已删除临时文件")

# ============================================================
# 5. 自定义JSON编码器
# ============================================================
print("\n" + "=" * 60)
print("5. 自定义JSON编码器 - 序列化特殊类型")
print("=" * 60)

from datetime import datetime, date


class CustomEncoder(json.JSONEncoder):
    """自定义编码器: 处理 datetime/date/set 等不可序列化类型"""

    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(o, date):
            return o.strftime("%Y-%m-%d")
        elif isinstance(o, set):
            return list(o)
        return super().default(o)


# 包含特殊类型的数据
special_data = {
    "created_at": datetime(2024, 6, 1, 10, 30, 0),
    "event_date": date(2024, 6, 15),
    "tags": {"Python", "JSON", "教程"},
    "message": "包含特殊类型"
}

# 使用自定义编码器
json_str = json.dumps(special_data, cls=CustomEncoder, ensure_ascii=False, indent=2)
print(f"序列化结果:\n{json_str}")

# 另一种方式: 使用 default 参数
json_str2 = json.dumps(
    special_data,
    default=lambda o: o.isoformat() if hasattr(o, 'isoformat') else list(o) if isinstance(o, set) else str(o),
    ensure_ascii=False,
    indent=2,
)
print(f"\n使用 default 参数:\n{json_str2}")

# ============================================================
# 6. JSON 实用技巧
# ============================================================
print("\n" + "=" * 60)
print("6. JSON 实用技巧")
print("=" * 60)

# 紧凑格式 vs 美化格式
compact = json.dumps(data, separators=(',', ':'))  # 最紧凑
print(f"紧凑格式 (最省空间): {len(compact)} 字节")

beautiful = json.dumps(data, indent=4, ensure_ascii=False)
print(f"美化格式 (最易读):   {len(beautiful)} 字节")

# 跳过不可序列化的值
from json import JSONDecodeError

# 验证 JSON 字符串是否合法
valid_json = '{"name": "test", "value": 123}'
invalid_json = '{"name": "test", "value": 123,}'  # 多余逗号

for js, label in [(valid_json, "合法"), (invalid_json, "非法")]:
    try:
        json.loads(js)
        print(f"\n{label} JSON: [OK] 解析成功")
    except JSONDecodeError as e:
        print(f"\n{label} JSON: [XX] {e}")

# 从 JSON 字符串提取特定字段 (不完整解析)
print("\n使用 object_hook 处理加载:")
json_src = '{"type": "user", "data": {"name": "王五", "age": 28}}'


def hook(obj):
    """object_hook: 在解析每个 dict 时调用"""
    if 'type' in obj:
        print(f"  检测到类型: {obj['type']}")
    return obj


result = json.loads(json_src, object_hook=hook)
print(f"  最终结果: {result}")
