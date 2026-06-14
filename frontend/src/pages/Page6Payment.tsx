import React from 'react'
import { useNavigate } from 'react-router-dom'

const Page6Payment: React.FC = () => {
  const navigate = useNavigate()

  return (
    <div className="flex flex-col min-h-screen px-6">
      <div className="flex-1 flex flex-col justify-center">
        <div className="text-center mb-8">
          <p className="text-sm text-gray-400 mb-4">
            你刚完成的，不是"一句训练"，<br />
            而是一次"阅读方式的诊断"。
          </p>
          <p className="text-sm text-gray-500 mb-6">
            诊断结果很清楚：你的大脑会自动去读所有词，<br />
            这是你英语慢的唯一原因。
          </p>
          <p className="text-base text-gray-700 mb-6">
            接下来的7天，我们要给你的大脑装上一个"信息过滤器"。
          </p>
        </div>

        <div className="bg-gray-50 rounded-xl p-6 mb-6">
          <h3 className="text-lg font-bold text-gray-900 text-center mb-4">
            【7天阅读压缩训练系统】
          </h3>
          <p className="text-sm text-gray-500 text-center mb-4">
            不是教你英语，是训练你"像扫描仪一样读句子"
          </p>
          <ul className="space-y-3 text-sm text-gray-600">
            <li className="flex items-start gap-2">
              <span className="text-blue-500">·</span>
              每天3篇真题句子，刻意练习"找主干-删干扰"
            </li>
            <li className="flex items-start gap-2">
              <span className="text-blue-500">·</span>
              自动计时，速度提升肉眼可见
            </li>
            <li className="flex items-start gap-2">
              <span className="text-blue-500">·</span>
              错题类型记录，系统会盯着你的弱点反复练
            </li>
          </ul>
        </div>

        <div className="text-center mb-6">
          <p className="text-3xl font-bold text-blue-600">29<span className="text-lg">元</span></p>
          <p className="text-xs text-gray-400 mt-2">一杯奶茶的价格，换一个阅读速度快2倍的机会</p>
        </div>
      </div>

      <div className="safe-area-bottom space-y-3 py-4">
        <button
          className="w-full py-4 bg-blue-600 text-white text-lg font-medium rounded-xl shadow-lg shadow-blue-200 active:scale-95 transition-all"
          onClick={() => {
            // TODO: 调起微信支付
            alert('支付功能开发中...')
          }}
        >
          [ 开始7天训练 ]
        </button>
        <p className="text-xs text-gray-300 text-center">
          支付即表示同意《服务协议》
        </p>
      </div>
    </div>
  )
}

export default Page6Payment
