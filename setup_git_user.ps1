# Git 사용자 정보 설정 스크립트

Write-Host "=== Git 사용자 정보 설정 ===" -ForegroundColor Cyan
Write-Host ""

$gitPath = "C:\Program Files\Git\bin\git.exe"

if (-not (Test-Path $gitPath)) {
    Write-Host "❌ Git을 찾을 수 없습니다." -ForegroundColor Red
    exit 1
}

Write-Host "GitHub에 푸시하려면 사용자 정보가 필요합니다." -ForegroundColor Yellow
Write-Host ""

# GitHub 사용자명 입력
$githubUsername = Read-Host "GitHub 사용자명을 입력하세요 (예: joshuagermany)"
if ([string]::IsNullOrWhiteSpace($githubUsername)) {
    $githubUsername = "joshuagermany"
    Write-Host "기본값 사용: $githubUsername" -ForegroundColor Gray
}

# 이메일 입력
$email = Read-Host "이메일 주소를 입력하세요 (GitHub 이메일 또는 noreply 이메일)"
if ([string]::IsNullOrWhiteSpace($email)) {
    $email = "$githubUsername@users.noreply.github.com"
    Write-Host "기본값 사용: $email" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Git 사용자 정보 설정 중..." -ForegroundColor Yellow

# 전역 설정
& $gitPath config --global user.name $githubUsername
& $gitPath config --global user.email $email

Write-Host ""
Write-Host "✅ Git 사용자 정보 설정 완료!" -ForegroundColor Green
Write-Host "   이름: $githubUsername" -ForegroundColor Gray
Write-Host "   이메일: $email" -ForegroundColor Gray
Write-Host ""

Write-Host "이제 다음 명령어로 커밋하고 푸시할 수 있습니다:" -ForegroundColor Cyan
Write-Host ""
Write-Host '  cd "C:\Users\venturus01\Desktop\TIPSMAX 1.0"' -ForegroundColor Yellow
Write-Host '  & "C:\Program Files\Git\bin\git.exe" add .' -ForegroundColor Yellow
Write-Host '  & "C:\Program Files\Git\bin\git.exe" commit -m "Initial commit: TIPSMAX 1.0"' -ForegroundColor Yellow
Write-Host '  & "C:\Program Files\Git\bin\git.exe" push -u origin main' -ForegroundColor Yellow
Write-Host ""
