"""FastAPI 服务入口：启动 Web 服务，暴露对话接口。

启动方式：uv run uvicorn research_assistant.main:app --reload
"""

# 导入 FastAPI：Web 框架本体
# app 对象是 FastAPI 应用的核心，uvicorn 加载它来运行服务
from fastapi import FastAPI

# 导入路由层（api/routes.py 里的 router）
# 对话接口 /api/chat、健康检查 /api/health 都在 router 里定义
from research_assistant.api.routes import router




# 创建 FastAPI 应用实例
app = FastAPI(
    title="research-assistant",
    description="个人研究助手 API（DeepAgents）",
) # title/description: 显示在 Swagger 文档（/docs）页面的标题和说明，方便你在浏览器里识别这是哪个服务

# 把路由注册进应用
app.include_router(router) # 这样 router 里所有以 /api 开头的接口都挂到了 app 上


# Python 的入口约定：只有直接运行本文件时（python -m research_assistant.main）才执行
# 用 uvicorn 命令行启动时（uvicorn research_assistant.main:app）不会走到这里
if __name__ == "__main__":
    # 导入 uvicorn（ASGI 服务器，让 FastAPI 跑起来的进程）
    import uvicorn

    # 启动服务
    # "research_assistant.main:app"：告诉 uvicorn 去哪里找 app 对象（模块:变量名）
    # host="127.0.0.1"：只在本机监听（不暴露到局域网，安全）
    # port=8000：HTTP 端口
    # reload=True：代码改了自动重启，开发期方便
    uvicorn.run("research_assistant.main:app", host="127.0.0.1", port=8000, reload=True)