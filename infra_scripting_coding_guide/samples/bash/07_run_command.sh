#!/usr/bin/env bash
# Run an external command safely: argument array, timeout, no eval.
#
# Exit codes: 0 ok, 1 command not found, 2 non-zero exit, 4 timeout.
set -euo pipefail

EXIT_OK=0
EXIT_COMMAND_NOT_FOUND=1
EXIT_NONZERO=2
EXIT_TIMEOUT=4

# Portable stand-in for GNU `timeout`, which is absent from a default
# macOS install. Mirrors its exit-code convention: 124 on timeout.
portable_timeout() {
  local secs="$1"
  shift
  local timedout_flag
  timedout_flag="$(mktemp)"
  rm -f "${timedout_flag}"

  "$@" &
  local cmd_pid=$!

  (
    sleep "${secs}"
    if kill -0 "${cmd_pid}" 2>/dev/null; then
      : > "${timedout_flag}"
      kill -TERM "${cmd_pid}" 2>/dev/null
    fi
  ) &
  local watcher_pid=$!

  local rc
  wait "${cmd_pid}" 2>/dev/null
  rc=$?

  # Stop the watcher if the command finished on its own; harmless if it
  # already exited.
  kill "${watcher_pid}" 2>/dev/null || true
  wait "${watcher_pid}" 2>/dev/null || true

  if [[ -f "${timedout_flag}" ]]; then
    rm -f "${timedout_flag}"
    return 124
  fi
  rm -f "${timedout_flag}"
  return "${rc}"
}

# Uses the system `timeout` if present (most Linux distributions),
# otherwise falls back to the portable implementation above.
run_with_timeout() {
  local secs="$1"
  shift
  if command -v timeout >/dev/null 2>&1; then
    timeout "${secs}" "$@"
  else
    portable_timeout "${secs}" "$@"
  fi
}

# run_command TIMEOUT_SECONDS CMD [ARGS...]
# Prints the command's stdout on stdout, diagnostics on stderr, and
# returns one of the EXIT_* codes above.
run_command() {
  local timeout_s="$1"
  shift
  if [[ $# -eq 0 ]]; then
    echo "run_command: no command given" >&2
    return "${EXIT_COMMAND_NOT_FOUND}"
  fi

  local cmd="$1"
  if ! command -v "${cmd}" >/dev/null 2>&1; then
    echo "command not found: ${cmd}" >&2
    return "${EXIT_COMMAND_NOT_FOUND}"
  fi

  local stderr_file
  stderr_file="$(mktemp)"
  local rc
  # Never build a shell string from "$@"; pass the argument array directly.
  # The rc capture must live in the else branch: with no else, "if false;
  # then ...; fi" itself exits 0, which would silently discard the real
  # exit code of run_with_timeout.
  if run_with_timeout "${timeout_s}" "$@" 2>"${stderr_file}"; then
    rm -f "${stderr_file}"
    return "${EXIT_OK}"
  else
    rc=$?
  fi

  local stderr_content
  stderr_content="$(cat "${stderr_file}")"
  rm -f "${stderr_file}"

  if [[ "${rc}" -eq 124 ]]; then
    echo "timed out after ${timeout_s}s" >&2
    return "${EXIT_TIMEOUT}"
  fi

  [[ -n "${stderr_content}" ]] && echo "${stderr_content}" >&2
  return "${EXIT_NONZERO}"
}

# --- CLI wrapper; skipped when this file is sourced for its functions ---
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  timeout_s=10
  args=()

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --timeout) timeout_s="${2:-}"; shift 2 ;;
      --) shift; args=("$@"); break ;;
      *) args=("$@"); break ;;
    esac
  done

  if [[ ${#args[@]} -eq 0 ]]; then
    echo "Usage: 07_run_command.sh [--timeout N] -- CMD [ARGS...]" >&2
    exit "${EXIT_COMMAND_NOT_FOUND}"
  fi

  run_command "${timeout_s}" "${args[@]}"
  exit $?
fi
