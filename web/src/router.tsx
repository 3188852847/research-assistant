// 路由定义：URL → 页面，全部套在 MainLayout 外壳下
// 加新模块 = 新建 feature 页面 + 这里加一行

// createBrowserRouter: 创建使用浏览器 history 的路由
import { createBrowserRouter } from 'react-router-dom'
// 主布局（三栏 + 底部 AI 栏）
import MainLayout from './layouts/MainLayout'
// 各 feature 页面
import DashboardPage from './features/dashboard/DashboardPage'
import ChatPage from './features/chat/ChatPage'
import PapersPage from './features/papers/PapersPage'
import AnalyzePage from './features/analyze/AnalyzePage'
import GapPage from './features/gap/GapPage'
import SearchPage from './features/search/SearchPage'

// 路由表
export const router = createBrowserRouter([
  {
    // 主布局路由：所有页面共享外壳
    path: '/',
    element: <MainLayout />,
    children: [
      // 首页 = 仪表盘（8-15 共识）
      { index: true, element: <DashboardPage /> },
      // 各功能页
      { path: 'chat', element: <ChatPage /> },
      { path: 'papers', element: <PapersPage /> },
      { path: 'analyze', element: <AnalyzePage /> },
      { path: 'gap', element: <GapPage /> },
      { path: 'search', element: <SearchPage /> },
    ],
  },
])