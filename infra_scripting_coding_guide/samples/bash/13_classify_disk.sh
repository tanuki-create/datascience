#!/usr/bin/env bash
# ディスク使用率を ok/warning/critical に分類する（第13章のテスト対象）。
# 標準入力から `df -P` 相当のテキストを受け取り、閾値で分類する。
#
# 使い方:
#   df -P | ./13_classify_disk.sh --warn-percent 80 --crit-percent 90
#
# 終了コード:
#   0 = 最悪ステータスが ok または warning
#   2 = 引数誤り、閾値誤り
#   3 = 最悪ステータスが critical
set -euo pipefail

usage() {
  cat <<'EOF' >&2
Usage: 13_classify_disk.sh [--warn-percent N] [--crit-percent N]
  --warn-percent N   default: 80
  --crit-percent N   default: 90

標準入力から df -P 相当のテキストを読み込む。
EOF
}

# used_percent を warn/crit の閾値で ok/warning/critical に分類する。
# 引数はすべて整数percentを想定する（df の出力に合わせる）。
classify_disk_usage() {
  local used_percent="$1"
  local warn_percent="$2"
  local crit_percent="$3"

  if (( warn_percent > crit_percent )); then
    echo "invalid thresholds: warn(${warn_percent}) > crit(${crit_percent})" >&2
    return 2
  fi
  if (( used_percent < 0 || used_percent > 100 )); then
    echo "used_percent out of range: ${used_percent}" >&2
    return 2
  fi

  if (( used_percent >= crit_percent )); then
    echo "critical"
  elif (( used_percent >= warn_percent )); then
    echo "warning"
  else
    echo "ok"
  fi
}

# 標準入力から df -P 相当のテキストを読み、1行ごとに分類結果を出力する。
# 最後に worst=... を標準エラーへ出し、戻り値でも最悪ステータスを表す。
parse_and_classify() {
  local warn_percent="$1"
  local crit_percent="$2"
  local worst="ok"
  local status
  local line

  # ヘッダー行を読み捨てる。入力が空の場合は何もせず正常終了する。
  if ! read -r _header; then
    echo "worst=${worst}" >&2
    return 0
  fi

  while IFS= read -r line || [[ -n "${line}" ]]; do
    [[ -z "${line}" ]] && continue

    local fields
    read -r -a fields <<< "${line}"
    if (( ${#fields[@]} < 6 )); then
      echo "skipping malformed line: ${line}" >&2
      continue
    fi

    local percent="${fields[4]%\%}"
    local mount="${fields[5]}"
    if ! [[ "${percent}" =~ ^[0-9]+$ ]]; then
      echo "skipping non-numeric percent: ${line}" >&2
      continue
    fi

    if ! status="$(classify_disk_usage "${percent}" "${warn_percent}" "${crit_percent}")"; then
      return 2
    fi
    echo "mount=${mount} used_percent=${percent} status=${status}"

    case "${status}" in
      critical) worst="critical" ;;
      warning)
        if [[ "${worst}" != "critical" ]]; then
          worst="warning"
        fi
        ;;
    esac
  done

  echo "worst=${worst}" >&2
  [[ "${worst}" != "critical" ]]
}

main() {
  local warn_percent=80
  local crit_percent=90

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --warn-percent) warn_percent="${2:-}"; shift 2 ;;
      --crit-percent) crit_percent="${2:-}"; shift 2 ;;
      -h|--help) usage; return 0 ;;
      *) echo "unknown argument: $1" >&2; usage; return 2 ;;
    esac
  done

  if parse_and_classify "${warn_percent}" "${crit_percent}"; then
    return 0
  else
    local rc=$?
    # rc=1 は「最悪ステータスがcritical」を表すparse_and_classifyの終了コード、
    # rc=2 は閾値やused_percentの検証エラーをそのまま伝播させる。
    if [[ "${rc}" -eq 1 ]]; then
      return 3
    fi
    return "${rc}"
  fi
}

# このファイルが直接実行された場合のみ main を呼ぶ。
# source されてテストから関数だけを使う場合は実行しない（第13章のテスト方法を参照）。
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
