"""
Python 测试 - pytest 基础与核心功能

学习目标：
  - pytest 安装与基本用法
  - 编写和运行第一个测试
  - assert 断言机制详解
  - pytest 常用命令行选项
  - @pytest.fixture 基础与作用域
  - @pytest.mark.parametrize 参数化测试
  - @pytest.mark 测试标记(skip/xfail/custom)
  - pytest.raises 异常测试

运行方式：
  python 15-testing/01_pytest_basics.py    # 运行概念演示
  pytest 15-testing/01_pytest_basics.py -v  # 运行测试
"""

# ============================================================
# 导入处理(兼容 python 和 pytest 两种运行方式)
# ============================================================
try:
    import pytest
except ImportError:
    # 当通过 python 直接运行时，提供一个最小化的 dummy pytest
    # 使 @pytest.fixture 等装饰器不会在 import 时崩溃
    class _Dummy:
        @staticmethod
        def fixture(*a, **kw):
            return lambda f: f

        class mark:
            skip = staticmethod(lambda *a, **kw: lambda f: f)
            xfail = staticmethod(lambda *a, **kw: lambda f: f)
            parametrize = staticmethod(lambda *a, **kw: lambda f: f)

        @staticmethod
        def param(*a, **kw):
            return a[0] if a else None

        class raises:
            def __init__(self, *a, **kw):
                pass

            def __enter__(self):
                return self

            def __exit__(self, *a):
                return True

    pytest = _Dummy()


# ============================================================
# 测试函数区域(由 pytest 发现并运行)
# ============================================================

# --- 1. 基本断言 ---

def test_simple_assertion():
    """最基本的测试：用 assert 验证条件"""
    assert 1 + 1 == 2
    assert "hello".upper() == "HELLO"
    assert len([1, 2, 3]) == 3


def test_assert_with_message():
    """assert 可以附带失败消息"""
    x = 42
    assert x > 0, f"期望 x > 0，但 x = {x}"
    assert isinstance(x, int), f"期望整数，实际类型为 {type(x).__name__}"


def test_comparison_operators():
    """断言支持所有比较运算符"""
    assert 10 > 5
    assert 10 >= 10
    assert 5 < 10
    assert 5 <= 5
    assert 10 == 10
    assert 10 != 5
    # 身份比较
    a = [1, 2]
    b = a
    assert a is b
    assert a is not [1, 2]


def test_collection_assertions():
    """对集合类型的断言"""
    # 列表
    assert [1, 2, 3] == [1, 2, 3]
    assert 3 in [1, 2, 3]
    assert [1, 2, 3] != [3, 2, 1]

    # 字典
    d = {"name": "Alice", "age": 30}
    assert "name" in d
    assert d["age"] == 30
    assert d.get("city", "unknown") == "unknown"

    # 字符串
    assert "hello pytest".startswith("hello")
    assert "hello pytest".endswith("pytest")
    assert "pytest" in "hello pytest"


def test_float_approximation():
    """浮点数比较：使用 pytest.approx 避免精度问题"""
    result = 0.1 + 0.2
    # 不要直接 assert result == 0.3(浮点精度问题)
    assert result == pytest.approx(0.3)
    assert 1.0 / 3.0 == pytest.approx(0.333333, abs=0.001)
    # 列表中的浮点数也适用
    assert [0.1 + 0.2, 1.0 / 3.0] == pytest.approx([0.3, 0.333333], abs=0.001)


# --- 2. Fixture 基础 ---

@pytest.fixture
def sample_list():
    """一个简单的 fixture：提供测试数据"""
    return [1, 2, 3, 4, 5]


def test_using_fixture(sample_list):
    """测试函数使用 fixture 作为参数"""
    assert len(sample_list) == 5
    assert sum(sample_list) == 15
    assert sample_list[0] == 1
    assert sample_list[-1] == 5


@pytest.fixture
def setup_teardown_fixture():
    """带 setup/teardown 的 fixture(使用 yield)"""
    # setup: 测试前准备
    print("\n  [fixture setup] 初始化资源...")
    resource = {"connected": True, "data": []}

    yield resource  # 将资源传给测试

    # teardown: 测试后清理(即使测试失败也会执行)
    print("  [fixture teardown] 清理资源...")
    resource["connected"] = False
    resource["data"].clear()


def test_fixture_teardown(setup_teardown_fixture):
    """验证 fixture 的 setup 和 teardown"""
    res = setup_teardown_fixture
    assert res["connected"] is True
    res["data"].append("test_record")
    assert len(res["data"]) == 1


# --- 3. Fixture 作用域 ---

_fixture_call_counts = {"function": 0, "module": 0}


@pytest.fixture(scope="function")
def func_scoped_fixture():
    """函数级 fixture：每个测试函数调用一次"""
    _fixture_call_counts["function"] += 1
    return _fixture_call_counts["function"]


@pytest.fixture(scope="module")
def module_scoped_fixture():
    """模块级 fixture：整个模块只调用一次"""
    _fixture_call_counts["module"] += 1
    return _fixture_call_counts["module"]


def test_function_scope_1(func_scoped_fixture, module_scoped_fixture):
    """函数级 fixture 每次测试都重新创建"""
    assert func_scoped_fixture >= 1
    assert module_scoped_fixture == 1  # 模块级，始终为 1


def test_function_scope_2(func_scoped_fixture, module_scoped_fixture):
    """模块级 fixture 在整个模块中只创建一次"""
    assert func_scoped_fixture >= 2  # 第二个测试调用，计数 >= 2
    assert module_scoped_fixture == 1  # 模块级，仍为 1


# --- 4. 参数化测试 ---

@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
    (100, -50, 50),
])
def test_parametrized_addition(a, b, expected):
    """参数化测试：一组数据跑多次"""
    assert a + b == expected


@pytest.mark.parametrize("text, expected", [
    ("hello", "HELLO"),
    ("Python", "PYTHON"),
    ("pytest", "PYTEST"),
])
def test_parametrized_string_upper(text, expected):
    """参数化字符串测试"""
    assert text.upper() == expected


@pytest.mark.parametrize("value, expected", [
    pytest.param(2, True, id="偶数-2"),
    pytest.param(7, False, id="奇数-7"),
    pytest.param(0, True, id="偶数-0"),
    pytest.param(-3, False, id="奇数-负三"),
])
def test_parametrized_with_ids(value, expected):
    """参数化测试：使用 pytest.param 自定义测试 ID"""
    assert (value % 2 == 0) == expected


# --- 5. 测试标记 ---

@pytest.mark.skip(reason="演示 skip 标记：此测试被永久跳过")
def test_skip_demo():
    """此测试永远不会执行"""
    assert False  # 这行不会被执行


@pytest.mark.xfail(reason="演示 xfail：预期此测试会失败")
def test_xfail_demo():
    """xfail：标记预期失败的测试"""
    assert 1 + 1 == 3  # 预期失败，xfail 标记让 pytest 不将其视为错误


@pytest.mark.xfail(reason="演示 xfail strict：预期失败但实际通过")
def test_xfail_unexpected_pass():
    """当 xfail 测试意外通过时，显示 XPASS"""
    assert 1 + 1 == 2  # 这会通过，产生 XPASS(意外通过)


# --- 6. 异常测试 ---

def test_raises_exception():
    """使用 pytest.raises 验证异常"""
    with pytest.raises(ZeroDivisionError):
        1 / 0

    with pytest.raises(ValueError):
        int("not_a_number")

    with pytest.raises(KeyError):
        {}["nonexistent"]


def test_raises_match():
    """pytest.raises 可以匹配异常消息"""
    with pytest.raises(ValueError, match="invalid literal.*int"):
        int("abc")

    with pytest.raises(TypeError, match="can only concatenate str"):
        "hello" + 5  # type: ignore[operator]


def test_raises_retrieve_exception():
    """从 pytest.raises 获取异常对象，进一步断言"""
    with pytest.raises(ValueError) as exc_info:
        int("abc")
    assert "invalid literal" in str(exc_info.value)
    assert isinstance(exc_info.value, ValueError)


# ============================================================
# Demo 演示函数区域(由 python 直接运行)
# ============================================================

def demo_installation():
    """演示 pytest 安装与基本用法"""
    print("=" * 60)
    print("1. pytest 安装与基本用法")
    print("=" * 60)

    print('''
    [安装 pytest]
      pip install pytest

    [运行测试的几种方式]
      pytest                          # 自动发现并运行所有测试
      pytest test_file.py             # 运行指定文件
      pytest test_file.py::test_func  # 运行指定测试函数
      pytest tests/                   # 运行指定目录下所有测试
      pytest -k "pattern"             # 按关键字匹配运行

    [pytest 自动发现规则]
      - 文件名以 test_ 开头或以 _test 结尾
      - 测试函数以 test_ 开头
      - 测试类以 Test 开头(不含 __init__ 方法)''')


def demo_first_test():
    """演示编写第一个测试"""
    print("=" * 60)
    print("2. 编写第一个测试")
    print("=" * 60)

    print('''
    pytest 测试就是普通的 Python 函数，函数名以 test_ 开头：

      def test_addition():
          assert 1 + 1 == 2

      def test_string_methods():
          assert "hello".upper() == "HELLO"
          assert "WORLD".lower() == "world"

    [运行结果符号]
      .  测试通过(PASSED)
      F  测试失败(FAILED)
      E  测试出错(ERROR，如 import 失败)
      s  测试跳过(SKIPPED)
      x  预期失败(XFAIL)
      X  预期失败但通过了(XPASS)

    本文件中的 test_xxx 函数都可以用 pytest 运行验证。''')


def demo_assertion():
    """演示断言机制"""
    print("=" * 60)
    print("3. assert 断言机制")
    print("=" * 60)

    # 基本断言演示
    print("[基本断言]")
    x, y = 10, 20
    print(f"  assert {x} < {y}    →  {'PASS' if x < y else 'FAIL'}")
    print(f"  assert {x} + {y} == {x + y}  →  PASS")

    # 断言失败消息
    print("\n[断言失败消息]")
    print('  assert x > 0, f"期望 x > 0，但 x = {x}"')

    # 容器断言
    print("\n[容器断言]")
    items = [1, 2, 3]
    print(f"  assert len(items) == 3      →  {'PASS' if len(items) == 3 else 'FAIL'}")
    print(f"  assert 2 in items           →  {'PASS' if 2 in items else 'FAIL'}")
    d = {"a": 1, "b": 2}
    print(f'  assert d.get("a") == 1      →  {"PASS" if d.get("a") == 1 else "FAIL"}')

    # 浮点数近似
    print("\n[浮点数近似比较(pytest.approx)]")
    result = 0.1 + 0.2
    print(f"  0.1 + 0.2 = {result}")
    print(f"  直接比较: 0.1 + 0.2 == 0.3  →  {result == 0.3}  ← 精度问题!")
    print(f"  使用 approx: pytest.approx(0.3)  →  {abs(result - 0.3) < 1e-9}")


def demo_cli_options():
    """演示 pytest 命令行选项"""
    print("=" * 60)
    print("4. pytest 常用命令行选项")
    print("=" * 60)

    print('''
    [常用选项一览]
      -v, --verbose        详细输出(显示每个测试名称和结果)
      -q, --quiet          简洁输出
      -s                   显示 print() 输出(默认 pytest 会捕获 stdout)
      -k EXPRESSION        按关键字过滤测试(如 -k "test_assert")
      -x, --exitfirst      遇到第一个失败就停止
      --maxfail=N          遇到 N 个失败后停止
      --tb=MODE            控制 traceback 格式
                            auto / long / short / line / native / no
      --lf, --last-failed  只运行上次失败的测试
      --ff, --failed-first 先运行上次失败的测试(然后运行其余)
      -l, --showlocals     失败时显示局部变量值
      --durations=N        显示最慢的 N 个测试
      --collect-only       只收集测试(不运行)，检查有哪些测试
      --co                 与 --collect-only 相同(缩写)

    [示例]
      pytest -v -s                     # 详细输出 + 显示 print
      pytest -k "test_assert"          # 运行名称含 test_assert 的
      pytest -k "addition or string"   # 多条件匹配(and/or/not)
      pytest -x                        # 遇到第一个失败就停
      pytest --tb=short                # 简短 traceback
      pytest --lf                      # 只运行上次失败的
      pytest --collect-only            # 看看有哪些测试(不运行)''')


def demo_fixture_basics():
    """演示 fixture 基础"""
    print("=" * 60)
    print("5. @pytest.fixture 基础")
    print("=" * 60)

    print('''
    [什么是 fixture？]
    fixture 是测试的"准备工作"——为测试提供数据、连接、状态等。
    它比传统的 setUp/tearDown 更灵活。

    [定义 fixture]
      @pytest.fixture
      def sample_data():
          return {"name": "Alice", "age": 30}

    [使用 fixture]
      def test_user(sample_data):          # 直接作为参数名
          assert sample_data["name"] == "Alice"

    [setup / teardown 模式]
      @pytest.fixture
      def db_connection():
          # === setup ===
          conn = connect_to_db()
          yield conn                       # 将 conn 传给测试
          # === teardown ===
          conn.close()                     # 即使测试失败也执行

      yield 之前的代码 = setup(测试前执行)
      yield 之后的代码 = teardown(测试后执行，即使失败也执行)

    [pytest 内置 fixture]
      tmp_path       临时目录(pathlib.Path，自动创建和清理)
      tmpdir         临时目录(py.path.local，旧版)
      capsys         捕获 stdout/stderr
      monkeypatch    运行时修改对象/环境变量
      caplog         捕获日志输出
      recwarn        记录警告信息
      request        fixture 请求信息(获取参数名、作用域等)''')


def demo_fixture_scope():
    """演示 fixture 作用域"""
    print("=" * 60)
    print("6. fixture 作用域")
    print("=" * 60)

    print('''
    [四种作用域]
      scope="function"  (默认) 每个测试函数调用一次
      scope="class"            每个测试类调用一次
      scope="module"           每个测试模块(文件)调用一次
      scope="session"          整个 pytest 会话调用一次

    [示例]
      @pytest.fixture(scope="module")
      def expensive_setup():
          """昂贵的初始化(如加载大文件、建立数据库连接)"""
          data = load_large_file()
          yield data
          # 模块级清理

    [选择原则]
      function   测试相互独立，需要干净状态        → 最常用(默认)
      class      同一类中多个测试共享状态          → 较少用
      module     模块内测试共享只读资源             → 加载配置/模型
      session    全局共享资源                       → 数据库连接池

    [演示]
    本文件中有 func_scoped_fixture 和 module_scoped_fixture
    运行 pytest -v -s 可以看到两者的调用次数差异。''')


def demo_parametrize():
    """演示参数化测试"""
    print("=" * 60)
    print("7. @pytest.mark.parametrize 参数化测试")
    print("=" * 60)

    print('''
    [为什么需要参数化？]
    避免为每组测试数据写重复的测试函数，用一份逻辑覆盖多种输入。

    [基本语法]
      @pytest.mark.parametrize("参数1, 参数2", [
          (值A1, 值B1),
          (值A2, 值B2),
      ])
      def test_xxx(参数1, 参数2):
          ...

    [示例]
      @pytest.mark.parametrize("a, b, expected", [
          (1, 2, 3),
          (0, 0, 0),
          (-1, 1, 0),
      ])
      def test_add(a, b, expected):
          assert a + b == expected

    pytest 会为每组参数生成独立用例：
      test_add[1-2-3]      PASSED
      test_add[0-0-0]      PASSED
      test_add[-1-1-0]     PASSED

    [高级用法]
      - 使用 pytest.param(value, id="自定义名称") 自定义测试 ID
      - 堆叠多个 @pytest.mark.parametrize(生成笛卡尔积组合)
      - indirect=True 将参数传给同名的 fixture
      - 参数可以是任意 Python 对象(列表、字典、自定义类)''')


def demo_markers():
    """演示测试标记"""
    print("=" * 60)
    print("8. @pytest.mark 测试标记")
    print("=" * 60)

    print('''
    [内置标记]
      @pytest.mark.skip(reason="...")     永久跳过该测试
      @pytest.mark.skipif(cond, reason)   条件跳过
      @pytest.mark.xfail(reason="...")    预期失败(不计入测试失败)
      @pytest.mark.parametrize(...)       参数化

    [skip 示例]
      @pytest.mark.skip(reason="功能尚未实现")
      def test_future_feature():
          ...

      @pytest.mark.skipif(sys.version_info < (3, 10), reason="需要 Python 3.10+")
      def test_new_syntax():
          ...

    [xfail 结果解读]
      x  测试如预期失败 → XFAIL(不计入失败数)
      X  测试意外通过  → XPASS(提示可能需要移除 xfail)
      F  硬失败         → 标记 strict=True 时，意外通过视为失败

    [自定义标记]
      在 pyproject.toml 中注册：

      [tool.pytest.ini_options]
      markers = [
          "slow: 慢速测试",
          "integration: 集成测试(需要外部服务)",
          "smoke: 冒烟测试",
      ]

      使用时：
      @pytest.mark.slow
      def test_heavy_computation():
          ...

      运行时过滤：
      pytest -m "slow"           # 只运行 slow 标记
      pytest -m "not slow"       # 跳过 slow 标记
      pytest -m "slow or integration"  # 组合条件
      pytest --strict-markers    # 使用未注册标记时报错''')


def demo_raises():
    """演示异常测试"""
    print("=" * 60)
    print("9. pytest.raises 异常测试")
    print("=" * 60)

    print('''
    [基本用法]
      import pytest

      def test_zero_division():
          with pytest.raises(ZeroDivisionError):
              1 / 0

    [匹配异常消息]
      with pytest.raises(ValueError, match="invalid literal"):
          int("abc")

    [获取异常对象进行进一步断言]
      with pytest.raises(ValueError) as exc_info:
          int("abc")
      assert "invalid" in str(exc_info.value)
      assert exc_info.type is ValueError

    [验证自定义异常的属性]
      with pytest.raises(MyError) as exc_info:
          raise MyError(code=404, message="Not Found")
      assert exc_info.value.code == 404
      assert exc_info.value.message == "Not Found"

    [!] 重要：
    - pytest.raises 必须用 with 语句，确保异常在上下文内触发
    - 如果被测试代码没有抛出异常，pytest.raises 会让测试失败
    - match 参数使用正则表达式匹配异常消息''')


def main():
    """运行所有概念演示"""
    print("\n" + "╔" + "═" * 58 + "╗")
    print("║" + "  Python 测试 — pytest 基础与核心功能演示".center(52) + "║")
    print("╚" + "═" * 58 + "╝")
    print()
    print("[INFO]  这是概念演示模式(python 运行)，不执行测试函数。")
    print("[INFO]  运行测试请用: pytest 15-testing/01_pytest_basics.py -v")
    print()

    demo_installation()
    print()
    demo_first_test()
    print()
    demo_assertion()
    print()
    demo_cli_options()
    print()
    demo_fixture_basics()
    print()
    demo_fixture_scope()
    print()
    demo_parametrize()
    print()
    demo_markers()
    print()
    demo_raises()

    print("\n" + "=" * 60)
    print("概念演示完成！")
    print("=" * 60)
    print()
    print("运行测试：")
    print("  pytest 15-testing/01_pytest_basics.py -v")
    print("  pytest 15-testing/01_pytest_basics.py -v -s    (显示 print 输出)")
    print("  pytest 15-testing/01_pytest_basics.py -k parametrize   (按关键字过滤)")
    print()
    print("继续学习 → 15-testing/02_pytest_advanced.py")
    print()


if __name__ == "__main__":
    main()
