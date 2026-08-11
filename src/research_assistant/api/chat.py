"""对话接口：POST /api/chat。

人机回环：遇到需审批的操作时返回 pending（待审操作），不返回最终回复。
"""

# 从共享依赖取 agent（全局唯一实例）
from research_assistant.core.deps import agent

# 导入 FastAPI 的 APIRouter（路由注册器）
from fastapi import APIRouter
# 从 pydantic 导入 BaseModel——请求/响应的数据结构定义
from pydantic import BaseModel

# 从 hitl 导入检查中断的函数
from research_assistant.core.hitl import check_interrupts

# 创建本模块的路由器
# prefix="/api" 表示这个路由下所有接口的 URL 都以 /api 开头
router = APIRouter(prefix="/api")


# 定义对话请求的数据结构（请求体）
class ChatRequest(BaseModel):
    """POST /api/chat 的请求体。

    message: 用户输入的问题文本
    thread_id: 会话 ID——同一个 ID 的多轮对话共享历史（会话内记忆）
    """
    message: str
    thread_id: str = "default"  # 默认会话 ID；不传则所有请求都进同一个会话


# 定义对话响应的数据结构
class ChatResponse(BaseModel):
    """POST /api/chat 的响应体。

    两种形态：
    - 正常：{"reply": "agent 的回答"}
    - 待审批：{"pending": [{"name": 工具, "args": 参数, "allowed_decisions": [...]}]}
    """
    reply: str | None = None          # agent 的最终回复（待审批时为 None）
    pending: list | None = None       # 待审操作列表（正常回复时为 None）


# POST /api/chat：对话接口（核心）
# request: ChatRequest 类型的请求体，FastAPI 自动解析 JSON 并校验
@router.post("/chat")
def chat(request: ChatRequest) -> ChatResponse:
    """接收用户消息，调用 agent 回答。

    人机回环：如果 agent 要执行需审批的操作（删除/写文件/执行命令），
    会中断并返回待审操作（pending），不返回最终回复；
    前端拿到 pending 后，调 /api/approve 提交决策继续。
    """
    # 调用 agent：把用户消息作为一条 user 消息传进去
    # config 里带 thread_id——checkpointer 按它存取会话历史
    result = agent.invoke(
        {"messages": [{"role": "user", "content": request.message}]},
        config={"configurable": {"thread_id": request.thread_id}},
    )

    # 检查是否被中断（agent 要执行需审批的操作）
    pending = check_interrupts(result)
    if pending:
        # 有待审操作：不返回最终回复，把操作详情返回给前端等审批
        return ChatResponse(reply=None, pending=pending)

    # 没有中断：取最后一条消息的文本内容，就是 agent 的最终回复
    final_answer = result["messages"][-1].content
    return ChatResponse(reply=final_answer, pending=None)