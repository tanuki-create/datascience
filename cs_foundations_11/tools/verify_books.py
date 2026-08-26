#!/usr/bin/env python3
"""CS基礎11冊の構造要件を検査する。外部依存は使わない。"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Book:
    filename: str
    required_original_chapters: int

    @property
    def expected_total(self) -> int:
        return self.required_original_chapters + 1


BOOKS = (
    Book("01_algorithms.md", 15),
    Book("02_discrete_math.md", 15),
    Book("03_automata_computability.md", 16),
    Book("04_programming_languages.md", 20),
    Book("05_operating_systems.md", 23),
    Book("06_concurrency_distributed.md", 30),
    Book("07_database.md", 28),
    Book("08_probability_statistics.md", 28),
    Book("09_software_engineering.md", 32),
    Book("10_hci.md", 29),
    Book("11_security.md", 39),
)

CHAPTER_RE = re.compile(r"^##\s+第(\d+)章\s+(.+)$", re.MULTILINE)
APPENDIX_TITLE = "## 付録　専門家の思考を測る"
APPENDIX_SECTIONS = (
    ("### 専門家が共有する5つの中核的メンタルモデル", 5),
    ("### 専門家の意見が根本的に分かれる3つの論点", 3),
    ("### 深い理解と暗記を見分ける10の質問", 10),
)
INLINE_LINK_RE = re.compile(
    r"!?\[[^\]]*\]\(\s*(?P<target><[^>]+>|[^\s)]+)",
)
REFERENCE_LINK_RE = re.compile(
    r"^[ \t]{0,3}\[[^\]]+\]:[ \t]*(?P<target><[^>]+>|\S+)",
    re.MULTILINE,
)
INLINE_CODE_RE = re.compile(r"(?P<fence>`+)[^`\n]*?(?P=fence)")


def count_work_items_between(chapter: str, start_label: str, end_labels: tuple[str, ...]) -> int:
    """章末section内の番号だけを数える。

    教科書にはheading形式とinline bold形式が混在する。labelの最初の出現から
    次labelまでを切り出し、本文中の年・式・他sectionの番号で水増ししない。
    """

    start = chapter.find(start_label)
    if start < 0:
        return 0
    start += len(start_label)
    ends = [chapter.find(label, start) for label in end_labels]
    valid_ends = [position for position in ends if position >= 0]
    end = min(valid_ends) if valid_ends else len(chapter)
    numbers = {
        int(number)
        for number in re.findall(r"(?<!\d)(\d{1,2})[\.．:]", chapter[start:end])
    }
    return len(numbers)


def without_code(text: str) -> str:
    """Markdown code内のlink風文字列を検査対象から除く。"""

    visible_lines: list[str] = []
    closing_fence: tuple[str, int] | None = None
    for line in text.splitlines(keepends=True):
        fence = re.match(r"^[ \t]{0,3}(`{3,}|~{3,})", line)
        if closing_fence is not None:
            marker, minimum_length = closing_fence
            if re.match(
                rf"^[ \t]{{0,3}}{re.escape(marker)}{{{minimum_length},}}[ \t]*(?:\n)?$",
                line,
            ):
                closing_fence = None
            visible_lines.append("\n" if line.endswith("\n") else "")
            continue
        if fence:
            delimiter = fence.group(1)
            closing_fence = (delimiter[0], len(delimiter))
            visible_lines.append("\n" if line.endswith("\n") else "")
            continue
        visible_lines.append(INLINE_CODE_RE.sub("", line))
    return "".join(visible_lines)


def relative_markdown_targets(text: str) -> set[str]:
    """本文中の相対`.md` link先を返す。fragment/queryは存在検査に使わない。"""

    visible = without_code(text)
    candidates = {
        match.group("target").strip("<>")
        for pattern in (INLINE_LINK_RE, REFERENCE_LINK_RE)
        for match in pattern.finditer(visible)
    }
    targets: set[str] = set()
    for candidate in candidates:
        if candidate.startswith("#"):
            continue
        parsed = urlsplit(candidate)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        path = unquote(parsed.path)
        if Path(path).is_absolute() or Path(path).suffix.lower() != ".md":
            continue
        targets.add(path)
    return targets


def inspect_markdown_links() -> list[str]:
    """ROOT配下の全Markdownで、source相対の`.md` link切れを検出する。"""

    errors: list[str] = []
    for source in sorted(ROOT.rglob("*.md")):
        text = source.read_text(encoding="utf-8")
        for target in sorted(relative_markdown_targets(text)):
            resolved = (source.parent / target).resolve()
            if not resolved.is_file():
                errors.append(
                    f"{source.relative_to(ROOT)}: broken relative markdown link "
                    f"{target!r} -> {resolved}"
                )
    return errors


def inspect_readme() -> list[str]:
    path = ROOT / "README.md"
    if not path.exists():
        return ["MISSING: README.md"]

    text = path.read_text(encoding="utf-8")
    failures: list[str] = []
    for book in BOOKS:
        expected_link = f"(books/{book.filename})"
        if expected_link not in text:
            failures.append(f"README.md: missing link to books/{book.filename}")

    for target in re.findall(r"\]\(([^)#]+\.md)(?:#[^)]+)?\)", text):
        if not (ROOT / target).exists():
            failures.append(f"README.md: broken local link {target}")
    return failures


def inspect(book: Book) -> list[str]:
    path = ROOT / "books" / book.filename
    if not path.exists():
        return [f"MISSING: {path.relative_to(ROOT)}"]

    text = path.read_text(encoding="utf-8")
    matches = list(CHAPTER_RE.finditer(text))
    errors: list[str] = []
    numbers = [int(m.group(1)) for m in matches]
    expected = list(range(1, book.expected_total + 1))
    if numbers != expected:
        errors.append(f"chapter sequence {numbers}; expected {expected}")
    if not matches:
        return [f"{book.filename}: no numbered chapters"]
    if "誤判断" not in matches[-1].group(2):
        errors.append("last chapter title does not contain 誤判断")
    if "総合演習" not in text:
        errors.append("no 総合演習")
    if text.count("```") % 2:
        errors.append("unbalanced fenced code block")
    if re.search(r"\b(?:TODO|TBD|PLACEHOLDER)\b", text, re.IGNORECASE):
        errors.append("contains unfinished-work marker")

    required_labels = ("要点", "誤解チェック", "基礎問題", "応用問題", "設計問題", "調査課題")
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        chapter = text[match.start():end]
        missing = [label for label in required_labels if label not in chapter]
        if missing:
            errors.append(f"chapter {match.group(1)} missing labels: {', '.join(missing)}")
        basics = count_work_items_between(chapter, "基礎問題", ("応用問題",))
        applications = count_work_items_between(
            chapter,
            "応用問題",
            ("知らないとする誤判断", "知らない場合", "次章", "次の学習"),
        )
        if basics < 5:
            errors.append(f"chapter {match.group(1)} has {basics} basic problems; need 5")
        if applications < 3:
            errors.append(f"chapter {match.group(1)} has {applications} applied problems; need 3")

    final_start = matches[-1].start()
    final_chapter = text[final_start:]
    # 最終章の一覧は太字・通常listのどちらでもよい。章末問題の1..5が
    # 混ざっても集合なので、1..20の連番が本文にあれば下限を満たす。
    misconception_numbers = {
        int(n) for n in re.findall(r"(?m)^\s*(\d{1,2})[\.．]\s+", final_chapter)
    }
    if len(misconception_numbers) < 20:
        errors.append(f"final misconception chapter has {len(misconception_numbers)} numbered cases; need 20")
    if len(text) < book.expected_total * 900:
        errors.append(f"content is suspiciously short: {len(text)} chars")

    appendix_start = text.find(APPENDIX_TITLE)
    if appendix_start < 0:
        errors.append("missing expert-thinking appendix")
    else:
        appendix = text[appendix_start:]
        later_h2 = re.search(r"(?m)^##\s+(?!付録　専門家の思考を測る).+", appendix)
        if later_h2:
            errors.append("expert-thinking appendix is not the final H2 section")
        for section_index, (heading, expected_count) in enumerate(APPENDIX_SECTIONS):
            start = appendix.find(heading)
            if start < 0:
                errors.append(f"expert-thinking appendix missing section: {heading}")
                continue
            start += len(heading)
            later_positions = [
                appendix.find(other_heading, start)
                for other_heading, _ in APPENDIX_SECTIONS[section_index + 1 :]
            ]
            valid_positions = [position for position in later_positions if position >= 0]
            end = min(valid_positions) if valid_positions else len(appendix)
            item_numbers = [
                int(number)
                for number in re.findall(r"(?m)^\s*(\d{1,2})[\.．]\s+", appendix[start:end])
            ]
            expected_numbers = list(range(1, expected_count + 1))
            if item_numbers != expected_numbers:
                errors.append(
                    f"{heading} item sequence {item_numbers}; expected {expected_numbers}"
                )
    return [f"{book.filename}: {error}" for error in errors]


def main() -> int:
    failures = inspect_readme()
    failures.extend(failure for book in BOOKS for failure in inspect(book))
    failures.extend(inspect_markdown_links())
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    linked_books = set(re.findall(r"\(books/([^\)]+\.md)\)", readme))
    expected_books = {book.filename for book in BOOKS}
    if linked_books != expected_books:
        failures.append(
            "README book links differ: "
            f"missing={sorted(expected_books - linked_books)}, "
            f"unexpected={sorted(linked_books - expected_books)}"
        )
    for linked in linked_books:
        if not (ROOT / "books" / linked).exists():
            failures.append(f"README broken local link: books/{linked}")
    if failures:
        print("STRUCTURE CHECK FAILED")
        print("\n".join(f"- {failure}" for failure in failures))
        return 1
    total = sum(book.expected_total for book in BOOKS)
    print(
        f"OK: {len(BOOKS)} books, {total} numbered chapters, "
        "required work sections and 5/3/10 expert appendices present"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
