# research-assistant v0.4（M4 记忆）

> 阶段：M4 记忆 · 完成日期：2026-08-11
> 里程碑目标：短期记忆（会话内）+ 长期记忆（跨会话），记住用户偏好

## 1. 本阶段做了什么

- 记忆文件：`core/memory/AGENTS.md`（角色/工具准则/用户偏好/记忆写入规则）
- deepagents 原生记忆：`memory=["/src/research_assistant/core/memory/AGENTS.md"]` 注入
  - 关键：路径是相对项目根的虚拟路径（LocalShellBackend 的 / = 项目根）
- 会话记忆：checkpointer（MemorySaver）+ thread_id——同一会话多轮共享历史
- Web 接入：`/api/chat` 新增 thread_id 字段，请求级会话
- 长期记忆：方案 A（agent 自主写 + 规则约束）——记忆文件写清「什么值得记」，agent 自己判断写入

## 2. 验证结果

| 能力 | 验证 | 结果 |
|------|------|------|
| 记忆注入 | 问「记忆文件写了什么」 | 准确复述角色/准则/偏好 ✅ |
| 会话内记忆 | 同 thread 记「我叫小明」→「我叫什么？」 | 答「你叫小明」✅ |
| 长期写入 | 说「报告用 Markdown」 | 自动写入记忆文件 ✅ |
| 跨会话回忆 | 新进程问「记得关于我什么」 | 回忆出全部 4 条偏好 ✅ |

## 3. 踩坑记录

- `memory` 路径：`/AGENTS.md` 会命中项目根 AGENTS.md（误读）；要写 `src/research_assistant/core/memory/AGENTS.md` 相对项目根的虚拟路径
- 加 checkpointer 后 invoke 必须带 `config={'configurable': {'thread_id': ...}}`，否则报错
- deepagents 内置 grep 在中文 Windows 报 gbk 解码错（deepagents bug，grep 中文文件时触发，可设 PYTHONUTF8=1 缓解）

## 4. 下一步（M5 人机回环）

- 关键步骤（写文件、删东西、花 API 钱）前停下确认
- 危险动作加护栏