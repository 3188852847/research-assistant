---
name: speed_analyze
description: 速拆单篇文献，按方法论提取研究问题/核心结论/局限/疑问，产出 analysis.json + analysis.md。当用户对某篇已导入文献发起「速拆/分析这篇/快速读这篇」时使用。
---

# 速拆文献技能

## 定位

速拆 = 不精读，快速提取一篇文献的四类信息，供后续横向对比、检索、问答复用。效率目标参照方法论「60 分钟拆 30 篇」，不是写论文解读。

## 触发

- 用户对某篇已导入文献（paper_id）发起「速拆/分析这篇」
- api/analyze 构造会话，invoke agent：任务 = 「用 speed_analyze 技能速拆 paper_id 这篇」

## 执行步骤

1. 调用 read_pdf 工具读取 paper_id 对应 PDF 全文
   - **PDF 路径约定**：该文献的 PDF 位于 `data/papers/<paper_id>/paper.pdf`（相对项目根）
   - 用 read_pdf 读这个路径（如 `data/papers/test_paper/paper.pdf`）
   - 若 read_pdf 返回「文件不存在/失败」，先尝试 glob/ls 确认文件位置再读
2. 按顺序翻阅（不要从头精读）：摘要 → 结论/讨论 → 局限与未来研究方向 →（必要时）方法
3. 提取四类信息，填 analysis.json（契约字段见下）
4. 产出 analysis.md 报告全文（给人读）

## 输出契约（与前后端契约一致，字段名不可改）

```json
{
  "paper_id": "string",          // 关联文献 id
  "research_question": "string", // 研究问题：作者具体探究什么？
  "core_conclusion": "string",   // 核心结论：最终发现什么？
  "limitations": "string",       // 研究局限：作者自己承认的不足
  "questions": "string",         // 我的疑问：真实产生的质疑
  "created_at": "ISO时间戳"      // 速拆时间（后端填）
}
```

## 两列纪律（方法论核心，违反即失败）

### 局限 limitations

- 尽量保留作者原话，不自行「补足」局限
- 表述含糊、无法从原文确认 → 停下，走人机回环问用户

### 疑问 questions

- 只记录真实产生的质疑，例如：
  - 换文化/行业/人群，结论会变吗？
  - 为何 A 显著而 B 不显著？
  - 是否存在遗漏的中介或调节变量？
  - 该理论放在新技术/新场景下是否失效？
  - 研究方法真能支撑因果推断吗？
- 没有真实疑问就如实留空，不要凑

## 人机回环（复用 M5 interrupt）

- 只在关键处停：局限/结论表述含糊、原文信息不足时
- 不停在无关细节——否则速拆变问答，失去效率
- 停下时卡片流弹审批卡：「这句局限原文是 X，我理解为 Y，对吗？」

## 产出落盘

- 速拆结果**必须在回复里直接输出 JSON**（四字段 + title/authors/year 元数据），字段契约见上
- 你**不要**调用任何「落盘/写文件」工具，也不要描述「由谁落盘」——只需把 JSON 输出在回复里
- 后端 API 层会解析你输出的 JSON，由 `core/store.py` 落盘 analysis.json + analysis.md + metadata.json
- 报告全文（analysis.md 内容，markdown）也直接输出在回复里（JSON 之后）

## 边界

- 只做单篇速拆，不做横向对比找信号（那是 gap 技能的事）
- 不写论文解读/文献综述
