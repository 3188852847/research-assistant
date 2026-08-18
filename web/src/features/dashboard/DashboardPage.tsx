// 工作台首页（仪表盘）：统计卡四宫格 + 最近动态
// 用 GlassCard 玻璃卡片；数据先用假数据（papers 后端建好后接 /api/stats）

import GlassCard from '../../components/GlassCard'

// 模拟统计卡数据（后续接 /api/stats）
const stats = [
  { label: '文献总数', value: 0, icon: '📄', desc: '已导入文库的论文' },
  { label: '待读', value: 0, icon: '📌', desc: '待阅读状态' },
  { label: '已分析', value: 0, icon: '🧠', desc: '已完成速拆' },
  { label: '实验进展', value: '—', icon: '🧪', desc: '研0（暂未开展）' },
]

// 模拟最近动态（后续接后端）
const recent = [
  { time: '', text: '暂无科研动态' },
]

// 仪表盘组件
export default function DashboardPage() {
  return (
    <div>
      {/* 标题 */}
      <h2 style={{ color: 'var(--text-1)', marginBottom: 20 }}>工作台</h2>

      {/* 统计卡四宫格 */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16 }}>
        {stats.map((s, i) => (
          <GlassCard key={i} hover style={{ textAlign: 'center' }}>
            {/* 图标 */}
            <div style={{ fontSize: 28 }}>{s.icon}</div>
            {/* 数值（大号强调） */}
            <div style={{ fontSize: 32, fontWeight: 700, color: 'var(--text-1)', margin: '8px 0' }}>
              {s.value}
            </div>
            {/* 标签 */}
            <div style={{ color: 'var(--text-2)', fontSize: 14 }}>{s.label}</div>
            {/* 描述 */}
            <div style={{ color: 'var(--text-3)', fontSize: 12, marginTop: 4 }}>{s.desc}</div>
          </GlassCard>
        ))}
      </div>

      {/* 最近动态 */}
      <div style={{ marginTop: 24 }}>
        <h3 style={{ color: 'var(--text-2)', marginBottom: 12 }}>最近动态</h3>
        <GlassCard>
          {recent.map((r, i) => (
            <div key={i} style={{ color: 'var(--text-3)', fontSize: 13 }}>
              {r.time} {r.text}
            </div>
          ))}
        </GlassCard>
      </div>
    </div>
  )
}
