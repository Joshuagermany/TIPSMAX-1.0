@echo off
chcp 65001 >nul
echo TIPSMAX 1.0 Backend 시작 중...
echo.

REM Python 찾기 (Windows 스토어 스텁 제외)
set PYTHON_CMD=
set PYTHON_FOUND=0

REM 실제 Python 경로 찾기
if exist "%LOCALAPPDATA%\Programs\Python\Python314\python.exe" (
    set PYTHON_CMD=%LOCALAPPDATA%\Programs\Python\Python314\python.exe
    set PYTHON_FOUND=1
) else if exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" (
    set PYTHON_CMD=%LOCALAPPDATA%\Programs\Python\Python313\python.exe
    set PYTHON_FOUND=1
) else if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    set PYTHON_CMD=%LOCALAPPDATA%\Programs\Python\Python312\python.exe
    set PYTHON_FOUND=1
) else if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    set PYTHON_CMD=%LOCALAPPDATA%\Programs\Python\Python311\python.exe
    set PYTHON_FOUND=1
)

REM 직접 경로를 못 찾으면 명령어로 시도
if %PYTHON_FOUND%==0 (
    python --version >nul 2>&1
    if not errorlevel 1 (
        REM 버전 확인해서 실제 Python인지 체크
        for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
        echo %PYTHON_VERSION% | findstr /R "Python [0-9]" >nul
        if not errorlevel 1 (
            set PYTHON_CMD=python
            set PYTHON_FOUND=1
        )
    )
)

if %PYTHON_FOUND%==0 (
    echo [오류] Python을 찾을 수 없습니다.
    echo.
    echo Python 3.11 이상이 설치되어 있는지 확인하세요.
    echo 일반 설치 경로: %LOCALAPPDATA%\Programs\Python\
    echo.
    pause
    exit /b 1
)

REM 가상환경 확인 및 생성
if not exist "venv" (
    echo [1/3] 가상환경 생성 중...
    "%PYTHON_CMD%" -m venv venv
    if errorlevel 1 (
        echo [오류] 가상환경 생성 실패
        pause
        exit /b 1
    )
    echo [완료] 가상환경 생성 완료
) else (
    echo [확인] 가상환경이 이미 있습니다
)

REM 가상환경 활성화
echo 가상환경 활성화 중...
call venv\Scripts\activate.bat

REM 의존성 설치 확인
if not exist "venv\Lib\site-packages\fastapi" (
    echo 의존성 설치 중...
    pip install -r requirements.txt
)

REM 서버 실행
echo.
echo Backend 서버 시작 중...
echo 접속 주소: http://localhost:8000
echo API 문서: http://localhost:8000/docs
echo.
uvicorn app.main:app --reload

pause
