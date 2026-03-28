#!/usr/bin/env bash
set -euo pipefail

# Stop both backend and frontend processes started by run.sh.
# PID files are used first; command matching is fallback cleanup.

RUNTIME_DIR="storage/tmp/runtime"
API_PID_FILE="${RUNTIME_DIR}/api.pid"
UI_PID_FILE="${RUNTIME_DIR}/ui.pid"

stop_by_pid_file() {
  local pid_file="$1"
  if [ -f "$pid_file" ]; then
    pid="$(cat "$pid_file" 2>/dev/null || true)"
    if [ -n "${pid:-}" ] && kill -0 "$pid" >/dev/null 2>&1; then
      kill "$pid" >/dev/null 2>&1 || true
      sleep 0.2
      kill -9 "$pid" >/dev/null 2>&1 || true
    fi
    rm -f "$pid_file"
  fi
}

stop_by_pid_file "$API_PID_FILE"
stop_by_pid_file "$UI_PID_FILE"

# Fallback for orphaned processes without PID files.
pkill -f "uvicorn api_fastapi.main:app" >/dev/null 2>&1 || true
pkill -f "streamlit run app_streamlit/app.py" >/dev/null 2>&1 || true

# On Git Bash/MSYS, pkill may not control native Windows Python processes.
if command -v powershell.exe >/dev/null 2>&1; then
  powershell.exe -NoProfile -Command \
    '$targets = Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match "uvicorn api_fastapi.main:app" -or $_.CommandLine -match "streamlit run app_streamlit/app.py" }; foreach($p in $targets){ try { Stop-Process -Id $p.ProcessId -Force -ErrorAction Stop } catch {} }' \
    >/dev/null 2>&1 || true
fi

echo "Research OS processes stopped (if running)."
