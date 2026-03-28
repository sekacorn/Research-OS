@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM One-command Windows startup for backend and frontend.
REM This script installs project dependencies, then launches both services.
REM Stop services with `stop.bat`.

set "API_HOST=127.0.0.1"
set "API_BASE_PORT=8000"
set "UI_BASE_PORT=8501"
set "API_PORT="
set "UI_PORT="
set "RUNTIME_DIR=storage\tmp\runtime"
set "API_LOG=%RUNTIME_DIR%\api.log"
set "UI_LOG=%RUNTIME_DIR%\ui.log"
set "PY_CMD="

where py >nul 2>nul
if %ERRORLEVEL%==0 (
    set "PY_CMD=py -3"
) else (
    where python >nul 2>nul
    if %ERRORLEVEL%==0 (
        set "PY_CMD=python"
    ) else (
        echo Missing system dependency: python
        echo Install Python 3.10+ and rerun.
        exit /b 1
    )
)

if not exist "%RUNTIME_DIR%" mkdir "%RUNTIME_DIR%"

REM Preflight check for already-running services or port collisions.
powershell -NoProfile -Command "$apiProc = Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'uvicorn api_fastapi.main:app' } | Select-Object -First 1; $uiProc = Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'streamlit run app_streamlit/app.py' } | Select-Object -First 1; function PortFrom($cmd,[int]$default){ if($cmd -match '--port\s+(\d+)'){ return [int]$matches[1] }; return $default }; if($apiProc -and $uiProc){ $ap = PortFrom $apiProc.CommandLine %API_BASE_PORT%; $up = PortFrom $uiProc.CommandLine %UI_BASE_PORT%; $api='DOWN'; $ui='DOWN'; try { $r=Invoke-WebRequest -Uri ('http://127.0.0.1:' + $ap + '/docs') -UseBasicParsing -TimeoutSec 2; $api=[string]$r.StatusCode } catch {}; try { $r=Invoke-WebRequest -Uri ('http://127.0.0.1:' + $up) -UseBasicParsing -TimeoutSec 2; $ui=[string]$r.StatusCode } catch {}; if($api -eq '200' -and $ui -eq '200'){ Write-Output 'ALREADY_UP'; Write-Output ('API_PORT=' + $ap); Write-Output ('UI_PORT=' + $up); exit 0 } }; $api='DOWN'; $ui='DOWN'; try { $r=Invoke-WebRequest -Uri 'http://127.0.0.1:%API_BASE_PORT%/docs' -UseBasicParsing -TimeoutSec 2; $api=[string]$r.StatusCode } catch {}; try { $r=Invoke-WebRequest -Uri 'http://127.0.0.1:%UI_BASE_PORT%' -UseBasicParsing -TimeoutSec 2; $ui=[string]$r.StatusCode } catch {}; if($api -eq '200' -and $ui -eq '200'){ Write-Output 'ALREADY_UP'; Write-Output ('API_PORT=' + %API_BASE_PORT%); Write-Output ('UI_PORT=' + %UI_BASE_PORT%); exit 0 }; function InUse([int]$p){ return [bool](netstat -ano | Select-String (':' + $p + '\s+.*LISTENING')) }; function Pick([int]$start,[int]$max){ for($p=$start; $p -le ($start+$max); $p++){ if(-not (InUse $p)){ return $p } }; return $null }; $ap=Pick %API_BASE_PORT% 30; $up=Pick %UI_BASE_PORT% 30; if(($null -eq $ap) -or ($null -eq $up)){ Write-Output 'PORT_CONFLICT'; exit 2 }; Write-Output ('API_PORT=' + $ap); Write-Output ('UI_PORT=' + $up); exit 0" > "%RUNTIME_DIR%\preflight.txt"
set /p PREFLIGHT=<"%RUNTIME_DIR%\preflight.txt"
for /f "tokens=1,2 delims==" %%a in (%RUNTIME_DIR%\preflight.txt) do (
  if /I "%%a"=="API_PORT" set "API_PORT=%%b"
  if /I "%%a"=="UI_PORT" set "UI_PORT=%%b"
)
if /I "%PREFLIGHT%"=="ALREADY_UP" (
  if "%API_PORT%"=="" set "API_PORT=%API_BASE_PORT%"
  if "%UI_PORT%"=="" set "UI_PORT=%UI_BASE_PORT%"
  echo Application is running.
  echo.
  echo - API: http://%API_HOST%:%API_PORT%/docs (200)
  echo - UI: http://127.0.0.1:%UI_PORT% (200)
  echo.
  echo When youre done, stop it with:
  echo.
  echo - stop.bat
  echo.
  echo Open a web browser, then copy and paste this UI IP and port first:
  echo - UI (copy/paste): http://127.0.0.1:%UI_PORT%
  echo - Backend : http://%API_HOST%:%API_PORT%/docs
  exit /b 0
)
if /I "%PREFLIGHT%"=="PORT_CONFLICT" (
  echo Endpoints are not available for startup.
  echo Could not find open ports near %API_BASE_PORT% and %UI_BASE_PORT%.
  echo Stop other processes or run stop.bat, then try again.
  exit /b 1
)
if "%API_PORT%"=="" (
  echo Failed to select API port.
  exit /b 1
)
if "%UI_PORT%"=="" (
  echo Failed to select UI port.
  exit /b 1
)

REM Clear previous logs so startup diagnostics stay current.
if exist "%API_LOG%" del /f /q "%API_LOG%" >nul 2>nul
if exist "%UI_LOG%" del /f /q "%UI_LOG%" >nul 2>nul

echo Stopping any existing Research OS app processes...
call stop.bat >nul 2>nul

echo Installing/refreshing dependencies...
%PY_CMD% -m pip install --upgrade pip
if errorlevel 1 exit /b 1
%PY_CMD% -m pip install -e .
if errorlevel 1 exit /b 1

echo Starting FastAPI backend on %API_HOST%:%API_PORT%...
start "ResearchOS_API" /MIN cmd /c "%PY_CMD% -m uvicorn api_fastapi.main:app --host %API_HOST% --port %API_PORT% > ""%API_LOG%"" 2>&1"

REM Wait until the backend responds before starting the frontend.
powershell -NoProfile -Command "$ok=$false; for($i=0;$i -lt 120;$i++){ try { $r=Invoke-WebRequest -Uri 'http://127.0.0.1:%API_PORT%/docs' -UseBasicParsing -TimeoutSec 1; if($r.StatusCode -eq 200){$ok=$true; break} } catch {}; Start-Sleep -Milliseconds 500 }; if(-not $ok){ exit 1 }"
if errorlevel 1 (
    echo FastAPI failed readiness check. See %API_LOG%.
    call stop.bat >nul 2>nul
    exit /b 1
)

echo Starting Streamlit frontend on port %UI_PORT%...
start "ResearchOS_UI" /MIN cmd /c "set STREAMLIT_BROWSER_GATHER_USAGE_STATS=false&& set STREAMLIT_SERVER_HEADLESS=true&& %PY_CMD% -m streamlit run app_streamlit/app.py --server.port %UI_PORT% --server.headless true > ""%UI_LOG%"" 2>&1"

REM Verify the frontend endpoint before returning control.
powershell -NoProfile -Command "$ok=$false; for($i=0;$i -lt 120;$i++){ try { $r=Invoke-WebRequest -Uri 'http://127.0.0.1:%UI_PORT%' -UseBasicParsing -TimeoutSec 1; if($r.StatusCode -ge 200 -and $r.StatusCode -lt 500){$ok=$true; break} } catch {}; Start-Sleep -Milliseconds 500 }; if(-not $ok){ exit 1 }"
if errorlevel 1 (
  echo Streamlit failed readiness check. See %UI_LOG%.
  call stop.bat >nul 2>nul
  exit /b 1
)

powershell -NoProfile -Command "$api='DOWN'; $ui='DOWN'; try { $r=Invoke-WebRequest -Uri 'http://127.0.0.1:%API_PORT%/docs' -UseBasicParsing -TimeoutSec 2; $api=[string]$r.StatusCode } catch {}; try { $r=Invoke-WebRequest -Uri 'http://127.0.0.1:%UI_PORT%' -UseBasicParsing -TimeoutSec 2; $ui=[string]$r.StatusCode } catch {}; Write-Output ('API=' + $api); Write-Output ('UI=' + $ui)" > "%RUNTIME_DIR%\health.txt"
for /f "tokens=1,2 delims==" %%a in (%RUNTIME_DIR%\health.txt) do (
  if /I "%%a"=="API" set "API_STATUS=%%b"
  if /I "%%a"=="UI" set "UI_STATUS=%%b"
)
if not "%API_STATUS%"=="200" (
  echo Endpoints are not available after startup.
  echo API status: %API_STATUS% ; UI status: %UI_STATUS%
  echo Other processes may be using ports or startup failed. Check logs:
  echo - %API_LOG%
  echo - %UI_LOG%
  call stop.bat >nul 2>nul
  exit /b 1
)
if not "%UI_STATUS%"=="200" (
  echo Endpoints are not available after startup.
  echo API status: %API_STATUS% ; UI status: %UI_STATUS%
  echo Other processes may be using ports or startup failed. Check logs:
  echo - %API_LOG%
  echo - %UI_LOG%
  call stop.bat >nul 2>nul
  exit /b 1
)

echo Application is running.
echo.
echo - API: http://%API_HOST%:%API_PORT%/docs (%API_STATUS%)
echo - UI: http://127.0.0.1:%UI_PORT% (%UI_STATUS%)
echo.
echo When youre done, stop it with:
echo.
echo - stop.bat
echo.
echo Open a web browser, then copy and paste this UI IP and port first:
echo - UI (copy/paste): http://127.0.0.1:%UI_PORT%
echo - Backend : http://%API_HOST%:%API_PORT%/docs
exit /b 0
