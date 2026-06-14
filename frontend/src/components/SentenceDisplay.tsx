import React from 'react'

interface SentenceDisplayProps {
  /** 英文句子 */
  text: string
  /** 每个词的标记状态：true=灰字+删除线 */
  wordStates: boolean[]
  /** 点击词的回调 */
  onToggle: (index: number) => void
  /** 是否可交互（完成后锁定） */
  disabled?: boolean
  /** 是否展示为对比模式（三色高亮） */
  comparison?: {
    /** 标准答案的保留词索引 */
    coreIndices: number[]
    /** 用户标记为删除的词索引 */
    userDeleted: number[]
  }
}

/**
 * 核心组件：句子展示 + 点击交互
 *
 * 交互模式（两态切换）：
 * - 点击词 → 黑字 ↔ 灰字+删除线 切换
 *
 * 对比模式（三色高亮）：
 * - 绿色：用户正确删除的干扰词
 * - 红色：用户错误删除的核心词
 * - 黄色：用户遗漏未删的干扰词
 */
const SentenceDisplay: React.FC<SentenceDisplayProps> = ({
  text,
  wordStates,
  onToggle,
  disabled = false,
  comparison,
}) => {
  const words = text.split(' ')

  if (comparison) {
    const { coreIndices, userDeleted } = comparison
    return (
      <div className="text-lg leading-8 px-4 py-6">
        {words.map((word, index) => {
          const isCore = coreIndices.includes(index)
          const isDeleted = userDeleted.includes(index)
          let className = 'word-token '

          if (isDeleted && !isCore) {
            // 用户正确删除的干扰词 → 绿色
            className += 'word-correct-delete'
          } else if (isDeleted && isCore) {
            // 用户错误删除的核心词 → 红色
            className += 'word-false-delete'
          } else if (!isDeleted && !isCore) {
            // 用户遗漏未删的干扰词 → 黄色背景
            className += 'word-missed-delete'
          } else {
            // 用户正确保留的核心词 → 正常
            className += 'text-gray-900'
          }

          return (
            <span key={index} className={className}>
              {word}{' '}
            </span>
          )
        })}
      </div>
    )
  }

  return (
    <div className="text-lg leading-8 px-4 py-6 select-none">
      {words.map((word, index) => (
        <span
          key={index}
          className={`word-token ${wordStates[index] ? 'deleted' : 'text-gray-900'}`}
          onClick={() => !disabled && onToggle(index)}
        >
          {word}{' '}
        </span>
      ))}
    </div>
  )
}

export default SentenceDisplay
