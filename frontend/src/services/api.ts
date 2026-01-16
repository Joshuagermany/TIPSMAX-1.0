import axios from 'axios';
import { UploadResponse, AnalysisResult } from '../types/analysis';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

console.log('🔧 API_BASE_URL:', API_BASE_URL);

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 300000, // 5분 타임아웃 (재무제표 분석이 오래 걸릴 수 있음)
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

export interface BusinessRegistrationInfo {
  company_name?: string;
  opening_date_raw?: string;
  opening_date_normalized?: string;
  head_office_address?: string;
}

export interface ShareholderInfo {
  name: string;
  share_ratio: string;
}

export interface ShareholderResult {
  shareholders: ShareholderInfo[];
}

export const analyzeBusinessRegistration = async (fileId: string, filename?: string): Promise<BusinessRegistrationInfo> => {
  const response = await api.post<BusinessRegistrationInfo>('/api/analyze/business-registration', {
    file_id: fileId,
    filename: filename,
  });

  return response.data;
};

export const analyzeShareholder = async (fileId: string): Promise<ShareholderResult> => {
  const response = await api.post<ShareholderResult>('/api/analyze/shareholder', {
    file_id: fileId,
  });

  return response.data;
};

export interface FinancialStatementPageInfo {
  page_number: number;
  type: string;
  revenue?: string;
}

export interface FinancialStatementResult {
  pages: FinancialStatementPageInfo[];
  revenue?: string;
}

export const analyzeFinancialStatement = async (fileId: string): Promise<FinancialStatementResult> => {
  const response = await api.post<FinancialStatementResult>('/api/analyze/financial-statement', {
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

export const naverLogin = async (code: string, state?: string) => {
  const response = await api.post('/api/auth/naver/callback', {
    code,
    state,
    provider: 'naver',
  });

  return response.data;
};
