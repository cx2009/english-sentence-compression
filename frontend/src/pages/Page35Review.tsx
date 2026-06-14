import React from 'react'
import { useNavigate, useLocation } from 'react-router-dom'

const MOCK_ERROR_GROUPS = [
  {
    tag: '定语从句',
    count: 2,
    items: [
      { sentence: 'The boy [who was running] in the park...', hint: '应该删掉 who was running，这是定语从句修饰 the boy' },
      { sentence: 'The book [that I bought] yesterday...', hint: '应该删掉 that I bought' },
    ],
  },
  {
    tag: '介词短语',
    count: 1,
    items: [
      { sentence: 'He arrived [in the morning]...', hint: '时间介词短语可删除' },
    ],
  },
]

interface LocationState {
  from?: 'targeted'
}

const Page35Review: React.FC = () => {
  const navigate = useNavigate()
  const location = useLocation()
  const state = location.state as LocationState | null
  const isTargeted = state?.from === 'targeted'

  return (
    <div className="flex flex-col min-h-screen px-4">
      <div className="py-4 text-center">
        <h2 className="text-lg font-bold text-gray-900">
          {isTargeted ? '针对性训练完成！' : '📋 今日错题回顾'}
        </h2>
      </div>

      <div className="flex-1 space-y-4">
        {/* 针对性训练反馈 */}
        {isTargeted && (
          <div className="bg-green-50 border border-green-200 rounded-xl p-4 mb-2">
            <p className="text-green-700 font-medium">🎉 太棒了！针对性训练完成</p>
            <p className="text-sm text-green-600 mt-1">你的薄弱知识点正在减少，继续保持！</p>
          </div>
        )}

        {/* 错题分组 */}
        {MOCK_ERROR_GROUPS.map((group) => (
          <div key={group.tag} className="bg-gray-50 rounded-xl p-4">
            <p className="text-sm font-bold text-gray-700 mb-3">
              {group.tag}（错{group.count}题）
            </p>
            {group.items.map((item, i) => (
              <div key={i} className="mb-3 last:mb-0">
                <p className="text-sm text-gray-900 mb-1">✘ {item.sentence}</p>
                <p className="text-xs text-gray-500 pl-3 border-l-2 border-blue-300">
                  {item.hint}
                </p>
              </div>
            ))}
          </div>
        ))}
      </div>

      {/* 底部操作 */}
      <div className="safe-area-bottom space-y-3 py-4">
        <button
          className="w-full py-3 bg-blue-600 text-white rounded-xl active:scale-95 transition-all"
          onClick={() => navigate('/train?mode=targeted&tag=定语从句')}
        >
          🔄 再来一组针对性训练
        </button>
        <button
          className="w-full py-3 border border-gray-300 text-gray-600 rounded-xl active:scale-95 transition-all"
          onClick={() => navigate('/score')}
        >
          查看评分分析
        </button>
      </div>
    </div>
  )
}

export default Page35Review
