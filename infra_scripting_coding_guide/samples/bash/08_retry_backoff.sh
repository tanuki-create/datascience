#!/usr/bin/env bash
# Ping hosts with retry and exponential backoff.
#
# check_once returns:
#   0  success
#   99 permanent failure (command missing) -- never retried
#   1  retryable failure -- retried up to --max-attempts
#
# Note: -W here is Linux ping's "wait seconds for a reply" flag; on
# macOS ping accepts -W too but its exact unit/behavior can differ by
# version. For strict cross-platform behavior prefer the Python sample.
set -euo pipefail

EXIT_OK=0
EXIT_USAGE=1
EXIT_RUNTIME=2
PERMANENT_RC=99

# Set by retry_with_backoff after it returns, so callers can report how
# many attempts were made.
RETRY_ATTEMPTS=0

check_once() {
  local host="$1" cmd="$2" timeout_s="$3"
  if ! command -v "${cmd}" >/dev/null 2>&1; then
    echo "command not found: ${cmd}" >&2
    return "${PERMANENT_RC}"
  fi
  if "${cmd}" -c 1 -W "${timeout_s}" "${host}" >/dev/null 2>&1; then
    return 0
  fi
  return 1
}

# retry_with_backoff MAX_ATTEMPTS BASE_DELAY_SECONDS CMD [ARGS...]
# BASE_DELAY_SECONDS is an integer; Bash arithmetic has no floats.
retry_with_backoff() {
  local max_attempts="$1" base_delay="$2"
  shift 2

  local attempt=1
  local rc
  while true; do
    # The rc capture must live in the else branch: with no else, "if
    # false; then ...; fi" itself exits 0, which would discard the real
    # exit code of "$@".
    if "$@"; then
      RETRY_ATTEMPTS="${attempt}"
      return 0
    else
      rc=$?
    fi
    RETRY_ATTEMPTS="${attempt}"

    if [[ "${rc}" -eq "${PERMANENT_RC}" ]]; then
      return "${rc}"
    fi
    if [[ "${attempt}" -ge "${max_attempts}" ]]; then
      return "${rc}"
    fi

    local delay=$(( base_delay * (2 ** (attempt - 1)) ))
    echo "attempt ${attempt}/${max_attempts} failed; retrying in ${delay}s" >&2
    sleep "${delay}"
    attempt=$(( attempt + 1 ))
  done
}

usage() {
  cat <<'EOF' >&2
Usage: 08_retry_backoff.sh --hosts-file PATH --report PATH
                            [--command NAME] [--timeout N]
                            [--max-attempts N] [--base-delay N]
EOF
}

# --- CLI wrapper; skipped when this file is sourced for its functions ---
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  hosts_file=""
  report=""
  cmd="ping"
  timeout_s=2
  max_attempts=4
  base_delay=1

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --hosts-file) hosts_file="${2:-}"; shift 2 ;;
      --report) report="${2:-}"; shift 2 ;;
      --command) cmd="${2:-}"; shift 2 ;;
      --timeout) timeout_s="${2:-}"; shift 2 ;;
      --max-attempts) max_attempts="${2:-}"; shift 2 ;;
      --base-delay) base_delay="${2:-}"; shift 2 ;;
      -h|--help) usage; exit 0 ;;
      *) echo "unknown argument: $1" >&2; usage; exit 1 ;;
    esac
  done

  if [[ -z "${hosts_file}" || -z "${report}" ]]; then
    echo "--hosts-file and --report are required" >&2
    usage
    exit "${EXIT_USAGE}"
  fi

  if [[ ! -f "${hosts_file}" ]]; then
    echo "hosts file not found: ${hosts_file}" >&2
    exit "${EXIT_USAGE}"
  fi

  mkdir -p "$(dirname "${report}")"
  echo "host,ok,attempts,detail" > "${report}"

  had_failure=0
  while IFS= read -r raw || [[ -n "${raw}" ]]; do
    line="$(printf '%s' "${raw}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
    [[ -z "${line}" || "${line}" == \#* ]] && continue

    # retry_with_backoff's return code depends on check_once failing,
    # which would trip "set -e" here if left unguarded; disable it for
    # this call.
    set +e
    retry_with_backoff "${max_attempts}" "${base_delay}" check_once "${line}" "${cmd}" "${timeout_s}"
    rc=$?
    set -e

    if [[ "${rc}" -eq 0 ]]; then
      echo "${line},true,${RETRY_ATTEMPTS},ok" >> "${report}"
    else
      detail="check failed after retrying"
      [[ "${rc}" -eq "${PERMANENT_RC}" ]] && detail="command not found: ${cmd}"
      echo "${line},false,${RETRY_ATTEMPTS},${detail}" >> "${report}"
      echo "host=${line} failed after ${RETRY_ATTEMPTS} attempts" >&2
      had_failure=1
    fi
  done < "${hosts_file}"

  echo "wrote report to ${report}" >&2

  if [[ "${had_failure}" -eq 1 ]]; then
    exit "${EXIT_RUNTIME}"
  fi
  exit "${EXIT_OK}"
fi
