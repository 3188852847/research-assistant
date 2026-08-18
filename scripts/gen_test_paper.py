"""生成一份测试论文 PDF（内容可读，供速拆功能测试）。跑完可删。"""

def make_pdf(text_lines: list[str], path: str) -> None:
    """手写一个最小合法 PDF，把文本写进去（ASCII 足够，中文用括号注释）。"""
    # 用 (X) Tj 逐行放置文本（PDF 文本运算符）
    lines = []
    y = 720  # 起始 y 坐标（PDF 左下原点，720 = 页面靠上）
    for i, line in enumerate(text_lines):
        lines.append(f"BT /F1 11 Tf 50 {y - i * 16} Td ({line}) Tj ET")
    content = "\n".join(lines)

    objects = []
    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    objects.append(b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
    objects.append(
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>"
    )
    # 内容流：计算 Length
    stream = f"BT /F1 11 Tf 50 720 Td (Test Paper) Tj ET\n" + content + "\n"
    stream_bytes = stream.encode("latin-1", errors="replace")
    objects.append(b"<< /Length " + str(len(stream_bytes)).encode() + b" >>\nstream\n" + stream_bytes + b"endstream")
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

    offset = 0
    pdf = bytearray(b"%PDF-1.4\n")
    offsets = []
    for i, obj in enumerate(objects, start=1):
        offsets.append(offset)
        pdf += f"{i} 0 obj\n".encode() + obj + b"\nendobj\n"
        offset = len(pdf)
    xref = offset
    pdf += f"xref\n0 {len(objects)+1}\n".encode() + b"0000000000 65535 f \n"
    for o in offsets:
        pdf += f"{o:010d} 00000 n \n".encode()
    pdf += b"trailer\n<< /Size " + str(len(objects)+1).encode() + b" /Root 1 0 R >>\nstartxref\n" + str(xref).encode() + b"\n%%EOF"
    with open(path, "wb") as f:
        f.write(bytes(pdf))


# 第二篇测试论文（与第一篇同主题「注意力」但结论/切入不同，供 Gap 对比找空白/矛盾）
text = [
    "Test Paper 2: Cross-Attention for Long Document Summarization",
    "Author: Li Hua",
    "Abstract: We study cross-attention for long document summarization.",
    "We show cross-attention improves summary quality but costs more memory.",
    "1. Research Question: Does cross-attention beat self-attention for long",
    "   document summarization (over 5000 tokens)?",
    "2. Method: Cross-attention encoder-decoder, evaluated on PubMed dataset,",
    "   10 epochs, batch 8, with sliding window.",
    "3. Results: ROUGE-L 42.1 (cross) vs 40.5 (self), but memory 1.8x higher.",
    "4. Limitation: Only summarization task; memory overhead not optimized.",
]
make_pdf(text, "tests/data/test_paper2.pdf")


# 直接放文献库？这里先输出到 data/papers/ 方便测试；也可改路径
import os  # 可选：也复制到 data/papers/ 便于直接入库（若用浏览器上传则不需要）
print("已生成第二篇测试论文 PDF: tests/data/test_paper2.pdf")