#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies Java comment-placement outputs against protected exact goldens and negative fixtures.

from __future__ import annotations

import re
from pathlib import Path, PurePosixPath


FIELD_PREFIXES = {
    "Copyright": "Copyright",
    "AI attribution": "AI attribution:",
    "Responsibility": "Responsibility:",
    "Design": "Design:",
    "Test plan": "Test plan:",
}

REQUIRED_EVIDENCE_HEADINGS = (
    "JAVA-COMMENT-PACKAGE",
    "JAVA-COMMENT-PACKAGED-TYPE",
    "JAVA-COMMENT-NO-PACKAGE",
    "JAVA-COMMENT-DUPLICATE-REJECTED",
    "JAVA-COMMENT-MISSING-REJECTED",
    "REVIEW-SYNTHESIS",
)
EVIDENCE_FIELDS = ("Affected path", "Verification result")
FENCE_OPEN_PATTERN = re.compile(r"^ {0,3}(?P<fence>`{3,}|~{3,}).*$")
EXACT_HEADING_PATTERN = re.compile(r"^## (?P<title>\S(?:.*\S)?)$")
PATH_SCHEME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")


def comment_blocks(text: str) -> list[tuple[int, int, str, bool]]:
    """Return block comments with exact spans and their Javadoc classification."""
    blocks: list[tuple[int, int, str, bool]] = []
    position = 0
    while True:
        start = text.find("/*", position)
        if start < 0:
            return blocks
        close = text.find("*/", start + 2)
        if close < 0:
            blocks.append((start, len(text), text[start:], text.startswith("/**", start)))
            return blocks
        end = close + 2
        blocks.append((start, end, text[start:end], text.startswith("/**", start)))
        position = end


def declaration_line(golden_text: str, golden_path: Path) -> str:
    """Return the exact package or public type declaration owned by one golden."""
    if golden_path.name == "package-info.java":
        prefix = "package "
    else:
        prefix = "public "
    declarations = [line for line in golden_text.splitlines() if line.startswith(prefix)]
    if len(declarations) != 1:
        raise ValueError(f"{golden_path}: expected one {prefix.strip()} declaration")
    return declarations[0]


def attached_javadoc_span(text: str, golden_path: Path) -> tuple[int, int, str] | None:
    """Return only the Javadoc immediately attached to the golden-owned declaration."""
    golden_text = golden_path.read_text(encoding="utf-8")
    declaration = declaration_line(golden_text, golden_path)
    declaration_positions: list[int] = []
    position = 0
    while True:
        found = text.find(declaration, position)
        if found < 0:
            break
        declaration_positions.append(found)
        position = found + len(declaration)
    if len(declaration_positions) != 1:
        return None

    declaration_start = declaration_positions[0]
    prefix = text[:declaration_start].rstrip()
    if not prefix.endswith("*/"):
        return None
    end = len(prefix)
    start = prefix.rfind("/**")
    if start < 0:
        return None
    comment = text[start:end]
    if "*/" in comment[:-2]:
        return None
    return start, end, comment


def attached_javadoc(text: str, golden_path: Path) -> str:
    """Return the exact Javadoc attached to the golden-owned declaration, if any."""
    attached = attached_javadoc_span(text, golden_path)
    return "" if attached is None else attached[2]


def documentation_lines(comment: str) -> list[str]:
    """Return normalized content lines from one complete Javadoc block."""
    if not comment.startswith("/**") or not comment.endswith("*/"):
        return []
    lines: list[str] = []
    for source_line in comment[3:-2].splitlines():
        line = source_line.strip()
        if line.startswith("*"):
            line = line[1:].strip()
        lines.append(line)
    return lines


def metadata_values(comment: str) -> dict[str, list[str]]:
    """Return every declared metadata value without collapsing duplicates."""
    values = {label: [] for label in FIELD_PREFIXES}
    for line in documentation_lines(comment):
        for label, prefix in FIELD_PREFIXES.items():
            if line == prefix:
                values[label].append("")
            elif label == "Copyright" and line.startswith(prefix + " "):
                values[label].append(line)
            elif label != "Copyright" and line.startswith(prefix):
                values[label].append(line[len(prefix) :].strip())
    return values


def public_documentation(comment: str) -> list[str]:
    """Return non-metadata public prose from one Javadoc block."""
    prose: list[str] = []
    for line in documentation_lines(comment):
        if not line:
            continue
        if any(
            line == prefix
            or (label == "Copyright" and line.startswith(prefix + " "))
            or (label != "Copyright" and line.startswith(prefix))
            for label, prefix in FIELD_PREFIXES.items()
        ):
            continue
        prose.append(line)
    return prose


def validate_java(path: Path, golden_path: Path) -> list[str]:
    """Return exact value, prose, attachment, duplication, and golden mismatches."""
    text = path.read_text(encoding="utf-8")
    golden_text = golden_path.read_text(encoding="utf-8")
    errors: list[str] = []
    golden_attached = attached_javadoc_span(golden_text, golden_path)
    if golden_attached is None:
        raise ValueError(f"{golden_path}: protected golden lacks attached Javadoc")
    expected_comment = golden_attached[2]
    expected_values = metadata_values(expected_comment)
    for label, values in expected_values.items():
        if len(values) != 1 or not values[0]:
            raise ValueError(f"{golden_path}: protected {label} value must be exact and non-empty")

    attached = attached_javadoc_span(text, golden_path)
    attached_span = None if attached is None else (attached[0], attached[1])
    candidate_comment = "" if attached is None else attached[2]
    candidate_values = metadata_values(candidate_comment)
    for label, expected in expected_values.items():
        values = candidate_values[label]
        if not values:
            errors.append(f"{path}: {label} is missing from attached Javadoc")
        elif len(values) > 1:
            errors.append(f"{path}: duplicate required metadata for {label}")
        elif not values[0]:
            errors.append(f"{path}: {label} value is blank")
        elif values[0] != expected[0]:
            errors.append(f"{path}: {label} value differs from protected golden")

    all_values = {label: [] for label in FIELD_PREFIXES}
    for start, end, comment, is_javadoc in comment_blocks(text):
        block_values = metadata_values(comment if is_javadoc else "/**" + comment[2:])
        carries_metadata = any(block_values[label] for label in FIELD_PREFIXES)
        for label in FIELD_PREFIXES:
            all_values[label].extend(block_values[label])
        if not carries_metadata:
            continue
        if not is_javadoc:
            errors.append(f"{path}: standalone metadata comment is forbidden")
        elif attached_span != (start, end):
            errors.append(f"{path}: metadata-bearing Javadoc is not attached to the declaration")

    for label, values in all_values.items():
        if len(values) > 1:
            errors.append(f"{path}: duplicate required metadata for {label}")

    if attached is None:
        errors.append(f"{path}: declaration lacks an attached metadata-bearing Javadoc")
    elif public_documentation(candidate_comment) != public_documentation(expected_comment):
        errors.append(f"{path}: public documentation differs from protected golden")

    if text != golden_text:
        errors.append(f"{path}: output differs from protected golden")
    return list(dict.fromkeys(errors))


def validate_negative_fixtures(root: Path) -> list[str]:
    """Confirm frozen duplicate and missing-information fixtures remain rejected."""
    golden_root = root / "negative-fixtures" / "golden"
    duplicate_errors = validate_java(
        root / "negative-fixtures" / "duplicate" / "DuplicateHeader.java",
        golden_root / "OrderService.java",
    )
    missing_errors = validate_java(
        root / "negative-fixtures" / "missing" / "MissingInformation.java",
        golden_root / "OrderImport.java",
    )
    failures: list[str] = []
    if not any("standalone metadata" in error for error in duplicate_errors):
        failures.append("duplicate fixture did not reject standalone metadata")
    if not any("duplicate required metadata" in error for error in duplicate_errors):
        failures.append("duplicate fixture did not reject repeated required fields")
    if not any("Test plan is missing" in error for error in missing_errors):
        failures.append("missing-information fixture did not reject the absent test plan")
    return failures


def markdown_sections(text: str) -> dict[str, list[str]]:
    """Return records delimited by exact heading lines outside fenced code."""
    sections: dict[str, list[str]] = {}
    current_title: str | None = None
    current_lines: list[str] = []
    fence_character: str | None = None
    fence_length = 0

    def finish_section() -> None:
        if current_title is not None:
            sections.setdefault(current_title, []).append("\n".join(current_lines).strip())

    for line in text.splitlines():
        if fence_character is not None:
            closing = re.fullmatch(
                rf" {{0,3}}{re.escape(fence_character)}{{{fence_length},}}[ \t]*",
                line,
            )
            if closing:
                fence_character = None
                fence_length = 0
            continue

        fence = FENCE_OPEN_PATTERN.fullmatch(line)
        if fence:
            marker = fence.group("fence")
            fence_character = marker[0]
            fence_length = len(marker)
            continue

        heading = EXACT_HEADING_PATTERN.fullmatch(line)
        if heading:
            finish_section()
            current_title = heading.group("title")
            current_lines = []
        elif current_title is not None:
            current_lines.append(line)

    finish_section()
    return sections


def evidence_field_values(content: str, field: str) -> list[str]:
    """Return exact non-commentary values for one required evidence field."""
    pattern = re.compile(rf"^{re.escape(field)}:[ \t]*(.*)$", re.MULTILINE)
    return [match.group(1).strip() for match in pattern.finditer(content)]


def is_repository_relative_path(value: str) -> bool:
    """Return whether one evidence value uses repository-relative POSIX syntax."""
    if (
        not value
        or value.startswith(("/", "~"))
        or "\x00" in value
        or "\\" in value
        or "<" in value
        or ">" in value
        or PATH_SCHEME_PATTERN.match(value)
    ):
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and path != PurePosixPath(".") and ".." not in path.parts


def validate_evidence(text: str) -> list[str]:
    """Validate required Markdown sections and their non-empty evidence fields."""
    sections = markdown_sections(text)
    errors: list[str] = []
    for heading in REQUIRED_EVIDENCE_HEADINGS:
        matches = sections.get(heading, [])
        if not matches:
            errors.append(f"missing required Markdown heading: {heading}")
            continue
        if len(matches) > 1:
            errors.append(f"duplicate required Markdown heading: {heading}")
            continue

        content = matches[0]
        for field in EVIDENCE_FIELDS:
            values = evidence_field_values(content, field)
            if not values:
                errors.append(f"{heading}: missing {field} field")
            elif len(values) > 1:
                errors.append(f"{heading}: duplicate {field} field")
            elif not values[0]:
                errors.append(f"{heading}: {field} value is blank")
        affected_paths = evidence_field_values(content, "Affected path")
        if len(affected_paths) == 1 and affected_paths[0] and not is_repository_relative_path(
            affected_paths[0]
        ):
            errors.append(f"{heading}: Affected path must be repository-relative")
    return errors


def main() -> None:
    """Validate editable sources, protected goldens, frozen negatives, and evidence."""
    root = Path(__file__).resolve().parent
    golden_root = root / "negative-fixtures" / "golden"
    source_goldens = (
        (
            root / "src" / "main" / "java" / "com" / "example" / "orders" / "package-info.java",
            golden_root / "package-info.java",
        ),
        (
            root / "src" / "main" / "java" / "com" / "example" / "orders" / "OrderService.java",
            golden_root / "OrderService.java",
        ),
        (
            root / "src" / "main" / "java" / "OrderImport.java",
            golden_root / "OrderImport.java",
        ),
    )
    source_errors = [
        error
        for source, golden in source_goldens
        for error in validate_java(source, golden)
    ]
    if source_errors:
        raise SystemExit("source verification failed:\n" + "\n".join(source_errors))

    negative_errors = validate_negative_fixtures(root)
    if negative_errors:
        raise SystemExit("negative fixture verification failed:\n" + "\n".join(negative_errors))

    evidence = root / "eval-result.md"
    evidence_text = evidence.read_text(encoding="utf-8") if evidence.is_file() else ""
    evidence_errors = validate_evidence(evidence_text)
    if evidence_errors:
        raise SystemExit("evaluation evidence failed:\n" + "\n".join(evidence_errors))


if __name__ == "__main__":
    main()
