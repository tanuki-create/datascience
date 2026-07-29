#!/usr/bin/env python3
"""opsctl向けの共通JSONロギングヘルパー。

各サブコマンドの先頭で configure_json_logging() を呼び、実行ID付きの
JSONログを標準エラーへ出す。ファイル出力を指定するとサイズ基準で
ローテーションする。

このスクリプトを直接実行すると、デモとしてログを出力する。
"""
from __future__ import annotations

import json
import logging
import re
import sys
import uuid
from logging.handlers import RotatingFileHandler
from pathlib import Path

_SECRET_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"(?i)(authorization\s*:\s*)(.+)"),
    re.compile(r"(?i)\b(token=)([^&\s]+)"),
    re.compile(r"(?i)\b(password=)([^&\s]+)"),
    re.compile(r"(?i)\b(api[_-]?key=)([^&\s]+)"),
]


def mask_secrets(message: str) -> str:
    """既知の秘密情報パターンを ``***`` へ置き換える。

    完全な検出は保証できない。ログに渡す前に、そもそも秘密情報を
    メッセージへ含めない設計を優先すること。
    """
    masked = message
    for pattern in _SECRET_PATTERNS:
        masked = pattern.sub(lambda m: f"{m.group(1)}***", masked)
    return masked


class JsonFormatter(logging.Formatter):
    def __init__(self, run_id: str) -> None:
        super().__init__()
        self.run_id = run_id

    def format(self, record: logging.LogRecord) -> str:
        message = mask_secrets(record.getMessage())
        payload: dict[str, object] = {
            "ts": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "run_id": self.run_id,
            "event": record.name,
            "message": message,
        }
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


def configure_json_logging(
    logger_name: str,
    *,
    verbose: bool = False,
    quiet: bool = False,
    log_file: Path | None = None,
) -> tuple[logging.Logger, str]:
    if verbose and quiet:
        raise ValueError("verbose and quiet are mutually exclusive")

    run_id = str(uuid.uuid4())
    logger = logging.getLogger(logger_name)
    logger.handlers.clear()  # 二重呼び出しで行が重複するのを防ぐ
    logger.propagate = False

    if quiet:
        level = logging.WARNING
    elif verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO
    logger.setLevel(level)

    formatter = JsonFormatter(run_id)

    stream_handler = logging.StreamHandler(stream=sys.stderr)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            log_file, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger, run_id


def main() -> int:
    logger, run_id = configure_json_logging(
        "opsctl.demo", verbose=True, log_file=Path("work/logs/demo.log")
    )
    logger.info("run started")
    logger.debug("connecting host=web01.example.invalid")
    logger.warning("Authorization: Bearer sk-do-not-log-this-value")
    logger.error("host unreachable host=web02.example.invalid")
    logger.info("run finished run_id=%s", run_id)
    return 0


if __name__ == "__main__":
    sys.exit(main())
