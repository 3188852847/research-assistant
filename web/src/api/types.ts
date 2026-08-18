// 前后端共享的数据类型定义
// 集中放这里：前后端数据结构变化时只改这一个文件

// 待审操作（人机回环，来自 /api/chat 的 pending）
export interface PendingItem {
  name: string                 // 工具名（如 delete）
  args: Record<string, unknown> // 工具参数
  allowed_decisions: string[]  // 允许的决策（approve/reject/edit）
}

// 对话请求体（POST /api/chat）
export interface ChatRequest {
  message: string
  thread_id: string
}

// 聊天响应体（两种形态：正常回复 或 待审批）
export interface ChatResponse {
  reply: string | null
  pending: PendingItem[] | null
}

// 审批请求体（POST /api/approve）
export interface ApproveRequest {
  thread_id: string
  decisions: { type: string }[]
}

// SSE 流式事件（/api/chat/stream 推送的消息），后端 JSON 里带 type
export type StreamEvent =
  | { type: 'progress'; line: string }        // 进度行（步骤描述）
  | { type: 'reasoning'; content: string }     // 模型推理内容
  | { type: 'done'; reply: string }            // 最终回复
  | { type: 'navigate'; to: string }           // AI 跳页事件（④ 预留，后置）
