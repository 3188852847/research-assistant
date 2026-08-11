"""本地工具包：纯本地能力，不依赖外部服务。

- basic.py：时间查询 / 四则运算
- files.py：读 PDF / CSV
"""

# 汇总本地工具
from research_assistant.core.tools.local.basic import get_current_time, calculator
from research_assistant.core.tools.local.files import read_pdf, read_csv

# 本地工具列表（agent 组装时用）
LOCAL_TOOLS = [get_current_time, calculator, read_pdf, read_csv]