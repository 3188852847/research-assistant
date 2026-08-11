"""配置单例：全局唯一的 Settings 实例。

配置读取成本低（读 .env），但「全局一份」的好处是：
- 所有模块拿到同一个配置对象，不会各读各的
- 未来配置可能来自数据库/远程（成本高），单例模式直接适用
- 与 get_agent() 的 lazy 模式一致，风格统一
"""

# 导入配置加载函数和 Settings 类型
from research_assistant.core.config import load_settings, Settings

# lazy 构建的配置单例
_settings = None


def get_settings() -> Settings:
    """获取全局唯一的配置实例（lazy：首次调用时加载，之后复用）。"""
    # 声明使用模块级变量
    global _settings
    # 首次调用时加载，之后直接返回
    if _settings is None:
        _settings = load_settings()
    return _settings


# 兼容：模块级直接暴露（和 deps.agent 一致的模式）
settings = get_settings()