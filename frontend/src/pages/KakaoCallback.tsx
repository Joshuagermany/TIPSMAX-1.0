import React, { useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { kakaoLogin } from '../services/api';
import { useAuth } from '../contexts/AuthContext';

export const KakaoCallback: React.FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { login } = useAuth();
  const code = searchParams.get('code');
  const error = searchParams.get('error');

  useEffect(() => {
    if (error) {
      console.error('카카오 로그인 오류:', error);
      navigate('/login');
      return;
    }

    if (code) {
      // 인증 코드를 Backend로 전송하여 로그인 처리
      handleKakaoCallback(code);
    } else {
      navigate('/login');
    }
  }, [code, error, navigate]);

  const handleKakaoCallback = async (authCode: string) => {
    try {
      const response = await kakaoLogin(authCode);
      console.log('카카오 로그인 성공:', response);
      
      // AuthContext를 통해 로그인 처리
      if (response.access_token && response.user) {
        login(response.user, response.access_token);
      }
      
      // 홈으로 이동
      navigate('/');
    } catch (error: any) {
      console.error('카카오 로그인 처리 오류:', error);
      navigate('/login');
    }
  };

  return (
    <div style={{ backgroundColor: '#000000', minHeight: '100vh' }} className="flex items-center justify-center">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
        <p className="text-white">카카오 로그인 처리 중...</p>
      </div>
    </div>
  );
};
