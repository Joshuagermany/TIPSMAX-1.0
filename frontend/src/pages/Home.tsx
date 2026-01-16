import React, { useState, useEffect } from 'react';
import { MultiFileUploadZone } from '../components/MultiFileUploadZone';
import { analyzeBusinessRegistration, BusinessRegistrationInfo, analyzeShareholder, ShareholderResult, analyzeFinancialStatement, FinancialStatementResult } from '../services/api';

export const Home: React.FC = () => {
  const [error, setError] = useState<string | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState<{ financial?: { fileId: string; filename: string }; shareholder?: { fileId: string; filename: string }; corporate?: { fileId: string; filename: string } } | null>(null);
  const [businessInfo, setBusinessInfo] = useState<BusinessRegistrationInfo | null>(null);
  const [shareholderInfo, setShareholderInfo] = useState<ShareholderResult | null>(null);
  const [financialStatementInfo, setFinancialStatementInfo] = useState<FinancialStatementResult | null>(null);
  const [analysisTime, setAnalysisTime] = useState<number | null>(null);

  // 재무제표 정보가 업데이트될 때마다 로그 출력
  useEffect(() => {
    if (financialStatementInfo) {
      console.log('🔄 재무제표 정보 상태 업데이트됨:', financialStatementInfo);
      console.log('🔄 재무제표 페이지 수:', financialStatementInfo.pages?.length || 0);
      console.log('🔄 재무제표 매출액:', financialStatementInfo.revenue);
      console.log('🔄 매출액 존재 여부:', !!financialStatementInfo.revenue);
    }
  }, [financialStatementInfo]);

  const handleAllFilesUploaded = (files: { financial?: { fileId: string; filename: string }; shareholder?: { fileId: string; filename: string }; corporate?: { fileId: string; filename: string } }) => {
    setError(null);
    setUploadedFiles(files);
    setBusinessInfo(null);
    setShareholderInfo(null);
    setFinancialStatementInfo(null);
    setAnalysisTime(null);
  };

  const handleStartAnalysis = async () => {
    if (!uploadedFiles?.financial?.fileId) {
      setError('먼저 사업자등록증 파일을 업로드해주세요.');
      return;
    }

    setError(null);
    setIsAnalyzing(true);
    setAnalysisTime(null);
    
    const startTime = Date.now();

    try {
      // 사업자등록증 분석 (파일명 전달)
      const businessInfoResult = await analyzeBusinessRegistration(
        uploadedFiles.financial.fileId,
        uploadedFiles.financial.filename
      );
      setBusinessInfo(businessInfoResult);

      // 주주명부 분석 (업로드된 경우)
      if (uploadedFiles?.shareholder?.fileId) {
        try {
          const shareholderResult = await analyzeShareholder(uploadedFiles.shareholder.fileId);
          setShareholderInfo(shareholderResult);
        } catch (shareholderErr: any) {
          console.error('주주명부 분석 실패:', shareholderErr);
          // 주주명부 분석 실패는 에러로 표시하지 않음 (선택적)
        }
      }

      // 재무제표 분석 (업로드된 경우) - 마지막에 실행하여 완료될 때까지 로딩 유지
      console.log('재무제표 파일 확인:', uploadedFiles?.corporate);
      if (uploadedFiles?.corporate?.fileId) {
        console.log('✅ 재무제표 분석 시작:', uploadedFiles.corporate.fileId);
        console.log('✅ 재무제표 파일명:', uploadedFiles.corporate.filename);
        try {
          console.log('✅ API 호출 전...');
          const financialStatementResult = await analyzeFinancialStatement(uploadedFiles.corporate.fileId);
          console.log('✅ 재무제표 분석 완료:', financialStatementResult);
          console.log('✅ 재무제표 페이지 수:', financialStatementResult.pages?.length || 0);
          console.log('✅ 재무제표 페이지 상세:', financialStatementResult.pages);
          console.log('✅ 재무제표 매출액:', financialStatementResult.revenue);
          console.log('✅ 매출액 타입:', typeof financialStatementResult.revenue);
          console.log('✅ 매출액 존재 여부:', !!financialStatementResult.revenue);
          
          // 상태 업데이트
          console.log('✅ 상태 업데이트 전 financialStatementInfo:', financialStatementInfo);
          setFinancialStatementInfo(financialStatementResult);
          console.log('✅ 상태 업데이트 호출 완료');
          console.log('✅ 새로운 값의 매출액:', financialStatementResult.revenue);
          
          // 상태가 제대로 반영되었는지 확인하기 위해 약간의 지연 후 재확인
          setTimeout(() => {
            console.log('✅ 1초 후 상태 확인:', financialStatementInfo);
          }, 1000);
        } catch (financialErr: any) {
          console.error('❌ 재무제표 분석 실패:', financialErr);
          console.error('❌ 에러 상세:', financialErr.response?.data);
          // 재무제표 분석 실패는 에러로 표시하지 않음 (선택적)
        }
      } else {
        console.log('⚠️ 재무제표 파일이 업로드되지 않음');
        console.log('⚠️ uploadedFiles:', uploadedFiles);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || '문서 분석 중 오류가 발생했습니다.');
    } finally {
      // 모든 분석이 완료된 후에만 로딩 상태 해제
      const endTime = Date.now();
      const elapsedTime = ((endTime - startTime) / 1000).toFixed(2); // 초 단위, 소수점 2자리
      setAnalysisTime(parseFloat(elapsedTime));
      console.log('✅ 모든 분석 완료, 로딩 상태 해제');
      console.log(`✅ 분석 소요 시간: ${elapsedTime}초`);
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
          <MultiFileUploadZone onAllFilesUploaded={handleAllFilesUploaded} onError={handleError} />
          <div className="mt-4 flex justify-end">
            <button
              type="button"
              onClick={handleStartAnalysis}
              disabled={!uploadedFiles?.financial?.fileId || isAnalyzing}
              className={`px-4 py-2 rounded-md text-sm font-medium border transition-colors ${
                uploadedFiles?.financial?.fileId && !isAnalyzing
                  ? 'bg-primary-600 border-primary-500 text-white hover:bg-primary-500'
                  : 'bg-gray-800 border-gray-700 text-gray-500 cursor-not-allowed'
              }`}
            >
              {isAnalyzing ? '분석 중...' : '분석 시작'}
            </button>
          </div>
        </div>

        {/* 에러 메시지 */}
        {error && (
          <div className="bg-red-900 border border-red-700 rounded-lg p-4 mb-6">
            <p className="text-red-200 text-sm">{error}</p>
          </div>
        )}

        {/* 안내 사항 */}
        <div className="bg-gray-800 border border-gray-700 rounded-lg p-6">
          <div className="flex justify-between items-center mb-2">
            <h3 className="font-semibold text-white">분석 항목</h3>
            {analysisTime !== null && (
              <span className="text-xs text-gray-400">
                분석 시간: {analysisTime}초
              </span>
            )}
          </div>

          {isAnalyzing ? (
            <div className="text-center py-8">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
              <p className="text-gray-300 text-sm">문서를 분석하고 있습니다...</p>
              <p className="text-gray-400 text-xs mt-2">잠시만 기다려주세요.</p>
            </div>
          ) : (
            <>
              {businessInfo && (
                <div className="mb-4 text-sm text-gray-300 space-y-1">
                  {businessInfo.company_name && (
                    <p>
                      <span className="font-semibold">기업명:</span>{' '}
                      {businessInfo.company_name}
                    </p>
                  )}
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

              {financialStatementInfo && financialStatementInfo.revenue && (
                <div className="mb-4 text-sm text-gray-300 space-y-1">
                  <p>
                    <span className="font-semibold">매출액:</span>{' '}
                    {financialStatementInfo.revenue}원
                  </p>
                </div>
              )}

              {shareholderInfo && shareholderInfo.shareholders.length > 0 && (
                <div className="mb-4">
                  <p className="text-sm font-semibold text-white mb-2">주주명부</p>
                  <div className="bg-gray-900 rounded border border-gray-700 overflow-hidden">
                    <table className="w-full text-sm">
                      <thead>
                        <tr className="bg-gray-800 border-b border-gray-700">
                          <th className="px-4 py-2 text-left text-gray-300 font-medium">주주명</th>
                          <th className="px-4 py-2 text-left text-gray-300 font-medium">주식비율</th>
                        </tr>
                      </thead>
                      <tbody>
                        {shareholderInfo.shareholders.map((shareholder, index) => (
                          <tr key={index} className="border-b border-gray-800 last:border-b-0">
                            <td className="px-4 py-2 text-gray-300">{shareholder.name}</td>
                            <td className="px-4 py-2 text-gray-300">
                              {shareholder.share_ratio === '-' ? '-' : `${shareholder.share_ratio}%`}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              {financialStatementInfo && (
                <div className="mb-4">
                  <p className="text-sm font-semibold text-white mb-2">재무제표 페이지 분류</p>
                  {financialStatementInfo.pages && financialStatementInfo.pages.length > 0 ? (
                    <div className="bg-gray-900 rounded border border-gray-700 overflow-hidden">
                      <table className="w-full text-sm">
                        <thead>
                          <tr className="bg-gray-800 border-b border-gray-700">
                            <th className="px-4 py-2 text-left text-gray-300 font-medium">페이지</th>
                            <th className="px-4 py-2 text-left text-gray-300 font-medium">문서 타입</th>
                          </tr>
                        </thead>
                        <tbody>
                          {financialStatementInfo.pages.map((page, index) => (
                            <tr key={index} className="border-b border-gray-800 last:border-b-0">
                              <td className="px-4 py-2 text-gray-300">{page.page_number}페이지</td>
                              <td className="px-4 py-2 text-gray-300">{page.type}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  ) : (
                    <div className="bg-gray-900 rounded border border-gray-700 p-4">
                      <p className="text-gray-400 text-sm">재무제표 페이지를 찾을 수 없습니다.</p>
                    </div>
                  )}
                </div>
              )}

              <ul className="text-sm text-gray-300 space-y-1 list-disc list-inside">
                <li>TIPS 기술 분야 자동 분류 (10개 분야)</li>
                <li>기술성, 사업성, 팀 역량, TIPS 적합성 평가</li>
                <li>종합 판단 및 심사역 코멘트 생성</li>
              </ul>
            </>
          )}
        </div>
      </div>
    </div>
  );
};
