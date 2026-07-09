"""Open Knowledge Format migration and validation helpers."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .constants import (
    CODE_FENCE_MARKER,
    INDEX_PAGE_NAME,
    MARKDOWN_FILE_SUFFIX,
    OKF_DEFAULT_TYPE,
    OKF_DESCRIPTION_MAX_LENGTH,
    OKF_DESCRIPTION_STOP_SUFFIXES,
    OKF_FRONTMATTER_DELIMITER,
    OKF_PATH_TYPES,
    OKF_REQUIRED_FRONTMATTER_FIELD,
    OKF_RESERVED_FILE_NAMES,
    OKF_ROOT_FILE_TYPES,
    WIKI_DIR,
)
from .core import extract_h1_title, read_text, relative_path, wiki_pages, write_text
from .models import LintResult


MARKDOWN_LINK_TEXT_PATTERN = re.compile(r"\[([^\]]+)\]\([^)]+\)")
HTML_TAG_PATTERN = re.compile(r"<[^>]+>")


@dataclass(frozen=True)
class OkfMigrationResult:
    path: Path
    changed: bool


def is_okf_reserved_file(path: Path) -> bool:
    return path.name in OKF_RESERVED_FILE_NAMES


def has_frontmatter(text: str) -> bool:
    lines = text.splitlines()
    return bool(lines) and lines[0] == OKF_FRONTMATTER_DELIMITER


def split_frontmatter(text: str) -> tuple[dict[str, object], str, bool]:
    if not has_frontmatter(text):
        return {}, text, False

    lines = text.splitlines(keepends=True)
    closing_index = 0
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == OKF_FRONTMATTER_DELIMITER:
            closing_index = index
            break

    if closing_index == 0:
        return {}, text, False

    frontmatter_text = "".join(lines[1:closing_index])
    body = "".join(lines[closing_index + 1 :]).lstrip("\n")
    return parse_simple_frontmatter(frontmatter_text), body, True


def parse_simple_frontmatter(frontmatter_text: str) -> dict[str, object]:
    parsed: dict[str, object] = {}
    for raw_line in frontmatter_text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, raw_value = line.split(":", maxsplit=1)
        key = key.strip()
        value = raw_value.strip()
        if not key:
            continue
        parsed[key] = parse_simple_value(value)
    return parsed


def parse_simple_value(value: str) -> object:
    if value.startswith("[") and value.endswith("]"):
        inner = value.removeprefix("[").removesuffix("]").strip()
        if not inner:
            return []
        return [strip_yaml_quotes(part.strip()) for part in inner.split(",")]
    return strip_yaml_quotes(value)


def strip_yaml_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def concept_pages() -> list[Path]:
    return [page for page in wiki_pages() if page.suffix == MARKDOWN_FILE_SUFFIX and not is_okf_reserved_file(page)]


def wiki_relative_parts(path: Path) -> tuple[str, ...]:
    if path.is_relative_to(WIKI_DIR):
        return path.relative_to(WIKI_DIR).parts
    parts = path.parts
    for index, part in enumerate(parts[:-1]):
        if part == "docs" and parts[index + 1] == "wiki":
            return parts[index + 2 :]
    return (path.name,)


def infer_type(path: Path) -> str:
    if path.parent == WIKI_DIR:
        return OKF_ROOT_FILE_TYPES.get(path.name, OKF_DEFAULT_TYPE)
    relative_parts = wiki_relative_parts(path)
    if len(relative_parts) == 1:
        return OKF_ROOT_FILE_TYPES.get(path.name, OKF_DEFAULT_TYPE)
    return OKF_PATH_TYPES.get(relative_parts[0], OKF_DEFAULT_TYPE)


def infer_tags(path: Path) -> list[str]:
    relative_parts = Path(*wiki_relative_parts(path)).with_suffix("").parts
    tags: list[str] = []
    for part in relative_parts[:-1]:
        tag = part.strip()
        if tag and tag not in tags:
            tags.append(tag)
    return tags


def infer_description(body: str) -> str:
    in_code_fence = False
    in_html_comment = False
    for raw_line in body.splitlines():
        line = raw_line.strip()
        if line.startswith(CODE_FENCE_MARKER):
            in_code_fence = not in_code_fence
            continue
        if in_code_fence:
            continue
        if in_html_comment:
            if "-->" in line:
                in_html_comment = False
            continue
        if line.startswith("<!--"):
            if "-->" not in line:
                in_html_comment = True
            continue
        if not line or line.startswith("#") or line.startswith("|"):
            continue
        if line.startswith("- "):
            line = line.removeprefix("- ").strip()
        line = plain_text_description(line)
        if not line:
            continue
        return shorten_description(line)
    return ""


def plain_text_description(description: str) -> str:
    without_links = MARKDOWN_LINK_TEXT_PATTERN.sub(r"\1", description)
    without_tags = HTML_TAG_PATTERN.sub("", without_links)
    return " ".join(without_tags.split())


def shorten_description(description: str) -> str:
    normalized = " ".join(description.split())
    if len(normalized) <= OKF_DESCRIPTION_MAX_LENGTH:
        return normalized
    clipped = normalized[: OKF_DESCRIPTION_MAX_LENGTH + 1]
    last_sentence = max(clipped.rfind(suffix) for suffix in OKF_DESCRIPTION_STOP_SUFFIXES)
    if last_sentence > 0:
        return clipped[: last_sentence + 1]
    last_space = clipped.rfind(" ")
    if last_space > 0:
        return clipped[:last_space].rstrip() + "..."
    return clipped[:OKF_DESCRIPTION_MAX_LENGTH].rstrip() + "..."


def yaml_scalar(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def yaml_list(values: list[str]) -> str:
    return "[" + ", ".join(yaml_scalar(value) for value in values) + "]"


def build_frontmatter(path: Path, body: str, existing: dict[str, object] | None = None) -> dict[str, object]:
    existing = existing or {}
    title = str(existing.get("title") or extract_h1_title(body) or path.with_suffix("").name.replace("-", " ").title())
    metadata: dict[str, object] = {
        OKF_REQUIRED_FRONTMATTER_FIELD: str(existing.get(OKF_REQUIRED_FRONTMATTER_FIELD) or infer_type(path)),
        "title": title,
    }
    description = infer_description(body) or str(existing.get("description") or "")
    if description:
        metadata["description"] = description
    tags = existing.get("tags")
    if isinstance(tags, list):
        normalized_tags = [str(tag) for tag in tags if str(tag)]
    else:
        normalized_tags = infer_tags(path)
    if normalized_tags:
        metadata["tags"] = normalized_tags
    for key, value in existing.items():
        if key not in metadata:
            metadata[key] = value
    return metadata


def format_frontmatter(metadata: dict[str, object]) -> str:
    lines = [OKF_FRONTMATTER_DELIMITER]
    for key, value in metadata.items():
        if isinstance(value, list):
            lines.append(f"{key}: {yaml_list([str(item) for item in value])}")
        else:
            lines.append(f"{key}: {yaml_scalar(str(value))}")
    lines.append(OKF_FRONTMATTER_DELIMITER)
    return "\n".join(lines) + "\n\n"


def migrate_page_to_okf(path: Path, dry_run: bool = False) -> OkfMigrationResult:
    original_text = read_text(path)
    existing, body, parsed = split_frontmatter(original_text)
    if is_okf_reserved_file(path):
        return OkfMigrationResult(path=path, changed=False)

    metadata = build_frontmatter(path, body, existing if parsed else None)
    migrated_text = format_frontmatter(metadata) + body
    changed = migrated_text != original_text
    if changed and not dry_run:
        write_text(path, migrated_text)
    return OkfMigrationResult(path=path, changed=changed)


def migrate_wiki_to_okf(dry_run: bool = False) -> list[OkfMigrationResult]:
    return [migrate_page_to_okf(page, dry_run) for page in concept_pages()]


def validate_okf_page(path: Path) -> list[LintResult]:
    text = read_text(path)
    findings: list[LintResult] = []
    if is_okf_reserved_file(path):
        if has_frontmatter(text) and not (path.parent == WIKI_DIR and path.name == INDEX_PAGE_NAME):
            findings.append(LintResult(path, "OKF reserved file must not use frontmatter"))
        if not text.startswith("# "):
            findings.append(LintResult(path, "OKF reserved file must start with a level one heading"))
        return findings

    frontmatter, _body, parsed = split_frontmatter(text)
    if not parsed:
        findings.append(LintResult(path, "OKF concept document must start with YAML frontmatter"))
        return findings
    concept_type = frontmatter.get(OKF_REQUIRED_FRONTMATTER_FIELD)
    if not isinstance(concept_type, str) or not concept_type.strip():
        findings.append(LintResult(path, "OKF concept document must have non-empty type frontmatter"))
    return findings


def validate_okf_wiki() -> list[LintResult]:
    findings: list[LintResult] = []
    for page in wiki_pages():
        findings.extend(validate_okf_page(page))
    return findings


def okf_summary(results: list[OkfMigrationResult]) -> tuple[int, int]:
    changed_count = sum(1 for result in results if result.changed)
    return changed_count, len(results)
