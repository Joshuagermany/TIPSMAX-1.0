import React from 'react';
import { AnalysisResult } from '../types/analysis';

interface ReportSectionProps {
  result: AnalysisResult;
}

export const ReportSection: React.FC<ReportSectionProps> = ({ result }) => {
  const getRecommendationColor = (rec: string) => {
    switch (rec) {
      case '추천':
        return 'bg-green-100 text-green-800 border-green-300';
      case '보류':
        return 'bg-yellow-100 text-yellow-800 border-yellow-300';
      case '비추천':
        return 'bg-red-100 text-red-800 border-red-300';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  return (
    <div className="space-y-6">
      {/* 기업 요약 */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">기업 요약</h3>
        <p className="text-gray-700 leading-relaxed whitespace-pre-line">
          {result.companySummary}
        </p>
      </div>

      {/* 종합 판단 */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">종합 판단</h3>
        <div className="flex items-center gap-4">
          <span
            className={`px-4 py-2 rounded-lg border font-semibold ${getRecommendationColor(
              result.recommendation
            )}`}
          >
            {result.recommendation}
          </span>
          <span className="text-sm text-gray-600">
            종합 점수: <span className="font-semibold">{result.overallScore}점</span>
          </span>
        </div>
      </div>

      {/* 강점 */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">핵심 강점 TOP 3</h3>
        <ul className="space-y-3">
          {result.strengths.map((strength, index) => (
            <li key={index} className="flex items-start gap-3">
              <span className="flex-shrink-0 w-6 h-6 bg-green-100 text-green-700 rounded-full flex items-center justify-center text-sm font-semibold">
                {index + 1}
              </span>
              <span className="text-gray-700">{strength}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* 리스크 */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">주요 리스크 TOP 3</h3>
        <ul className="space-y-3">
          {result.risks.map((risk, index) => (
            <li key={index} className="flex items-start gap-3">
              <span className="flex-shrink-0 w-6 h-6 bg-red-100 text-red-700 rounded-full flex items-center justify-center text-sm font-semibold">
                {index + 1}
              </span>
              <span className="text-gray-700">{risk}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* 심사역 코멘트 */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">심사역 코멘트</h3>
        <div className="bg-gray-50 rounded-lg p-4 border-l-4 border-primary-500">
          <p className="text-gray-700 leading-relaxed whitespace-pre-line">
            {result.comments}
          </p>
        </div>
      </div>
    </div>
  );
};
