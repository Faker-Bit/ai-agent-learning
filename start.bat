@echo off
setlocal

rem ============================================================
rem  Agent Pilot - one-shot start script for Windows
rem  Creates the venv, installs deps, exports the content,
rem  builds the frontend and launches the API.
rem ============================================================

cd /d "%~dp0"
set ROOT=%CD%
set BACKEND=%ROOT%\backend
set FRONTEND=%ROOT%\frontend
set VENV=%BACKEND%\.venv
set PORT=8010
set AMT_PORT=8010

echo.
echo   Agent Pilot
echo   --------------
echo   Project: %ROOT%
echo.

rem ---- python ----
where python >nul 2>nul
if errorlevel 1 goto nopython
where node >nul 2>nul
if errorlevel 1 goto nonode

rem ---- venv ----
if not exist "%VENV%\Scripts\python.exe" goto makevenv
echo   [1/5] Virtual environment already exists.
goto deps

:makevenv
echo   [1/5] Creating virtual environment...
python -m venv "%VENV%"
if errorlevel 1 goto failvenv

:deps
echo   [2/5] Installing backend dependencies...
"%VENV%\Scripts\python.exe" -m pip install --upgrade pip --quiet
"%VENV%\Scripts\python.exe" -m pip install -r "%BACKEND%\requirements.txt" --quiet
if errorlevel 1 goto faildeps

rem ---- env file ----
if exist "%BACKEND%\.env" goto noenv
copy "%BACKEND%\.env.example" "%BACKEND%\.env" >nul
echo   [i] Created backend\.env from the example.
:noenv

rem ---- free the port ----
rem A server left over from an older build keeps the port and serves stale
rem content, which shows up as a failure to load the site content.
for /f "tokens=5" %%p in ('netstat -ano ^| findstr LISTENING ^| findstr ":%PORT% "') do taskkill /PID %%p /F >nul 2>nul

rem ---- frontend deps ----
if exist "%FRONTEND%\node_modules" goto nodeok
echo   [3/5] Installing frontend dependencies...
pushd "%FRONTEND%"
call npm.cmd install --no-audit --no-fund
popd
goto export

:nodeok
:export
echo   [4/5] Exporting the site content...
pushd "%BACKEND%"
"%VENV%\Scripts\python.exe" tools\export_content.py
if errorlevel 1 goto failexport
popd

echo   [5/5] Building the frontend...
pushd "%FRONTEND%"
call npm.cmd run build
if errorlevel 1 goto failbuild
popd

echo.
echo   Starting the API on http://127.0.0.1:%PORT%
start "Agent Pilot API" /D "%BACKEND%" "%VENV%\Scripts\python.exe" -m uvicorn main:app --host 127.0.0.1 --port %PORT%

timeout /t 5 /nobreak >nul
start "" "http://127.0.0.1:%PORT%"

echo.
echo   Done. The site is at http://127.0.0.1:%PORT%
echo   Stop the API window to shut it down.
echo.
pause
endlocal
exit /b 0

:nopython
echo   [x] Python not found on PATH. Install Python 3.12+ and try again.
pause
exit /b 1

:nonode
echo   [x] Node.js not found on PATH. Install Node.js 20+ and try again.
pause
exit /b 1

:failvenv
echo   [x] Failed to create the virtual environment.
pause
exit /b 1

:faildeps
echo   [x] Backend dependency install failed.
pause
exit /b 1

:failexport
popd
echo   [x] Content export failed.
pause
exit /b 1

:failbuild
popd
echo   [x] Frontend build failed.
pause
exit /b 1