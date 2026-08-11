# research-assistant v0.5（M5 人机回环）

> 阶段：M5 人机回环 · 完成日期：2026-08-11
> 里程碑目标：关键步骤（写文件、删东西、执行命令）停下确认，危险动作加护栏

## 1. 本阶段做了什么

- agent 层：`build_agent()` 加 `interrupt_on`——delete（全开）/execute（批准/拒绝）/write_file/edit_file（批准/拒绝）需审批，只读工具不中断
- 处理层：`core/hitl.py`——check_interrupts（提取待审操作）+ resume（Command 恢复执行）
- Web 层：API 路由按资源拆分（chat.py / approve.py / health.py + __init__.py 汇总）
  - POST /api/chat：遇中断返回 pending（待审操作），不返回最终回复
  - POST /api/approve：提交决策（approve/reject/edit）恢复执行

## 2. 验证结果

| 路径 | 结果 |
|------|------|
| 中断 | delete 操作在工具执行前被拦住，返回工具名/参数/允许决策 ✅ |
| 批准 | agent 真正删除文件（Test-Path False）✅ |
| 拒绝 | 文件保留（Test-Path True），agent 明确说明未执行 ✅ |

## 3. 踩坑记录

- deepagents 0.7.5 不用 version="v2" 时，中断信息在 result["__interrupt__"]（dict 形式），不是 result.interrupts——hitl 要兼容两种
- 同一 thread_id 反复测试会积累历史状态，可能导致恢复时上下文错乱（用全新 thread 验证）
- interrupt_on 的 PyCharm 类型警告（dict[Literal...] vs dict[str, bool | InterruptOnConfig]）是静态检查过严，运行正常，可忽略

## 4. 下一步（M6 前端美化）

- 核心能力已全部打通，M6 做真正的漂亮 Web 界面（替换 Swagger）