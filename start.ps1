# ============================================================
#  Agent Pilot - start script (PowerShell)
#  Creates the venv, installs deps, exports the content,
#  builds the frontend and launches the API. The built SPA
#  is served by the API itself, so there is only one URL.
# ============================================================

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Backend = Join-Path $Root "backend"
$Frontend = Join-Path $Root "frontend"
$Venv = Join-Path $Backend ".venv"
$Port = 8010

Write-Host ""
Write-Host "  Agent Pilot" -ForegroundColor Cyan
Write-Host "  Project: $Root"
Write-Host ""

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "[x] Python not found on PATH. Install Python 3.12+." -ForegroundColor Red
    exit 1
}
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "[x] Node.js not found on PATH. Install Node.js 20+." -ForegroundColor Red
    exit 1
}

if (-not (Test-Path "$Venv\Scripts\python.exe")) {
    Write-Host "[1/5] Creating virtual environment..." -ForegroundColor DarkGray
    python -m venv $Venv
} else {
    Write-Host "[1/5] Virtual environment already exists." -ForegroundColor DarkGray
}

Write-Host "[2/5] Installing backend dependencies..." -ForegroundColor DarkGray
& "$Venv\Scripts\python.exe" -m pip install --upgrade pip --quiet
& "$Venv\Scripts\python.exe" -m pip install -r "$Backend\requirements.txt" --quiet

if (-not (Test-Path "$Backend\.env")) {
    Copy-Item "$Backend\.env.example" "$Backend\.env"
    Write-Host "[i] Created backend\.env." -ForegroundColor Yellow
}

# A server left over from an older build keeps the port and serves stale
# content, which shows up as "could not load the site content".
$stale = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
foreach ($conn in $stale) {
    Write-Host "[i] Stopping the process already listening on port $Port (PID $($conn.OwningProcess))..." -ForegroundColor Yellow
    Stop-Process -Id $conn.OwningProcess -Force -ErrorAction SilentlyContinue
}

if (-not (Test-Path "$Frontend\node_modules")) {
    Write-Host "[3/5] Installing frontend dependencies..." -ForegroundColor DarkGray
    Push-Location $Frontend
    npm.cmd install --no-audit --no-fund
    Pop-Location
}

Write-Host "[4/5] Exporting the site content..." -ForegroundColor DarkGray
Push-Location $Backend
& "$Venv\Scripts\python.exe" tools\export_content.py
Pop-Location

Write-Host "[5/5] Building the frontend..." -ForegroundColor DarkGray
Push-Location $Frontend
npm.cmd run build
Pop-Location

Write-Host ""
Write-Host "  Site: http://127.0.0.1:$Port" -ForegroundColor Green
Write-Host "  Docs: http://127.0.0.1:$Port/docs" -ForegroundColor DarkGray
Write-Host ""
Write-Host "  Press Ctrl+C to stop." -ForegroundColor DarkGray

$env:AMT_PORT = $Port
Push-Location $Backend
& "$Venv\Scripts\python.exe" -m uvicorn main:app --host 127.0.0.1 --port $Port --reload
Pop-Location
