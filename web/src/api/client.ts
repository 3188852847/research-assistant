// 前端 API 客户端：封装所有后端调用
// 组件里不再直接 fetch，统一走这里——后端地址/错误处理改一处即可

// 导入后端数据类型
import type { ChatRequest, ChatResponse, ApproveRequest } from './types'

// 发送聊天消息
// 参数: message 用户输入, threadId 会话 ID
// 返回: 后端响应（可能含 pending 待审批操作）
export async function sendChat(message: string, threadId: string): Promise<ChatResponse> {
  // 组装请求体
  const body: ChatRequest = { message, thread_id: threadId }

  // 调用后端 /api/chat（Vite 代理转发到 FastAPI）
  const res = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
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
  const body: ApproveRequest = { thread_id: threadId, decisions }

  // 调用后端 /api/approve
  const res = await fetch('/api/approve', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  // 解析响应
  return await res.json() as ChatResponse
}