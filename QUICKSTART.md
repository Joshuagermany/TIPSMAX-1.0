# TIPSMAX 1.0 빠른 시작 가이드

## 5분 안에 시작하기

### 1단계: Backend 설정 (2분)

```bash
# Backend 디렉토리로 이동
cd backend

# 가상 환경 생성 및 활성화
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux  
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 파일 생성
# Windows (PowerShell)
New-Item -Path .env -ItemType File
# macOS/Linux
touch .env
```

`.env` 파일에 다음 내용 추가:
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-4-turbo-preview
```

```bash
# 서버 실행
uvicorn app.main:app --reload
```

✅ Backend가 `http://localhost:8000`에서 실행됩니다.

### 2단계: Frontend 설정 (2분)

새 터미널 창에서:

```bash
# Frontend 디렉토리로 이동
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

✅ Frontend가 `http://localhost:5173`에서 실행됩니다.

### 3단계: 사용하기 (1분)

1. 브라우저에서 `http://localhost:5173` 접속
2. PDF, DOCX, 또는 TXT 파일을 드래그 앤 드롭
3. 분석 결과 확인!

## 문제 해결

### Backend 오류

**문제**: `ModuleNotFoundError`
```bash
# 가상 환경이 활성화되었는지 확인
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
```

**문제**: `OPENAI_API_KEY` 오류
- `.env` 파일이 `backend/` 디렉토리에 있는지 확인
- API 키가 올바른지 확인

### Frontend 오류

**문제**: `npm install` 실패
```bash
# Node.js 버전 확인 (18 이상 필요)
node --version

# 캐시 클리어 후 재시도
npm cache clean --force
npm install
```

**문제**: Backend 연결 실패
- Backend가 `http://localhost:8000`에서 실행 중인지 확인
- 브라우저 콘솔에서 CORS 오류 확인

## 다음 단계

- [README.md](README.md)에서 상세한 기능 설명 확인
- [ARCHITECTURE.md](ARCHITECTURE.md)에서 아키텍처 이해
- API 문서는 `http://localhost:8000/docs`에서 확인
