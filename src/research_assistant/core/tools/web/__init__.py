"""联网工具包：依赖外部服务。

- search.py：Tavily 联网搜索（需要 TAVILY_API_KEY）
"""

# 汇总联网工具
from research_assistant.core.tools.web.search import internet_search

# 联网工具列表
WEB_TOOLS = [internet_search]