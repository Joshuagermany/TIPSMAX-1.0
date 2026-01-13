# Python 설치 가이드

## 🔴 현재 상황

Python이 설치되어 있지 않습니다. 먼저 Python을 설치해야 합니다.

## ✅ Python 설치 방법 (3단계)

### 1단계: Python 다운로드

1. **공식 웹사이트 방문**: https://www.python.org/downloads/
2. **"Download Python 3.12.x"** 버튼 클릭 (최신 버전)
   - 또는 Python 3.11 이상이면 OK

### 2단계: Python 설치

1. 다운로드한 `.exe` 파일 실행
2. ⚠️ **중요**: 설치 화면에서 **"Add Python to PATH"** 체크박스를 반드시 체크하세요!
3. "Install Now" 클릭

### 3단계: 설치 확인

**새 PowerShell 창**을 열고:
```powershell
python --version
```

다음과 같이 표시되면 성공:
```
Python 3.12.0
```

## 🚀 설치 후 TIPSMAX 실행

Python 설치가 완료되면:

### 방법 1: 배치 파일 (가장 간단)

**Backend:**
```
backend 폴더 → start.bat 더블클릭
```

**Frontend:**
```
frontend 폴더 → start.bat 더블클릭
```

### 방법 2: PowerShell 스크립트

```powershell
cd "C:\Users\venturus01\Desktop\TIPSMAX 1.0\backend"
.\setup_and_run.ps1
```

### 방법 3: 수동 실행

```powershell
cd "C:\Users\venturus01\Desktop\TIPSMAX 1.0\backend"
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## ❓ 문제 해결

### "Add Python to PATH"를 체크 안 했어요!

**해결 방법:**

1. **Python 재설치** (권장)
   - 제어판 → 프로그램 및 기능 → Python 제거
   - 위 방법대로 다시 설치 (이번엔 PATH 체크!)

2. **또는 수동으로 PATH 추가**
   - Python이 설치된 경로 찾기 (보통 `C:\Users\사용자명\AppData\Local\Programs\Python\Python3XX`)
   - 시스템 환경 변수 → Path에 다음 추가:
     - `C:\Users\사용자명\AppData\Local\Programs\Python\Python3XX`
     - `C:\Users\사용자명\AppData\Local\Programs\Python\Python3XX\Scripts`

### 여전히 "python" 명령어가 안 돼요!

1. **PowerShell 재시작** (새 창 열기)
2. 설치 경로 확인:
   ```powershell
   Get-ChildItem "$env:LOCALAPPDATA\Programs\Python" -Recurse -Filter "python.exe"
   ```
3. 위 경로를 PATH에 추가

## 📞 도움이 필요하신가요?

- Python 공식 문서: https://docs.python.org/3/
- Python 설치 문제: https://docs.python.org/3/using/windows.html
