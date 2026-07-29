#!/usr/bin/env bash
# Classify disk usage rows and write a status report.
#
# Demonstrates splitting a Bash script into single-responsibility
# functions: load_usages (I/O), classify (pure), write_header/append_row
# (I/O), summarize_exit_code (pure).
set -euo pipefail

input_file=""
output_file=""
warn=80
crit=90

usage() {
  cat <<'EOF' >&2
Usage: 05_disk_report.sh --input PATH --output PATH [--warn N] [--crit N]

Input CSV format: host,usage_percent
EOF
}

# --- pure function: no I/O, deterministic ---
classify() {
  local usage_percent="$1" warn_v="$2" crit_v="$3"
  if (( usage_percent >= crit_v )); then
    echo CRITICAL
  elif (( usage_percent >= warn_v )); then
    echo WARNING
  else
    echo OK
  fi
}

# --- I/O function ---
load_usages() {
  local path="$1"
  if [[ ! -f "${path}" ]]; then
    echo "usage file not found: ${path}" >&2
    return 1
  fi
  # Skip the header line, print "host,usage_percent" data rows.
  tail -n +2 "${path}"
}

# --- I/O function ---
write_header() {
  local path="$1"
  mkdir -p "$(dirname "${path}")"
  echo "host,usage_percent,status" > "${path}"
}

# --- I/O function ---
append_row() {
  local path="$1" host="$2" usage_percent="$3" status="$4"
  echo "${host},${usage_percent},${status}" >> "${path}"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --input) input_file="${2:-}"; shift 2 ;;
    --output) output_file="${2:-}"; shift 2 ;;
    --warn) warn="${2:-}"; shift 2 ;;
    --crit) crit="${2:-}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown argument: $1" >&2; usage; exit 1 ;;
  esac
done

if [[ -z "${input_file}" || -z "${output_file}" ]]; then
  echo "--input and --output are required" >&2
  usage
  exit 1
fi

if (( warn > crit )); then
  echo "--warn must be <= --crit" >&2
  exit 1
fi

rows="$(load_usages "${input_file}")" || exit 1
write_header "${output_file}"

had_critical=0
while IFS=',' read -r host usage_percent; do
  [[ -z "${host}" ]] && continue
  status="$(classify "${usage_percent}" "${warn}" "${crit}")"
  append_row "${output_file}" "${host}" "${usage_percent}" "${status}"
  [[ "${status}" == "CRITICAL" ]] && had_critical=1
done <<< "${rows}"

echo "wrote report to ${output_file}" >&2

if [[ "${had_critical}" -eq 1 ]]; then
  exit 3
fi
exit 0
