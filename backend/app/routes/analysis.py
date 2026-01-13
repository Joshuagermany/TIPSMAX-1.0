"""
분석 라우트
"""

import os
from fastapi import APIRouter, HTTPException
from app.models.analysis import AnalysisRequest, AnalysisResult
from app.services.document_parser import DocumentParser
from app.services.llm_analyzer import LLMAnalyzer

router = APIRouter()
UPLOAD_DIR = "uploads"


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
