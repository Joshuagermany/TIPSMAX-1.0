"""
TIPSMAX 1.0 Backend API
FastAPI 기반 문서 분석 서비스
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import logging

# 환경 변수 로드 (모듈 import 전에 실행되어야 함)
load_dotenv()

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from app.routes import upload, analysis, auth

logger.info("TIPSMAX 1.0 Backend 시작 중...")

app = FastAPI(
    title="TIPSMAX 1.0 API",
    description="VC 심사역을 위한 스타트업 문서 분석 AI 에이전트",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite 기본 포트
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우트 등록
try:
    app.include_router(upload.router, prefix="/api", tags=["upload"])
    app.include_router(analysis.router, prefix="/api", tags=["analysis"])
    app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
    logger.info("라우트 등록 완료")
except Exception as e:
    logger.error(f"라우트 등록 오류: {e}", exc_info=True)
    raise


@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "service": "TIPSMAX 1.0",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """헬스 체크"""
    logger.info("Health check 요청")
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
