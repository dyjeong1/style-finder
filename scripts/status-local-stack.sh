#!/bin/zsh
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
RUNTIME_DIR="$ROOT_DIR/.local-runtime"
BACKEND_PID_FILE="$RUNTIME_DIR/backend.pid"
FRONTEND_PID_FILE="$RUNTIME_DIR/frontend.pid"
BACKEND_LOG_FILE="$RUNTIME_DIR/backend.log"
FRONTEND_LOG_FILE="$RUNTIME_DIR/frontend.log"
BACKEND_PORT="8000"
FRONTEND_PORT="3000"

find_listen_pid() {
  local port="$1"
  lsof -tiTCP:"$port" -sTCP:LISTEN 2>/dev/null | head -n 1
}

print_status() {
  local name="$1"
  local pid_file="$2"
  local url="$3"
  local log_file="$4"
  local port="$5"
  local pid=""

  if [[ -f "$pid_file" ]]; then
    pid="$(tr -d '[:space:]' < "$pid_file")"
  fi

  if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
    echo "$name: running (pid $pid)"
    echo "  url: $url"
    echo "  log: $log_file"
    return 0
  fi

  pid="$(find_listen_pid "$port" || true)"
  if [[ -n "$pid" ]]; then
    printf '%s\n' "$pid" > "$pid_file"
    echo "$name: running (pid $pid)"
    echo "  url: $url"
    echo "  log: $log_file"
    return 0
  fi

  rm -f "$pid_file"
  echo "$name: stopped"
}

print_status "backend" "$BACKEND_PID_FILE" "http://127.0.0.1:$BACKEND_PORT/health" "$BACKEND_LOG_FILE" "$BACKEND_PORT"
print_status "frontend" "$FRONTEND_PID_FILE" "http://127.0.0.1:$FRONTEND_PORT/upload" "$FRONTEND_LOG_FILE" "$FRONTEND_PORT"
