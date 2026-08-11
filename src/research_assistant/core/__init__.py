"""core 包：项目核心逻辑层（与 api 外壳解耦）。

公共出口（外部统一从这里 import，不关心内部路径）：
- build_agent：构建主 agent（最常用）
- load_settings / Settings：配置加载

其他能力（工具/子代理/记忆/人机回环）各自有独立的聚合出口：
- core.tools.TOOLS
- core.subagents
- core.human_in_the_loop（check_interrupts / resume）
- core.common（全局共享依赖）
"""

# 导出 agent 构建函数（cli.py、deps.py 等从这拿）
from research_assistant.core.agent import build_agent

# 导出配置加载（任何需要配置的地方）
from research_assistant.core.config import load_settings, Settings

# 声明「from research_assistant.core import *」时导出的名字
# （明确列出公共 API，防止意外导出内部模块）
__all__ = ["build_agent", "load_settings", "Settings"]