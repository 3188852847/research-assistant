"""记忆子系统：存储 + 加载 + 内容文件。

结构：
- store.py   记忆存储（读写/格式管理）——记忆方案升级时在此实现
- loader.py  记忆加载（注入 agent 上下文）——记忆方案升级时在此实现
- AGENTS.md  记忆内容文件（当前由 deepagents memory 参数注入）

当前：结构占位，功能仍由 deepagents 原生机制承担。
"""

# 导出存储与加载的入口（记忆改造时实现后，外部从这里用）
from research_assistant.core.memory.store import read_memory, append_preference
from research_assistant.core.memory.loader import load_memory_context

# 公共出口
__all__ = ["read_memory", "append_preference", "load_memory_context"]