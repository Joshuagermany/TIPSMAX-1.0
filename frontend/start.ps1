# TIPSMAX 1.0 Frontend 시작 스크립트

Write-Host "TIPSMAX 1.0 Frontend 시작 중..." -ForegroundColor Cyan
Write-Host ""

# Node.js 확인
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "Node.js가 설치되어 있지 않습니다." -ForegroundColor Red
    Write-Host "Node.js 18 이상을 설치해주세요: https://nodejs.org/" -ForegroundColor Yellow
    Read-Host "계속하려면 Enter를 누르세요"
    exit 1
}

# 의존성 설치 확인
if (-not (Test-Path "node_modules")) {
    Write-Host "의존성 설치 중..." -ForegroundColor Yellow
    npm install
}

# 개발 서버 실행
Write-Host ""
Write-Host "Frontend 개발 서버 시작 중..." -ForegroundColor Green
Write-Host "접속 주소: http://localhost:5173" -ForegroundColor Cyan
Write-Host ""
npm run dev
