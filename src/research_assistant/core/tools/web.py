"""联网检索工具：用 Tavily 搜索实时信息。

Tavily 是一个专门给 AI agent 用的搜索 API，返回结构化结果。
key 从 .env 的 TAVILY_API_KEY 读取（config.py 已 load_dotenv）。
"""

# 导入 os，用于读取环境变量（Tavily key）
import os
# 导入 dotenv 的加载函数
from dotenv import load_dotenv

# 模块级先加载 .env：因为本模块在 import 阶段就要读 TAVILY_API_KEY，
# 不能依赖 config.py 的 load_settings()（那是 agent 构建时才调用，太晚了）
load_dotenv()

# 导入 TavilyClient：Tavily 的官方客户端
from tavily import TavilyClient

# 创建 Tavily 客户端实例
# api_key 从环境变量读取——注意必须先 load_dotenv() 才能读到 .env
# （config.py 的 load_settings() 里已调用 load_dotenv()，agent 构建时已生效）
tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])


# 联网搜索工具（deepagents 自定义工具 = 普通函数 + docstring）
# 参数带类型注解，agent 会按签名生成调用参数
# docstring 是给 agent 看的说明书：首行说用途，Args 段逐参数说明
def internet_search(query: str, max_results: int = 5) -> str:
    """运行联网搜索，获取实时信息。用于查找最新新闻、事实核查、实时数据。

    Args:
        query: 搜索关键词（用中文问就传中文）
        max_results: 返回结果条数，默认 5
    返回:
        搜索结果摘要文本（标题+链接+内容片段）
    """
    # 调用 Tavily 搜索接口
    # search 返回一个 dict，里面的 "results" 是搜索结果列表
    response = tavily_client.search(query, max_results=max_results)

    # 把原始结果整理成可读文本（agent 直接消费的）
    # 遍历每条结果，拼成「标题 - 链接 - 内容」的格式
    lines = []
    for item in response.get("results", []):
        # 每条结果提取三个字段，用空字符串兜底（防止字段缺失报错）
        title = item.get("title", "")
        url = item.get("url", "")
        content = item.get("content", "")
        # 拼成一行，追加到列表
        lines.append(f"- {title} | {url} | {content[:200]}")
    # 用换行符把所有行拼成一个字符串返回
    return "\n".join(lines)