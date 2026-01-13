import axios from 'axios';
import { UploadResponse, AnalysisResult } from '../types/analysis';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

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
