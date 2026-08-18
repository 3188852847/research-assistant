"""速拆结果存储：analysis.json（结构化字段）+ analysis.md（报告全文）

按功能规划 Analysis 字段契约：
- analysis.json：可检索的原子值（研究问题/核心结论/局限/疑问），存 data/papers/<id>/
- analysis.md：报告全文（给人读）
"""

import json
from pathlib import Path


# 项目根：core/analysis/store.py -> 上推到项目根
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent  # core/analysis -> 上5级
PAPERS_DIR = PROJECT_ROOT / "data" / "papers"


# 保存 or 更新某篇文献的速拆结果
def save_analysis(paper_id: str, fields: dict, report_full: str) -> dict:
    """把速拆结果写到 data/papers/<paper_id>/。

    参数:
        paper_id: 文献 id（文件夹名）
        fields: 结构化字段字典（research_question/core_conclusion/limitations/questions）
        report_full: 报告全文（markdown 给人读）
    返回:
        合并后的完整 analysis 数据
    """
    folder = PAPERS_DIR / paper_id
    folder.mkdir(parents=True, exist_ok=True)

    # 补 created_at（ISO 时间戳）
    from datetime import datetime, timezone
    fields["paper_id"] = paper_id
    fields["created_at"] = datetime.now(timezone.utc).isoformat()

    # 写 analysis.json（ensure_ascii=False 保留中文，indent 可读）
    (folder / "analysis.json").write_text(
        json.dumps(fields, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    # 写 analysis.md（报告全文）
    (folder / "analysis.md").write_text(report_full, encoding="utf-8")

    return fields


# 读取某篇文献的速拆结果
def get_analysis(paper_id: str) -> dict | None:
    """读取一篇文献的速拆结果。

    参数:
        paper_id: 文献 id
    返回:
        analysis 数据（结构化字段）；无速拆结果返回 None
    """
    json_path = PAPERS_DIR / paper_id / "analysis.json"
    if not json_path.exists():
        return None
    try:
        return json.loads(json_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


# 读取报告全文
def get_analysis_report(paper_id: str) -> str:
    """读取一篇文献的速拆报告全文。

    参数:
        paper_id: 文献 id（文件夹名）
    返回:
        报告 markdown 文本；无则返回空字符串
    """
    md_path = PAPERS_DIR / paper_id / "analysis.md"
    if md_path.exists():
        return md_path.read_text(encoding="utf-8")
    return ""
