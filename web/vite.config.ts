import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  // 开发服务器配置
  server: {
    port: 5173,
    // 代理：把 /api 请求转发到后端 FastAPI（8000）
    // 前端代码直接写 fetch('/api/...') 即可，浏览器无跨域问题
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
  },
})
