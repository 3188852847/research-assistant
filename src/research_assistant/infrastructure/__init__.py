"""基础设施层：与业务逻辑平级的工程设施（横切关注点）。

成员：
- logging.py     日志系统（统一配置 + get_logger）
- errors.py      异常体系（AppError 基类 + 具体错误类型）
- tracing.py     请求追踪 / token 统计（后续档实现）
- persistence.py 持久化（SQLite checkpointer，后续档实现）

原则：core（业务）可以使用 infrastructure，但 infrastructure 不依赖 core。
"""

# 导出日志与异常（第一档）
from research_assistant.infrastructure.logging import setup_logging, get_logger
from research_assistant.infrastructure.errors import (
    AppError,
    ConfigError,
    ModelError,
    ToolError,
    ApprovalError,
)

# 导出追踪（第二档）
from research_assistant.infrastructure.tracing import extract_usage, TraceContext

# 公共出口
__all__ = [
    "setup_logging", "get_logger",
    "AppError", "ConfigError", "ModelError", "ToolError", "ApprovalError",
    "extract_usage", "TraceContext",
]