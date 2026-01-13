"""
TIPSMAX 1.0 Backend API
FastAPI 기반 문서 분석 서비스
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from app.routes import upload, analysis

# 환경 변수 로드
load_dotenv()

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
app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(analysis.router, prefix="/api", tags=["analysis"])


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
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
