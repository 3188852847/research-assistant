"""基础工具：时间查询 + 四则运算计算器。

本模块的两个函数会被 tools/__init__.py 汇总导出给 agent。
"""

# 导入标准库 datetime，用于获取当前时间
from datetime import datetime


# ---- 工具 1：当前时间 ----
# deepagents 自定义工具 = 带 docstring 的普通函数
# 函数名 = 工具名（agent 调用时用的名字）
# docstring = 工具的说明书（agent 靠它判断何时调用、怎么用）
def get_current_time() -> str:
    """获取当前本地日期和时间（年-月-日 时:分:秒）。

    当用户问「现在几点」「今天几号」之类的时间问题时调用。
    返回一个人类可读的字符串。
    """
    # datetime.now() 获取当前本地时间，返回一个 datetime 对象
    # strftime 把 datetime 对象格式化成字符串
    # 格式代码含义：
    #   %Y = 4 位年份，%m = 2 位月份，%d = 2 位日期
    #   %H = 24 小时制小时，%M = 分钟，%S = 秒
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ---- 工具 2：四则运算计算器 ----
# 参数带类型注解（a: float, b: float, op: str = "add"）
# agent 会按签名生成调用参数，所以类型和默认值要写清楚
# docstring 里 Args: 段逐参数说明，参数名必须和函数签名一字不差
def calculator(a: float, b: float, op: str = "add") -> float:
    """对两个数字做四则运算。

    Args:
        a: 第一个操作数
        b: 第二个操作数
        op: 运算符，可选 add（加）、subtract（减）、multiply（乘）、divide（除），默认 add
    返回:
        计算结果；除数为 0 或运算符不支持时抛出 ValueError。
    """
    # 根据 op 的值进入对应的运算分支
    if op == "add":
        # 加法：直接返回两数之和
        return a + b
    # 减法分支
    elif op == "subtract":
        return a - b
    # 乘法分支
    elif op == "multiply":
        return a * b
    # 除法分支
    elif op == "divide":
        # 除法前先检查除数是否为 0
        # 如果不检查，Python 会抛 ZeroDivisionError，报错信息对模型不友好
        # 这里主动抛出带中文说明的 ValueError，模型更容易理解
        if b == 0:
            raise ValueError("除数不能为 0")
        # 除数合法，执行除法
        return a / b
    # op 传了不支持的取值（比如 "power"）
    else:
        # 抛出明确错误，同时列出可选值方便模型改正
        raise ValueError(f"不支持的运算符: {op}，可选值: add/subtract/multiply/divide")