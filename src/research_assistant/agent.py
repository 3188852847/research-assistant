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
from research_assistant.config import load_settings

# 从 tools 包导入工具汇总列表（get_current_time + calculator）
from research_assistant.tools import TOOLS


# 构建并返回主 agent 的函数
# 返回类型注解：create_deep_agent 返回的对象（deepagents 的 agent）
def build_agent():
    # 加载配置：读取 .env 中的 API key / base_url / model
    # 如果 .env 没配好，这里会抛出带引导信息的 ValueError（config.py 里写的）
    settings = load_settings()

    # 调用 create_deep_agent 组装 agent
    agent = create_deep_agent(
        model=settings.model,  # model: 指定模型。deepagents 从 .env 读取 DEEPSEEK_API_KEY 等配置。注：.env 不会自动加载，必须先在 config.py 里 load_dotenv()
        system_prompt=( # system_prompt: 给模型设定身份和行为准则
            "你是 research-assistant，一个跑在用户自己电脑上的个人研究助手。\n"
            "你的能力：检索资料、读论文、整理知识、按需调用工具。\n"
            "回答使用中文，简洁准确；涉及时间、计算等具体问题时，优先调用工具获取准确结果，"
            "不要凭记忆猜测。"
        ),
        tools=TOOLS,  # tools: 追加自定义工具（内置的 ls/read_file/execute 等 9 个工具自动保留）
        backend=LocalShellBackend(), # backend: 本地文件系统后端，文件真实落盘到当前工作目录
        debug=True,  # debug: 设为 True 会打印 agent 思考/调用工具的详细过程，方便排查。注：M1 调试阶段先开 True，跑通后改成 False 保持输出干净
    )
    # 把组装好的 agent 返回给调用方（main.py 用）
    return agent