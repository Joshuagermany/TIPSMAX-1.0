# Python Installation Helper Script

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  TIPSMAX 1.0 - Python 설치 필요" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is actually installed
$pythonFound = $false
$pythonVersion = $null

# Check common Python locations
$commonPaths = @(
    "$env:LOCALAPPDATA\Programs\Python",
    "$env:ProgramFiles\Python*",
    "${env:ProgramFiles(x86)}\Python*"
)

foreach ($pathPattern in $commonPaths) {
    $pythonExes = Get-ChildItem -Path $pathPattern -ErrorAction SilentlyContinue -Recurse -Filter "python.exe" | Where-Object { $_.FullName -notlike "*WindowsApps*" }
    if ($pythonExes) {
        try {
            $versionOutput = & $pythonExes[0].FullName --version 2>&1 | Out-String
            if ($versionOutput -match "Python \d+\.\d+") {
                $pythonFound = $true
                $pythonVersion = $versionOutput.Trim()
                break
            }
        } catch {
            continue
        }
    }
}

if ($pythonFound) {
    Write-Host "[OK] Python is already installed!" -ForegroundColor Green
    Write-Host "  Version: $pythonVersion" -ForegroundColor Gray
    Write-Host ""
    Write-Host "You can now run TIPSMAX:" -ForegroundColor Cyan
    Write-Host "  cd backend" -ForegroundColor Yellow
    Write-Host "  .\start.bat" -ForegroundColor Yellow
    Write-Host ""
    exit 0
}

Write-Host "[WARNING] Python is not installed or not found in PATH" -ForegroundColor Red
Write-Host ""
Write-Host "Python installation is required to run TIPSMAX 1.0" -ForegroundColor Yellow
Write-Host ""

Write-Host "Installation options:" -ForegroundColor Cyan
Write-Host "  1. Download from python.org (Recommended)" -ForegroundColor White
Write-Host "     URL: https://www.python.org/downloads/" -ForegroundColor Gray
Write-Host ""
Write-Host "  2. Install from Microsoft Store" -ForegroundColor White
Write-Host "     Search for 'Python 3.12' in Microsoft Store" -ForegroundColor Gray
Write-Host ""
Write-Host "IMPORTANT during installation:" -ForegroundColor Red
Write-Host "  ✓ Check 'Add Python to PATH' option" -ForegroundColor Yellow
Write-Host ""

$choice = Read-Host "Open Python download page in browser? (Y/N)"

if ($choice -eq "Y" -or $choice -eq "y") {
    Write-Host ""
    Write-Host "Opening Python download page..." -ForegroundColor Cyan
    Start-Process "https://www.python.org/downloads/"
    Write-Host ""
    Write-Host "After installation:" -ForegroundColor Yellow
    Write-Host "  1. Close all PowerShell windows" -ForegroundColor White
    Write-Host "  2. Open a new PowerShell window" -ForegroundColor White
    Write-Host "  3. Run: python --version" -ForegroundColor White
    Write-Host "  4. Then run TIPSMAX setup again" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "Please install Python manually:" -ForegroundColor Yellow
    Write-Host "  https://www.python.org/downloads/" -ForegroundColor Cyan
}

Write-Host ""
Read-Host "Press Enter to exit"
