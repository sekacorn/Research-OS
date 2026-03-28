#!/usr/bin/env bash
set -euo pipefail

# One-command Unix startup for backend and frontend.
# This script installs dependencies, starts both services, and returns.
# Stop services with `bash stop.sh`.

API_HOST="127.0.0.1"
API_BASE_PORT="8000"
UI_BASE_PORT="8501"
API_PORT=""
UI_PORT=""
RUNTIME_DIR="storage/tmp/runtime"
API_LOG="${RUNTIME_DIR}/api.log"
UI_LOG="${RUNTIME_DIR}/ui.log"
API_PID_FILE="${RUNTIME_DIR}/api.pid"
UI_PID_FILE="${RUNTIME_DIR}/ui.pid"

PY_BIN=""
PY_ARGS=()

if command -v python3 >/dev/null 2>&1 && python3 -V >/dev/null 2>&1; then
  PY_BIN="python3"
elif command -v python >/dev/null 2>&1 && python -V >/dev/null 2>&1; then
  PY_BIN="python"
elif command -v py >/dev/null 2>&1 && py -3 -V >/dev/null 2>&1; then
  PY_BIN="py"
  PY_ARGS=(-3)
elif command -v py >/dev/null 2>&1 && py -V >/dev/null 2>&1; then
  PY_BIN="py"
else
  echo "Missing system dependency: python3"
  echo "Install Python 3.10+ and rerun."
  exit 1
fi

py_run() {
  "$PY_BIN" "${PY_ARGS[@]}" "$@"
}

get_http_status() {
  local url="$1"
  if command -v curl >/dev/null 2>&1; then
    local code
    code="$(curl -s -o /dev/null -w "%{http_code}" "$url" || true)"
    if [ -z "$code" ] || [ "$code" = "000" ]; then
      echo "DOWN"
    else
      echo "$code"
    fi
    return 0
  fi
  py_run -c "import urllib.request, urllib.error
u='${url}'
try:
    r = urllib.request.urlopen(u, timeout=2)
    print(getattr(r, 'status', 200))
except urllib.error.HTTPError as e:
    print(e.code)
except Exception:
    print('DOWN')" 2>/dev/null
}

running_port_from_process() {
  local pattern="$1"
  local default_port="$2"
  local pid
  pid="$(pgrep -f "$pattern" | head -n 1 || true)"
  if [ -z "$pid" ]; then
    echo ""
    return 0
  fi
  local cmd
  cmd="$(ps -p "$pid" -o args= 2>/dev/null || true)"
  if [ -n "$cmd" ] && echo "$cmd" | grep -E -- "--port[[:space:]]+[0-9]+" >/dev/null 2>&1; then
    echo "$cmd" | sed -nE 's/.*--port[[:space:]]+([0-9]+).*/\1/p'
    return 0
  fi
  echo "$default_port"
}

port_in_use() {
  local p="$1"
  if command -v ss >/dev/null 2>&1; then
    ss -ltn 2>/dev/null | grep -E "[:.]${p}[[:space:]]" >/dev/null 2>&1 && return 0
  fi
  if command -v netstat >/dev/null 2>&1; then
    netstat -an 2>/dev/null | grep -E "[:.]${p}[[:space:]].*LISTEN" >/dev/null 2>&1 && return 0
  fi
  return 1
}

find_free_port() {
  local start="$1"
  local max_offset="${2:-30}"
  local p
  for p in $(seq "$start" $((start + max_offset))); do
    if ! port_in_use "$p"; then
      echo "$p"
      return 0
    fi
  done
  echo "NONE"
  return 1
}

mkdir -p "$RUNTIME_DIR"
: > "$API_LOG"
: > "$UI_LOG"

# Preflight check for already-running services or port conflicts.
running_api_port="$(running_port_from_process "uvicorn api_fastapi.main:app" "$API_BASE_PORT")"
running_ui_port="$(running_port_from_process "streamlit run app_streamlit/app.py" "$UI_BASE_PORT")"
if [ -n "$running_api_port" ] && [ -n "$running_ui_port" ]; then
  api_status="$(get_http_status "http://${API_HOST}:${running_api_port}/docs")"
  ui_status="$(get_http_status "http://127.0.0.1:${running_ui_port}")"
  if [ "$api_status" = "200" ] && [ "$ui_status" = "200" ]; then
    echo "Application is running."
    echo
    echo "- API: http://${API_HOST}:${running_api_port}/docs (${api_status})"
    echo "- UI: http://127.0.0.1:${running_ui_port} (${ui_status})"
  echo
  echo "When youre done, stop it with:"
  echo
  echo "- stop.sh"
  echo
  echo "Open a web browser, then copy and paste this UI IP and port first:"
  echo "- UI (copy/paste): http://127.0.0.1:${running_ui_port}"
  echo "- Backend : http://${API_HOST}:${running_api_port}/docs"
  exit 0
fi
fi

api_status="$(get_http_status "http://${API_HOST}:${API_BASE_PORT}/docs")"
ui_status="$(get_http_status "http://127.0.0.1:${UI_BASE_PORT}")"
if [ "$api_status" = "200" ] && [ "$ui_status" = "200" ]; then
  echo "Application is running."
  echo
  echo "- API: http://${API_HOST}:${API_BASE_PORT}/docs (${api_status})"
  echo "- UI: http://127.0.0.1:${UI_BASE_PORT} (${ui_status})"
  echo
  echo "When youre done, stop it with:"
  echo
  echo "- stop.sh"
  echo
  echo "Open a web browser, then copy and paste this UI IP and port first:"
  echo "- UI (copy/paste): http://127.0.0.1:${UI_BASE_PORT}"
  echo "- Backend : http://${API_HOST}:${API_BASE_PORT}/docs"
  exit 0
fi

API_PORT="$(find_free_port "$API_BASE_PORT" 30 || true)"
UI_PORT="$(find_free_port "$UI_BASE_PORT" 30 || true)"
if [ "$API_PORT" = "NONE" ] || [ "$UI_PORT" = "NONE" ] || [ -z "$API_PORT" ] || [ -z "$UI_PORT" ]; then
  echo "Endpoints are not available for startup."
  echo "Could not find open ports near ${API_BASE_PORT} and ${UI_BASE_PORT}."
  echo "Stop other processes or run stop.sh, then try again."
  exit 1
fi

echo "Stopping any existing Research OS app processes..."
bash stop.sh >/dev/null 2>&1 || true

echo "Installing/refreshing dependencies..."
py_run -m pip install --upgrade pip
py_run -m pip install -e .

echo "Starting FastAPI backend on ${API_HOST}:${API_PORT}..."
nohup bash -lc "$(printf '%q ' "$PY_BIN" "${PY_ARGS[@]}") -m uvicorn api_fastapi.main:app --host ${API_HOST} --port ${API_PORT}" >>"$API_LOG" 2>&1 &
echo $! > "$API_PID_FILE"

# Wait for backend readiness before frontend launch.
api_ok=0
for _ in $(seq 1 40); do
  if py_run -c "import sys,urllib.request; r=urllib.request.urlopen('http://${API_HOST}:${API_PORT}/docs', timeout=1); sys.exit(0 if r.status==200 else 1)" >/dev/null 2>&1; then
    api_ok=1
    break
  fi
  sleep 0.5
done
if [ "$api_ok" -ne 1 ]; then
  echo "FastAPI failed readiness check. See ${API_LOG}."
  bash stop.sh >/dev/null 2>&1 || true
  exit 1
fi

echo "Starting Streamlit frontend on port ${UI_PORT}..."
nohup bash -lc "STREAMLIT_BROWSER_GATHER_USAGE_STATS=false STREAMLIT_SERVER_HEADLESS=true $(printf '%q ' "$PY_BIN" "${PY_ARGS[@]}") -m streamlit run app_streamlit/app.py --server.port ${UI_PORT} --server.headless true" >>"$UI_LOG" 2>&1 &
echo $! > "$UI_PID_FILE"

# Verify the frontend endpoint before returning success.
ui_ok=0
for _ in $(seq 1 40); do
  if py_run -c "import sys,urllib.request; r=urllib.request.urlopen('http://127.0.0.1:${UI_PORT}', timeout=1); sys.exit(0 if 200 <= r.status < 500 else 1)" >/dev/null 2>&1; then
    ui_ok=1
    break
  fi
  sleep 0.5
done
if [ "$ui_ok" -ne 1 ]; then
  echo "Streamlit failed readiness check. See ${UI_LOG}."
  bash stop.sh >/dev/null 2>&1 || true
  exit 1
fi

api_status="$(get_http_status "http://${API_HOST}:${API_PORT}/docs")"
ui_status="$(get_http_status "http://127.0.0.1:${UI_PORT}")"
if [ "$api_status" != "200" ] || [ "$ui_status" != "200" ]; then
  echo "Endpoints are not available after startup."
  echo "API status: ${api_status} ; UI status: ${ui_status}"
  echo "Other processes may be using ports or startup failed. Check logs:"
  echo "- ${API_LOG}"
  echo "- ${UI_LOG}"
  bash stop.sh >/dev/null 2>&1 || true
  exit 1
fi

echo "Application is running."
echo
echo "- API: http://${API_HOST}:${API_PORT}/docs (${api_status})"
echo "- UI: http://127.0.0.1:${UI_PORT} (${ui_status})"
echo
echo "When youre done, stop it with:"
echo
echo "- stop.sh"
echo
echo "Open a web browser, then copy and paste this UI IP and port first:"
echo "- UI (copy/paste): http://127.0.0.1:${UI_PORT}"
echo "- Backend : http://${API_HOST}:${API_PORT}/docs"
