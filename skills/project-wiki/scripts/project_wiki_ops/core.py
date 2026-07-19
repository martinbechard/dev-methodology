# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Modified with AI assistance.
# Summary: Implements deterministic project-wiki inspection, setup guidance, linking, lint, and scaffold operations.

"""Deterministic project wiki inspection and scaffold operations."""

from __future__ import annotations

import re
import os
import subprocess
from pathlib import Path

from .constants import (
    CODE_FENCE_MARKER,
    DIGESTS_DIR_NAME,
    EXEMPT_SCHEMA_FILES,
    GREP_SEARCH_COMMAND,
    GIT_CHANGED_COMMAND,
    INDEX_PAGE_NAME,
    LIST_ITEM_PREFIX,
    MARKDOWN_FILE_SUFFIX,
    MARKDOWN_HEADING_PREFIX,
    MIN_LEAF_TITLE_ALNUM_COUNT,
    NO_OPEN_QUESTIONS_PREFIX,
    OPEN_QUESTIONS_HEADING,
    PROJECT_ROOT,
    REQUIRED_WIKI_FILES,
    RIPGREP_SEARCH_COMMAND,
    ROOT_RELATIVE_PREFIXES,
    RAW_SOURCE_PATH_SEGMENT,
    SECTION_HEADING_PREFIX,
    SOURCE_TO_WIKI_PATTERNS,
    TOPIC_REQUIRED_HEADINGS,
    WIKI_DIR,
    CONTINUATION_PREFIX,
)
from .models import LeafLinkChange, LeafPage, LintResult, OpenQuestion


MARKDOWN_LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
MARKDOWN_LINK_SPAN_PATTERN = re.compile(r"\[[^\]]+\]\([^)]+\)")
PLAIN_LOCAL_PATH_PATTERN = re.compile(
    r"(?P<path>(?:backlog|docs|src|tests|\.agents)/[A-Za-z0-9_./()[\]-]+|procedure-[A-Za-z0-9_.-]+\.md|AGENTS\.md|README\.md)"
)
PAGE_TEMPLATES = {
    "README.md": """# Project Wiki

This folder contains the maintained synthesis layer for this repository.

The wiki organizes current project understanding across source documents, code, tests, plans, and backlog records. It is a navigation and synthesis layer. It is not the source of truth.

## Use

Agents use the project-wiki skill before changing or explaining specs, architecture, plans, backlog files, documentation surfaces, or user-visible behavior.

Run:

```bash
python3 project-wiki-skill-root/scripts/wiki_ops.py status
python3 project-wiki-skill-root/scripts/wiki_ops.py suggest --changed
python3 project-wiki-skill-root/scripts/wiki_ops.py link-leaves
python3 project-wiki-skill-root/scripts/wiki_ops.py lint
python3 project-wiki-skill-root/scripts/wiki_ops.py questions
```

## Pages

- [schema.md](schema.md)
- [topic-index.md](topic-index.md)
- [glossary.md](glossary.md)
- [open-decisions.md](open-decisions.md)
- [known-defects.md](known-defects.md)
- [maintenance-log.md](maintenance-log.md)
- [digests/index.md](digests/index.md) when raw news or development sources are ingested

## Topic Folders

Use topic folders for related pages. Each topic folder should have an index.md hub page plus granular leaf pages.
Use docs/wiki/digests for monthly development digests that link to entity leaf pages.
""",
    "schema.md": """# Wiki Schema

The wiki is a maintained synthesis layer. It summarizes and links project knowledge but does not replace authoritative sources.

## Authority Order

1. Code and tests describe actual behavior.
2. Functional specifications and requirements describe intended behavior.
3. AGENTS.md, README files, and procedure files describe workflow obligations.
4. Defect and feature backlog files describe tracked work. Status headings or explicit status fields determine whether an item is open, fixed, completed, or otherwise closed.
5. Architecture and plan documents describe design intent.
6. Help, RAG, or generated documentation describes the current documentation and retrieval surface.
7. Wiki pages summarize and navigate the above sources.

## Topic Page Sections

Topic pages should include:

```markdown
# Topic Name

## Current Understanding

## Authoritative Sources

## Related Code

## Related Tests

## Related Backlog Items

## Related Wiki Pages

## Open Questions

## Maintenance Notes
```

## Maintenance Rules

- Update the wiki when a task changes current behavior, intended behavior, workflow obligations, backlog state, or the meaning of a project concept.
- Prefer granular pages over monolithic pages.
- Use topic folders with index.md hub pages when related concepts, providers, components, snapshots, workflows, or decisions belong together.
- When processing raw source files, create or update durable entity leaf pages for products, companies, models, frameworks, techniques, protocols, standards, workflows, notable features, and security issues mentioned in the source.
- Run the leaf-link pass after creating or updating a durable leaf page.
- Use repository grep to find existing wiki mentions of each leaf title before finishing.
- A page that mentions a durable leaf title should link the first unlinked mention to that leaf unless the mention is inside a heading, code fence, or existing link.
- If a raw source does not explain a named entity enough for a useful leaf, use focused research and cite the sources.
- Create monthly development digests under docs/wiki/digests. Digest entries may keep the date when information was added or modified, but each entry should summarize the content that changed instead of listing page or file changes. Use one digest entry per independently changing item or closely coupled product family; do not bundle unrelated items into one dated paragraph. Keep monthly digest Current Understanding entries in reverse chronological order by entry date, newest first. Keep each entry to at most three lines and link to the entity leaf that holds the details.
- When repairing an existing digest, inspect the current month page for bundled dated paragraphs and rewrite the requested date range into item-level synopsis entries instead of only appending new entries. Reorder the affected Current Understanding entries into reverse chronological order by entry date before finishing. Use durable leaf pages as the content anchor for digest prose; keep source files in Authoritative Sources as provenance rather than repeating source-log wording. Do not create separate digest entries for duplicate raw captures or repeated source-window sightings unless they add distinct content; fold them into the existing item or closely coupled product-family entry.
- Raw-source ingest automation prompts must repeat the digest granularity and ordering rules directly: one digest entry per independently changing item or closely coupled product family; never group digest entries by raw source artifact, collector run, sweep category, or ingestion batch; keep monthly digest Current Understanding entries in reverse chronological order by entry date.
- When a digest page changes, the automation closeout must report that digest granularity and ordering were checked with the project-wiki-topic-verify checklist, or that the full verifier returned GOOD.
- High-volume raw sources may update many durable leaves without forcing every touched leaf into the digest; omit low-signal digest mentions rather than compress unrelated entities into a vague grouped bullet.
- Keep dated research, news, meeting notes, raw-source synthesis, and migration history as leaf pages under durable topic folders.
- After raw files are fully processed into entity leaves and the monthly digest, move them under raw/processed and update wiki source links to the processed path using relative links from the wiki page, not absolute filesystem paths.
- Mention local files and wiki pages as Markdown links, not as bare filenames or paths.
- Prefer contextual links in the relevant explanation. Use Related Wiki Pages only when a short linked cross-reference adds navigation value.
- Keep steady-state explanations free of historical comparison unless the page is documenting a migration or maintenance note.
- Preserve unresolved contradictions in Open Questions.
- Review unresolved questions with python3 project-wiki-skill-root/scripts/wiki_ops.py questions. Ask one question at a time, update the wiki from the answer, rerun questions to confirm the item is gone, then run lint.
- Never invent source paths, test coverage, backlog status, or fallback behavior.
""",
    "topic-index.md": """# Topic Index

## Primary Topics

- [known-defects.md](known-defects.md) summarizes defect backlog interpretation.
- [glossary.md](glossary.md) defines recurring project terms.
- [open-decisions.md](open-decisions.md) collects unresolved decisions.

## Source Neighborhoods

- docs/architecture holds design intent when present.
- docs/plans holds implementation plans when present.
- backlog/defect-backlog holds tracked defects when present.
- backlog/feature-backlog holds tracked feature requests when present.
- AGENTS.md, README files, and procedure files hold workflow obligations.
""",
    "glossary.md": """# Glossary

## Terms

- Project wiki: The maintained synthesis layer under docs/wiki.
- Backlog status heading: The status field or heading inside a backlog file that determines whether the item is active, fixed, completed, or otherwise closed.

## Maintenance Notes

- Add recurring project terms when they appear in multiple source documents or wiki pages.
""",
    "open-decisions.md": """# Open Decisions

## Current Decisions Needed

- No project wiki source conflicts are recorded yet.

## Maintenance Rules

- Add an entry when authoritative sources disagree and the correct steady-state answer is unclear.
- Include the source files involved.
- Remove or resolve an entry only after the authoritative source has been updated or verified.
""",
    "known-defects.md": """# Known Defects

## Current Understanding

Defect files are tracked defect records. File presence alone does not prove that a defect is open. Agents must inspect the status heading or explicit status field inside each defect file before reporting active defects or choosing work.

## Authoritative Sources

- Not yet identified.

## Related Code

- Not yet identified.

## Related Tests

- Not yet identified.

## Related Backlog Items

- Not yet identified.

## Related Wiki Pages

- [topic-index.md](topic-index.md)

## Open Questions

- No open wiki questions are recorded for defect backlog interpretation.

## Maintenance Notes

- Keep this page aligned with the repository's defect backlog status conventions.
""",
    "maintenance-log.md": """# Maintenance Log

## Current Entries

- Created the project wiki scaffold.
""",
}


def relative_path(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def stable_path_key(path: Path) -> str:
    if path.is_relative_to(PROJECT_ROOT):
        return relative_path(path)
    return path.as_posix()


def wiki_pages() -> list[Path]:
    if not WIKI_DIR.exists():
        return []
    return sorted(WIKI_DIR.rglob("*.md"))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def markdown_body_text(text: str) -> str:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return text
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return "".join(lines[index + 1 :]).lstrip("\n")
    return text


def extract_h1_title(text: str) -> str:
    for line in markdown_body_text(text).splitlines():
        if line.startswith("# "):
            return line.removeprefix("# ").strip()
    return ""


def is_durable_leaf_page(path: Path) -> bool:
    if not path.is_relative_to(WIKI_DIR):
        return False
    if path.suffix != MARKDOWN_FILE_SUFFIX:
        return False
    if path.parent == WIKI_DIR:
        return False
    if path.parent.name == DIGESTS_DIR_NAME:
        return False
    return path.name != INDEX_PAGE_NAME


def has_linkable_leaf_title(title: str) -> bool:
    alnum_count = sum(1 for character in title if character.isalnum())
    return alnum_count >= MIN_LEAF_TITLE_ALNUM_COUNT


def leaf_pages(selected_paths: list[str] | None = None) -> list[LeafPage]:
    paths = [resolve_input_path(path) for path in selected_paths] if selected_paths else wiki_pages()
    leaves: list[LeafPage] = []
    for path in paths:
        if not is_durable_leaf_page(path):
            continue
        title = extract_h1_title(read_text(path))
        if has_linkable_leaf_title(title):
            leaves.append(LeafPage(path=path, title=title))
    return sorted(leaves, key=leaf_sort_key)


def leaf_sort_key(leaf: LeafPage) -> tuple[int, str]:
    return (-len(leaf.title), stable_path_key(leaf.path))


def resolve_input_path(path: str) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate.resolve()
    return (PROJECT_ROOT / candidate).resolve()


def grep_leaf_mention_paths(leaf: LeafPage) -> list[Path]:
    for command in (RIPGREP_SEARCH_COMMAND, GREP_SEARCH_COMMAND):
        result = subprocess.run(
            (*command, "--", leaf.title, str(WIKI_DIR)),
            cwd=PROJECT_ROOT,
            check=False,
            text=True,
            capture_output=True,
        )
        if result.returncode in (0, 1):
            return [
                Path(line).resolve()
                for line in result.stdout.splitlines()
                if line.strip()
            ]
    return []


def relative_link_target(source_page: Path, target_page: Path) -> str:
    return Path(os.path.relpath(target_page, source_page.parent)).as_posix()


def leaf_title_pattern(title: str) -> re.Pattern[str]:
    escaped_title = re.escape(title)
    return re.compile(rf"(?<![A-Za-z0-9])({escaped_title})(?![A-Za-z0-9])", re.IGNORECASE)


def is_span_inside(candidate_span: tuple[int, int], container_spans: list[tuple[int, int]]) -> bool:
    candidate_start, candidate_end = candidate_span
    return any(start <= candidate_start and candidate_end <= end for start, end in container_spans)


def link_first_unlinked_mention(text: str, title: str, target_link: str) -> tuple[str, bool]:
    pattern = leaf_title_pattern(title)
    lines = text.splitlines(keepends=True)
    in_code_fence = False
    updated_lines: list[str] = []

    for line_index, line in enumerate(lines):
        stripped_line = line.lstrip()
        if stripped_line.startswith(CODE_FENCE_MARKER):
            in_code_fence = not in_code_fence
            updated_lines.append(line)
            continue
        if in_code_fence or stripped_line.startswith(MARKDOWN_HEADING_PREFIX):
            updated_lines.append(line)
            continue

        link_spans = [match.span() for match in MARKDOWN_LINK_SPAN_PATTERN.finditer(line)]
        for match in pattern.finditer(line):
            if is_span_inside(match.span(), link_spans):
                continue
            linked_text = f"[{match.group(0)}]({target_link})"
            updated_line = line[: match.start()] + linked_text + line[match.end() :]
            updated_lines.append(updated_line)
            updated_lines.extend(lines[line_index + 1 :])
            return "".join(updated_lines), True
        updated_lines.append(line)

    return text, False


def page_links_to_leaf(page: Path, text: str, leaf_path: Path) -> bool:
    return any(
        is_local_reference(link) and resolve_reference(page, link).resolve() == leaf_path.resolve()
        for link in extract_markdown_links(text)
    )


def apply_leaf_links_to_page_texts(
    leaves: list[LeafPage],
    page_texts: dict[Path, str],
    mention_paths_by_leaf: dict[Path, list[Path]] | None = None,
) -> tuple[dict[Path, str], list[LeafLinkChange]]:
    updated_texts = dict(page_texts)
    changes: list[LeafLinkChange] = []

    for leaf in sorted(leaves, key=leaf_sort_key):
        target_paths = mention_paths_by_leaf.get(leaf.path, list(updated_texts)) if mention_paths_by_leaf else list(updated_texts)
        for target_path in sorted(target_paths, key=stable_path_key):
            if target_path == leaf.path or target_path not in updated_texts:
                continue
            current_text = updated_texts[target_path]
            if page_links_to_leaf(target_path, current_text, leaf.path):
                continue
            linked_text, changed = link_first_unlinked_mention(
                current_text,
                leaf.title,
                relative_link_target(target_path, leaf.path),
            )
            if not changed:
                continue
            updated_texts[target_path] = linked_text
            changes.append(LeafLinkChange(leaf_path=leaf.path, target_path=target_path, title=leaf.title))

    return updated_texts, changes


def link_leaf_mentions(selected_paths: list[str] | None = None, dry_run: bool = False) -> list[LeafLinkChange]:
    leaves = leaf_pages(selected_paths)
    pages = wiki_pages()
    page_texts = {page: read_text(page) for page in pages}
    mention_paths_by_leaf = {leaf.path: grep_leaf_mention_paths(leaf) for leaf in leaves}
    updated_texts, changes = apply_leaf_links_to_page_texts(leaves, page_texts, mention_paths_by_leaf)

    if dry_run:
        return changes

    for page, updated_text in updated_texts.items():
        if page_texts[page] != updated_text:
            write_text(page, updated_text)

    return changes


def init_wiki() -> list[Path]:
    WIKI_DIR.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []
    for file_name in REQUIRED_WIKI_FILES:
        path = WIKI_DIR / file_name
        if path.exists():
            continue
        path.write_text(PAGE_TEMPLATES[file_name], encoding="utf-8")
        created.append(path)
    return created


def missing_required_files() -> list[str]:
    return [file_name for file_name in REQUIRED_WIKI_FILES if not (WIKI_DIR / file_name).exists()]


def extract_markdown_links(text: str) -> list[str]:
    return [match.group(1).strip() for match in MARKDOWN_LINK_PATTERN.finditer(text)]


def extract_local_paths(text: str) -> list[str]:
    paths = set(extract_markdown_links(text))
    for match in PLAIN_LOCAL_PATH_PATTERN.finditer(text):
        paths.add(match.group("path").rstrip(".,"))
    return sorted(path for path in paths if is_local_reference(path))


def is_local_reference(value: str) -> bool:
    return not value.startswith(("http://", "https://", "#", "mailto:"))


def resolve_reference(page: Path, value: str) -> Path:
    reference = value.split("#", maxsplit=1)[0]
    if not reference:
        return page
    candidate = Path(reference)
    if candidate.is_absolute():
        return candidate
    if reference.startswith(("../", "./")):
        return (page.parent / candidate).resolve()
    if not reference.startswith(ROOT_RELATIVE_PREFIXES):
        return (page.parent / candidate).resolve()
    return (PROJECT_ROOT / candidate).resolve()


def is_absolute_raw_reference(value: str) -> bool:
    reference = value.split("#", maxsplit=1)[0]
    if not reference:
        return False
    candidate = Path(reference)
    return candidate.is_absolute() and RAW_SOURCE_PATH_SEGMENT in candidate.parts


def lint_page(path: Path) -> list[LintResult]:
    text = read_text(path)
    body = markdown_body_text(text)
    findings: list[LintResult] = []
    if not body.startswith("# "):
        findings.append(LintResult(path, "page must start with a level one heading"))
    if path.name not in EXEMPT_SCHEMA_FILES:
        findings.extend(missing_heading_findings(path, body))
    findings.extend(broken_link_findings(path, body))
    return findings


def missing_heading_findings(path: Path, text: str) -> list[LintResult]:
    return [
        LintResult(path, f"missing required heading: {heading}")
        for heading in TOPIC_REQUIRED_HEADINGS
        if heading not in text
    ]


def broken_link_findings(path: Path, text: str) -> list[LintResult]:
    findings: list[LintResult] = []
    for link in extract_markdown_links(text):
        if is_absolute_raw_reference(link):
            findings.append(LintResult(path, f"raw source link must be relative, not absolute: {link}"))
            continue
        if is_local_reference(link) and not resolve_reference(path, link).exists():
            findings.append(LintResult(path, f"broken local link: {link}"))
    return findings


def bare_local_path_findings(path: Path, text: str) -> list[LintResult]:
    linked_paths = set(extract_markdown_links(text))
    findings: list[LintResult] = []
    for match in PLAIN_LOCAL_PATH_PATTERN.finditer(text):
        candidate = match.group("path").rstrip(".,")
        if candidate not in linked_paths:
            findings.append(LintResult(path, f"bare local path should be a Markdown link: {candidate}"))
    return findings


def lint_wiki() -> list[LintResult]:
    findings: list[LintResult] = []
    for file_name in missing_required_files():
        findings.append(LintResult(WIKI_DIR / file_name, "required wiki file is missing"))
    for page in wiki_pages():
        findings.extend(lint_page(page))
    findings.extend(orphan_findings())
    return findings


def orphan_findings() -> list[LintResult]:
    topic_pages = [
        page
        for page in wiki_pages()
        if page.parent != WIKI_DIR or page.name not in EXEMPT_SCHEMA_FILES
    ]
    linked_pages: set[Path] = set()
    for page in wiki_pages():
        for link in extract_markdown_links(read_text(page)):
            resolved = resolve_reference(page, link)
            if resolved.is_relative_to(WIKI_DIR) and resolved.suffix == ".md" and resolved != page:
                linked_pages.add(resolved)
    return [
        LintResult(page, "topic page is not linked by another wiki page")
        for page in topic_pages
        if page not in linked_pages
    ]


def changed_files() -> list[str]:
    result = subprocess.run(
        GIT_CHANGED_COMMAND,
        cwd=PROJECT_ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        return []
    return [parse_porcelain_path(line) for line in result.stdout.splitlines() if line.strip()]


def parse_porcelain_path(line: str) -> str:
    path = line[3:].strip()
    if " -> " in path:
        path = path.split(" -> ", maxsplit=1)[1]
    return path


def suggested_pages(paths: list[str]) -> dict[str, set[str]]:
    suggestions: dict[str, set[str]] = {}
    for source_path in paths:
        for pattern, wiki_page in SOURCE_TO_WIKI_PATTERNS:
            if source_path == pattern or source_path.startswith(pattern) or pattern in source_path:
                suggestions.setdefault(wiki_page, set()).add(source_path)
    return suggestions


def is_section_heading(line: str) -> bool:
    return line.startswith(SECTION_HEADING_PREFIX)


def normalize_question(text: str) -> str:
    return " ".join(text.strip().split())


def is_open_questions_placeholder(question: str) -> bool:
    return question.startswith(NO_OPEN_QUESTIONS_PREFIX)


def extract_open_questions_from_page(path: Path) -> list[OpenQuestion]:
    questions: list[OpenQuestion] = []
    in_open_questions_section = False
    current_question_parts: list[str] = []
    current_question_line = 0

    def flush_current_question() -> None:
        nonlocal current_question_parts
        nonlocal current_question_line

        if not current_question_parts:
            return

        question = normalize_question(" ".join(current_question_parts))
        if question and not is_open_questions_placeholder(question):
            questions.append(OpenQuestion(path=path, line=current_question_line, question=question))

        current_question_parts = []
        current_question_line = 0

    for line_number, raw_line in enumerate(read_text(path).splitlines(), start=1):
        line = raw_line.rstrip()

        if line == OPEN_QUESTIONS_HEADING:
            flush_current_question()
            in_open_questions_section = True
            continue

        if in_open_questions_section and is_section_heading(line):
            flush_current_question()
            in_open_questions_section = False
            continue

        if not in_open_questions_section:
            continue

        stripped_line = line.strip()
        if not stripped_line:
            flush_current_question()
            continue

        if line.startswith(LIST_ITEM_PREFIX):
            flush_current_question()
            current_question_parts = [line.removeprefix(LIST_ITEM_PREFIX)]
            current_question_line = line_number
            continue

        if current_question_parts and line.startswith(CONTINUATION_PREFIX):
            current_question_parts.append(stripped_line)

    flush_current_question()
    return questions


def extract_open_questions() -> list[OpenQuestion]:
    return [question for page in wiki_pages() for question in extract_open_questions_from_page(page)]
