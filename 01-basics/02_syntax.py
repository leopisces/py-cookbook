"""
Python 基础语法

学习目标：
  - 缩进规则（用缩进代替大括号）
  - 多行语句（行连接符）
  - 同行多语句（分号分隔）
  - 代码组概念（if/while/for/def）
"""

def main():
    # ========== 1. 缩进规则 ==========
    print("=== 1. 缩进规则 ===")
    # Python 使用缩进来表示代码块，同一代码块的缩进必须一致
    x = 10
    if x > 5:
        print("x 大于 5")          # 缩进 4 个空格（推荐）
        if x > 8:
            print("x 大于 8")      # 嵌套缩进 8 个空格
    print("if 语句块结束")          # 回到外层，缩进取消

    # 错误示范（注释掉的无效代码，展示缩进重要性）:
    # if True:
    # print("缩进错误")  # 缺少缩进会报 IndentationError
    # if True:
    #   print("这是2空格")
    #     print("这是4空格")  # 不一致缩进会报错

    # ========== 2. 多行语句 ==========
    print("\n=== 2. 多行语句 ===")
    # 方式一：使用反斜杠 \ 连接多行
    total = 1 + 2 + 3 + \
            4 + 5 + 6
    print(f"使用 \\ 连接多行: {total}")

    # 方式二：在括号内可以自由换行（推荐）
    result = (100
              + 200
              + 300)
    print(f"使用括号换行: {result}")

    # 列表、元组、字典也可自由换行
    fruits = [
        "苹果",
        "香蕉",
        "橘子",
        "葡萄",
    ]
    print(f"多行列表: {fruits}")

    # ========== 3. 同行多语句 ==========
    print("\n=== 3. 同行多语句 ===")
    # 使用分号 ; 将多个语句写在同一行（不推荐，降低可读性）
    a = 1; b = 2; c = 3
    print(f"a={a}, b={b}, c={c}")

    # ========== 4. 代码组概念 ==========
    print("\n=== 4. 代码组概念 ===")
    # 以 : 结尾的复合语句（if, while, for, def, class）后面必须跟着缩进的代码块

    # if-elif-else 代码组
    score = 85
    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    else:
        grade = "D"
    print(f"分数 {score} -> 等级 {grade}")

    # while 循环代码组
    count = 0
    result = []
    while count < 3:
        result.append(count)
        count += 1
    print(f"while 循环结果: {result}")

    # for 循环代码组
    squares = []
    for i in range(1, 5):
        squares.append(i * i)
    print(f"for 循环结果: {squares}")

    # def 函数代码组
    def greet(name):
        """简单的问候函数"""
        return f"你好，{name}！"

    print(greet("Python"))

    # ========== 5. 空语句 pass ==========
    print("\n=== 5. pass 占位语句 ===")
    # pass 是什么都不做的占位语句，用于语法上需要但逻辑上暂无内容的场景
    if True:
        pass  # 暂时留空，将来再补充

    for _ in range(1):
        pass  # 循环体暂不执行任何操作

    def future_function():
        pass  # 函数暂时没有实现

    print("pass 语句不执行任何操作，仅用于占位")


if __name__ == "__main__":
    main()
