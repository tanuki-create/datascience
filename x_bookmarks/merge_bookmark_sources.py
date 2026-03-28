#!/usr/bin/env python3
"""Merge bookmark text from repo markdown/tsv into one deduped list (unique keys)."""
from __future__ import annotations

import glob
import re
from pathlib import Path

DIR = Path(__file__).resolve().parent
TSV = DIR / "_parsed_bookmarks.tsv"
DIGEST = DIR / "bookmarks_digest_with_points.md"
BOOKMARKS_2026 = DIR / "bookmarks_2026-03-28.md"
SCROLL50 = DIR / "scroll_50_session.md"
EXTENDED = DIR / "bookmarks_extended_2026-03-28.md"
KEY_POINTS = DIR / "bookmarks_key_points.md"
CATEGORIES = DIR / "categories_summary.md"
EXTRA_NAMES = DIR / "snapshot_dumps" / "extra_link_names.txt"


def norm(s: str) -> str:
    return " ".join(s.strip().split())[:480]


def from_tsv() -> list[str]:
    if not TSV.is_file():
        return []
    return [ln.strip() for ln in TSV.read_text(encoding="utf-8").splitlines() if ln.strip()]


def from_digest() -> list[str]:
    if not DIGEST.is_file():
        return []
    text = DIGEST.read_text(encoding="utf-8")
    out: list[str] = []
    for m in re.finditer(r"\*\*原文断片\*\*:\s*(.+?)(?=\n\n|\Z)", text, re.DOTALL):
        raw = m.group(1).strip()
        raw = re.sub(r"\n\s*-\s+", " ", raw)
        if raw:
            out.append(raw)
    for m in re.finditer(r"\*\*要約\*\*:\s*(.+)$", text, re.MULTILINE):
        raw = m.group(1).strip()
        if raw and len(raw) >= 12:
            out.append(raw)
    return out


def from_bookmarks_2026() -> list[str]:
    if not BOOKMARKS_2026.is_file():
        return []
    text = BOOKMARKS_2026.read_text(encoding="utf-8")
    out: list[str] = []
    for m in re.finditer(r"^##\s+\d+\.\s+(.+)$", text, re.MULTILINE):
        title = m.group(1).strip()
        if title:
            out.append(title)
    for m in re.finditer(r"^\-\s+\*\*要約\*\*:\s*(.+)$", text, re.MULTILINE):
        out.append(m.group(1).strip())
    for m in re.finditer(r"^\-\s+\*\*リンク[^*]*\*\*:\s*(.+)$", text, re.MULTILINE):
        out.append(m.group(1).strip())
    for m in re.finditer(r"^\-\s+\*\*話題\*\*:\s*(.+)$", text, re.MULTILINE):
        out.append(m.group(1).strip())
    for m in re.finditer(r"^\-\s+\*\*要覧\*\*:\s*(.+)$", text, re.MULTILINE):
        out.append(m.group(1).strip())
    return out


def from_table_cells_individual(paths: list[Path]) -> list[str]:
    """2列マークダウン表の各セルを別エントリとしても取り込む（500件寄せ・要確認）。"""
    out: list[str] = []
    row_re = re.compile(r"^\|([^|]+)\|([^|]+)\|\s*$")
    skip_a = {"---", "手がかり", "トピック", "投稿", "#", "----------", ""}
    skip_b = {"要点", "メモ", "---", ""}
    for path in paths:
        if not path.is_file():
            continue
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            m = row_re.match(line.strip())
            if not m:
                continue
            a, b = m.group(1).strip(), m.group(2).strip()
            if a in skip_a or "----" in a:
                continue
            if b in skip_b or "----" in b:
                continue
            if len(a) >= 18:
                out.append(a)
            if len(b) >= 22:
                out.append(b)
    return out


def from_markdown_tables(paths: list[Path]) -> list[str]:
    out: list[str] = []
    row_re = re.compile(r"^\|([^|]+)\|([^|]+)\|\s*$")
    for path in paths:
        if not path.is_file():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            m = row_re.match(line.strip())
            if not m:
                continue
            a, b = m.group(1).strip(), m.group(2).strip()
            if not a or not b:
                continue
            if a.startswith("---") or b.startswith("---"):
                continue
            low = (a + b).lower()
            if "手がかり" in a and "メモ" in b:
                continue
            if "トピック" in a and "要点" in b:
                continue
            if a == "投稿" and b == "要点":
                continue
            if "----------" in a:
                continue
            sep = " — " if b else ""
            cell = f"{a}{sep}{b}".strip()
            if len(cell) >= 8:
                out.append(cell)
    return out


def from_all_markdown_bullets() -> list[str]:
    """全 *.md から 要約/原文/リンク の行を拾う（重複は norm で落ちる）。"""
    out: list[str] = []
    for path in sorted(DIR.glob("*.md")):
        if path.name.startswith("_"):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for m in re.finditer(r"^\-\s+\*\*要約\*\*:\s*(.+)$", text, re.MULTILINE):
            raw = m.group(1).strip()
            if len(raw) >= 12:
                out.append(raw)
        for m in re.finditer(r"^\-\s+\*\*原文[^*]*\*\*:\s*(.+)$", text, re.MULTILINE):
            raw = m.group(1).strip()
            if len(raw) >= 12:
                out.append(raw)
        for m in re.finditer(
            r"^\-\s+\*\*リンク[^*]*\*\*:\s*(.+)$", text, re.MULTILINE
        ):
            raw = m.group(1).strip()
            if len(raw) >= 10:
                out.append(raw)
    return out


def from_markdown_at_lines() -> list[str]:
    """各 .md 内の @ または http を含む長めの行（表・箇条書きの実投稿断片）。"""
    out: list[str] = []
    for path in sorted(DIR.glob("*.md")):
        if path.name.startswith("_"):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for line in text.splitlines():
            s = line.strip()
            s = re.sub(r"^[\-\*\+]\s+", "", s)
            s = re.sub(r"^\d+\.\s+", "", s)
            if len(s) < 28:
                continue
            if "@" not in s and "http" not in s.lower():
                continue
            if s.startswith("|"):
                continue
            lab = re.match(r"^\*\*(?:要約|原文断片|原文)\*\*:\s*(.+)", s)
            if lab:
                s = lab.group(1).strip()
            elif re.match(r"^\*\*(断片|URL|日付|操作|ビュー)", s):
                continue
            if s.startswith("#"):
                continue
            if s.startswith("**日付") or s.startswith("**取得方法"):
                continue
            out.append(s)
    return out


def from_extra_link_names() -> list[str]:
    """ブラウザでフォルダ巡回時に追記した 1 行 1 リンク断片。"""
    if not EXTRA_NAMES.is_file():
        return []
    out: list[str] = []
    for ln in EXTRA_NAMES.read_text(encoding="utf-8", errors="replace").splitlines():
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        s = re.sub(r"^\[FOLDER:[^\]]+\]\s*", "", s)
        if len(s) >= 12:
            out.append(s)
    return out


def from_keypoints_numbered_rows() -> list[str]:
    """bookmarks_key_points.md の | # | 投稿 | 要点 | 形式。"""
    if not KEY_POINTS.is_file():
        return []
    out: list[str] = []
    for m in re.finditer(r"^\| (\d+) \| ([^|]+) \| (.+) \|$", KEY_POINTS.read_text(encoding="utf-8"), re.MULTILINE):
        if m.group(2).strip().startswith("---") or m.group(2).strip() == "投稿":
            continue
        a, b = m.group(2).strip(), m.group(3).strip()
        if len(a) + len(b) > 20:
            out.append(f"{a} — {b}")
    return out


def from_categories_summary() -> list[str]:
    """カテゴリまとめの具体度高めの箇条書き（短すぎる話題ラベルは除外）。"""
    if not CATEGORIES.is_file():
        return []
    text = CATEGORIES.read_text(encoding="utf-8", errors="replace")
    out: list[str] = []
    for m in re.finditer(r"^\- \*\*([^*]+)\*\*(.+)$", text, re.MULTILINE):
        rest = m.group(2).strip()
        if len(rest) < 4:
            continue
        line = f"{m.group(1).strip()}{rest}".strip()
        if len(line) >= 14:
            out.append(line)
    for m in re.finditer(r"^\- (.+)$", text, re.MULTILINE):
        line = m.group(1).strip()
        if line.startswith("**") or len(line) < 15:
            continue
        if re.match(r"^\d+\.\s+", line):
            continue
        if line.startswith("または ") or line.startswith("ブックマーク一覧"):
            continue
        out.append(line)
    return out


def from_catalog_exports() -> list[str]:
    """bookmarks_*_*.md のフルテキスト/断片行（過去ビルドの再取り込み用）。"""
    out: list[str] = []
    for path in sorted(glob.glob(str(DIR / "bookmarks_*_*.md"))):
        name = Path(path).name
        if name.startswith("bookmarks_extended") or name.startswith("bookmarks_2026"):
            continue
        text = Path(path).read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(
            r"^\-\s+\*\*フルテキスト（取得できた範囲）\*\*:\s*(.+)$", text, re.MULTILINE
        ):
            out.append(m.group(1).strip())
        for m in re.finditer(r"^\-\s+\*\*断片 / ラベル\*\*:\s*(.+)$", text, re.MULTILINE):
            out.append(m.group(1).strip())
    return out


def from_scroll50() -> list[str]:
    if not SCROLL50.is_file():
        return []
    text = SCROLL50.read_text(encoding="utf-8")
    out: list[str] = []
    for m in re.finditer(r"^\d+\.\s+\*\*(.+?)\*\*", text, re.MULTILINE):
        out.append(m.group(1).strip())
    for m in re.finditer(r"^\d+\.\s+([^\n*].+)$", text, re.MULTILINE):
        line = m.group(1).strip()
        if line and not line.startswith("**"):
            out.append(line)
    return out


def main() -> None:
    seen: set[str] = set()
    merged: list[str] = []
    for src in (
        from_tsv(),
        from_digest(),
        from_bookmarks_2026(),
        from_scroll50(),
        from_markdown_tables([EXTENDED, KEY_POINTS]),
        from_table_cells_individual([EXTENDED, KEY_POINTS]),
        from_catalog_exports(),
        from_categories_summary(),
        from_keypoints_numbered_rows(),
        from_all_markdown_bullets(),
        from_extra_link_names(),
        from_markdown_at_lines(),
    ):
        for item in src:
            k = norm(item)
            if not k or k in seen:
                continue
            seen.add(k)
            merged.append(item)
    print(f"unique={len(merged)}")
    out_path = DIR / "_merged_bookmarks.tsv"
    out_path.write_text("\n".join(merged), encoding="utf-8")
    print(f"-> {out_path}")


if __name__ == "__main__":
    main()
