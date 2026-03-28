#!/usr/bin/env python3
"""Parse a Cursor/browser accessibility snapshot YAML; print ref ids for 「さらに表示」 buttons."""
from __future__ import annotations

import re
import sys
from pathlib import Path


def refs_from_snapshot(text: str) -> list[str]:
    return re.findall(r"\n      name: さらに表示\n      ref: (e\d+)", text)


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if not path or not path.is_file():
        print("usage: extract_show_more_refs.py <snapshot.yaml>", file=sys.stderr)
        sys.exit(1)
    text = path.read_text(encoding="utf-8", errors="replace")
    for r in refs_from_snapshot(text):
        print(r)


if __name__ == "__main__":
    main()
