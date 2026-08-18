// 玻璃卡片：全站统一的卡片容器，保证风格一致
// 用法：<GlassCard>...</GlassCard> 或 <GlassCard hover>...</GlassCard>
// 玻璃参数定义在 tokens.css + glass.css，这里只引用，不写死色值

import type { ReactNode } from 'react'

// 组件 props
interface GlassCardProps {
  children: ReactNode            // 卡片内容
  hover?: boolean                // 是否启用 hover 提亮
  style?: React.CSSProperties    // 额外样式（可选）
}

// 玻璃卡片组件
export default function GlassCard({ children, hover, style }: GlassCardProps) {
  return (
    // div 套 glass-card 原子类（玻璃底 + blur + 微光边框 + 圆角 + 阴影）
    // hover 为 true 时加 hover 提亮类
    <div
      className={`glass-card ${hover ? 'glass-card-hover' : ''}`}
      style={{ padding: 16, ...style }}
    >
      {children}
    </div>
  )
}
