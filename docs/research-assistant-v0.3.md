# research-assistant v0.3（M3 子代理）

> 阶段：M3 子代理 · 完成日期：2026-08-11
> 里程碑目标：文献/代码/写作分工，多 agent 协作（本阶段落地为「研究员 + 写作员」）

## 1. 本阶段做了什么

- 新增 `core/subagents/` 包：researcher.py + writer.py + __init__.py
- 研究员（researcher）：工具=联网检索+读PDF/CSV，负责联网调研、交叉验证
- 写作员（writer）：工具=读文件，负责把材料整理成结构化报告
- 主 agent 接入：`build_agent()` 加 `subagents=[researcher, writer]`，system_prompt 补充委派指引
- 主代理通过内置 task 工具委派（子代理上下文隔离，中间过程不占主代理上下文）

## 2. 验证结果

- 结构验证：task 工具描述含 researcher/writer（注册成功硬证据）
- 端到端：调研 LangChain 最新情况 → 主 agent 委派 → 研究员联网调研 → 写作员成文
  - 实时信息：langchain 1.3.14（2026-07）、B 轮融资 1.25 亿美元（2025-10）、langchain-community 停用
  - 结构化：一句话摘要 + 六节分章 + 表格 + 结论 + 时效性提示
  - 对比 M3 前：无子代理时主代理硬答、知识截止 2025 年中、多处「待核实」

## 3. 踩坑/注意

- 子代理 tools/system_prompt 不继承主代理，必须自己配；tools 最小化（研究员有联网，写作员没有）
- model 不传则继承主代理
- 预算：子代理多轮调用 token 消耗上升，README 风险项，M3 后评估

## 4. 下一步（M4 记忆）

- 短期记忆（会话内）+ 长期记忆（跨会话），记住用户偏好
- 方案待定：文件起步，够用再说（README 待定项）