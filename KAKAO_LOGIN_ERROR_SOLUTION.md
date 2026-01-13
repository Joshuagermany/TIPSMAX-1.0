# 카카오 로그인 오류 해결 가이드

## 🔴 현재 오류

```
카카오 토큰 발급 실패: {"error":"invalid_client","error_description":"Bad client credentials","error_code":"KOE010"}
```

## 📋 원인 분석

### 1. Client Secret 문제 (가장 가능성 높음)

**현재 상태:**
- 코드에서 `KAKAO_CLIENT_SECRET`이 빈 문자열로 설정됨
- 로그에 "Client Secret 미사용 (기본 설정)" 표시
- 카카오 개발자 콘솔에서 Client Secret이 **활성화**되어 있을 가능성

**카카오 개발자 콘솔 확인 방법:**
1. [카카오 개발자 콘솔](https://developers.kakao.com/) 접속
2. 내 애플리케이션 > 앱 선택
3. **앱 설정 > 앱 키** 메뉴로 이동
4. **Client Secret** 섹션 확인:
   - **활성화됨**: Client Secret 값이 표시됨 → 환경 변수에 설정 필요
   - **비활성화됨**: Client Secret이 없음 → 현재 코드 그대로 사용 가능

### 2. REST API KEY 문제

**확인 사항:**
- 카카오 개발자 콘솔의 **REST API 키**가 코드의 값과 일치하는지 확인
- 현재 코드: `84ebc5642421faf44961b796f6102ec4`
- 앱 상태가 **"운영중"** 또는 **"개발중"**인지 확인

### 3. Redirect URI 불일치

**현재 설정:**
- 코드: `http://localhost:5173/login?provider=kakao`
- 카카오 개발자 콘솔에 정확히 동일하게 등록되어 있어야 함

**확인 방법:**
1. 카카오 개발자 콘솔 > **제품 설정 > 카카오 로그인** 메뉴
2. **Redirect URI** 섹션에서 다음 URI가 등록되어 있는지 확인:
   ```
   http://localhost:5173/login?provider=kakao
   ```
3. 정확히 일치해야 함 (대소문자, 슬래시, 쿼리 파라미터 포함)

## ✅ 해결 방법

### 방법 1: Client Secret이 활성화된 경우

1. **카카오 개발자 콘솔에서 Client Secret 복사**
   - 앱 설정 > 앱 키 > Client Secret 값 복사

2. **환경 변수 설정**
   
   **Windows PowerShell:**
   ```powershell
   $env:KAKAO_CLIENT_SECRET="복사한_Client_Secret_값"
   ```
   
   **또는 .env 파일 생성 (backend 폴더에):**
   ```env
   KAKAO_REST_API_KEY=84ebc5642421faf44961b796f6102ec4
   KAKAO_CLIENT_SECRET=복사한_Client_Secret_값
   KAKAO_REDIRECT_URI=http://localhost:5173/login?provider=kakao
   ```
   
   **.env 파일 사용 시 python-dotenv 설치 필요:**
   ```bash
   pip install python-dotenv
   ```
   
   **main.py에 .env 로드 추가:**
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

3. **Backend 재시작**
   - 환경 변수 변경 후 서버 재시작 필요

### 방법 2: Client Secret 비활성화 (권장)

1. **카카오 개발자 콘솔에서 Client Secret 비활성화**
   - 앱 설정 > 앱 키 > Client Secret 섹션
   - "비활성화" 또는 "사용 안 함" 선택
   - 저장

2. **코드는 그대로 사용**
   - Client Secret이 비활성화되면 현재 코드 그대로 작동

### 방법 3: Redirect URI 확인 및 수정

1. **카카오 개발자 콘솔 확인**
   - 제품 설정 > 카카오 로그인 > Redirect URI
   - `http://localhost:5173/login?provider=kakao` 추가

2. **코드와 일치 확인**
   - `backend/app/routes/auth.py`의 `KAKAO_REDIRECT_URI` 값 확인
   - 정확히 일치하도록 수정

## 🔍 디버깅 체크리스트

- [ ] 카카오 개발자 콘솔에서 Client Secret 상태 확인
- [ ] REST API KEY가 정확한지 확인
- [ ] Redirect URI가 정확히 일치하는지 확인
- [ ] 앱 상태가 "운영중" 또는 "개발중"인지 확인
- [ ] 환경 변수가 올바르게 설정되었는지 확인
- [ ] Backend 서버를 재시작했는지 확인

## 📝 참고

- **KOE010**: 클라이언트 자격 증명 오류
- 카카오 OAuth는 Client Secret 활성화 여부에 따라 요구사항이 다름
- Redirect URI는 정확히 일치해야 함 (대소문자, 슬래시, 쿼리 파라미터 포함)
