"""FastAPI 服务入口：启动 Web 服务，暴露对话接口。

启动方式：uv run uvicorn research_assistant.main:app --reload
"""

# 导入 FastAPI：Web 框架本体
# app 对象是 FastAPI 应用的核心，uvicorn 加载它来运行服务
from fastapi import FastAPI
# 导入 FastAPI 的静态文件托管
from fastapi.staticfiles import StaticFiles
# 导入 pathlib 的 Path：跨平台路径处理
from pathlib import Path

# 导入路由层（api/ 包汇总的 router）
from research_assistant.api import router


# 计算前端构建产物目录（绝对路径，不依赖启动目录）
# main.py 在 src/research_assistant/ 下：
#   parent = src/research_assistant
#   parent.parent = src
#   parent.parent.parent = 项目根（web/ 在这里）
_PROJECT_ROOT = Path(__file__).parent.parent.parent
WEB_DIST = _PROJECT_ROOT / "web" / "dist"


# 创建 FastAPI 应用的工厂函数
# 抽成函数的好处：可测试（测试里能反复创建干净实例）、可配置
def create_app() -> FastAPI:
    """构建并返回 FastAPI 应用实例。"""
    # 创建 FastAPI 应用实例
    # title/description: 显示在 Swagger 文档（/docs）页面的标题和说明
    app = FastAPI(
        title="research-assistant",
        description="个人研究助手 API（DeepAgents）",
    )

    # 把路由注册进应用（/api/chat、/api/approve、/api/health）
    app.include_router(router)

    # 挂载前端静态文件（M6 生产模式）
    # StaticFiles(html=True) 会自动伺服 index.html
    # 注意：必须在所有 API 路由注册之后挂载（/ 是兜底路径，先挂会拦截一切）
    # app.mount("/", StaticFiles(directory=str(WEB_DIST), html=True), name="static")

    return app


# 模块级创建 app 实例（uvicorn 命令行加载的就是这个）
app = create_app()


# Python 的入口约定：只有直接运行本文件时才执行
if __name__ == "__main__":
    # 导入 uvicorn（ASGI 服务器）
    import uvicorn

    # 启动服务（host/port/reload）
    uvicorn.run("research_assistant.main:app", host="127.0.0.1", port=8000, reload=True)