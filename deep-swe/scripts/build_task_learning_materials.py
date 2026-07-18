#!/usr/bin/env python3
"""Build learner-facing materials from DeepSWE task prompts."""

from __future__ import annotations

import argparse
import re
import shutil
import textwrap
import tomllib
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
TASKS_DIR = ROOT / "tasks"
OUTPUT_DIR = ROOT / "tasks-learning"
GENERATED_AT = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y-%m-%d %H:%M:%S %Z")


LANGUAGE_NOTES = {
    "go": "Go の課題では、公開 API と内部実装の境界、並行処理、エラー値、既存テストの期待を先に確認します。",
    "python": "Python の課題では、公開 API、例外型、型変換、既存テストのフィクスチャを先に確認します。",
    "typescript": "TypeScript の課題では、型定義、公開 API、ビルド後の出力、既存テストの使われ方を先に確認します。",
    "javascript": "JavaScript の課題では、実行時の挙動、公開 API、型なしコードでの境界条件を先に確認します。",
    "rust": "Rust の課題では、公開型、所有権とライフタイム、エラー型、既存テストの期待を先に確認します。",
}


SPECIAL_BEGINNER_NOTES = {
    "abs-module-cache-flags": """## 例題としての詳しい読み解き

この課題の中心は、`require()` の対象を「文字列として同じか」ではなく「最終的に同じファイルを指すか」で扱うことです。

たとえば、相対パス、絶対パス、`ABS_MODULE_PATH` 経由の探索が混ざると、同じ module file に複数の到達経路が生まれます。
キャッシュキーを入力文字列のままにすると、同じファイルが二重に読み込まれ、状態や副作用が不安定になります。
そのため、この課題では canonical absolute path を基準にして、解決、キャッシュ、表示をそろえる必要があります。

次に見るべき責務は、モジュール探索の順序です。
bare module name は `demo` のように区切りや拡張子を含まない名前で、`demo/index.abs` として探します。
探索順は、現在実行中の ABS ファイルのディレクトリを先に見てから、`ABS_MODULE_PATH` を順番に見ます。
`ABS_MODULE_PATH` の重複排除では、文字列の一致ではなく canonical directory の一致を見る点が読みどころです。

キャッシュ可視化 API は、実装者向けの内部デバッグではなく、ABS の実行環境から呼べる公開機能として扱います。
`require_cache_info()`、`require_cache_keys()`、`reset_require_cache()` は、テストから観測できる公開 API です。
`inflight` は「今まさに読み込みスタック上にあるモジュール」の数なので、通常のキャッシュ済み件数とは別に考えます。

循環 import は、単にエラーにするだけでは足りません。
エラーメッセージが `cyclic module import detected:` で始まり、どの順番で循環したかを含む必要があります。
初心者はここを、グラフアルゴリズムではなく「読み込み中のスタックに同じファイルが再登場したら、そのスタックを表示する」と捉えると理解しやすくなります。

最後に、CLI フラグの扱いはモジュールローダー本体とは責務が違います。
`--module-path` と `--module-debug` は script mode でも効く必要があります。
ただし `BeginRepl(args []string, version string)` の公開シグネチャは保つ必要があります。
この制約は、内部 helper の形は変えてよいが、外から呼ばれる入口は壊さない、という意味です。
""",
}


GENERIC_TERMS = {
    "cache": "キャッシュ",
    "caching": "キャッシュ",
    "stream": "ストリーム",
    "streaming": "ストリーミング",
    "json": "JSON",
    "schema": "スキーマ",
    "query": "クエリ",
    "parser": "パーサ",
    "parsing": "パース",
    "serialization": "シリアライズ",
    "formatting": "フォーマット",
    "routing": "ルーティング",
    "middleware": "ミドルウェア",
    "module": "モジュール",
    "modules": "モジュール",
    "async": "非同期",
    "concurrent": "並行処理",
    "deterministic": "決定的な挙動",
    "incremental": "差分処理",
    "recursive": "再帰",
    "validation": "検証",
    "headers": "ヘッダー",
    "window": "ウィンドウ関数",
}


IDEA_RULES = [
    (
        ("cache", "caching", "persistent"),
        "同じ対象を同じキーや同じ状態として扱い、再利用、無効化、観測結果がぶれないようにすること",
    ),
    (
        ("stream", "streaming", "sse", "iterator", "iteration"),
        "一括処理に寄せず、データを読む順序、消費済み状態、終了条件を公開 API の挙動としてそろえること",
    ),
    (
        ("parser", "parsing", "grammar", "sql", "toml", "html", "xml", "json", "jsonpath"),
        "入力を文字列の例外処理で扱わず、構文要素として解釈して既存の整形や変換規則に組み込むこと",
    ),
    (
        ("schema", "validation", "typed", "dto"),
        "型やスキーマの表現を増やしても、検証、変換、公開される型情報が同じ意味を保つようにすること",
    ),
    (
        ("route", "routing", "middleware", "headers", "http", "fastapi", "response"),
        "HTTP 利用者から見える挙動を、既存のルーティング、レスポンス生成、ミドルウェアの責務に沿って追加すること",
    ),
    (
        ("async", "concurrent", "cancellation", "coalescing", "lifecycle"),
        "非同期処理の開始、待機、キャンセル、後始末を一つのライフサイクルとして扱うこと",
    ),
    (
        ("deterministic", "sorting", "order", "ordered", "priority"),
        "同じ入力から同じ順序の結果が得られるように、比較規則や優先順位を明示的な仕様にすること",
    ),
    (
        ("recursive", "hierarchical", "graph", "dependency", "dependencies"),
        "親子関係や依存関係を局所的な分岐で処理せず、全体の関係をたどれる構造として扱うこと",
    ),
    (
        ("snapshot", "rollback", "replay", "restore"),
        "状態の保存、復元、差分確認を、実行時の一時的な副作用ではなく明示的な操作として扱うこと",
    ),
    (
        ("cli", "flag", "config"),
        "設定や CLI オプションを入口だけで処理せず、実際の実行経路まで一貫して伝えること",
    ),
]


@dataclass(frozen=True)
class Task:
    task_id: str
    language: str
    category: str
    title: str
    description: str
    repository_url: str
    base_commit_hash: str
    instruction: str
    solution_patch: str
    test_patch: str


def load_task(task_dir: Path) -> Task:
    metadata = tomllib.loads((task_dir / "task.toml").read_text(encoding="utf-8"))
    meta = metadata.get("metadata", {})
    return Task(
        task_id=task_dir.name,
        language=str(meta.get("language", "")).lower(),
        category=str(meta.get("category", "")),
        title=str(meta.get("display_title") or meta.get("original_title") or task_dir.name),
        description=str(meta.get("display_description") or ""),
        repository_url=str(meta.get("repository_url") or ""),
        base_commit_hash=str(meta.get("base_commit_hash") or ""),
        instruction=(task_dir / "instruction.md").read_text(encoding="utf-8").strip() + "\n",
        solution_patch=(task_dir / "solution" / "solution.patch").read_text(encoding="utf-8"),
        test_patch=(task_dir / "tests" / "test.patch").read_text(encoding="utf-8"),
    )


def load_tasks() -> list[Task]:
    tasks: list[Task] = []
    for task_dir in sorted(TASKS_DIR.iterdir()):
        if not task_dir.is_dir():
            continue
        if (task_dir / "instruction.md").exists() and (task_dir / "task.toml").exists():
            tasks.append(load_task(task_dir))
    return tasks


def compact_line(line: str, limit: int = 180) -> str:
    line = re.sub(r"\s+", " ", line).strip()
    if len(line) <= limit:
        return line
    return line[: limit - 1].rstrip() + "..."


def clean_added_line(line: str) -> str:
    line = line[1:] if line.startswith("+") else line
    return line.rstrip()


def first_paragraph(text: str) -> str:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]
    return compact_line(paragraphs[0]) if paragraphs else ""


def notable_requirements(text: str, limit: int = 8) -> list[str]:
    lines: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("IMPORTANT:"):
            continue
        if re.match(r"^(Expected outcomes|Implementation notes|IMPORTANT)", line, re.I):
            continue
        if re.match(r"^#{1,6}\s+", line) or re.match(r"^\d+\.\s+", line) or line.startswith("- "):
            normalized = re.sub(r"^#{1,6}\s+", "", line)
            normalized = re.sub(r"^\d+\.\s+", "", normalized)
            normalized = re.sub(r"^-\s+", "", normalized)
            lines.append(compact_line(normalized))
        if len(lines) >= limit:
            break
    return lines


def first_unique(items: list[str], limit: int) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        normalized = item.strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        result.append(normalized)
        if len(result) >= limit:
            break
    return result


def parse_patch_files(patch: str) -> list[dict[str, object]]:
    files: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    for raw in patch.splitlines():
        if raw.startswith("diff --git "):
            parts = raw.split()
            path = parts[-1][2:] if len(parts) >= 4 and parts[-1].startswith("b/") else parts[-1]
            current = {"path": path, "additions": 0, "deletions": 0, "contexts": []}
            files.append(current)
            continue
        if current is None:
            continue
        if raw.startswith("@@"):
            context = raw.split("@@")[-1].strip()
            if context:
                current["contexts"].append(compact_line(context, 90))
            continue
        if raw.startswith("+++") or raw.startswith("---"):
            continue
        if raw.startswith("+"):
            current["additions"] = int(current["additions"]) + 1
        elif raw.startswith("-"):
            current["deletions"] = int(current["deletions"]) + 1
    return files


def patch_file_bullets(files: list[dict[str, object]], limit: int = 8) -> str:
    if not files:
        return "- 参照解答の変更ファイルを検出できませんでした。"
    top_files = sorted(
        files,
        key=lambda item: int(item["additions"]) + int(item["deletions"]),
        reverse=True,
    )[:limit]
    bullets = []
    for item in top_files:
        path = str(item["path"])
        additions = int(item["additions"])
        deletions = int(item["deletions"])
        contexts = first_unique(list(item["contexts"]), 2)
        context_text = f"。主な文脈は `{'; '.join(contexts)}` です" if contexts else ""
        bullets.append(f"- `{path}`：追加 {additions} 行、削除 {deletions} 行{context_text}。")
    return "\n".join(bullets)


def extract_symbols(patch: str, limit: int = 14) -> list[str]:
    patterns = [
        r"^\+\s*(?:export\s+)?(?:async\s+)?function\s+([A-Za-z_][A-Za-z0-9_]*)",
        r"^\+\s*(?:export\s+)?(?:const|let|var)\s+([A-Za-z_][A-Za-z0-9_]*)\s*[=:]",
        r"^\+\s*(?:export\s+)?(?:class|interface|type)\s+([A-Za-z_][A-Za-z0-9_]*)",
        r"^\+\s*def\s+([A-Za-z_][A-Za-z0-9_]*)",
        r"^\+\s*class\s+([A-Za-z_][A-Za-z0-9_]*)",
        r"^\+\s*func\s+(?:\([^)]+\)\s*)?([A-Za-z_][A-Za-z0-9_]*)",
        r"^\+\s*(?:pub\s+)?(?:async\s+)?fn\s+([A-Za-z_][A-Za-z0-9_]*)",
        r"^\+\s*(?:pub\s+)?(?:struct|enum|trait)\s+([A-Za-z_][A-Za-z0-9_]*)",
    ]
    symbols: list[str] = []
    for line in patch.splitlines():
        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                symbols.append(match.group(1))
                break
    return first_unique(symbols, limit)


def extract_test_names(patch: str, limit: int = 10) -> list[str]:
    patterns = [
        r"^\+\s*func\s+(Test[A-Za-z0-9_]+)",
        r"^\+\s*def\s+(test_[A-Za-z0-9_]+)",
        r"^\+\s*(?:it|test|describe)\(\s*['\"]([^'\"]+)['\"]",
        r"^\+\s*(?:async\s+)?function\s+(test[A-Za-z0-9_]+)",
        r"^\+\s*fn\s+(test_[A-Za-z0-9_]+)",
    ]
    names: list[str] = []
    for line in patch.splitlines():
        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                names.append(match.group(1))
                break
    return first_unique(names, limit)


def extract_example_lines(patch: str, limit: int = 8) -> list[str]:
    primary: list[str] = []
    secondary: list[str] = []
    primary_pattern = re.compile(
        r"(assert|expect|Equal|DeepEqual|require\.|raises|rejects|throws|toBe|toEqual|toThrow|assert_eq|assert!|testStringObject|testIntegerObject|testBooleanObject)"
    )
    secondary_pattern = re.compile(
        r"(want|expected|DecodingError|StreamConsumed|Content-Type|Allow|==|!=|\|[A-Za-z0-9_]+\|)"
    )
    for raw in patch.splitlines():
        if not raw.startswith("+") or raw.startswith("+++"):
            continue
        line = clean_added_line(raw).strip()
        if not line or line.startswith("//") or line.startswith("#"):
            continue
        if len(line) > 160:
            continue
        if primary_pattern.search(line):
            primary.append(line)
        elif secondary_pattern.search(line):
            secondary.append(line)
    return first_unique(primary + secondary, limit)


def extract_instruction_examples(text: str, limit: int = 5) -> list[str]:
    examples: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if "`" in line or "for example" in line.lower() or "e.g." in line.lower():
            line = re.sub(r"^-\s+", "", line)
            examples.append(compact_line(line, 170))
    return first_unique(examples, limit)


def fenced_lines(lines: list[str], language: str = "text") -> str:
    if not lines:
        return ""
    body = "\n".join(lines)
    return f"```{language}\n{body}\n```"


def language_solution_note(language: str) -> str:
    notes = {
        "go": "Go では、公開関数の追加だけでなく、既存の構造体、パッケージ境界、テストヘルパーの責務に沿って変更します。",
        "python": "Python では、公開 API、例外型、既存のテストフィクスチャ、型変換の入口を同じ流れで確認します。",
        "typescript": "TypeScript では、実行時の挙動と型定義がずれないように、公開型、builder、export 面を同時に追います。",
        "javascript": "JavaScript では、型システムに頼りすぎず、入力の正規化、既存 API の戻り値、テストで観測される副作用を確認します。",
        "rust": "Rust では、公開型、エラー型、所有権、既存 trait や enum への統合を分けて追います。",
    }
    return notes.get(language, "この課題では、公開 API、内部状態、既存テストの観測点を分けて追います。")


def write_solution_guide(task: Task, guide_output_dir: Path) -> None:
    solution_files = parse_patch_files(task.solution_patch)
    test_files = parse_patch_files(task.test_patch)
    solution_symbols = extract_symbols(task.solution_patch)
    test_names = extract_test_names(task.test_patch)
    example_lines = extract_example_lines(task.test_patch)
    instruction_examples = extract_instruction_examples(task.instruction)
    requirements = notable_requirements(task.instruction, limit=10)

    symbols_block = (
        "\n".join(f"- `{symbol}`" for symbol in solution_symbols)
        if solution_symbols
        else "- 追加された公開名や helper 名はパッチから機械的には抽出できませんでした。変更ファイルの hunk を読んで責務を確認します。"
    )
    test_names_block = (
        "\n".join(f"- `{name}`" for name in test_names)
        if test_names
        else "- テスト名は機械的には抽出できませんでした。`tests/test.patch` の追加行を読み、期待値と失敗条件を確認します。"
    )
    example_lines_block = (
        "\n".join(f"- `{line}`" for line in example_lines)
        if example_lines
        else "- 期待値の具体行は機械的には抽出できませんでした。課題文の例と追加テストの入力データを照合します。"
    )
    instruction_examples_block = (
        "\n".join(f"- {line}" for line in instruction_examples)
        if instruction_examples
        else "- 課題文に短いコード例が少ないため、追加テストの入力と期待値を例として使います。"
    )
    requirements_block = (
        "\n".join(f"- {item}" for item in requirements)
        if requirements
        else "- 課題文の段落全体を読み、公開 API、入力、出力、状態、エラーに分けます。"
    )
    concrete_code_block = fenced_lines(example_lines[:5], "text") if example_lines else ""

    content = f"""# {task.task_id} 詳細解法ガイド

## 課題の要約

対象は `{task.language or "unknown"}` の `{task.category or "unknown"}` 課題です。
対象リポジトリは `{task.repository_url or "未記載"}`、base commit は `{task.base_commit_hash or "未記載"}` です。

一文で言うと、`{task.title}` を既存コードの責務に沿って実装する課題です。
このガイドは `instruction.md`、`tests/test.patch`、`solution/solution.patch` を根拠にしています。

参照解答は一つの設計例です。
同じ観測可能な挙動を満たす別実装もあり得るため、差分の形ではなく責務の置き場所を読みます。

## 解法の軸

{center_idea(task)}

## 要求の分解

まず、課題文で目立つ要求を受け入れ条件の候補として分けます。
次の項目は機械的な抽出なので、正確な条件は必ず `instruction.md` 本文に戻って確認します。

{requirements_block}

この段階では、公開 API や設定、入力形式、出力として観測される値、内部状態、エラー条件を別々に扱います。
これらを混ぜると、テストの一例だけに合わせた分岐になりやすくなります。

## 具体例で見る期待動作

課題文から拾える例は次の通りです。

{instruction_examples_block}

追加テストで特に名前が付いている確認項目は次の通りです。
テスト名は、解法が満たすべき振る舞いの短いラベルとして使えます。

{test_names_block}

テスト内の期待値や検証行には、実装者が再現すべき観測結果が出ます。
次の行を読むときは、左辺の入力や操作と、右辺の期待結果を分けます。

{example_lines_block}

短いコード片として読むと、次のようになります。
この断片は追加テストから抜き出した観測点であり、周辺の fixture や setup は省略しています。

{concrete_code_block if concrete_code_block else "追加テストから短いコード片を抽出できませんでした。`tests/test.patch` の fixture と assertion を対応させて読んでください。"}

## 参照解答の変更箇所

参照解答では、主に次のファイルが変更されています。
行数は変更の大きさを見るための目安で、設計上の重要度とは一致しない場合があります。

{patch_file_bullets(solution_files)}

テスト側では、次のファイルに受け入れ条件が追加されています。

{patch_file_bullets(test_files, limit=5)}

ここで確認できる事実は、どのファイルに変更が入り、どのテストが受け入れ条件を追加したかです。
一方で、パッチだけから「この実装だけが正解」とは断定できません。
解釈は、課題文とテストの観測結果に照らして行います。

## 解き方の手順

1. `instruction.md` の要求を、公開 API、内部状態、入力解釈、出力の観測点に分けます。
2. 参照解答で変更されたファイルを見て、既存コードがその責務をどこに置いていたかを確認します。
3. 新しい関数や型を追加する場合は、既存の命名、エラー処理、テストヘルパーの置き場所に合わせます。
4. 追加テストの具体例を一つ選び、入力から期待値までの処理経路を紙に書ける程度まで追います。
5. その経路が通ったあとで、境界条件、エラー、順序、既存挙動の回帰を確認します。

この課題の言語別の注意点は次の通りです。
{language_solution_note(task.language)}

## 参照実装の設計例

参照実装は、課題文の要求を既存コードの責務へ接続する例として読みます。
新規ファイルがある場合は、新しい責務を分離した可能性があります。
既存ファイルへの大きな変更がある場合は、既存の入口や状態管理に新しい条件を組み込んだ可能性があります。

変更ファイルの hunk header は、既存関数内の変更位置を示すことがあります。
そのため、hunk header に出た名前をそのまま新規 API とみなさず、追加された宣言と既存スコープを分けて読みます。

## 変更名から見る実装の入口

参照解答の追加行から、次の関数名や型名が見えます。
これらは実装の入口候補です。
ただし、内部 helper も含まれるため、公開 API か内部実装かを必ず分けて読んでください。

{symbols_block}

## 初学者が詰まりやすい点

テストを通すだけの局所分岐を先に書くと、課題文にある別の条件と衝突しやすくなります。
先に責務の置き場所を決め、同じデータや同じ状態を一箇所の規則で扱う形に寄せます。

参照解答と自分の実装を比べるときは、変更行数ではなく、同じ入力をどの段階で正規化しているかを見ます。
入力の正規化、状態更新、出力生成、エラー化の段階が混ざっている場合は、あとで条件が増えたときに壊れやすくなります。

具体例として、テストに `assert` や `expect` がある場合、その行だけを満たす分岐を足すのではなく、assertion が表している規則を探します。
たとえば順序の assertion は「この順に並べる」ではなく、比較規則や安定化規則を実装する問題として読みます。
エラーの assertion は「この文字列を返す」ではなく、どの境界で入力を拒否するかを決める問題として読みます。

## 復習チェック

- 追加テストの例を一つ選び、入力から期待値までを説明できる。
- 参照解答が変更した主要ファイルの責務を説明できる。
- 新しく見えた関数名や型名について、公開 API と内部 helper を区別できる。
- 課題文の条件を、テストの具体例だけでなく設計上の規則として言い換えられる。
"""
    guide_output_dir.joinpath("solution.ja.md").write_text(content, encoding="utf-8")



def readable_topic(task: Task) -> str:
    parts = task.task_id.split("-")
    known = [GENERIC_TERMS[p] for p in parts if p in GENERIC_TERMS]
    if known:
        topic = "、".join(dict.fromkeys(known))
        return f"{topic}に関する既存ライブラリの挙動を直す課題"
    if task.description:
        return "既存ライブラリの機能追加または不具合修正を行う課題"
    return "OSS 由来のコードベースに対して、課題文で指定された挙動を実装する課題"


def language_note(language: str) -> str:
    return LANGUAGE_NOTES.get(language, "この課題では、公開 API、既存設計、テストで観測される挙動を先に確認します。")


def task_words(task: Task) -> set[str]:
    text = " ".join([task.task_id, task.title, task.description, first_paragraph(task.instruction)]).lower()
    return set(re.findall(r"[a-z][a-z0-9]+", text))


def center_idea(task: Task) -> str:
    words = task_words(task)
    matched_ideas: list[str] = []
    for keywords, idea in IDEA_RULES:
        if any(keyword in words for keyword in keywords):
            matched_ideas.append(idea)
        if len(matched_ideas) == 2:
            break

    if not matched_ideas:
        matched_ideas.append("新しい機能を既存コードに足すだけでなく、公開 API、内部状態、既存挙動の責務をそろえること")

    title = task.title.rstrip(".")
    first_idea = matched_ideas[0]
    detail = ""
    if len(matched_ideas) > 1:
        detail = f"\n\n補助線としては、{matched_ideas[1]}も見ます。"

    return (
        f"この課題の中心アイデアは、`{title}` を個別ケースの追加として扱わず、"
        f"{first_idea}です。"
        f"{detail}\n\n"
        "そのため、まず課題文が触っている公開 API、内部状態、入力の解釈、出力の観測点を分けます。"
        "細かい条件は、それぞれをこの責務に割り当てて読みます。"
    )


def write_readme(tasks: list[Task]) -> None:
    by_language: dict[str, int] = {}
    by_category: dict[str, int] = {}
    for task in tasks:
        by_language[task.language or "unknown"] = by_language.get(task.language or "unknown", 0) + 1
        by_category[task.category or "unknown"] = by_category.get(task.category or "unknown", 0) + 1

    language_rows = "\n".join(
        f"| {language} | {count} |" for language, count in sorted(by_language.items())
    )
    category_rows = "\n".join(
        f"| {category} | {count} |" for category, count in sorted(by_category.items())
    )

    content = f"""# DeepSWE 学習用 instruction 集

生成日時：{GENERATED_AT}

このフォルダは、`tasks/` 配下の 113 件のベンチマーク課題から、学習の入口になる `instruction.md` だけを抜き出したものです。

元の `tasks/` にはテスト、Docker 環境、参照解答が含まれます。
このフォルダでは、課題ごとに問題文・初学者向け解説・解法ガイドを同じディレクトリにまとめています。解法ガイドは自力で考えた後に読んでください。

## instruction.md を見ればよいか

最初に見るファイルは `instruction.md` で合っています。

`instruction.md` は、ベンチマーク上でエージェントに渡される課題文です。
何を直すか、どの挙動を満たすか、公開 API をどう保つかが書かれています。

ただし、学習では `instruction.md` だけで完結させないほうがよいです。
実装前に `task.toml` で対象リポジトリ、言語、base commit を確認します。
行き詰まった後に `tests/test.patch` を読むと、課題文のどの条件が採点されるかを確認できます。
`solution/solution.patch` は参照解答なので、最初には読まず、最後に自分の設計と比較するために使います。

## 推奨する読み方

1. `<task-id>/instruction.md` を読む。
2. `<task-id>/beginner.ja.md` の「中心アイデア」で、設計上そろえる対象を確認する。
3. 原文の要求を「入力」「期待する出力」「守るべき既存仕様」「公開 API」に分ける。
4. 元の `tasks/<task-id>/task.toml` で対象リポジトリ、言語、base commit を確認する。
5. 実装方針を立ててから、必要に応じて `tasks/<task-id>/tests/test.patch` を読む。
6. 行き詰まった後、または自力実装後に `<task-id>/solution.ja.md` を読む。
7. 最後に `tasks/<task-id>/solution/solution.patch` を見て、設計差分を復習する。

## フォルダ構成

```text
tasks-learning/
  README.md
  index.md
  <task-id>/
    instruction.md
    beginner.ja.md
    solution.ja.md
```

## 言語別件数

| language | count |
| --- | ---: |
{language_rows}

## カテゴリ別件数

| category | count |
| --- | ---: |
{category_rows}

## 例：abs-module-cache-flags の読み方

この課題は ABS という言語処理系のモジュール読み込みを堅牢にする問題です。

初心者は、まず「同じファイルを別のパスで `require()` したときに、キャッシュが二重にならないようにする」と読み替えると入口が見えます。
次に、`ABS_MODULE_PATH`、循環 import、デバッグ出力、CLI フラグという周辺仕様を分けて読みます。
全部を一つの if 文で処理するのではなく、解決処理、キャッシュ管理、循環検出、CLI オプション解析を別の責務として見るのが自然です。

この種の課題では、`instruction.md` の箇条書きはほぼ受け入れ条件です。
実装を始める前に、各条件を「どの入力で」「どの観測結果なら成功か」に変換すると学習しやすくなります。
"""
    (OUTPUT_DIR / "README.md").write_text(content, encoding="utf-8")


def write_index(tasks: list[Task]) -> None:
    rows = []
    for task in tasks:
        rows.append(
            "| "
            + " | ".join(
                [
                    f"[{task.task_id}]({task.task_id}/beginner.ja.md)",
                    task.language or "",
                    task.category or "",
                    task.title.replace("|", "\\|"),
                    f"[解説]({task.task_id}/solution.ja.md)",
                ]
            )
            + " |"
        )
    content = """# Task Index

| task | language | category | title | solution guide |
| --- | --- | --- | --- | --- |
""" + "\n".join(rows) + "\n"
    (OUTPUT_DIR / "index.md").write_text(content, encoding="utf-8")


def write_beginner_explanation(task: Task, task_output_dir: Path) -> None:
    requirements = notable_requirements(task.instruction)
    if requirements:
        requirement_block = "\n".join(f"- {item}" for item in requirements)
    else:
        requirement_block = "- 原文の本文全体が受け入れ条件です。段落ごとに入力、期待結果、制約に分けて読みます。"

    opening = first_paragraph(task.instruction)
    description = task.description or task.title

    special_note = SPECIAL_BEGINNER_NOTES.get(task.task_id, "")
    if special_note:
        special_note = "\n" + special_note + "\n"

    content = f"""# {task.task_id} 初学者向け解説

## この課題の位置づけ

この課題は、{readable_topic(task)}です。

対象言語は `{task.language or "unknown"}`、カテゴリは `{task.category or "unknown"}` です。

英語の短い説明は次の内容です。

> {description}

## まず読むべき原文

`instruction.md` の冒頭は、この課題のゴールを一文または短い段落で説明しています。

> {opening}

初心者は、この段落を「既存コードのどの利用者が、どんな入力で困っていて、修正後に何を期待するか」に分けて読みます。

## 中心アイデア

{center_idea(task)}

## 問題を分解するときの観点

目的：どの利用者向けの挙動を追加または修正する課題かを一文で言い換えます。

公開 API や設定：関数名、クラス名、設定名、HTTP ヘッダー名、CLI フラグは翻訳せず、どこから使われるものかを確認します。

状態や順序：キャッシュ、ストリーム、並行処理、優先順位、継承規則がある場合は、実装場所より先に状態遷移を整理します。

エラーと境界条件：不正入力、空入力、重複、順序違い、既存挙動との衝突を、課題文の条件として分けます。

やらないこと：課題文に明示された対象外の挙動があれば、実装を広げすぎないために別枠に置きます。

## 原文で目立つ要求

次の項目は、課題文から機械的に抜き出した目印です。
正確な条件は必ず `instruction.md` 本文を優先してください。

{requirement_block}

{special_note}
## 解く前に確認すること

{language_note(task.language)}

最初から参照解答を読まず、まず課題文の要求を自分の言葉で分解します。
分解するときは、公開 API、内部状態、エラー処理、順序、境界条件を分けます。

`task.toml` では、対象リポジトリと base commit を確認します。
同じライブラリでもバージョンが違うと実装場所や既存設計が変わるためです。

## 実装方針を考える順序

1. 既存の似た機能を探す。
2. 課題文の各要求を、観測可能な振る舞いに変換する。
3. 既存設計に合う責務の置き場所を決める。
4. 境界条件をテストとして想像する。
5. 行き詰まったら元の `tasks/{task.task_id}/tests/test.patch` を読む。
6. 実装後に `solution.patch` と比較し、設計の違いを復習する。

## 注意

このファイルは学習補助です。
採点で正になる条件は `instruction.md` と verifier 側のテストで決まります。
"""
    task_output_dir.joinpath("beginner.ja.md").write_text(content, encoding="utf-8")


def build(force: bool) -> None:
    tasks = load_tasks()
    if OUTPUT_DIR.exists():
        if not force:
            raise SystemExit(f"{OUTPUT_DIR} already exists. Re-run with --force to regenerate it.")
        shutil.rmtree(OUTPUT_DIR)

    OUTPUT_DIR.mkdir(parents=True)
    write_readme(tasks)
    write_index(tasks)

    for task in tasks:
        task_output_dir = OUTPUT_DIR / task.task_id
        task_output_dir.mkdir(parents=True)
        task_output_dir.joinpath("instruction.md").write_text(task.instruction, encoding="utf-8")
        write_beginner_explanation(task, task_output_dir)
        write_solution_guide(task, task_output_dir)

    count_text = textwrap.dedent(
        f"""
        Wrote {len(tasks)} tasks to {OUTPUT_DIR.relative_to(ROOT)}
        Instruction files: {len(list(OUTPUT_DIR.glob('*/instruction.md')))}
        Beginner explanations: {len(list(OUTPUT_DIR.glob('*/beginner.ja.md')))}
        Solution guides: {len(list(OUTPUT_DIR.glob('*/solution.ja.md')))}
        """
    ).strip()
    print(count_text)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="regenerate tasks-learning if it already exists")
    args = parser.parse_args()
    build(force=args.force)


if __name__ == "__main__":
    main()
