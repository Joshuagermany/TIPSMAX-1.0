import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { AnalysisResult } from '../types/analysis';
import { RadarChartComponent } from '../components/RadarChart';
import { GaugeChart } from '../components/GaugeChart';
import { BarChartComponent } from '../components/BarChart';
import { ReportSection } from '../components/ReportSection';

export const Results: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { result, filename } = location.state as { result: AnalysisResult; filename: string };

  if (!result) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600 mb-4">분석 결과를 찾을 수 없습니다.</p>
          <button
            onClick={() => navigate('/')}
            className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
          >
            홈으로 돌아가기
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* 헤더 */}
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">분석 결과</h1>
            <p className="text-gray-600">{filename}</p>
          </div>
          <button
            onClick={() => navigate('/')}
            className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
          >
            새로 분석하기
          </button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Radar Chart */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">4가지 관점 평가</h2>
            <RadarChartComponent evaluations={result.evaluations} />
          </div>

          {/* Gauge Chart */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 flex items-center justify-center">
            <div>
              <h2 className="text-lg font-semibold text-gray-900 mb-4 text-center">
                종합 TIPS 적합도
              </h2>
              <GaugeChart score={result.overallScore} />
            </div>
          </div>
        </div>

        {/* Bar Chart */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">TIPS 분야별 적합도</h2>
          <BarChartComponent categories={result.tipsCategories} />
        </div>

        {/* 리포트 섹션 */}
        <ReportSection result={result} />
      </div>
    </div>
  );
};
