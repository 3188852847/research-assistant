# research-assistant v0.1（M1 骨架）

> 阶段：M1 骨架 · 完成日期：2026-08-11
> 里程碑目标：项目初始化、配置加载、一个能对话的 agent（带 1-2 个简单工具）→ 证明链路通

## 1. 本阶段做了什么

- 项目初始化：git 仓库 + `.gitignore`（忽略 .venv/.env/.idea 等）+ src layout 目录结构
- 依赖：`deepagents`、`langchain-openai`、`python-dotenv`、`langchain-deepseek`（uv 管理）
- 配置加载：`.env.example` + `config.py`（Settings / load_settings / settings_summary，key 脱敏显示）
- 两个简单工具：`get_current_time`（当前时间）、`calculator`（四则运算，含除零/非法运算符校验）
- 主 agent：`create_deep_agent` 组装 DeepSeek 模型 + 工具 + 身份 system_prompt + LocalShellBackend
- 命令行入口：`main.py` 对话循环（exit/quit 退出）

## 2. 怎么运行

    uv run python -m research_assistant.main

启动后输入问题对话，输入 `exit` 或 `quit` 退出。

## 3. 验证结果（验收标准对照）

| 验收标准 | 结果 |
|---------|------|
| 1. 亲手跑过，功能确实工作 | 跑通，时间/计算/身份三问全部准确 |
| 2. 对照组验证工具生效 | 带工具答出当前时间（18:55:27），不带工具无法回答时间类问题 |
| 3. 笔记沉淀 | 本文件 + Obsidian 项目经历.md 踩坑记录 |
| 4. 结构清晰 | 见下方目录结构 |

## 4. 目录结构（当前）

    research-assistant/
    ├── README.md
    ├── pyproject.toml          # uv 项目定义（含 build-system）
    ├── uv.lock                 # 依赖锁文件
    ├── .env.example            # 配置模板（复制为 .env 填 key）
    ├── src/research_assistant/
    │   ├── main.py             # 入口：命令行对话循环
    │   ├── agent.py            # 主 agent 构建
    │   ├── config.py           # 配置加载
    │   └── tools/
    │       ├── __init__.py     # 工具汇总导出
    │       └── basic.py        # 基础工具（时间/计算器）
    ├── tests/                  # 测试（占位）
    └── docs/                   # 版本说明文档

## 5. 踩坑记录

- git init 后 PyCharm 自动暂存 .idea/ → `git rm --cached` 解决
- 首次 commit 报 Author identity unknown → 配置 user.name/user.email
- GitHub push 报 Connection was reset → git 配置代理（http.proxy/https.proxy）
- src layout 下 import 报 ModuleNotFoundError → pyproject.toml 加 [build-system] + uv sync
- create_deep_agent 报缺 langchain-deepseek → uv add langchain-deepseek
- .env 不会自动加载 → 代码里 load_dotenv()
- deepseek 模型身份混淆（自称 Claude）→ 用 system_prompt 显式声明身份

（详细版见 Obsidian vault「research-assistant-项目经历.md」）

## 6. 下一步（M2）

- 接入真实工具：检索、读文件等
- 对照组验证真实工具的效果
- 评估工具调用的稳定性与成本