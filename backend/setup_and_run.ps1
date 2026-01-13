# TIPSMAX 1.0 Backend 설정 및 실행 스크립트

Write-Host "=== TIPSMAX 1.0 Backend 설정 ===" -ForegroundColor Cyan
Write-Host ""

# Python 찾기
$pythonCmd = $null
$pythonPaths = @("python", "python3", "py", "$env:LOCALAPPDATA\Programs\Python\Python*\python.exe")

foreach ($path in $pythonPaths) {
    try {
        if ($path -match "\\") {
            # 전체 경로인 경우
            $found = Get-ChildItem -Path $path -ErrorAction SilentlyContinue | Select-Object -First 1
            if ($found) {
                $pythonCmd = $found.FullName
                break
            }
        } else {
            # 명령어인 경우
            $found = Get-Command $path -ErrorAction SilentlyContinue
            if ($found) {
                $pythonCmd = $found.Path
                break
            }
        }
    } catch {
        continue
    }
}

if (-not $pythonCmd) {
    Write-Host "❌ Python을 찾을 수 없습니다!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Python 설치가 필요합니다:" -ForegroundColor Yellow
    Write-Host "1. https://www.python.org/downloads/ 에서 Python 3.11 이상 다운로드" -ForegroundColor Yellow
    Write-Host "2. 설치 시 'Add Python to PATH' 옵션 체크" -ForegroundColor Yellow
    Write-Host "3. 설치 후 PowerShell을 다시 시작" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "또는 이미 설치되어 있다면:" -ForegroundColor Yellow
    Write-Host "- Python이 설치된 경로를 PATH 환경 변수에 추가하세요" -ForegroundColor Yellow
    Read-Host "Enter를 눌러 종료"
    exit 1
}

Write-Host "✅ Python 발견: $pythonCmd" -ForegroundColor Green
$version = & $pythonCmd --version 2>&1
Write-Host "   버전: $version" -ForegroundColor Gray
Write-Host ""

# 가상환경 확인 및 생성
if (-not (Test-Path "venv")) {
    Write-Host "📦 가상환경 생성 중..." -ForegroundColor Yellow
    & $pythonCmd -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ 가상환경 생성 실패" -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ 가상환경 생성 완료" -ForegroundColor Green
}

# 가상환경 활성화 (여러 방법 시도)
$activated = $false

# 방법 1: Activate.ps1 직접 실행
if (Test-Path "venv\Scripts\Activate.ps1") {
    try {
        & "venv\Scripts\Activate.ps1"
        $activated = $true
        Write-Host "✅ 가상환경 활성화 완료 (방법 1)" -ForegroundColor Green
    } catch {
        Write-Host "⚠️  방법 1 실패, 다른 방법 시도 중..." -ForegroundColor Yellow
    }
}

# 방법 2: 환경 변수 직접 설정
if (-not $activated) {
    $env:VIRTUAL_ENV = (Resolve-Path "venv").Path
    $env:PATH = "$env:VIRTUAL_ENV\Scripts;$env:PATH"
    $env:PSModulePath = "$env:VIRTUAL_ENV\Lib\site-packages;$env:PSModulePath"
    $activated = $true
    Write-Host "✅ 가상환경 활성화 완료 (방법 2 - 환경 변수)" -ForegroundColor Green
}

Write-Host ""

# pip 확인 및 업그레이드
Write-Host "📦 pip 업그레이드 중..." -ForegroundColor Yellow
& "$env:VIRTUAL_ENV\Scripts\python.exe" -m pip install --upgrade pip --quiet
Write-Host ""

# 의존성 설치
if (-not (Test-Path "venv\Lib\site-packages\fastapi")) {
    Write-Host "📦 패키지 설치 중... (시간이 걸릴 수 있습니다)" -ForegroundColor Yellow
    & "$env:VIRTUAL_ENV\Scripts\python.exe" -m pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ 패키지 설치 실패" -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ 패키지 설치 완료" -ForegroundColor Green
} else {
    Write-Host "✅ 패키지가 이미 설치되어 있습니다" -ForegroundColor Green
}

Write-Host ""

# .env 파일 확인
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  .env 파일이 없습니다" -ForegroundColor Yellow
    Write-Host "   Mock 결과로 실행됩니다 (실제 분석을 원하면 .env 파일을 설정하세요)" -ForegroundColor Yellow
    Write-Host ""
}

# 서버 실행
Write-Host "🚀 Backend 서버 시작 중..." -ForegroundColor Green
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "  접속 주소: http://localhost:8000" -ForegroundColor White
Write-Host "  API 문서:  http://localhost:8000/docs" -ForegroundColor White
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""
Write-Host "서버를 종료하려면 Ctrl+C를 누르세요" -ForegroundColor Gray
Write-Host ""

& "$env:VIRTUAL_ENV\Scripts\uvicorn.exe" app.main:app --reload
