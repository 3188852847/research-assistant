# research-assistant

> 个人研究助手 —— DeepAgents 学完后的第一个实战项目。

## 一、一句话定位

一个跑在自己电脑上的 AI 研究助手：能检索资料、读论文、整理知识、按需调用工具，并在关键时刻停下问主人确认 —— 把 DeepAgents 教程里学到的**工具调用 / 子代理 / 记忆 / 技能 / 人机回环**全部集成进一个真实可用的项目。**以 Web 界面为最终形态**（不是黑窗口命令行）。

## 二、背景与目标

### 为什么做

- DeepAgents 教程 12 章已学完（0-11 全闭环），需要一个实战项目把知识变成能力
- 现有工具栈（Hermes + Obsidian）已覆盖日常，但缺少一个「按自己需求定制」的研究助手
- 本项目可作为 AI 应用开发的学习载体与后续研究的实验平台

### 目标（做什么）

| 能力 | 说明 | 来自教程哪块 |
|------|------|--------------|
| 工具调用 | 检索、读文件、执行脚本等，agent 按需选工具 | DeepAgents 工具章节 |
| 子代理 | 文献 / 代码 / 写作分工协作 | 子代理章节 |
| 记忆 | 记住用户偏好、项目上下文、历史结论 | 记忆章节 |
| 技能 | 把常用流程固化成可复用技能 | 技能章节 |
| 人机回环 | 关键步骤（写文件、删东西、花 API 钱）停下问主人 | 人机回环章节 |
| Web 服务 | FastAPI 暴露能力，浏览器操作；最终做漂亮前端 | 后端章节 |

### 非目标（不做什么）

- ~~不做成网页服务~~（已推翻：改为 Web 形态，见里程碑）
- 核心稳定前**不做花哨前端**——先 FastAPI 自带 Swagger 界面顶着，能力全部打通后再打磨界面
- 不追求多模态（文本为主）
- 不接微信/QQ 等社交网关（那是 Hermes 的事，不重复造轮子）

## 三、技术选型

| 项 | 选择 | 理由 |
|----|------|------|
| 语言 | Python 3.12+ | 教程同栈，AI 生态最全 |
| 包管理 | uv | 快、省心，与 DeepAgents_learn 环境一致 |
| 模型 | DeepSeek API（deepseek-chat） | 便宜够用，教程实战已验证 |
| Agent 框架 | deep_agents（DeepAgents 库） | 教程主线，学了就用 |
| Web 后端 | FastAPI | 现代、自带 Swagger 交互文档、类型安全，从 M1 就上 |
| 配置 | .env 存密钥 | 不把 key 写进代码 |
| 版本管理 | git | 每个阶段可回退，留改动账目 |

> 依赖按需添加，不一次性装全（uv add，不用 pip）。

## 四、项目结构（当前）

```
research-assistant/
├── README.md            # 本文档
├── pyproject.toml       # uv 项目定义
├── .env                 # API key（不入库）
├── src/research_assistant/
│   ├── main.py          # 入口：FastAPI app 工厂 + 静态托管
│   ├── api/             # 表现层：HTTP 路由（chat/approve/health）
│   ├── core/            # 领域层：业务逻辑（与外壳解耦，CLI/Web 共用）
│   │   ├── agent.py     # 主 agent 构建
│   │   ├── config.py    # 配置加载
│   │   ├── cli.py       # CLI 备用入口（含思考过程可视化）
│   │   ├── common/      # 业务共享单例（agent/settings）
│   │   ├── tools/       # 工具集（local 本地 / web 联网 分层）
│   │   ├── subagents/   # 子代理（researcher/writer）
│   │   ├── memory/      # 记忆（AGENTS.md + store/loader 占位）
│   │   ├── skills/      # 技能（按类别分目录，SKILL.md 按需加载）
│   │   ├── human_in_the_loop/  # 人机回环子系统
│   │   └── presenters/  # 呈现层（思考过程可视化）
│   └── infrastructure/  # 基础设施层：日志/异常/token 统计/SQLite 持久化
├── web/                 # 前端（React+TS，独立于 Python 包）
│   └── src/{pages,components,api,hooks,styles}
├── tests/               # 测试（unit/ 分层）
└── data/                # 运行时数据（checkpoints.sqlite，不入库）
```

## 五、开发计划（里程碑）

按「先跑通再扩展」推进，每个里程碑结束 = 用户亲自验证通过 + 有笔记沉淀。

- **M1 骨架**：项目初始化、配置加载、FastAPI 服务跑起来（Swagger `/docs` 可访问）+ 一个能对话的 agent（带 1-2 个简单工具）→ 证明链路通
- **M2 工具扩展**：接入检索/读文件等真实工具，带对照组验证工具确实生效
- **M3 子代理**：文献/代码/写作分工，多 agent 协作
- **M4 记忆**：短期记忆（会话内）+ 长期记忆（跨会话），记住用户偏好
- **M5 人机回环**：关键操作前停下确认，危险动作加护栏
- **M6 前端美化**：核心能力全部稳定后，做真正的漂亮 Web 界面（替换 Swagger 顶着用的阶段）
- **M7 收尾**：文档补全、测试补全、复盘沉淀

> **Web 路线**：M1-M5 全程 FastAPI + Swagger 交互文档（浏览器点按钮就能测，比 CLI 好看且零前端成本）→ M6 一次性上真前端。
> **当前进度**：M1-M7 全部完成（2026-08-11）。五大能力 + Web 前端 + 思考过程可视化已落地；结构大优化（api/core/infrastructure 分层、web 移到根目录）；基础设施（日志/异常/token 统计/SQLite 持久化）已建。见 `docs/` 各版本说明。
## 六、验收标准

每个里程碑完成后自问：

1. 我（用户）亲手跑过，功能确实工作，不是 AI 自说自话
2. 演示功能的示例带了对照组（如「有工具 vs 没工具」），能独立验证
3. 有笔记沉淀在 vault（500-实验与项目 或对应目录）
4. 代码结构清楚，隔一周回来还能看懂

## 七、待定 / 风险

- [x] 具体子代理分工细节 → M3 已定：研究员（联网调研）+ 写作员（成文）
- [x] 预算控制 → 已建 token 用量统计（infrastructure/tracing.py），可量化评估
- [ ] 记忆方案（文件 / 向量库 / 复用腾讯记忆栈？）→ 已落地文件版（M4），向量库升级待研究

## 八、使用说明

### 开发模式（前后端分离，热更新）
- 后端：`uv run uvicorn research_assistant.main:app --reload`（:8000，Swagger 在 /docs）
- 前端：`cd web && npm run dev`（:5173，代理转发 /api 到 :8000）

### 生产模式（一条命令）
- 构建前端：`cd web && npm run build`
- 启动：`uv run uvicorn research_assistant.main:app --reload`（:8000，直接访问界面）

### 测试
- `uv run pytest`（核心工具测试，tests/unit/）

### CLI 备用入口（含思考过程可视化）
- `uv run python -m research_assistant.core.cli`

### 基础设施
- 日志：`infrastructure/logging.py`（setup_logging + get_logger）
- 持久化：SQLite 检查点（data/checkpoints.sqlite，对话历史跨重启保留）
- token 统计：`infrastructure/tracing.py`（每次调用记录用量）
- 技能：`core/skills/skills/{research,writing,coding}/`（SKILL.md 按需加载）
---

*项目启动：2026-08-11 · 配套基础笔记见 vault「100-基础」*
