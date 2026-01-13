import axios from 'axios';
import { UploadResponse, AnalysisResult } from '../types/analysis';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

console.log('🔧 API_BASE_URL:', API_BASE_URL);

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30초 타임아웃
});

// 요청 인터셉터 (에러 로깅)
api.interceptors.request.use(
  (config) => {
    const fullUrl = `${config.baseURL}${config.url}`;
    console.log('📤 API 요청:', config.method?.toUpperCase(), fullUrl);
    console.log('📤 요청 데이터:', config.data);
    return config;
  },
  (error) => {
    console.error('❌ API 요청 설정 오류:', error);
    return Promise.reject(error);
  }
);

// 응답 인터셉터 (에러 로깅)
api.interceptors.response.use(
  (response) => {
    console.log('✅ API 응답 성공:', response.config.url, response.status);
    console.log('✅ 응답 데이터:', response.data);
    return response;
  },
  (error) => {
    const fullUrl = error.config ? `${error.config.baseURL}${error.config.url}` : 'unknown';
    console.error('❌ API 응답 오류:', {
      fullUrl,
      method: error.config?.method,
      status: error.response?.status,
      statusText: error.response?.statusText,
      data: error.response?.data,
      message: error.message,
      code: error.code,
      request: error.request ? '요청은 전송됨' : '요청 전송 실패',
    });
    return Promise.reject(error);
  }
);

export const uploadFile = async (file: File): Promise<UploadResponse> => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post<UploadResponse>('/api/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

export const analyzeDocument = async (fileId: string): Promise<AnalysisResult> => {
  const response = await api.post<AnalysisResult>('/api/analyze', {
    file_id: fileId,
  });
  
  return response.data;
};

export const kakaoLogin = async (code: string) => {
  const response = await api.post('/api/auth/kakao/callback', {
    code: code,
    provider: 'kakao',
  });
  
  return response.data;
};

export const googleLogin = async (code: string) => {
  const response = await api.post('/api/auth/google/callback', {
    code: code,
    provider: 'google',
  });
  
  return response.data;
};
