"""记忆加载：把记忆注入 agent 上下文。

当前状态：结构占位——记忆注入目前由 agent.py 的 memory 参数
（deepagents 原生机制）完成，本模块尚未接入。

将来改造方向：
- 从 store 读取记忆并格式化
- 决定注入方式（全文 / 摘要 / 向量检索结果）
"""

# 导入记忆存储的读取函数
from research_assistant.core.memory.store import read_memory


def load_memory_context() -> str:
    """加载记忆上下文（供注入 agent）。

    返回: 格式化后的记忆文本。
    """
    # TODO(记忆改造): 调用 read_memory 并格式化
    raise NotImplementedError("记忆加载将在记忆方案升级时实现")