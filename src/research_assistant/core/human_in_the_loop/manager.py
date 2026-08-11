"""人机回环（Human-in-the-Loop）处理层。

封装「检查中断 → 展示待审操作 → 恢复执行」的流程函数，
让 Web 层（api/routes.py）可以干净地做两阶段交互。
"""

# 导入 Command：langgraph 的恢复指令
# 中断后用它携带用户的决策（批准/拒绝/编辑）续跑 agent
from langgraph.types import Command


# 从共享依赖取 agent（全局唯一实例）
from research_assistant.core.common.deps import agent

def check_interrupts(result) -> list[dict] | None:
    """检查 agent 调用结果是否被中断。

    参数:
        result: agent.invoke() 的返回值（可能是 dict 或带 .interrupts 的对象）
    返回:
        有待审操作时返回操作列表（每个含 name/args/allowed_decisions），
        没有中断时返回 None。
    """
    # 兼容两种返回形式：
    # 1. dict 形式：中断信息在 result["__interrupt__"]
    # 2. 对象形式（version="v2"）：中断信息在 result.interrupts
    interrupts = getattr(result, "interrupts", None)  # 优先取对象属性
    if interrupts is None and isinstance(result, dict):
        interrupts = result.get("__interrupt__")      # dict 形式兜底

    # 没有中断（None 或空列表）就返回 None
    if not interrupts:
        return None

    # 取第一个中断的 value（本次设计每次调用至多一个中断点）
    interrupt_value = interrupts[0].value

    # 待审操作列表：每个是 {"name": 工具名, "args": 参数, ...}
    action_requests = interrupt_value["action_requests"]

    # 审查配置：每个操作的允许决策（approve/edit/reject/respond）
    review_configs = interrupt_value["review_configs"]
    # 按工具名建索引，方便下面合并
    config_map = {cfg["action_name"]: cfg for cfg in review_configs}

    # 组装成前端友好的结构：工具名 + 参数 + 允许的决策
    pending = []
    for action in action_requests:
        cfg = config_map[action["name"]]
        pending.append({
            "name": action["name"],          # 工具名（如 delete）
            "args": action["args"],          # 工具参数（如 {"path": "temp.txt"}）
            "allowed_decisions": cfg["allowed_decisions"],  # 允许哪些决策
        })
    return pending


def resume(thread_id: str, decisions: list[dict]) -> dict:
    """用用户的决策恢复被中断的 agent 执行。

    参数:
        thread_id: 首次调用的会话 ID（必须一致，否则找不到中断状态）
        decisions: 决策列表，顺序对应待审操作
            [{"type": "approve"}] 或 [{"type": "reject"}]
            或 [{"type": "edit", "edited_action": {"name": 工具名, "args": {...}}}]
    返回:
        {"reply": 最终回复, "pending": 是否再次中断}
    """
    # 用 Command 携带决策恢复执行
    # config 必须用同一个 thread_id（人机回环恢复的硬性要求）
    result = agent.invoke(
        Command(resume={"decisions": decisions}),
        config={"configurable": {"thread_id": thread_id}},
        version="v2",  # 中断恢复需要 v2 协议
    )

    # 恢复后可能再次中断（比如多个操作逐一审批）
    pending = check_interrupts(result)
    if pending:
        # 又遇到新的待审操作：返回给前端继续处理
        return {"reply": None, "pending": pending}

    # 没有中断了：返回最终回复
    return {"reply": result.value["messages"][-1].content, "pending": None}