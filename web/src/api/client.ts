// 基础请求封装：统一 fetch 的 JSON 请求 + 错误处理
// 各 api/xxx.ts 基于它封装具体接口

// 通用 JSON 请求函数
// params: path 接口路径, options（可选）method/body
// 返回: 解析后的 JSON（泛型 T 指定结构）
export async function request<T = unknown>(
  path: string,
  options: { method?: string; body?: unknown } = {},
): Promise<T> {
  // 组装请求配置
  const config: RequestInit = {
    method: options.method ?? 'GET',   // 默认 GET
    headers: {},                        // 请求头（下面看 body 再加）
  }

  // 有 body 时设置 JSON 头 + 序列化 body
  if (options.body !== undefined) {
    config.headers = { 'Content-Type': 'application/json' }
    config.body = JSON.stringify(options.body)
  }

  // 发请求
  const res = await fetch(path, config)

  // 非 2xx 状态：抛错（显示状态）
  if (!res.ok) {
    throw new Error(`请求失败: ${res.status} ${res.statusText}`)
  }

  // 解析 JSON 返回
  return await res.json() as T
}
