// 思考过程折叠面板：显示进度行 + 模型推理（antd Collapse）
// 每次对话一个面板：收起时看状态摘要，展开看推理细节

// 导入 antd 组件：Collapse（折叠面板）
import { Collapse } from 'antd'

// 组件 props
interface ThinkingPanelProps {
  title: string        // 面板标题（如「💭 思考中...」或「💭 已思考」）
  progress: string[]   // 进度行列表（🚀/🔧/✅ 等）
  reasoning: string[]  // 模型推理内容片段
  active: boolean      // 是否默认展开（思考中展开，完成收起）
}

// 思考折叠面板组件
export default function ThinkingPanel({ title, progress, reasoning, active }: ThinkingPanelProps) {
  return (
    // antd 折叠面板
    <Collapse
      // 受控展开/收起：active 决定
      activeKey={active ? ['thinking'] : []}
      // 面板项
      items={[{
        key: 'thinking',
        // 标题：状态摘要
        label: title,
        // 展开后的内容
        children: (
          <div style={{ fontSize: 12, color: '#666' }}>
            {/* 模型推理内容（如果有）：浅色块展示 */}
            {reasoning.length > 0 && (
              <div style={{
                background: '#f9f9f9',          // 浅灰底
                borderLeft: '3px solid #1677ff', // 蓝边
                padding: '8px 12px',
                marginBottom: 8,
                whiteSpace: 'pre-wrap',
                fontFamily: 'monospace',         // 等宽（推理原文感）
              }}>
                {/* 每个推理片段一段 */}
                {reasoning.map((r, i) => (
                  <div key={i} style={{ marginBottom: 4 }}>{r}</div>
                ))}
              </div>
            )}
            {/* 进度行列表 */}
            {progress.map((line, i) => (
              <div key={i} style={{ padding: '2px 0' }}>{line}</div>
            ))}
          </div>
        ),
      }]}
    />
  )
}