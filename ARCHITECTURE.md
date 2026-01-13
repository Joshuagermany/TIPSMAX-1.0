# TIPSMAX 1.0 아키텍처 설계

## 1. 전체 시스템 아키텍처

```
┌─────────────────┐
│   Frontend      │
│  React + TS     │
│  Tailwind CSS   │
│  Recharts       │
└────────┬────────┘
         │ HTTP/REST
         │
┌────────▼────────┐
│   Backend API   │
│   FastAPI       │
│   Python 3.11+  │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐ ┌──▼────┐
│ 문서  │ │  LLM  │
│ 파싱  │ │  API  │
│ 모듈  │ │       │
└───────┘ └───────┘
```

## 2. 디렉토리 구조

```
TIPSMAX-1.0/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI 앱 진입점
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── analysis.py      # 분석 결과 모델
│   │   │   └── upload.py         # 업로드 모델
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── document_parser.py  # PDF/DOCX/TXT 파싱
│   │   │   ├── llm_analyzer.py     # LLM 분석 로직
│   │   │   └── prompt_templates.py # 프롬프트 템플릿
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── upload.py         # 파일 업로드 엔드포인트
│   │       └── analysis.py       # 분석 요청 엔드포인트
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── UploadZone.tsx
│   │   │   ├── RadarChart.tsx
│   │   │   ├── GaugeChart.tsx
│   │   │   ├── BarChart.tsx
│   │   │   └── ReportSection.tsx
│   │   ├── pages/
│   │   │   ├── Home.tsx
│   │   │   └── Results.tsx
│   │   ├── services/
│   │   │   └── api.ts
│   │   ├── types/
│   │   │   └── analysis.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   └── vite.config.ts
├── README.md
└── ARCHITECTURE.md
```

## 3. API 엔드포인트 설계

### POST /api/upload
- 파일 업로드 (PDF, DOCX, TXT)
- 응답: `{ file_id: string, filename: string }`

### POST /api/analyze
- 문서 분석 요청
- Body: `{ file_id: string }`
- 응답: 분석 결과 JSON

### GET /api/analysis/{analysis_id}
- 분석 결과 조회

## 4. 데이터 모델

### AnalysisResult
```typescript
{
  companySummary: string;           // 기업 5줄 요약
  tipsCategories: {                 // TIPS 분야별 점수
    category: string;
    score: number;                  // 0-100
  }[];
  evaluations: {
    technology: number;             // 기술성 0-100
    business: number;               // 사업성 0-100
    team: number;                   // 팀 역량 0-100
    tipsFit: number;                // TIPS 적합성 0-100
  };
  overallScore: number;            // 종합 점수
  recommendation: "추천" | "보류" | "비추천";
  strengths: string[];              // 강점 TOP 3
  risks: string[];                 // 리스크 TOP 3
  comments: string;                 // 심사역 코멘트
}
```

## 5. LLM 분석 파이프라인

1. **문서 추출**: PDF/DOCX → 텍스트
2. **문서 요약**: 핵심 정보 추출
3. **분류 분석**: TIPS 분야 분류 + 점수
4. **평가 분석**: 4가지 관점 점수화
5. **종합 판단**: 추천/보류/비추천 결정
6. **설명 생성**: 코멘트 및 강점/리스크 도출

## 6. 프롬프트 설계 전략

- **구조화된 출력**: JSON Schema 강제
- **평가 기준 명시**: 각 항목별 평가 기준 포함
- **VC 톤 유지**: 심사역 관점의 객관적 분석
- **Few-shot 예시**: 일관성 있는 평가를 위한 예시 제공

## 7. 기술 스택

### Backend
- FastAPI 0.104+
- Python 3.11+
- PyPDF2 / pdfplumber (PDF 파싱)
- python-docx (DOCX 파싱)
- OpenAI API (GPT-4) 또는 Anthropic Claude
- Pydantic (데이터 검증)

### Frontend
- React 18+
- TypeScript 5+
- Vite
- Tailwind CSS 3+
- Recharts (차트 라이브러리)
- Axios (HTTP 클라이언트)

## 8. 보안 및 환경 변수

- API 키는 환경 변수로 관리
- 파일 업로드 크기 제한 (예: 10MB)
- CORS 설정
- 파일 타입 검증
