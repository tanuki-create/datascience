#!/usr/bin/env bash
# Safely update a text configuration file.
#
# Takes a timestamped backup before writing, and replaces the target file
# atomically via a temporary file in the same directory plus mv.
#
# WARNING: this script overwrites the target file in place (after backing
# it up). Do not point it at a production file without testing in a
# sandbox first.
set -euo pipefail

target=""
content_file=""
backup_dir=""

usage() {
  cat <<'EOF' >&2
Usage: 06_safe_config_update.sh --target PATH --content-file PATH --backup-dir DIR
EOF
}

update_config() {
  local path="$1" new_content_file="$2" backup_dir="$3"
  local timestamp
  timestamp="$(date -u +%Y%m%dT%H%M%SZ)"

  mkdir -p "${backup_dir}"

  if [[ -f "${path}" ]]; then
    cp -p "${path}" "${backup_dir}/$(basename "${path}").${timestamp}.bak"
    echo "backed up previous content to ${backup_dir}/$(basename "${path}").${timestamp}.bak" >&2
  else
    echo "no previous file; creating ${path}" >&2
  fi

  local tmp_file
  tmp_file="$(mktemp "$(dirname "${path}")/.$(basename "${path}").XXXXXX")"
  # If we exit before the mv below, remove the leftover temp file.
  trap 'rm -f "${tmp_file}"' RETURN

  cp "${new_content_file}" "${tmp_file}"
  mv "${tmp_file}" "${path}"
  trap - RETURN
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target) target="${2:-}"; shift 2 ;;
    --content-file) content_file="${2:-}"; shift 2 ;;
    --backup-dir) backup_dir="${2:-}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown argument: $1" >&2; usage; exit 1 ;;
  esac
done

if [[ -z "${target}" || -z "${content_file}" || -z "${backup_dir}" ]]; then
  echo "--target, --content-file and --backup-dir are required" >&2
  usage
  exit 1
fi

if [[ ! -f "${content_file}" ]]; then
  echo "content file not found: ${content_file}" >&2
  exit 1
fi

if [[ ! -s "${content_file}" ]]; then
  echo "refusing to write empty content" >&2
  exit 2
fi

update_config "${target}" "${content_file}" "${backup_dir}"
echo "updated ${target}" >&2
exit 0
