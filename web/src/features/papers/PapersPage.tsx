// 文库页：上传 PDF + 文献列表 + 删除
// 用 antd Upload（上传）+ Table（列表）+ 玻璃卡片

import { useEffect, useState } from 'react'
import { Upload, Button, Table, Popconfirm, message } from 'antd'
import { UploadOutlined, DeleteOutlined } from '@ant-design/icons'
import type { ColumnsType } from 'antd/es/table'
import { listPapers, uploadPaper, deletePaper, type Paper } from '../../api/papers'

// 文库页组件
export default function PapersPage() {
  // 文献列表
  const [papers, setPapers] = useState<Paper[]>([])
  // 加载态
  const [loading, setLoading] = useState(false)

  // 加载文献列表
  async function load() {
    setLoading(true)
    try {
      const data = await listPapers()
      setPapers(data)
    } catch (err) {
      console.error('加载文献失败:', err)
    } finally {
      setLoading(false)
    }
  }

  // 首次挂载加载
  useEffect(() => { load() }, [])

  // 上传回调（antd Upload 的自定义上传）
  async function handleUpload(file: File) {
    try {
      await uploadPaper(file)
      message.success('上传成功')
      load()   // 刷新列表
    } catch (err) {
      message.error('上传失败')
      console.error(err)
    }
    // 返回 false 阻止 antd 默认上传（我们手动传了）
    return false
  }

  // 删除回调
  async function handleDelete(paperId: string) {
    try {
      await deletePaper(paperId)
      message.success('已删除')
      load()
    } catch (err) {
      message.error('删除失败')
    }
  }

  // 表格列定义
  const columns: ColumnsType<Paper> = [
    { title: '标题', dataIndex: 'title', key: 'title', ellipsis: true,
      render: (t) => t || '(未命名)' },
    { title: '作者', dataIndex: 'authors', key: 'authors', width: 180,
      render: (a) => a || '—' },
    { title: '年份', dataIndex: 'year', key: 'year', width: 80,
      render: (y) => y || '—' },
    { title: '状态', dataIndex: 'status', key: 'status', width: 100 },
    { title: '操作', key: 'action', width: 80,
      render: (_, record) => (
        <Popconfirm title="确认删除这篇文献？" onConfirm={() => handleDelete(record.paper_id)}>
          <Button type="text" danger icon={<DeleteOutlined />} />
        </Popconfirm>
      ) },
  ]

  return (
    <div>
      {/* 标题 + 上传按钮 */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <h2 style={{ color: 'var(--text-1)', margin: 0 }}>文库</h2>
        {/* 上传 PDF（拖拽或点击） */}
        <Upload accept=".pdf" showUploadList={false} beforeUpload={handleUpload}>
          <Button type="primary" icon={<UploadOutlined />}>导入 PDF</Button>
        </Upload>
      </div>

      {/* 文献列表（玻璃卡片包一层） */}
      <div className="glass-card" style={{ padding: 0, overflow: 'hidden' }}>
        <Table
          rowKey="paper_id"
          columns={columns}
          dataSource={papers}
          loading={loading}
          pagination={false}
          locale={{ emptyText: '暂无文献，点击上方「导入 PDF」添加' }}
        />
      </div>
    </div>
  )
}
