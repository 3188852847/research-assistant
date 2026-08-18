// 速拆页：选文献 → 流式速拆（卡片流显示工具调用过程）→ 四字段 + 报告
import { useEffect, useState } from 'react'
import { Select, Button, Card, Collapse, Input, message } from 'antd'
import { listPapers, type Paper } from '../../api/papers'
import { runAnalyzeStream, askAnalysis, type Analysis } from '../../api/analyze'
import ToolCallCard from '../../components/ToolCallCard'

export default function AnalyzePage() {
  const [papers, setPapers] = useState<Paper[]>([])
  const [selected, setSelected] = useState<string>()
  const [toolCalls, setToolCalls] = useState<{ tool: string; args: Record<string, unknown> }[]>([])
  const [analysis, setAnalysis] = useState<Analysis | null>(null)
  const [report, setReport] = useState('')
  const [loading, setLoading] = useState(false)
  // 追问：输入 + 回答 + 加载态
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [asking, setAsking] = useState(false)

  useEffect(() => {
    listPapers().then(setPapers).catch(() => message.error('加载文献失败'))
  }, [])

  async function handleAnalyze() {
    if (!selected) return message.warning('请先选择一篇文献')
    setLoading(true)
    setAnalysis(null)
    setReport('')
    setToolCalls([])
    try {
      await runAnalyzeStream(
        selected,
        (tool, args) => setToolCalls(prev => [...prev, { tool, args }]),  // 收集工具卡片
        () => {},
        (a, r) => { setAnalysis(a); setReport(r) },
      )
    } catch {
      message.error('速拆失败')
    } finally {
      setLoading(false)
    }
  }

  // 追问：基于分析结果提问
  async function handleAsk() {
    if (!selected || !question.trim() || asking) return
    setAsking(true)
    setAnswer('')
    try {
      const res = await askAnalysis(selected, question)
      setAnswer(res.answer)
    } catch {
      message.error('追问失败')
    } finally {
      setAsking(false)
    }
  }

  return (
    <div>
      <h2 style={{ color: 'var(--text-1)' }}>速拆</h2>
      <div style={{ display: 'flex', gap: 8, margin: '16px 0' }}>
        <Select
          placeholder="选择要速拆的文献"
          style={{ flex: 1 }}
          value={selected}
          onChange={setSelected}
          options={papers.map(p => ({ value: p.paper_id, label: p.title || p.paper_id }))}
        />
        <Button type="primary" loading={loading} onClick={handleAnalyze} disabled={!selected}>
          {loading ? '速拆中…' : '开始速拆'}
        </Button>
      </div>

      {/* 速拆过程：工具调用卡片流（实时） */}
      {toolCalls.length > 0 && (
        <div style={{ marginBottom: 16 }}>
          <h3 style={{ color: 'var(--text-2)', fontSize: 14 }}>分析过程</h3>
          {toolCalls.map((tc, i) => (
            <ToolCallCard key={i} toolName={tc.tool} args={tc.args} />
          ))}
        </div>
      )}

      {/* 结果 */}
      {analysis && (
        <div className="glass-card" style={{ padding: 20 }}>
          <h3 style={{ color: 'var(--text-1)', marginTop: 0 }}>速拆结果</h3>
          <Card size="small" title="研究问题" bordered={false}>{analysis.research_question}</Card>
          <Card size="small" title="核心结论" bordered={false}>{analysis.core_conclusion}</Card>
          <Card size="small" title="研究局限" bordered={false}>{analysis.limitations}</Card>
          <Card size="small" title="我的疑问" bordered={false}>{analysis.questions}</Card>
          {report && (
            <Collapse ghost
              items={[{ key: 'report', label: '查看报告全文', children: <div style={{ whiteSpace: 'pre-wrap' }}>{report}</div> }]}
            />
          )}

          {/* 追问：基于分析结果提问 */}
          <div style={{ marginTop: 16 }}>
            <div style={{ display: 'flex', gap: 8 }}>
              <Input
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onPressEnter={handleAsk}
                placeholder="追问（如「这个方法的局限是什么？」）"
              />
              <Button onClick={handleAsk} loading={asking} disabled={!question.trim()}>追问</Button>
            </div>
            {answer && (
              <div className="glass-card" style={{ marginTop: 8, padding: 12 }}>
                <div style={{ color: 'var(--text-3)', fontSize: 12, marginBottom: 4 }}>回答</div>
                <div style={{ whiteSpace: 'pre-wrap', color: 'var(--text-1)' }}>{answer}</div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
