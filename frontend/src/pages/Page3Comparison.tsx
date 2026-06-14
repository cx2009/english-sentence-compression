import React from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import SentenceDisplay from '../components/SentenceDisplay'
import type { TrainingMode } from '../types'

interface LocationState {
  trainingData?: { sentence_id: number; deleted_words: number[]; time_spent: number }
  wordStates?: boolean[]
  mode?: TrainingMode
  sentenceText?: string
  coreIndices?: number[]
}

const Page3Comparison: React.FC = () => {
  const navigate = useNavigate()
  const location = useLocation()
  const state = location.state as LocationState | null
  const isTargeted = state?.mode === 'targeted'

  const sentenceText = state?.sentenceText || ''
  const coreIndices = state?.coreIndices || []
  const userDeleted = state?.wordStates
    ?.map((v, i) => (v ? i : -1))
    .filter(i => i !== -1) || []

  // 分析错误类型
  const coreSet = new Set(coreIndices)
  const deletedSet = new Set(userDeleted)
  const falselyDeleted = userDeleted.filter(i => coreSet.has(i))
  const missedDeleted = [...coreSet].filter(i => !deletedSet.has(i))
  const correctDeleted = userDeleted.filter(i => !coreSet.has(i))

  return (
    <div className="flex flex-col min-h-screen px-4">
      <div className="py-4 text-center">
        <h2 className="text-lg font-bold text-gray-900">标准答案对比</h2>
      </div>

      <div className="flex-1 space-y-6">
        {/* 左侧：用户版本 */}
        <div className="bg-gray-50 rounded-xl p-4">
          <p className="text-sm text-gray-400 mb-2">你的压缩版本</p>
          <SentenceDisplay
            text={sentenceText}
            wordStates={state?.wordStates || []}
            onToggle={() => {}}
            disabled
            comparison={{ coreIndices, userDeleted }}
          />
        </div>

        {/* 右侧：标准版本 */}
        <div className="bg-gray-50 rounded-xl p-4">
          <p className="text-sm text-gray-400 mb-2">系统标准压缩版本</p>
          <SentenceDisplay
            text={sentenceText}
            wordStates={[]}
            onToggle={() => {}}
            disabled
            comparison={{ coreIndices, userDeleted: [] }}
          />
        </div>

        {/* 差异分析 */}
        <div className="bg-green-50 rounded-xl p-4">
          <p className="text-sm font-medium text-gray-700 mb-2">差异分析</p>
          <p className="text-sm text-gray-600 mb-1">
            ✔ 正确删除干扰词：{correctDeleted.length} 个
          </p>
          {falselyDeleted.length > 0 && (
            <p className="text-sm text-red-500 mb-1">
              ✘ 错误删除核心词：{falselyDeleted.length} 个
            </p>
          )}
          {missedDeleted.length > 0 && (
            <p className="text-sm text-yellow-600">
              ⚠ 遗漏未删干扰词：{missedDeleted.length} 个
            </p>
          )}
        </div>
      </div>

      {/* 底部按钮 */}
      <div className="safe-area-bottom py-4">
        <button
          className="w-full py-3 bg-blue-600 text-white rounded-xl active:scale-95 transition-all"
          onClick={() => {
            if (isTargeted) {
              navigate('/error-review', { state: { from: 'targeted' } })
            } else {
              navigate('/error-review')
            }
          }}
        >
          查看错题分析
        </button>
      </div>
    </div>
  )
}

export default Page3Comparison
