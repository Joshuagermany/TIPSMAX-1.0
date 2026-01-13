# TIPSMAX 1.0 실행 가이드

## 🔍 문제 해결: PowerShell 실행 오류

PowerShell에서 `Activate.ps1` 실행이 안 되는 경우, 다음 방법을 시도하세요.

## ✅ 해결 방법 1: 배치 파일 사용 (가장 간단)

**Backend 실행:**
```
backend 폴더에서 start.bat 더블클릭
```

**Frontend 실행:**
```
frontend 폴더에서 start.bat 더블클릭
```

## ✅ 해결 방법 2: 개선된 PowerShell 스크립트 사용

**Backend 실행:**
```powershell
cd backend
.\setup_and_run.ps1
```

이 스크립트는:
- Python 자동 감지
- 가상환경 자동 생성
- 실행 정책 문제 자동 우회
- 패키지 자동 설치

## ✅ 해결 방법 3: 수동 실행 (Python이 설치되어 있을 때)

### Backend

**PowerShell에서:**
```powershell
cd "C:\Users\venturus01\Desktop\TIPSMAX 1.0\backend"

# Python 확인
python --version

# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (실행 정책 문제 시 이 방법 사용)
$env:VIRTUAL_ENV = "$PWD\venv"
$env:PATH = "$PWD\venv\Scripts;$env:PATH"

# 패키지 설치
pip install -r requirements.txt

# 서버 실행
uvicorn app.main:app --reload
```

**또는 CMD에서:**
```cmd
cd "C:\Users\venturus01\Desktop\TIPSMAX 1.0\backend"
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

**PowerShell 또는 CMD에서:**
```powershell
cd "C:\Users\venturus01\Desktop\TIPSMAX 1.0\frontend"
npm install
npm run dev
```

## ❌ Python이 설치되어 있지 않은 경우

1. **Python 다운로드 및 설치**
   - https://www.python.org/downloads/
   - Python 3.11 이상 다운로드
   - ⚠️ **중요**: 설치 시 **"Add Python to PATH"** 옵션 체크

2. **설치 확인**
   ```powershell
   python --version
   ```

3. **설치 후 PowerShell 재시작**

## 🎯 실행 순서

1. **Backend 실행** (첫 번째 터미널)
   ```
   backend\start.bat (더블클릭)
   ```
   → `http://localhost:8000` 에서 실행

2. **Frontend 실행** (두 번째 터미널)
   ```
   frontend\start.bat (더블클릭)
   ```
   → `http://localhost:5173` 에서 실행

3. **브라우저 접속**
   ```
   http://localhost:5173
   ```

## 🐛 자주 발생하는 오류

### 오류: "python은(는) 내부 또는 외부 명령, 실행할 수 있는 프로그램, 또는 배치 파일이 아닙니다."

**해결:** Python이 PATH에 없음
1. Python 재설치 (Add to PATH 옵션 체크)
2. 또는 Python 경로를 PATH에 수동 추가

### 오류: "Activate.ps1을 로드할 수 없습니다"

**해결:** 실행 정책 문제
- `start.bat` 파일 사용 (CMD 방식)
- 또는 `setup_and_run.ps1` 사용 (자동 우회)

### 오류: "npm은(는) 내부 또는 외부 명령..."

**해결:** Node.js가 설치되어 있지 않음
- https://nodejs.org/ 에서 Node.js 18 이상 설치

## 💡 팁

- **가장 쉬운 방법**: `start.bat` 파일 더블클릭
- Backend와 Frontend는 **별도의 터미널**에서 실행
- Backend가 먼저 실행되어야 Frontend가 연결 가능
