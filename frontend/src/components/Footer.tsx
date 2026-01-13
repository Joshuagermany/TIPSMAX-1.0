import React from 'react';

export const Footer: React.FC = () => {
  return (
    <footer className="text-gray-300 mt-auto" style={{ backgroundColor: '#343333' }}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* 회사 정보 */}
          <div>
            <h3 className="text-white font-semibold mb-4 text-lg">COMMAX VENTURUS</h3>
            <p className="text-sm text-gray-400 mb-2">
              VC 심사역을 위한 스타트업 문서 분석 도구
            </p>
            <p className="text-sm text-gray-400 mb-2">
              TIPS 적합성 분석 AI 에이전트
            </p>
            <p className="text-sm text-gray-500 mt-4">
              주식회사 코맥스벤처러스
            </p>
          </div>

          {/* 연락처 정보 */}
          <div>
            <h3 className="text-white font-semibold mb-4 text-lg">Contact</h3>
            <div className="space-y-3 text-sm text-gray-400">
              <div>
                <p className="text-gray-500 mb-1">주소</p>
                <p className="leading-relaxed">
                  서울특별시 강남구 역삼로 165<br />
                  해성빌딩 7F (우) 06247
                </p>
                <p className="leading-relaxed mt-2">
                  경기도 성남시 중원구 둔촌대로 494<br />
                  (우) 13229
                </p>
              </div>
              <div className="mt-4">
                <p className="text-gray-500 mb-1">이메일</p>
                <a 
                  href="mailto:support@iventurus.com" 
                  className="text-gray-300 hover:text-white transition-colors"
                >
                  support@iventurus.com
                </a>
              </div>
            </div>
          </div>

          {/* 기타 정보 */}
          <div>
            <h3 className="text-white font-semibold mb-4 text-lg">About</h3>
            <div className="space-y-2 text-sm text-gray-400">
              <p>Version 1.0</p>
              <p className="text-gray-500">
                Internal Use Only
              </p>
            </div>
          </div>
        </div>

        {/* 하단 구분선 */}
        <div className="mt-8 pt-8" style={{ borderTop: '1px solid #2a2a2a' }}>
          <div className="flex flex-col md:flex-row justify-between items-center">
            <p className="text-sm text-gray-500 mb-2 md:mb-0">
              © 2026 COMMAX VENTURUS. All rights reserved.
            </p>
            <p className="text-sm text-gray-500">
              TIPSMAX 1.0 - TIPS 적합성 분석 AI 에이전트
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
};
