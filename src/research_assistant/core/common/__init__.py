"""common 包：跨模块共享的全局单例/资源。

规矩（放这里的标准）：
- 必须是「跨模块共享」的资源（多个模块都用同一个实例）
- 采用 lazy 单例模式（get_xxx() + 模块级 xxx 兼容）
- 不适合放这里的：单一模块私有的工具、不共享的配置

当前成员：
- deps.get_agent()：全局唯一 agent 实例
- settings.get_settings()：全局唯一配置实例
"""

# 导出共享依赖（agent 单例）
from research_assistant.core.common.deps import agent, get_agent
# 导出配置单例
from research_assistant.core.common.settings import settings, get_settings

# 明确公共 API
__all__ = ["agent", "get_agent", "settings", "get_settings"]