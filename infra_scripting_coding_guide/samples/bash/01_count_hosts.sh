#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 HOSTS_FILE" >&2
  exit 1
fi

hosts_file="$1"
if [[ ! -f "${hosts_file}" ]]; then
  echo "hosts file not found: ${hosts_file}" >&2
  exit 2
fi

count=0
line_no=0
while IFS= read -r raw || [[ -n "${raw}" ]]; do
  line_no=$((line_no + 1))
  line="$(printf '%s' "${raw}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
  [[ -z "${line}" ]] && continue
  [[ "${line}" == \#* ]] && continue
  if [[ "${line}" =~ [[:space:]] ]]; then
    echo "invalid host at line ${line_no}: contains whitespace" >&2
    exit 2
  fi
  count=$((count + 1))
done < "${hosts_file}"

echo "loaded ${count} hosts" >&2
echo "${count}"
