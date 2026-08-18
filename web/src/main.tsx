// 应用入口：挂载 React 应用

// 导入 React 的 StrictMode（开发模式检查）
import { StrictMode } from 'react'
// 导入 createRoot：React 18+ 的挂载 API
import { createRoot } from 'react-dom/client'
// 导入 antd 的 ConfigProvider：全局配置（语言包/主题）
import { ConfigProvider } from 'antd'
// 导入 antd 中文语言包（组件文案显示中文）
import zhCN from 'antd/locale/zh_CN'
// 导入全局样式
import './styles/index.css'
// 导入根组件
import App from './App.tsx'

// 挂载到 index.html 的 #root 元素
createRoot(document.getElementById('root')!).render(
  // StrictMode：开发模式的双重渲染检查（帮助发现 bug）
  <StrictMode>
    {/* ConfigProvider：antd 全局配置，locale=zhCN 让组件显示中文 */}
    <ConfigProvider locale={zhCN}>
      <App />
    </ConfigProvider>
  </StrictMode>,
)