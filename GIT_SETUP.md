# GitHub 푸시 가이드

## Git 설치 필요

Git이 설치되어 있지 않습니다. 먼저 Git을 설치해야 합니다.

## Git 설치 방법

### 방법 1: 공식 웹사이트에서 설치 (권장)

1. **Git 다운로드**: https://git-scm.com/download/win
2. **설치 실행**: 다운로드한 `.exe` 파일 실행
3. **중요**: 설치 시 "Add Git to PATH" 옵션 체크
4. **설치 완료 후**: PowerShell 재시작

### 방법 2: GitHub Desktop 사용

- GitHub Desktop 설치: https://desktop.github.com/
- 자동으로 Git이 포함되어 있음

## Git 설치 확인

설치 후 새 PowerShell 창에서:
```powershell
git --version
```

## GitHub에 푸시하기

Git 설치 후 다음 명령어를 실행하세요:

```powershell
cd "C:\Users\venturus01\Desktop\TIPSMAX 1.0"

# Git 저장소 초기화 (처음 한 번만)
git init

# 원격 저장소 추가
git remote add origin https://github.com/joshuagermany/TIPSMAX-1.0.git

# 또는 이미 원격 저장소가 있다면
git remote set-url origin https://github.com/joshuagermany/TIPSMAX-1.0.git

# 모든 파일 추가
git add .

# 커밋
git commit -m "Initial commit: TIPSMAX 1.0 - TIPS 적합성 분석 AI 에이전트"

# 푸시 (main 브랜치)
git branch -M main
git push -u origin main
```

## 자동화 스크립트

Git 설치 후 `push_to_github.ps1` 스크립트를 실행하세요.
