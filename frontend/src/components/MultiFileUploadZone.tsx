import React, { useCallback, useState } from 'react';
import { uploadFile } from '../services/api';

export type FileType = 'financial' | 'shareholder' | 'corporate';

interface FileUploadState {
  file: File | null;
  fileId: string | null;
  filename: string | null;
  isUploading: boolean;
  isUploaded: boolean;
}

interface MultiFileUploadZoneProps {
  onAllFilesUploaded: (files: { financial?: { fileId: string; filename: string }; shareholder?: { fileId: string; filename: string }; corporate?: { fileId: string; filename: string } }) => void;
  onError: (error: string) => void;
}

export const MultiFileUploadZone: React.FC<MultiFileUploadZoneProps> = ({ onAllFilesUploaded, onError }) => {
  const [files, setFiles] = useState<Record<FileType, FileUploadState>>({
    financial: { file: null, fileId: null, filename: null, isUploading: false, isUploaded: false },
    shareholder: { file: null, fileId: null, filename: null, isUploading: false, isUploaded: false },
    corporate: { file: null, fileId: null, filename: null, isUploading: false, isUploaded: false },
  });
  const [hasStartupCertificate, setHasStartupCertificate] = useState<boolean>(true);

  const fileTypeLabels: Record<FileType, string> = {
    financial: '사업자등록증',
    shareholder: '주주명부',
    corporate: '재무제표',
  };

  const handleFile = useCallback(async (file: File, fileType: FileType) => {
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

    // 파일 상태 업데이트
    setFiles(prev => ({
      ...prev,
      [fileType]: { ...prev[fileType], file, isUploading: true, isUploaded: false },
    }));

    try {
      const result = await uploadFile(file);
      
      // 업데이트된 파일 상태를 계산
      setFiles(prev => {
        const updatedFiles = {
          ...prev,
          [fileType]: {
            file,
            fileId: result.file_id,
            filename: result.filename,
            isUploading: false,
            isUploaded: true,
          },
        };

        // 모든 파일이 업로드되었는지 확인
        const uploadedFiles: { financial?: { fileId: string; filename: string }; shareholder?: { fileId: string; filename: string }; corporate?: { fileId: string; filename: string } } = {};
        if (updatedFiles.financial.isUploaded && updatedFiles.financial.fileId) {
          uploadedFiles.financial = { fileId: updatedFiles.financial.fileId, filename: updatedFiles.financial.filename! };
        }
        if (updatedFiles.shareholder.isUploaded && updatedFiles.shareholder.fileId) {
          uploadedFiles.shareholder = { fileId: updatedFiles.shareholder.fileId, filename: updatedFiles.shareholder.filename! };
        }
        if (updatedFiles.corporate.isUploaded && updatedFiles.corporate.fileId) {
          uploadedFiles.corporate = { fileId: updatedFiles.corporate.fileId, filename: updatedFiles.corporate.filename! };
        }

        // 모든 파일이 업로드되었으면 콜백 호출
        if (uploadedFiles.financial && uploadedFiles.shareholder && uploadedFiles.corporate) {
          setTimeout(() => onAllFilesUploaded(uploadedFiles), 100);
        }

        return updatedFiles;
      });
    } catch (error: any) {
      setFiles(prev => ({
        ...prev,
        [fileType]: { ...prev[fileType], isUploading: false, isUploaded: false },
      }));
      onError(error.response?.data?.detail || '파일 업로드 중 오류가 발생했습니다.');
    }
  }, [onError, onAllFilesUploaded]);

  const handleDrop = useCallback((e: React.DragEvent<HTMLDivElement>, fileType: FileType) => {
    e.preventDefault();
    e.stopPropagation();

    const file = e.dataTransfer.files[0];
    if (file) {
      handleFile(file, fileType);
    }
  }, [handleFile]);

  const handleDragOver = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
  }, []);

  const handleFileInput = useCallback((e: React.ChangeEvent<HTMLInputElement>, fileType: FileType) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFile(file, fileType);
    }
  }, [handleFile]);

  const renderUploadZone = (fileType: FileType) => {
    const fileState = files[fileType];
    const inputId = `file-input-${fileType}`;

    return (
      <div key={fileType} className="mb-4">
        <label className="block text-sm font-medium text-gray-300 mb-2">
          {fileTypeLabels[fileType]}
        </label>
        <div
          className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
            fileState.isUploading
              ? 'border-gray-600 opacity-50 cursor-not-allowed'
              : fileState.isUploaded
              ? 'border-green-600 bg-green-900/20'
              : 'border-gray-600 hover:border-primary-400 cursor-pointer'
          }`}
          onDrop={(e) => handleDrop(e, fileType)}
          onDragOver={handleDragOver}
          onClick={() => !fileState.isUploading && !fileState.isUploaded && document.getElementById(inputId)?.click()}
        >
          <input
            id={inputId}
            type="file"
            accept=".pdf,.docx,.doc,.txt"
            className="hidden"
            onChange={(e) => handleFileInput(e, fileType)}
            disabled={fileState.isUploading || fileState.isUploaded}
          />
          
          {fileState.isUploading ? (
            <div className="space-y-2">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
              <p className="text-gray-300 text-sm">업로드 중...</p>
            </div>
          ) : fileState.isUploaded ? (
            <div className="space-y-2">
              <svg
                className="mx-auto h-8 w-8 text-green-500"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              <p className="text-green-300 text-sm font-medium">{fileState.filename}</p>
              <p className="text-green-400 text-xs">업로드 완료</p>
            </div>
          ) : (
            <div className="space-y-2">
              <svg
                className="mx-auto h-8 w-8 text-gray-400"
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
              <p className="text-gray-300 text-sm">
                파일을 드래그하거나 클릭하여 업로드
              </p>
              <p className="text-gray-400 text-xs">
                PDF, DOCX, TXT 파일 지원 (최대 10MB)
              </p>
            </div>
          )}
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-6">
      {renderUploadZone('financial')}
      {renderUploadZone('shareholder')}
      {renderUploadZone('corporate')}

      <p className="text-gray-400 text-sm text-left">
        * 사업자등록증, 주주명부, 재무제표 세 가지 파일을 모두 업로드해주세요.
      </p>

      {/* 창업기업확인서 보유 여부 질문 */}
      <div className="mt-4 flex items-center gap-4">
        <span className="text-gray-300 text-sm">
          창업기업확인서를 보유하고 있나요?
        </span>
        <div className="flex gap-2">
          <button
            type="button"
            onClick={() => setHasStartupCertificate(true)}
            className={`px-3 py-1 rounded-md text-sm font-medium border ${
              hasStartupCertificate
                ? 'bg-primary-600 border-primary-500 text-white'
                : 'bg-gray-800 border-gray-600 text-gray-300 hover:bg-gray-700'
            }`}
          >
            예
          </button>
          <button
            type="button"
            onClick={() => setHasStartupCertificate(false)}
            className={`px-3 py-1 rounded-md text-sm font-medium border ${
              !hasStartupCertificate
                ? 'bg-primary-600 border-primary-500 text-white'
                : 'bg-gray-800 border-gray-600 text-gray-300 hover:bg-gray-700'
            }`}
          >
            아니오
          </button>
        </div>
      </div>
    </div>
  );
};
