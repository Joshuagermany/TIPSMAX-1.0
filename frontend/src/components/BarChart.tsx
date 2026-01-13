import React from 'react';
import { BarChart as RechartsBarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { TipsCategoryScore } from '../types/analysis';

interface BarChartProps {
  categories: TipsCategoryScore[];
}

export const BarChartComponent: React.FC<BarChartProps> = ({ categories }) => {
  // 점수가 0보다 큰 항목만 필터링하고 내림차순 정렬
  const filteredData = categories
    .filter(item => item.score > 0)
    .sort((a, b) => b.score - a.score)
    .map(item => ({
      name: item.category,
      score: item.score,
    }));

  return (
    <div className="w-full h-96">
      <ResponsiveContainer width="100%" height="100%">
        <RechartsBarChart
          data={filteredData}
          layout="vertical"
          margin={{ top: 5, right: 30, left: 100, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis type="number" domain={[0, 100]} tick={{ fill: '#6B7280', fontSize: 12 }} />
          <YAxis
            type="category"
            dataKey="name"
            tick={{ fill: '#374151', fontSize: 11 }}
            width={90}
          />
          <Tooltip
            formatter={(value: number) => [`${value}점`, '적합도']}
            contentStyle={{ backgroundColor: '#fff', border: '1px solid #e5e7eb', borderRadius: '6px' }}
          />
          <Bar dataKey="score" fill="#0284c7" radius={[0, 4, 4, 0]} />
        </RechartsBarChart>
      </ResponsiveContainer>
    </div>
  );
};
