"""呈现层：把核心执行翻译成用户可读形式。

与核心逻辑解耦——agent 怎么跑由 core/ 负责，
怎么把过程/结果「呈现」给用户由本包负责。

成员：
- progress.py：思考过程可视化（事件流 → 进度文本）

将来：
- sse.py：Web 流式输出（SSE 格式）
- errors.py：错误信息友好化
"""

# 导出进度可视化函数
from research_assistant.core.presenters.progress import translate_event, stream_with_progress

from research_assistant.core.presenters.progress import translate_event, stream_with_progress, stream_agent

# 公共出口
__all__ = ["translate_event", "stream_with_progress", "stream_agent"]
