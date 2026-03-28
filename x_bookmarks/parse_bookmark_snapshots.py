#!/usr/bin/env python3
"""Parse Cursor browser snapshot YAML logs from X bookmarks; write deduped lines to _parsed_bookmarks.tsv."""
from __future__ import annotations

import glob
import re
from pathlib import Path

LOG_DIR = Path("/Users/hiromitsu/.cursor/browser-logs")
SNAPSHOT_DUMPS = Path(__file__).resolve().parent / "snapshot_dumps"
OUT = Path(__file__).resolve().parent / "_parsed_bookmarks.tsv"

SKIP_PREFIX = (
    "キーボード", "ホームタイムラインに移動", "トレンドに移動", "調べたいものを検索",
    "通知（", "ダイレクトメッセージ", "SuperGrok", "プレミアム", "クリエイタースタジオ",
    "記事", "プロフィール", "その他のメニュー", "ポストする", "アカウントメニュー",
    "Grokのアクション", "もっと見る", "さらに表示", "件の返信", "件のリポスト",
    "件のいいね", "ブックマークに追加済み",
    "ポストを共有", "メインメニュー", "すべてのブックマーク", "フォルダを作成",
    "戻る", "動画を再生", "プレイ", "ミュート", "音量", "全画面", "ピクチャー",
    "動画の設定", "再生位置", "ミュートを解除", "placeholder",
    "ホームタイムライン", "ブックマークを検索", "キーボードショートカット",
)

NAME_RE = re.compile(r"^\s+name:\s+(.+)$")


def is_noise(t: str) -> bool:
    t = t.strip()
    if "ポストアナリティクスを表示" in t:
        return True
    if len(t) < 15:
        return True
    if t in ("X", "ホーム", "ブックマーク"):
        return True
    for p in SKIP_PREFIX:
        if t.startswith(p):
            return True
    if re.match(r"^@\w+$", t):
        return True
    if re.match(r"^[0-9]+月[0-9]+日$", t):
        return True
    if re.match(r"^[0-9]+ 時間前$", t):
        return True
    if re.match(r"^[0-9]+ 日前$", t):
        return True
    if re.match(r"^20[0-9]{2}年[0-9]+月[0-9]+日$", t):
        return True
    return False


def _has_cjk(s: str) -> bool:
    return any("\u3040" <= c <= "\u30ff" or "\u4e00" <= c <= "\u9fff" for c in s)


def is_candidate(raw: str) -> bool:
    if is_noise(raw):
        return False
    if "@" in raw or "http" in raw.lower():
        return True
    if len(raw) >= 55 and any(c in raw for c in "。、！？・"):
        return True
    if len(raw) >= 70:
        return True
    if _has_cjk(raw) and len(raw) >= 40:
        return True
    return False


def stem_key(raw: str) -> str:
    """Approximate same-post key: strip dates and compress."""
    t = raw.lower()
    t = re.sub(r"\d+ 時間前|\d+ 日前|[0-9]+月[0-9]+日|20[0-9]{2}年[0-9]+月[0-9]+日", " ", t)
    t = " ".join(t.split())[:140]
    return t


def main() -> None:
    paths = sorted(glob.glob(str(LOG_DIR / "snapshot-*.log")), key=lambda p: Path(p).stat().st_mtime)
    if SNAPSHOT_DUMPS.is_dir():
        for p in sorted(glob.glob(str(SNAPSHOT_DUMPS / "*"))):
            if Path(p).suffix.lower() in (".log", ".yaml", ".yml", ".txt") and Path(p).is_file():
                paths.append(p)
        paths.sort(key=lambda p: Path(p).stat().st_mtime)
    # stem -> longest candidate (prefers expanded 「さらに表示」 text)
    best: dict[str, str] = {}
    for path in paths:
        try:
            text = Path(path).read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for line in text.splitlines():
            m = NAME_RE.match(line)
            if not m:
                continue
            raw = m.group(1)
            if raw.startswith('"') and raw.endswith('"'):
                raw = raw[1:-1].replace('\\"', '"')
            if not is_candidate(raw):
                continue
            sk = stem_key(raw)
            prev = best.get(sk)
            if prev is None or len(raw) > len(prev):
                best[sk] = raw

    rows = sorted(best.values(), key=lambda r: (-len(r), r))

    OUT.write_text("\n".join(r.replace("\t", " ") for r in rows), encoding="utf-8")
    print(f"logs={len(paths)} unique={len(rows)} -> {OUT}")


if __name__ == "__main__":
    main()
