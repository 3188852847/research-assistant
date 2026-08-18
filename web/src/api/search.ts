// 检索接口封装：GET /api/search
import { request } from './client'

// 检索命中项
export interface SearchHit {
  paper_id: string        // 文献 id
  title: string           // 标题
  matched_field: string   // 命中字段（research_question 等）
  snippet: string         // 命中片段
}

// 检索：按关键词扫 Analysis
export async function searchPapers(q: string): Promise<SearchHit[]> {
  return await request<SearchHit[]>(`/api/search?q=${encodeURIComponent(q)}`)
}
