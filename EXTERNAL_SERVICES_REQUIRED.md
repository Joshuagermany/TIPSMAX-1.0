# TIPSMAX 1.0 - 필요한 외부 서비스 및 API

## 🔴 필수 (AI 분석 기능 사용 시)

### 1. LLM API (OpenAI 또는 Anthropic 중 하나 선택)

**OpenAI API**
- **사이트**: https://platform.openai.com/
- **필요한 것**: 
  - OpenAI 계정 생성
  - API 키 발급 (Billing 설정 필요)
  - 모델: `gpt-4-turbo-preview` 또는 `gpt-4o` (권장)
- **비용**: 사용량 기반 (토큰당 과금)
- **설정 방법**:
  ```env
  LLM_PROVIDER=openai
  OPENAI_API_KEY=sk-your-api-key-here
  OPENAI_MODEL=gpt-4-turbo-preview
  ```

**Anthropic Claude API** (대안)
- **사이트**: https://console.anthropic.com/
- **필요한 것**:
  - Anthropic 계정 생성
  - API 키 발급
  - 모델: `claude-3-opus-20240229` 또는 `claude-3-5-sonnet-20241022` (권장)
- **비용**: 사용량 기반 (토큰당 과금)
- **설정 방법**:
  ```env
  LLM_PROVIDER=anthropic
  ANTHROPIC_API_KEY=sk-ant-your-api-key-here
  ANTHROPIC_MODEL=claude-3-opus-20240229
  ```

**⚠️ 중요**: API 키가 없으면 Mock 데이터만 반환됩니다 (실제 분석 불가)

---

## 🟡 선택사항 (소셜 로그인 기능 사용 시)

### 2. 카카오 OAuth

**카카오 개발자 콘솔**
- **사이트**: https://developers.kakao.com/
- **필요한 것**:
  - 카카오 계정으로 로그인
  - 내 애플리케이션 생성
  - REST API 키 발급
  - Client Secret (선택사항, 보안 강화용)
  - Redirect URI 등록: `http://localhost:5173/login?provider=kakao`
- **설정 방법**:
  ```env
  KAKAO_REST_API_KEY=your_rest_api_key
  KAKAO_CLIENT_SECRET=your_client_secret (선택사항)
  KAKAO_REDIRECT_URI=http://localhost:5173/login?provider=kakao
  ```

### 3. 구글 OAuth

**Google Cloud Console**
- **사이트**: https://console.cloud.google.com/
- **필요한 것**:
  - Google 계정
  - 프로젝트 생성
  - OAuth 2.0 클라이언트 ID 생성
  - 승인된 리디렉션 URI 등록: `http://localhost:5173/login?provider=google`
- **설정 방법**:
  ```env
  GOOGLE_CLIENT_ID=your_client_id
  GOOGLE_CLIENT_SECRET=your_client_secret
  GOOGLE_REDIRECT_URI=http://localhost:5173/login?provider=google
  ```

### 4. 네이버 OAuth

**네이버 개발자 센터**
- **사이트**: https://developers.naver.com/
- **필요한 것**:
  - 네이버 계정
  - 애플리케이션 등록
  - Client ID 및 Client Secret 발급
  - 서비스 URL 및 Callback URL 등록: `http://localhost:5173/login?provider=naver`
- **설정 방법**:
  ```env
  NAVER_CLIENT_ID=your_client_id
  NAVER_CLIENT_SECRET=your_client_secret
  NAVER_REDIRECT_URI=http://localhost:5173/login?provider=naver
  ```

---

## 📋 요약

### 최소 구성 (기본 기능만 사용)
- ✅ **LLM API** (OpenAI 또는 Anthropic) - **필수**
- ❌ OAuth 서비스 - 불필요 (로그인 없이 사용 가능)

### 완전한 구성 (모든 기능 사용)
- ✅ **LLM API** (OpenAI 또는 Anthropic) - **필수**
- ✅ **카카오 OAuth** - 선택사항
- ✅ **구글 OAuth** - 선택사항
- ✅ **네이버 OAuth** - 선택사항

---

## 💰 예상 비용

### LLM API 비용 (문서 분석 1회당)
- **OpenAI GPT-4 Turbo**: 약 $0.01 ~ $0.05 (문서 길이에 따라 다름)
- **Anthropic Claude Opus**: 약 $0.03 ~ $0.15 (문서 길이에 따라 다름)

### OAuth 서비스
- **무료** (모든 OAuth 서비스 무료 제공)

---

## 🔧 설정 방법

1. **Backend `.env` 파일 생성**:
   ```bash
   cd backend
   # .env 파일이 없으면 env.example.txt를 참고하여 생성
   ```

2. **필수 API 키 설정**:
   ```env
   # LLM API (필수)
   LLM_PROVIDER=openai
   OPENAI_API_KEY=sk-your-api-key-here
   OPENAI_MODEL=gpt-4-turbo-preview
   ```

3. **OAuth 설정** (선택사항):
   ```env
   # 카카오
   KAKAO_REST_API_KEY=your_key
   KAKAO_CLIENT_SECRET=your_secret
   
   # 구글
   GOOGLE_CLIENT_ID=your_id
   GOOGLE_CLIENT_SECRET=your_secret
   
   # 네이버
   NAVER_CLIENT_ID=your_id
   NAVER_CLIENT_SECRET=your_secret
   ```

4. **서버 재시작**:
   - 환경 변수 변경 후 Backend 서버 재시작 필요

---

## ⚠️ 주의사항

1. **API 키 보안**:
   - `.env` 파일은 절대 Git에 커밋하지 마세요
   - `.gitignore`에 이미 포함되어 있습니다
   - 프로덕션 환경에서는 환경 변수로 관리하세요

2. **OAuth Redirect URI**:
   - 개발 환경: `http://localhost:5173/login?provider={provider}`
   - 프로덕션 환경: 실제 도메인으로 변경 필요

3. **API 키 없이 사용 시**:
   - LLM API 키가 없으면 Mock 데이터만 반환됩니다
   - 실제 분석은 불가능하지만 UI 테스트는 가능합니다
