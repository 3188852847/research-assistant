// 检索页：输入关键词 → grep 扫 Analysis → 结果列表 → 点开看 Analysis
import { useState } from 'react'
import { Input, Button, List, Modal, Tag, message } from 'antd'
import { searchPapers, type SearchHit } from '../../api/search'
import { getAnalysis } from '../../api/analyze'

export default function SearchPage() {
  const [q, setQ] = useState('')
  const [results, setResults] = useState<SearchHit[]>([])
  const [loading, setLoading] = useState(false)
  // 点开看的 Analysis
  const [detail, setDetail] = useState<{ paper_id: string; analysis: Record<string, string>; report: string } | null>(null)

  async function handleSearch() {
    if (!q.trim()) return
    setLoading(true)
    try {
      const hits = await searchPapers(q)
      setResults(hits)
    } catch {
      message.error('检索失败')
    } finally {
      setLoading(false)
    }
  }

  // 点开看该篇 Analysis（四字段 + 报告）
  async function openDetail(paperId: string) {
    try {
      const data = await getAnalysis(paperId)
      setDetail({ paper_id: paperId, analysis: data.analysis, report: data.report })
    } catch {
      message.error('无法读取该篇的分析')
    }
  }

  return (
    <div>
      <h2 style={{ color: 'var(--text-1)' }}>检索</h2>
      {/* 搜索框 */}
      <div style={{ display: 'flex', gap: 8, margin: '16px 0' }}>
        <Input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          onPressEnter={handleSearch}
          placeholder="搜索分析的词组（如「对比学习」「注意力」）"
        />
        <Button type="primary" onClick={handleSearch} loading={loading}>检索</Button>
      </div>

      {/* 结果列表 */}
      {results.length > 0 && (
        <div className="glass-card" style={{ padding: 12 }}>
          <List
            dataSource={results}
            renderItem={(hit) => (
              <List.Item
                onClick={() => openDetail(hit.paper_id)}
                style={{ cursor: 'pointer' }}
              >
                <List.Item.Meta
                  title={<span style={{ color: 'var(--text-1)' }}>{hit.title}</span>}
                  description={
                    <div>
                      <Tag color="green">{hit.matched_field}</Tag>
                      <span style={{ color: 'var(--text-2)' }}>{hit.snippet}</span>
                    </div>
                  }
                />
              </List.Item>
            )}
          />
        </div>
      )}
      {!loading && results.length === 0 && q && (
        <div style={{ color: 'var(--text-3)' }}>无匹配结果（MVP 用关键词扫描，未用向量）</div>
      )}

      {/* 点开看 Analysis 弹窗 */}
      <Modal
        open={!!detail}
        title="Analysis 详情"
        onCancel={() => setDetail(null)}
        footer={null}
        width={600}
      >
        {detail && (
          <div>
            <div style={{ marginBottom: 8 }}><b>研究问题</b><div>{detail.analysis.research_question}</div></div>
            <div style={{ marginBottom: 8 }}><b>核心结论</b><div>{detail.analysis.core_conclusion}</div></div>
            <div style={{ marginBottom: 8 }}><b>研究局限</b><div>{detail.analysis.limitations}</div></div>
            <div style={{ marginBottom: 8 }}><b>我的疑问</b><div>{detail.analysis.questions}</div></div>
          </div>
        )}
      </Modal>
    </div>
  )
}
