# build.ps1 — build a one-file Windows exe using PyInstaller
# Usage: Open PowerShell in this folder and run: .\build.ps1

param(
    [string]$Name = "screener",
    [switch]$NoWindow
)

Write-Host "Checking Python..."
python --version 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Python not found in PATH. Please install Python 3.8+ and retry." -ForegroundColor Red
    exit 1
}

Write-Host "Installing/ensuring dependencies..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install --upgrade pyinstaller

$pyArgs = @("--onefile","--name",$Name)
if (-not $NoWindow) { $pyArgs += "--windowed" }
$pyArgs += "screener.py"

Write-Host "Running PyInstaller..."
& python -m PyInstaller @pyArgs

if ($LASTEXITCODE -eq 0) {
    Write-Host "Build complete. Output: dist\$Name.exe" -ForegroundColor Green
} else {
    Write-Host "PyInstaller failed. Try running without --windowed to see console errors." -ForegroundColor Yellow
}
