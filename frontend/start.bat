@echo off
echo TIPSMAX 1.0 Frontend 시작 중...
echo.

REM Node.js 확인
where node >nul 2>&1
if errorlevel 1 (
    echo Node.js가 설치되어 있지 않습니다.
    echo Node.js 18 이상을 설치해주세요: https://nodejs.org/
    pause
    exit /b 1
)

REM 의존성 설치 확인
if not exist "node_modules" (
    echo 의존성 설치 중...
    call npm install
)

REM 개발 서버 실행
echo.
echo Frontend 개발 서버 시작 중...
echo 접속 주소: http://localhost:5173
echo.
call npm run dev

pause
