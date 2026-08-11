# research-assistant v0.7（M7 收尾）

> 阶段：M7 收尾 · 完成日期：2026-08-11
> 里程碑目标：文档补全、测试补全（pytest 引入）、复盘沉淀

## 1. 本阶段做了什么

- 引入 pytest（开发依赖）+ 核心工具测试
  - calculator：加/减/乘/除 + 除零 + 非法运算符（6 个测试）
  - read_csv：正常读取 + 缺文件容错（2 个测试）
- pyproject.toml 加 [tool.pytest.ini_options] testpaths=["tests"]
  - 坑：pytest 9 对无 __init__.py 的 tests 目录默认不递归收集，需显式配置
- README 补「使用说明」章节 + 当前进度标注

## 2. 验证结果

- `uv run pytest` → 8 passed（无参数直接跑通）

## 3. 项目最终状态（M1-M7 全景）

| 里程碑 | 内容 | 状态 |
|--------|------|------|
| M1 | 骨架：git/配置/FastAPI/基础工具 | ✅ |
| M2 | 工具：Tavily 联网 + PDF/CSV 读取 | ✅ |
| M3 | 子代理：研究员 + 写作员 | ✅ |
| M4 | 记忆：AGENTS.md 注入 + 会话 + 文件持久化 | ✅ |
| M5 | 人机回环：interrupt_on + 两阶段接口 | ✅ |
| M6 | 前端：React+TS 界面 + 审批 UI + 生产托管 | ✅ |
| M7 | 收尾：pytest + 文档 + 复盘 | ✅ |

## 4. 下一步（项目外）

- 后续可选：记忆方案升级（向量库/语义检索）、更多测试覆盖、前端打磨
- 可选：技能（skills）独立里程碑、更多测试覆盖、记忆方案升级（向量库）