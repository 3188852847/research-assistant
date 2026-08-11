"""工具集：所有工具的注册入口。

本文件只负责汇总导出工具，工具的具体实现在各个独立模块里
（如 basic.py 放基础工具）。agent 构建时只需从这里导入 TOOLS 一次。
"""

# 从 basic 模块导入两个工具函数
# 模块路径规则：research_assistant.tools.basic 表示
# research_assistant/tools/ 目录下的 basic.py 文件
from research_assistant.tools.basic import get_current_time, calculator

# TOOLS 列表：把工具汇总成列表，供 agent 挂载
# 以后新增工具：在新模块里实现 → 在这里 import → 追加进列表
# 这样 agent.py 永远只需要 TOOLS 一个入口，不用感知每个工具细节
TOOLS = [get_current_time, calculator]