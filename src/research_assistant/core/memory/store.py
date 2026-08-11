"""记忆存储：负责记忆的读写与格式管理。

当前状态：结构占位——记忆目前由 deepagents 原生机制（memory 参数注入）
+ agent 自主写入（write_file 更新 AGENTS.md）承担，本模块尚未接入。

将来改造方向（记忆方案升级时在此实现）：
- 记忆文件的读写封装（读取/追加/更新用户偏好）
- 格式管理（AGENTS.md 的 markdown 结构解析）
- 升级向量库时：语义检索替代全文注入（只改这里，接口不变）
"""

# 记忆文件路径（相对项目根，供 agent 虚拟路径映射用）
# 注意：agent.py 的 memory=["/src/research_assistant/core/memory/AGENTS.md"]
# 与此路径对应，改动需同步
MEMORY_FILE = "src/research_assistant/core/memory/AGENTS.md"


def read_memory() -> str:
    """读取记忆文件内容。

    返回: 记忆文件的完整文本（供注入 agent 上下文）。
    """
    # TODO(记忆改造): 实现记忆文件读取
    raise NotImplementedError("记忆存储将在记忆方案升级时实现")


def append_preference(text: str) -> None:
    """把一条用户偏好追加进记忆文件。

    参数:
        text: 要记住的偏好内容（如「报告用 Markdown 格式」）。
    """
    # TODO(记忆改造): 实现偏好追加（去重、格式对齐）
    raise NotImplementedError("记忆存储将在记忆方案升级时实现")