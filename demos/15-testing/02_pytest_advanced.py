"""
Python 测试 - pytest 高级功能

学习目标：
  - fixture 依赖与组合
  - fixture 返回值与 yield teardown
  - conftest.py 共享 fixture 机制
  - tmp_path 临时目录与文件测试
  - mock/monkeypatch 概念与实践
  - 测试覆盖率(pytest-cov)
  - 测试组织与发现规则
  - pytest 配置(pyproject.toml / pytest.ini)
  - 实际项目中的测试最佳实践

运行方式：
  python 15-testing/02_pytest_advanced.py    # 运行概念演示
  pytest 15-testing/02_pytest_advanced.py -v  # 运行测试
"""

import json
import os

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
            parametrize = staticmethod(lambda *a, **kw: lambda f: f)

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

# --- 1. Fixture 依赖与组合 ---

@pytest.fixture
def raw_scores():
    """基础 fixture：提供原始分数列表"""
    return [85, 92, 78, 95, 88]


@pytest.fixture
def sorted_scores(raw_scores):
    """依赖 raw_scores 的 fixture：返回排序后的分数"""
    return sorted(raw_scores)


@pytest.fixture
def score_stats(raw_scores):
    """依赖 raw_scores 的 fixture：返回统计信息"""
    return {
        "sum": sum(raw_scores),
        "min": min(raw_scores),
        "max": max(raw_scores),
        "count": len(raw_scores),
        "avg": sum(raw_scores) / len(raw_scores),
    }


def test_fixture_dependency(sorted_scores):
    """测试使用依赖链的 fixture"""
    assert sorted_scores == [78, 85, 88, 92, 95]
    assert sorted_scores[0] == min(sorted_scores)
    assert sorted_scores[-1] == max(sorted_scores)


def test_multiple_fixtures(sorted_scores, score_stats):
    """测试使用多个 fixture(它们共依赖 raw_scores，pytest 只创建 raw_scores 一次)"""
    assert score_stats["sum"] == sum(sorted_scores)
    assert score_stats["min"] == sorted_scores[0]
    assert score_stats["max"] == sorted_scores[-1]
    assert score_stats["count"] == len(sorted_scores)


# --- 2. Fixture 返回值与 yield ---

class DatabaseSimulator:
    """模拟数据库连接，演示 setup/teardown 模式"""

    def __init__(self):
        self.connected = False
        self.data = {}

    def connect(self):
        self.connected = True

    def close(self):
        self.connected = False
        self.data.clear()


@pytest.fixture
def db_connection():
    """fixture 使用 yield 实现 setup / teardown"""
    # === setup ===
    db = DatabaseSimulator()
    db.connect()
    db.data["initialized"] = True

    yield db  # 将 db 传给测试函数

    # === teardown ===
    db.close()


def test_db_connection_available(db_connection):
    """验证 fixture 提供了已连接的数据库"""
    assert db_connection.connected is True
    assert db_connection.data["initialized"] is True


def test_db_connection_writable(db_connection):
    """验证可以在 fixture 提供的数据库上写入数据"""
    db_connection.data["user"] = "Alice"
    assert db_connection.data["user"] == "Alice"
    assert "user" in db_connection.data


# --- 3. tmp_path fixture(临时目录与文件)---

def test_tmp_path_create_file(tmp_path):
    """使用 tmp_path 创建临时文本文件"""
    # tmp_path 是 pathlib.Path 对象
    file_path = tmp_path / "test_data.txt"
    file_path.write_text("Hello, pytest!", encoding="utf-8")

    assert file_path.exists()
    assert file_path.read_text() == "Hello, pytest!"


def test_tmp_path_write_json(tmp_path):
    """在临时目录中读写 JSON 文件"""
    data = {"name": "Alice", "scores": [90, 85, 92]}
    file_path = tmp_path / "data.json"
    file_path.write_text(json.dumps(data), encoding="utf-8")

    loaded = json.loads(file_path.read_text())
    assert loaded["name"] == "Alice"
    assert loaded["scores"] == [90, 85, 92]


def test_tmp_path_create_subdirectory(tmp_path):
    """在临时目录中创建嵌套子目录"""
    sub_dir = tmp_path / "sub" / "deep"
    sub_dir.mkdir(parents=True)

    nested_file = sub_dir / "nested.txt"
    nested_file.write_text("nested content")

    assert nested_file.exists()
    assert nested_file.read_text() == "nested content"


# --- 4. monkeypatch fixture ---

def get_app_mode():
    """模拟从环境变量读取配置的函数"""
    return os.environ.get("APP_MODE", "production")


def test_monkeypatch_setenv(monkeypatch):
    """使用 monkeypatch 设置环境变量"""
    monkeypatch.setenv("APP_MODE", "testing")
    assert get_app_mode() == "testing"

    # 删除环境变量后，回退到默认值
    monkeypatch.delenv("APP_MODE", raising=False)
    assert get_app_mode() == "production"


class Calculator:
    """被测试的简单计算器"""

    def add(self, a, b):
        return a + b


def test_monkeypatch_method(monkeypatch):
    """使用 monkeypatch 替换对象方法"""

    def always_return_100(self, a, b):
        return 100

    calc = Calculator()
    assert calc.add(2, 3) == 5  # 原始行为

    # 替换 Calculator.add 方法
    monkeypatch.setattr(Calculator, "add", always_return_100)
    assert calc.add(2, 3) == 100  # 被替换后的行为


def test_monkeypatch_attribute(monkeypatch):
    """使用 monkeypatch 动态设置对象属性"""
    calc = Calculator()
    monkeypatch.setattr(calc, "version", "2.0.0", raising=False)
    assert calc.version == "2.0.0"  # type: ignore[attr-defined]


def test_monkeypatch_dict(monkeypatch):
    """使用 monkeypatch 修改字典中的值"""
    config = {"host": "localhost", "port": 5432}
    monkeypatch.setitem(config, "port", 9999)
    assert config["port"] == 9999
    assert config["host"] == "localhost"  # 其他键不受影响


# --- 5. capsys fixture(捕获 stdout/stderr)---

def greet(name):
    """简单的问候函数"""
    print(f"Hello, {name}!")
    return f"Hello, {name}!"


def test_capsys_stdout(capsys):
    """使用 capsys 捕获 stdout 输出"""
    result = greet("Alice")
    captured = capsys.readouterr()

    assert result == "Hello, Alice!"
    assert "Hello, Alice!" in captured.out
    assert captured.err == ""  # 没有 stderr 输出


def test_capsys_multiple_prints(capsys):
    """capsys 可捕获多次 print 的输出"""
    print("line 1")
    print("line 2")
    captured = capsys.readouterr()

    assert "line 1" in captured.out
    assert "line 2" in captured.out


# --- 6. 堆叠 parametrize(笛卡尔积)---

@pytest.mark.parametrize("operation", ["upper", "lower", "title"])
@pytest.mark.parametrize("text, expected_base", [
    ("hello world", "hello world"),
])
def test_stacked_parametrize(operation, text, expected_base):
    """堆叠 parametrize 生成 3×1=3 个测试用例(笛卡尔积)"""
    result = getattr(text, operation)()
    expected = getattr(expected_base, operation)()
    assert result == expected


# ============================================================
# Demo 演示函数区域(由 python 直接运行)
# ============================================================

def demo_fixture_dependency():
    """演示 fixture 依赖与组合"""
    print("=" * 60)
    print("1. fixture 依赖与组合")
    print("=" * 60)

    print('''
    [fixture 之间可以互相依赖]

      @pytest.fixture
      def raw_data():
          return [5, 2, 8, 1, 9, 3]

      @pytest.fixture
      def sorted_data(raw_data):      # 依赖 raw_data
          return sorted(raw_data)

      @pytest.fixture
      def data_stats(raw_data):       # 也依赖 raw_data
          return {"sum": sum(raw_data), "min": min(raw_data)}

      def test_example(sorted_data, data_stats):
          # 两个 fixture 都依赖 raw_data
          # pytest 智能处理：raw_data 只创建一次！
          assert data_stats["min"] == sorted_data[0]

    [依赖链规则]
      - fixture A 依赖 B → B 在 A 之前执行
      - 多个 fixture 依赖同一个 → 该 fixture 只创建一次(缓存)
      - pytest 自动解析依赖图，确定执行顺序
      - 循环依赖会报错(A → B → A)

    [典型使用场景]
      - 数据库连接 → 测试数据准备 → 测试执行
      - 配置文件加载 → API 客户端初始化 → 测试执行
      - 用户创建 → 登录 token → 带认证的请求测试''')


def demo_fixture_yield():
    """演示 fixture 返回值与 yield"""
    print("=" * 60)
    print("2. fixture 返回值与 yield teardown")
    print("=" * 60)

    print('''
    [return vs yield 对比]

      # 方式1: return — 没有清理逻辑
      @pytest.fixture
      def simple_data():
          return {"key": "value"}

      # 方式2: yield — 有清理逻辑
      @pytest.fixture
      def managed_resource():
          resource = acquire()   # ← setup
          yield resource         # ← 传给测试
          release(resource)      # ← teardown(即使测试失败也执行)

    [yield 的执行顺序]
      1. yield 之前的代码  →  setup(测试前执行)
      2. 测试函数体
      3. yield 之后的代码  →  teardown(测试后执行，失败也会执行)

    [多个 fixture 嵌套时的 teardown 顺序]
      @pytest.fixture
      def outer(inner):
          print("outer setup")
          yield "outer"
          print("outer teardown")

      @pytest.fixture
      def inner():
          print("inner setup")
          yield "inner"
          print("inner teardown")

      def test_something(outer):
          print("  test body")

      输出顺序(栈式，后进先出)：
        inner setup
        outer setup
          test body
        outer teardown
        inner teardown

    [!] 注意事项
      - yield 之后不能再有 return
      - 如果想在 teardown 后返回 cleanup 结果，用 addfinalizer
      - teardown 中的异常会使测试标记为 ERROR''')


def demo_conftest():
    """演示 conftest.py 概念"""
    print("=" * 60)
    print("3. conftest.py 共享 fixture")
    print("=" * 60)

    print('''
    [conftest.py 是什么？]
    conftest.py 是 pytest 的特殊配置文件，用于:
      - 共享 fixture(无需 import，自动发现)
      - 注册自定义 hook
      - 加载插件

    [作用范围]
      项目根目录/                    ← 影响所有子目录
      ├── conftest.py
      ├── tests/
      │   ├── conftest.py             ← 只影响 tests/ 及其子目录
      │   ├── unit/
      │   │   └── conftest.py         ← 只影响 unit/ 目录
      │   └── integration/
      └── src/

    [conftest.py 示例]
      # tests/conftest.py
      import pytest

      @pytest.fixture(scope="session")
      def db_connection():
          """全局数据库连接，所有测试共享"""
          conn = create_connection()
          yield conn
          conn.close()

      @pytest.fixture
      def sample_user(db_connection):
          """创建测试用户(依赖 db_connection)"""
          user = db_connection.create_user(name="test_user")
          yield user
          db_connection.delete_user(user.id)

      def pytest_configure(config):
          """注册自定义标记"""
          config.addinivalue_line("markers", "slow: 慢速测试")

    [最佳实践]
      - conftest.py 中的 fixture 自动可用(不需要 import)
      - 子目录的 conftest.py 会覆盖父目录的同名 fixture
      - 不要把业务逻辑放在 conftest.py 中
      - 仅放 fixture、hook 和插件配置
      - 一个 conftest.py 不应太大，可拆成多个模块再 import''')


def demo_tmp_path():
    """演示临时目录与文件"""
    print("=" * 60)
    print("4. tmp_path 临时目录与文件")
    print("=" * 60)

    print('''
    [tmp_path fixture]
    pytest 内置 fixture，提供 pathlib.Path 类型的临时目录。
    测试结束后自动删除，无需手动清理。

    [基本用法]
      def test_write_file(tmp_path):
          file = tmp_path / "data.txt"
          file.write_text("hello", encoding="utf-8")
          assert file.read_text() == "hello"

      def test_create_dir(tmp_path):
          sub = tmp_path / "subdir"
          sub.mkdir()
          (sub / "nested.txt").write_text("data")

    [tmp_path vs tmpdir]
      tmp_path   →  pathlib.Path 对象(推荐，Python 3.6+)
      tmpdir     →  py.path.local 对象(旧版，兼容老项目)

    [实际应用场景]
      - 文件处理函数测试(读/写/解析)
      - JSON / CSV / XML 文件读写测试
      - 需要创建临时配置文件的测试
      - 测试生成文件的函数

    [tmp_path_factory(session 级)]
      def test_something(tmp_path_factory):
          # factory 不是目录，需要显式创建
          base = tmp_path_factory.mktemp("my_temp")
          file = base / "data.txt"
          file.write_text("shared data")''')


def demo_mock_monkeypatch():
    """演示 mock 与 monkeypatch 概念"""
    print("=" * 60)
    print("5. mock 与 monkeypatch 概念")
    print("=" * 60)

    print('''
    [为什么要 mock / monkeypatch？]
    测试应该只关注当前代码逻辑，不依赖外部系统。
    mock 替换外部依赖，让测试快速、可靠、可重复。

    [pytest 内置 monkeypatch]
      无需额外安装，可直接使用：

      monkeypatch.setenv("VAR", "value")    # 设置环境变量
      monkeypatch.delenv("VAR")             # 删除环境变量
      monkeypatch.setattr(obj, "attr", val) # 设置属性
      monkeypatch.delattr(obj, "attr")      # 删除属性
      monkeypatch.setitem(d, "key", "val")  # 设置字典项
      monkeypatch.delitem(d, "key")         # 删除字典项
      monkeypatch.syspath_prepend(path)     # 添加 sys.path

    [unittest.mock 集成(更强大的 mock)]
      from unittest.mock import Mock, patch, MagicMock

      # 创建 Mock 对象
      mock_service = Mock()
      mock_service.get_data.return_value = {"result": "ok"}
      mock_service.get_data.side_effect = TimeoutError

      # 使用 patch 上下文管理器
      with patch("mymodule.external_api.call") as mock_call:
          mock_call.return_value = "mocked response"
          result = my_function()
          mock_call.assert_called_once_with(expected_arg)

    [mock 设计原则]
      - 只 mock 你自己的接口，不 mock 标准库类型
      - mock 返回合理的数据，不要过度简化
      - 验证 mock 被正确调用(assert_called_with 等)
      - 优先用依赖注入设计，减少 mock 使用
      - monkeypatch 适合简单替换，unittest.mock 适合复杂 mock''')


def demo_coverage():
    """演示测试覆盖率概念"""
    print("=" * 60)
    print("6. 测试覆盖率(pytest-cov)")
    print("=" * 60)

    print('''
    [什么是覆盖率？]
    测试覆盖率衡量测试代码执行了多少行/分支/路径。

    [安装 pytest-cov]
      pip install pytest-cov

    [运行覆盖率测试]
      pytest --cov=my_package tests/
      pytest --cov=my_package --cov-report=html tests/
      pytest --cov=my_package --cov-report=term-missing tests/

    [覆盖率报告解读]
      Name           Stmts   Miss  Cover   Missing
      ---------------------------------------------
      module_a.py       50      5    90%   12-15, 42
      module_b.py       30      3    90%   8, 21, 29
      ---------------------------------------------
      TOTAL             80      8    90%

      Stmts   = 可执行语句数(statements)
      Miss    = 未覆盖的语句数
      Cover   = 覆盖率百分比
      Missing = 未覆盖的具体行号

    [覆盖率类型]
      行覆盖    哪些代码行被执行了
      分支覆盖   if/else 等分支是否都覆盖(--cov-branch)
      路径覆盖   所有可能的执行路径

    [常见选项]
      --cov=PKG           指定覆盖哪个包
      --cov-report=html   生成 HTML 报告(可视化)
      --cov-report=xml    生成 XML 报告(CI 集成)
      --cov-report=term   终端输出报告
      --cov-fail-under=80 覆盖率低于 80% 则失败
      --cov-branch        启用分支覆盖率

    [覆盖率不是全部]
      [+] 高覆盖率 ≠ 好测试
      [-] 100% 覆盖率不一定需要(可能是不必要的追求)
      [+] 重点关注核心业务逻辑的覆盖
      [-] 不要为了覆盖率写无意义的测试''')


def demo_test_organization():
    """演示测试组织与发现"""
    print("=" * 60)
    print("7. 测试组织与发现")
    print("=" * 60)

    print('''
    [推荐目录结构]

      my_project/
      ├── src/
      │   └── my_package/
      │       ├── __init__.py
      │       ├── calculator.py
      │       └── utils.py
      ├── tests/
      │   ├── __init__.py             # 可以为空
      │   ├── conftest.py             # 共享 fixture
      │   ├── unit/                   # 单元测试
      │   │   ├── __init__.py
      │   │   ├── test_calculator.py
      │   │   └── test_utils.py
      │   └── integration/            # 集成测试
      │       ├── __init__.py
      │       └── test_api.py
      ├── pyproject.toml              # pytest 配置
      └── README.md

    [pytest 默认发现规则]
      1. 从当前目录开始递归搜索
      2. 匹配文件: test_*.py 或 *_test.py
      3. 文件中匹配:
         - 函数: 以 test_ 开头
         - 类:   以 Test 开头(不含 __init__ 方法)
         - 方法: 以 test_ 开头

    [自定义发现规则(pyproject.toml)]
      [tool.pytest.ini_options]
      testpaths = ["tests"]
      python_files = ["test_*.py", "*_test.py"]
      python_classes = ["Test*"]
      python_functions = ["test_*"]

    [命名约定建议]
      文件:   test_<模块名>.py           → test_calculator.py
      类:     Test<功能描述>              → TestCalculator
      函数:   test_<场景>_<预期结果>      → test_add_positive_numbers
      函数:   test_<场景>_raises_<异常>  → test_divide_by_zero_raises_error''')


def demo_configuration():
    """演示 pytest 配置"""
    print("=" * 60)
    print("8. pytest 配置")
    print("=" * 60)

    print('''
    [配置方式(优先级从高到低)]
      1. 命令行参数               pytest -v --tb=short
      2. pyproject.toml           [tool.pytest.ini_options]
      3. pytest.ini               [pytest]
      4. tox.ini                  [pytest]
      5. setup.cfg                [tool:pytest]

    [pyproject.toml 配置示例]
      [tool.pytest.ini_options]
      addopts = "-v --tb=short --strict-markers"
      testpaths = ["tests"]
      minversion = "7.0"
      markers = [
          "slow: 慢速测试",
          "integration: 集成测试",
          "unit: 单元测试",
      ]
      filterwarnings = [
          "error",
          "ignore::DeprecationWarning",
      ]

    [pytest.ini 配置示例]
      [pytest]
      addopts = -v --tb=short
      testpaths = tests
      python_files = test_*.py
      python_classes = Test*
      python_functions = test_*
      markers =
          slow: 慢速测试
          integration: 集成测试(需要外部服务)

    [常用 addopts 配置]
      -v                     始终详细输出
      --tb=short             简短 traceback
      --strict-markers       未注册标记时报错(防止拼写错误)
      --strict-config        配置错误时报错
      -p no:cacheprovider    禁用缓存(CI 环境常用)

    本项目可在 pyproject.toml 中按需添加 [tool.pytest.ini_options]。''')


def demo_best_practices():
    """演示测试最佳实践"""
    print("=" * 60)
    print("9. 实际项目中的测试最佳实践")
    print("=" * 60)

    practices = {
        "测试金字塔": [
            "单元测试(Unit)        多而快，测试单个函数/方法",
            "集成测试(Integration)   中等数量，测试模块间交互",
            "端到端测试(E2E)         少而慢，测试完整用户流程",
        ],
        "FIRST 原则": [
            "Fast        测试必须快(秒级，不是分钟级)",
            "Independent   测试之间完全独立，不依赖执行顺序",
            "Repeatable    在任何环境都能重复运行",
            "Self-Validating  自动判断通过/失败，无需人工检查",
            "Timely       及时编写(TDD：先写测试再写代码)",
        ],
        "编写可测试的代码": [
            "依赖注入(将依赖作为参数传入，而非内部创建)",
            "函数小而专一(单一职责原则)",
            "避免全局状态(用参数传递代替全局变量)",
            "接口隔离(为测试提供 mock 接口)",
            "纯函数更易测试(相同输入 → 相同输出，无副作用)",
        ],
        "测试命名规范": [
            "test_<被测功能>_<场景>_<预期结果>",
            "例: test_divide_by_zero_raises_error",
            "例: test_get_user_with_valid_id_returns_user",
        ],
        "AAA 测试结构": [
            "Arrange   准备：设置测试数据和初始状态",
            "Act       执行：调用被测试的代码",
            "Assert    断言：验证结果是否符合预期",
            "示例:",
            "  # Arrange",
            "  user = User(name='Alice', age=30)",
            "  # Act",
            "  result = user.greet()",
            "  # Assert",
            "  assert result == 'Hello, Alice!'",
        ],
        "常用 pytest 插件": [
            "pytest-cov         覆盖率",
            "pytest-xdist       并行执行(-n auto)",
            "pytest-mock        增强 mock 支持",
            "pytest-timeout     测试超时控制",
            "pytest-randomly    随机执行顺序(发现顺序依赖)",
            "pytest-sugar       美化输出",
            "pytest-html        HTML 报告",
            "pytest-benchmark   性能基准测试",
            "pytest-asyncio     异步测试",
            "pytest-env         设置测试环境变量",
        ],
        "CI/CD 集成": [
            "pytest --junitxml=report.xml     生成 JUnit 格式报告",
            "pytest --cov --cov-report=xml     生成覆盖率 XML",
            "在 GitHub Actions / GitLab CI / Jenkins 中运行",
            "设置覆盖率阈值: --cov-fail-under=80",
            "失败时保存测试报告供排查",
        ],
        "常见陷阱": [
            "测试之间共享可变状态(导致顺序依赖)",
            "过度 mock(测试只验证了 mock 行为)",
            "测试太慢(网络请求、文件 I/O 过多)",
            "覆盖率 100% 的执着(关注质量而非数字)",
            "测试代码质量差(测试也需要维护)",
            "没有测试失败信息(不知道哪里出问题)",
        ],
    }

    for title, items in practices.items():
        print(f"\n  [{title}]")
        for item in items:
            print(f"    - {item}")


def main():
    """运行所有概念演示"""
    print("\n" + "╔" + "═" * 58 + "╗")
    print("║" + "  Python 测试 — pytest 高级功能演示".center(52) + "║")
    print("╚" + "═" * 58 + "╝")
    print()
    print("[INFO]  这是概念演示模式(python 运行)，不执行测试函数。")
    print("[INFO]  运行测试请用: pytest 15-testing/02_pytest_advanced.py -v")
    print()

    demo_fixture_dependency()
    print()
    demo_fixture_yield()
    print()
    demo_conftest()
    print()
    demo_tmp_path()
    print()
    demo_mock_monkeypatch()
    print()
    demo_coverage()
    print()
    demo_test_organization()
    print()
    demo_configuration()
    print()
    demo_best_practices()

    print("\n" + "=" * 60)
    print("概念演示完成！")
    print("=" * 60)
    print()
    print("运行测试：")
    print("  pytest 15-testing/02_pytest_advanced.py -v")
    print("  pytest 15-testing/ -v                        (运行所有测试)")
    print("  pytest 15-testing/ -v --tb=short              (简短 traceback)")
    print("  pytest 15-testing/ -v -k monkeypatch          (按关键字过滤)")
    print()
    print("相关文件：")
    print("  ← 01_pytest_basics.py     pytest 基础与核心功能")
    print()


if __name__ == "__main__":
    main()
