#!/usr/bin/env bash
# 13_classify_disk.sh のテスト。
# フレームワークを使わず、関数呼び出しと終了コード・出力の比較で assert する。
#
# 実行方法:
#   bash tests/test_13_classify_disk.sh
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# shellcheck source=/dev/null
source "${repo_root}/samples/bash/13_classify_disk.sh"

failures=0

assert_eq() {
  local expected="$1"
  local actual="$2"
  local message="$3"
  if [[ "${expected}" != "${actual}" ]]; then
    echo "FAIL: ${message}: expected=${expected} actual=${actual}" >&2
    failures=$(( failures + 1 ))
  else
    echo "ok: ${message}"
  fi
}

# --- classify_disk_usage: 正常系・境界値 ---

assert_eq "ok" "$(classify_disk_usage 50 80 90)" "50% with warn=80/crit=90 is ok"
assert_eq "warning" "$(classify_disk_usage 80 80 90)" "80% (=warn) is warning"
assert_eq "critical" "$(classify_disk_usage 90 80 90)" "90% (=crit) is critical"
assert_eq "critical" "$(classify_disk_usage 100 80 90)" "100% is critical"
assert_eq "ok" "$(classify_disk_usage 0 80 90)" "0% is ok"

# --- classify_disk_usage: 異常系 ---

set +e
classify_disk_usage 85 90 80 > /dev/null 2>&1
rc=$?
set -e
assert_eq "2" "${rc}" "inverted thresholds return exit code 2"

set +e
classify_disk_usage 150 80 90 > /dev/null 2>&1
rc=$?
set -e
assert_eq "2" "${rc}" "out-of-range used_percent returns exit code 2"

# --- parse_and_classify: 複数行、worstの判定 ---

sample_input=$'Filesystem 1024-blocks Used Available Capacity Mounted-on\n/dev/sda1 100 88 12 88% /\n/dev/sda2 100 35 65 35% /var\n/dev/sda3 100 98 2 98% /data\n'

set +e
output="$(printf '%s' "${sample_input}" | parse_and_classify 80 90 2>/tmp/test_13_classify_disk_stderr.$$)"
rc=$?
set -e
stderr_output="$(cat "/tmp/test_13_classify_disk_stderr.$$")"
rm -f "/tmp/test_13_classify_disk_stderr.$$"

assert_eq "1" "${rc}" "parse_and_classify returns 1 when worst=critical"
assert_eq "worst=critical" "${stderr_output##*$'\n'}" "stderr reports worst=critical"
[[ "${output}" == *"mount=/data used_percent=98 status=critical"* ]] || {
  echo "FAIL: expected /data critical line in output, got: ${output}" >&2
  failures=$(( failures + 1 ))
}

# --- main: 終了コードの総合確認 ---

set +e
printf '%s' "${sample_input}" | main --warn-percent 80 --crit-percent 90 > /dev/null 2>&1
rc=$?
set -e
assert_eq "3" "${rc}" "main returns 3 when worst=critical"

set +e
printf 'Filesystem 1024-blocks Used Available Capacity Mounted-on\n/dev/sda1 100 10 90 10%% /\n' | main > /dev/null 2>&1
rc=$?
set -e
assert_eq "0" "${rc}" "main returns 0 when all ok"

if [[ "${failures}" -gt 0 ]]; then
  echo "FAILED: ${failures} assertion(s) failed" >&2
  exit 1
fi

echo "all assertions passed"
