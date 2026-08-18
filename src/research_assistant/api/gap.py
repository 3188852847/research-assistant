"""Gap 发现接口：POST /api/gap

选 N 篇同主题文献，把它们的 Analysis 拼起来喂 agent 横向对比，
产出「研究空白/矛盾/空缺」报告。MVP 不用向量（注意点③：拼上下文给 AI 即可）。
"""

import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# 全局唯一 agent
from research_assistant.core.common.deps import agent
# 读 Analysis
from research_assistant.core.analysis.store import get_analysis

router = APIRouter(prefix="/api/gap")


# Gap 请求体
class GapRequest(BaseModel):
    """POST /api/gap 请求体。

    paper_ids: 要横向对比的文献 id 列表（多篇同主题）
    """
    paper_ids: list[str]


# 触发 Gap 发现
@router.post("")
def gap(req: GapRequest):
    """对多篇文献的 Analysis 做横向对比，找研究空白。

    流程: 读每篇 Analysis -> 拼上下文 -> invoke agent 对比 -> 返回 Gap 报告
    """
    if not req.paper_ids:
        raise HTTPException(status_code=400, detail="请选择至少一篇文献")

    # 收集每篇的 Analysis 上下文
    contexts = []
    for pid in req.paper_ids:
        analysis = get_analysis(pid)
        if not analysis:
            raise HTTPException(status_code=404, detail=f"文献 {pid} 还没有速拆分析")
        contexts.append(
            f"### 文献 {pid}\n"
            f"研究问题: {analysis.get('research_question','')}\n"
            f"核心结论: {analysis.get('core_conclusion','')}\n"
            f"研究局限: {analysis.get('limitations','')}\n"
            f"我的疑问: {analysis.get('questions','')}\n"
        )

    all_context = "\n".join(contexts)
    task = (
        "请对以下多篇文献的速拆分析做横向对比，找出研究空白（Gap）。\n"
        f"{all_context}\n"
        "请从三个角度输出报告：\n"
        "1. **已被研究过**：这些文献共同覆盖了什么\n"
        "2. **矛盾/争议**：哪些地方结论互相矛盾或证据冲突\n"
        "3. **研究空白**：哪些方向还没被做，值得关注\n"
        "用中文，结构化 markdown 输出，控制在 500 字内。"
    )

    thread_id = f"gap-{uuid.uuid4().hex[:6]}"
    result = agent.invoke(
        {"messages": [{"role": "user", "content": task}]},
        {"configurable": {"thread_id": thread_id}},
    )
    reply = result["messages"][-1].content if isinstance(result, dict) else result.value["messages"][-1].content

    return {"paper_ids": req.paper_ids, "gap_report": reply}
