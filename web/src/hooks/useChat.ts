// 对话状态 hook：管理消息、思考过程、流式、审批
// chat feature 的核心逻辑，UI 组件只用它给的状态

import { useState } from 'react'
import { sendChatStream, sendApprove } from '../api/chat'
import type { PendingItem } from '../api/types'

// 消息类型（前端对话消息）
export interface Msg {
  role: 'user' | 'agent' | 'pending'   // 角色
  content: string                       // 文本
  pending?: PendingItem[]               // 待审操作（role=pending 时）
  thinking?: boolean                    // 是否「思考中」占位（显示打字指示器）
}

// useChat hook
export function useChat(threadId: string) {
  // 消息列表
  const [messages, setMessages] = useState<Msg[]>([])
  // 思考过程（进度行 + 推理片段）
  const [progress, setProgress] = useState<string[]>([])
  const [reasoning, setReasoning] = useState<string[]>([])
  const [thinking, setThinking] = useState(false)   // 是否思考中
  // 加载态
  const [loading, setLoading] = useState(false)

  // 发送消息（流式）
  async function send(message: string) {
    if (!message.trim() || loading) return

    // 用户消息入列
    setMessages(prev => [...prev, { role: 'user', content: message }])

    // 重置思考过程（新一轮）
    setProgress([])
    setReasoning([])
    setThinking(true)
    setLoading(true)

    try {
      // 流式：进度/推理实时收集，完成时收起思考 + 显示回复
      await sendChatStream(
        message,
        threadId,
        (line) => setProgress(prev => [...prev, line]),          // 进度行
        (content) => setReasoning(prev => [...prev, content]),   // 推理
        (reply) => {
          setThinking(false)
          setMessages(prev => [...prev, { role: 'agent', content: reply }])
        },
        // onEvent 预留：未来 AI 跳页 navigate 在这里处理
        () => {},
      )
    } catch (err) {
      console.error('请求失败:', err)
      setThinking(false)
      setMessages(prev => [...prev, { role: 'agent', content: '⚠️ 请求失败，请检查后端是否启动' }])
    } finally {
      setLoading(false)
    }
  }

  // 审批（人机回环）
  async function approve(decision: 'approve' | 'reject', pendingMsgIndex: number) {
    setLoading(true)
    try {
      const data = await sendApprove(threadId, [{ type: decision }])
      // 把已审批的 pending 消息替换
      setMessages(prev => prev.map((m, i) =>
        i === pendingMsgIndex ? { role: 'agent', content: '(审批已提交)' } : m
      ))
      // 处理结果：可能又一轮 pending 或最终回复
      if (data.pending) {
        setMessages(prev => [...prev, { role: 'pending', content: '还有操作需要审批：', pending: data.pending! }])
      } else {
        setMessages(prev => [...prev, { role: 'agent', content: data.reply ?? '' }])
      }
    } catch (err) {
      console.error('审批失败:', err)
    } finally {
      setLoading(false)
    }
  }

  // 暴露给组件的状态和动作
  return {
    messages, progress, reasoning, thinking, loading,
    send, approve,
  }
}
