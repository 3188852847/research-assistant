// 对话页：组装 useChat + MessageList + 底部输入栏
// chat feature 的页面入口（AI 全局者的对话交互）

import { useState } from 'react'
import { Input, Button } from 'antd'
import { useChat } from '../../hooks/useChat'
import MessageList from './components/MessageList'

// 会话 ID：简单起见用固定值（后续可加会话管理）
const THREAD_ID = 'default'

// 对话页组件
export default function ChatPage() {
  // 对话状态（useChat 管理消息/思考/审批）
  const { messages, progress, reasoning, thinking, loading, send, approve } = useChat(THREAD_ID)
  // 输入框
  const [input, setInput] = useState('')

  // 发送：调 api，清空输入
  const handleSend = () => {
    if (!input.trim() || loading) return
    send(input)
    setInput('')
  }

  return (
    // 对话页：垂直布局，消息列表占满 + 底部输入
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%', gap: 8 }}>
      {/* 消息列表（含思考折叠 + 审批） */}
      <MessageList
        messages={messages}
        progress={progress}
        reasoning={reasoning}
        thinking={thinking}
        loading={loading}
        onApprove={approve}
      />

      {/* 底部输入栏 */}
      <div style={{ display: 'flex', gap: 8 }}>
        <Input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onPressEnter={handleSend}
          placeholder="输入消息，Enter 发送"
          disabled={loading}
        />
        <Button type="primary" onClick={handleSend} disabled={loading || !input.trim()} loading={loading}>
          {loading ? '思考中' : '发送'}
        </Button>
      </div>
    </div>
  )
}
