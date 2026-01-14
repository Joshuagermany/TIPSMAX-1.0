import React from 'react';

export const CompanyStatus: React.FC = () => {
  return (
    <div style={{ backgroundColor: '#000000', minHeight: '100%' }}>
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">기업 현황</h1>
          <p className="text-gray-400">분석 완료된 기업들의 현황을 확인할 수 있습니다.</p>
        </div>

        {/* 기업 현황 리스트 영역 */}
        <div className="bg-gray-900 rounded-lg shadow-sm border border-gray-700 p-8">
          <div className="text-center py-12">
            <p className="text-gray-400 text-lg">기업현황 없음</p>
          </div>
        </div>
      </div>
    </div>
  );
};
