// 聊天界面组件：消息流 + 输入框 + 发送
// 这是 React 函数组件——一个返回 JSX 的普通函数

// 导入 React 的 Hooks：useState（状态）、useRef（引用 DOM）
// 类型：FormEvent（表单事件）、ChangeEvent（输入框事件）
import { useState, type ChangeEvent, type KeyboardEvent } from 'react'

// 定义消息的数据结构（TypeScript 接口）
// role: 谁说的（user=用户 / agent=助手 / pending=待审批操作）
// content: 消息文本
// pending: 可选字段，仅当 role=pending 时存在，存待审操作列表
interface Message {
  role: 'user' | 'agent' | 'pending'
  content: string
  pending?: PendingItem[]
}

// 待审操作的数据结构（来自后端 /api/chat 的 pending 字段）
interface PendingItem {
  name: string          // 工具名（如 delete）
  args: Record<string, unknown>  // 工具参数
  allowed_decisions: string[]    // 允许的决策（approve/reject/edit）
}

// 聊天组件：接收 threadId 和 onThreadChange 两个 props（会话管理由父组件负责）
export default function Chat({ threadId }: {
  threadId: string
}) {
  // messages: 消息列表状态，初始为空数组
  const [messages, setMessages] = useState<Message[]>([])
  // input: 输入框当前内容
  const [input, setInput] = useState('')
  // loading: 是否正在等待 agent 回复（发送后禁用输入框）
  const [loading, setLoading] = useState(false)

  // 发送消息给后端
  async function sendMessage() {
    // 空输入不发送
    if (!input.trim() || loading) return

    // 把用户消息加入列表
    const userMsg: Message = { role: 'user', content: input }
    setMessages(prev => [...prev, userMsg])
    // 清空输入框、进入加载态
    setInput('')
    setLoading(true)

    try {
      // 调用后端 /api/chat
      // fetch 是浏览器原生 API，发 HTTP 请求；/api 前缀会被 Vite 代理转发到后端
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input, thread_id: threadId }),
      })
      const data = await res.json()

      // 判断返回形态：pending（待审批）还是 reply（正常回复）
      if (data.pending) {
        // 有待审操作：把它作为一条 pending 消息加入列表（审批卡片由阶段 4 渲染）
        setMessages(prev => [...prev, {
          role: 'pending',
          content: '以下操作需要你的审批：',
          pending: data.pending,
        }])
      } else {
        // 正常回复：加入消息列表
        setMessages(prev => [...prev, { role: 'agent', content: data.reply }])
      }
    } catch (err) {
      // 请求失败：显示错误
      console.error('请求失败:', err)
      setMessages(prev => [...prev, { role: 'agent', content: '⚠️ 请求失败，请检查后端是否启动' }])
    } finally {
      // 无论成功失败，结束加载态
      setLoading(false)
    }
  }

    // 提交审批决策：批准或拒绝待审操作，恢复 agent 执行
  async function sendDecision(decisions: { type: string }[], pendingMsgIndex: number) {
    // 进入加载态（禁用界面）
    setLoading(true)
    try {
      // 调用后端 /api/approve（审批接口，M5 写的）
      const res = await fetch('/api/approve', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ thread_id: threadId, decisions }),
      })
      const data = await res.json()

      // 移除已审批的 pending 消息（用索引定位，替换成占位文本）
      setMessages(prev => prev.map((m, i) =>
        i === pendingMsgIndex ? { role: 'agent', content: '(审批已提交)' } : m
      ))

      // 处理审批后的结果：可能是回复，也可能又一轮 pending
      if (data.pending) {
        // 又有新的待审操作（多个操作逐一审批）
        setMessages(prev => [...prev, {
          role: 'pending',
          content: '还有操作需要你的审批：',
          pending: data.pending,
        }])
      } else {
        // 审批完成，显示最终回复
        setMessages(prev => [...prev, { role: 'agent', content: data.reply }])
      }
    } catch (err) {
      console.error('审批失败:', err)
      setMessages(prev => [...prev, { role: 'agent', content: '⚠️ 审批请求失败' }])
    } finally {
      setLoading(false)
    }
  }

  // 处理输入框的 Enter 键发送
  function handleKeyDown(e: KeyboardEvent<HTMLInputElement>) {
    // Enter 键（不是 Shift+Enter）触发发送
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="chat">
      {/* 消息列表区：messages.map 遍历渲染每条消息 */}
      <div className="messages">
        {messages.map((msg, i) => (
          // key 是 React 列表渲染要求，用索引即可（本项目消息不删除）
          <div key={i} className={`message ${msg.role}`}>
            {/* 消息内容 */}
            <div className="bubble">{msg.content}</div>
                        {/* 如果是 pending 消息，渲染审批卡片（含批准/拒绝按钮） */}
            {msg.pending && (
              <div className="pending-list">
                {msg.pending.map((p, j) => (
                  <div key={j} className="pending-item">
                    {/* 工具名和参数 */}
                    <div><strong>{p.name}</strong></div>
                    <div className="pending-args">{JSON.stringify(p.args)}</div>
                    {/* 审批按钮：批准 / 拒绝 */}
                    <div className="pending-actions">
                      {/* 批准按钮：调 /api/approve，决策类型 approve */}
                      <button
                        className="btn-approve"
                        disabled={loading}
                        onClick={() => sendDecision([{ type: 'approve' }], i)}
                      >
                        批准
                      </button>
                      {/* 拒绝按钮：决策类型 reject（仅当允许决策里含 reject 时显示） */}
                      {p.allowed_decisions.includes('reject') && (
                        <button
                          className="btn-reject"
                          disabled={loading}
                          onClick={() => sendDecision([{ type: 'reject' }], i)}
                        >
                          拒绝
                        </button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>

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