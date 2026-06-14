import React from 'react'
import { useNavigate } from 'react-router-dom'

const Page1Entry: React.FC = () => {
  const navigate = useNavigate()

  return (
    <div className="flex flex-col items-center justify-center min-h-screen px-6 bg-gradient-to-b from-blue-50 to-white">
      <div className="text-5xl mb-6">📖</div>
      <h1 className="text-2xl font-bold text-center text-gray-900 mb-3 leading-snug">
        ❗90%学生英语慢，<br />是因为不会"删词读句子"
      </h1>
      <p className="text-base text-gray-500 mb-8 text-center">
        用3分钟测试你的阅读压缩能力
      </p>
      <button
        className="w-full max-w-xs bg-blue-600 text-white text-lg font-medium py-4 px-8 rounded-xl shadow-lg shadow-blue-200 active:scale-95 transition-all"
        onClick={() => navigate('/train')}
      >
        👉 开始训练
      </button>
    </div>
  )
}

export default Page1Entry
