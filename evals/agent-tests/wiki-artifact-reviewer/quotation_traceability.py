# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Resolves exact quotation evidence against named frozen review sources.
# Governing design: evals/agent-tests/wiki-artifact-reviewer/skills/wiki-artifact-reviewer-suite-contract/SKILL.md
# Governing test plan: evals/agent-tests/wiki-artifact-reviewer/scenarios.yaml

from __future__ import annotations

import argparse
import json
from pathlib import Path


_EXACT_TYPE = "- Evidence type: exact quotation"
_SOURCE_FIELD = "- Evidence source:"
_EVIDENCE_FIELD = "- Evidence:"
_OMISSION = "[omitted]"


def _normalized_text(path: Path) -> str:
    return path.read_bytes().decode("utf-8").replace("\r\n", "\n")


def _exact_records(review_text: str) -> list[tuple[int, str | None, str | None]]:
    lines = review_text.split("\n")
    records: list[tuple[int, str | None, str | None]] = []
    index = 0
    while index < len(lines):
        if lines[index].strip() != _EXACT_TYPE:
            index += 1
            continue
        start_line = index + 1
        source: str | None = None
        quotation: str | None = None
        index += 1
        while index < len(lines) and not lines[index].strip().startswith("- Evidence type:"):
            stripped = lines[index].strip()
            if stripped.startswith(_SOURCE_FIELD):
                source = stripped.removeprefix(_SOURCE_FIELD).strip()
            elif stripped.startswith(_EVIDENCE_FIELD):
                inline_evidence = stripped.removeprefix(_EVIDENCE_FIELD).strip()
                if inline_evidence:
                    quotation = inline_evidence
                    index += 1
                    continue
                quoted_lines: list[str] = []
                index += 1
                while index < len(lines):
                    candidate = lines[index].lstrip()
                    if not candidate.startswith(">"):
                        break
                    value = candidate[1:]
                    quoted_lines.append(value[1:] if value.startswith(" ") else value)
                    index += 1
                quotation = "\n".join(quoted_lines)
                continue
            index += 1
        records.append((start_line, source, quotation))
    return records


def _occurs_exactly(quotation: str, source_text: str) -> bool:
    if _OMISSION not in quotation:
        return quotation in source_text
    segments = quotation.split(_OMISSION)
    if any(not segment for segment in segments):
        return False
    cursor = 0
    for segment in segments:
        location = source_text.find(segment, cursor)
        if location < 0:
            return False
        cursor = location + len(segment)
    return True


def validate_review_quotations(review_path: Path, evidence_root: Path) -> list[str]:
    """Return source-specific diagnostics for unsupported exact quotation records.

    The review must name each evidence source relative to evidence_root. Only line
    endings are normalized. The literal [omitted] marker may replace intervening
    source text, but every retained segment must occur exactly and in source order.
    Missing, malformed, unreadable, or escaping sources produce diagnostics rather
    than exceptions so a retained review can surface the evidence gap.
    """
    diagnostics: list[str] = []
    root = evidence_root.resolve()
    try:
        records = _exact_records(_normalized_text(review_path))
    except (OSError, UnicodeError) as error:
        return [f"review evidence is unreadable: {error}"]
    for line, source, quotation in records:
        if not source:
            diagnostics.append(f"line {line}: exact quotation has no named evidence source")
            continue
        if not quotation:
            diagnostics.append(f"line {line}: exact quotation has no evidence text")
            continue
        try:
            source_path = (root / source).resolve()
            source_path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            diagnostics.append(f"line {line}: evidence source is outside the evidence root: {source}")
            continue
        try:
            source_text = _normalized_text(source_path)
        except (OSError, UnicodeError) as error:
            diagnostics.append(f"line {line}: evidence source is unreadable: {source}: {error}")
            continue
        if not _occurs_exactly(quotation, source_text):
            diagnostics.append(
                f"line {line}: quoted evidence does not occur exactly in {source}"
            )
    return diagnostics


def main() -> int:
    """Validate one retained review and print a deterministic JSON disposition."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review", required=True, type=Path)
    parser.add_argument("--evidence-root", required=True, type=Path)
    arguments = parser.parse_args()
    diagnostics = validate_review_quotations(arguments.review, arguments.evidence_root)
    print(json.dumps({"valid": not diagnostics, "diagnostics": diagnostics}, sort_keys=True))
    return 0 if not diagnostics else 3


if __name__ == "__main__":
    raise SystemExit(main())
