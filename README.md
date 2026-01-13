# TIPSMAX 1.0

**TIPS 적합성 분석 AI 에이전트**

COMMAX VENTURUS 심사역을 위한 스타트업 문서 자동 분석 웹서비스

## 📋 개요

TIPSMAX 1.0은 스타트업의 사업계획서, IR Deck, 기술자료를 업로드하면 AI가 자동으로 다음을 분석하는 웹 기반 AI 에이전트입니다:

- **TIPS 기술 분야 자동 분류** (10개 분야)
- **4가지 관점 평가** (기술성, 사업성, 팀 역량, TIPS 적합성)
- **종합 판단 및 시각화 리포트** 생성

## 🏗️ 아키텍처

```
Frontend (React + TypeScript)  ←→  Backend (FastAPI)  ←→  LLM API
```

### 기술 스택

**Backend**
- FastAPI (Python 3.11+)
- PyPDF2 / pdfplumber (PDF 파싱)
- python-docx (DOCX 파싱)
- OpenAI API 또는 Anthropic Claude

**Frontend**
- React 18 + TypeScript
- Vite
- Tailwind CSS
- Recharts (시각화)

## 🚀 시작하기

### 사전 요구사항

- Python 3.11 이상
- Node.js 18 이상
- LLM API 키 (OpenAI 또는 Anthropic) - 선택사항 (없으면 Mock 결과 반환)

### ⚡ 빠른 실행 (추천)

**Windows에서 가장 간단한 방법:**

1. **Backend 실행**:
   - `backend` 폴더에서 `start.bat` 더블클릭
   - 또는 PowerShell에서: `cd backend` → `.\start.ps1`

2. **Frontend 실행** (새 터미널):
   - `frontend` 폴더에서 `start.bat` 더블클릭
   - 또는 PowerShell에서: `cd frontend` → `.\start.ps1`

3. 브라우저에서 `http://localhost:5173` 접속

### Backend 설정 (수동)

1. Backend 디렉토리로 이동:
```bash
cd backend
```

2. 가상 환경 생성 및 활성화:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. 의존성 설치:
```bash
pip install -r requirements.txt
```

4. 환경 변수 설정:
```bash
# .env 파일 생성
cp .env.example .env
```

`.env` 파일을 편집하여 LLM API 키를 설정:
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4-turbo-preview
```

또는 Anthropic 사용 시:
```env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=your_api_key_here
ANTHROPIC_MODEL=claude-3-opus-20240229
```

5. Backend 서버 실행:
```bash
uvicorn app.main:app --reload
```

Backend는 `http://localhost:8000`에서 실행됩니다.

### Frontend 설정

1. Frontend 디렉토리로 이동:
```bash
cd frontend
```

2. 의존성 설치:
```bash
npm install
```

3. 개발 서버 실행:
```bash
npm run dev
```

Frontend는 `http://localhost:5173`에서 실행됩니다.

## 📖 사용 방법

1. 웹 브라우저에서 `http://localhost:5173` 접속
2. PDF, DOCX, 또는 TXT 파일을 드래그 앤 드롭 또는 클릭하여 업로드
3. AI가 문서를 분석하는 동안 대기 (약 30초~1분)
4. 분석 결과 페이지에서 다음을 확인:
   - 4가지 관점 평가 (Radar Chart)
   - 종합 TIPS 적합도 (Gauge Chart)
   - TIPS 분야별 적합도 (Bar Chart)
   - 기업 요약, 강점, 리스크, 심사역 코멘트

## 📊 분석 항목

### TIPS 기술 분야 (10개)
- AI·빅데이터
- 시스템반도체 / 팹리스
- 바이오·헬스케어
- 미래모빌리티
- 친환경·에너지
- 로봇·자동화
- 디지털헬스
- 콘텐츠·플랫폼
- SaaS / B2B 솔루션
- 딥테크 기타

### 평가 관점 (각 0~100점)
- **기술성**: 차별성, 구현 가능성, 진입장벽, 기술 설명 구체성
- **사업성**: 문제 정의, 시장 크기, BM 명확성, 수익 구조
- **팀 역량**: 창업자 전문성, 기술-비즈니스 균형, 과거 성과, 팀 구성
- **TIPS 적합성**: 기술 기반 창업, R&D 중심, 정부 과제 연계, 종합 판단

### 종합 판단
- ✅ **추천**: TIPS 추천 가능
- ⚠️ **보류**: 보완 필요
- ❌ **비추천**: TIPS 부적합

## 🔧 API 엔드포인트

### POST /api/upload
파일 업로드
- **Content-Type**: `multipart/form-data`
- **응답**: `{ file_id: string, filename: string, file_size: number }`

### POST /api/analyze
문서 분석 요청
- **Body**: `{ file_id: string }`
- **응답**: `AnalysisResult` (JSON)

## 📁 프로젝트 구조

```
TIPSMAX-1.0/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI 앱
│   │   ├── models/              # 데이터 모델
│   │   ├── services/            # 비즈니스 로직
│   │   └── routes/              # API 라우트
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/          # React 컴포넌트
│   │   ├── pages/               # 페이지
│   │   ├── services/            # API 클라이언트
│   │   └── types/               # TypeScript 타입
│   └── package.json
├── ARCHITECTURE.md              # 아키텍처 문서
└── README.md
```

## 🎯 향후 고도화 아이디어

1. **포트폴리오 DB 연동**
   - 기존 TIPS 성공기업 데이터베이스와 비교 분석
   - 유사 기업 추천

2. **심사역 개인 성향 반영**
   - 심사역별 평가 기준 가중치 설정
   - 개인화된 분석 리포트

3. **배치 분석**
   - 여러 문서 동시 분석
   - 비교 분석 리포트

4. **히스토리 관리**
   - 분석 이력 저장 및 조회
   - 트렌드 분석

5. **고급 시각화**
   - 타임라인 분석
   - 경쟁사 비교 차트

## 📝 라이선스

이 프로젝트는 COMMAX VENTURUS 내부 사용을 위한 것입니다.

## 👥 기여

COMMAX VENTURUS 내부 프로젝트입니다.

---

**TIPSMAX 1.0** - VC 심사역의 업무 효율을 극대화하는 AI 에이전트
