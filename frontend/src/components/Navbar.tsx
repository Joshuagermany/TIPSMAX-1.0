import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

export const Navbar: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, isAuthenticated, logout } = useAuth();

  // 디버깅용 로그
  React.useEffect(() => {
    console.log('Navbar 렌더링 - isAuthenticated:', isAuthenticated, 'user:', user);
  }, [isAuthenticated, user]);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

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

          {/* 네비게이션 메뉴 */}
          <div className="flex items-center space-x-4">
            {/* 사용자 이름 표시 (로그인 시) */}
            {isAuthenticated && user && (
              <span className="text-sm text-gray-300">
                {user.nickname}님 환영합니다.
              </span>
            )}
            
            <Link
              to="/company-status"
              className="px-4 py-2 rounded-md text-sm font-medium transition-colors text-white border border-gray-600 hover:border-gray-500 hover:bg-gray-700"
              style={
                location.pathname === '/company-status'
                  ? { backgroundColor: 'rgba(255, 255, 255, 0.15)', borderColor: 'rgba(255, 255, 255, 0.3)' }
                  : { backgroundColor: 'rgba(255, 255, 255, 0.05)' }
              }
            >
              기업 현황
            </Link>
            
            {isAuthenticated ? (
              <button
                onClick={handleLogout}
                className="px-4 py-2 rounded-md text-sm font-medium transition-colors text-white border border-gray-600 hover:border-gray-500 hover:bg-gray-700"
                style={{ backgroundColor: 'rgba(255, 255, 255, 0.05)' }}
              >
                로그아웃
              </button>
            ) : (
              <Link
                to="/login"
                className="px-4 py-2 rounded-md text-sm font-medium transition-colors text-white border border-gray-600 hover:border-gray-500 hover:bg-gray-700"
                style={
                  location.pathname === '/login'
                    ? { backgroundColor: 'rgba(255, 255, 255, 0.15)', borderColor: 'rgba(255, 255, 255, 0.3)' }
                    : { backgroundColor: 'rgba(255, 255, 255, 0.05)' }
                }
              >
                로그인
              </Link>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};
