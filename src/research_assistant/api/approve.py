"""审批接口：POST /api/approve。

人机回环的第二阶段：用户对待审操作提交决策（批准/拒绝），恢复 agent 执行。
"""

# 导入 FastAPI 的 APIRouter
from fastapi import APIRouter
# 从 pydantic 导入 BaseModel
from pydantic import BaseModel

# 从 hitl 导入恢复执行的函数
from research_assistant.core.hitl import resume


# 本模块的路由器
router = APIRouter(prefix="/api")


# 定义审批请求的数据结构
class ApproveRequest(BaseModel):
    """POST /api/approve 的请求体。

    thread_id: 会话 ID（必须和产生中断的那次 /api/chat 一致）
    decisions: 决策列表，顺序对应待审操作
        [{"type": "approve"}] 批准 / [{"type": "reject"}] 拒绝
    """
    thread_id: str
    decisions: list[dict]


# 审批接口：用户提交决策，恢复 agent 执行
# 注意：resume 内部用 deps 的全局 agent（与 /api/chat 同一实例），
# 所以这里不需要再 import agent
@router.post("/approve")
def approve(request: ApproveRequest) -> dict:
    """提交人机回环的审批决策，恢复 agent 执行。

    返回 {"reply": 最终回复} 或 {"pending": 新的待审操作}。
    """
    # 调用 hitl.resume 恢复执行
    # 返回 {"reply": 最终回复} 或 {"pending": 新的待审操作}
    outcome = resume(request.thread_id, request.decisions)
    # 把处理结果直接返回（FastAPI 自动序列化成 JSON）
    return outcome