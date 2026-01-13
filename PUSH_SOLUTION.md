# GitHub 푸시 해결 방법

## 현재 문제

토큰 권한 오류 (403)가 발생하고 있습니다.

## 해결 방법

### 방법 1: GitHub Desktop 사용 (가장 쉬움) ⭐

1. **GitHub Desktop 설치**
   - https://desktop.github.com/ 접속
   - 다운로드 및 설치

2. **저장소 추가**
   - GitHub Desktop 실행
   - File → Add Local Repository
   - "Choose..." 클릭
   - 프로젝트 폴더 선택: `C:\Users\venturus01\Desktop\TIPSMAX 1.0`
   - "Add repository" 클릭

3. **푸시**
   - 상단의 "Publish repository" 버튼 클릭
   - 저장소 이름 확인: `TIPSMAX-1.0`
   - "Publish repository" 클릭

### 방법 2: 새 Personal Access Token 생성

1. **GitHub에서 토큰 생성**
   - https://github.com/settings/tokens 접속
   - "Generate new token (classic)" 클릭
   - Note: "TIPSMAX-1.0 Push" 입력
   - Expiration: 원하는 기간 선택
   - **Scopes**: `repo` 체크 (모든 repo 권한)
   - "Generate token" 클릭
   - 토큰 복사 (한 번만 표시됨!)

2. **토큰으로 푸시**
   ```powershell
   cd "C:\Users\venturus01\Desktop\TIPSMAX 1.0"
   
   # 새 토큰으로 원격 URL 설정
   $newToken = "새로_생성한_토큰"
   & "C:\Program Files\Git\bin\git.exe" remote set-url origin "https://$newToken@github.com/Joshuagermany/TIPSMAX-1.0.git"
   
   # 푸시
   & "C:\Program Files\Git\bin\git.exe" push -u origin main
   ```

### 방법 3: SSH 키 사용

1. **SSH 키 생성**
   ```powershell
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

2. **SSH 키를 GitHub에 추가**
   - https://github.com/settings/keys 접속
   - "New SSH key" 클릭
   - `C:\Users\venturus01\.ssh\id_ed25519.pub` 파일 내용 복사하여 추가

3. **원격 URL을 SSH로 변경**
   ```powershell
   & "C:\Program Files\Git\bin\git.exe" remote set-url origin git@github.com:Joshuagermany/TIPSMAX-1.0.git
   & "C:\Program Files\Git\bin\git.exe" push -u origin main
   ```

## 현재 상태

- ✅ 저장소 존재: https://github.com/Joshuagermany/TIPSMAX-1.0
- ✅ 커밋 완료: 57개 파일
- ✅ 원격 저장소 설정 완료
- ❌ 푸시 실패: 토큰 권한 문제

## 추천

**GitHub Desktop 사용을 권장합니다.** 가장 간단하고 안전합니다.
