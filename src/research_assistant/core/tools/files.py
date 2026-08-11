"""文件读取工具：扩展内置 read_file 读不了的格式（PDF、CSV）。

内置 read_file 只能读纯文本；本模块补充 PDF/CSV 的读取，
让 agent 能读论文（PDF）和表格数据（CSV）。
"""

# 导入 csv 模块：Python 标准库，解析 CSV 文件
import csv

# 导入 Path：跨平台路径处理（Windows 反斜杠 / Linux 斜杠自动适配）
from pathlib import Path

# 导入 PdfReader：pypdf 库的 PDF 读取器
# 注意：只有真正读 PDF 时才 import，避免依赖缺失导致模块导入失败
# （如果 pypdf 没装，其他工具仍可用）
try:
    from pypdf import PdfReader
    # PDF 支持标志：True 表示 pypdf 可用
    PDF_SUPPORTED = True
except ImportError:
    # pypdf 未安装时降级：PDF 工具仍存在但会提示缺依赖
    PDF_SUPPORTED = False


def read_pdf(file_path: str, max_pages: int = 3) -> str:
    """读取 PDF 文件的文本内容（前若干页）。

    Args:
        file_path: PDF 文件的路径（相对或绝对）
        max_pages: 最多读取的页数，默认 3 页（论文摘要+引言够用，省 token）
    返回:
        PDF 提取出的文本；读取失败时返回错误说明。
    """
    # 检查 pypdf 是否可用（import 时已探测）
    if not PDF_SUPPORTED:
        # 未安装时给出明确提示
        return "错误：未安装 pypdf，无法读取 PDF。请执行 uv add pypdf"

    # 用 Path 规范化路径（处理相对/绝对路径）
    path = Path(file_path)

    # 检查文件是否存在
    if not path.exists():
        return f"错误：文件不存在：{file_path}"

    # 打开 PDF 并读取文本
    try:
        # 创建 PdfReader 对象（读取整个 PDF 的元数据和页面）
        reader = PdfReader(str(path))

        # 逐页提取文本
        # 只取前 max_pages 页，避免长论文撑爆上下文
        pages_text = []
        for i, page in enumerate(reader.pages[:max_pages]):
            # 每页提取文本，strip() 去掉首尾空白
            text = page.extract_text() or ""
            # 给每页加页码标记，agent 能知道内容在第几页
            pages_text.append(f"--- 第 {i + 1} 页 ---\n{text.strip()}")

        # 所有页拼成一个字符串返回
        return "\n\n".join(pages_text)
    except Exception as e:
        # 任何解析错误都转成可读信息（而不是让 agent 看到裸异常）
        return f"读取 PDF 失败：{e}"


def read_csv(file_path: str, max_rows: int = 20) -> str:
    """读取 CSV 文件的表格内容（前若干行）。

    Args:
        file_path: CSV 文件的路径（相对或绝对）
        max_rows: 最多返回的数据行数，默认 20 行
    返回:
        表格文本（每行用 | 分隔列），读取失败时返回错误说明。
    """
    # 规范化路径
    path = Path(file_path)

    # 检查文件是否存在
    if not path.exists():
        return f"错误：文件不存在：{file_path}"

    # 打开并解析 CSV
    try:
        # 以 UTF-8 打开（中文 CSV 最常见编码）
        # newline="" 是 csv 模块的要求，避免 Windows 下换行错乱
        with open(path, "r", encoding="utf-8", newline="") as f:
            # csv.reader 把每一行解析成「单元格列表」
            reader = csv.reader(f)

            # 逐行处理，最多 max_rows 行
            lines = []
            for i, row in enumerate(reader):
                # 到上限就停
                if i >= max_rows:
                    break
                # 每行单元格用 | 连接（比逗号更清晰，因为单元格里可能含逗号）
                lines.append(" | ".join(row))

        # 所有行拼成一个字符串返回
        return "\n".join(lines)
    except Exception as e:
        # 解析错误转成可读信息
        return f"读取 CSV 失败：{e}"