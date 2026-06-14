// PRD §9.3 核心数据表对应的 TypeScript 类型

/** 句子 */
export interface Sentence {
  id: number
  content: string
  difficulty: '简单' | '中等' | '高考'
  core_indices: number[]   // 标准压缩版本保留词索引
  tags: string[]           // 知识点标签
  analysis?: {
    subject: string
    predicate: string
    modifiers: string[]
  }
}

/** 训练记录 */
export interface TrainingRecord {
  id: number
  user_id: string
  sentence_id: number
  training_mode: 'normal' | 'targeted'
  deleted_words: number[]          // 用户删除的词索引
  score_core_retention: number     // 核心保留率 0-100
  score_deletion_accuracy: number  // 删除正确率 0-100
  time_spent: number               // 秒
  compression_index: number        // 阅读压缩指数
  errors?: TrainingError[]
  error_tags?: string[]
  created_at: string
}

/** 错误详情 */
export interface TrainingError {
  type: 'false_delete' | 'missed_delete'
  word: string
  index: number
  explanation: string
}

/** LLM 反馈 */
export interface LLMFeedback {
  weak_points: WeakPoint[]
  overall_assessment: string
  review_suggestion: string
  next_focus: string
}

export interface WeakPoint {
  tag: string
  severity: 'high' | 'medium' | 'low'
  feedback: string
  missed_words?: string[]
  false_deleted_words?: string[]
  is_praise?: boolean
}

/** 错题聚合（模块六） */
export interface ErrorReviewGroup {
  tag: string
  count: number
  errors: ReviewedError[]
}

export interface ReviewedError {
  sentence: string
  error_type: 'missed_delete' | 'false_delete'
  user_action: string
  correct_action: string
  words: string[]
}

/** 用户 */
export interface User {
  openid: string
  level: number
  paid: boolean
  paid_expire_at?: string
  created_at: string
}

/** 训练模式 */
export type TrainingMode = 'normal' | 'targeted'

/** 评分维度 */
export interface ScoreDimensions {
  recognition_speed: number    // 1-5 星
  structure_grasp: number
  info_filtering: number
  overall_level: string
  training_focus: string
}
