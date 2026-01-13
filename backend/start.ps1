# TIPSMAX 1.0 Backend 시작 스크립트

Write-Host "TIPSMAX 1.0 Backend 시작 중..." -ForegroundColor Cyan
Write-Host ""

# Python 확인
$pythonCmd = $null
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $pythonCmd = "python3"
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonCmd = "py"
} else {
    Write-Host "Python이 설치되어 있지 않습니다." -ForegroundColor Red
    Write-Host "Python 3.11 이상을 설치해주세요: https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "계속하려면 Enter를 누르세요"
    exit 1
}

# 가상환경 확인 및 생성
if (-not (Test-Path "venv")) {
    Write-Host "가상환경 생성 중..." -ForegroundColor Yellow
    & $pythonCmd -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "가상환경 생성 실패" -ForegroundColor Red
        exit 1
    }
}

# 가상환경 활성화
Write-Host "가상환경 활성화 중..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# 실행 정책 오류 시 대안
if ($LASTEXITCODE -ne 0) {
    Write-Host "PowerShell 실행 정책 문제로 인해 직접 활성화합니다..." -ForegroundColor Yellow
    $env:VIRTUAL_ENV = "$PWD\venv"
    $env:PATH = "$PWD\venv\Scripts;$env:PATH"
}

# 의존성 설치 확인
if (-not (Test-Path "venv\Lib\site-packages\fastapi")) {
    Write-Host "의존성 설치 중..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

# 서버 실행
Write-Host ""
Write-Host "Backend 서버 시작 중..." -ForegroundColor Green
Write-Host "접속 주소: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API 문서: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
uvicorn app.main:app --reload
