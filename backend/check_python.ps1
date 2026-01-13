# Python Installation Check Script

Write-Host "=== Python Installation Check ===" -ForegroundColor Cyan
Write-Host ""

$pythonFound = $false
$pythonPath = $null
$pythonVersion = $null

# Try to find Python
$commands = @("python", "python3", "py")

foreach ($cmd in $commands) {
    try {
        $found = Get-Command $cmd -ErrorAction SilentlyContinue
        if ($found) {
            # Windows Store stub 체크 (WindowsApps 경로는 스텁일 가능성 높음)
            if ($found.Path -like "*WindowsApps*") {
                continue
            }
            
            $pythonPath = $found.Path
            $testOutput = & $cmd --version 2>&1 | Out-String
            
            # 버전이 제대로 출력되는지 확인 (숫자가 포함되어야 함)
            if ($testOutput -and $testOutput -match "Python \d+\.\d+" -and $testOutput.Length -gt 10) {
                $pythonFound = $true
                $pythonVersion = $testOutput.Trim()
                break
            }
        }
    } catch {
        continue
    }
}

# Search file system
if (-not $pythonFound) {
    $commonPaths = @(
        "$env:LOCALAPPDATA\Programs\Python",
        "C:\Program Files\Python*"
    )
    
    foreach ($pathPattern in $commonPaths) {
        try {
            $pythonExes = Get-ChildItem -Path $pathPattern -ErrorAction SilentlyContinue -Recurse -Filter "python.exe" | Select-Object -First 1
            if ($pythonExes) {
                $testOutput = & $pythonExes.FullName --version 2>&1
                if ($testOutput -and $testOutput.ToString() -notmatch "store") {
                    $pythonFound = $true
                    $pythonPath = $pythonExes.FullName
                    $pythonVersion = $testOutput.ToString()
                    break
                }
            }
        } catch {
            continue
        }
    }
}

# Display results
if ($pythonFound) {
    Write-Host "[OK] Python found!" -ForegroundColor Green
    Write-Host "  Path: $pythonPath" -ForegroundColor Gray
    Write-Host "  Version: $pythonVersion" -ForegroundColor Gray
    Write-Host ""
    Write-Host "You can now run:" -ForegroundColor Cyan
    Write-Host "  python -m venv venv" -ForegroundColor Yellow
    Write-Host "  or" -ForegroundColor Gray
    Write-Host "  .\start.bat" -ForegroundColor Yellow
} else {
    Write-Host "[ERROR] Python is not installed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python:" -ForegroundColor Yellow
    Write-Host "1. Visit: https://www.python.org/downloads/" -ForegroundColor White
    Write-Host "2. Download Python 3.11 or higher" -ForegroundColor White
    Write-Host "3. IMPORTANT: Check 'Add Python to PATH' during installation!" -ForegroundColor Red
    Write-Host "4. Restart PowerShell after installation" -ForegroundColor White
    Write-Host ""
    Write-Host "See INSTALL_PYTHON.md for detailed instructions." -ForegroundColor Cyan
    
    $response = Read-Host "Open Python download page? (Y/N)"
    if ($response -eq "Y" -or $response -eq "y") {
        Start-Process "https://www.python.org/downloads/"
    }
}

Write-Host ""
