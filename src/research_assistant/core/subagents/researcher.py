"""研究员子代理：负责联网调研 + 读资料，输出结构化结论。

被主代理通过 task() 委派。注意：
- 子代理的 tools / system_prompt 不继承主代理，要自己配
- 工具保持最小化：研究员只需要联网检索和读文件（读论文/资料）
"""

# 导入联网检索工具（M2 写的）
from research_assistant.core.tools.web import internet_search
# 导入读 PDF/CSV 工具（M2 写的，读论文/数据）
from research_assistant.core.tools.local.files import read_pdf, read_csv

# 研究员子代理定义（deepagents 的 subagents 字典格式）
researcher = {
    "name": "researcher",  # 唯一标识，主代理 task() 用这个名字委派
    "description": (  # 功能描述：要具体、面向操作，主代理靠它决定何时委派
        "用于需要联网获取实时信息的调研任务。"
        "当用户的问题需要最新数据、事实核查、或者查阅外部资料时，委派给我。"
    ),
    "system_prompt": (  # 子代理自己的指令（不继承主代理）
        "你是一位专业研究员。你的任务：\n"
        "1. 用 internet_search 搜索相关资料，必要时多次搜索交叉验证\n"
        "2. 如需阅读 PDF/CSV 资料，用 read_pdf / read_csv\n"
        "3. 把调研结果整理成结构化摘要：结论先行，附关键事实和数据来源\n"
        "只返回调研结论和要点，不要输出原始搜索结果。"
    ),
    "tools": [internet_search, read_pdf, read_csv],  # 最小化工具集
    # model 不传 = 继承主代理模型（DeepSeek）
}