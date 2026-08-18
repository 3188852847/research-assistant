// 对话接口封装：chat（普通）、approve（审批）、stream（流式）

// 导入基础请求
import { request } from './client'
// 导入流式事件类型
import type { ChatResponse, StreamEvent } from './types'

// 普通对话（POST /api/chat）
// params: message 用户输入, threadId 会话 ID
// 返回: 后端响应（正常回复或待审批）
export async function sendChat(message: string, threadId: string): Promise<ChatResponse> {
  return await request<ChatResponse>('/api/chat', {
    method: 'POST',
    body: { message, thread_id: threadId },
  })
}

// 审批（POST /api/approve）—— 人机回环
// params: threadId 会话 ID, decisions 决策列表
export async function sendApprove(
  threadId: string,
  decisions: { type: string }[],
): Promise<ChatResponse> {
  return await request<ChatResponse>('/api/approve', {
    method: 'POST',
    body: { thread_id: threadId, decisions },
  })
}

// 流式对话（POST /api/chat/stream）—— 逐条推事件，实时回调
// params: message, threadId, 三个回调（进度/推理/完成）
// onEvent: 预留的通用事件回调（未来 AI 跳页 navigate 也走它）
export async function sendChatStream(
  message: string,
  threadId: string,
  onProgress: (line: string) => void,
  onReasoning: (content: string) => void,
  onDone: (reply: string) => void,
  onEvent?: (event: StreamEvent) => void,   // 预留：处理所有流事件（含未来 navigate）
): Promise<void> {
  // 发 SSE 请求
  const res = await fetch('/api/chat/stream', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, thread_id: threadId }),
  })

  // 检查响应
  if (!res.ok || !res.body) {
    throw new Error('流式请求失败')
  }

  // 流式读取：ReadableStream 逐块读
  const reader = res.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''

  // 循环读直到流结束
  while (true) {
    const { done, value } = await reader.read()
    if (done) break

    // 解码 + 拼缓冲
    buffer += decoder.decode(value, { stream: true })

    // 按 SSE 分隔符拆消息（空行分隔）
    const messages = buffer.split('\n\n')
    buffer = messages.pop() ?? ''   // 最后一段可能不完整，留缓冲区

    // 逐条处理
    for (const msg of messages) {
      // 只处理 data: 开头
      if (!msg.startsWith('data: ')) continue
      // 解析 JSON
      const payload = JSON.parse(msg.slice(6)) as StreamEvent

      // 先给通用事件回调（预留 AI 跳页等）
      onEvent?.(payload)

      // 按类型分发到具体回调
      switch (payload.type) {
        case 'progress':
          onProgress(payload.line)
          break
        case 'reasoning':
          onReasoning(payload.content)
          break
        case 'done':
          onDone(payload.reply)
          break
        // navigate 等预留类型：只走 onEvent，不在这里处理
      }
    }
  }
}
