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
│   └ 07_string.py              # 字符串(索引/切片/方法/编码)
│
├── 02-datatypes/           # 数据类型
│   ├── 01_list.py              # 列表(CRUD/排序/拷贝/嵌套)
│   ├── 02_tuple.py             # 元组(不可变/解包/命名元组)
│   ├── 03_dict.py              # 字典(创建/方法/推导式/遍历)
│   ├── 04_set.py               # 集合(交并差/frozenset/去重)
│   ├── 05_data_structure.py    # 数据结构(栈/队列/堆/对比)
│   ├── 06_bytes.py             # bytes与bytearray(编码/解码)
│   └ 07_none.py                # NoneType与bool(truthy/falsy)
│
├── 03-control-flow/        # 流程控制
│   ├── 01_conditional.py       # 条件控制(if/elif/else/三元)
│   ├── 02_for_loop.py          # for循环(range/enumerate/zip/else)
│   ├── 03_while_loop.py        # while循环(死循环/while-else)
│   └ 04_comprehensions.py      # 推导式(列表/字典/集合/生成器)
│
├── 04-functions/           # 函数
│   ├── 01_function.py          # 函数(参数/返回值/作用域/闭包)
│   ├── 02_lambda.py            # 匿名函数(map/filter/sorted)
│   ├── 03_decorator.py         # 装饰器(wraps/带参/类装饰器)
│   ├── 04_iterator_generator.py # 迭代器与生成器(yield/send)
│   └ 05_namespace_scope.py     # 命名空间与作用域(LEGB/global)
│
├── 05-oop/                # 面向对象
│   ├── 01_class.py             # 类与对象(init/classmethod/staticmethod)
│   ├── 02_inheritance.py       # 继承与多态(super/ABC/Mixin/MRO)
│    └ 03_magic_methods.py     # 魔术方法与类型注解(typing)
│
├── 06-modules/             # 模块与包
│   ├── 01_module.py            # 模块(import/sys.path/包/__all__)
│    └ 02_name_main.py         # __name__与__main__
│
├── 07-io/                 # 输入输出与文件
│   ├── 01_input_output.py      # 输入输出(print/f-string/format)
│   ├── 02_file.py              # 文件操作(read/write/seek/二进制)
│   ├── 03_os_module.py         # OS模块(os.path/shutil/walk)
│    └ 04_with_statement.py    # with语句(上下文管理器)
│
├── 08-errors/              # 错误与异常
│   ├── 01_try_except.py         # try/except基础(捕获/else/finally/常见异常/assert)
│   ├── 02_custom_exceptions.py  # 自定义异常(ValidationError/BusinessError)
│   └ 03_exception_chaining.py   # 异常链(raise from/from None/__cause__)
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
│   └ 05_multiprocessing.py    # 多进程(Process/Queue/共享内存/进程池/对比threading)
│
├── 11-builtin/             # 内置函数
│   ├── 01_type_functions.py    # 类型与对象(30+函数: type/isinstance/repr/id/dir等)
│   ├── 02_math_iteration.py    # 数学与迭代(20+函数: abs/round/sum/map/filter等)
│    └ 03_object_io.py         # 输入输出与执行(open/eval/exec/globals等)
├── .gitignore
└ README.md
```

## 环境

- Python 3.10+

## 使用

```bash
# 运行任意示例
python 01-basics/01_hello_world.py

# 批量运行某个分类下所有示例
python 01-basics/01_hello_world.py && python 01-basics/02_syntax.py
```

## 知识体系概览

| 分类 | 文件数 | 核心知识点 |
|------|--------|-----------|
| 01-basics 基础语法 | 7 | 语法规则、运算符、类型转换、数字、字符串 |
| 02-datatypes 数据类型 | 7 | 列表、元组、字典、集合、bytes、数据结构 |
| 03-control-flow 流程控制 | 4 | 条件、for、while、推导式 |
| 04-functions 函数 | 5 | 函数参数、lambda、装饰器、生成器、作用域 |
| 05-oop 面向对象 | 3 | 类、继承多态、魔术方法、类型注解 |
| 06-modules 模块 | 2 | import机制、__name__ |
| 07-io 输入输出 | 4 | print格式化、文件读写、OS模块、with语句 |
| 08-errors 异常 | 3 | try/except、自定义异常、异常链 |
| 09-stdlib 标准库 | 19 | math/random/datetime/re/json/csv/sys/hashlib/pickle/logging/itertools/collections/functools等 |
| 10-advanced 高级 | 5 | 多线程、异步、XML、网络编程、多进程 |
| 11-builtin 内置函数 | 3 | 类型/对象、数学/迭代、IO/执行 |

## License

MIT