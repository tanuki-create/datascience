#!/usr/bin/env bash
# opsctl ping-check（補助実装）: 複数ホストへの疎通確認を並列に行う。
#
# samples/python/15_ping_check.py が主実装であり、こちらはBashだけで
# 完結させたい場面向けの簡易版である。重要ホスト判定や全体デッドラインは
# 実装していない。
set -euo pipefail

hosts_file=""
report_file=""
timeout=3
max_parallel=8
dry_run=0

usage() {
  cat <<'EOF' >&2
Usage: 15_ping_check.sh --hosts-file PATH --report PATH \
       [--timeout N] [--max-parallel N] [--dry-run]

Linuxの ping -W は秒指定である。macOSでは -W がミリ秒指定になり
挙動が異なるため、ラボ環境はLinuxを前提にする。
EOF
}

log() {
  local level="$1"; shift
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) ${level} $*" >&2
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --hosts-file) hosts_file="${2:-}"; shift 2 ;;
    --report) report_file="${2:-}"; shift 2 ;;
    --timeout) timeout="${2:-}"; shift 2 ;;
    --max-parallel) max_parallel="${2:-}"; shift 2 ;;
    --dry-run) dry_run=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown argument: $1" >&2; usage; exit 1 ;;
  esac
done

if [[ -z "${hosts_file}" || -z "${report_file}" ]]; then
  echo "--hosts-file and --report are required" >&2
  usage
  exit 1
fi

if [[ ! -f "${hosts_file}" ]]; then
  echo "hosts file not found: ${hosts_file}" >&2
  exit 1
fi

mkdir -p "$(dirname "${report_file}")"

check_host() {
  local host="$1"
  if ping -c 1 -W "${timeout}" "${host}" >/dev/null 2>&1; then
    echo "${host},true"
  else
    echo "${host},false"
  fi
}
export -f check_host
export timeout

mapfile -t hosts < <(grep -vE '^[[:space:]]*(#|$)' "${hosts_file}")

if [[ "${#hosts[@]}" -eq 0 ]]; then
  echo "hosts file is empty: ${hosts_file}" >&2
  exit 1
fi

if [[ "${dry_run}" -eq 1 ]]; then
  for host in "${hosts[@]}"; do
    log INFO "dry-run: would ping ${host} timeout=${timeout}s"
  done
  exit 0
fi

echo "host,ok" > "${report_file}"
printf '%s\n' "${hosts[@]}" | xargs -P "${max_parallel}" -I{} bash -c 'check_host "$@"' _ {} >> "${report_file}"

failures="$(grep -c ',false$' "${report_file}" || true)"
log INFO "wrote report to ${report_file} (failures=${failures})"

if [[ "${failures}" -gt 0 ]]; then
  exit 2
fi
exit 0
