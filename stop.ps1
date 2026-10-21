# Stops the Agent Pilot API (and any Vite dev server on 5173).
$ErrorActionPreference = "SilentlyContinue"

$targets = @()
foreach ($port in @(8010, 5173)) {
    $conns = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
    foreach ($conn in $conns) {
        $targets += $conn.OwningProcess
    }
}

$targets = $targets | Sort-Object -Unique
if ($targets.Count -eq 0) {
    Write-Host "Nothing is listening on 8010 or 5173."
    exit 0
}

foreach ($pid_ in $targets) {
    $proc = Get-Process -Id $pid_ -ErrorAction SilentlyContinue
    if ($proc) {
        Write-Host "Stopping $($proc.ProcessName) (PID $pid_)..."
        Stop-Process -Id $pid_ -Force
    }
}

Write-Host "Stopped."
