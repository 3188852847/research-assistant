// 对话页面：会话管理 + 聊天界面
// 页面级组件：从 App.tsx 拆出的「对话」页面职责
// 将来新增页面（设置页/历史页…）也放 pages/ 下，App 只做路由

// 导入 React Hooks：useState
import { useState } from 'react'
// 导入聊天组件（从组件出口聚合拿）
import { Chat } from '../components'

// 生成新会话 ID 的函数：时间戳 + 随机数
// 会话 ID 是后端 checkpointer 识别会话的钥匙，每次新建会话生成一个唯一的
function newThreadId(): string {
  return 'thread-' + Date.now().toString(36) + Math.random().toString(36).slice(2, 6)
}

// 对话页面组件
export default function ChatPage() {
  // threadId: 当前会话 ID，初始生成一个
  const [threadId, setThreadId] = useState<string>(newThreadId())

  // 切换会话：生成新 ID（key 变化会让 Chat 整体重建，消息清空）
  function switchThread() {
    setThreadId(newThreadId())
  }

  return (
    <div className="app">
      {/* 顶栏：标题 + 新建会话按钮 */}
      <header className="app-header">
        <h1>research-assistant</h1>
        <button onClick={switchThread}>新建会话</button>
      </header>
      {/* 聊天主区域：key={threadId} 让会话切换时组件重建 */}
      <Chat key={threadId} threadId={threadId} />
    </div>
  )
}