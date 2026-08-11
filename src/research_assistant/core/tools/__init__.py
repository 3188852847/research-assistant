"""工具集：聚合本地 + 联网工具，对外统一导出 TOOLS。

tools/ 按能力分层：
- local/：纯本地（时间/计算/读文件），不依赖外部服务
- web/：联网（Tavily 搜索），依赖外部 API

新增工具原则：
- 纯本地 → 放 local/，加进 LOCAL_TOOLS
- 联网/外部服务 → 放 web/（或新建子包），加进 WEB_TOOLS
"""

# 从子包导入工具列表
from research_assistant.core.tools.local import LOCAL_TOOLS
from research_assistant.core.tools.web import WEB_TOOLS

# 对外统一出口：agent 组装时只需 import TOOLS
TOOLS = LOCAL_TOOLS + WEB_TOOLS