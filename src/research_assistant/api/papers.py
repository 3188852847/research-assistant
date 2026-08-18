"""文献库接口：上传/列表/删除/详情

对接前端 api/papers.ts。文件存储逻辑在 core/papers/store.py。
"""

import re
from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel

# 导入文献库存储
from research_assistant.core.papers.store import (
    list_papers, save_pdf, delete_paper, get_metadata, save_metadata,
)

# 本模块路由
router = APIRouter(prefix="/api/papers")


# 更新元数据的请求体
class MetadataUpdate(BaseModel):
    """PATCH 元数据的请求体。

    可更新字段：title/authors/year/status（AI 抽取后人工审核修正）
    """
    title: str | None = None
    authors: str | None = None
    year: str | None = None
    status: str | None = None


# 生成安全的 paper_id（从文件名去扩展名 + 清理特殊字符）
def make_paper_id(filename: str) -> str:
    """从上传文件名生成一份安全的 paper_id。

    参数:
        filename: 上传的原始文件名（如 "attention_is_all_you_need.pdf"）
    返回:
        去掉扩展名、清理非法字符的 id
    """
    # 去掉扩展名（最后一个点之后）
    base = filename.rsplit(".", 1)[0]
    # 只保留字母数字、横线、下划线、中文（其他替换成横线）
    cleaned = re.sub(r"[^\w\u4e00-\u9fff-]", "-", base)
    # 去掉首尾横线
    return cleaned.strip("-") or "paper"


# 上传 PDF（新建一篇文献）
@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    """上传 PDF 到文献库，创建每篇一文件夹。

    请求: multipart 表单，字段名 file（PDF 文件）
    返回: 新建的文献信息
    """
    # 校验是 PDF（Content-Type 含 pdf 或文件名 .pdf）
    if not (file.filename or "").lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="只支持 PDF 文件")

    # 读 PDF 字节
    pdf_bytes = await file.read()
    # 空文件校验
    if not pdf_bytes:
        raise HTTPException(status_code=400, detail="文件为空")

    # 生成 paper_id（文件名去扩展名）
    paper_id = make_paper_id(file.filename or "paper")
    # 保存到文献库（每篇一文件夹）
    save_pdf(paper_id, pdf_bytes)

    # 返回新建的文献信息
    return {"paper_id": paper_id, "message": "上传成功"}


# 文献列表
@router.get("")
def get_list():
    """返回文献库全部文献列表。

    返回: [{paper_id, title, authors, year, status, has_pdf}, ...]
    """
    return list_papers()


# 单篇详情（元数据）
@router.get("/{paper_id}")
def get_detail(paper_id: str):
    """返回一篇文献的元数据详情。

    参数:
        paper_id: 文献 id（文件夹名）
    """
    # 读元数据
    meta = get_metadata(paper_id)
    # 无该篇（元数据里也查不到该文件夹）→ 404
    if not meta.get("title") and not get_metadata(paper_id).get("paper_id"):
        raise HTTPException(status_code=404, detail="文献不存在")
    return meta


# 删除文献
@router.delete("/{paper_id}")
def remove(paper_id: str):
    """删除一篇文献的整个文件夹。"""
    ok = delete_paper(paper_id)
    if not ok:
        raise HTTPException(status_code=404, detail="文献不存在")
    return {"paper_id": paper_id, "message": "已删除"}


# 更新元数据（AI 抽取后人工审核）
@router.patch("/{paper_id}")
def update_metadata(paper_id: str, update: MetadataUpdate):
    """更新一篇文献的元数据（title/authors/year/status）。

    参数:
        paper_id: 文献 id
        update: 要更新的字段
    """
    # 读当前元数据
    meta = get_metadata(paper_id)
    # 把更新字段合并进去（只更新提供的字段）
    for field in ("title", "authors", "year", "status"):
        value = getattr(update, field)
        if value is not None:
            meta[field] = value
    # 写回
    save_metadata(paper_id, meta)
    return meta
