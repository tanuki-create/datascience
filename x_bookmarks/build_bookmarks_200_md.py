#!/usr/bin/env python3
"""Build bookmarks_200_2026-03-28.md and analysis_200_2026-03-28.md from _merged_bookmarks.tsv."""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

DIR = Path(__file__).resolve().parent
MERGED = DIR / "_merged_bookmarks.tsv"
OUT_LIST = DIR / "bookmarks_200_2026-03-28.md"
OUT_ANALYSIS = DIR / "analysis_200_2026-03-28.md"
TARGET = 200

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
    lines = [ln.strip() for ln in MERGED.read_text(encoding="utf-8").splitlines() if ln.strip()]
    top = lines[:TARGET]
    rest = len(lines) - TARGET

    cats = Counter(bucket(x) for x in top)

    list_parts: list[str] = [
        "# X ブックマーク 200 件カタログ（2026-03-28）",
        "",
        "出所: ブラウザスナップショット由来の [`_parsed_bookmarks.tsv`](_parsed_bookmarks.tsv) と、"
        "リポジトリ内の一覧・要点表・拡張メモを **`merge_bookmark_sources.py`** で重複除去マージした [`_merged_bookmarks.tsv`](_merged_bookmarks.tsv) の **先頭 200 件**。",
        "",
        "**注意**: X は仮想スクロールのため、タイムライン上ですべてのブックマークを連続取得できず、同一トピックの **カテゴリ要約行** と **原文断片行** が両方入っている場合があります。",
        "",
        f"マージ全体のユニーク件数: **{len(lines)}**（このファイルでは最大 {TARGET} 件を掲載。残り {max(rest, 0)} 件は TSV を参照）。",
        "",
        "関連: [bookmarks_key_points.md](bookmarks_key_points.md)（トピック別の読み物レベル要点）、"
        "[analysis_200_2026-03-28.md](analysis_200_2026-03-28.md)（200 件の偏り分析）。",
        "",
        "---",
        "",
    ]

    for i, raw in enumerate(top, 1):
        sumry = summarize(raw)
        list_parts.append(f"## {i}")
        list_parts.append("")
        list_parts.append(f"- **断片 / ラベル**: {raw}")
        list_parts.append(f"- **要点**: {sumry}")
        list_parts.append("")

    OUT_LIST.write_text("\n".join(list_parts), encoding="utf-8")

    total = sum(cats.values())
    analysis_lines = [
        "# ブックマーク 200 件の分析（2026-03-28）",
        "",
        "対象: [`bookmarks_200_2026-03-28.md`](bookmarks_200_2026-03-28.md) に列挙した **先頭 200 件**。"
        "分類はキーワード一致による **近似ラベリング**（複数に該当しうるが、先にマッチしたタグのみ集計）。",
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
        "- **AI・開発基盤**（LLM、エージェント、量子化、コーディング IDE）と **マルチメディア系**（音声・画像）の行が多く、フォルダ上の「LLM」「画像生成」「研究」タブと整合的。",
        "- **日本語ソース**（メディア、行政、国内 LLM、製造業コメント）がまとまっており、英語圏の界隈ネタと **ほぼ半々ではないまでも一定分量**ある。",
        "- **起業・個人開発・キャリア**（PG、MVP 論、iOS ニッチ、習慣系アプリ収益）が塊として存在し、「kaggel, ML」より **プロダクト志向の保存**が目立つ。",
        "- **マクロ・労働・健康**は件数は少なめだが、ブックマークの **保存動機が長期視点**のものとして浮きやすい。",
        "",
        "## 限界",
        "",
        "- 200 件中に **同一トピックの要約行と引用行**が別エントリとして残る場合がある（マージ方針のため）。深掘り時はキーワードでグルーピングするとよい。",
        "- **仮想スクロール未取得**の投稿はこのカタログに含まれない。追補は `snapshot_dumps/` にスナップショット YAML を追加して `parse_bookmark_snapshots.py` → `merge_bookmark_sources.py` → 本ビルドを再実行。",
        "",
    ]
    OUT_ANALYSIS.write_text("\n".join(analysis_lines), encoding="utf-8")
    print(f"wrote {OUT_LIST} and {OUT_ANALYSIS}")


if __name__ == "__main__":
    main()
