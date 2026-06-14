import React, { useEffect, useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import SentenceDisplay from '../components/SentenceDisplay'
import { useTraining } from '../hooks/useTraining'

const Page2Training: React.FC = () => {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const mode = (searchParams.get('mode') as 'normal' | 'targeted') || 'normal'
  const tag = searchParams.get('tag') || undefined

  const {
    sentence, wordStates, timeSpent, isLoading, error,
    loadSentence, toggleWord, reset, submit,
  } = useTraining()

  useEffect(() => {
    loadSentence(mode, tag)
  }, [mode, tag, loadSentence])

  const handleSubmit = () => {
    const data = submit()
    // 标记用户是否为空提交
    if (data.deleted_words.length === wordStates.length) {
      alert('请至少保留一个核心词')
      return
    }
    navigate(`/compare?sentence_id=${data.sentence_id}`, {
      state: {
        trainingData: data,
        wordStates,
        mode,
        sentenceText: sentence!.content,
        coreIndices: sentence!.core_indices,
      },
    })
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p className="text-gray-400">加载中...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p className="text-red-500">{error}</p>
      </div>
    )
  }

  return (
    <div className="flex flex-col min-h-screen px-4">
      {/* 顶部：训练模式标识 + 计时 */}
      <div className="flex justify-between items-center py-4 text-sm text-gray-400">
        <span className="bg-gray-100 px-3 py-1 rounded-full text-xs">
          {mode === 'targeted' ? `针对性训练（${tag}）` : '正常训练'}
        </span>
        <span>{timeSpent}s</span>
      </div>

      {/* 句子展示区 */}
      <div className="flex-1 flex items-center justify-center">
        {sentence && (
          <SentenceDisplay
            text={sentence.content}
            wordStates={wordStates}
            onToggle={toggleWord}
          />
        )}
      </div>

      {/* 底部操作栏 */}
      <div className="safe-area-bottom flex gap-3 py-4">
        <button
          className="flex-1 py-3 px-6 border border-gray-300 text-gray-600 rounded-xl active:scale-95 transition-all"
          onClick={reset}
        >
          重置
        </button>
        <button
          className="flex-1 py-3 px-6 bg-blue-600 text-white rounded-xl shadow-lg shadow-blue-200 active:scale-95 transition-all"
          onClick={handleSubmit}
        >
          提交
        </button>
      </div>
    </div>
  )
}

export default Page2Training
