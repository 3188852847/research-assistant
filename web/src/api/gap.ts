// Gap 接口封装：POST /api/gap
import { request } from './client'

// 触发 Gap 发现（选多篇文献横向对比）
export async function runGap(paperIds: string[]): Promise<{ paper_ids: string[]; gap_report: string }> {
  return await request('/api/gap', {
    method: 'POST',
    body: { paper_ids: paperIds },
  })
}
