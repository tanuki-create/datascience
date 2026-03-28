#!/usr/bin/env python3
"""500件マージTSVをバケット別レポート（日本語）へ出力。GitHub URL は行から抽出。"""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

DIR = Path(__file__).resolve().parent
MERGED = DIR / "_merged_bookmarks.tsv"
OUT_DIR = DIR / "reports" / "by_bucket_2026-03-28"

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

GH_SLUG = re.compile(
    r"github\.com/([a-zA-Z0-9_.-]+/[a-zA-Z0-9_.\-]+)(?:[\s/:\"'<>]|$)",
    re.I,
)
GH_DASH = re.compile(r"GitHub\s*[-–]\s*([a-zA-Z0-9_.-]+/[a-zA-Z0-9_.\-]+)", re.I)


def bucket(line: str) -> str:
    for name, pat in TAGS:
        if re.search(pat, line, re.I):
            return name
    return "その他・横断"


def extract_github(line: str) -> list[str]:
    out: list[str] = []
    for m in GH_SLUG.finditer(line):
        slug = m.group(1).rstrip("/.")
        if "github.com" in slug.lower():
            continue
        if len(slug) > 3 and "/" in slug:
            out.append(f"https://github.com/{slug}")
    for m in GH_DASH.finditer(line):
        out.append(f"https://github.com/{m.group(1)}")
    return out


def slug_filename(name: str) -> str:
    return re.sub(r"[^\w・\-]", "_", name) + ".md"


def main() -> None:
    lines = [ln.strip() for ln in MERGED.read_text(encoding="utf-8").splitlines() if ln.strip()]
    by_b: dict[str, list[str]] = defaultdict(list)
    gh_by_b: dict[str, set[str]] = defaultdict(set)
    for line in lines:
        b = bucket(line)
        by_b[b].append(line)
        for url in extract_github(line):
            gh_by_b[b].add(url)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    order = [t[0] for t in TAGS] + ["その他・横断"]

    for b in order:
        rows = by_b.get(b, [])
        gh = sorted(gh_by_b.get(b, []))
        # 優先度高め: 公式・研究・ツール名を含む長めの行
        scored = sorted(rows, key=lambda s: (-len(s), s))
        highlights = []
        seen_h = set()
        for s in scored:
            if len(s) < 50:
                continue
            key = s[:120]
            if key in seen_h:
                continue
            seen_h.add(key)
            highlights.append(s)
            if len(highlights) >= 12:
                break

        body = [
            f"# バケットレポート: {b}",
            "",
            f"対象: [`_merged_bookmarks.tsv`](../_merged_bookmarks.tsv) 全行をキーワードルールで分類。**{len(rows)} 件**がこのバケットに該当（1行が複数バケットに載ることはありません: 先にマッチしたタグのみ）。",
            "",
            "## 今あらためて見るべきポイント（抜粋）",
            "",
            "長さ・情報密度が高い行と、公式/製品/研究らしきキーワードを優先して列挙。**一次ソースで更新**してから判断してください。",
            "",
        ]
        for i, h in enumerate(highlights, 1):
            body.append(f"{i}. {h}")
        body += [
            "",
            "## GitHub リポジトリ（行から抽出）",
            "",
        ]
        if gh:
            for u in gh:
                body.append(f"- [{u}]({u})")
        max_k = 30
        body += [
            "",
            f"（{len(gh)} 件。表記ゆれで重複・薄い言及が混じる場合があります。）",
            "",
            "## 示唆・読み方",
            "",
            _blurb_for_bucket(b),
            "",
            "---",
            "",
            f"- 全文500件カタログ: [`bookmarks_500_2026-03-28.md`](../bookmarks_500_2026-03-28.md)",
            f"- 全体分析: [`analysis_500_2026-03-28.md`](../analysis_500_2026-03-28.md)",
            "",
        ]
        (OUT_DIR / slug_filename(b)).write_text("\n".join(body), encoding="utf-8")

    index = [
        "# バケット別レポート（2026-03-28）",
        "",
        "500件マージ（`_merged_bookmarks.tsv`）を **analysis と同じキーワードルール** で分類し、各バケットごとに「再訪の焦点」「GitHub 一覧」「短文の示唆」を置いた。",
        "",
        "## 一覧",
        "",
    ]
    for b in order:
        index.append(f"- [{b}]({slug_filename(b)}) — {len(by_b.get(b, []))} 件")
    index += [
        "",
        "## メモ",
        "",
        "- **バケット**は排他的（先着）で、境界事例は手で別フォルダに振り分けたい場合がある。",
        "- **「見るべき」**は機械的なスコアであり、ブックマークの意図とずれることがある。",
        "",
    ]
    (OUT_DIR / "README.md").write_text("\n".join(index), encoding="utf-8")
    print(f"wrote {OUT_DIR} ({len(order)} reports + README)")


def _blurb_for_bucket(b: str) -> str:
    blurbs = {
        "LLM・エージェント": (
            "**推論コストとコンテキスト**が中心。TurboQuant 系（KV 圧縮・量子化）は自前・端末運用の単価に直結するため、"
            "公式ブログと実装の追従をセットで。RAG / Mythos 等のバズ系は「再現・一次ソース」を確認してから設計に載せるのが安全。"
            "Embedding・ドメイン特化ベクトルは検索品質のレバーなので、HF 記事と社内データの距離感をセットで見直す価値あり。"
        ),
        "コーディングツール": (
            "**エージェントが大規模リポをどう読むか**（Instant Grep 等）と、**マルチエージェントのタスク管理**（Cline Kanban）が実務近い。"
            "Gemini の developer skill は「常に鮮度のある SDK 知識を仕組みで渡す」パターンの参考。**linter 論**は自動生成が進んでも設計境界で効くかどうかの整理に使える。"
        ),
        "音声・音楽・TTS": (
            "**Flash Live**・**Lyria**・**Transcribe** と、音声 UX（双方向・割り込み）の噂・発表が並ぶ。"
            "プロダクトに音声を載せるなら、遅延・失敗モード・ライセンスの三角で整理してから深掘り。"
        ),
        "画像・動画・VLM": (
            "**プロンプト資産**（例: Nano-Banana 系）、**VLM/動画パイプライン**（moondream 等）、同人・販路向けの **レイヤ分解・Live2D** が混在。"
            "制作アトリエ寄りとメディア生成API寄りでスタックが変わるので、自分の用途に寄せて再スクリーニング。"
        ),
        "日本・政策・メディア": (
            "**行政クラウド**・**国内 LLM 記事**・**防衛/産業**ニュース・**OCR/NDL** 系が塊。"
            "リスク・調達・日本語データ管轄の観点で「政策インフラ」を追う場合の入口になりやすい。"
        ),
        "起業・プロダクト": (
            "**MVP 論争**・**PG の戒律**・**ニッチ収益**・**面接**など、意思決定の言語化が多い。"
            "ツールが進んでも「何を作るか・誰に刺すか」がボトルネックになる、という仮説の検証材料として読み返す価値がある。"
        ),
        "社会・労働・健康": (
            "**資本主義と AI**の長文考察、**認知負荷（brain fry）**、インフラ信頼（S3/SOC2）など、短期開発と無縁に見えて**組織・倫理・運用**に効く話題。"
        ),
        "SNS・コミュニティ": (
            "**新SNS**・**超大バズ**・コミュニティ製品の話。伸び方と持続の両方を分けて読むとブックマークの意図が整理しやすい。"
        ),
        "その他・横断": (
            "どのキーワードにも強く当たらなかった行。**表の片側だけ**・**短いラベル**が多い。"
            "定期的にここを人間が眺めて、新しいタグルールを足すか、bucket に昇格させるのがよい。"
        ),
    }
    return blurbs.get(b, "（概要未設定）")


if __name__ == "__main__":
    main()
