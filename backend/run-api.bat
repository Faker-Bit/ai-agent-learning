@echo off
rem Starts the Agent Pilot API from the backend folder.
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo [x] Virtual environment missing. Run start.bat from the project root first.
  pause
  exit /b 1
)
if "%AMT_PORT%"=="" set AMT_PORT=8010
".venv\Scripts\python.exe" -m uvicorn main:app --host 127.0.0.1 --port %AMT_PORT% --reload
pause
