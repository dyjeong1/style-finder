#!/bin/zsh
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
RUNTIME_DIR="$ROOT_DIR/.local-runtime"
BACKEND_PID_FILE="$RUNTIME_DIR/backend.pid"
FRONTEND_PID_FILE="$RUNTIME_DIR/frontend.pid"
BACKEND_LOG_FILE="$RUNTIME_DIR/backend.log"
FRONTEND_LOG_FILE="$RUNTIME_DIR/frontend.log"

print_status() {
  local name="$1"
  local pid_file="$2"
  local url="$3"
  local log_file="$4"

  if [[ ! -f "$pid_file" ]]; then
    echo "$name: stopped"
    return 0
  fi

  local pid
  pid="$(tr -d '[:space:]' < "$pid_file")"
  if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
    echo "$name: running (pid $pid)"
    echo "  url: $url"
    echo "  log: $log_file"
    return 0
  fi

  rm -f "$pid_file"
  echo "$name: stopped (stale pid removed)"
}

print_status "backend" "$BACKEND_PID_FILE" "http://127.0.0.1:8000/health" "$BACKEND_LOG_FILE"
print_status "frontend" "$FRONTEND_PID_FILE" "http://127.0.0.1:3000/upload" "$FRONTEND_LOG_FILE"
