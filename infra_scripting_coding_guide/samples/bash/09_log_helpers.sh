#!/usr/bin/env bash
# ログ用ヘルパー関数。source して使う。
#   source samples/bash/09_log_helpers.sh
#   log INFO "starting"
#   log_json INFO "starting"
set -uo pipefail

log() {
  local level="$1"
  shift
  printf '%s %s %s\n' "$(date -u +'%Y-%m-%dT%H:%M:%SZ')" "${level}" "$*" >&2
}

log_json() {
  local level="$1"
  local message="$2"
  if ! command -v jq >/dev/null 2>&1; then
    log "${level}" "${message}"
    return 0
  fi
  jq -n -c \
    --arg ts "$(date -u +'%Y-%m-%dT%H:%M:%SZ')" \
    --arg level "${level}" \
    --arg run_id "${RUN_ID:-unknown}" \
    --arg message "${message}" \
    '{ts: $ts, level: $level, run_id: $run_id, event: "opsctl", message: $message}' >&2
}

# このファイルが直接実行された場合は簡単なデモを表示する
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  RUN_ID="$(python3 -c 'import uuid; print(uuid.uuid4())' 2>/dev/null || echo unknown)"
  log INFO "starting"
  log_json WARNING "disk usage high: 85%"
  log INFO "finished"
fi
