// 应用入口：挂载 React 应用 + antd 暗色主题 + Menu 玻璃化定制

import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
// antd 全局配置 + 暗色主题算法
import { ConfigProvider, theme } from 'antd'
// 全局样式（含 tokens/glass）
import './styles/index.css'
import App from './App.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    {/* antd 配置：暗色算法 + 绿色强调 + 自定 token + Menu 玻璃化 */}
    <ConfigProvider
      theme={{
        algorithm: theme.darkAlgorithm,   // antd 暗色主题
        token: {
          colorPrimary: '#01B149',        // 强调色（荧光绿）
          colorBgBase: '#0B0D11',         // 背景近黑
          colorTextBase: '#FFFFFF',       // 文字白
          borderRadius: 10,               // 组件圆角
        },
        components: {
          // Menu 定制：解决选中项纯绿实底刺眼，改成半透明玻璃绿
          Menu: {
            itemSelectedBg: 'rgba(1, 177, 73, 0.15)',   // 选中项：半透明绿底（保留玻璃感）
            itemSelectedColor: '#FFFFFF',                 // 选中文字白
            itemBg: 'transparent',                        // 整项底透明（露出侧边栏玻璃）
            itemColor: 'rgba(255,255,255,0.60)',          // 未选文字半透明
          },
        },
      }}
    >
      <App />
    </ConfigProvider>
  </StrictMode>,
)
