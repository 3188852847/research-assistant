// Gap 发现页：选多篇同主题文献 → 触发 agent 横向对比 → Gap 报告
import { useEffect, useState } from 'react'
import { Select, Button, message } from 'antd'
import { listPapers, type Paper } from '../../api/papers'
import { runGap } from '../../api/gap'

export default function GapPage() {
  const [papers, setPapers] = useState<Paper[]>([])
  // 选中的文献（多选）
  const [selected, setSelected] = useState<string[]>([])
  const [report, setReport] = useState('')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    listPapers().then(setPapers).catch(() => message.error('加载文献失败'))
  }, [])

  async function handleGap() {
    if (selected.length < 2) return message.warning('请选择至少 2 篇同主题文献')
    setLoading(true)
    setReport('')
    try {
      const res = await runGap(selected)
      setReport(res.gap_report)
    } catch {
      message.error('Gap 分析失败')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h2 style={{ color: 'var(--text-1)' }}>Gap 发现</h2>
      {/* 选文献（多选）+ 找 Gap */}
      <div style={{ display: 'flex', gap: 8, margin: '16px 0' }}>
        <Select
          mode="multiple"
          placeholder="选多篇同主题文献（≥2）"
          style={{ flex: 1 }}
          value={selected}
          onChange={setSelected}
          options={papers.map(p => ({ value: p.paper_id, label: p.title || p.paper_id }))}
        />
        <Button type="primary" onClick={handleGap} loading={loading} disabled={selected.length < 2}>
          {loading ? '分析中…' : '找 Gap'}
        </Button>
      </div>

      {/* Gap 报告 */}
      {report && (
        <div className="glass-card" style={{ padding: 20 }}>
          <h3 style={{ color: 'var(--text-1)', marginTop: 0 }}>Gap 报告</h3>
          <div style={{ whiteSpace: 'pre-wrap', color: 'var(--text-1)' }}>{report}</div>
        </div>
      )}
    </div>
  )
}
