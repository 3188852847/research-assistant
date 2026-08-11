"""日志系统：统一的项目日志配置。

为什么需要：
- 现在项目出错全靠 traceback，没有时间戳/模块/级别的结构化记录
- 排查问题（尤其 agent 卡住、API 报错）时，日志能告诉「什么时候、在哪个模块、发生了什么」

用法（任何模块）：
    from research_assistant.infrastructure.logging import logger
    logger.info("构建 agent 完成")
    logger.error("调用失败: %s", e)
"""

# 导入 Python 标准库 logging：内置日志框架
import logging
# 导入 sys：输出到控制台（stderr）
import sys


# 配置根日志器的函数（项目启动时调用一次）
def setup_logging(level: int = logging.INFO) -> None:
    """初始化全局日志配置。

    参数:
        level: 日志级别（DEBUG/INFO/WARNING/ERROR），默认 INFO
    """
    # 获取根日志器（所有 logger 的祖先）
    root = logging.getLogger()
    # 设置级别：低于该级别的不输出
    root.setLevel(level)

    # 创建控制台处理器：日志输出到终端
    # StreamHandler(sys.stdout) = 输出到标准输出
    handler = logging.StreamHandler(sys.stdout)
    # 定义日志格式：时间 | 级别 | 模块:行号 | 消息
    # %(asctime)s=时间 %(levelname)s=级别 %(name)s=logger名 %(lineno)d=行号
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-7s | %(name)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    # 把格式器挂到处理器
    handler.setFormatter(formatter)

    # 清掉已有的处理器（避免重复添加，比如测试多次调用 setup）
    root.handlers.clear()
    # 添加我们的处理器
    root.addHandler(handler)


# 模块级便利函数：各模块直接 `from ...logging import get_logger`
def get_logger(name: str) -> logging.Logger:
    """获取指定名称的日志器。

    参数:
        name: 日志器名称（惯例用 __name__，即模块全名，日志里能看出是哪个模块）
    返回:
        配置好的 Logger 对象
    """
    # logging.getLogger 返回（或创建）指定名的日志器
    # 子日志器自动继承根日志器的配置（级别/处理器）
    return logging.getLogger(name)