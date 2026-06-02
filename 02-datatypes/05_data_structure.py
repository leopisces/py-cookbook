"""
Python 数据结构

学习目标：
  - 栈：用列表实现栈（LIFO 后进先出）
  - 队列：用 collections.deque 实现队列（FIFO 先进先出）
  - 堆（优先队列）：用 heapq 模块实现
  - 各数据类型对比与选择指南
"""

from collections import deque
import heapq

def main():
    # ========== 1. 栈 (Stack) — 后进先出 LIFO ==========
    print("=== 1. 栈 (Stack) — 后进先出 LIFO ===")

    # Python 列表天然支持栈操作
    stack = []
    print("模拟浏览器前进/后退:")

    # push — 入栈（访问新页面）
    stack.append("首页")
    stack.append("新闻页")
    stack.append("详情页")
    print(f"浏览路径: {stack}")

    # pop — 出栈（后退）
    page = stack.pop()
    print(f"后退: 离开 '{page}'")
    print(f"当前栈: {stack}")

    page = stack.pop()
    print(f"再后退: 离开 '{page}'")
    print(f"当前栈: {stack} (只剩 '{stack[-1]}')")

    # peek — 查看栈顶元素
    if stack:
        print(f"当前页面: {stack[-1]}")

    # 栈的完整演示: 括号匹配
    print("\n--- 括号匹配检查 ---")
    def is_balanced(expr):
        """使用栈检查括号是否匹配"""
        stack_b = []
        pairs = {")": "(", "]": "[", "}": "{"}
        for ch in expr:
            if ch in "([{":
                stack_b.append(ch)
            elif ch in ")]}":
                if not stack_b or stack_b.pop() != pairs[ch]:
                    return False
        return len(stack_b) == 0

    print(f'"([]){{}}" 匹配? {is_balanced("([]){}")}')
    print(f'"(])" 匹配? {is_balanced("(])")}')

    # ========== 2. 队列 (Queue) — 先进先出 FIFO ==========
    print("\n=== 2. 队列 (Queue) — 先进先出 FIFO ===")

    # 用 deque 实现高效队列（list 的 pop(0) 是 O(n)，deque 的 popleft() 是 O(1)）
    queue = deque()
    print("模拟排队系统:")

    # 入队 — 来人排队
    queue.append("张三")
    queue.append("李四")
    queue.append("王五")
    print(f"排队中: {list(queue)}")

    # 出队 — 第一个人办业务
    person = queue.popleft()
    print(f"服务: {person}, 剩余排队: {list(queue)}")

    # 继续入队
    queue.append("赵六")
    queue.append("孙七")
    print(f"新人加入: {list(queue)}")

    # 连续服务
    while queue:
        person = queue.popleft()
        print(f"服务: {person}, 剩余: {list(queue)}")

    # deque 的其他操作
    print("\n--- deque 双向操作 ---")
    d = deque([1, 2, 3])
    d.appendleft(0)          # 从左边插入
    d.pop()                  # 从右边弹出
    print(f"deque 双向操作后: {d}")
    d.rotate(1)              # 向右旋转
    print(f"rotate(1) 后: {d}")
    d.rotate(-2)             # 向左旋转
    print(f"rotate(-2) 后: {d}")

    # ========== 3. 堆 (Heap) — 优先队列 ==========
    print("\n=== 3. 堆 (Heap) — 优先队列 ===")

    # heapq 默认实现最小堆（根节点最小）
    nums = [3, 1, 4, 1, 5, 9, 2, 6]
    print(f"原始列表: {nums}")

    # heapify — 原地转换为堆
    heapq.heapify(nums)
    print(f"堆化后 (heapify): {nums}")
    print(f"注意: 堆只保证 nums[0] 是最小值，不保证完全有序")

    # heappush — 入堆
    heap = []
    print("\n模拟任务调度 (数字小=优先级高):")
    heapq.heappush(heap, 3)
    heapq.heappush(heap, 1)
    heapq.heappush(heap, 4)
    heapq.heappush(heap, 2)
    print(f"插入 3,1,4,2 后: {heap}")

    # heappop — 出堆（总是弹出最小的）
    print("按优先级处理:")
    while heap:
        task = heapq.heappop(heap)
        print(f"  处理优先级 {task} 的任务, 堆剩余: {heap}")

    # Top-K 问题 — 找出最大的 K 个元素
    scores = [78, 92, 85, 63, 99, 88, 76]
    top3 = heapq.nlargest(3, scores)
    bottom3 = heapq.nsmallest(3, scores)
    print(f"\n成绩: {scores}")
    print(f"前三名: {top3}")
    print(f"后三名: {bottom3}")

    # 最大堆 — 通过取负值实现
    max_heap = []
    for x in [3, 1, 4, 2]:
        heapq.heappush(max_heap, -x)  # 负数入堆
    print(f"\n最大堆 (取负): {[-x for x in max_heap]}")
    print(f"pop 最大值: { -heapq.heappop(max_heap)}")

    # ========== 4. 数据类型对比与选择 ==========
    print("\n=== 4. 数据类型对比与选择 ===")

    print("""
    ┌──────────┬──────────┬──────────┬────────────┬──────────────────────┐
    │ 数据类型  │ 是否可变  │ 是否有序  │ 是否可重复  │ 选择场景             │
    ├──────────┼──────────┼──────────┼────────────┼──────────────────────┤
    │ list     │ 可变      │ 有序      │ 可重复      │ 通用有序集合         │
    │ tuple    │ 不可变    │ 有序      │ 可重复      │ 常数值、多返回值     │
    │ dict     │ 可变      │ 3.7+有序  │ 键不可重复  │ 键值对映射、快速查找 │
    │ set      │ 可变      │ 无序      │ 不可重复    │ 去重、集合运算       │
    │ frozenset│ 不可变    │ 无序      │ 不可重复    │ 不可变的去重集合     │
    │ deque    │ 可变      │ 有序      │ 可重复      │ 队列/栈(高效两端操作)│
    └──────────┴──────────┴──────────┴────────────┴──────────────────────┘
    """)

    # 时间复杂度对比
    print("时间复杂度对比:")
    print("  列表 append: O(1)  |  列表 insert(0): O(n)")
    print("  列表 in: O(n)      |  集合 in: O(1)")
    print("  字典 get: O(1)     |  deque popleft: O(1)")
    print("  堆 push/pop: O(log n)")


if __name__ == "__main__":
    main()
