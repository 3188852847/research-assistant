"""共享依赖：全局唯一的 agent 实例。

人机回环要求 /api/chat 和 /api/approve 用同一个 agent 实例
（checkpointer 状态在 agent 内部，两个实例互不相通会丢状态）。
本模块是 agent 的唯一持有者，各路由从这里取。
"""

# 导入 agent 构建函数
from research_assistant.core.agent import build_agent

# 模块级构建一次（服务启动时），全局唯一实例
agent = build_agent()