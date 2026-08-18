// 应用根组件：只负责「渲染哪个页面」（目前只有对话页）
// 将来加页面/路由时，App 在这里做切换，页面组件放 pages/

// 导入对话页面
import ChatPage from './pages/ChatPage'
// 导入样式
import './styles/App.css'

// 应用根组件
function App() {
  // 目前只有一个页面：直接渲染对话页
  return <ChatPage />
}


// 导出根组件（main.tsx 用到）
export default App