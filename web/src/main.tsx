// 应用入口：挂载 React 应用 + antd 暗色主题

import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
// antd 全局配置 + 暗色主题算法
import { ConfigProvider, theme } from 'antd'
// 全局样式（含 tokens/glass）
import './styles/index.css'
import App from './App.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    {/* antd 配置：暗色算法 + 绿色强调 + 自定 token */}
    <ConfigProvider
      theme={{
        algorithm: theme.darkAlgorithm,   // antd 暗色主题
        token: {
          colorPrimary: '#01B149',        // 强调色（荧光绿）
          colorBgBase: '#0B0D11',         // 背景近黑
          colorTextBase: '#FFFFFF',       // 文字白
          borderRadius: 10,               // 组件圆角
        },
      }}
    >
      <App />
    </ConfigProvider>
  </StrictMode>,
)