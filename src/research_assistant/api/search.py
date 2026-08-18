"""检索接口：GET /api/search?q=关键词

MVP 用 grep 扫 data/papers/*/analysis.json，找含关键词的 Analysis。
命中 = 返回文献列表（paper_id + 命中字段 + 标题），点开可看 Analysis。
不用向量库（注意点③：文献少时 grep 够快）。
"""

from fastapi import APIRouter
from pathlib import Path

# 项目根 / data/papers
# search.py 在 src/research_assistant/api/，上推 4 级到项目根：
#   api -> research_assistant -> src -> 项目根
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
PAPERS_DIR = PROJECT_ROOT / "data" / "papers"

router = APIRouter(prefix="/api/search")


# 检索：grep 扫所有 analysis.json
@router.get("")
def search(q: str):
    """按关键词检索 Analysis 四字段。

    参数:
        q: 检索关键词
    返回:
        [{paper_id, title, matched_field, snippet}, ...]  命中的文献
    """
    # 关键词为空：返回空
    if not q.strip():
        return []

    results = []
    query = q.strip().lower()

    # 遍历每篇文献的 analysis.json
    if PAPERS_DIR.exists():
        for folder in PAPERS_DIR.iterdir():
            if not folder.is_dir():
                continue
            aj = folder / "analysis.json"
            if not aj.exists():
                continue
            # 读 analysis + metadata（标题）
            import json
            try:
                analysis = json.loads(aj.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue

            # 在四字段里搜关键词（大小写不敏感）
            for field in ("research_question", "core_conclusion", "limitations", "questions"):
                val = analysis.get(field, "")
                if query in val.lower():
                    # 命中：截取命中片段前后附近文字
                    idx = val.lower().find(query)
                    snippet = val[max(0, idx-20): idx+len(query)+30]
                    results.append({
                        "paper_id": folder.name,
                        "title": analysis.get("title", "") or folder.name,
                        "matched_field": field,
                        "snippet": snippet,
                    })
                    break  # 一篇只取一条命中

    return results
