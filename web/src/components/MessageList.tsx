// 消息列表组件：渲染所有消息（用户/agent/pending）
// 纯展示组件：接收消息数组 + 审批回调，不持有聊天状态

import type { Message } from '../api/types'
// 导入审批卡片组件
import PendingCard from './PendingCard'

// 组件 props 定义
interface MessageListProps {
  messages: Message[]          // 消息列表
  loading: boolean             // 是否正在请求
  onApprove: (decision: 'approve' | 'reject', pendingIndex: number) => void  // 审批回调（带消息索引）
}

// 消息列表组件
export default function MessageList({ messages, loading, onApprove }: MessageListProps) {
  return (
    // 消息列表容器（可滚动）
    <div className="messages">
      {/* 遍历渲染每条消息 */}
      {messages.map((msg, i) => (
        // key 用索引（本项目消息不删除，安全）
        <div key={i} className={`message ${msg.role}`}>
          {/* 消息文本气泡 */}
          <div className="bubble">{msg.content}</div>

          {/* pending 消息：渲染审批卡片列表 */}
          {msg.pending && (
            <div className="pending-list">
              {/* 每个待审操作一个卡片 */}
              {msg.pending.map((p, j) => (
                // 卡片组件：数据 + 回调（onApprove 携带消息索引 i）
                <PendingCard
                  key={j}
                  item={p}
                  loading={loading}
                  onDecision={(d) => onApprove(d, i)}
                />
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  )
}