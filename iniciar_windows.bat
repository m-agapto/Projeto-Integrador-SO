@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Ambiente Python nao encontrado.
  echo Execute primeiro: powershell -ExecutionPolicy Bypass -File scripts\setup_windows.ps1
  pause
  exit /b 1
)
echo Iniciando Agendador Web...
echo Abra http://127.0.0.1:5000 no navegador.
".venv\Scripts\python.exe" -m flask --app run.py run --debug
pause
