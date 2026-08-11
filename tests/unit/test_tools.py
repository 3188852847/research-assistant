"""工具函数的单元测试。

pytest 会自动发现 test_*.py 文件里的 test_* 函数并执行。
这些测试不联网、不调 API，只测纯逻辑——最快、最稳的测试。
"""

# 导入要测试的工具函数
from research_assistant.core.tools.local.basic import calculator
from research_assistant.core.tools.local.files import read_csv


# ---- calculator 测试 ----

# 测试加法
def test_add():
    # 断言：calculator(1, 2, "add") 应该等于 3
    # assert 失败 = 测试失败，pytest 会报告
    assert calculator(1, 2, "add") == 3


# 测试减法
def test_subtract():
    assert calculator(10, 4, "subtract") == 6


# 测试乘法（M1 验证过的例子）
def test_multiply():
    assert calculator(15, 7, "multiply") == 105


# 测试除法
def test_divide():
    assert calculator(20, 4, "divide") == 5


# 测试除零：应该抛 ValueError
def test_divide_by_zero():
    # pytest.raises 断言「调用会抛指定异常」
    import pytest
    with pytest.raises(ValueError):
        calculator(1, 0, "divide")


# 测试非法运算符：应该抛 ValueError
def test_invalid_op():
    import pytest
    with pytest.raises(ValueError):
        calculator(1, 2, "power")


# ---- read_csv 测试 ----

# 测试读取正常 CSV（用 tests/data/demo.csv）
def test_read_csv_normal():
    # 读 demo.csv，应包含表头和 3 行数据
    result = read_csv("tests/data/demo.csv")
    # 断言内容包含关键信息
    assert "小明" in result      # 含小明
    assert "25" in result        # 含年龄 25
    assert "北京" in result      # 含城市北京


# 测试缺文件：应该返回错误说明而不是崩溃
def test_read_csv_missing_file():
    result = read_csv("tests/data/不存在的文件.csv")
    # 应返回「错误：文件不存在」开头的字符串
    assert "文件不存在" in result