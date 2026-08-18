// 文库页：上传 PDF + 文献列表 + 删除
// 用 antd Upload（上传）+ Table（列表）+ 玻璃卡片

import { useEffect, useState } from 'react'
import { Upload, Button, Table, Popconfirm, message, Dropdown, Checkbox } from 'antd'
import { UploadOutlined, DeleteOutlined, SettingOutlined } from '@ant-design/icons'
import type { ColumnsType } from 'antd/es/table'
import { listPapers, uploadPaper, deletePaper, type Paper } from '../../api/papers'

// 可显示的列（key 与 dataIndex 对应），用于列显隐控制
const ALL_COLUMNS = [
  { key: 'title', label: '标题' },
  { key: 'authors', label: '作者' },
  { key: 'year', label: '年份' },
  { key: 'status', label: '状态' },
  { key: 'action', label: '操作' },
]

// 文库页组件
export default function PapersPage() {
  // 文献列表
  const [papers, setPapers] = useState<Paper[]>([])
  // 加载态
  const [loading, setLoading] = useState(false)
  // 显示的列（默认全部）
  const [visibleKeys, setVisibleKeys] = useState<string[]>(ALL_COLUMNS.map(c => c.key))

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

  // 双击标题打开 PDF
  function openPdf(paperId: string) {
    // 打开后端的 PDF 下载接口（浏览器新窗口预览）
    window.open(`/api/papers/${paperId}/pdf`, '_blank')
  }

  // 表格列定义（标题/作者列自适应；columns 带 key，用于列显隐过滤）
  const allColumns: ColumnsType<Paper> = [
    // 标题列：自适应宽度，ellipsis 保持一行；双击打开 PDF
    { key: 'title', title: '标题', dataIndex: 'title', ellipsis: true,
      render: (t, record) => (
        <span
          title="双击打开 PDF"
          onDoubleClick={() => openPdf(record.paper_id)}
          style={{ cursor: 'pointer', color: 'var(--text-1)' }}
        >
          {t || '(未命名)'}
        </span>
      ) },
    // 作者列：自适应，ellipsis 保持一行
    { key: 'authors', title: '作者', dataIndex: 'authors', ellipsis: true,
      render: (a) => a || '—' },
    // 年份：固定窄列
    { key: 'year', title: '年份', dataIndex: 'year', width: 70,
      render: (y) => y || '—' },
    { key: 'status', title: '状态', dataIndex: 'status', width: 90 },
    { key: 'action', title: '操作', width: 70,
      render: (_, record) => (
        <Popconfirm title="确认删除这篇文献？" onConfirm={() => handleDelete(record.paper_id)}>
          <Button type="text" danger icon={<DeleteOutlined />} />
        </Popconfirm>
      ) },
  ]
  // 按用户勾选的列过滤（hidden 掉未选的）
  const columns = allColumns.filter(col => visibleKeys.includes(String(col.key)))

  return (
    <div>
      {/* 标题 + 上传按钮 + 列设置 */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <h2 style={{ color: 'var(--text-1)', margin: 0 }}>文库</h2>
        <div style={{ display: 'flex', gap: 8 }}>
          {/* 列设置：勾选显示哪些列 */}
          <Dropdown
            trigger={['click']}
            dropdownRender={() => (
              <div className="glass-card" style={{ padding: 12 }}>
                <Checkbox.Group
                  value={visibleKeys}
                  onChange={(keys) => setVisibleKeys(keys as string[])}
                  options={ALL_COLUMNS.map(c => ({ value: c.key, label: c.label }))}
                />
              </div>
            )}
          >
            <Button icon={<SettingOutlined />}>列设置</Button>
          </Dropdown>
          {/* 导入 PDF */}
          <Upload accept=".pdf" showUploadList={false} beforeUpload={handleUpload}>
            <Button type="primary" icon={<UploadOutlined />}>导入 PDF</Button>
          </Upload>
        </div>
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
