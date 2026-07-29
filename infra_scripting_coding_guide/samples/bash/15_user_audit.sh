#!/usr/bin/env bash
# opsctl user-audit（補助実装、Linux）: /etc/passwd を棚卸しする。
#
# samples/powershell/15_user_audit.ps1 がWindows向けの主実装であり、
# こちらはLinuxのローカルアカウントを対象にした簡易版である。
# 読み取り専用であり、アカウントの変更は行わない。
set -euo pipefail

uid_min=1000
report_file="work/reports/user_audit.csv"
dry_run=0
declare -a allowed_shells=("/bin/bash" "/usr/sbin/nologin" "/bin/false")

usage() {
  cat <<'EOF' >&2
Usage: 15_user_audit.sh [--uid-min N] [--report PATH] [--dry-run]
EOF
}

log() {
  local level="$1"; shift
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) ${level} $*" >&2
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --uid-min) uid_min="${2:-}"; shift 2 ;;
    --report) report_file="${2:-}"; shift 2 ;;
    --dry-run) dry_run=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown argument: $1" >&2; usage; exit 1 ;;
  esac
done

is_allowed_shell() {
  local shell="$1"
  local allowed
  for allowed in "${allowed_shells[@]}"; do
    [[ "${shell}" == "${allowed}" ]] && return 0
  done
  return 1
}

if [[ ! -r /etc/passwd ]]; then
  echo "/etc/passwd is not readable" >&2
  exit 1
fi

mapfile -t target_lines < <(awk -F: -v min="${uid_min}" '$3 >= min {print}' /etc/passwd)

if [[ "${dry_run}" -eq 1 ]]; then
  for line in "${target_lines[@]}"; do
    name="$(cut -d: -f1 <<< "${line}")"
    log INFO "dry-run: would audit account=${name}"
  done
  exit 0
fi

mkdir -p "$(dirname "${report_file}")"
echo "name,uid,shell,finding" > "${report_file}"

had_finding=0
for line in "${target_lines[@]}"; do
  name="$(cut -d: -f1 <<< "${line}")"
  uid="$(cut -d: -f3 <<< "${line}")"
  shell="$(cut -d: -f7 <<< "${line}")"
  finding=""
  if ! is_allowed_shell "${shell}"; then
    finding="unexpected_shell:${shell}"
    had_finding=1
  fi
  echo "${name},${uid},${shell},${finding}" >> "${report_file}"
  [[ -n "${finding}" ]] && log WARNING "account=${name} finding=${finding}"
done

log INFO "wrote report to ${report_file}"

if [[ "${had_finding}" -eq 1 ]]; then
  exit 2
fi
exit 0
