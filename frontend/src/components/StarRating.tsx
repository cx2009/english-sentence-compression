import React from 'react'

interface StarRatingProps {
  label: string
  value: number  // 1-5
  hint: string
}

const StarRating: React.FC<StarRatingProps> = ({ label, value, hint }) => {
  return (
    <div>
      <div className="flex items-center justify-between mb-1">
        <span className="text-sm text-gray-600">{label}</span>
        <div className="flex gap-0.5">
          {[1, 2, 3, 4, 5].map((star) => (
            <span key={star} className={`text-lg ${star <= value ? 'text-yellow-400' : 'text-gray-200'}`}>
              ★
            </span>
          ))}
        </div>
      </div>
      <p className="text-xs text-gray-400 pl-1">{hint}</p>
    </div>
  )
}

export default StarRating
