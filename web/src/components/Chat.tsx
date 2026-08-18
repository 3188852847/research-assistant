// 聊天组件：编排层——状态 + 调 api + 组合子组件（含思考折叠面板）

// 导入 React Hooks
import { useState, useEffect } from 'react'
// 导入 antd 组件
import { Input, Button } from 'antd'
// 导入 api 层
import { sendChat, sendApprove, sendChatStream } from '../api/client'
// 导入类型
import type { Message } from '../api/types'
// 导入消息列表
import MessageList from './MessageList'
// 导入思考折叠面板
import ThinkingPanel from './ThinkingPanel'

// 聊天组件
export default function Chat({ threadId }: { threadId: string }) {
  // 消息列表
  const [messages, setMessages] = useState<Message[]>([])
  // 输入框
  const [input, setInput] = useState('')
  // 加载状态
  const [loading, setLoading] = useState(false)

  // ---- 思考过程状态（当前这一轮）----
  // 进度行列表
  const [progress, setProgress] = useState<string[]>([])
  // 模型推理片段
  const [reasoning, setReasoning] = useState<string[]>([])
  // 面板是否展开（思考中展开，完成收起）
  const [thinkingActive, setThinkingActive] = useState(false)
  // 是否正在思考（控制面板标题）
  const [thinking, setThinking] = useState(false)

  // 发送消息（流式 + 思考面板）
  async function sendMessage() {
    if (!input.trim() || loading) return

    // 用户消息入列
    const userMsg: Message = { role: 'user', content: input }
    setMessages(prev => [...prev, userMsg])
    setInput('')

    // 重置思考面板（新一轮）
    setProgress([])
    setReasoning([])
    setThinking(true)          // 显示「思考中」
    setThinkingActive(true)    // 展开
    setLoading(true)

    try {
      // 流式接口：进度/推理/完成三回调
      await sendChatStream(
        input,
        threadId,
        // 进度回调：追加进度行
        (line) => setProgress(prev => [...prev, line]),
        // 推理回调：追加推理片段
        (content) => setReasoning(prev => [...prev, content]),
        // 完成回调：收起面板 + 显示最终回复
        (reply) => {
          setThinking(false)       // 标题变「已思考」
          setThinkingActive(false) // 收起面板（可点开看）
          setMessages(prev => [...prev, { role: 'agent', content: reply }])
        },
      )
    } catch (err) {
      console.error('请求失败:', err)
      setThinking(false)
      setMessages(prev => [...prev, { role: 'agent', content: '⚠️ 请求失败，请检查后端是否启动' }])
    } finally {
      setLoading(false)
    }
  }

  // 审批（逻辑不变）
  async function handleApprove(decision: 'approve' | 'reject', pendingMsgIndex: number) {
    setLoading(true)
    try {
      const data = await sendApprove(threadId, [{ type: decision }])
      setMessages(prev => prev.map((m, i) => i === pendingMsgIndex ? { role: 'agent', content: '(审批已提交)' } : m))
      if (data.pending) {
        setMessages(prev => [...prev, { role: 'pending', content: '还有操作需要你的审批：', pending: data.pending ?? undefined }])
      } else {
        setMessages(prev => [...prev, { role: 'agent', content: data.reply ?? '' }])
      }
    } catch (err) {
      console.error('审批失败:', err)
      setMessages(prev => [...prev, { role: 'agent', content: '⚠️ 审批请求失败' }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ flex: 1, display: 'flex', flexDirection: 'column', height: '100%' }}>
      {/* 消息列表 */}
      <MessageList messages={messages} loading={loading} onApprove={handleApprove} />

      {/* 思考过程折叠面板（有内容才显示） */}
      {(progress.length > 0 || reasoning.length > 0 || thinking) && (
        <div style={{ padding: '0 12px' }}>
          <ThinkingPanel
            title={thinking ? '💭 思考中...' : '💭 已思考（点击展开）'}
            progress={progress}
            reasoning={reasoning}
            active={thinkingActive}
          />
        </div>
      )}

      {/* 输入区 */}
      <div style={{ display: 'flex', gap: 8, padding: 12, borderTop: '1px solid #f0f0f0' }}>
        <Input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onPressEnter={sendMessage}
          placeholder="输入消息，Enter 发送"
          disabled={loading}
        />
        <Button type="primary" onClick={sendMessage} disabled={loading || !input.trim()} loading={loading}>
          {loading ? '思考中...' : '发送'}
        </Button>
      </div>
    </div>
  )
}