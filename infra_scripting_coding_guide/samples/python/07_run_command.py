#!/usr/bin/env python3
"""Run an external command safely: argument list, timeout, no shell=True.

Distinguishes command-not-found, non-zero exit, and timeout with
different exit codes so callers can react appropriately.
"""
from __future__ import annotations

import argparse
import logging
import shutil
import subprocess
import sys
from dataclasses import dataclass

EXIT_OK = 0
EXIT_COMMAND_NOT_FOUND = 1
EXIT_NONZERO = 2
EXIT_TIMEOUT = 4

logger = logging.getLogger("run_command")


@dataclass
class CommandResult:
    stdout: str
    stderr: str
    returncode: int
    exit_code: int


def run_command(args: list[str], timeout: int) -> CommandResult:
    """Run args (already split, never a shell string) with a timeout."""
    if not args:
        raise ValueError("args must not be empty")

    if shutil.which(args[0]) is None:
        return CommandResult(
            stdout="",
            stderr=f"command not found: {args[0]}",
            returncode=-1,
            exit_code=EXIT_COMMAND_NOT_FOUND,
        )

    try:
        completed = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return CommandResult(
            stdout="",
            stderr=f"timed out after {timeout}s",
            returncode=-1,
            exit_code=EXIT_TIMEOUT,
        )

    exit_code = EXIT_OK if completed.returncode == 0 else EXIT_NONZERO
    return CommandResult(
        stdout=completed.stdout,
        stderr=completed.stderr,
        returncode=completed.returncode,
        exit_code=exit_code,
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run an external command with a timeout and no shell interpretation",
    )
    parser.add_argument("--timeout", type=int, default=10)
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument(
        "command",
        nargs=argparse.REMAINDER,
        help="command and its arguments, e.g. -- ping -c 1 web01.example.invalid",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(message)s",
        stream=sys.stderr,
    )

    command = args.command
    if command and command[0] == "--":
        command = command[1:]

    if not command:
        logger.error("no command given; usage: 07_run_command.py [--timeout N] -- CMD [ARGS...]")
        return EXIT_COMMAND_NOT_FOUND

    result = run_command(command, args.timeout)
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        logger.info("stderr: %s", result.stderr.strip())
    logger.debug("returncode=%s exit_code=%s", result.returncode, result.exit_code)
    return result.exit_code


if __name__ == "__main__":
    sys.exit(main())
