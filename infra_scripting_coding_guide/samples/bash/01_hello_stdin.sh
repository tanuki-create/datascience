#!/usr/bin/env bash
set -euo pipefail

read -r name
if [[ -z "${name}" ]]; then
  echo "name is required" >&2
  exit 1
fi

echo "hello, ${name}"
