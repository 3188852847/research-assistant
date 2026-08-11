"""主 agent 构建：把模型、工具、系统提示词组装成 deep agent。

本模块是项目的核心——所有对话都通过这里构建的 agent 进行。
"""

# 导入 create_deep_agent：deepagents 框架的入口函数
# 它接收模型、工具、系统提示词等配置，返回一个可调用的 agent 对象
from deepagents import create_deep_agent

# 导入 LocalShellBackend：本地文件系统后端
# 笔记里的坑：不传 backend 时文件不落盘（默认 StateBackend 写进内存）
# LocalShellBackend 让 agent 真实读写磁盘文件
# 注意：无沙箱，agent 能执行任意 shell 命令，仅限可信环境（个人本机 OK）
from deepagents.backends import LocalShellBackend

# 从 config 模块导入配置加载函数
# load_settings() 读取 .env 里的 DeepSeek 配置并校验
from research_assistant.core.config import load_settings

# 从 tools 包导入工具汇总列表（get_current_time + calculator）
from research_assistant.core.tools import TOOLS

# 导入子代理定义（M3：研究员 + 写作员）
from research_assistant.core.subagents.researcher import researcher
from research_assistant.core.subagents.writer import writer

# 导入持久化检查点（SQLite，重启不丢会话）
from research_assistant.infrastructure.persistence import get_checkpointer
# 导入 create_file_data：把记忆文件内容装进 agent 的文件系统
from deepagents.backends.utils import create_file_data

# 导入技能源目录（core/skills 包导出的常量）
from research_assistant.core.skills import SKILLS_DIR

# 构建并返回主 agent 的函数
# 返回类型注解：create_deep_agent 返回的对象（deepagents 的 agent）
def build_agent():
    # 加载配置：读取 .env 中的 API key / base_url / model
    # 如果 .env 没配好，这里会抛出带引导信息的 ValueError（config.py 里写的）
    settings = load_settings()


    # 读取记忆文件内容（AGENTS.md 注入用）
    # 记忆文件：给 agent 的持久上下文（角色/偏好/准则），始终注入
    from pathlib import Path
    memories_dir = Path(__file__).parent / "memory"
    agents_md = (memories_dir / "AGENTS.md").read_text(encoding="utf-8")

    # 获取持久化检查点（SQLite 落盘，重启后会话历史仍在）
    checkpointer = get_checkpointer()


    # 调用 create_deep_agent 组装 agent
    agent = create_deep_agent(
        model=settings.model,  # model: 指定模型。deepagents 从 .env 读取 DEEPSEEK_API_KEY 等配置。注：.env 不会自动加载，必须先在 config.py 里 load_dotenv()
        system_prompt=(
            "你是 research-assistant，一个跑在用户自己电脑上的个人研究助手。\n"
            "你的能力：检索资料、读论文、整理知识、按需调用工具。\n"
            "回答使用中文，简洁准确；涉及时间、计算等具体问题时，优先调用工具获取准确结果，"
            "不要凭记忆猜测。\n"
            "复杂研究任务：先委派给 researcher 子代理联网调研，再委派给 writer 子代理整理成报告。"
        ),
        tools=TOOLS,  # tools: 追加自定义工具（内置的 ls/read_file/execute 等 9 个工具自动保留）
        backend=LocalShellBackend(
            root_dir=str(Path(__file__).parent.parent.parent.parent)  # 项目根：core/agent.py → 上推 4 级
        ),  # backend: 本地文件系统后端，root_dir 固定为项目根，任何启动目录下都一致
        subagents=[researcher, writer],  # 子代理：复杂任务委派给研究员调研、写作员成文
        skills=[SKILLS_DIR],  # 技能源目录：agent 按需加载技能（渐进式披露）
        memory=["/src/research_assistant/core/memory/AGENTS.md"],  # 记忆文件：指向我们自己的 agent 记忆（角色/偏好/准则）
        checkpointer=checkpointer,  # 检查点：保存每个会话的状态（对话历史），会话内多轮记忆的基础




        interrupt_on={ # 人机回环：哪些工具要人工审批
            "delete": {"allowed_decisions": ["approve", "edit", "reject"]}, # 高风险：删除/执行命令，全开（可批准/可编辑/可拒绝）
            "execute": {"allowed_decisions": ["approve", "reject"]},
            "write_file": {"allowed_decisions": ["approve", "reject"]}, # 中风险：写文件/改文件，允许批准或拒绝
            "edit_file": {"allowed_decisions": ["approve", "reject"]},
            # 低风险（读文件/搜索/自定义工具）不配置 = 不中断
        },

        debug=False,  # debug: 设为 True 会打印 agent 思考/调用工具的详细过程，方便排查。注：M1 调试阶段先开 True，跑通后改成 False 保持输出干净

    )
    # 把组装好的 agent 返回给调用方（main.py 用）
    return agent