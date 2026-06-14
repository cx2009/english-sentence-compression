import React from 'react'
import { useNavigate } from 'react-router-dom'
import StarRating from '../components/StarRating'

const Page4Scoring: React.FC = () => {
  const navigate = useNavigate()
  const [showFullFeedback] = React.useState(false) // 付费用户=true

  return (
    <div className="flex flex-col min-h-screen px-4">
      <div className="py-4 text-center">
        <h2 className="text-lg font-bold text-gray-900">📊 你的阅读压缩能力</h2>
      </div>

      <div className="flex-1 space-y-6">
        {/* 评分展示 */}
        <div className="bg-gray-50 rounded-xl p-4 space-y-4">
          <StarRating label="识别速度" value={2} hint="你还会被时间地点带跑" />
          <StarRating label="结构抓取" value={3} hint="你能抓住主干，这很棒" />
          <StarRating label="信息过滤" value={2} hint="修饰信息仍会干扰你" />
          <div className="pt-2 text-center">
            <p className="text-sm text-gray-400">当前水平：70分区间常见水平</p>
            <p className="text-sm text-blue-600 mt-2 font-medium">
              你的训练重点：在抓住主干后，更果断地舍弃"何时、何地"等细节
            </p>
          </div>
        </div>

        {/* LLM 反馈区域（PRD 模块五） */}
        <div className="bg-indigo-50 rounded-xl p-4">
          <p className="text-sm font-bold text-gray-700 mb-2">🤖 你的薄弱知识点</p>
          {showFullFeedback ? (
            <div className="space-y-3">
              <div>
                <p className="text-sm text-red-600">✘ 定语从句识别 — 漏删了"who was running in the park"</p>
                <p className="text-xs text-gray-500 mt-1">定语从句修饰名词，在阅读压缩时通常可以整体删除，只保留被修饰的名词即可。</p>
              </div>
              <div>
                <p className="text-sm text-yellow-600">✘ 时间状语"yesterday"未识别为干扰</p>
                <p className="text-xs text-gray-500 mt-1">时间地点信息在阅读时通常可以忽略。</p>
              </div>
              <div className="pt-2">
                <p className="text-xs text-gray-400">📚 建议复习：定语从句基础</p>
              </div>
            </div>
          ) : (
            <div>
              <div className="space-y-2 opacity-50 pointer-events-none">
                <div className="h-4 bg-indigo-200 rounded w-3/4" />
                <div className="h-4 bg-indigo-200 rounded w-1/2" />
                <div className="h-4 bg-indigo-200 rounded w-2/3" />
              </div>
              <button
                className="mt-3 w-full py-3 bg-indigo-600 text-white rounded-xl text-sm active:scale-95 transition-all"
                onClick={() => navigate('/pay')}
              >
                🔒 解锁完整知识点分析
              </button>
            </div>
          )}
        </div>
      </div>

      {/* 底部 */}
      <div className="safe-area-bottom space-y-3 py-4">
        <button
          className="w-full py-3 bg-blue-600 text-white rounded-xl active:scale-95 transition-all"
          onClick={() => navigate('/cognitive')}
        >
          查看分析报告
        </button>
      </div>
    </div>
  )
}

export default Page4Scoring
