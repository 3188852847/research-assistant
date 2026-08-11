"""请求追踪与 token 统计。

为什么需要：
- 每次 agent 调用都产生 token 消耗（花钱），README 风险项提到要「评估用量」
- 追踪 trace_id：一次对话的完整链路能在日志里串起来

用法：
    from research_assistant.infrastructure.tracing import record_usage, TraceContext
"""

# 导入时间戳（记录调用时间）
import time
# 导入 dataclass（数据类：轻量结构）
from dataclasses import dataclass, field
# 导入 uuid（生成 trace_id）
import uuid


# 单次模型调用的用量记录
@dataclass
class UsageRecord:
    """一次 agent 调用的 token 用量统计。

    属性:
        trace_id: 追踪 ID（一次对话一个，串起所有调用）
        input_tokens: 输入 token 数
        output_tokens: 输出 token 数
        total_tokens: 总 token 数
        model: 使用的模型名
        timestamp: 调用时间（Unix 时间戳）
    """
    trace_id: str                      # 追踪 ID
    input_tokens: int = 0              # 输入 token
    output_tokens: int = 0             # 输出 token
    total_tokens: int = 0              # 总 token
    model: str = ""                    # 模型名
    timestamp: float = field(default_factory=time.time)  # 记录时间


# 从 agent 响应里提取 token 用量
def extract_usage(result, trace_id: str) -> UsageRecord:
    """从 agent.invoke() 的结果里提取 token 用量。

    参数:
        result: agent.invoke 的返回（dict，含 messages）
        trace_id: 本次对话的追踪 ID
    返回:
        UsageRecord（提取不到就返回全 0 的记录）
    """
    # 遍历消息，找带 token_usage 的 AI 消息
    messages = result.get("messages", []) if isinstance(result, dict) else getattr(result, "value", {}).get("messages", [])
    for msg in messages:
        # 找 AI 消息（模型输出才有 token 统计）
        if getattr(msg, "type", "") == "ai" or type(msg).__name__ == "AIMessage":
            # 从 response_metadata 里取 token_usage
            meta = getattr(msg, "response_metadata", {}) or {}
            usage = meta.get("token_usage", {}) or {}
            # 模型名
            model = meta.get("model_name", "")
            # 构造用量记录
            return UsageRecord(
                trace_id=trace_id,
                input_tokens=usage.get("prompt_tokens", 0),
                output_tokens=usage.get("completion_tokens", 0),
                total_tokens=usage.get("total_tokens", 0),
                model=model,
            )
    # 没找到带 token 信息的消息：返回空记录
    return UsageRecord(trace_id=trace_id)


# 追踪上下文：一次对话的追踪信息
@dataclass
class TraceContext:
    """对话追踪上下文。

    属性:
        trace_id: 唯一追踪 ID（新建会话时生成）
    """
    trace_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])

    # 打印追踪信息的方法
    def log_usage(self, usage: UsageRecord, logger) -> None:
        """把一次调用的用量写入日志。

        参数:
            usage: 用量记录
            logger: 日志器（infrastructure.logging.get_logger）
        """
        # 输出一行可读的用量日志
        logger.info(
            "[%s] token 用量: 输入 %d / 输出 %d / 总计 %d (model=%s)",
            self.trace_id,
            usage.input_tokens,
            usage.output_tokens,
            usage.total_tokens,
            usage.model,
        )