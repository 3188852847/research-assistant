"""共享依赖容器：全局唯一的 agent 实例（及其他共享资源）。

为什么需要单例：
- 人机回环要求 /api/chat 和 /api/approve 用同一个 agent 实例
  （checkpointer 状态在 agent 内部，两个实例互不相通会丢状态，M6 踩过坑）
- agent 构建成本高（读配置、组装图），应该构建一次全局复用

本目录（common/）是共享组件的家：以后需要跨模块共享的资源
（数据库连接、记忆存储、配置单例等）都放这里，统一管理。
"""

# 导入 agent 构建函数
from research_assistant.core.agent import build_agent


# 用 None 占位 + lazy 构建（首次访问时才真正构建 agent）
# 好处：import 时不立刻构建（快），用到才构建；测试时可重置
_agent = None


def get_agent():
    """获取全局唯一的 agent 实例（lazy：首次调用时构建，之后复用）。"""
    # 声明使用模块级变量（否则会被当成局部变量）
    global _agent
    # 首次调用时构建，之后直接返回已有的
    if _agent is None:
        _agent = build_agent()
    return _agent


# 兼容旧用法：模块级直接暴露 agent（chat.py/manager.py 已用 from deps import agent）
# 保持向后兼容，新代码建议用 get_agent()
agent = get_agent()