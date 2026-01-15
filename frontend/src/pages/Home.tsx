import React, { useState } from 'react';
import { MultiFileUploadZone } from '../components/MultiFileUploadZone';
import { analyzeBusinessRegistration, BusinessRegistrationInfo } from '../services/api';

export const Home: React.FC = () => {
  const [error, setError] = useState<string | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState<{ financial?: { fileId: string; filename: string }; shareholder?: { fileId: string; filename: string }; corporate?: { fileId: string; filename: string } } | null>(null);
  const [businessInfo, setBusinessInfo] = useState<BusinessRegistrationInfo | null>(null);

  const handleAllFilesUploaded = (files: { financial?: { fileId: string; filename: string }; shareholder?: { fileId: string; filename: string }; corporate?: { fileId: string; filename: string } }) => {
    setError(null);
    setUploadedFiles(files);
    setBusinessInfo(null);
  };

  const handleStartAnalysis = async () => {
    if (!uploadedFiles?.financial?.fileId) {
      setError('먼저 사업자등록증 파일을 업로드해주세요.');
      return;
    }

    setError(null);
    setIsAnalyzing(true);

    try {
      const info = await analyzeBusinessRegistration(uploadedFiles.financial.fileId);
      setBusinessInfo(info);
    } catch (err: any) {
      setError(err.response?.data?.detail || '사업자등록증 분석 중 오류가 발생했습니다.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleError = (errorMessage: string) => {
    setError(errorMessage);
  };

  return (
    <div style={{ backgroundColor: '#000000', minHeight: '100%' }}>
      <div className="max-w-4xl mx-auto px-4 py-12">
        {/* 헤더 */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-white mb-4">
            문서 분석 시작
          </h1>
          <p className="text-lg text-gray-300 mb-2">
            TIPS 적합성 분석 AI 에이전트
          </p>
          <p className="text-sm text-gray-400">
            COMMAX VENTURUS 심사역을 위한 스타트업 문서 분석 도구
          </p>
        </div>

        {/* 업로드 영역 */}
        <div className="bg-gray-900 rounded-lg shadow-sm border border-gray-700 p-8 mb-6">
          {isAnalyzing ? (
            <div className="text-center py-12">
              <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary-600 mx-auto mb-4"></div>
              <p className="text-gray-300 text-lg">문서를 분석하고 있습니다...</p>
              <p className="text-gray-400 text-sm mt-2">잠시만 기다려주세요.</p>
            </div>
          ) : (
            <>
              <MultiFileUploadZone onAllFilesUploaded={handleAllFilesUploaded} onError={handleError} />
              <div className="mt-4 flex justify-end">
                <button
                  type="button"
                  onClick={handleStartAnalysis}
                  disabled={!uploadedFiles?.financial?.fileId}
                  className={`px-4 py-2 rounded-md text-sm font-medium border transition-colors ${
                    uploadedFiles?.financial?.fileId
                      ? 'bg-primary-600 border-primary-500 text-white hover:bg-primary-500'
                      : 'bg-gray-800 border-gray-700 text-gray-500 cursor-not-allowed'
                  }`}
                >
                  분석 시작
                </button>
              </div>
            </>
          )}
        </div>

        {/* 에러 메시지 */}
        {error && (
          <div className="bg-red-900 border border-red-700 rounded-lg p-4 mb-6">
            <p className="text-red-200 text-sm">{error}</p>
          </div>
        )}

        {/* 안내 사항 */}
        <div className="bg-gray-800 border border-gray-700 rounded-lg p-6">
          <h3 className="font-semibold text-white mb-2">분석 항목</h3>

          {businessInfo && (
            <div className="mb-4 text-sm text-gray-300 space-y-1">
              <p>
                <span className="font-semibold">개업연월일:</span>{' '}
                {businessInfo.opening_date_normalized || businessInfo.opening_date_raw || '-'}
              </p>
              <p>
                <span className="font-semibold">본점소재지:</span>{' '}
                {businessInfo.head_office_address || '-'}
              </p>
            </div>
          )}

          <ul className="text-sm text-gray-300 space-y-1 list-disc list-inside">
            <li>TIPS 기술 분야 자동 분류 (10개 분야)</li>
            <li>기술성, 사업성, 팀 역량, TIPS 적합성 평가</li>
            <li>종합 판단 및 심사역 코멘트 생성</li>
          </ul>
        </div>
      </div>
    </div>
  );
};
