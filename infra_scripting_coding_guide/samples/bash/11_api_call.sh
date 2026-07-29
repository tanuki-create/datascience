#!/usr/bin/env bash
# example.invalid（実在しないドメイン）へのAPI呼び出し例。
# 実行しても名前解決に失敗するので、curlの組み立てとオプションの参考にする。
#
# Usage: OPSCTL_API_TOKEN=xxx ./11_api_call.sh [TIMEOUT_SECONDS]
set -euo pipefail

base_url="${OPSCTL_API_BASE_URL:-https://api.example.invalid}"
timeout="${1:-10}"

if [[ -z "${OPSCTL_API_TOKEN:-}" ]]; then
  echo "OPSCTL_API_TOKEN is required" >&2
  exit 1
fi

if ! [[ "${timeout}" =~ ^[1-9][0-9]*$ ]]; then
  echo "timeout must be a positive integer" >&2
  exit 1
fi

# --max-time: リクエスト全体のハードタイムアウト
# --retry / --retry-delay / --retry-connrefused: 一時的な失敗を有限回リトライ
# curlはTLS証明書検証を既定で行う。-k/--insecureを付けない
response="$(curl --silent --show-error --fail \
  --max-time "${timeout}" \
  --retry 3 --retry-delay 2 --retry-connrefused \
  -H "Authorization: Bearer ${OPSCTL_API_TOKEN}" \
  -H "Accept: application/json" \
  "${base_url}/v1/hosts?limit=100")"

if command -v jq >/dev/null 2>&1; then
  echo "${response}" | jq -r '.items[] | [.host, .status, .last_seen] | @csv'
else
  echo "${response}"
fi
