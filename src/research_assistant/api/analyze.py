"""速拆接口：POST /api/analyze

触发 agent 用 speed_analyze 技能速拆某篇文献，产出 analysis.json + analysis.md。
走 deepagents agent（用户要求 AI 相关都走 agent），不直连模型。
"""

import json
import re
import uuid  # 生成唯一 thread，避免历史复用
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import StreamingResponse

# 全局唯一 agent（deps 持有，含工具/记忆/技能）
from research_assistant.core.common.deps import agent
# 速拆结果落盘
from research_assistant.core.analysis.store import save_analysis
# 文献元数据（拿 paper_id 是否存在）
from research_assistant.core.papers.store import get_metadata

router = APIRouter(prefix="/api/analyze")


# 速拆请求体
class AnalyzeRequest(BaseModel):
    """POST /api/analyze 请求体。

    paper_id: 要速拆的文献 id
    """
    paper_id: str


# 从 agent 回复里提取 JSON 字段（四字段契约）
def extract_fields(reply: str) -> dict:
    """从 agent 的文本回复里解析四字段 + 元数据 JSON。

    兼容：agent 可能输出完整 JSON（含 research_question/core_conclusion/
    limitations/questions，还带 title/authors/year 元数据）。
    这里用正则 + JSON 解析，提取结构化字段。
    """
    # 先尝试找包含 research_question 的 JSON 对象（四字段必有它）
    json_match = re.search(r"\{[\s\S]*?\"research_question\"[\s\S]*?\}", reply)
    if json_match:
        try:
            data = json.loads(json_match.group(0))
            return data
        except json.JSONDecodeError:
            pass

    # 兼容：从代码块 ```json ``` 里提取
    block = re.search(r"```(?:json)?\s*(\{[\s\S]*?\})\s*```", reply)
    if block:
        try:
            data = json.loads(block.group(1))
            return data
        except json.JSONDecodeError:
            pass

    # 兜底：如果 agent 没按 JSON，返回空（至少不崩）
    return {
        "research_question": "",
        "core_conclusion": "",
        "limitations": "",
        "questions": "",
    }


# 保存分析结果 + 顺带从 AI 提取的 JSON 里取元数据存 metadata.json
def save_analysis_and_metadata(paper_id: str, fields: dict, report: str) -> None:
    """落盘 analysis.json + analysis.md，并提取 title/authors/year 存 metadata.json。

    参数:
        paper_id: 文献 id
        fields: 速拆四字段（可能含 title/authors/year）
        report: 报告全文
    """
    # 落盘 analysis（四字段 + 报告全文）
    save_analysis(paper_id, fields, report)

    # 从 fields 里取元数据（agent 按 prompt 放了 title/authors/year）
    meta = get_metadata(paper_id)
    for key in ("title", "authors", "year"):
        val = fields.get(key)
        if val:
            meta[key] = val
    # 写回 metadata.json
    from research_assistant.core.papers.store import save_metadata
    save_metadata(paper_id, meta)


# 触发速拆
@router.post("")
def analyze(req: AnalyzeRequest):
    """对某篇文献发起速拆。

    流程: invoke agent -> agent 加载 speed_analyze 技能 -> 读 PDF -> 填四字段
        -> 后端解析 JSON -> 落盘 analysis.json + analysis.md
    """
    paper_id = req.paper_id

    # 校验文献存在
    meta = get_metadata(paper_id)
    if not meta.get("paper_id"):
        raise HTTPException(status_code=404, detail="文献不存在")

    # 构造速拆任务的 user prompt（直接给 PDF 完整路径，避免 agent 用 ls 乱找）
    pdf_path = f"data/papers/{paper_id}/paper.pdf"   # 该文献 PDF 的相对路径（项目根）
    task = (
        f"请对文献库中的论文进行速拆。\n"
        f"- paper_id: {paper_id}\n"
        f"- PDF 路径（相对项目根）: {pdf_path}\n"
        "直接调用 read_pdf 读取上述路径的 PDF（不要用 ls 探索，路径已给出）。\n"
        "使用 speed_analyze 技能，按方法论提取四类信息。\n"
        "**必须把结果以 JSON 格式输出**，字段为 research_question / core_conclusion "
        "/ limitations / questions，值用中文。\n"
        "**同时把文献元数据 title（标题）、authors（作者）、year（年份）也放进同一个 JSON。**\n"
        "随后再输出 analysis.md 报告全文（markdown）。"
    )

    # 调 agent（用唯一 thread，避免历史复用导致跳过提取）
    thread_id = f"analyze-{paper_id}-{uuid.uuid4().hex[:6]}"
    result = agent.invoke(
        {"messages": [{"role": "user", "content": task}]},
        {"configurable": {"thread_id": thread_id}},
    )

    # 取 agent 最终回复
    reply = result["messages"][-1].content if isinstance(result, dict) else result.value["messages"][-1].content

    # 提取四字段 + 报告全文
    fields = extract_fields(reply)
    # 统一落盘：analysis + 顺带存元数据（title/authors/year）
    save_analysis_and_metadata(paper_id, fields, reply)

    return {"paper_id": paper_id, "analysis": fields, "report": reply}


# 流式速拆：POST /api/analyze/stream（SSE，逐条推工具调用卡片，最后推结果）
@router.post("/stream")
def analyze_stream(req: AnalyzeRequest):
    """流式速拆，过程实时可见（复用 agent.stream）。

    SSE 事件：
      {"type":"tool_call","tool":"read_pdf","args":{...}}  工具调用卡片
      {"type":"progress","line":"..."}                      进度行
      {"type":"done","analysis":{...},"report":"..."}       完成（含四字段）
    """
    paper_id = req.paper_id
    meta = get_metadata(paper_id)
    if not meta.get("paper_id"):
        raise HTTPException(status_code=404, detail="文献不存在")

    # 速拆任务 prompt（直接给 PDF 路径，避免 ls 探索）
    pdf_path = f"data/papers/{paper_id}/paper.pdf"
    task = (
        f"请对文献库中的论文进行速拆。\n"
        f"- paper_id: {paper_id}\n"
        f"- PDF 路径（相对项目根）: {pdf_path}\n"
        "直接调用 read_pdf 读取上述路径的 PDF（不要用 ls 探索，路径已给出）。\n"
        "使用 speed_analyze 技能，按方法论提取四类信息。\n"
        "**必须把结果以 JSON 格式输出**，字段为 research_question / core_conclusion "
        "/ limitations / questions，值用中文。\n"
        "**同时把文献元数据 title（标题）、authors（作者）、year（年份）也放进同一个 JSON。**\n"
        "随后再输出 analysis.md 报告全文（markdown）。"
    )
    thread_id = f"analyze-stream-{paper_id}-{uuid.uuid4().hex[:6]}"

    # SSE 生成器
    def event_gen():
        # 收集 agent 最终回复用
        final_reply = ""
        # 用 agent.stream 流式跑
        for event in agent.stream(
            {"messages": [{"role": "user", "content": task}]},
            {"configurable": {"thread_id": thread_id}},
        ):
            # 从事件提取「工具调用」用于卡片
            for key, value in event.items():
                if key == "model":
                    msgs = value.get("messages", [])
                    if msgs:
                        msg = msgs[-1]
                        # 有工具调用 → 推送 tool_call 事件
                        for tc in getattr(msg, "tool_calls", []) or []:
                            yield f"data: {json.dumps({'type':'tool_call','tool':tc['name'],'args':tc.get('args',{})}, ensure_ascii=False)}\n\n"
                        # 有正文 → 收进最终回复
                        content = getattr(msg, "content", "") or ""
                        if content.strip():
                            final_reply = content
                if key == "tools":
                    # 工具执行完成 → 推送一个 done 标记（可选）
                    yield f"data: {json.dumps({'type':'progress','line':'✅ 工具执行完成'}, ensure_ascii=False)}\n\n"

        # 流结束：落盘 analysis + 元数据 + 推 done（含四字段）
        fields = extract_fields(final_reply)
        save_analysis_and_metadata(paper_id, fields, final_reply)
        yield f"data: {json.dumps({'type':'done','analysis':fields,'report':final_reply}, ensure_ascii=False)}\n\n"

    return StreamingResponse(event_gen(), media_type="text/event-stream")

