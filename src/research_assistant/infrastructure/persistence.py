"""持久化：SQLite 检查点，让对话历史跨进程存活。

为什么需要：
- MemorySaver（内存）在 uvicorn 重启后会话全丢——像失忆
- SqliteSaver 把检查点（对话状态）存到磁盘文件，重启后仍在

注意：SqliteSaver 必须用 with 打开（from_conn_string 返回上下文管理器），
所以这里在模块级打开一次并保持，整个进程生命周期复用。
"""

# 导入 Path：定位持久化文件路径
from pathlib import Path
# 导入 sqlite3：Python 内置 SQLite 驱动（手动建连接）
import sqlite3
# 导入 SqliteSaver：langgraph 的 SQLite 检查点
from langgraph.checkpoint.sqlite import SqliteSaver


# 持久化文件路径：项目根/data/checkpoints.sqlite（不依赖启动目录）
_PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
# 数据目录：项目根/data（集中放运行时生成的数据）
DATA_DIR = _PROJECT_ROOT / "data"
# 检查点数据库文件
DB_PATH = DATA_DIR / "checkpoints.sqlite"


def get_checkpointer() -> SqliteSaver:
    """获取全局唯一的 SQLite 检查点（进程生命周期内复用）。

    实现：手动创建 sqlite3 连接 + SqliteSaver(conn) 构造，
    绕开 from_conn_string 的上下文管理器问题（那个必须 with 用）。
    """
    # 确保数据目录存在
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # 手动创建 SQLite 连接（check_same_thread=False：允许跨线程使用，
    # FastAPI 多线程请求会共享这个检查点）
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)

    # 用连接构造 SqliteSaver（构造器直接接受连接对象，返回真 saver）
    # 这绕开了 from_conn_string 的 with 要求
    saver = SqliteSaver(conn)

    # 返回检查点实例
    return saver