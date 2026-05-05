#!/bin/zsh
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
RUNTIME_DIR="$ROOT_DIR/.local-runtime"
BACKEND_PID_FILE="$RUNTIME_DIR/backend.pid"
FRONTEND_PID_FILE="$RUNTIME_DIR/frontend.pid"
BACKEND_PORT="8000"
FRONTEND_PORT="3000"

find_listen_pid() {
  local port="$1"
  lsof -tiTCP:"$port" -sTCP:LISTEN 2>/dev/null | head -n 1
}

stop_process() {
  local name="$1"
  local pid_file="$2"
  local port="$3"
  local pid=""

  if [[ -f "$pid_file" ]]; then
    pid="$(tr -d '[:space:]' < "$pid_file")"
  fi

  if [[ -z "$pid" ]] || ! kill -0 "$pid" 2>/dev/null; then
    pid="$(find_listen_pid "$port" || true)"
  fi
  rm -f "$pid_file"

  if [[ -z "$pid" ]] || ! kill -0 "$pid" 2>/dev/null; then
    echo "$name already stopped"
    return 0
  fi

  kill "$pid" 2>/dev/null || true
  for _ in $(seq 1 20); do
    if ! kill -0 "$pid" 2>/dev/null; then
      echo "$name stopped"
      return 0
    fi
    sleep 1
  done

  kill -9 "$pid" 2>/dev/null || true
  echo "$name force stopped"
}

stop_process "frontend" "$FRONTEND_PID_FILE" "$FRONTEND_PORT"
stop_process "backend" "$BACKEND_PID_FILE" "$BACKEND_PORT"
