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
from research_assistant.api.stream import router as stream_router


# 创建总路由器：把各子路由合并
router = APIRouter()
router.include_router(health_router)
router.include_router(chat_router)
router.include_router(approve_router)
router.include_router(stream_router)