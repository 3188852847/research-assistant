// 消息列表：渲染用户/AI 消息 + 思考折叠面板（模型推理）+ 审批卡片
// photo 纯展示组件，数据来自 useChat

import { Collapse, Tag } from 'antd'
import type { Msg } from '../../hooks/useChat'
import PendingCard from './PendingCard'

// props
interface MessageListProps {
  messages: Msg[]                          // 消息列表
  progress: string[]                       // 思考进度行（最新一轮）
  reasoning: string[]                      // 模型推理片段（最新一轮）
  thinking: boolean                        // 是否思考中
  loading: boolean                         // 请求中
  onApprove: (decision: 'approve' | 'reject', pendingIndex: number) => void
}

// 消息列表组件
export default function MessageList({
  messages, progress, reasoning, thinking, loading, onApprove,
}: MessageListProps) {
  return (
    <div style={{ flex: 1, overflowY: 'auto', padding: 24, display: 'flex', flexDirection: 'column', gap: 16 }}>
      {/* 遍历消息 */}
      {messages.map((msg, i) => (
        // 普通消息：用户靠右蓝绿底，agent 靠左玻璃卡
        <div key={i} style={{
          alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
          maxWidth: '75%',
        }}>
          <div style={{
            padding: '10px 14px',
            borderRadius: 'var(--radius-md)',
            background: msg.role === 'user' ? 'rgba(1,177,73,0.2)' : 'var(--glass-bg)',
            border: msg.role === 'user' ? '1px solid rgba(1,177,73,0.3)' : '1px solid var(--glass-border)',
            color: 'var(--text-1)',
            whiteSpace: 'pre-wrap',
          }}>
            {/* agent 消息带标签 */}
            {msg.role === 'agent' && (
              <Tag color="green" style={{ marginBottom: 4 }}>assistant</Tag>
            )}
            <div>{msg.content}</div>
          </div>

          {/* pending 消息：渲染审批卡片列表 */}
          {msg.pending && (
            <div>
              {msg.pending.map((p, j) => (
                <PendingCard key={j} item={p} loading={loading} onDecision={(d) => onApprove(d, i)} />
              ))}
            </div>
          )}
        </div>
      ))}

      {/* 思考过程折叠面板（最新一轮，有内容才显示） */}
      {(progress.length > 0 || reasoning.length > 0 || thinking) && (
        <Collapse
          ghost   // 无边框透明（玻璃风）
          defaultActiveKey={thinking ? ['t'] : []}   // 思考中默认展开，完成收起
          items={[{
            key: 't',
            // 标题：思考中 vs 已思考
            label: (
              <span style={{ color: 'var(--text-2)' }}>
                {thinking ? '💭 思考中...' : '💭 已思考（点击展开）'}
              </span>
            ),
            // 展开内容：推理 + 进度行
            children: (
              <div style={{ fontSize: 12, color: 'var(--text-2)' }}>
                {/* 模型推理（可选） */}
                {reasoning.length > 0 && (
                  <div style={{
                    background: 'var(--glass-bg)', borderLeft: '3px solid var(--accent)',
                    padding: '8px 12px', marginBottom: 8, whiteSpace: 'pre-wrap',
                    fontFamily: 'monospace',
                  }}>
                    {reasoning.map((r, idx) => <div key={idx} style={{ marginBottom: 2 }}>{r}</div>)}
                  </div>
                )}
                {/* 进度行 */}
                {progress.map((line, idx) => (
                  <div key={idx} style={{ padding: '2px 0' }}>{line}</div>
                ))}
              </div>
            ),
          }]}
        />
      )}
    </div>
  )
}
