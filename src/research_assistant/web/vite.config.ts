// Vite 构建配置
// 参考：https://vite.dev/config/
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// defineConfig 是 Vite 的配置函数，返回配置对象
export default defineConfig({
  // 插件：react 插件让 Vite 支持 React 的 JSX 语法和热更新
  plugins: [react()],
  // server: 开发服务器的配置
  server: {
    // port: 开发服务器端口（默认 5173）
    port: 5173,
    // proxy: 请求代理——把特定前缀的请求转发到别的服务器
    proxy: {
      // '/api': 所有以 /api 开头的请求（如 /api/chat）
      '/api': {
        // target: 转发目标——我们的 FastAPI 后端地址
        target: 'http://127.0.0.1:8000',
        // changeOrigin: 修改请求头里的 Host 为目标地址（后端按主机名判断时需要）
        changeOrigin: true,
      },
    },
  },
})