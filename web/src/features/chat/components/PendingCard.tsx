// 审批卡片：待审操作的批准/拒绝交互（人机回环）
// 玻璃卡片样式，显示工具名 + 参数 + 批准/拒绝按钮

import { Button, Tag, Space } from 'antd'
import type { PendingItem } from '../../api/types'

// props
interface PendingCardProps {
  item: PendingItem                 // 待审操作
  loading: boolean                  // 请求中禁用按钮
  onDecision: (type: 'approve' | 'reject') => void  // 审批回调
}

// 审批卡片组件
export default function PendingCard({ item, loading, onDecision }: PendingCardProps) {
  return (
    // 玻璃卡片
    <div className="glass-card" style={{ padding: 12, marginTop: 8, background: 'var(--glass-bg)' }}>
      {/* 工具名标签 */}
      <div style={{ marginBottom: 4 }}>
        <Tag color="green">{item.name}</Tag>
      </div>
      {/* 参数 JSON */}
      <div style={{ fontSize: 12, color: 'var(--text-2)', wordBreak: 'break-all', marginBottom: 8 }}>
        {JSON.stringify(item.args)}
      </div>
      {/* 审批按钮 */}
      <Space>
        <Button type="primary" size="small" disabled={loading} onClick={() => onDecision('approve')}>
          批准
        </Button>
        {item.allowed_decisions.includes('reject') && (
          <Button danger size="small" disabled={loading} onClick={() => onDecision('reject')}>
            拒绝
          </Button>
        )}
      </Space>
    </div>
  )
}
