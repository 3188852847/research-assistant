// 主布局：顶栏（应用切换器）+ 左导航 + 内容区 + 底部 AI 栏（全宽，非对话页显示）
// 规则：底部 AI 栏霸占底部全宽（不被左导航挡）；进入对话页(/chat)时隐藏它，
//       对话页用自己的输入框（专注对话）

import { useState } from 'react'
import { Outlet, useLocation, useNavigate } from 'react-router-dom'
import { Layout, Menu, Select, Input, Button } from 'antd'
import {
  DashboardOutlined,
  FileTextOutlined,
  ThunderboltOutlined,
  ScanOutlined,
  SearchOutlined,
} from '@ant-design/icons'

const { Sider, Header, Content } = Layout

// 左导航：当前应用（研究助手）的模块
const appMenus = [
  { key: '/', icon: <DashboardOutlined />, label: '工作台' },
  { key: '/chat', icon: <ScanOutlined />, label: '对话' },
  { key: '/papers', icon: <FileTextOutlined />, label: '文库' },
  { key: '/analyze', icon: <ThunderboltOutlined />, label: '速拆' },
  { key: '/gap', icon: <SearchOutlined />, label: 'Gap' },
  { key: '/search', icon: <SearchOutlined />, label: '检索' },
]

// 当前应用清单（多应用容器）：现在只有研究助手，未来可加
const apps = [
  { value: 'research', label: '🎓 研究助手工作台' },
]

export default function MainLayout() {
  const location = useLocation()
  const navigate = useNavigate()
  // 底部 AI 栏输入
  const [aiInput, setAiInput] = useState('')

  // 是否对话页：对话页隐藏全局 AI 栏（用页面自己的输入框）
  const isChatPage = location.pathname === '/chat'

  // 底部 AI 栏发送（待接入 chat/stream，现在先占位清空）
  const handleSend = () => {
    if (!aiInput.trim()) return
    // TODO: 接入 /api/chat/stream，处理 AI 指令（含未来 navigate 跳页）
    setAiInput('')
  }

  return (
    // 整体背景加光斑（毛玻璃有东西可模糊）
    <Layout style={{ height: '100vh' }} className="page-bg">
      {/* 顶栏：应用切换器（多应用容器，跨应用切换） */}
      <Header style={{
        display: 'flex', alignItems: 'center', gap: 12, padding: '0 16px',
        background: 'var(--bg-elevated)', borderBottom: '1px solid var(--glass-border)',
        height: 48, lineHeight: '48px',
      }}>
        <Select value="research" style={{ width: 200 }} options={apps} />
        <span style={{ color: 'var(--text-3)', fontSize: 12 }}>个人 AI 工作平台</span>
      </Header>

      {/* 主体：左导航 + 内容区（占满剩余，flex 纵向） */}
      <Layout style={{ background: 'transparent', flex: 1 }}>
        {/* 左导航：当前应用内的模块 */}
        <Sider
          width={200}
          style={{
            background: 'var(--bg-elevated)',
            borderRight: '1px solid var(--glass-border)',
          }}
        >
          <Menu
            mode="inline"
            theme="dark"
            selectedKeys={[location.pathname]}
            items={appMenus}
            onClick={({ key }) => navigate(key)}
            style={{ background: 'transparent', borderRight: 'none', paddingTop: 8 }}
          />
        </Sider>

        {/* 内容区：当前页面 */}
        <Content style={{ overflow: 'auto', padding: 24 }}>
          <Outlet />
        </Content>
      </Layout>

      {/* 底部 AI 栏：全宽（整个 Layout 最底，不被左导航挡），非对话页才显示 */}
      {!isChatPage && (
        <div style={{
          padding: 12, borderTop: '1px solid var(--glass-border)',
          background: 'var(--bg-elevated)', display: 'flex', gap: 8,
        }}>
          <Input
            value={aiInput}
            onChange={(e) => setAiInput(e.target.value)}
            onPressEnter={handleSend}
            placeholder="向 AI 提问，或指令它去某个模块（如「去文献库看看」）"
            style={{ flex: 1 }}
          />
          <Button type="primary" onClick={handleSend}>发送</Button>
        </div>
      )}
    </Layout>
  )
}
