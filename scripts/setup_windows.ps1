$ErrorActionPreference = "Stop"
$ProjectDir = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectDir

Write-Host "== Agendador Web: instalação para Windows ==" -ForegroundColor Cyan
try {
    $python = Get-Command py -ErrorAction Stop
    & py -3 --version
    if ($LASTEXITCODE -ne 0) { throw "Python 3 não foi encontrado pelo launcher 'py'." }
    & py -3 -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw "Não foi possível criar o ambiente virtual." }
    & .\.venv\Scripts\python.exe -m pip install --upgrade pip
    if ($LASTEXITCODE -ne 0) { throw "Falha ao atualizar o pip." }
    & .\.venv\Scripts\python.exe -m pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) { throw "Falha ao instalar dependências. Verifique sua internet." }
    New-Item -ItemType Directory -Force -Path .\instance\logs | Out-Null
    Write-Host "`nInstalação concluída!" -ForegroundColor Green
    Write-Host "Execute .\iniciar_windows.bat para iniciar o sistema."
} catch {
    Write-Host "Erro: $_" -ForegroundColor Red
    Write-Host "Instale Python 3.10 ou superior em https://www.python.org/downloads/windows/"
    Write-Host "Durante a instalação, marque 'Add python.exe to PATH'."
    exit 1
}
