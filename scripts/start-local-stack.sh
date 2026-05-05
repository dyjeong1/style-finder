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

mkdir -p "$RUNTIME_DIR"

read_pid() {
  local pid_file="$1"
  [[ -f "$pid_file" ]] || return 1
  local pid
  pid="$(tr -d '[:space:]' < "$pid_file")"
  [[ -n "$pid" ]] || return 1
  printf '%s\n' "$pid"
}

ensure_pid_file_state() {
  local pid_file="$1"
  local port="$2"
  local pid
  if ! pid="$(read_pid "$pid_file")"; then
    pid="$(find_listen_pid "$port" || true)"
    if [[ -n "$pid" ]]; then
      printf '%s\n' "$pid" > "$pid_file"
      return 0
    fi
    rm -f "$pid_file"
    return 1
  fi
  if kill -0 "$pid" 2>/dev/null; then
    return 0
  fi
  pid="$(find_listen_pid "$port" || true)"
  if [[ -n "$pid" ]]; then
    printf '%s\n' "$pid" > "$pid_file"
    return 0
  fi
  rm -f "$pid_file"
  return 1
}

find_listen_pid() {
  local port="$1"
  lsof -tiTCP:"$port" -sTCP:LISTEN 2>/dev/null | head -n 1
}

record_listen_pid() {
  local pid_file="$1"
  local port="$2"
  local pid
  pid="$(find_listen_pid "$port" || true)"
  [[ -n "$pid" ]] || return 1
  printf '%s\n' "$pid" > "$pid_file"
  return 0
}

start_backend() {
  if ensure_pid_file_state "$BACKEND_PID_FILE" "$BACKEND_PORT"; then
    echo "backend already running (pid $(read_pid "$BACKEND_PID_FILE"))"
    return 0
  fi

  (
    cd "$ROOT_DIR/backend"
    nohup python3 -m uvicorn src.main:app --host 127.0.0.1 --port 8000 > "$BACKEND_LOG_FILE" 2>&1 &
    echo $! > "$BACKEND_PID_FILE"
  )
  echo "backend starting"
}

start_frontend() {
  if ensure_pid_file_state "$FRONTEND_PID_FILE" "$FRONTEND_PORT"; then
    echo "frontend already running (pid $(read_pid "$FRONTEND_PID_FILE"))"
    return 0
  fi

  (
    export NVM_DIR="$HOME/.nvm"
    if [[ -s "$NVM_DIR/nvm.sh" ]]; then
      . "$NVM_DIR/nvm.sh"
    fi
    cd "$ROOT_DIR/frontend"
    nohup npm run local > "$FRONTEND_LOG_FILE" 2>&1 &
    echo $! > "$FRONTEND_PID_FILE"
  )
  echo "frontend starting"
}

wait_for_url() {
  local url="$1"
  local name="$2"
  local attempts="${3:-120}"

  for _ in $(seq 1 "$attempts"); do
    if curl -fsS "$url" >/dev/null 2>&1; then
      echo "$name ready: $url"
      return 0
    fi
    sleep 1
  done

  echo "$name failed to become ready: $url" >&2
  return 1
}

show_recent_log() {
  local log_file="$1"
  if [[ -f "$log_file" ]]; then
    tail -n 40 "$log_file" >&2
  fi
}

start_backend
if ! wait_for_url "http://127.0.0.1:$BACKEND_PORT/health" "backend" 30; then
  show_recent_log "$BACKEND_LOG_FILE"
  exit 1
fi
record_listen_pid "$BACKEND_PID_FILE" "$BACKEND_PORT" || true

start_frontend
if ! wait_for_url "http://127.0.0.1:$FRONTEND_PORT/upload" "frontend" 120; then
  show_recent_log "$FRONTEND_LOG_FILE"
  exit 1
fi
record_listen_pid "$FRONTEND_PID_FILE" "$FRONTEND_PORT" || true

echo "local stack ready"
echo "frontend: http://127.0.0.1:$FRONTEND_PORT/upload"
echo "backend:  http://127.0.0.1:$BACKEND_PORT/health"
echo "logs: $BACKEND_LOG_FILE / $FRONTEND_LOG_FILE"
