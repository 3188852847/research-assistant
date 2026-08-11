# research-assistant v0.6（M6 前端美化）

> 阶段：M6 前端美化 · 完成日期：2026-08-11
> 里程碑目标：核心能力稳定后做真正的漂亮 Web 界面（替换 Swagger）

## 1. 本阶段做了什么

- 前端脚手架：Vite 8 + React 19 + TypeScript 6 + Oxlint（`web/` 目录）
- 开发代理：vite.config.ts 把 /api/* 转发到 FastAPI（5173 → 8000）
- 聊天界面：`web/src/components/Chat.tsx`（消息流 + 输入框 + Enter 发送 + 加载态）
- 会话管理：`App.tsx` 的 thread_id 生成 + 新建会话（key 强制重建 Chat）
- 审批 UI：pending 消息渲染成审批卡片（工具/参数/批准/拒绝按钮），对接 /api/approve
- 生产托管：main.py 挂载 web/dist 静态文件，一条 uvicorn 命令跑完整应用
- 架构修正：新增 `core/deps.py` 统一持有全局唯一 agent 实例（人机回环状态共享的关键）

## 2. 验证结果

- 开发模式：npm run dev（5173）+ uvicorn（8000），代理联通，对话正常
- 审批流程（Web 端）：发删除 → 审批卡片 → 批准 → 文件真正删除 ✅
- 生产模式：uvicorn 单进程，访问 :8000 直接看到界面，对话 + 审批全通

## 3. 踩坑记录（本阶段核心）

- **agent 单例 bug**：chat 和 approve 各建 agent → checkpointer 状态分裂 → 审批恢复错乱。修复：core/deps.py 统一持有（详见 vault 项目经历）
- 循环导入：approve 从 api 包 import agent ↔ api/__init__ 互相引用 → agent 移出 api 包
- 文件名带空格：test_delete_me.txt 实际是 " test_delete_me.txt"，agent 找不到——排查文件问题先看文件名细节
- root_dir 固定：LocalShellBackend(root_dir=Path(__file__) 上推 4 级)，不依赖启动目录
- npm 安装慢：切 npmmirror 镜像源

## 4. 下一步（M7 收尾）

- 文档补全、测试补全（pytest 引入）、复盘沉淀