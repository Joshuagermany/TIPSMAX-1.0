# Python 설치 필수 가이드

## ❌ 현재 상황

Python이 설치되어 있지 않습니다. Windows 스토어 스텁 파일만 있어서 `python --version`이 제대로 작동하지 않습니다.

## ✅ Python 설치 방법 (필수!)

### 방법 1: 공식 웹사이트에서 설치 (권장)

1. **Python 다운로드 페이지 방문**
   - https://www.python.org/downloads/
   - 또는 직접 다운로드: https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe

2. **다운로드한 파일 실행**

3. **⚠️ 매우 중요: 설치 옵션**
   - ✅ **"Add Python to PATH"** 체크박스를 반드시 체크하세요!
   - ✅ "Install for all users" (선택사항)
   - "Install Now" 클릭

4. **설치 완료 후**
   - PowerShell을 완전히 종료하고 새로 열기
   - 다음 명령어로 확인:
     ```powershell
     python --version
     ```
   - `Python 3.12.0` 같은 버전이 표시되면 성공!

### 방법 2: Microsoft Store에서 설치

1. Microsoft Store 열기
2. "Python 3.12" 검색
3. 설치
4. PowerShell 재시작 후 확인

## 🔍 설치 확인

설치 후 **새 PowerShell 창**에서:

```powershell
python --version
```

다음과 같이 나와야 합니다:
```
Python 3.12.0
```

## 🚀 설치 후 TIPSMAX 실행

Python 설치가 완료되면:

```powershell
cd "C:\Users\venturus01\Desktop\TIPSMAX 1.0\backend"

# 방법 1: 배치 파일 사용 (가장 간단)
.\start.bat

# 방법 2: 수동 실행
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## ❌ 여전히 문제가 있나요?

### "python --version"이 여전히 작동하지 않아요

1. **PowerShell 완전히 종료 후 재시작**
   - 모든 PowerShell 창 닫기
   - 새 PowerShell 창 열기

2. **PATH 환경 변수 확인**
   ```powershell
   $env:PATH -split ';' | Where-Object { $_ -like '*Python*' }
   ```
   - Python 경로가 없으면 PATH에 추가 필요

3. **Python 재설치**
   - 제어판 → 프로그램 및 기능 → Python 제거
   - 다시 설치 (이번엔 PATH 체크!)

### Python이 설치되었는데 명령어가 안 돼요

**수동으로 PATH 추가:**

1. Python 설치 경로 찾기 (보통):
   ```
   C:\Users\사용자명\AppData\Local\Programs\Python\Python312
   C:\Users\사용자명\AppData\Local\Programs\Python\Python312\Scripts
   ```

2. 시스템 환경 변수 편집:
   - `Win + R` → `sysdm.cpl` 입력
   - "고급" 탭 → "환경 변수"
   - "Path" 선택 → "편집"
   - "새로 만들기" → 위 경로들 추가
   - 확인 후 PowerShell 재시작

## 📞 도움말

- Python 공식 문서: https://docs.python.org/3/
- Windows 설치 가이드: https://docs.python.org/3/using/windows.html
