# Py Cookbook

Python 学习教程项目，参照菜鸟教程 Python3 知识体系，每个知识点一个可执行 demo 文件。

## 目录结构

```
py-cookbook/
├── 01-basics/              # 基础语法
│   ├── 01_hello_world.py       # 第一个程序
│   ├── 02_syntax.py            # 基础语法(缩进/多行/代码组)
│   ├── 03_comments.py          # 注释(单行/多行/docstring)
│   ├── 04_operators.py         # 运算符(算术/比较/赋值/逻辑/位/成员/身份)
│   ├── 05_type_conversion.py   # 数据类型转换
│   ├── 06_number.py            # 数字类型(int/float/complex/math)
│   └── 07_string.py            # 字符串(索引/切片/方法/编码)
│
├── 02-datatypes/           # 数据类型
│   ├── 01_list.py              # 列表(CRUD/排序/拷贝/嵌套)
│   ├── 02_tuple.py             # 元组(不可变/解包/命名元组)
│   ├── 03_dict.py              # 字典(创建/方法/推导式/遍历)
│   ├── 04_set.py               # 集合(交并差/frozenset/去重)
│   ├── 05_data_structure.py    # 数据结构(栈/队列/堆/对比)
│   ├── 06_bytes.py             # bytes与bytearray(编码/解码)
│   └── 07_none.py              # NoneType与bool(truthy/falsy)
│
├── 03-control-flow/        # 流程控制
│   ├── 01_conditional.py       # 条件控制(if/elif/else/三元)
│   ├── 02_for_loop.py          # for循环(range/enumerate/zip/else)
│   ├── 03_while_loop.py        # while循环(死循环/while-else)
│   └── 04_comprehensions.py      # 推导式(列表/字典/集合/生成器)
│
├── 04-functions/           # 函数
│   ├── 01_function.py          # 函数(参数/返回值/作用域/闭包)
│   ├── 02_lambda.py            # 匿名函数(map/filter/sorted)
│   ├── 03_decorator.py         # 装饰器(wraps/带参/类装饰器)
│   ├── 04_iterator_generator.py # 迭代器与生成器(yield/send)
│   └── 05_namespace_scope.py     # 命名空间与作用域(LEGB/global)
│
├── 05-oop/                # 面向对象
│   ├── 01_class.py             # 类与对象(init/classmethod/staticmethod)
│   ├── 02_inheritance.py       # 继承与多态(super/ABC/Mixin/MRO)
│   └── 03_magic_methods.py     # 魔术方法与类型注解(typing)
│
├── 06-modules/             # 模块与包
│   ├── 01_module.py            # 模块(import/sys.path/包/__all__)
│   ├── 02_name_main.py         # __name__与__main__
│   └── 03_pip_package.py       # pip与包管理(安装/依赖/venv/镜像源)
│
├── 07-io/                 # 输入输出与文件
│   ├── 01_input_output.py      # 输入输出(print/f-string/format)
│   ├── 02_file.py              # 文件操作(read/write/seek/二进制)
│   ├── 03_os_module.py         # OS模块(os.path/shutil/walk)
│   └── 04_with_statement.py    # with语句(上下文管理器)
│
├── 08-errors/              # 错误与异常
│   ├── 01_try_except.py         # try/except基础(捕获/else/finally/常见异常/assert)
│   ├── 02_custom_exceptions.py  # 自定义异常(ValidationError/BusinessError)
│   ├── 03_exception_chaining.py # 异常链(raise from/from None/__cause__)
│   └── 04_warnings.py           # warnings警告机制(类别/过滤/自定义)
│
├── 09-stdlib/              # 标准库
│   ├── 01_math.py              # math(常量/取整/三角函数)
│   ├── 02_random.py            # random(随机数/种子/密码生成)
│   ├── 03_datetime.py          # datetime(日期/时间差/格式化)
│   ├── 04_re.py                # re(正则表达式/分组/常用模式)
│   ├── 05_json.py              # json(序列化/中文/自定义编码)
│   ├── 06_csv.py               # csv(读写/DictReader/DictWriter)
│   ├── 07_sys.py               # sys(argv/path/platform)
│   ├── 08_os_path.py           # os.path(路径操作/pathlib)
│   ├── 09_operator.py          # operator(itemgetter/attrgetter)
│   ├── 10_statistics.py        # statistics(均值/方差/分位数)
│   ├── 11_hashlib.py           # hashlib(md5/sha256/HMAC/PBKDF2)
│   ├── 12_pickle.py            # pickle(序列化/协议版本)
│   ├── 13_stringio.py          # StringIO与BytesIO(内存缓冲)
│   ├── 14_logging.py           # logging(配置/Handler/格式化)
│   ├── 15_subprocess.py        # subprocess(run/Popen/管道)
│   ├── 16_queue.py              # queue(生产者-消费者/优先级)
│   ├── 17_itertools.py          # itertools(无限迭代/累积/组合排列/实用组合)
│   ├── 18_collections.py        # collections(namedtuple/defaultdict/Counter/deque/ChainMap)
│   └── 19_functools.py          # functools(partial/reduce/lru_cache/total_ordering/singledispatch)
│
├── 10-advanced/            # 高级特性
│   ├── 01_threading.py         # 多线程(Thread/Lock/Event/线程池/GIL)
│   ├── 02_asyncio.py           # 异步编程(async/await/gather)
│   ├── 03_xml.py               # XML解析(ElementTree)
│   ├── 04_socket.py             # 网络编程(TCP/UDP/echo服务)
│   └── 05_multiprocessing.py    # 多进程(Process/Queue/共享内存/进程池/对比threading)
│
├── 11-builtin/             # 内置函数
│   ├── 01_type_functions.py    # 类型与对象(30+函数: type/isinstance/repr/id/dir等)
│   ├── 02_math_iteration.py    # 数学与迭代(20+函数: abs/round/sum/map/filter等)
│   └── 03_object_io.py         # 输入输出与执行(open/eval/exec/globals等)
│
├── 12-pattern-matching/    # 模式匹配 (Python 3.10+)
│   └── 01_match_case.py        # match/case(字面量/序列/映射/类/OR/守卫/嵌套/as模式)
│
├── 13-dataclass_enum/      # 数据类与枚举
│   ├── 01_dataclass.py         # dataclass(字段/frozen/post_init/继承)
│   └── 02_enum.py              # enum(Enum/IntEnum/StrEnum/Flag/auto/unique)
│
├── 14-typing/              # 类型注解
│   ├── 01_type_annotations.py  # 类型注解基础(Optional/Union/Literal/Callable/Final)
│   └── 02_advanced_typing.py   # 高级类型(TypeVar/Generic/Protocol/ParamSpec/TypeGuard)
│
├── 15-testing/             # 测试
│   ├── 01_pytest_basics.py     # pytest基础(assert/fixture/参数化/标记)
│   └── 02_pytest_advanced.py   # pytest高级(fixture组合/mock/覆盖率/配置)
│
├── run_all.py              # 批量运行所有 demo 的验证脚本
├── .gitignore
└ README.md
```

## 环境

- Python 3.10+
- 开发工具: ruff (代码检查/格式化)、pytest (测试框架)

## 快速开始

```bash
# 运行任意示例
python 01-basics/01_hello_world.py

# 批量运行所有示例并验证完整性
python run_all.py

# 运行 pytest 测试
pytest 15-testing/ -v
```

## 知识体系概览

| 分类 | 文件数 | 核心知识点 |
|------|--------|-----------|
| 01-basics 基础语法 | 7 | 语法规则、运算符、类型转换、数字、字符串 |
| 02-datatypes 数据类型 | 7 | 列表、元组、字典、集合、bytes、数据结构 |
| 03-control-flow 流程控制 | 4 | 条件、for、while、推导式 |
| 04-functions 函数 | 5 | 函数参数、lambda、装饰器、生成器、作用域 |
| 05-oop 面向对象 | 3 | 类、继承多态、魔术方法、类型注解 |
| 06-modules 模块与包 | 3 | import机制、__name__、pip包管理 |
| 07-io 输入输出 | 4 | print格式化、文件读写、OS模块、with语句 |
| 08-errors 异常与警告 | 4 | try/except、自定义异常、异常链、warnings |
| 09-stdlib 标准库 | 19 | math/random/datetime/re/json/csv/sys/hashlib/pickle/logging/itertools/collections/functools等 |
| 10-advanced 高级 | 5 | 多线程、异步、XML、网络编程、多进程 |
| 11-builtin 内置函数 | 3 | 类型/对象、数学/迭代、IO/执行 |
| 12-pattern-matching 模式匹配 | 1 | match/case字面量/序列/映射/类/OR/守卫/嵌套 |
| 13-dataclass_enum 数据类与枚举 | 2 | dataclass字段/frozen/post_init、Enum/IntEnum/StrEnum |
| 14-typing 类型注解 | 2 | Optional/Union/Literal、TypeVar/Generic/Protocol |
| 15-testing 测试 | 2 | pytest基础/fixture/参数化、mock/覆盖率/配置 |

**共计 65+ 个 demo 文件，覆盖 Python 3.10+ 核心知识体系。**

## 代码风格

- 使用 `ruff` 进行代码检查和格式化
- 每个文件遵循统一模式: docstring → demo 函数 → `if __name__ == "__main__": main()`
- 中文注释 + 英文变量名
- 所有 demo 均为可独立运行的纯标准库示例

```bash
# 代码检查
ruff check .

# 代码格式化
ruff format .
```

## 贡献指南

1. Fork & Clone 本仓库
2. 新增 demo 文件时遵循现有命名规范: `序号_主题.py`
3. 每个文件必须有模块级 docstring（含学习目标）
4. 使用 `if __name__ == "__main__": main()` 作为入口
5. 运行 `python run_all.py` 验证所有文件无报错
6. 提交前执行 `ruff check .` 确保代码风格一致

## License

MIT