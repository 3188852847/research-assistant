"""文献库存储：data/papers/ 每篇一文件夹（PDF + metadata.json + notes.md + analysis）

按功能规划：
- data/papers/<论文名>/paper.pdf -> PDF 原文
- data/papers/<论文名>/metadata.json -> 元数据（作者/年份/标题/状态）
- data/papers/<论文名>/notes.md -> 笔记（可空）
- analysis：速拆后才有（analysis.json + analysis.md），MVP 先不管

本模块负责文件系统的读写（新建/列表/删除），不涉及 AI 元数据抽取。
"""

import json
import shutil
from pathlib import Path


# 文献库根目录：data/papers/（项目根下，跟着项目走、进 Git 好备份）
# persistence.py 用上推四级得项目根，这里同款
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent  # core/papers/store.py -> 上推到项目根
PAPERS_DIR = PROJECT_ROOT / "data" / "papers"


# 获取某篇文献的文件夹路径
def paper_dir(paper_id: str) -> Path:
    """返回某篇文献的文件夹路径。

    参数:
        paper_id: 文献 id（= 文件夹名）
    返回:
        该文献对应的 data/papers/<id> 路径
    """
    return PAPERS_DIR / paper_id


# 保存上传的 PDF（新建一篇文献）
def save_pdf(paper_id: str, pdf_bytes: bytes) -> Path:
    """保存 PDF 到文献库，创建每篇一文件夹。

    参数:
        paper_id: 文献 id（建议用文件名或 uuid）
        pdf_bytes: PDF 文件内容（字节）
    返回:
        保存的 PDF 路径
    """
    # 确保文献库根存在
    PAPERS_DIR.mkdir(parents=True, exist_ok=True)
    # 该篇文件夹
    folder = paper_dir(paper_id)
    folder.mkdir(parents=True, exist_ok=True)

    # PDF 路径
    pdf_path = folder / "paper.pdf"
    # 写 PDF 字节
    pdf_path.write_bytes(pdf_bytes)

    # 初始化空元数据（后续 AI 抽取填）
    metadata_path = folder / "metadata.json"
    if not metadata_path.exists():
        metadata_path.write_text(json.dumps({
            "paper_id": paper_id,
            "title": "",
            "authors": "",
            "year": "",
            "status": "待读",
        }, ensure_ascii=False, indent=2), encoding="utf-8")

    # 初始化空笔记
    notes_path = folder / "notes.md"
    if not notes_path.exists():
        notes_path.write_text("", encoding="utf-8")

    return pdf_path


# 列出所有文献（扫描 data/papers/ 下每个文件夹）
def list_papers() -> list[dict]:
    """列出文献库全部文献。

    返回:
        列表，每个 = {paper_id, title, authors, year, status, has_pdf}
    """
    # 文献库不存在 = 空库
    if not PAPERS_DIR.exists():
        return []

    papers = []
    # 遍历每个子文件夹（一篇文献一个）
    for folder in PAPERS_DIR.iterdir():
        # 只处理文件夹
        if not folder.is_dir():
            continue

        paper_id = folder.name
        # 读元数据（文件可能不存在/缺字段，用默认兜底）
        meta = {}
        meta_path = folder / "metadata.json"
        if meta_path.exists():
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                meta = {}

        # 组装返回结构
        papers.append({
            "paper_id": paper_id,
            "title": meta.get("title", ""),
            "authors": meta.get("authors", ""),
            "year": meta.get("year", ""),
            "status": meta.get("status", "待读"),
            "has_pdf": (folder / "paper.pdf").exists(),
        })

    # 按 paper_id 排序（稳定）
    papers.sort(key=lambda p: p["paper_id"])
    return papers


# 删除一篇文献
def delete_paper(paper_id: str) -> bool:
    """删除某篇文献的整个文件夹。

    参数:
        paper_id: 文献 id
    返回:
        是否删除成功（True=删了，False=不存在）
    """
    folder = paper_dir(paper_id)
    # 文件夹不存在 = 无可删
    if not folder.exists():
        return False
    # 递归删除整个文件夹（PDF+元数据+笔记）
    shutil.rmtree(folder)
    return True


# 读取一篇文献的元数据
def get_metadata(paper_id: str) -> dict:
    """读取一篇文献的元数据（用于详情/编辑）。

    参数:
        paper_id: 文献 id
    返回:
        元数据字典；无该篇或元数据缺失时返回默认
    """
    folder = paper_dir(paper_id)
    meta_path = folder / "metadata.json"
    if meta_path.exists():
        try:
            return json.loads(meta_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {"paper_id": paper_id, "title": "", "authors": "", "year": "", "status": "待读"}


# 保存元数据（AI 抽取后 / 人工编辑后写入）
def save_metadata(paper_id: str, metadata: dict) -> None:
    """保存一篇文献的元数据到 metadata.json。

    参数:
        paper_id: 文献 id
        metadata: 元数据字典（含 title/authors/year/status 等）
    """
    folder = paper_dir(paper_id)
    folder.mkdir(parents=True, exist_ok=True)
    # 确保 paper_id 在里面
    metadata["paper_id"] = paper_id
    # 写 JSON（ensure_ascii=False 保留中文，indent 可读）
    (folder / "metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
