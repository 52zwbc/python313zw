# -*- coding: utf-8 -*-
"""中文内置别名: 自动加载(见 site.main), 提供中文函数/类型/异常名.
位置参数与英文完全通用; 常用函数同时支持中文关键字参数(英文也可用).
打开() 默认编码为 utf-8, 避免中文用户忘记设置编码.
"""
import builtins as _B

_ALIASES = {
    "绝对值": "abs", "商和余": "divmod", "最大值": "max", "最小值": "min",
    "幂": "pow", "求和": "sum", "舍入": "round",
    "二进制": "bin", "八进制": "oct", "十六进制": "hex",
    "编码转字符": "chr", "字符转编码": "ord", "字串表示": "repr",
    "字节串": "bytes", "可变字节串": "bytearray",
    "全真": "all", "任意真": "any", "可调用": "callable",
    "包含属性": "hasattr", "是子类": "issubclass", "是实例": "isinstance",
    "长度": "len", "枚举": "enumerate", "过滤": "filter", "迭代器": "iter",
    "映射": "map", "下一个": "next", "反转": "reversed", "排序": "sorted",
    "打包": "zip", "范围": "range", "切片": "slice", "格式化": "format",
    "查看成员": "dir", "查看属性": "vars", "获取属性": "getattr",
    "设置属性": "setattr", "删除属性": "delattr", "哈希值": "hash",
    "帮助": "help", "类型": "type", "父类": "super", "属性": "property",
    "静态方法": "staticmethod", "类方法": "classmethod", "唯一标识": "id",
    "输入": "input", "编译": "compile", "评估": "eval", "运行代码": "exec",
    "局部变量": "locals", "全局变量": "globals",
    "整数": "int", "浮点数": "float", "复数": "complex",
    "字符串": "str", "列表": "list", "字典": "dict", "元组": "tuple",
    "布尔": "bool", "不可变集合": "frozenset", "集合": "set",
    "基础对象": "object", "省略号": "Ellipsis", "未实现值": "NotImplemented",
    "内存视图": "memoryview", "字符转ascii": "ascii", "断点": "breakpoint",
    "异步迭代器": "aiter", "异步下一个": "anext",
    "异常": "Exception",
    "异常_系统退出": "SystemExit", "异常_基础异常": "BaseException",
    "异常_算术错误": "ArithmeticError", "异常_断言错误": "AssertionError",
    "异常_属性错误": "AttributeError", "异常_文件末尾错误": "EOFError",
    "异常_导入错误": "ImportError", "异常_查找错误": "LookupError",
    "异常_内存错误": "MemoryError", "异常_名称错误": "NameError",
    "异常_系统错误": "OSError", "异常_运行时错误": "RuntimeError",
    "异常_语法错误": "SyntaxError", "异常_类型错误": "TypeError",
    "异常_值错误": "ValueError", "异常_警告": "Warning",
    "异常_除零错误": "ZeroDivisionError", "异常_溢出错误": "OverflowError",
    "异常_索引错误": "IndexError", "异常_键错误": "KeyError",
    "异常_局部未绑定": "UnboundLocalError", "异常_模块未找到": "ModuleNotFoundError",
    "异常_未实现": "NotImplementedError", "异常_递归错误": "RecursionError",
    "异常_缩进错误": "IndentationError", "异常_制表符错误": "TabError",
    "异常_编码错误": "UnicodeError", "异常_编码解码错误": "UnicodeDecodeError",
    "异常_编码编码错误": "UnicodeEncodeError",
    "异常_文件未找到": "FileNotFoundError", "异常_权限错误": "PermissionError",
    "异常_文件已存在": "FileExistsError", "异常_是目录错误": "IsADirectoryError",
    "异常_非目录错误": "NotADirectoryError", "异常_超时错误": "TimeoutError",
    "异常_连接错误": "ConnectionError", "异常_连接中止错误": "ConnectionAbortedError",
    "异常_连接被拒错误": "ConnectionRefusedError", "异常_连接重置错误": "ConnectionResetError",
    "异常_中断错误": "InterruptedError", "异常_用户警告": "UserWarning",
    "异常_弃用警告": "DeprecationWarning", "异常_未来警告": "FutureWarning",
    "异常_语法警告": "SyntaxWarning", "异常_运行时警告": "RuntimeWarning",
    "异常_待弃用警告": "PendingDeprecationWarning", "异常_字节警告": "BytesWarning",
    "异常_资源警告": "ResourceWarning", "异常_编码警告": "UnicodeWarning",
}

# 中文关键字参数 -> 英文 (常用函数; 未列出的函数位置参数照常用, 英文关键字也可用)
_PARAM_MAP = {
    "最大值": {"可迭代对象": "iterable", "键": "key", "默认": "default"},
    "最小值": {"可迭代对象": "iterable", "键": "key", "默认": "default"},
    "求和": {"可迭代对象": "iterable", "起始": "start"},
    "排序": {"可迭代对象": "iterable", "键": "key", "逆序": "reverse"},
    "映射": {"函数": "function", "可迭代对象": "iterable"},
    "过滤": {"函数": "function", "可迭代对象": "iterable"},
    "枚举": {"可迭代对象": "iterable", "起始": "start"},
    "打包": {"可迭代对象": "iterable"},
    "格式化": {"数值": "value", "格式": "format_spec"},
    "获取属性": {"对象": "obj", "名称": "name", "默认": "default"},
    "设置属性": {"对象": "obj", "名称": "name", "值": "value"},
    "删除属性": {"对象": "obj", "名称": "name"},
    "包含属性": {"对象": "obj", "名称": "name"},
}

def _make_wrapper(en_func, zh_name, zh2en):
    def wrapper(*args, **kwargs):
        if kwargs and zh2en:
            kwargs = {zh2en.get(k, k): v for k, v in kwargs.items()}
        return en_func(*args, **kwargs)
    wrapper.__name__ = zh_name
    wrapper.__qualname__ = zh_name
    try:
        wrapper.__module__ = "builtins"
    except Exception:
        pass
    try:
        wrapper.__doc__ = getattr(en_func, "__doc__", None)
    except Exception:
        pass
    return wrapper

def 打开(文件, 模式="r", 缓冲=-1, 编码="utf-8", 错误=None, 换行=None,
         关闭文件描述符=True, 开启器=None,
         file=None, mode=None, buffering=None, encoding=None,
         errors=None, newline=None, closefd=None, opener=None):
    """打开(文件, 模式='r', 编码='utf-8', ...) 与 open 相同, 默认编码 utf-8.
    中文参数与英文参数都可用, 中文优先."""
    if file is not None:
        文件 = file
    if mode is not None:
        模式 = mode
    if buffering is not None:
        缓冲 = buffering
    if encoding is not None:
        编码 = encoding
    if errors is not None:
        错误 = errors
    if newline is not None:
        换行 = newline
    if closefd is not None:
        关闭文件描述符 = closefd
    if opener is not None:
        开启器 = opener
    return _B.open(文件, 模式, 缓冲, 编码, 错误, 换行, 关闭文件描述符, 开启器)

for _zh, _en in _ALIASES.items():
    try:
        _obj = getattr(_B, _en)
    except AttributeError:
        continue
    if _zh in _PARAM_MAP:
        try:
            setattr(_B, _zh, _make_wrapper(_obj, _zh, _PARAM_MAP[_zh]))
        except Exception:
            pass
    else:
        try:
            setattr(_B, _zh, _obj)
        except Exception:
            pass

try:
    setattr(_B, "打开", 打开)
except Exception:
    pass

# 英文 open 默认编码也改为 utf-8(便于多国语言; 二进制模式不受影响)
try:
    _orig_open_en = _B.open
    class _OpenWrapperEn:
        def __init__(self, orig):
            self._orig = orig
            try:
                self.__doc__ = orig.__doc__
            except Exception:
                pass
            try:
                self.__name__ = "open"
            except Exception:
                pass
            try:
                self.__module__ = "builtins"
            except Exception:
                pass
        def __call__(self, file, mode="r", buffering=-1, encoding=None,
                     errors=None, newline=None, closefd=True, opener=None):
            if encoding is None and isinstance(mode, str) and "b" not in mode:
                encoding = "utf-8"
            return self._orig(file, mode, buffering, encoding, errors,
                              newline, closefd, opener)
    _B.open = _OpenWrapperEn(_orig_open_en)
except Exception:
    pass

# 标准库中文别名暂不加载(本版按用户要求跳过 _zh_stdlib)
# try:
#     import _zh_stdlib
#     _zh_stdlib.install()
# except Exception:
#     pass
# 退出: site.setquit() 后才有 quit/exit, 此处尽力别名
for _q_zh, _q_en in (("退出", "quit"),):
    try:
        setattr(_B, _q_zh, getattr(_B, _q_en))
    except Exception:
        pass

# 初始化=__init__: 类中 def 初始化(self) 自动视为构造器
try:
    _orig_build_class = _B.__build_class__
    def __build_class__(func, name, *bases, **kwds):
        cls = _orig_build_class(func, name, *bases, **kwds)
        try:
            # 仅默认元类走快捷路径, 避免触发自定义元类的 __dict__ 描述器
            # (否则 inspect 的 metaclass_dict_as_property 测试会失败)
            if type(cls) is type:
                d = getattr(cls, "__dict__", None)
                if d is not None and "初始化" in d and "__init__" not in d:
                    setattr(cls, "__init__", d["初始化"])
        except Exception:
            pass
        return cls
    __build_class__._zh_wrapped = True
    _B.__build_class__ = __build_class__
except Exception:
    pass

# 注意: 保留 _B 供 打开() 运行时使用, 仅清理循环变量
try:
    del _zh, _en, _obj
except NameError:
    pass
try:
    del _q_zh, _q_en
except NameError:
    pass
