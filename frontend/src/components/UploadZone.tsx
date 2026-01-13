import React, { useCallback, useState } from 'react';
import { uploadFile } from '../services/api';

interface UploadZoneProps {
  onUploadSuccess: (fileId: string, filename: string) => void;
  onError: (error: string) => void;
}

export const UploadZone: React.FC<UploadZoneProps> = ({ onUploadSuccess, onError }) => {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);

  const handleFile = useCallback(async (file: File) => {
    // 파일 형식 검증
    const allowedTypes = ['.pdf', '.docx', '.doc', '.txt'];
    const fileExt = '.' + file.name.split('.').pop()?.toLowerCase();
    
    if (!allowedTypes.includes(fileExt)) {
      onError('지원하지 않는 파일 형식입니다. PDF, DOCX, TXT 파일만 업로드 가능합니다.');
      return;
    }

    // 파일 크기 검증 (10MB)
    if (file.size > 10 * 1024 * 1024) {
      onError('파일 크기가 너무 큽니다. 최대 10MB까지 업로드 가능합니다.');
      return;
    }

    setIsUploading(true);
    try {
      const result = await uploadFile(file);
      onUploadSuccess(result.file_id, result.filename);
    } catch (error: any) {
      onError(error.response?.data?.detail || '파일 업로드 중 오류가 발생했습니다.');
    } finally {
      setIsUploading(false);
    }
  }, [onUploadSuccess, onError]);

  const handleDrop = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);

    const file = e.dataTransfer.files[0];
    if (file) {
      handleFile(file);
    }
  }, [handleFile]);

  const handleDragOver = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleFileInput = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFile(file);
    }
  }, [handleFile]);

  return (
    <div
      className={`border-2 border-dashed rounded-lg p-12 text-center transition-colors ${
        isDragging
          ? 'border-primary-500 bg-gray-800'
          : 'border-gray-600 hover:border-primary-400'
      } ${isUploading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
      style={{ backgroundColor: isDragging ? 'rgba(31, 41, 55, 0.5)' : 'transparent' }}
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onClick={() => !isUploading && document.getElementById('file-input')?.click()}
    >
      <input
        id="file-input"
        type="file"
        accept=".pdf,.docx,.doc,.txt"
        className="hidden"
        onChange={handleFileInput}
        disabled={isUploading}
      />
      
      {isUploading ? (
        <div className="space-y-4">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="text-gray-300">업로드 중...</p>
        </div>
      ) : (
        <div className="space-y-4">
          <svg
            className="mx-auto h-12 w-12 text-gray-400"
            stroke="currentColor"
            fill="none"
            viewBox="0 0 48 48"
          >
            <path
              d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
              strokeWidth={2}
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          <div>
            <p className="text-lg font-medium text-gray-200">
              파일을 드래그하거나 클릭하여 업로드
            </p>
            <p className="text-sm text-gray-400 mt-2">
              PDF, DOCX, TXT 파일 지원 (최대 10MB)
            </p>
          </div>
        </div>
      )}
    </div>
  );
};
