// 消息列表组件：渲染所有消息（antd 版）
// 纯展示：接收消息数组 + 审批回调

// 导入 antd 组件：Tag（角色标签）
import {Tag} from 'antd'
// 导入类型
import type {Message} from '../api/types'
// 导入审批卡片
import PendingCard from './PendingCard'

// 组件 props
interface MessageListProps {
    messages: Message[]
    loading: boolean
    onApprove: (decision: 'approve' | 'reject', pendingIndex: number) => void
}

// 消息列表组件
export default function MessageList({messages, loading, onApprove}: MessageListProps) {
    return (
        // 消息容器：纵向排列、可滚动、留白
        <div style={{flex: 1, overflowY: 'auto', padding: 20, display: 'flex', flexDirection: 'column', gap: 12}}>
            {/* 遍历消息 */}
            {messages.map((msg, i) => (
                // 思考中占位：显示跳动三点（打字指示器）
                msg.thinking ? (
                        <div key={i} style={{
                            alignSelf: 'flex-start',
                            display: 'flex', alignItems: 'center', gap: 6,
                            padding: '10px 4px',
                        }}>
                            {/* 三个跳动圆点（CSS 动画） */}
                            <span className="typing-dot"/>
                            <span className="typing-dot" style={{animationDelay: '0.2s'}}/>
                            <span className="typing-dot" style={{animationDelay: '0.4s'}}/>
                            <span style={{fontSize: 12, color: '#999', marginLeft: 4}}>正在思考...</span>
                        </div>
                    ) :
                    // 进度行：特殊的小字灰色样式（思考过程日志）
                    msg.isProgress ? (
                        // 进度行容器：靠左、整行、小字
                        <div key={i} style={{
                            alignSelf: 'flex-start',
                            fontSize: 12,               // 小字
                            color: '#999',              // 灰色
                            fontFamily: 'monospace',    // 等宽字体（日志感）
                            padding: '2px 0',
                            whiteSpace: 'pre-wrap',
                        }}>
                            {/* 进度内容（行内已有图标 🚀🤔🔧 等） */}
                            {msg.content}
                        </div>
                    ) : (
                        // 正常消息（用户/agent 气泡）
                        <div key={i} style={{
                            alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
                            maxWidth: '75%',
                        }}>
                            <div style={{
                                padding: '10px 14px',
                                borderRadius: 12,
                                background: msg.role === 'user' ? '#1677ff' : msg.role === 'pending' ? '#fffbe6' : '#f5f5f5',
                                color: msg.role === 'user' ? '#fff' : 'inherit',
                                whiteSpace: 'pre-wrap',
                            }}>
                                {msg.role === 'agent' && (
                                    <Tag color="blue" style={{marginBottom: 4}}>assistant</Tag>
                                )}
                                <div>{msg.content}</div>
                            </div>
                            {msg.pending && (
                                <div>
                                    {msg.pending.map((p, j) => (
                                        <PendingCard key={j} item={p} loading={loading}
                                                     onDecision={(d) => onApprove(d, i)}/>
                                    ))}
                                </div>
                            )}
                        </div>
                    )
            ))}
        </div>
    )
}