# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Resolves and validates local Markdown links from a saved Wiki Researcher report.

from __future__ import annotations

import argparse
import os
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit


_MARKDOWN_LINK_START = re.compile(r"!?\[[^\]]*\]\(\s*")
_MARKDOWN_REFERENCE = re.compile(
    r"(?m)^[ \t]{0,3}\[[^\]]+\]:[ \t]*(?P<target><[^>\n]+>|\S+)"
)


class SourceLinkValidationError(ValueError):
    """Signals that a saved report contains one or more invalid local links."""


def relative_source_link(report_path: Path, source_path: Path, repository_root: Path) -> str:
    """Return a portable local link from a report location to one repository source.

    The report may not exist yet, but its intended location and the source must remain
    inside repository_root. The source must already exist. The function performs no I/O
    other than resolving the source and repository paths and raises ValueError when a
    path crosses the repository boundary or the source is missing.
    """

    root = repository_root.resolve(strict=True)
    report = report_path.resolve()
    source = source_path.resolve(strict=True)
    _require_within_repository(report, root, "report")
    _require_within_repository(source, root, "source")
    if not source.is_file():
        raise ValueError(f"source path is not a file: {source}")
    return Path(os.path.relpath(source, report.parent)).as_posix()


def validate_report_links(report_path: Path, repository_root: Path) -> tuple[str, ...]:
    """Return deterministic diagnostics for invalid local links in one saved report.

    HTTP and other URI schemes, protocol-relative URLs, and document-only fragments are
    external to this filesystem check. Every other Markdown link is resolved from the
    report's parent directory. Missing, absolute, malformed, or repository-escaping
    local targets produce diagnostics; reading failures propagate to the caller.
    """

    root = repository_root.resolve(strict=True)
    report = report_path.resolve(strict=True)
    _require_within_repository(report, root, "report")
    diagnostics: list[str] = []
    contents = report.read_text(encoding="utf-8")
    reference_targets = (match.group("target") for match in _MARKDOWN_REFERENCE.finditer(contents))
    for raw_target in (*_inline_link_targets(contents), *reference_targets):
        target = raw_target[1:-1] if raw_target.startswith("<") else raw_target
        if _is_external_link(target):
            continue
        parsed = urlsplit(target)
        local_path = unquote(parsed.path)
        if not local_path:
            continue
        if "\\" in local_path:
            diagnostics.append(f"local link uses non-portable separators: {target}")
            continue
        relative = Path(local_path)
        if relative.is_absolute():
            diagnostics.append(f"local link must be report-relative: {target}")
            continue
        candidate = (report.parent / relative).resolve()
        try:
            _require_within_repository(candidate, root, "link")
        except ValueError:
            diagnostics.append(f"local link escapes repository: {target}")
            continue
        if not candidate.is_file():
            diagnostics.append(f"local link does not resolve from report: {target}")
    return tuple(diagnostics)


def require_valid_report_links(report_path: Path, repository_root: Path) -> None:
    """Fail before handoff when any local Markdown link in a saved report is invalid.

    Callers pass the final report location and repository root after saving and before
    committing. The function has no side effects and raises SourceLinkValidationError
    with every deterministic diagnostic when validation fails.
    """

    diagnostics = validate_report_links(report_path, repository_root)
    if diagnostics:
        raise SourceLinkValidationError("\n".join(diagnostics))


def _is_external_link(target: str) -> bool:
    return target.startswith(("#", "//")) or bool(urlsplit(target).scheme)


def _inline_link_targets(contents: str) -> tuple[str, ...]:
    targets: list[str] = []
    for match in _MARKDOWN_LINK_START.finditer(contents):
        start = match.end()
        if start < len(contents) and contents[start] == "<":
            closing = contents.find(">", start + 1)
            if closing != -1:
                targets.append(contents[start : closing + 1])
            continue
        target: list[str] = []
        depth = 0
        position = start
        while position < len(contents):
            character = contents[position]
            if character == "\\" and position + 1 < len(contents):
                target.append(contents[position + 1])
                position += 2
                continue
            if character == "(":
                depth += 1
            elif character == ")":
                if depth == 0:
                    break
                depth -= 1
            elif character.isspace() and depth == 0:
                break
            target.append(character)
            position += 1
        if target:
            targets.append("".join(target))
    return tuple(targets)


def _require_within_repository(path: Path, root: Path, label: str) -> None:
    if path != root and root not in path.parents:
        raise ValueError(f"{label} path is outside repository: {path}")


def main() -> int:
    """Validate one final report path for fixture and supervisor command-line use."""

    parser = argparse.ArgumentParser()
    parser.add_argument("report", type=Path)
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    arguments = parser.parse_args()
    diagnostics = validate_report_links(arguments.report, arguments.repository_root)
    for diagnostic in diagnostics:
        print(diagnostic)
    return 1 if diagnostics else 0


if __name__ == "__main__":
    raise SystemExit(main())
