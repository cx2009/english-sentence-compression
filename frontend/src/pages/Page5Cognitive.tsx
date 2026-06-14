import React from 'react'
import { useNavigate } from 'react-router-dom'

const Page5Cognitive: React.FC = () => {
  const navigate = useNavigate()

  return (
    <div className="flex flex-col min-h-screen px-6 items-center justify-center">
      <h1 className="text-2xl font-bold text-gray-900 mb-4 text-center">
        为什么你英语读得慢？
      </h1>

      <div className="space-y-3 text-center mb-8">
        <p className="text-gray-400 line-through text-lg">不是单词不够</p>
        <p className="text-gray-400 line-through text-lg">不是语法不行</p>
        <p className="text-xl font-bold text-gray-900 mt-6">是你在读"所有信息"</p>
        <div className="mt-4 p-4 bg-blue-50 rounded-xl">
          <p className="text-sm text-blue-700">
            而高分学生只读：
          </p>
          <p className="text-lg font-bold text-blue-800 mt-1">
            👉 主干 + 动词 + 结果
          </p>
        </div>
      </div>

      <div className="safe-area-bottom w-full space-y-3">
        <button
          className="w-full py-3 bg-blue-600 text-white rounded-xl active:scale-95 transition-all"
          onClick={() => navigate('/pay')}
        >
          开始7天训练 →
        </button>
        <button
          className="w-full py-3 text-gray-400 text-sm active:scale-95 transition-all"
          onClick={() => navigate('/')}
        >
          [ 领取我的能力诊断报告 ]
        </button>
      </div>
    </div>
  )
}

export default Page5Cognitive
