// 文献库接口封装：upload/list/delete/update
// 对接后端 /api/papers*

// 导入基础请求
import { request } from './client'

// 文献列表项结构
export interface Paper {
  paper_id: string       // 文献 id
  title: string          // 标题
  authors: string        // 作者
  year: string           // 年份
  status: string         // 状态（待读/在读/读完/重点）
  has_pdf: boolean       // 是否有 PDF
}

// 上传 PDF（multipart 表单，文件字段名 file）
// params: file 选中的 PDF 文件
export async function uploadPaper(file: File): Promise<{ paper_id: string }> {
  // 构造 FormData（multipart 上传）
  const form = new FormData()
  form.append('file', file)
  // 发上传请求（multipart 不用 JSON 头）
  const res = await fetch('/api/papers/upload', {
    method: 'POST',
    body: form,
  })
  if (!res.ok) {
    throw new Error(`上传失败: ${res.status}`)
  }
  return await res.json()
}

// 文献列表
export async function listPapers(): Promise<Paper[]> {
  return await request<Paper[]>('/api/papers')
}

// 删除文献
export async function deletePaper(paperId: string): Promise<void> {
  await request(`/api/papers/${paperId}`, { method: 'DELETE' })
}
