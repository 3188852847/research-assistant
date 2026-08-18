// 占位页组件：开发中的功能模块显示「建设中」

interface PlaceholderProps {
  title: string      // 模块名
  desc?: string      // 说明（可选）
}

// 占位组件
export default function Placeholder({ title, desc }: PlaceholderProps) {
  return (
    <div style={{ padding: 48, textAlign: 'center', color: 'var(--text-secondary)' }}>
      {/* 模块名 */}
      <div style={{ fontSize: 20, fontWeight: 600, color: 'var(--text-primary)', marginBottom: 8 }}>
        {title}
      </div>
      {/* 说明 */}
      <div style={{ fontSize: 14 }}>{desc ?? '建设中，敬请期待'}</div>
    </div>
  )
}