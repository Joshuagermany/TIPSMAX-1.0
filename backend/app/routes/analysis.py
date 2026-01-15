"""
분석 라우트
"""

import os
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models.analysis import AnalysisRequest, AnalysisResult
from app.services.document_parser import DocumentParser
from app.services.llm_analyzer import LLMAnalyzer
from app.services.business_registration_extractor import extract_business_registration_fields

router = APIRouter()
UPLOAD_DIR = "uploads"


class BusinessRegistrationRequest(BaseModel):
    file_id: str


class BusinessRegistrationResult(BaseModel):
    opening_date_raw: Optional[str] = None
    opening_date_normalized: Optional[str] = None
    head_office_address: Optional[str] = None


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
        document_text = parser.parse(file_path, file_ext)

        if not document_text or len(document_text.strip()) < 10:
            raise HTTPException(
                status_code=400,
                detail="문서에서 텍스트를 추출할 수 없습니다."
            )

        # 디버깅: 추출된 텍스트의 일부를 로그로 출력
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"사업자등록증 텍스트 길이: {len(document_text)}")
        logger.info(f"사업자등록증 텍스트 앞 500자:\n{document_text[:500]}")
        
        fields = extract_business_registration_fields(document_text)
        logger.info(f"추출된 필드: {fields}")
        
        return BusinessRegistrationResult(**fields)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"사업자등록증 분석 중 오류가 발생했습니다: {str(e)}"
        )
