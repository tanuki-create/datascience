#!/usr/bin/env python3
"""opsctl config-patch: 設定ファイルの一括変更（正規表現置換）。

対象ディレクトリ配下の設定ファイル群に、ルールファイル（YAML）で
定義した正規表現置換を適用する。変更前に必ずタイムスタンプ付き
バックアップを取り、一時ファイル経由の原子的な書き込みで上書きする。

--dry-run では、実際の書き込みもバックアップも行わず、変更予定の
差分（unified diff）だけを表示する。ルールの誤りは対象ファイルを
まとめて壊しうるため、必ず --dry-run で差分を確認してから
実行すること。
"""
from __future__ import annotations

import argparse
import csv
import difflib
import fnmatch
import json
import logging
import os
import re
import shutil
import sys
import tempfile
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_RUNTIME = 2

logger = logging.getLogger("opsctl.config_patch")


@dataclass
class PatchRule:
    pattern: str
    replacement: str
    glob: str = "*"

    def compiled(self) -> re.Pattern[str]:
        return re.compile(self.pattern, re.MULTILINE)


@dataclass
class PatchResult:
    path: str
    status: str  # "changed" | "unchanged" | "would_change" | "error"
    detail: str


def load_rules(path: Path) -> list[PatchRule]:
    if yaml is None:
        raise RuntimeError("PyYAML is required to read rules files (pip install PyYAML)")
    if not path.is_file():
        raise FileNotFoundError(f"rules file not found: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"rules file must be a YAML list: {path}")
    rules: list[PatchRule] = []
    for i, item in enumerate(data):
        if not isinstance(item, dict) or "pattern" not in item or "replacement" not in item:
            raise ValueError(f"rule #{i} must have 'pattern' and 'replacement': {item!r}")
        rules.append(PatchRule(pattern=item["pattern"], replacement=item["replacement"], glob=item.get("glob", "*")))
    return rules


def iter_target_files(target_dir: Path, glob: str) -> list[Path]:
    if not target_dir.is_dir():
        raise FileNotFoundError(f"target dir not found: {target_dir}")
    return sorted(p for p in target_dir.rglob("*") if p.is_file() and fnmatch.fnmatch(p.name, glob))


def apply_rules(content: str, rules: list[PatchRule], filename: str) -> str:
    new_content = content
    for rule in rules:
        if not fnmatch.fnmatch(filename, rule.glob):
            continue
        new_content = rule.compiled().sub(rule.replacement, new_content)
    return new_content


def make_backup(path: Path, backup_dir: Path) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup_target = backup_dir / f"{path.name}.{timestamp}.bak"
    shutil.copy2(path, backup_target)
    return backup_target


def atomic_write(path: Path, content: str) -> None:
    fd, tmp_name = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.")
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as fh:
            fh.write(content)
        shutil.copymode(path, tmp_path)
        os.replace(tmp_path, path)
    except BaseException:
        tmp_path.unlink(missing_ok=True)
        raise


def patch_file(path: Path, rules: list[PatchRule], backup_dir: Path, *, dry_run: bool) -> PatchResult:
    try:
        original = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return PatchResult(str(path), "error", f"could not read file: {exc}")

    updated = apply_rules(original, rules, path.name)
    if updated == original:
        return PatchResult(str(path), "unchanged", "no rule matched")

    if dry_run:
        diff = "\n".join(
            difflib.unified_diff(
                original.splitlines(),
                updated.splitlines(),
                fromfile=f"a/{path.name}",
                tofile=f"b/{path.name}",
                lineterm="",
            )
        )
        return PatchResult(str(path), "would_change", diff[:2000])

    try:
        backup = make_backup(path, backup_dir)
        atomic_write(path, updated)
    except OSError as exc:
        return PatchResult(str(path), "error", f"failed to write: {exc}")

    return PatchResult(str(path), "changed", f"backup={backup}")


def write_report(path: Path, results: list[PatchResult]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["path", "status", "detail"])
        writer.writeheader()
        for r in results:
            writer.writerow(asdict(r))


def resolve_report_path(cli_value: Path | None, output_dir_hint: Path) -> Path:
    if cli_value is not None:
        return cli_value
    return output_dir_hint / "config_patch.csv"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="opsctl config-patch: bulk regex-based config file update")
    parser.add_argument("--target-dir", type=Path, required=True)
    parser.add_argument("--rules-file", type=Path, required=True)
    parser.add_argument("--backup-dir", type=Path, default=Path("backups/config-patch"))
    parser.add_argument("--report", type=Path, default=None)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    run_id = str(uuid.uuid4())
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format=f"%(asctime)s %(levelname)s run_id={run_id} %(message)s",
        stream=sys.stderr,
        force=True,
    )

    try:
        rules = load_rules(args.rules_file)
        targets = iter_target_files(args.target_dir, "*")
    except (OSError, ValueError, RuntimeError) as exc:
        logger.error("%s", exc)
        return EXIT_USAGE

    if not rules:
        logger.error("rules file has no rules: %s", args.rules_file)
        return EXIT_USAGE

    report_path = resolve_report_path(args.report, Path("reports"))

    logger.info(
        "applying %s rule(s) to %s candidate file(s) under %s (dry_run=%s)",
        len(rules), len(targets), args.target_dir, args.dry_run,
    )
    if not args.dry_run:
        logger.warning(
            "%s file(s) may be modified. backups will be written to %s before each change.",
            len(targets), args.backup_dir,
        )

    results = [patch_file(p, rules, args.backup_dir, dry_run=args.dry_run) for p in targets]
    write_report(report_path, results)

    changed = [r for r in results if r.status in ("changed", "would_change")]
    errors = [r for r in results if r.status == "error"]

    for r in changed:
        if args.dry_run:
            logger.info("would change %s\n%s", r.path, r.detail)
        else:
            logger.info("changed %s (%s)", r.path, r.detail)
    for r in errors:
        logger.error("failed %s: %s", r.path, r.detail)

    summary = {
        "run_id": run_id,
        "subcommand": "config-patch",
        "total": len(results),
        "changed": len(changed),
        "errors": len(errors),
        "dry_run": args.dry_run,
        "report": str(report_path),
    }
    print(json.dumps(summary))
    logger.info("finished total=%s changed=%s errors=%s", len(results), len(changed), len(errors))
    return EXIT_RUNTIME if errors else EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
