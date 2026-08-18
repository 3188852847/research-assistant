// 应用根组件：挂载路由

// RouterProvider: 提供路由上下文并渲染匹配页面
import { RouterProvider } from 'react-router-dom'
// 路由表
import { router } from './router'

// 应用根组件
function App() {
  return <RouterProvider router={router} />
}

export default App