"""
Python 错误处理 - 自定义异常类

学习目标：
  - 自定义异常类的基本写法
  - __str__ / __repr__ 与异常信息展示
  - 业务异常与验证异常的设计
  - raise 抛出异常
"""


class ValidationError(Exception):
    """自定义验证异常"""
    def __init__(self, field, value, message="验证失败"):
        self.field = field
        self.value = value
        self.message = f"{message}: 字段 '{field}' 的值 '{value}' 不合法"
        super().__init__(self.message)


class BusinessError(Exception):
    """自定义业务异常（带错误码）"""
    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")


def validate_age(age):
    """验证年龄是否合法"""
    if not isinstance(age, int):
        raise ValidationError("age", age, "类型错误")
    if age < 0 or age > 150:
        raise ValidationError("age", age, "范围错误")
    return age


def transfer_money(amount, balance):
    """模拟转账操作"""
    if amount <= 0:
        raise BusinessError("E001", "转账金额必须大于0")
    if amount > balance:
        raise BusinessError("E002", f"余额不足（余额: {balance}, 需要: {amount}）")
    return balance - amount


def main():
    # ========== 1. 自定义异常 ==========
    print("=" * 50)
    print("1. 自定义异常")
    print("=" * 50)

    # 验证异常 - 测试
    test_ages = [25, -5, "abc"]
    for age in test_ages:
        try:
            valid = validate_age(age)
            print(f"  年龄 {valid} 验证通过")
        except ValidationError as e:
            print(f"  {e}")

    # 业务异常
    print()
    try:
        transfer_money(500, 300)
    except BusinessError as e:
        print(f"  {e.message}")


if __name__ == "__main__":
    main()
