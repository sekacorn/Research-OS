@echo off
setlocal EnableExtensions

REM Stop both backend and frontend processes started by run.bat.
REM Command-line matching is explicit to avoid killing unrelated Python jobs.

powershell -NoProfile -Command ^
  "$self = $PID; $targets = Get-CimInstance Win32_Process | Where-Object { $_.ProcessId -ne $self -and (" ^
  "$_.CommandLine -match 'uvicorn api_fastapi.main:app' -or " ^
  "$_.CommandLine -match 'streamlit run app_streamlit/app.py')" ^
  "}; foreach($p in $targets){ try { Stop-Process -Id $p.ProcessId -Force -ErrorAction Stop } catch {} }"

echo Research OS processes stopped (if running).
exit /b 0
