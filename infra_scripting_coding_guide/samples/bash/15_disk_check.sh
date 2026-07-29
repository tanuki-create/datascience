#!/usr/bin/env bash
# opsctl disk-check: ディスク使用率監視（Bash/df実装）。
#
# 学習用サンプルである。本番監視には既存の監視プラグインも検討すること。
# 一部パスの取得失敗後も残りを継続するため、意図して set -e は使わない。
set -uo pipefail

readonly EXIT_OK=0
readonly EXIT_USAGE=1
readonly EXIT_RUNTIME=2
readonly EXIT_CRITICAL=3

run_id="$(date -u +%Y%m%dT%H%M%SZ)-$$"
paths=()
warn_percent=80
crit_percent=90
report=""
alert_command=""
dry_run=0
verbose=0

log() {
  local level="$1"; shift
  if [[ "${level}" == "DEBUG" && "${verbose}" -ne 1 ]]; then
    return 0
  fi
  printf '%s %s run_id=%s %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "${level}" "${run_id}" "$*" >&2
}

usage() {
  cat <<'EOF' >&2
Usage: 15_disk_check.sh [--paths PATH ...] [--warn N] [--crit N]
                         [--report FILE] [--alert-command CMD]
                         [--dry-run] [--verbose]

  --paths PATH         filesystem path to check (repeatable, default: /)
  --warn N             warning threshold percent (default: 80)
  --crit N             critical threshold percent (default: 90)
  --report FILE        write CSV report to FILE (skipped in --dry-run)
  --alert-command CMD  trusted fixed command to run once if any CRITICAL
  --dry-run            evaluate thresholds but do not write report or alert
  --verbose            print DEBUG logs
EOF
}

classify() {
  local usage="$1"
  if (( usage >= crit_percent )); then
    echo CRITICAL
  elif (( usage >= warn_percent )); then
    echo WARNING
  else
    echo OK
  fi
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --paths)
      paths+=("${2:?missing value for --paths}")
      shift 2
      ;;
    --warn)
      warn_percent="${2:?missing value for --warn}"
      shift 2
      ;;
    --crit)
      crit_percent="${2:?missing value for --crit}"
      shift 2
      ;;
    --report)
      report="${2:?missing value for --report}"
      shift 2
      ;;
    --alert-command)
      alert_command="${2:?missing value for --alert-command}"
      shift 2
      ;;
    --dry-run)
      dry_run=1
      shift
      ;;
    --verbose)
      verbose=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "unknown argument: $1" >&2
      usage
      exit "${EXIT_USAGE}"
      ;;
  esac
done

if [[ ${#paths[@]} -eq 0 ]]; then
  paths=("/")
fi

if ! [[ "${warn_percent}" =~ ^[0-9]+$ && "${crit_percent}" =~ ^[0-9]+$ ]]; then
  echo "--warn/--crit must be integers" >&2
  exit "${EXIT_USAGE}"
fi
if (( warn_percent > crit_percent )); then
  echo "--warn must be <= --crit" >&2
  exit "${EXIT_USAGE}"
fi
if (( warn_percent > 100 || crit_percent > 100 )); then
  echo "--warn/--crit must be <= 100" >&2
  exit "${EXIT_USAGE}"
fi

rows=()
had_error=0
had_critical=0

for path in "${paths[@]}"; do
  if [[ ! -e "${path}" ]]; then
    log ERROR "path not found: ${path}"
    rows+=("${path},,ERROR,path not found")
    had_error=1
    continue
  fi

  # POSIX df (-P). macOS / Linux 両対応。
  df_line="$(df -P "${path}" 2>/dev/null | awk 'NR==2 {print $5}')"
  if [[ -z "${df_line}" ]]; then
    log ERROR "df failed for path=${path}"
    rows+=("${path},,ERROR,df failed")
    had_error=1
    continue
  fi

  usage_percent="${df_line%%%}"
  if ! [[ "${usage_percent}" =~ ^[0-9]+$ ]]; then
    log ERROR "unexpected df output for path=${path}: ${df_line}"
    rows+=("${path},,ERROR,unexpected df output")
    had_error=1
    continue
  fi

  status="$(classify "${usage_percent}")"
  log INFO "path=${path} usage_percent=${usage_percent} status=${status}"
  rows+=("${path},${usage_percent},${status},ok")
  if [[ "${status}" == "CRITICAL" ]]; then
    had_critical=1
  fi
done

if [[ "${dry_run}" -eq 1 ]]; then
  log INFO "dry-run: skip report write and alert-command"
  for row in "${rows[@]}"; do
    log DEBUG "dry-run row=${row}"
  done
else
  if [[ -n "${report}" ]]; then
    mkdir -p "$(dirname "${report}")"
    {
      echo "path,percent,status,detail"
      printf '%s\n' "${rows[@]}"
    } > "${report}"
    log INFO "wrote report ${report}"
  fi
  if [[ "${had_critical}" -eq 1 && -n "${alert_command}" ]]; then
    log WARNING "running alert-command"
    # 呼び出し側が信頼できる固定コマンドだけを渡すこと。
    bash -c "${alert_command}"
    alert_rc=$?
    if [[ "${alert_rc}" -ne 0 ]]; then
      log ERROR "alert-command failed rc=${alert_rc}"
      had_error=1
    fi
  fi
fi

if [[ "${had_critical}" -eq 1 ]]; then
  exit "${EXIT_CRITICAL}"
fi
if [[ "${had_error}" -eq 1 ]]; then
  exit "${EXIT_RUNTIME}"
fi
exit "${EXIT_OK}"
