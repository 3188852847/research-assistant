"""API 路由包：汇总各路由模块并构建共享 agent。

main.py 只需 from research_assistant.api import router 一次，
就能拿到全部接口（/health、/chat、/approve）。
"""

# 导入 FastAPI 的 APIRouter（用于合并子路由）
from fastapi import APIRouter

# 导入构建 agent 的函数
from research_assistant.core.agent import build_agent

# 从各路由模块导入它们的 router
from research_assistant.api.health import router as health_router
from research_assistant.api.chat import router as chat_router
from research_assistant.api.approve import router as approve_router

# 构建 agent（模块级：服务启动时构建一次，所有请求复用同一个实例）
# 每个请求都重建 agent 会浪费时间和 token，所以构建一次放这里
# 注意：chat.py 里用到的 agent 就是从这个包导入的（见下方）
agent = build_agent()

# 把 chat.py 里引用的 agent 绑定为这里的实例
# 这样 chat.py 不需要自己构建，共享同一个 agent（含 checkpointer 状态）
import research_assistant.api.chat as chat_module
chat_module.agent = agent

# 创建总路由器：把各子路由合并
router = APIRouter()
router.include_router(health_router)
router.include_router(chat_router)
router.include_router(approve_router)