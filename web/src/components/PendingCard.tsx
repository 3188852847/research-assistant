// 审批卡片组件：显示待审操作 + 批准/拒绝按钮
// 纯展示组件：不持有状态，通过 props 接收数据和回调

// 导入待审操作的数据类型
import type { PendingItem } from '../api/types'

// 组件 props 定义
interface PendingCardProps {
  item: PendingItem            // 待审操作数据（工具名/参数/允许决策）
  loading: boolean             // 是否正在请求（禁用按钮）
  onDecision: (type: 'approve' | 'reject') => void  // 用户决策回调
}

// 审批卡片组件
export default function PendingCard({ item, loading, onDecision }: PendingCardProps) {
  return (
    // 卡片容器
    <div className="pending-item">
      {/* 工具名 */}
      <div><strong>{item.name}</strong></div>
      {/* 工具参数（JSON 展示） */}
      <div className="pending-args">{JSON.stringify(item.args)}</div>
      {/* 审批按钮区 */}
      <div className="pending-actions">
        {/* 批准按钮：绿色，点击触发 onDecision('approve') */}
        <button
          className="btn-approve"
          disabled={loading}
          onClick={() => onDecision('approve')}
        >
          批准
        </button>
        {/* 拒绝按钮：仅当后端允许 reject 决策时显示 */}
        {item.allowed_decisions.includes('reject') && (
          <button
            className="btn-reject"
            disabled={loading}
            onClick={() => onDecision('reject')}
          >
            拒绝
          </button>
        )}
      </div>
    </div>
  )
}