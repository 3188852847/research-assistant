"""健康检查接口：GET /api/health。"""

# 导入 FastAPI 的 APIRouter
from fastapi import APIRouter

# 本模块的路由器
router = APIRouter(prefix="/api")


# GET /api/health：健康检查
# 启动后浏览器访问 http://127.0.0.1:8000/api/health 应返回 {"status": "ok"}
@router.get("/health")
def health() -> dict:
    """健康检查：确认服务活着。"""
    # 返回一个简单的 JSON
    return {"status": "ok"}