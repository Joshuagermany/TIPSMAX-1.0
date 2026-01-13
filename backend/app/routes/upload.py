"""
파일 업로드 라우트
"""

import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.models.analysis import UploadResponse
import aiofiles

router = APIRouter()

# 업로드 디렉토리
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".doc", ".txt"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """파일 업로드 엔드포인트"""
    
    # 파일 확장자 검증
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"지원하지 않는 파일 형식입니다. 허용 형식: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # 파일 크기 검증
    file_content = await file.read()
    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"파일 크기가 너무 큽니다. 최대 크기: {MAX_FILE_SIZE / 1024 / 1024}MB"
        )
    
    # 파일 저장
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}{file_ext}")
    
    async with aiofiles.open(file_path, 'wb') as f:
        await f.write(file_content)
    
    return UploadResponse(
        file_id=file_id,
        filename=file.filename,
        file_size=len(file_content)
    )
