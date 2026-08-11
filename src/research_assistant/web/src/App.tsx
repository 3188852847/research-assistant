// 应用根组件：会话管理 + 聊天界面
// 负责 thread_id 的生成和切换（新建会话/继续会话）

// 导入 React Hooks：useState（状态）
import { useState } from 'react'
// 导入聊天组件
import Chat from './components/Chat'
// 导入样式
import './App.css'

// 生成新会话 ID 的函数：时间戳 + 随机数
// 会话 ID 是后端 checkpointer 识别会话的钥匙，每次新建会话生成一个唯一的
function newThreadId(): string {
  return 'thread-' + Date.now().toString(36) + Math.random().toString(36).slice(2, 6)
}

// 应用根组件
function App() {
  // threadId: 当前会话 ID，初始生成一个
  const [threadId, setThreadId] = useState<string>(newThreadId())

  // 切换会话的函数：生成新 ID 传给 Chat（Chat 内部消息列表会清空吗？不会，见下方说明）
  function switchThread() {
    setThreadId(newThreadId())
  }

  return (
    // 页面容器
    <div className="app">
      {/* 顶栏：标题 + 新建会话按钮 */}
      <header className="app-header">
        <h1>research-assistant</h1>
        <button onClick={switchThread}>新建会话</button>
      </header>
      {/* key={threadId}：thread 变化时 Chat 组件整体重建，消息历史自动清空 */}
      <Chat key={threadId} threadId={threadId} />
    </div>
  )
}

// 导出根组件（main.tsx 会用到）
export default App