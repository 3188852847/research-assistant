"""API 路由层：把 core 的核心能力暴露成 HTTP 接口。

FastAPI 通过 APIRouter 组织路由，main.py 里把 router 挂到 app 上。
"""

# 导入 FastAPI 的 APIRouter（路由注册器）和 HTTPException（错误响应）
from fastapi import APIRouter, HTTPException

# 从 pydantic 导入 BaseModel——请求/响应的数据结构定义
# FastAPI 用类型定义自动做参数校验 + 生成 Swagger 文档
from pydantic import BaseModel

# 导入构建 agent 的函数（core 层的核心逻辑）
from research_assistant.core.agent import build_agent

# 构建 agent（模块级：服务启动时构建一次，所有请求复用同一个实例）
# 每个请求都重建 agent 会浪费时间和 token，所以构建一次放这里
agent = build_agent()


# 创建路由器实例
# prefix="/api" 表示这个路由下所有接口的 URL 都以 /api 开头
router = APIRouter(prefix="/api")


# 定义对话请求的数据结构（请求体）
class ChatRequest(BaseModel):
    """POST /api/chat 的请求体。

    message: 用户输入的问题文本
    """
    message: str


# 定义对话响应的数据结构
class ChatResponse(BaseModel):
    """POST /api/chat 的响应体。

    reply: agent 的回答文本
    """
    reply: str


# GET /api/health：健康检查
# 启动后浏览器访问 http://127.0.0.1:8000/api/health 应返回 {"status": "ok"}
@router.get("/health")
def health() -> dict:
    """健康检查：确认服务活着。"""
    # 返回一个简单的 JSON
    return {"status": "ok"}


# POST /api/chat：对话接口（核心）
# request: ChatRequest 类型的请求体，FastAPI 自动解析 JSON 并校验
@router.post("/chat")
def chat(request: ChatRequest) -> ChatResponse:
    """接收用户消息，调用 agent 回答。

    注意：本函数用 def 而非 async def 定义。
    FastAPI 会自动把普通 def 端点放进线程池执行，
    这样 agent.invoke()（同步阻塞调用）不会卡住事件循环。
    """
    # 调用 agent：把用户消息作为一条 user 消息传进去
    # invoke 返回结果对象，里面包含多轮消息
    result = agent.invoke({"messages": [{"role": "user", "content": request.message}]})

    # 取最后一条消息的文本内容，就是 agent 的最终回复
    final_answer = result["messages"][-1].content

    # 返回结构化响应（FastAPI 自动序列化成 JSON）
    return ChatResponse(reply=final_answer)