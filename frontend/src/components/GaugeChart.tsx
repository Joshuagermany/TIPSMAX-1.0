import React from 'react';

interface GaugeChartProps {
  score: number; // 0-100
  label?: string;
}

export const GaugeChart: React.FC<GaugeChartProps> = ({ score, label = '종합 점수' }) => {
  const percentage = Math.min(100, Math.max(0, score));
  const circumference = 2 * Math.PI * 90; // radius = 90
  const offset = circumference - (percentage / 100) * circumference;

  // 색상 결정
  let color = '#10b981'; // green
  if (percentage < 40) {
    color = '#ef4444'; // red
  } else if (percentage < 70) {
    color = '#f59e0b'; // yellow
  }

  return (
    <div className="flex flex-col items-center justify-center">
      <div className="relative w-64 h-64">
        <svg className="transform -rotate-90 w-64 h-64">
          {/* 배경 원 */}
          <circle
            cx="128"
            cy="128"
            r="90"
            stroke="#e5e7eb"
            strokeWidth="16"
            fill="none"
          />
          {/* 진행 원 */}
          <circle
            cx="128"
            cy="128"
            r="90"
            stroke={color}
            strokeWidth="16"
            fill="none"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            strokeLinecap="round"
            className="transition-all duration-500"
          />
        </svg>
        {/* 중앙 텍스트 */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-5xl font-bold" style={{ color }}>
            {Math.round(percentage)}
          </span>
          <span className="text-sm text-gray-500 mt-1">{label}</span>
        </div>
      </div>
    </div>
  );
};
