# GitHub 푸시 가이드

## 현재 상태

- ✅ Git 저장소 초기화 완료
- ✅ 원격 저장소 설정 완료: `https://github.com/joshuagermany/TIPSMAX-1.0.git`
- ✅ 커밋 완료 (57개 파일)
- ❌ 푸시 실패 (403 권한 오류)

## 해결 방법

### 1단계: GitHub 저장소 확인

1. GitHub에 로그인: https://github.com/joshuagermany
2. 저장소가 존재하는지 확인: https://github.com/joshuagermany/TIPSMAX-1.0

**저장소가 없다면:**
- 새 저장소 생성: https://github.com/new
- 저장소 이름: `TIPSMAX-1.0` (정확히 일치해야 함)
- Public 또는 Private 선택
- **README, .gitignore, license 추가하지 않기** (이미 있음)

### 2단계: Personal Access Token 확인

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. 토큰 확인:
   - `repo` 권한이 체크되어 있는지 확인
   - 토큰이 만료되지 않았는지 확인

### 3단계: 푸시 재시도

저장소를 생성한 후 다음 명령어 실행:

```powershell
cd "C:\Users\venturus01\Desktop\TIPSMAX 1.0"

# 토큰을 사용하여 원격 URL 설정
# 주의: 실제 토큰은 환경 변수나 안전한 곳에 저장하세요
$token = "YOUR_GITHUB_PERSONAL_ACCESS_TOKEN"
& "C:\Program Files\Git\bin\git.exe" remote set-url origin "https://$token@github.com/joshuagermany/TIPSMAX-1.0.git"

# 푸시
& "C:\Program Files\Git\bin\git.exe" push -u origin main
```

## 대안: GitHub Desktop 사용

1. GitHub Desktop 설치: https://desktop.github.com/
2. File → Add Local Repository
3. 프로젝트 폴더 선택: `C:\Users\venturus01\Desktop\TIPSMAX 1.0`
4. "Publish repository" 클릭

## 저장소 이름 확인

현재 설정된 저장소:
- `https://github.com/joshuagermany/TIPSMAX-1.0.git`

저장소 이름이 다르다면 (예: `tipsmax-1.0`, `TIPSMAX1.0` 등):
```powershell
& "C:\Program Files\Git\bin\git.exe" remote set-url origin "https://토큰@github.com/joshuagermany/실제저장소이름.git"
```
