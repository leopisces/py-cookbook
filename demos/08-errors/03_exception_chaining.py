"""
Python 错误处理 - 异常链与高级模式

学习目标：
  - raise ... from ... 显式异常链
  - raise ... from None 切断异常链
  - __cause__ / __context__ 属性
  - 分层异常转换设计
"""


class DataError(Exception):
    """数据层异常"""
    pass


class ServiceError(Exception):
    """服务层异常"""
    pass


def load_data():
    """底层函数可能抛出原始异常"""
    raise DataError("数据库连接超时")


def process_data():
    """上层函数捕获并转换为业务异常"""
    try:
        load_data()
    except DataError as e:
        # raise ... from ... 保留原始异常链
        raise ServiceError("数据处理失败") from e


def main():
    # ========== 1. 异常链：raise ... from ... ==========
    print("=" * 50)
    print("1. 异常链：raise ... from ...")
    print("=" * 50)

    try:
        process_data()
    except ServiceError as e:
        print(f"  捕获到: {e}")
        print(f"  原始异常: {e.__cause__}")
        print(f"  异常链: {type(e).__name__} -> {type(e.__cause__).__name__}")

    # raise ... from None 可以切断异常链
    print("\n--- from None 切断异常链 ---")
    try:
        try:
            raise ValueError("内部错误")
        except ValueError:
            raise RuntimeError("外部错误") from None
    except RuntimeError as e:
        print(f"  捕获: {e}")
        print(f"  原始异常: {e.__cause__}")  # None


if __name__ == "__main__":
    main()

# ============================================================
# 相关主题:
#   - 05-oop/03_magic_methods.py  → __enter__/__exit__ 异常处理中的上下文
# ============================================================
