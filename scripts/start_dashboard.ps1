$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)
$python = Join-Path (Get-Location) ".venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    Write-Host "Virtual environment not found. Run: py -3.12 -m venv .venv" -ForegroundColor Yellow
    exit 1
}
& $python -m streamlit run app/dashboard.py