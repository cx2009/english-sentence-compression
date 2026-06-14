// API 封装层，对接后端接口

const API_BASE = import.meta.env.VITE_API_BASE || '/api'

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options?.headers },
    ...options,
  })
  if (!res.ok) throw new Error(`API error: ${res.status}`)
  return res.json()
}

// 训练 API
export const trainingApi = {
  // 获取句子（支持 normal / targeted 模式）
  getSentence: (mode: string, tag?: string) =>
    request<import('../types').Sentence>(
      `/train/sentence?mode=${mode}${tag ? `&tag=${tag}` : ''}`
    ),
  // 提交训练结果
  submit: (data: {
    sentence_id: number
    deleted_words: number[]
    time_spent: number
    training_mode: string
  }) =>
    request<{
      record_id: number
      scores: {
        core_retention: number
        deletion_accuracy: number
        compression_index: number
      }
    }>('/train/submit', { method: 'POST', body: JSON.stringify(data) }),
  // 获取今日训练列表
  getDaily: () => request<{ sentences: import('../types').Sentence[]; completed: number[] }>('/train/daily'),
  // 获取针对性训练句子
  getTargeted: (tag: string) => request<import('../types').Sentence[]>(`/train/targeted?tag=${tag}`),
}

// 用户 API
export const userApi = {
  login: (code: string) =>
    request<{ openid: string }>('/user/login', { method: 'POST', body: JSON.stringify({ code }) }),
  profile: () => request<import('../types').User>('/user/profile'),
}

// 反馈 API
export const feedbackApi = {
  getFeedback: (recordId: number) =>
    request<import('../types').LLMFeedback>(`/feedback/${recordId}`),
}

// 错题 API
export const errorApi = {
  getReview: () => request<import('../types').ErrorReviewGroup[]>('/errors/review'),
}

// 支付 API
export const paymentApi = {
  createOrder: (product: string) =>
    request<{ order_id: string; prepay_id: string }>('/pay/create-order', {
      method: 'POST',
      body: JSON.stringify({ product }),
    }),
  checkOrder: (orderId: string) =>
    request<{ status: string }>(`/pay/check-order?order_id=${orderId}`),
}
