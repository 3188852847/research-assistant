"""进度呈现：把 agent 执行过程翻译成人类可读的进度。

属于 presenters 呈现层——把核心执行翻译成用户可读形式。
CLI 和 Web 共用这里的翻译逻辑，各自的输出方式由调用方决定。
"""

# 导入类型：agent 事件流的类型提示用
from typing import Any, Iterator


def translate_event(event: dict) -> str | None:
    """把一个 stream 事件翻译成人类可读的进度行。

    参数:
        event: agent.stream() 产出的事件字典（如 {'model': {...}}）
    返回:
        进度文本；无法翻译的事件返回 None（跳过不显示）。
    """
    # 事件只有 1 个键（中间件名或阶段名），取出来判断
    for key, value in event.items():
        # ---- 模型事件：模型在思考或调用工具 ----
        if key == "model":
            # 取出消息列表（AIMessage）
            msgs = value.get("messages", [])
            if not msgs:
                return None
            # 取最后一条 AI 消息
            msg = msgs[-1]

            # 情况 1：模型发起了工具调用（tool_calls 非空）
            if msg.tool_calls:
                # 列出所有要调用的工具名
                names = ", ".join(tc["name"] for tc in msg.tool_calls)
                return f"🔧 调用工具: {names}"
            # 情况 2：模型有思考内容（reasoning）
            reasoning = getattr(msg, "reasoning_content", None)
            if reasoning:
                # 只显示思考的前 50 字（完整思考太长）
                return f"🤔 思考中: {reasoning[:50]}..."
            # 情况 3：普通输出（最终回复前的一步）
            return "💬 生成回复中..."

        # ---- 工具事件：工具执行完返回结果 ----
        if key == "tools":
            msgs = value.get("messages", [])
            if msgs:
                # 取工具名（ToolMessage 的 name 字段）
                name = getattr(msgs[-1], "name", "?")
                return f"✅ 工具 {name} 执行完成"
            return None

        # ---- 记忆加载 ----
        if key == "MemoryMiddleware.before_agent":
            return "📂 加载记忆..."

        # ---- 人机回环检查 ----
        if key == "HumanInTheLoopMiddleware.after_model":
            return None  # 中间检查点，跳过

        # ---- 其他中间件 ----
        if key == "PatchToolCallsMiddleware.before_agent":
            return "🚀 开始处理..."

    # 不认识的事件，跳过
    return None


def stream_with_progress(agent, input_data: dict, config: dict) -> Iterator[str]:
    """流式执行 agent，逐段产出进度文本。

    参数:
        agent: deepagents 构建的 agent
        input_data: invoke 的输入（{"messages": [...]}）
        config: 会话配置（{"configurable": {"thread_id": ...}}）
    产出:
        进度文本（每步一条，如「🤔 思考中: ...」）
    """
    # agent.stream() 逐步产出事件
    for event in agent.stream(input_data, config=config):
        # 把事件翻译成进度行
        line = translate_event(event)
        # 能翻译的才产出（None 跳过）
        if line:
            yield line