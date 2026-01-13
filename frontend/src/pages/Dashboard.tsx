import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

export const Dashboard: React.FC = () => {
  const { user, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  if (!isAuthenticated) {
    navigate('/login');
    return null;
  }

  return (
    <div style={{ backgroundColor: '#000000', minHeight: '100vh' }}>
      <div className="max-w-7xl mx-auto px-4 py-12">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-white mb-4">대시보드</h1>
          <p className="text-lg text-gray-300">
            {user?.nickname}님, 환영합니다!
          </p>
        </div>

        <div className="bg-gray-900 rounded-lg shadow-sm border border-gray-700 p-8">
          <h2 className="text-2xl font-semibold text-white mb-4">사용자 정보</h2>
          <div className="space-y-3 text-gray-300">
            <p><span className="font-semibold">닉네임:</span> {user?.nickname}</p>
            {user?.email && (
              <p><span className="font-semibold">이메일:</span> {user.email}</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
