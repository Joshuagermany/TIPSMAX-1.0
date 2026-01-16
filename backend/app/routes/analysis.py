"""
분석 라우트
"""

import os
import logging
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models.analysis import AnalysisRequest, AnalysisResult
from app.services.document_parser import DocumentParser
from app.services.llm_analyzer import LLMAnalyzer
from app.services.business_registration_extractor import extract_business_registration_fields
from app.services.shareholder_extractor import extract_shareholder_fields
from app.services.financial_statement_extractor import extract_financial_statement_fields

router = APIRouter()
UPLOAD_DIR = "uploads"
logger = logging.getLogger(__name__)


class BusinessRegistrationRequest(BaseModel):
    file_id: str
    filename: Optional[str] = None  # 파일명 추가 (기업명 추출용)


class BusinessRegistrationResult(BaseModel):
    company_name: Optional[str] = None
    opening_date_raw: Optional[str] = None
    opening_date_normalized: Optional[str] = None
    head_office_address: Optional[str] = None


class ShareholderRequest(BaseModel):
    file_id: str


class ShareholderItem(BaseModel):
    name: str
    share_ratio: str


class ShareholderResult(BaseModel):
    shareholders: list[ShareholderItem] = []


class FinancialStatementRequest(BaseModel):
    file_id: str


class FinancialStatementPageItem(BaseModel):
    page_number: int
    type: str
    revenue: Optional[str] = None  # 매출액 (표준손익계산서인 경우)


class FinancialStatementResult(BaseModel):
    pages: list[FinancialStatementPageItem] = []
    revenue: Optional[str] = None  # 매출액


@router.post("/analyze", response_model=AnalysisResult)
async def analyze_document(request: AnalysisRequest):
    """문서 분석 엔드포인트"""
    
    file_id = request.file_id
    
    # 업로드된 파일 찾기
    file_path = None
    file_ext = None
    
    for ext in [".pdf", ".docx", ".doc", ".txt"]:
        candidate_path = os.path.join(UPLOAD_DIR, f"{file_id}{ext}")
        if os.path.exists(candidate_path):
            file_path = candidate_path
            file_ext = ext
            break
    
    if not file_path:
        raise HTTPException(
            status_code=404,
            detail="파일을 찾을 수 없습니다."
        )
    
    try:
        # 문서 파싱
        parser = DocumentParser()
        document_text = parser.parse(file_path, file_ext)
        
        if not document_text or len(document_text.strip()) < 100:
            raise HTTPException(
                status_code=400,
                detail="문서에서 충분한 텍스트를 추출할 수 없습니다."
            )
        
        # LLM 분석
        analyzer = LLMAnalyzer()
        result = analyzer.analyze(document_text)
        
        return result
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"분석 중 오류가 발생했습니다: {str(e)}"
        )


@router.post("/analyze/business-registration", response_model=BusinessRegistrationResult)
async def analyze_business_registration(request: BusinessRegistrationRequest):
    """사업자등록증에서 개업연월일 및 본점소재지를 추출하는 엔드포인트"""

    file_id = request.file_id
    filename = request.filename or ""

    # 파일명에서 기업명 추출 ("사업자등록증_" 뒤의 부분, 첫 번째 언더바까지만)
    company_name = None
    if filename:
        # "사업자등록증_기업명_2025.pdf" 형식에서 기업명 추출
        # 예: "사업자등록증_아크론에코_2025" → "아크론에코"
        import re
        # 파일 확장자 제거
        name_without_ext = os.path.splitext(filename)[0]
        # "사업자등록증_" 또는 "사업자등록증 "으로 시작하는지 확인
        # 첫 번째 언더바 이후 부분에서, 다음 언더바 전까지 추출
        match = re.search(r'사업자등록증[_\s]+([^_]+)', name_without_ext, re.IGNORECASE)
        if match:
            # 첫 번째 언더바 이후 부분에서, 다음 언더바 전까지
            company_name = match.group(1).strip()
        else:
            # "사업자등록증_"이 없으면 전체 파일명 사용 (확장자 제외)
            # 하지만 언더바가 있으면 첫 번째 언더바까지만
            if '_' in name_without_ext:
                company_name = name_without_ext.split('_')[0]
            else:
                company_name = name_without_ext

    # 업로드된 파일 찾기 (기존 로직 재사용)
    file_path = None
    file_ext = None

    for ext in [".pdf", ".docx", ".doc", ".txt"]:
        candidate_path = os.path.join(UPLOAD_DIR, f"{file_id}{ext}")
        if os.path.exists(candidate_path):
            file_path = candidate_path
            file_ext = ext
            break

    if not file_path:
        raise HTTPException(
            status_code=404,
            detail="파일을 찾을 수 없습니다."
        )

    try:
        parser = DocumentParser()
        # 사업자등록증은 OCR 전용, 상단 50%만 분석
        document_text = parser.parse(file_path, file_ext, ocr_only=True, top_half_only=True)

        if not document_text or len(document_text.strip()) < 10:
            raise HTTPException(
                status_code=400,
                detail="문서에서 텍스트를 추출할 수 없습니다."
            )

        # 디버깅: 추출된 텍스트의 일부를 로그로 출력
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"사업자등록증 파일명: {filename}")
        logger.info(f"추출된 기업명: {company_name}")
        logger.info(f"사업자등록증 텍스트 길이: {len(document_text)}")
        logger.info(f"사업자등록증 텍스트 앞 500자:\n{document_text[:500]}")
        
        fields = extract_business_registration_fields(document_text)
        fields["company_name"] = company_name
        logger.info(f"추출된 필드: {fields}")
        
        return BusinessRegistrationResult(**fields)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"사업자등록증 분석 중 오류가 발생했습니다: {str(e)}"
        )


@router.post("/analyze/shareholder", response_model=ShareholderResult)
async def analyze_shareholder(request: ShareholderRequest):
    """주주명부에서 주주명과 주식비율을 추출하는 엔드포인트"""

    file_id = request.file_id

    # 업로드된 파일 찾기
    file_path = None
    file_ext = None

    for ext in [".pdf", ".docx", ".doc", ".txt"]:
        candidate_path = os.path.join(UPLOAD_DIR, f"{file_id}{ext}")
        if os.path.exists(candidate_path):
            file_path = candidate_path
            file_ext = ext
            break

    if not file_path:
        raise HTTPException(
            status_code=404,
            detail="파일을 찾을 수 없습니다."
        )

    try:
        parser = DocumentParser()
        document_text = parser.parse(file_path, file_ext)

        if not document_text or len(document_text.strip()) < 10:
            raise HTTPException(
                status_code=400,
                detail="문서에서 텍스트를 추출할 수 없습니다."
            )

        # 디버깅: 추출된 텍스트의 일부를 로그로 출력
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"주주명부 텍스트 길이: {len(document_text)}")
        logger.info(f"주주명부 텍스트 앞 500자:\n{document_text[:500]}")
        
        # 주주명부 추출 (파일 경로와 텍스트 둘 다 전달)
        result = extract_shareholder_fields(file_path, file_ext, document_text)
        logger.info(f"추출된 주주 수: {len(result['shareholders'])}")
        logger.info(f"추출된 주주 목록: {result['shareholders']}")
        
        # ShareholderItem 리스트로 변환
        shareholder_items = [
            ShareholderItem(name=item["name"], share_ratio=item["share_ratio"])
            for item in result["shareholders"]
        ]
        
        return ShareholderResult(shareholders=shareholder_items)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"주주명부 분석 중 오류가 발생했습니다: {str(e)}"
        )


@router.post("/analyze/financial-statement", response_model=FinancialStatementResult)
async def analyze_financial_statement(request: FinancialStatementRequest):
    """재무제표에서 각 페이지를 분류하는 엔드포인트"""
    
    import sys
    sys.stdout.flush()  # 버퍼 강제 출력
    
    print("\n" + "=" * 60)
    print("재무제표 분석 엔드포인트 호출됨!")
    print("=" * 60)
    logger.info("=" * 60)
    logger.info("재무제표 분석 엔드포인트 호출됨!")
    logger.info(f"파일 ID: {request.file_id}")
    print(f"파일 ID: {request.file_id}")
    print("=" * 60 + "\n")
    sys.stdout.flush()
    
    file_id = request.file_id

    # 업로드된 파일 찾기
    file_path = None
    file_ext = None

    logger.info(f"파일 찾기 시작: {file_id}")
    print(f"파일 찾기 시작: {file_id}")
    
    for ext in [".pdf", ".docx", ".doc", ".txt"]:
        candidate_path = os.path.join(UPLOAD_DIR, f"{file_id}{ext}")
        logger.info(f"확인 중: {candidate_path}")
        if os.path.exists(candidate_path):
            file_path = candidate_path
            file_ext = ext
            logger.info(f"파일 찾음: {file_path}")
            print(f"파일 찾음: {file_path}")
            break

    if not file_path:
        logger.error(f"파일을 찾을 수 없음: {file_id}")
        print(f"파일을 찾을 수 없음: {file_id}")
        raise HTTPException(
            status_code=404,
            detail="파일을 찾을 수 없습니다."
        )

    try:
        logger.info("재무제표 페이지 분류 시작...")
        print("재무제표 페이지 분류 시작...")
        # 재무제표 페이지 분류 (텍스트 파싱 없이 직접 PDF 분석)
        result = extract_financial_statement_fields(file_path, file_ext, None)
        logger.info(f"분류된 페이지 수: {len(result['pages'])}")
        logger.info(f"페이지 분류 결과: {result['pages']}")
        logger.info(f"매출액: {result.get('revenue')}")
        print(f"분류된 페이지 수: {len(result['pages'])}")
        print(f"페이지 분류 결과: {result['pages']}")
        print(f"매출액: {result.get('revenue')}")
        logger.info("=" * 60)
        print("=" * 60 + "\n")
        
        # FinancialStatementPageItem 리스트로 변환
        page_items = [
            FinancialStatementPageItem(
                page_number=item["page_number"],
                type=item["type"],
                revenue=item.get("revenue")
            )
            for item in result["pages"]
        ]
        
        # 매출액은 result에서 직접 가져오거나, 페이지에서 가져오기
        revenue = result.get("revenue")
        if not revenue:
            # 페이지에서 매출액 찾기
            for item in result["pages"]:
                if item.get("type") == "표준손익계산서" and item.get("revenue"):
                    revenue = item.get("revenue")
                    break
        
        logger.info(f"최종 반환할 매출액: {revenue}")
        print(f"최종 반환할 매출액: {revenue}")
        
        return FinancialStatementResult(
            pages=page_items,
            revenue=revenue
        )

    except ValueError as e:
        logger.error(f"재무제표 분석 오류 (ValueError): {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"재무제표 분석 오류: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"재무제표 분석 중 오류가 발생했습니다: {str(e)}"
        )
