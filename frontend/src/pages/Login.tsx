import React, { useEffect, useRef, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { kakaoLogin, googleLogin, naverLogin } from '../services/api';
import { useAuth } from '../contexts/AuthContext';

export const Login: React.FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { login } = useAuth();
  const code = searchParams.get('code');
  const error = searchParams.get('error');
  const provider = searchParams.get('provider'); // kakao, google, naver
  const stateParam = searchParams.get('state');

  // 상태 관리
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const processedCodeRef = useRef<string | null>(null); // 이미 처리된 code 추적

  // URL 파라미터에서 인증 코드가 있으면 콜백 처리 (한 번만)
  useEffect(() => {
    // code가 없거나 provider가 없으면 아무것도 하지 않음
    if (!code || !provider) {
      return;
    }

    // 이미 처리된 code면 아무것도 하지 않음
    if (processedCodeRef.current === code) {
      return;
    }

    // OAuth 에러가 있으면 처리하지 않음
    if (error) {
      console.error('OAuth 에러:', error);
      setErrorMessage('로그인 중 오류가 발생했습니다.');
      setLoading(false);
      return;
    }

    // code 처리 시작 (한 번만 실행되도록 ref에 저장)
    processedCodeRef.current = code;
    setLoading(true);
    setErrorMessage(null);

    const handleCallback = async () => {
      try {
        setLoading(true);
        setErrorMessage(null);
        
        console.log('🚀 로그인 콜백 시작:', { provider, code: code?.substring(0, 20) + '...' });
        
        // 백엔드 API 호출
        let response;
        if (provider === 'kakao') {
          console.log('📞 카카오 로그인 API 호출 중...');
          response = await kakaoLogin(code!);
        } else if (provider === 'google') {
          console.log('📞 구글 로그인 API 호출 중...');
          response = await googleLogin(code!);
        } else if (provider === 'naver') {
          console.log('📞 네이버 로그인 API 호출 중...', { state: stateParam });
          response = await naverLogin(code!, stateParam || undefined);
        } else {
          throw new Error('지원하지 않는 provider입니다.');
        }

        console.log('📥 API 응답 받음:', response);

        // 응답 확인
        if (!response) {
          throw new Error('서버 응답이 없습니다.');
        }

        // 사용자 정보 추출
        const userData = response.user;
        const accessToken = response.access_token || 'temp_token_' + Date.now();

        if (!userData) {
          console.error('❌ 사용자 정보 없음:', response);
          throw new Error('사용자 정보를 가져올 수 없습니다.');
        }

        console.log('✅ 로그인 성공, 사용자 정보:', userData);

        // 로그인 처리
        login(userData, accessToken);
        
        // URL 파라미터 제거 후 홈으로 이동
        window.history.replaceState({}, '', '/');
        navigate('/', { replace: true });
        
      } catch (error: any) {
        console.error('❌ 로그인 오류 상세:', error);
        console.error('❌ 에러 타입:', {
          hasResponse: !!error.response,
          hasRequest: !!error.request,
          message: error.message,
          code: error.code,
        });
        
        // 에러 메시지 설정
        let errorMsg = '로그인 처리 중 오류가 발생했습니다.';
        
        if (error.response) {
          // 백엔드에서 에러 응답 (200이 아닌 상태 코드)
          errorMsg = error.response.data?.detail || error.response.data?.message || errorMsg;
          console.error('❌ 백엔드 에러 응답:', error.response.status, error.response.data);
        } else if (error.request) {
          // 요청은 보냈지만 응답이 없음 (네트워크 오류)
          errorMsg = `서버에 연결할 수 없습니다. (${error.message || '네트워크 오류'}) 백엔드가 http://localhost:8000에서 실행 중인지 확인해주세요.`;
          console.error('❌ 네트워크 오류 - 요청은 전송되었지만 응답이 없음');
        } else {
          // 요청 설정 중 오류
          errorMsg = error.message || errorMsg;
          console.error('❌ 요청 설정 오류:', error.message);
        }
        
        setErrorMessage(errorMsg);
        setLoading(false);
        processedCodeRef.current = null;
      }
    };

    handleCallback();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [code, provider, error]); // login, navigate는 의존성에서 제외 (무한 루프 방지)

  const handleKakaoLogin = () => {
    const KAKAO_REST_API_KEY = "84ebc5642421faf44961b796f6102ec4";
    const redirectUri = encodeURIComponent(`${window.location.origin}/login?provider=kakao`);
    
    window.location.href =
      "https://kauth.kakao.com/oauth/authorize" +
      `?client_id=${KAKAO_REST_API_KEY}` +
      `&redirect_uri=${redirectUri}` +
      "&response_type=code";
  };

  const handleGoogleLogin = () => {
    const GOOGLE_CLIENT_ID = "458353712714-0sjghe4t2jls4rmmp21ipqm5s8n6qkuo.apps.googleusercontent.com";
    const redirectUri = encodeURIComponent(`${window.location.origin}/login?provider=google`);
  
    window.location.href =
      "https://accounts.google.com/o/oauth2/v2/auth" +
      `?client_id=${GOOGLE_CLIENT_ID}` +
      `&redirect_uri=${redirectUri}` +
      "&response_type=code" +
      "&scope=openid email profile";
  };

  const handleNaverLogin = () => {
    const NAVER_CLIENT_ID = 'M_7h7fexbmq3A0mKYWON';
    const redirectUri = encodeURIComponent(`${window.location.origin}/login?provider=naver`);
    const state = 'tipsmax_naver_state';

    window.location.href =
      'https://nid.naver.com/oauth2.0/authorize' +
      `?response_type=code` +
      `&client_id=${NAVER_CLIENT_ID}` +
      `&redirect_uri=${redirectUri}` +
      `&state=${state}`;
  };

  return (
    <div style={{ backgroundColor: '#000000', minHeight: '100vh' }} className="flex items-center justify-center">
      <div className="max-w-md w-full mx-auto px-4 pt-4 pb-12">
        {loading ? (
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
            <p className="text-white text-lg">로그인 처리 중...</p>
          </div>
        ) : errorMessage ? (
          <div className="text-center">
            <div className="bg-red-900 border border-red-700 rounded-lg p-6 mb-4">
              <p className="text-red-300 text-lg font-semibold mb-2">로그인 실패</p>
              <p className="text-red-200 text-sm">{errorMessage}</p>
            </div>
            <button
              onClick={() => {
                setErrorMessage(null);
                processedCodeRef.current = null;
                window.history.replaceState({}, '', '/login');
                navigate('/login', { replace: true });
              }}
              className="px-4 py-2 bg-gray-700 text-gray-200 rounded-lg hover:bg-gray-600 transition-colors"
            >
              다시 시도
            </button>
          </div>
        ) : (
          <>
            <div className="text-center mb-12">
              <h1 className="text-4xl font-bold text-white mb-4">로그인</h1>
              <p className="text-gray-400">소셜 계정으로 로그인하세요</p>
            </div>

        {/* 소셜 로그인 버튼들 */}
        <div className="space-y-4">
          {/* 카카오톡 로그인 */}
          <button
            onClick={handleKakaoLogin}
            className="w-full py-4 px-6 rounded-lg font-semibold text-lg transition-all hover:opacity-90 hover:shadow-lg flex items-center justify-center gap-3"
            style={{ backgroundColor: '#FEE500', color: '#000000' }}
          >
            <svg
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M12 3C6.477 3 2 6.477 2 11c0 2.558 1.58 4.74 3.81 5.64L5 21l4.5-1.5c.5.08 1 .12 1.5.12 5.523 0 10-3.477 10-8s-4.477-8-10-8z"
                fill="#000000"
              />
            </svg>
            카카오톡으로 로그인
          </button>

          {/* 구글 로그인 */}
          <button
            onClick={handleGoogleLogin}
            className="w-full py-4 px-6 rounded-lg font-semibold text-lg transition-all hover:opacity-90 hover:shadow-lg flex items-center justify-center gap-3 bg-white text-gray-900"
          >
            <svg
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                fill="#4285F4"
              />
              <path
                d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                fill="#34A853"
              />
              <path
                d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                fill="#FBBC05"
              />
              <path
                d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                fill="#EA4335"
              />
            </svg>
            구글로 로그인
          </button>

          {/* 네이버 로그인 */}
          <button
            onClick={handleNaverLogin}
            className="w-full py-4 px-6 rounded-lg font-semibold text-lg transition-all hover:opacity-90 hover:shadow-lg flex items-center justify-center gap-3"
            style={{ backgroundColor: '#03C75A', color: '#FFFFFF' }}
          >
            <svg
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M16.273 12.845L7.376 0H0V24H7.726V11.156L16.624 24H24V0H16.273V12.845Z"
                fill="currentColor"
              />
            </svg>
            네이버로 로그인
          </button>
        </div>
          </>
        )}
      </div>
    </div>
  );
};
