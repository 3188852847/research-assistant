"""配置加载：从 .env 读取 DeepSeek 配置，集中校验。

所有模块都从这里获取配置，不要在别处直接读环境变量。
"""

from dataclasses import dataclass

from dotenv import load_dotenv
import os


@dataclass(frozen=True)
class Settings:
    """应用配置。frozen=True 表示不可变，防止运行时被意外修改。"""

    api_key: str
    base_url: str
    model: str


def load_settings() -> Settings:
    """加载 .env 并构造 Settings。

    缺失 API key 时抛出带引导信息的 ValueError，而不是静默失败。
    """
    # 从项目根目录加载 .env（dotenv 会从当前目录向上找，这里显式指定更稳）
    load_dotenv()

    api_key = os.getenv("DEEPSEEK_API_KEY", "").strip()
    base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com").strip()
    model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat").strip()

    if not api_key:
        raise ValueError(
            "未找到 DEEPSEEK_API_KEY。\n"
            "请把项目根目录的 .env.example 复制为 .env，"
            "并在其中填入你的 DeepSeek API key。"
        )

    return Settings(api_key=api_key, base_url=base_url, model=model)


def settings_summary(settings: Settings) -> str:
    """打印配置概览（不泄露 key 本身，只显示掩码）。"""
    masked = f"{settings.api_key[:4]}...{settings.api_key[-4:]}" if settings.api_key else "(空)"
    return (
        f"API Key:   {masked}\n"
        f"Base URL:  {settings.base_url}\n"
        f"Model:     {settings.model}"
    )