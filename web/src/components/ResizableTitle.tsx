// 可调整列宽的表格表头单元格
// antd Table 的 components.header.cell 用它，实现列宽拖拽调节

import type { ReactNode } from 'react'
import { Resizable, type ResizeCallbackData } from 'react-resizable'
import 'react-resizable/css/styles.css'

interface ResizableTitleProps {
  children?: ReactNode
  width?: number   // 当前列宽
  onResize?: (e: unknown, data: ResizeCallbackData) => void
}

// 表头单元格：包一层可拖拽
export default function ResizableTitle({ children, width, onResize }: ResizableTitleProps) {
  if (!width) {
    return <th>{children}</th>   // 无宽度就不支持拖拽
  }
  return (
    // 用 Resizable 组件包裹：右侧拖拽手柄
    <Resizable width={width} height={0} onResize={onResize} >
      {/* 表头内容 + 拖拽手柄 */}
      <th style={{ position: 'relative' }}>{children}</th>
    </Resizable>
  )
}
