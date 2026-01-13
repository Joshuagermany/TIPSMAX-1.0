import React from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer } from 'recharts';
import { Evaluations } from '../types/analysis';

interface RadarChartProps {
  evaluations: Evaluations;
}

export const RadarChartComponent: React.FC<RadarChartProps> = ({ evaluations }) => {
  const data = [
    { subject: '기술성', value: evaluations.technology, fullMark: 100 },
    { subject: '사업성', value: evaluations.business, fullMark: 100 },
    { subject: '팀 역량', value: evaluations.team, fullMark: 100 },
    { subject: 'TIPS 적합성', value: evaluations.tipsFit, fullMark: 100 },
  ];

  return (
    <div className="w-full h-80">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart data={data}>
          <PolarGrid />
          <PolarAngleAxis dataKey="subject" tick={{ fill: '#374151', fontSize: 12 }} />
          <PolarRadiusAxis angle={90} domain={[0, 100]} tick={{ fill: '#6B7280', fontSize: 10 }} />
          <Radar
            name="평가 점수"
            dataKey="value"
            stroke="#0284c7"
            fill="#0284c7"
            fillOpacity={0.6}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
};
