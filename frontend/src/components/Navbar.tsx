import React from 'react';
import { Link, useLocation } from 'react-router-dom';

export const Navbar: React.FC = () => {
  const location = useLocation();

  return (
    <nav className="shadow-lg" style={{ backgroundColor: '#343333', borderBottom: '1px solid #2a2a2a' }}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* 로고 */}
          <div className="flex items-center">
            <Link to="/" className="flex items-center hover:opacity-80 transition-opacity">
              <img
                src="/tipsmax-logo.png"
                alt="TIPSMAX Logo"
                className="h-12 w-auto max-h-12 object-contain"
                style={{ maxWidth: '200px' }}
                onError={(e) => {
                  console.error('로고 이미지 로드 실패:', e);
                  // 로고 로드 실패 시 대체 텍스트 표시
                  const img = e.target as HTMLImageElement;
                  img.style.display = 'none';
                  const parent = img.parentElement;
                  if (parent && !parent.querySelector('.logo-fallback')) {
                    const fallback = document.createElement('span');
                    fallback.className = 'logo-fallback text-white font-bold text-xl';
                    fallback.textContent = 'TIPSMAX 1.0';
                    parent.appendChild(fallback);
                  }
                }}
                onLoad={() => {
                  console.log('로고 이미지 로드 성공');
                }}
              />
            </Link>
          </div>

          {/* 네비게이션 메뉴 (추후 기능 추가 예정) */}
          <div className="flex items-center space-x-4">
            {/* 메뉴 아이템들은 추후 추가 */}
            <Link
              to="/"
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                location.pathname === '/'
                  ? 'text-white'
                  : 'text-gray-300 hover:text-white'
              }`}
              style={location.pathname === '/' ? { backgroundColor: 'rgba(255, 255, 255, 0.1)' } : {}}
            >
              분석하기
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
};
