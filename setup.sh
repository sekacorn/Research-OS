#!/usr/bin/env bash
set -euo pipefail

# Project setup script for Unix-like shells.
# By default it creates a local virtual environment in .venv and installs
# runtime plus development dependencies.

USE_VENV=1
VENV_DIR=".venv"

for arg in "$@"; do
  case "$arg" in
    --system)
      USE_VENV=0
      ;;
    --venv-dir=*)
      VENV_DIR="${arg#*=}"
      ;;
    *)
      echo "Unknown option: $arg"
      echo "Usage: bash setup.sh [--system] [--venv-dir=.venv]"
      exit 1
      ;;
  esac
done

detect_python() {
  if command -v python3 >/dev/null 2>&1; then
    echo "python3"
    return 0
  fi
  if command -v python >/dev/null 2>&1; then
    echo "python"
    return 0
  fi
  if command -v py >/dev/null 2>&1; then
    echo "py -3"
    return 0
  fi
  return 1
}

if ! PY_CMD="$(detect_python)"; then
  echo "Missing system dependency: Python 3.10+"
  echo "Install Python, then rerun setup.sh."
  exit 1
fi

run_py() {
  # shellcheck disable=SC2086
  $PY_CMD "$@"
}

if [ "$USE_VENV" -eq 1 ]; then
  if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in $VENV_DIR..."
    run_py -m venv "$VENV_DIR"
  else
    echo "Using existing virtual environment in $VENV_DIR..."
  fi

  if [ -x "$VENV_DIR/bin/python" ]; then
    PYTHON_BIN="$VENV_DIR/bin/python"
    ACTIVATE_HINT="source $VENV_DIR/bin/activate"
  elif [ -x "$VENV_DIR/Scripts/python.exe" ]; then
    PYTHON_BIN="$VENV_DIR/Scripts/python.exe"
    ACTIVATE_HINT="source $VENV_DIR/Scripts/activate"
  else
    echo "Could not locate the virtual environment Python interpreter."
    exit 1
  fi
else
  PYTHON_BIN=""
  ACTIVATE_HINT=""
fi

run_install() {
  local python_bin="$1"
  "$python_bin" -m pip install --upgrade pip
  "$python_bin" -m pip install -e .
  if [ -f requirements-dev.txt ]; then
    "$python_bin" -m pip install -r requirements-dev.txt
  fi
}

echo "Installing project dependencies..."
if [ "$USE_VENV" -eq 1 ]; then
  run_install "$PYTHON_BIN"
else
  # shellcheck disable=SC2086
  $PY_CMD -m pip install --upgrade pip
  # shellcheck disable=SC2086
  $PY_CMD -m pip install -e .
  if [ -f requirements-dev.txt ]; then
    # shellcheck disable=SC2086
    $PY_CMD -m pip install -r requirements-dev.txt
  fi
fi

echo
echo "Setup complete."
if [ "$USE_VENV" -eq 1 ]; then
  echo "Activate the environment with:"
  echo "  $ACTIVATE_HINT"
fi
echo "Run tests with:"
echo "  python -m pytest -q"
echo "Start the app with:"
echo "  bash run.sh"
