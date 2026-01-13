# GitHub 푸시 가이드

## 빠른 시작

### 1단계: Git 설치

Git이 설치되어 있지 않다면:
1. https://git-scm.com/download/win 에서 다운로드
2. 설치 시 **"Add Git to PATH"** 옵션 체크
3. PowerShell 재시작

### 2단계: GitHub 저장소 생성

1. GitHub에 로그인: https://github.com
2. 새 저장소 생성: https://github.com/new
3. 저장소 이름: `TIPSMAX-1.0`
4. Public 또는 Private 선택
5. **README, .gitignore, license 추가하지 않기** (이미 있음)

### 3단계: 코드 푸시

**방법 1: 자동 스크립트 사용 (권장)**
```powershell
.\push_to_github.ps1
```

**방법 2: 수동 실행**
```powershell
cd "C:\Users\venturus01\Desktop\TIPSMAX 1.0"

# Git 초기화 (처음 한 번만)
git init

# 원격 저장소 추가
git remote add origin https://github.com/joshuagermany/TIPSMAX-1.0.git

# 파일 추가 및 커밋
git add .
git commit -m "Initial commit: TIPSMAX 1.0"

# 푸시
git branch -M main
git push -u origin main
```

## 인증 문제 해결

### Personal Access Token 사용

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. "Generate new token" 클릭
3. 권한 선택: `repo` 체크
4. 토큰 생성 후 복사
5. 푸시 시 비밀번호 대신 토큰 사용

### GitHub Desktop 사용

1. GitHub Desktop 설치: https://desktop.github.com/
2. 저장소 열기: File → Add Local Repository
3. 프로젝트 폴더 선택
4. Publish repository 클릭

## 주의사항

- `.env` 파일은 `.gitignore`에 포함되어 있어 푸시되지 않습니다
- `venv/` 폴더도 제외됩니다
- `node_modules/`도 제외됩니다
- 업로드된 파일(`backend/uploads/`)도 제외됩니다

## 추가 명령어

```powershell
# 상태 확인
git status

# 변경사항 확인
git diff

# 커밋 히스토리
git log

# 원격 저장소 확인
git remote -v
```
