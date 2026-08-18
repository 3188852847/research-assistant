// 审批卡片组件：显示待审操作 + 批准/拒绝按钮（antd 版）

// 导入 antd 组件：Card（卡片）、Tag（标签）、Button（按钮）、Space（间距）
import { Card, Tag, Button, Space } from 'antd'
// 导入类型：待审操作
import type { PendingItem } from '../api/types'

// 组件 props 定义
interface PendingCardProps {
  item: PendingItem            // 待审操作数据
  loading: boolean             // 是否正在请求
  onDecision: (type: 'approve' | 'reject') => void  // 用户决策回调
}

// 审批卡片组件
export default function PendingCard({ item, loading, onDecision }: PendingCardProps) {
  return (
    // antd Card：带边框的卡片容器，标题显示工具名
    <Card
      size="small"                        // 小尺寸卡片
      title={<Tag color="orange">{item.name}</Tag>}  // 工具名用橙色标签
      style={{ marginTop: 8, background: '#fffbe6' }}  // 浅黄背景（审批提示）
    >
      {/* 工具参数：等宽字体展示 JSON */}
      <div style={{ fontSize: 12, color: '#666', wordBreak: 'break-all', marginBottom: 8 }}>
        {JSON.stringify(item.args)}
      </div>
      {/* 审批按钮组：水平排列 */}
      <Space>
        {/* 批准按钮：主色（蓝） */}
        <Button type="primary" size="small" disabled={loading} onClick={() => onDecision('approve')}>
          批准
        </Button>
        {/* 拒绝按钮：危险色（红），仅后端允许 reject 时显示 */}
        {item.allowed_decisions.includes('reject') && (
          <Button danger size="small" disabled={loading} onClick={() => onDecision('reject')}>
            拒绝
          </Button>
        )}
      </Space>
    </Card>
  )
}