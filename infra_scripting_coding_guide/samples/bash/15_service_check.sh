#!/usr/bin/env bash
# opsctl service-check: サービス稼働確認（systemd / SysV）。
#
# 警告: --restart-on-failure はサービスを再起動する。
# 本番では変更管理の承認なしに使わないこと。まず --dry-run で確認する。
set -uo pipefail

readonly EXIT_OK=0
readonly EXIT_USAGE=1
readonly EXIT_RUNTIME=2
readonly EXIT_CRITICAL=3

run_id="$(date -u +%Y%m%dT%H%M%SZ)-$$"
services=()
init_type="auto"
restart_on_failure=0
report=""
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
Usage: 15_service_check.sh --service NAME [--service NAME ...]
                            [--init systemd|sysv|auto]
                            [--restart-on-failure]
                            [--report FILE] [--dry-run] [--verbose]
EOF
}

detect_init() {
  if command -v systemctl >/dev/null 2>&1; then
    echo systemd
  elif command -v service >/dev/null 2>&1; then
    echo sysv
  else
    echo none
  fi
}

is_active() {
  local name="$1"
  case "${init_type}" in
    systemd)
      systemctl is-active --quiet "${name}"
      ;;
    sysv)
      service "${name}" status >/dev/null 2>&1
      ;;
    *)
      return 1
      ;;
  esac
}

do_restart() {
  local name="$1"
  case "${init_type}" in
    systemd)
      systemctl restart "${name}"
      ;;
    sysv)
      service "${name}" restart
      ;;
    *)
      return 1
      ;;
  esac
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --service)
      services+=("${2:?missing value for --service}")
      shift 2
      ;;
    --init)
      init_type="${2:?missing value for --init}"
      shift 2
      ;;
    --restart-on-failure)
      restart_on_failure=1
      shift
      ;;
    --report)
      report="${2:?missing value for --report}"
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

if [[ ${#services[@]} -eq 0 ]]; then
  echo "at least one --service is required" >&2
  usage
  exit "${EXIT_USAGE}"
fi

case "${init_type}" in
  auto)
    init_type="$(detect_init)"
    ;;
  systemd|sysv)
    ;;
  *)
    echo "--init must be systemd, sysv, or auto" >&2
    exit "${EXIT_USAGE}"
    ;;
esac

if [[ "${init_type}" == "none" && "${dry_run}" -ne 1 ]]; then
  echo "neither systemctl nor service is available on this host" >&2
  echo "use --dry-run to validate arguments on unsupported hosts" >&2
  exit "${EXIT_USAGE}"
fi

log INFO "init_type=${init_type} dry_run=${dry_run} restart_on_failure=${restart_on_failure}"

rows=()
had_error=0
had_critical=0

for svc in "${services[@]}"; do
  if [[ "${dry_run}" -eq 1 ]]; then
    log INFO "dry-run: would check service=${svc} via ${init_type}"
    if [[ "${restart_on_failure}" -eq 1 ]]; then
      log INFO "dry-run: would restart ${svc} if inactive"
    fi
    rows+=("${svc},dry-run,skipped")
    continue
  fi

  if is_active "${svc}"; then
    log INFO "service=${svc} status=active"
    rows+=("${svc},active,ok")
    continue
  fi

  log WARNING "service=${svc} status=inactive"
  action="none"
  if [[ "${restart_on_failure}" -eq 1 ]]; then
    log WARNING "restarting service=${svc}"
    if do_restart "${svc}"; then
      if is_active "${svc}"; then
        action="restarted"
        log INFO "service=${svc} restarted and active"
        rows+=("${svc},active,${action}")
        continue
      fi
      action="restart_failed"
      log ERROR "service=${svc} still inactive after restart"
    else
      action="restart_failed"
      log ERROR "restart command failed for service=${svc}"
    fi
  fi

  rows+=("${svc},inactive,${action}")
  had_critical=1
done

if [[ "${dry_run}" -ne 1 && -n "${report}" ]]; then
  mkdir -p "$(dirname "${report}")"
  {
    echo "service,status,detail"
    printf '%s\n' "${rows[@]}"
  } > "${report}"
  log INFO "wrote report ${report}"
fi

if [[ "${dry_run}" -eq 1 ]]; then
  exit "${EXIT_OK}"
fi
if [[ "${had_critical}" -eq 1 ]]; then
  exit "${EXIT_CRITICAL}"
fi
if [[ "${had_error}" -eq 1 ]]; then
  exit "${EXIT_RUNTIME}"
fi
exit "${EXIT_OK}"
