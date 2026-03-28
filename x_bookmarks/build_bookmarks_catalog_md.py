#!/usr/bin/env python3
"""Build bookmarks_{N}_YYYY-MM-DD.md and analysis_{N}_... from _merged_bookmarks.tsv."""
from __future__ import annotations

import argparse
import re
from collections import Counter
from datetime import date
from pathlib import Path

DIR = Path(__file__).resolve().parent
MERGED = DIR / "_merged_bookmarks.tsv"

TAGS = [
    ("LLM・エージェント", r"LLM|GPT|Claude|Gemini|RAG|embedding|TurboQuant|量子化|エージェント|Codex|skill"),
    ("コーディングツール", r"Cursor|Cline|GitHub|TypeScript|linter|grep|ワークツリー"),
    ("音声・音楽・TTS", r"音声|Lyria|Flash Live|Transcribe|文字起こし|TTS|ボイス|bidirectional"),
    ("画像・動画・VLM", r"画像|動画|moondream|Live2D|ピクセル|プロンプト|Nano-Banana|VLM"),
    ("日本・政策・メディア", r"デジタル庁|ITmedia|GIGAZINE|国会図書館|PLaMo|国産|防衛|ATLA|トヨタ"),
    ("起業・プロダクト", r"MVP|Paul Graham|ニッチ|収益|起業|資金調達|面接|Karpathy|個人開発"),
    ("社会・労働・健康", r"資本主義|労働|認知|brain fry|睡眠|iPad|S3|SOC2"),
    ("SNS・コミュニティ", r"SNS|Karotter|Meadow|フォロワ|バズ"),
]


def summarize(line: str) -> str:
    s = line.strip()
    if " — " in s:
        left, right = s.split(" — ", 1)
        a, b = left.strip(), right.strip()
        b = re.sub(r"\*\*([^*]+)\*\*", r"\1", b)
        if len(b) > 220:
            b = b[:217] + "…"
        return f"「{a}」に関するメモ: {b}"
    s = re.sub(r"\*\*([^*]+)\*\*", r"\1", s)
    if len(s) > 240:
        return s[:237] + "…"
    return s


def bucket(line: str) -> str:
    for name, pat in TAGS:
        if re.search(pat, line, re.I):
            return name
    return "その他・横断"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=500)
    ap.add_argument("--date", type=str, default="2026-03-28")
    args = ap.parse_args()
    target = max(1, args.limit)
    d = args.date

    lines = [ln.strip() for ln in MERGED.read_text(encoding="utf-8").splitlines() if ln.strip()]
    top = lines[:target]
    rest = len(lines) - target

    cats = Counter(bucket(x) for x in top)
    out_list = DIR / f"bookmarks_{target}_{d}.md"
    out_an = DIR / f"analysis_{target}_{d}.md"

    list_parts: list[str] = [
        f"# X ブックマーク {target} 件カタログ（{d}）",
        "",
        "出所: [`_parsed_bookmarks.tsv`](_parsed_bookmarks.tsv)、各種 `.md`、表のセル分割、フォルダ巡回の `snapshot_dumps/extra_link_names.txt` などを **`merge_bookmark_sources.py`** でマージした "
        f"[`_merged_bookmarks.tsv`](_merged_bookmarks.tsv) の **先頭 {target} 件**。"
        "**フルテキスト**列はアクセシビリティツリー上の **link name**（「さらに表示」クリック後に長くなることがある）を主にしており、"
        "公式 API の全文・常に末尾まで揃う保証はありません。",
        "",
        "**注意**: 仮想スクロールでタイムライン全体を連続取得できません。公式のデータダウンロード（bookmarks JSON）との突合で完全性を担保してください。",
        "",
        f"マージ全体のユニーク件数: **{len(lines)}**（掲載 {min(target, len(lines))} 件。残りは `_merged_bookmarks.tsv` の末尾を参照）。",
        "",
        f"関連: [bookmarks_key_points.md](bookmarks_key_points.md)、[analysis_{target}_{d}.md](analysis_{target}_{d}.md)。",
        "",
        "---",
        "",
    ]

    for i, raw in enumerate(top, 1):
        sumry = summarize(raw)
        list_parts.append(f"## {i}")
        list_parts.append("")
        list_parts.append(f"- **フルテキスト（取得できた範囲）**: {raw}")
        list_parts.append(f"- **要点**: {sumry}")
        list_parts.append("")

    out_list.write_text("\n".join(list_parts), encoding="utf-8")

    total = sum(cats.values())
    analysis_lines = [
        f"# ブックマーク {target} 件の分析（{d}）",
        "",
        f"対象: [`bookmarks_{target}_{d}.md`](bookmarks_{target}_{d}.md) の先頭 **{target} 件**。"
        "分類はキーワード一致による **近似ラベリング**（先にマッチしたタグのみ）。",
        "",
        "## 件数の目安（キーワード・バケット）",
        "",
        "| バケット | 件数 | 割合 |",
        "|----------|-----:|-----:|",
    ]
    for name, _pat in TAGS + [("その他・横断", "")]:
        c = cats.get(name, 0)
        pct = 100.0 * c / total if total else 0
        analysis_lines.append(f"| {name} | {c} | {pct:.1f}% |")

    analysis_lines += [
        "",
        "## 読み取り",
        "",
        "- 件数が増えるほど **ツール・モデル・メディア周り**と **個人開発／プロダクト論**の比率が伸びやすい（保存行動の偏り）。",
        "- **日本語・国内メディア・行政**の行はクラスタとして埋まり、英語ポストの **引用チェーン**と共存する。",
        "",
        "## 限界",
        "",
        "- **同一トピック**が「表の要約行」と「リンク断片」で二重にカウントされる場合がある。",
        "- **500 件未満**のときは `snapshot_dumps/*.yaml` を増やし "
        "`parse_bookmark_snapshots.py` → `merge_bookmark_sources.py` → 本スクリプトを再実行。",
        "",
    ]
    out_an.write_text("\n".join(analysis_lines), encoding="utf-8")
    print(f"wrote {out_list} and {out_an} (merged_total={len(lines)})")


if __name__ == "__main__":
    main()
