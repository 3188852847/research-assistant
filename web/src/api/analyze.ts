// 速拆接口封装：POST /api/analyze
// 对接后端 api/analyze.py

import { request } from './client'

// 速拆结果（四字段契约，对齐功能规划 Analysis 字段）
export interface Analysis {
  paper_id: string             // 文献 id
  research_question: string    // 研究问题
  core_conclusion: string      // 核心结论
  limitations: string          // 研究局限（作者原话）
  questions: string            // 我的疑问
  created_at?: string          // 速拆时间
}

// 触发速拆（后端跑 agent，可能耗时较长）
// params: paperId 文献 id
// 返回: 速拆结果 + 报告全文
export async function runAnalyze(paperId: string): Promise<{ paper_id: string; analysis: Analysis; report: string }> {
  return await request('/api/analyze', {
    method: 'POST',
    body: { paper_id: paperId },
  })
}

// 流式速拆：POST /api/analyze/stream（SSE 逐条推工具调用卡片）
// params: paperId, 三个回调
//   onToolCall(工具名, 参数)   渲染工具卡片
//   onProgress(进度行)        渲染进度
//   onDone(analysis, report)  完成（四字段+报告）
export async function runAnalyzeStream(
  paperId: string,
  onToolCall: (tool: string, args: Record<string, unknown>) => void,
  onProgress: (line: string) => void,
  onDone: (analysis: Analysis, report: string) => void,
): Promise<void> {
  const res = await fetch('/api/analyze/stream', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ paper_id: paperId }),
  })
  if (!res.ok || !res.body) throw new Error('流式速拆失败')

  const reader = res.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''

  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    buffer += decoder.decode(value, { stream: true })
    const messages = buffer.split('\n\n')
    buffer = messages.pop() ?? ''
    for (const msg of messages) {
      if (!msg.startsWith('data: ')) continue
      const payload = JSON.parse(msg.slice(6))
      switch (payload.type) {
        case 'tool_call': onToolCall(payload.tool, payload.args); break
        case 'progress': onProgress(payload.line); break
        case 'done': onDone(payload.analysis, payload.report); break
      }
    }
  }
}
