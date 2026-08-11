# AGENTS.md

> 个人研究助手（research-assistant）—— 跑在本地的 DeepAgents 实战项目。此文件是给 AI 助手看的项目指南，每行都进入会话上下文，保持精简。

## Project

- 定位：本地命令行 AI 研究助手（检索资料、读论文、整理知识、按需调工具）
- 技术栈：Python 3.12 / uv / deepagents 0.7.x / langchain-deepseek / DeepSeek API（deepseek-chat 或 deepseek-v4-flash，见 .env）
- 入口：`src/research_assistant/main.py`（CLI 对话循环）；M1 已完成，M2 起接入真实工具
- 语言：代码注释、提示词、文档一律中文

## Commands

- 启动 Web 服务：`uv run uvicorn research_assistant.main:app --reload` → 浏览器开 http://127.0.0.1:8000/docs
- CLI 备用入口：`uv run python -m research_assistant.core.cli`
- 安装依赖：`uv add <包名>`（不用 pip）；同步项目：`uv sync`
- 单文件验证：`uv run python -c "..."`（先 import 再执行）
- git：`git add .` → `git commit -m "..."` → `git push`

## Architecture

- `main.py` — FastAPI 入口（创建 app、注册路由、uvicorn 启动）
- `api/routes.py` — HTTP 路由层：GET /api/health、POST /api/chat（模块级构建 agent 复用）
- `core/agent.py` — `build_agent()`：create_deep_agent 组装模型/工具/system_prompt/backend
- `core/config.py` — 配置唯一入口：load_settings() 读 .env 校验，settings_summary() 脱敏
- `core/cli.py` — CLI 对话循环（备用调试入口）
- `core/tools/__init__.py` — 工具汇总导出（TOOLS）；
- `core/tools/` — 工具集：basic.py（时间/计算器）、web.py（Tavily 联网检索）、files.py（read_pdf/read_csv）；`__init__.py` 汇总导出 TOOLS
- `core/subagents/` — researcher（联网调研）、writer（整理报告）；`core/memory/AGENTS.md` — agent 记忆文件（M4 已启用，memory 参数注入 + 会话 checkpointer）
- `core/hitl.py` — 人机回环（M5）：check_interrupts（提取待审操作）+ resume（Command 恢复）；`api/` 拆分为 chat.py/approve.py/health.py
- `docs/` — 版本说明文档（v0.1 已出）

## Conventions

- **代码逐行写详细中文注释**（每行都要说明作用，不只 docstring）——用户硬性要求
- **创建文件/目录一律让用户手动操作**（PyCharm 等），只给「位置 + 文件名 + 内容」，不给命令行创建指令
- 工具 = 带 docstring 的普通函数（deepagents 风格），docstring 首行说明用途 + Args 段逐参数
- src layout：代码在 `src/research_assistant/`（下划线包名），配置在项目根 `research-assistant/`（连字符目录名）
- 密钥只在 .env（已 gitignore），程序里打印 key 必须走 settings_summary() 脱敏
- 配置集中读 config.py，不在别处直接 os.getenv

## Notes

- （待补充：M2 接入真实工具后的经验）
