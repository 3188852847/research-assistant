# research-assistant v0.2（M2 工具扩展）

> 阶段：M2 工具扩展 · 完成日期：2026-08-11
> 里程碑目标：接入真实工具（联网检索、读 PDF/CSV），扩展 agent 能力

## 1. 本阶段做了什么

- 内置工具确认：deepagents 默认自带 9 个工具（ls/read_file/write_file/edit_file/delete/glob/grep/execute/task），M1 起就可用
- 新增 Tavily 联网检索：`core/tools/web.py` 的 `internet_search`（需 TAVILY_API_KEY）
- 新增自定义读文件：`core/tools/files.py` 的 `read_pdf`（pypdf，前 3 页）、`read_csv`（标准库，前 20 行）
  - 动机：内置 read_file 只能读纯文本，PDF/CSV 读不了——论文场景必须扩展
- 工具总数：5 个（get_current_time / calculator / internet_search / read_pdf / read_csv）
- 测试数据：`tests/data/`（demo.csv、demo.pdf）

## 2. 验证结果

| 工具 | 验证方式 | 结果 |
|------|---------|------|
| 内置文件工具 | 让 agent 读 demo.txt | 准确复述内容 ✅ |
| internet_search | 搜 2025 诺贝尔物理学奖 | 返回 Nature/Physics World/Yale 结果，agent 回答与之一致 ✅ |
| read_pdf | 直接调用读 demo.pdf | 提取出 "Hello PDF Test" ✅ |
| read_csv | 直接调用 + agent 端到端 | 输出 3 行表格，agent 准确转述 ✅ |

## 3. 踩坑记录（本阶段新增）

- `search.py` 模块级读 TAVILY_API_KEY 报 KeyError → 模块自己先 load_dotenv()（import 阶段就执行，不能依赖 config 的延迟加载）
- 测试数据应放 tests/ 而非项目根目录（规范）
- pytest 尚未引入，tests/ 目前只放测试数据（M7 再补自动化测试）

## 4. 下一步（M3 子代理）

- 文献 / 代码 / 写作分工，多 agent 协作
- 具体分工细节做到 M3 再定