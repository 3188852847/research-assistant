// 对话页面：会话管理 + 聊天界面
// 用 antd Layout 布局：顶部 Header + 内容区

// 导入 React Hooks
import { useState } from 'react'
// 导入 antd 组件：Layout（布局）、Button（按钮）、Typography（标题）
import { Layout, Button, Typography } from 'antd'
// 导入聊天组件（从组件出口聚合拿）
import { Chat } from '../components'

// 解构 Layout 的子组件（Header=顶栏，Content=内容区）
const { Header, Content } = Layout

// 生成新会话 ID 的函数：时间戳 + 随机数
function newThreadId(): string {
  return 'thread-' + Date.now().toString(36) + Math.random().toString(36).slice(2, 6)
}

// 对话页面组件
export default function ChatPage() {
  // threadId: 当前会话 ID
  const [threadId, setThreadId] = useState<string>(newThreadId())

  // 切换会话：生成新 ID（key 变化让 Chat 重建，消息清空）
  function switchThread() {
    setThreadId(newThreadId())
  }

  return (
    // antd 布局容器：占满全屏
    <Layout style={{ height: '100vh' }}>
      {/* 顶栏：标题 + 新建会话按钮 */}
      <Header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        {/* 标题：白色文字 */}
        <Typography.Title level={4} style={{ color: '#fff', margin: 0 }}>
          research-assistant
        </Typography.Title>
        {/* 新建会话按钮 */}
        <Button onClick={switchThread}>新建会话</Button>
      </Header>
      {/* 内容区：放聊天组件，占满剩余高度 */}
      <Content style={{ display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
        {/* key={threadId}：会话切换时组件重建 */}
        <Chat key={threadId} threadId={threadId} />
      </Content>
    </Layout>
  )
}