// 前后端共享的数据类型定义
// 集中放这里：将来前后端数据结构变化，只改这一个文件

// 待审操作的数据结构（来自后端 /api/chat 的 pending 字段）
export interface PendingItem {
    name: string          // 工具名（如 delete）
    args: Record<string, unknown>  // 工具参数
    allowed_decisions: string[]    // 允许的决策（approve/reject/edit）
}

// 消息的数据结构（前端聊天消息）
// role: 谁说的（user=用户 / agent=助手 / pending=待审批操作）
// content: 消息文本
// pending: 可选字段，仅当 role=pending 时存在，存待审操作列表
export interface Message {
    role: 'user' | 'agent' | 'pending'
    content: string
    pending?: PendingItem[]
    isProgress?: boolean      // ★ 是否为思考过程进度行（true=小字灰色样式）
    thinking?: boolean        // ★ 是否为「思考中」占位消息（显示跳动三点）
    reasoning?: string[]    // ★ 模型推理内容片段列表（折叠面板里展示）
}

// 聊天请求体（POST /api/chat）
export interface ChatRequest {
    message: string
    thread_id: string
}

// 聊天响应体（两种形态：reply 或 pending）
export interface ChatResponse {
    reply: string | null
    pending: PendingItem[] | null
}

// 审批请求体（POST /api/approve）
export interface ApproveRequest {
    thread_id: string
    decisions: { type: string }[]
}