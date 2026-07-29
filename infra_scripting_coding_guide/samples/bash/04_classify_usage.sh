#!/usr/bin/env bash
# opsctl helper: classify disk usage percent (integer).
set -euo pipefail

usage=""
warn=80
crit=90

usage_help() {
  cat <<'EOF' >&2
Usage: 04_classify_usage.sh --usage N [--warn N] [--crit N]
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --usage) usage="${2:-}"; shift 2 ;;
    --warn) warn="${2:-}"; shift 2 ;;
    --crit) crit="${2:-}"; shift 2 ;;
    -h|--help) usage_help; exit 0 ;;
    *) echo "unknown argument: $1" >&2; usage_help; exit 1 ;;
  esac
done

if [[ -z "${usage}" ]]; then
  echo "--usage is required" >&2
  usage_help
  exit 1
fi

if ! [[ "${usage}" =~ ^[0-9]+$ && "${warn}" =~ ^[0-9]+$ && "${crit}" =~ ^[0-9]+$ ]]; then
  echo "usage/warn/crit must be non-negative integers" >&2
  exit 1
fi

if (( usage > 100 || warn > 100 || crit > 100 )); then
  echo "usage/warn/crit must be <= 100" >&2
  exit 1
fi

if (( warn > crit )); then
  echo "warn must be <= crit" >&2
  exit 1
fi

if (( usage >= crit )); then
  echo CRITICAL
  exit 3
fi
if (( usage >= warn )); then
  echo WARNING
  exit 0
fi
echo OK
exit 0
