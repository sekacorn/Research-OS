#!/usr/bin/env bash
set -euo pipefail

# Unix bootstrap for setup, test, and full app startup.
# Report only missing system dependencies here.
# Python packages are installed from pyproject.toml / requirements-dev.txt.

missing=()
API_HOST="127.0.0.1"
API_PORT="8000"
UI_PORT="8501"
API_PID=""

# Python is the only required system-level tool for this script path.
if command -v python3 >/dev/null 2>&1; then
  PY_CMD="python3"
elif command -v python >/dev/null 2>&1; then
  PY_CMD="python"
else
  missing+=("python3")
fi

if [ "${#missing[@]}" -gt 0 ]; then
  printf 'Missing system dependencies:%s\n' " ${missing[*]}"
  echo "Install the missing system tools, then rerun this script."
  exit 1
fi

# Keep pip current to reduce installation edge cases.
"$PY_CMD" -m pip install --upgrade pip

# Runtime dependencies come from pyproject.toml.
"$PY_CMD" -m pip install -e .

# Dev dependencies enable pytest and dev checks when present.
if [ -f requirements-dev.txt ]; then
  "$PY_CMD" -m pip install -r requirements-dev.txt
fi

# Run tests before launching the UI to fail fast on setup issues.
"$PY_CMD" -m pytest -q

cleanup() {
  # When the frontend stops, cleanly stop the backend to avoid orphan ports.
  if [ -n "${API_PID}" ]; then
    kill "${API_PID}" >/dev/null 2>&1 || true
    wait "${API_PID}" 2>/dev/null || true
  fi
}

trap cleanup EXIT INT TERM

echo "Tests passed. Starting FastAPI on ${API_HOST}:${API_PORT}..."
"$PY_CMD" -m uvicorn api_fastapi.main:app --host "$API_HOST" --port "$API_PORT" >/tmp/research_os_api.log 2>&1 &
API_PID=$!

# Wait for backend readiness before launching Streamlit.
api_ok=0
for _ in $(seq 1 20); do
  if "$PY_CMD" -c "import sys, urllib.request; r=urllib.request.urlopen('http://${API_HOST}:${API_PORT}/docs', timeout=1); sys.exit(0 if r.status==200 else 1)" >/dev/null 2>&1; then
    api_ok=1
    break
  fi
  sleep 0.5
done

if [ "$api_ok" -ne 1 ]; then
  echo "FastAPI did not become ready on http://${API_HOST}:${API_PORT}/docs"
  echo "Last backend log lines:"
  tail -n 40 /tmp/research_os_api.log || true
  exit 1
fi

echo "FastAPI is ready. Starting Streamlit on port ${UI_PORT}..."
"$PY_CMD" -m streamlit run app_streamlit/app.py --server.port "$UI_PORT"
