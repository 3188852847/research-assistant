// 工具调用卡片：把 AI 分析过程中的「工具调用」显示成一张卡片
// 用于卡片流（chat/analyze 共用）——让 AI 干了什么可见、可被审
// 玻璃样式引用 tokens.css 变量

// 工具卡片 props
interface ToolCallCardProps {
  toolName: string                            // 工具名（如 read_pdf / internet_search）
  args?: Record<string, unknown>              // 调用参数（可选）
  result?: string                             // 工具返回结果摘要（可选）
  status?: 'running' | 'done' | 'error'       // 状态
}

// 工具调用卡片组件
export default function ToolCallCard({
  toolName, args, result, status = 'done',
}: ToolCallCardProps) {
  return (
    // 玻璃卡片容器（hover 提亮）
    <div className="glass-card glass-card-hover" style={{ padding: 12, marginBottom: 8 }}>
      {/* 第一行：状态点 + 工具名 + 状态文字 */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: 13 }}>
        {/* 状态点：绿=完成 蓝=运行 红=错误 */}
        <span style={{
          width: 8, height: 8, borderRadius: '50%',
          background: status === 'done' ? 'var(--accent)' : status === 'error' ? '#F5483B' : '#1677ff',
        }} />
        {/* 工具名 */}
        <strong style={{ color: 'var(--text-1)' }}>{toolName}</strong>
        {/* 状态文字 */}
        <span style={{ color: 'var(--text-3)' }}>
          {status === 'done' ? '完成' : status === 'error' ? '出错' : '执行中'}
        </span>
      </div>

      {/* 参数（可选）：显示传入的参数 */}
      {args && Object.keys(args).length > 0 && (
        <div style={{ marginTop: 6, fontSize: 12, color: 'var(--text-2)' }}>
          {Object.entries(args).map(([k, v]) => (
            <div key={k} style={{ marginTop: 2 }}>
              <span style={{ color: 'var(--text-3)' }}>{k}: </span>
              {/* 值转字符串显示（对象/数组用 JSON） */}
              {typeof v === 'string' ? v : JSON.stringify(v)}
            </div>
          ))}
        </div>
      )}

      {/* 结果摘要（可选） */}
      {result && (
        <div style={{
          marginTop: 6, fontSize: 12, color: 'var(--text-2)',
          maxHeight: 80, overflow: 'auto', whiteSpace: 'pre-wrap',
          borderTop: '1px solid var(--glass-border)', paddingTop: 6,
        }}>
          {result}
        </div>
      )}
    </div>
  )
}
