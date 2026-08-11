// 聊天组件：编排层——持有聊天状态，调 api 层，组合子组件
// 不再直接 fetch（已移到 api/client.ts）、不再渲染消息细节（已拆 MessageList/PendingCard）

// 导入 React Hooks：useState（状态）
import { useState, type ChangeEvent, type KeyboardEvent } from 'react'

// 导入 api 层（后端调用封装）
import { sendChat, sendApprove } from '../api/client'
// 导入数据类型
import type { Message } from '../api/types'
// 导入消息列表组件
import MessageList from './MessageList'

// 聊天组件：接收 threadId（会话管理由父组件负责）
export default function Chat({ threadId }: {
  threadId: string
}) {
  // messages: 消息列表状态
  const [messages, setMessages] = useState<Message[]>([])
  // input: 输入框当前内容
  const [input, setInput] = useState('')
  // loading: 是否正在等待回复
  const [loading, setLoading] = useState(false)

  // 发送消息给后端
  async function sendMessage() {
    // 空输入不发送
    if (!input.trim() || loading) return

    // 把用户消息加入列表、清空输入、进入加载态
    const userMsg: Message = { role: 'user', content: input }
    setMessages(prev => [...prev, userMsg])
    setInput('')
    setLoading(true)

    try {
      // 调 api 层（不再直接 fetch）
      const data = await sendChat(input, threadId)

      // 判断返回形态：pending（待审批）还是 reply（正常回复）
      if (data.pending) {
        setMessages(prev => [...prev, {
          role: 'pending',
          content: '以下操作需要你的审批：',
          pending: data.pending ?? undefined,
        }])
      } else {
        setMessages(prev => [...prev, { role: 'agent', content: data.reply ?? '' }])
      }
    } catch (err) {
      // 请求失败
      console.error('请求失败:', err)
      setMessages(prev => [...prev, { role: 'agent', content: '⚠️ 请求失败，请检查后端是否启动' }])
    } finally {
      setLoading(false)
    }
  }

  // 提交审批决策（批准/拒绝）
  async function handleApprove(decision: 'approve' | 'reject', pendingMsgIndex: number) {
    // 进入加载态
    setLoading(true)
    try {
      // 调 api 层（审批接口）
      const data = await sendApprove(threadId, [{ type: decision }])

      // 把已审批的 pending 消息替换成占位文本
      setMessages(prev => prev.map((m, i) =>
        i === pendingMsgIndex ? { role: 'agent', content: '(审批已提交)' } : m
      ))

      // 处理审批后的结果
      if (data.pending) {
        // 又有新的待审操作
        setMessages(prev => [...prev, {
          role: 'pending',
          content: '还有操作需要你的审批：',
          pending: data.pending ?? undefined,
        }])
      } else {
        // 审批完成，显示最终回复
        setMessages(prev => [...prev, { role: 'agent', content: data.reply ?? '' }])
      }
    } catch (err) {
      console.error('审批失败:', err)
      setMessages(prev => [...prev, { role: 'agent', content: '⚠️ 审批请求失败' }])
    } finally {
      setLoading(false)
    }
  }

  // 输入框 Enter 键发送
  function handleKeyDown(e: KeyboardEvent<HTMLInputElement>) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="chat">
      {/* 消息列表（子组件，传消息数组 + 审批回调） */}
      <MessageList
        messages={messages}
        loading={loading}
        onApprove={handleApprove}
      />

      {/* 输入区：输入框 + 发送按钮 */}
      <div className="input-area">
        <input
          value={input}
          onChange={(e: ChangeEvent<HTMLInputElement>) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="输入消息，Enter 发送"
          disabled={loading}
        />
        <button onClick={sendMessage} disabled={loading || !input.trim()}>
          {loading ? '思考中...' : '发送'}
        </button>
      </div>
    </div>
  )
}