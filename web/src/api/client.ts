// 前端 API 客户端：封装所有后端调用
// 组件里不再直接 fetch，统一走这里——后端地址/错误处理改一处即可

// 导入后端数据类型
import type {ChatRequest, ChatResponse, ApproveRequest} from './types'

// 发送聊天消息
// 参数: message 用户输入, threadId 会话 ID
// 返回: 后端响应（可能含 pending 待审批操作）
export async function sendChat(message: string, threadId: string): Promise<ChatResponse> {
    // 组装请求体
    const body: ChatRequest = {message, thread_id: threadId}

    // 调用后端 /api/chat（Vite 代理转发到 FastAPI）
    const res = await fetch('/api/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(body),
    })
    // 解析响应为 ChatResponse 结构
    return await res.json() as ChatResponse
}

// 提交审批决策
// 参数: threadId 会话 ID, decisions 决策列表（approve/reject）
// 返回: 后端响应（可能是最终回复或新一轮 pending）
export async function sendApprove(threadId: string, decisions: { type: string }[]): Promise<ChatResponse> {
    // 组装请求体
    const body: ApproveRequest = {thread_id: threadId, decisions}

    // 调用后端 /api/approve
    const res = await fetch('/api/approve', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(body),
    })
    // 解析响应
    return await res.json() as ChatResponse
}


// 流式对话：调用 /api/chat/stream，逐条回调进度和最终回复
// 参数: message 用户输入, threadId 会话 ID
//       onProgress 进度回调（收到一条进度行时调用）
//       onDone 完成回调（收到最终回复时调用）
export async function sendChatStream(
    message: string,
    threadId: string,
    onProgress: (line: string) => void,
    onReasoning: (content: string) => void,   // ★ 新增：推理内容回调
    onDone: (reply: string) => void,
): Promise<void> {
    // 调用 SSE 接口（不 await 响应体，用流式读取）
    const res = await fetch('/api/chat/stream', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message, thread_id: threadId}),
    })

    // 检查响应是否 OK
    if (!res.ok || !res.body) {
        throw new Error('流式请求失败')
    }

    // 获取流读取器（ReadableStream 的标准读取方式）
    const reader = res.body.getReader()
    // TextDecoder 把字节流解码成文本（处理中文）
    const decoder = new TextDecoder()
    // 缓冲区：SSE 消息可能跨多个 chunk，需要拼接
    let buffer = ''

    // 循环读取直到流结束
    while (true) {
        // 读一块数据（done=true 表示流结束）
        const {done, value} = await reader.read()
        // 流结束：退出循环
        if (done) break

        // 把字节解码成文本，追加到缓冲区
        buffer += decoder.decode(value, {stream: true})

        // 按 SSE 分隔符（空行）拆出完整消息
        // SSE 消息格式：data: {...}\n\n（两条消息间有空行）
        const messages = buffer.split('\n\n')
        // 最后一段可能不完整（等下一个 chunk），留在缓冲区
        buffer = messages.pop() ?? ''

        // 逐条处理完整的消息
        for (const msg of messages) {
            // 只处理 data: 开头的行
            if (!msg.startsWith('data: ')) continue
            // 去掉 data: 前缀，解析 JSON
            const payload = JSON.parse(msg.slice(6))
            // 按类型分发：progress=进度行，reasoning=模型推理，done=最终回复
            if (payload.type === 'progress') {
                onProgress(payload.line)
            } else if (payload.type === 'reasoning') {
                onReasoning(payload.content)          // ★ 新增分支
            } else if (payload.type === 'done') {
                onDone(payload.reply)
            }
        }
    }
}