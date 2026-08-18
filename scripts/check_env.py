"""环境检查：启动前验证项目环境是否就绪。

检查项：
1. Python 依赖（核心包能否 import）
2. .env 配置（API key 是否齐全）
3. 目录结构（关键路径是否存在）
4. 前端依赖（web/node_modules 是否安装）

用法：uv run python scripts/check_env.py
"""

# 导入 sys：退出码控制（检查失败返回非 0）
import sys
# 导入 Path：路径检查
from pathlib import Path


# ---- 项目根路径（不依赖启动目录）----
# scripts/check_env.py → parent=scripts → parent.parent=项目根
PROJECT_ROOT = Path(__file__).parent.parent


# 检查结果计数器
_errors = []   # 错误列表（检查失败项）
_warns = []    # 警告列表（不致命但值得注意）


# 记录错误的辅助函数
def error(msg: str) -> None:
    """记录一条错误。"""
    _errors.append(msg)


# 记录警告的辅助函数
def warn(msg: str) -> None:
    """记录一条警告。"""
    _warns.append(msg)


# ---- 检查 1：Python 依赖 ----
def check_dependencies() -> None:
    """检查核心 Python 包能否 import。"""
    # 必需的核心包清单
    required = [
        "deepagents",       # agent 框架
        "fastapi",          # Web 后端
        "uvicorn",          # ASGI 服务器
        "langchain_deepseek",  # DeepSeek 接入（容易漏装！）
        "tavily",           # 联网检索
        "pypdf",            # PDF 读取
        "dotenv",           # .env 加载
    ]
    # 逐个尝试 import
    for pkg in required:
        try:
            # __import__ 动态导入包名
            __import__(pkg)
        except ImportError:
            # import 失败 = 没装
            error(f"缺少依赖: {pkg}（运行 uv add {pkg} 安装）")


# ---- 检查 2：.env 配置 ----
def check_env() -> None:
    """检查 .env 是否存在、key 是否齐全。"""
    # .env 文件路径
    env_file = PROJECT_ROOT / ".env"
    # .env 不存在
    if not env_file.exists():
        error("缺少 .env 文件（复制 .env.example 为 .env 并填入 key）")
        return

    # 读取 .env 内容（只检查 key 名是否存在，不读值）
    content = env_file.read_text(encoding="utf-8")
    # 必需的配置项
    required_keys = ["DEEPSEEK_API_KEY", "DEEPSEEK_BASE_URL", "DEEPSEEK_MODEL"]
    # 逐个检查
    for key in required_keys:
        # 检查 key 是否出现在 .env 且不是空值
        # 简单判断：key= 后跟非空内容
        lines = [l for l in content.splitlines() if l.strip() and not l.strip().startswith("#")]
        if not any(l.strip().startswith(f"{key}=") and l.strip().split("=", 1)[1].strip() for l in lines):
            error(f".env 缺少配置: {key}")


# ---- 检查 3：目录结构 ----
def check_structure() -> None:
    """检查关键路径是否存在。"""
    # 关键路径清单（相对项目根）
    required_paths = [
        "src/research_assistant/main.py",          # 后端入口
        "src/research_assistant/core/agent.py",    # agent 构建
        "web/package.json",                         # 前端项目
        "web/src/App.tsx",                          # 前端源码
        "src/research_assistant/core/memory/AGENTS.md",  # 记忆文件
    ]
    # 逐个检查
    for rel in required_paths:
        if not (PROJECT_ROOT / rel).exists():
            error(f"缺少路径: {rel}")


# ---- 检查 4：前端依赖 ----
def check_frontend() -> None:
    """检查前端 node_modules 是否安装。"""
    # node_modules 目录
    nm = PROJECT_ROOT / "web" / "node_modules"
    if not nm.exists():
        warn("web/node_modules 未安装（运行 cd web && npm install）")


# ---- 主检查函数 ----
def main() -> int:
    """执行全部检查，返回退出码（0=通过，1=有错误）。"""
    print("=== research-assistant 环境检查 ===\n")

    # 依次执行四组检查
    check_dependencies()
    check_env()
    check_structure()
    check_frontend()

    # 输出警告
    if _warns:
        print("⚠️ 警告：")
        for w in _warns:
            print(f"  - {w}")
        print()

    # 输出错误
    if _errors:
        print("❌ 错误（需修复）：")
        for e in _errors:
            print(f"  - {e}")
        print(f"\n共 {len(_errors)} 个错误，请先修复再启动。")
        # 有错误：返回退出码 1
        return 1

    # 全部通过
    print("✅ 环境检查通过，可以启动！")
    # 通过：返回退出码 0
    return 0


# 入口约定：直接运行本文件时执行
if __name__ == "__main__":
    # 执行检查，用退出码退出
    sys.exit(main())