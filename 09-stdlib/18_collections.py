"""
collections模块 - Python标准库专用容器数据类型

涵盖内容:
  1. namedtuple - 命名元组（创建、访问、替换、转换为dict）
  2. defaultdict - 默认字典（不同default_factory类型）
  3. Counter - 计数器（统计、算术运算）
  4. deque - 双端队列（高效操作、性能对比）
  5. OrderedDict - 有序字典（排序控制）
  6. ChainMap - 链式映射（多字典合并查找）

参考: https://docs.python.org/zh-cn/3/library/collections.html
"""

from collections import namedtuple, defaultdict, Counter, deque, OrderedDict, ChainMap
import timeit


def deque_vs_list_performance(n=50000):
    """对比deque和list在左侧插入的性能差异"""
    d = deque()
    lst = []

    def deque_left_insert():
        for i in range(n):
            d.appendleft(i)

    def list_left_insert():
        for i in range(n):
            lst.insert(0, i)

    deque_time = timeit.timeit(deque_left_insert, number=1)
    list_time = timeit.timeit(list_left_insert, number=1)
    return deque_time, list_time


def main():
    # ============================================================
    # 1. namedtuple - 命名元组
    # ============================================================
    print("=" * 50)
    print("1. namedtuple (命名元组)")
    print("=" * 50)

    # 创建: 定义字段名 -> 实例化
    Point = namedtuple("Point", ["x", "y"])
    p1 = Point(3, 4)
    print(f"创建命名元组 Point(x=3, y=4): {p1}")

    # 通过名称和索引访问
    print(f"  按名称访问: p1.x={p1.x}, p1.y={p1.y}")
    print(f"  按索引访问: p1[0]={p1[0]}, p1[1]={p1[1]}")

    # _replace - 替换字段, 返回新实例 (原对象不变)
    p2 = p1._replace(x=10)
    print(f"  _replace(x=10): {p2} (原对象不变: {p1})")

    # _asdict - 转换为 OrderedDict
    d = p2._asdict()
    print(f"  _asdict(): {d} (类型: {type(d).__name__})")

    # _make - 从可迭代对象创建
    p3 = Point._make([7, 8])
    print(f"  _make([7, 8]): {p3}")

    # _fields - 查看字段名
    print(f"  _fields: {Point._fields}")

    # 应用示例: 定义 RGB 颜色
    Color = namedtuple("Color", ["r", "g", "b"])
    white = Color(255, 255, 255)
    red = Color(255, 0, 0)
    print(f"\n  颜色示例: 白色={white}, 红色={red}")

    # ============================================================
    # 2. defaultdict - 默认字典
    # ============================================================
    print("\n" + "=" * 50)
    print("2. defaultdict (默认字典)")
    print("=" * 50)

    # int 作为 default_factory - 计数场景
    dd_int = defaultdict(int)
    chars = "abracadabra"
    for c in chars:
        dd_int[c] += 1  # 首次访问自动初始化为 0
    print(f"defaultdict(int) 计数 '{chars}':")
    print(f"  {dict(dd_int)}")

    # list 作为 default_factory - 分组场景
    dd_list = defaultdict(list)
    students = [("一班", "张三"), ("二班", "李四"), ("一班", "王五"), ("二班", "赵六")]
    for grade, name in students:
        dd_list[grade].append(name)
    print(f"\ndefaultdict(list) 分组:")
    for grade, names in dd_list.items():
        print(f"  {grade}: {names}")

    # set 作为 default_factory - 去重收集
    dd_set = defaultdict(set)
    data = [("A", 1), ("A", 2), ("A", 1), ("B", 3)]  # ("A", 1) 重复
    for key, val in data:
        dd_set[key].add(val)
    print(f"\ndefaultdict(set) 去重收集: {dict(dd_set)}")

    # lambda 作为 default_factory - 自定义默认值
    dd_custom = defaultdict(lambda: "未找到")
    dd_custom["name"] = "Alice"
    print(f"\ndefaultdict(lambda): dd['name']={dd_custom['name']}, dd['age']={dd_custom['age']}")

    # 与普通 dict 对比
    print("\n[对比] 普通 dict 处理缺失键:")
    normal_dict = {}
    key = "missing"
    try:
        val = normal_dict[key]
    except KeyError:
        print(f"  dict['{key}'] -> KeyError 异常 (需手动检查或使用 get/setdefault)")
    print(f"  defaultdict(int)['{key}'] -> 自动返回默认值 0, 无需 try/except")

    # ============================================================
    # 3. Counter - 计数器
    # ============================================================
    print("\n" + "=" * 50)
    print("3. Counter (计数器)")
    print("=" * 50)

    # 从可迭代对象创建
    words = "mississippi"
    cnt = Counter(words)
    print(f"Counter('{words}'): {cnt}")

    # most_common - 最常见的 N 个元素
    print(f"  most_common(2): {cnt.most_common(2)}")
    print(f"  most_common(): {cnt.most_common()} (全部, 按频率降序)")

    # elements - 按计数展开所有元素
    print(f"  elements(): {list(cnt.elements())} (每个元素重复对应次数)")

    # 算术运算: + - & |
    cnt_a = Counter(a=3, b=1)
    cnt_b = Counter(a=1, b=2, c=3)
    print(f"\n  计数器 a: {dict(cnt_a)}")
    print(f"  计数器 b: {dict(cnt_b)}")
    print(f"  a + b (求和): {dict(cnt_a + cnt_b)}")
    print(f"  a - b (求差, 只保留正数): {dict(cnt_a - cnt_b)}")
    print(f"  a & b (交集, 取最小值): {dict(cnt_a & cnt_b)}")
    print(f"  a | b (并集, 取最大值): {dict(cnt_a | cnt_b)}")

    # 从列表统计词频
    fruits = ["apple", "banana", "apple", "orange", "banana", "apple"]
    fruit_cnt = Counter(fruits)
    print(f"\n  水果统计: {fruit_cnt}")
    print(f"  出现最多的水果: '{fruit_cnt.most_common(1)[0][0]}' ({fruit_cnt.most_common(1)[0][1]}次)")

    # ============================================================
    # 4. deque - 双端队列
    # ============================================================
    print("\n" + "=" * 50)
    print("4. deque (双端队列)")
    print("=" * 50)

    # 创建与双端操作
    d = deque([1, 2, 3])
    print(f"初始: deque([1, 2, 3])")

    d.append(4)
    print(f"  append(4) -> 右侧追加: {d}")

    d.appendleft(0)
    print(f"  appendleft(0) -> 左侧追加: {d}")

    right = d.pop()
    print(f"  pop() -> 右侧弹出: {d} (弹出了 {right})")

    left = d.popleft()
    print(f"  popleft() -> 左侧弹出: {d} (弹出了 {left})")

    # extend / extendleft
    d.extend([5, 6])
    print(f"  extend([5, 6]) -> 右侧扩展: {d}")

    d.extendleft([-1, -2])
    print(f"  extendleft([-1, -2]) -> 左侧扩展: {d} (注意: 迭代顺序反转)")

    # rotate - 旋转
    d_rot = deque([1, 2, 3, 4, 5])
    print(f"\n旋转前: {d_rot}")
    d_rot.rotate(2)
    print(f"  rotate(2) -> 右旋2位: {d_rot}")
    d_rot.rotate(-3)
    print(f"  rotate(-3) -> 左旋3位: {d_rot}")

    # maxlen - 固定长度队列 (达到上限自动丢弃对面端元素)
    d_fixed = deque(maxlen=3)
    for item in [1, 2, 3, 4, 5]:
        d_fixed.append(item)
        print(f"  append({item}) -> {list(d_fixed)} (maxlen=3, 左侧自动丢弃)")
    print(f"  最终: {list(d_fixed)}")

    # 性能对比: deque vs list 左侧插入
    print(f"\n[性能对比] deque vs list 左侧插入 (n=50000):")
    d_time, lst_time = deque_vs_list_performance()
    print(f"  deque.appendleft: {d_time:.4f}s")
    print(f"  list.insert(0):   {lst_time:.4f}s")
    print(f"  deque 快约 {lst_time / d_time:.0f} 倍 (因为 list.insert(0) 是 O(n), deque 是 O(1))")

    # ============================================================
    # 5. OrderedDict - 有序字典
    # ============================================================
    print("\n" + "=" * 50)
    print("5. OrderedDict (有序字典)")
    print("=" * 50)

    print("[注] Python 3.7+ 的普通 dict 已默认保持插入顺序")
    print("     OrderedDict 主要通过 move_to_end() / popitem() 提供额外功能\n")

    od = OrderedDict()
    od["a"] = 1
    od["b"] = 2
    od["c"] = 3
    print(f"初始 (插入顺序): {od}")

    # move_to_end - 将指定键移到最后 (或最前)
    od.move_to_end("a")
    print(f"  move_to_end('a'):       {od} (将 'a' 移到最后)")

    od.move_to_end("c", last=False)
    print(f"  move_to_end('c', False): {od} (将 'c' 移到最前)")

    # popitem - 弹出末端 (或首端) 键值对
    od2 = OrderedDict([("x", 10), ("y", 20), ("z", 30)])
    last = od2.popitem()
    print(f"\n  popitem() 弹出: {last}, 剩余: {od2} (默认 last=True, 弹出最后)")

    first = od2.popitem(last=False)
    print(f"  popitem(last=False) 弹出: {first}, 剩余: {od2} (弹出最前)")

    # 相等性比较: OrderedDict 关注顺序
    od_a = OrderedDict([("a", 1), ("b", 2)])
    od_b = OrderedDict([("b", 2), ("a", 1)])
    print(f"\n  OrderedDict 相等比较 (关注顺序):")
    print(f"    {od_a} == {od_b} -> {od_a == od_b} (顺序不同 -> 不等)")
    print(f"    dict 相等比较 (不关注顺序):")
    print(f"    {dict(od_a)} == {dict(od_b)} -> {dict(od_a) == dict(od_b)} (顺序无关)")

    # ============================================================
    # 6. ChainMap - 链式映射
    # ============================================================
    print("\n" + "=" * 50)
    print("6. ChainMap (链式映射)")
    print("=" * 50)

    # 模拟配置作用域: 命令行 > 环境变量 > 默认值 (均用 str 值便于演示)
    defaults = {"host": "localhost", "port": "8080", "debug": "off"}
    env_vars = {"host": "prod-server", "debug": "on"}
    cli_args = {"port": "9090"}

    cm = ChainMap(cli_args, env_vars, defaults)
    print(f"默认配置:   {defaults}")
    print(f"环境变量:   {env_vars}")
    print(f"命令行参数: {cli_args}")
    print(f"\nChainMap 合并查找 (优先级: 命令行 > 环境 > 默认):")
    print(f"  cm['host']  = '{cm['host']}'  (来自环境变量)")
    print(f"  cm['port']  = '{cm['port']}'  (来自命令行)")
    print(f"  cm['debug'] = '{cm['debug']}'  (来自环境变量)")

    # .maps 属性 - 查看所有映射
    print(f"\n  cm.maps: {cm.maps} (第一个是最高优先级)")

    # new_child - 在链前添加新映射
    cm2 = cm.new_child({"host": "override-host"})
    print(f"\n  new_child 后 (增加了更高优先级的临时映射):")
    print(f"  cm2['host'] = '{cm2['host']}' (来自 new_child)")
    print(f"  cm2.maps: {cm2.maps}")

    # parents - 去除最前面的映射
    cm_parents = cm2.parents
    print(f"\n  cm2.parents 后 (去除了最前面的映射):")
    print(f"  cm_parents['host'] = '{cm_parents['host']}' (回退到环境变量)")
    print(f"  cm_parents.maps: {cm_parents.maps}")

    # 作用域模拟示例
    print(f"\n[示例] ChainMap 模拟 Python 变量作用域:")
    builtins_scope = {"print": print, "len": len, "max": max}
    global_scope = {"x": 10, "y": 20}
    local_scope = {"x": 100}

    scope = ChainMap(local_scope, global_scope, builtins_scope)
    print(f"  局部 x={scope['x']} (覆盖了全局), 全局 y={scope['y']}")
    print(f"  查找流程: local -> global -> builtins (LEGB 规则)")


if __name__ == "__main__":
    main()
