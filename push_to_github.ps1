# TIPSMAX 1.0 GitHub 푸시 스크립트

Write-Host "=== TIPSMAX 1.0 GitHub 푸시 ===" -ForegroundColor Cyan
Write-Host ""

# Git 확인
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Git이 설치되어 있지 않습니다!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Git 설치가 필요합니다:" -ForegroundColor Yellow
    Write-Host "1. https://git-scm.com/download/win 방문" -ForegroundColor White
    Write-Host "2. Git 다운로드 및 설치" -ForegroundColor White
    Write-Host "3. 설치 시 'Add Git to PATH' 옵션 체크" -ForegroundColor Red
    Write-Host "4. PowerShell 재시작 후 다시 실행" -ForegroundColor White
    Write-Host ""
    Write-Host "자세한 내용은 GIT_SETUP.md 파일을 참고하세요." -ForegroundColor Cyan
    
    $response = Read-Host "Git 다운로드 페이지를 열까요? (Y/N)"
    if ($response -eq "Y" -or $response -eq "y") {
        Start-Process "https://git-scm.com/download/win"
    }
    exit 1
}

Write-Host "✅ Git 발견: $(git --version)" -ForegroundColor Green
Write-Host ""

# 프로젝트 디렉토리로 이동
$projectPath = "C:\Users\venturus01\Desktop\TIPSMAX 1.0"
Set-Location $projectPath

Write-Host "프로젝트 디렉토리: $projectPath" -ForegroundColor Gray
Write-Host ""

# Git 저장소 초기화 확인
if (-not (Test-Path ".git")) {
    Write-Host "📦 Git 저장소 초기화 중..." -ForegroundColor Yellow
    git init
    Write-Host "✅ Git 저장소 초기화 완료" -ForegroundColor Green
} else {
    Write-Host "✅ Git 저장소가 이미 있습니다" -ForegroundColor Green
}

Write-Host ""

# 원격 저장소 설정
$remoteUrl = "https://github.com/joshuagermany/TIPSMAX-1.0.git"
$currentRemote = git remote get-url origin 2>$null

if ($LASTEXITCODE -ne 0) {
    Write-Host "📡 원격 저장소 추가 중..." -ForegroundColor Yellow
    git remote add origin $remoteUrl
    Write-Host "✅ 원격 저장소 추가 완료" -ForegroundColor Green
} elseif ($currentRemote -ne $remoteUrl) {
    Write-Host "📡 원격 저장소 URL 업데이트 중..." -ForegroundColor Yellow
    git remote set-url origin $remoteUrl
    Write-Host "✅ 원격 저장소 URL 업데이트 완료" -ForegroundColor Green
} else {
    Write-Host "✅ 원격 저장소가 이미 설정되어 있습니다" -ForegroundColor Green
}

Write-Host ""

# 파일 추가
Write-Host "📝 변경사항 추가 중..." -ForegroundColor Yellow
git add .
Write-Host "✅ 파일 추가 완료" -ForegroundColor Green
Write-Host ""

# 커밋 메시지
$commitMessage = Read-Host "커밋 메시지를 입력하세요 (Enter: 기본 메시지 사용)"
if ([string]::IsNullOrWhiteSpace($commitMessage)) {
    $commitMessage = "Initial commit: TIPSMAX 1.0 - TIPS 적합성 분석 AI 에이전트"
}

Write-Host ""
Write-Host "💾 커밋 중..." -ForegroundColor Yellow
git commit -m $commitMessage

if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  커밋할 변경사항이 없거나 이미 커밋되어 있습니다." -ForegroundColor Yellow
} else {
    Write-Host "✅ 커밋 완료" -ForegroundColor Green
}

Write-Host ""

# 브랜치를 main으로 설정
Write-Host "🌿 브랜치 설정 중..." -ForegroundColor Yellow
git branch -M main
Write-Host "✅ 브랜치 설정 완료" -ForegroundColor Green
Write-Host ""

# 푸시
Write-Host "🚀 GitHub에 푸시 중..." -ForegroundColor Yellow
Write-Host "   저장소: $remoteUrl" -ForegroundColor Gray
Write-Host ""

$pushResponse = Read-Host "푸시를 진행하시겠습니까? (Y/N)"
if ($pushResponse -eq "Y" -or $pushResponse -eq "y") {
    git push -u origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ 푸시 완료!" -ForegroundColor Green
        Write-Host ""
        Write-Host "GitHub에서 확인하세요:" -ForegroundColor Cyan
        Write-Host "  https://github.com/joshuagermany/TIPSMAX-1.0" -ForegroundColor Yellow
    } else {
        Write-Host ""
        Write-Host "❌ 푸시 실패" -ForegroundColor Red
        Write-Host ""
        Write-Host "가능한 원인:" -ForegroundColor Yellow
        Write-Host "1. GitHub 인증이 필요할 수 있습니다" -ForegroundColor White
        Write-Host "2. 저장소가 존재하지 않을 수 있습니다" -ForegroundColor White
        Write-Host "3. 권한이 없을 수 있습니다" -ForegroundColor White
        Write-Host ""
        Write-Host "해결 방법:" -ForegroundColor Yellow
        Write-Host "- GitHub에서 저장소를 먼저 생성하세요" -ForegroundColor White
        Write-Host "- Personal Access Token을 사용하거나 GitHub Desktop을 사용하세요" -ForegroundColor White
    }
} else {
    Write-Host "푸시가 취소되었습니다." -ForegroundColor Yellow
}

Write-Host ""
