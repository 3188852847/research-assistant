"""流式对话接口：POST /api/chat/stream（SSE 流式输出）。

前端用 fetch 读取流，逐条显示 agent 的思考过程 + 最终回复。
SSE 格式：每条消息 "data: {json}\n\n"。
"""

# 导入 FastAPI 的 APIRouter 和流式响应
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
# 导入 pydantic 的 BaseModel
from pydantic import BaseModel
# 导入 json：把数据序列化成 SSE 消息
import json

# 从共享依赖取 agent（全局唯一实例）
from research_assistant.core.common.deps import agent
# 导入流式执行（高效版，边产进度边收结果）
from research_assistant.core.presenters import stream_agent


# 本模块的路由器
router = APIRouter(prefix="/api")


# 流式对话请求体
class StreamRequest(BaseModel):
    """POST /api/chat/stream 的请求体。

    message: 用户输入
    thread_id: 会话 ID
    """
    message: str
    thread_id: str = "default"


# 流式对话接口
@router.post("/chat/stream")
def chat_stream(request: StreamRequest):
    """流式对话：逐条推送进度 + 最终回复（SSE）。"""

    # 定义生成器：产出 SSE 消息流
    def event_generator():
        # 调用流式执行（agent.stream + 收集推理/结果）
        for item in stream_agent(
                agent,
                {"messages": [{"role": "user", "content": request.message}]},
                {"configurable": {"thread_id": request.thread_id}},
        ):
            # 判断消息类型（三种：推理内容 / 进度行 / 完成标记）
            if isinstance(item, tuple):
                # tuple = 特殊标记（推理或完成）
                marker = item[0]

                # 推理内容：推送 reasoning 类型消息
                if marker == "__reasoning__":
                    # item[1] 是推理文本
                    reasoning = item[1]
                    # SSE：data: {"type": "reasoning", "content": "..."}\n\n
                    yield f"data: {json.dumps({'type': 'reasoning', 'content': reasoning}, ensure_ascii=False)}\n\n"

                # 完成标记：推送最终回复
                elif marker == "__done__":
                    reply = item[1] or "(无回复)"
                    # SSE：data: {"type": "done", "reply": "..."}\n\n
                    yield f"data: {json.dumps({'type': 'done', 'reply': reply}, ensure_ascii=False)}\n\n"
            else:
                # 非 tuple = 进度行
                # SSE：data: {"type": "progress", "line": "..."}\n\n
                yield f"data: {json.dumps({'type': 'progress', 'line': item}, ensure_ascii=False)}\n\n"

    # 返回 SSE 流式响应
    # media_type 必须是 text/event-stream（SSE 标准）
    return StreamingResponse(event_generator(), media_type="text/event-stream")