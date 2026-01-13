# Google OAuth 설정 가이드

## 문제
`redirect_uri_mismatch` 오류가 발생하는 경우, Google Cloud Console에 리다이렉트 URI가 등록되지 않았거나 일치하지 않을 때 발생합니다.

## 해결 방법

### 1. Google Cloud Console 접속
1. [Google Cloud Console](https://console.cloud.google.com/)에 접속
2. 프로젝트 선택 (또는 새 프로젝트 생성)

### 2. OAuth 동의 화면 설정
1. 왼쪽 메뉴에서 **"API 및 서비스"** > **"OAuth 동의 화면"** 클릭
2. 사용자 유형 선택 (내부/외부)
3. 앱 정보 입력:
   - 앱 이름: TIPSMAX 1.0
   - 사용자 지원 이메일: 선택
   - 개발자 연락처 정보: 이메일 입력
4. **저장 후 계속** 클릭

### 3. 승인된 리디렉션 URI 등록
1. 왼쪽 메뉴에서 **"API 및 서비스"** > **"사용자 인증 정보"** 클릭
2. OAuth 2.0 클라이언트 ID 목록에서 해당 클라이언트 ID 클릭 (또는 새로 생성)
3. **"승인된 리디렉션 URI"** 섹션에서 **"URI 추가"** 클릭
4. 다음 URI들을 추가:
   ```
   http://localhost:5173/login
   http://localhost:5173/login?provider=google
   ```
   또는 더 정확하게:
   ```
   http://localhost:5173/login?provider=google
   ```
5. **저장** 클릭

### 4. 프로덕션 환경용 URI (선택사항)
프로덕션 환경을 사용하는 경우, 실제 도메인도 추가:
```
https://yourdomain.com/login
https://yourdomain.com/login?provider=google
```

## 현재 사용 중인 리다이렉트 URI
- 개발 환경: `http://localhost:5173/login?provider=google`
- 포트가 다른 경우 해당 포트로 변경

## 확인 사항
1. 클라이언트 ID가 코드와 일치하는지 확인
2. 리다이렉트 URI가 정확히 일치하는지 확인 (대소문자, 슬래시, 쿼리 파라미터 포함)
3. 변경 사항이 저장되었는지 확인 (저장 후 몇 분 소요될 수 있음)

## 참고
- Google OAuth는 리다이렉트 URI를 정확히 일치시켜야 합니다
- 쿼리 파라미터(`?provider=google`)도 URI의 일부이므로 정확히 일치해야 합니다
- 변경 사항이 반영되는 데 몇 분이 걸릴 수 있습니다
