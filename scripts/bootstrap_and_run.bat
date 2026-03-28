@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM Windows bootstrap for setup, test, and full app startup.
REM This script reports only missing system dependencies.
REM Python packages are installed from pyproject.toml / requirements-dev.txt.

set "MISSING="
set "PY_CMD="
set "API_HOST=127.0.0.1"
set "API_PORT=8000"
set "UI_PORT=8501"

REM Prefer the Python launcher on Windows; fall back to python.exe.
where py >nul 2>nul
if %ERRORLEVEL%==0 (
    set "PY_CMD=py -3"
) else (
    where python >nul 2>nul
    if %ERRORLEVEL%==0 (
        set "PY_CMD=python"
    ) else (
        set "MISSING=!MISSING! python"
    )
)

if not "%MISSING%"=="" (
    echo Missing system dependencies:%MISSING%
    echo Install the missing system tools, then rerun this script.
    exit /b 1
)

REM Upgrade pip first so editable installs behave consistently.
%PY_CMD% -m pip install --upgrade pip
if errorlevel 1 exit /b 1

REM Runtime dependencies come from pyproject.toml.
%PY_CMD% -m pip install -e .
if errorlevel 1 exit /b 1

REM Dev dependencies are optional but needed for pytest in many environments.
if exist requirements-dev.txt (
    %PY_CMD% -m pip install -r requirements-dev.txt
    if errorlevel 1 exit /b 1
)

REM Run tests before startup so failures are caught early.
%PY_CMD% -m pytest -q
if errorlevel 1 exit /b 1

echo Tests passed. Starting FastAPI on %API_HOST%:%API_PORT%...
start "ResearchOS_API" /B cmd /c "%PY_CMD% -m uvicorn api_fastapi.main:app --host %API_HOST% --port %API_PORT%"
if errorlevel 1 (
    echo Failed to launch FastAPI process.
    exit /b 1
)

REM Poll the API docs endpoint so the frontend starts only after the backend is ready.
powershell -NoProfile -Command "$ok=$false; for($i=0;$i -lt 20;$i++){ try { $r=Invoke-WebRequest -Uri 'http://127.0.0.1:8000/docs' -UseBasicParsing -TimeoutSec 1; if($r.StatusCode -eq 200){$ok=$true; break} } catch {}; Start-Sleep -Milliseconds 500 }; if(-not $ok){ exit 1 }"
if errorlevel 1 (
    echo FastAPI did not become ready on http://%API_HOST%:%API_PORT%/docs.
    call :cleanup_api
    exit /b 1
)

echo FastAPI is ready. Starting Streamlit on port %UI_PORT%...
%PY_CMD% -m streamlit run app_streamlit/app.py --server.port %UI_PORT%
set "STREAMLIT_EXIT=%ERRORLEVEL%"

REM When the frontend exits, tear down the backend to avoid orphan processes.
call :cleanup_api
exit /b %STREAMLIT_EXIT%

:cleanup_api
powershell -NoProfile -Command "$procs=Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*.exe' -and $_.CommandLine -match 'uvicorn api_fastapi.main:app --host 127.0.0.1 --port 8000' }; foreach($p in $procs){ try { Stop-Process -Id $p.ProcessId -Force -ErrorAction Stop } catch {} }"
exit /b 0
