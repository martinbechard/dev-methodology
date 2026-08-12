#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Correlates linked Git worktrees with terminal archived work-item evidence by using ripgrep.
# Tests: .archive/2026-08-12-worktree-cleanup/scripts/test_audit_worktree_completion_links.py

"""Report likely links between registered worktrees and archived work items."""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import re
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Iterable, Sequence


SUCCESS_EXIT_CODE = 0
ERROR_EXIT_CODE = 1
DEFAULT_ARCHIVE_ROOTS = (
    Path("backlog/completed-backlog"),
    Path("backlog/failed-backlog"),
)
SIGNAL_SCORES = {
    "worktree-path": 100,
    "branch": 95,
    "head": 90,
    "head-short": 80,
    "basename": 60,
    "normalized-slug": 30,
}
TASK_TOKEN_PATTERN = re.compile(r"(?:^|-)(?:019[a-f0-9]{5,})(?=-|$)", re.IGNORECASE)
TRAILING_ROLE_PATTERN = re.compile(
    r"-(?:correction(?:-?\d+)?|retry(?:-?\d+)?|resume|verify|verification|"
    r"review|source|artifact|work|isolated|integration(?:-prep)?|current-main|"
    r"coder|reviewer|orchestrator)$",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Worktree:
    """One record from Git's registered worktree inventory."""

    path: Path
    head: str
    branch: str | None = None
    detached: bool = False
    prunable: str = ""
    dirty: bool | None = None
    head_in_main: bool | None = None


@dataclass(frozen=True)
class Signal:
    """One fixed-string archive query derived from a worktree."""

    value: str
    kind: str


@dataclass(frozen=True)
class SearchHit:
    """One archive line matched by ripgrep for one worktree."""

    path: Path
    line_number: int
    line: str
    signal_kinds: tuple[str, ...]
    worktree_path: Path | None = None


@dataclass(frozen=True)
class ArchiveMatch:
    """Ranked evidence linking one worktree to one archived work item."""

    path: Path
    confidence: str
    score: int
    signal_kinds: tuple[str, ...]
    evidence: tuple[str, ...]


@dataclass(frozen=True)
class Correlation:
    """All archived work-item candidates for one worktree."""

    worktree: Worktree
    confidence: str
    matches: tuple[ArchiveMatch, ...]


def _run(
    arguments: Sequence[str],
    *,
    cwd: Path,
    input_text: str | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(arguments),
        cwd=cwd,
        input=input_text,
        text=True,
        encoding="utf-8",
        errors="surrogateescape",
        capture_output=True,
        check=check,
    )


def parse_worktree_porcelain(payload: str) -> list[Worktree]:
    """Parse Git's line-oriented porcelain worktree representation."""

    worktrees: list[Worktree] = []
    current: dict[str, object] | None = None
    for line in payload.splitlines():
        if line.startswith("worktree "):
            if current is not None:
                worktrees.append(Worktree(**current))
            current = {"path": Path(line.removeprefix("worktree "))}
        elif current is None:
            continue
        elif line.startswith("HEAD "):
            current["head"] = line.removeprefix("HEAD ")
        elif line.startswith("branch "):
            current["branch"] = line.removeprefix("branch ").removeprefix("refs/heads/")
        elif line == "detached":
            current["detached"] = True
        elif line.startswith("prunable "):
            current["prunable"] = line.removeprefix("prunable ")
    if current is not None:
        worktrees.append(Worktree(**current))
    return worktrees


def normalized_slug(worktree: Worktree) -> str:
    """Remove common execution suffixes while retaining the work-item-shaped stem."""

    value = (worktree.branch or worktree.path.name).removeprefix("codex/").lower()
    value = TASK_TOKEN_PATTERN.sub("", value).strip("-")
    previous = ""
    while value != previous:
        previous = value
        value = TRAILING_ROLE_PATTERN.sub("", value).strip("-")
    return value


def signals_for(worktree: Worktree) -> tuple[Signal, ...]:
    """Build fixed-string queries with explicit confidence-bearing kinds."""

    candidates = [
        Signal(str(worktree.path), "worktree-path"),
        Signal(worktree.head, "head"),
        Signal(worktree.head[:12], "head-short"),
    ]
    codex_managed = ".codex" in worktree.path.parts and "worktrees" in worktree.path.parts
    if not codex_managed:
        candidates.append(Signal(worktree.path.name, "basename"))
    if worktree.branch:
        candidates.append(Signal(worktree.branch, "branch"))
    slug = normalized_slug(worktree) if worktree.branch or not codex_managed else ""
    if len(slug) >= 8:
        candidates.append(Signal(slug, "normalized-slug"))

    unique: dict[tuple[str, str], Signal] = {}
    for signal in candidates:
        if signal.value and "\n" not in signal.value and "\r" not in signal.value:
            unique[(signal.value.casefold(), signal.kind)] = signal
    return tuple(unique.values())


def _relative_archive_path(repo: Path, raw_path: str) -> Path:
    path = Path(raw_path)
    if not path.is_absolute():
        path = repo / path
    try:
        return path.resolve().relative_to(repo.resolve())
    except ValueError:
        return path.resolve()


def search_archives(
    repo: Path,
    archive_roots: Sequence[Path],
    worktrees: Sequence[Worktree],
    rg_executable: str,
) -> tuple[SearchHit, ...]:
    """Run one batched fixed-string ripgrep query and attribute hits to worktrees."""

    signal_owners: dict[str, list[tuple[Path, str]]] = defaultdict(list)
    signal_text: dict[str, str] = {}
    for worktree in worktrees:
        for signal in signals_for(worktree):
            folded = signal.value.casefold()
            signal_text.setdefault(folded, signal.value)
            signal_owners[folded].append((worktree.path, signal.kind))
    if not signal_text:
        return ()

    existing_roots = tuple(root for root in archive_roots if root.is_dir())
    if not existing_roots:
        raise ValueError("No archive roots exist")
    patterns = "\n".join(signal_text.values()) + "\n"
    command = [
        rg_executable,
        "--json",
        "--fixed-strings",
        "--ignore-case",
        "--glob",
        "*.md",
        "--file",
        "-",
        *(str(root) for root in existing_roots),
    ]
    completed = _run(command, cwd=repo, input_text=patterns, check=False)
    if completed.returncode not in (0, 1):
        raise RuntimeError(completed.stderr.strip() or "ripgrep archive search failed")

    hits: list[SearchHit] = []
    for raw_event in completed.stdout.splitlines():
        event = json.loads(raw_event)
        if event.get("type") != "match":
            continue
        data = event["data"]
        line = data["lines"]["text"].rstrip("\r\n")
        folded_line = line.casefold()
        owners: dict[Path, set[str]] = defaultdict(set)
        for folded_signal, signal_value in signal_text.items():
            if folded_signal in folded_line:
                for worktree_path, kind in signal_owners[folded_signal]:
                    owners[worktree_path].add(kind)
        archive_path = _relative_archive_path(repo, data["path"]["text"])
        for worktree_path, kinds in owners.items():
            hits.append(
                SearchHit(
                    path=archive_path,
                    line_number=int(data["line_number"]),
                    line=line,
                    signal_kinds=tuple(sorted(kinds)),
                    worktree_path=worktree_path,
                )
            )
    return tuple(hits)


def confidence_for_score(score: int) -> str:
    if score >= SIGNAL_SCORES["head-short"]:
        return "strong"
    if score >= SIGNAL_SCORES["basename"]:
        return "likely"
    if score > 0:
        return "possible"
    return "none"


def correlate_worktree(
    worktree: Worktree,
    hits: Sequence[SearchHit],
) -> Correlation:
    """Rank archived work items for one worktree from their strongest evidence."""

    grouped: dict[Path, list[SearchHit]] = defaultdict(list)
    for hit in hits:
        if hit.worktree_path is None or hit.worktree_path == worktree.path:
            grouped[hit.path].append(hit)

    matches: list[ArchiveMatch] = []
    for path, path_hits in grouped.items():
        kinds = tuple(sorted({kind for hit in path_hits for kind in hit.signal_kinds}))
        score = max((SIGNAL_SCORES.get(kind, 0) for kind in kinds), default=0)
        evidence = tuple(
            f"line {hit.line_number}: {hit.line.strip()}"
            for hit in sorted(path_hits, key=lambda item: item.line_number)[:3]
        )
        matches.append(
            ArchiveMatch(
                path=path,
                confidence=confidence_for_score(score),
                score=score,
                signal_kinds=kinds,
                evidence=evidence,
            )
        )
    matches.sort(key=lambda match: (-match.score, str(match.path)))
    confidence = matches[0].confidence if matches else "none"
    return Correlation(worktree=worktree, confidence=confidence, matches=tuple(matches))


def _inspect_worktree(repo: Path, worktree: Worktree) -> Worktree:
    if worktree.prunable or not worktree.path.is_dir():
        return worktree
    status = _run(
        ["git", "-C", str(worktree.path), "status", "--porcelain", "--untracked-files=normal"],
        cwd=repo,
        check=False,
    )
    ancestry = _run(
        ["git", "merge-base", "--is-ancestor", worktree.head, "main"],
        cwd=repo,
        check=False,
    )
    return replace(
        worktree,
        dirty=bool(status.stdout) if status.returncode == 0 else None,
        head_in_main=ancestry.returncode == 0,
    )


def collect_worktrees(repo: Path) -> tuple[Worktree, ...]:
    """Return inspected non-primary registered worktrees."""

    completed = _run(["git", "worktree", "list", "--porcelain"], cwd=repo)
    primary = repo.resolve()
    worktrees = tuple(
        worktree
        for worktree in parse_worktree_porcelain(completed.stdout)
        if worktree.path.resolve() != primary
    )
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
        inspected = tuple(executor.map(lambda item: _inspect_worktree(repo, item), worktrees))
    return inspected


def _summary(correlations: Sequence[Correlation]) -> Counter[str]:
    counts = Counter(correlation.confidence for correlation in correlations)
    counts["total"] = len(correlations)
    return counts


def _state(value: bool | None) -> str:
    if value is None:
        return "unknown"
    return "yes" if value else "no"


def render_text(repo: Path, correlations: Sequence[Correlation], *, summary_only: bool = False) -> str:
    """Render a compact human-readable audit."""

    counts = _summary(correlations)
    lines = [
        "Worktree completion-link audit",
        f"Repository: {repo}",
        (
            "Summary: "
            f"total={counts['total']} strong={counts['strong']} likely={counts['likely']} "
            f"possible={counts['possible']} none={counts['none']}"
        ),
    ]
    if summary_only:
        return "\n".join(lines) + "\n"

    for correlation in correlations:
        worktree = correlation.worktree
        identity = worktree.branch or f"detached:{worktree.head[:12]}"
        lines.append("")
        lines.append(
            f"[{correlation.confidence}] {identity} | {worktree.path} | "
            f"dirty={_state(worktree.dirty)} head-in-main={_state(worktree.head_in_main)}"
        )
        if not correlation.matches:
            lines.append("  no archived work-item match")
            continue
        for match in correlation.matches[:5]:
            kinds = ",".join(match.signal_kinds)
            lines.append(f"  {match.confidence}: {match.path} ({kinds})")
            for evidence in match.evidence:
                lines.append(f"    {evidence}")
        if len(correlation.matches) > 5:
            lines.append(f"  ... {len(correlation.matches) - 5} additional candidates")
    return "\n".join(lines) + "\n"


def render_json(repo: Path, correlations: Sequence[Correlation]) -> str:
    """Render the complete correlation report as stable JSON."""

    counts = _summary(correlations)
    payload = {
        "repository": str(repo),
        "summary": {key: counts[key] for key in ("total", "strong", "likely", "possible", "none")},
        "worktrees": [
            {
                "path": str(correlation.worktree.path),
                "branch": correlation.worktree.branch,
                "head": correlation.worktree.head,
                "detached": correlation.worktree.detached,
                "prunable": correlation.worktree.prunable or None,
                "dirty": correlation.worktree.dirty,
                "head_in_main": correlation.worktree.head_in_main,
                "confidence": correlation.confidence,
                "matches": [
                    {
                        "path": str(match.path),
                        "confidence": match.confidence,
                        "score": match.score,
                        "signal_kinds": list(match.signal_kinds),
                        "evidence": list(match.evidence),
                    }
                    for match in correlation.matches
                ],
            }
            for correlation in correlations
        ],
    }
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def _resolve_repo(path: Path) -> Path:
    completed = _run(["git", "rev-parse", "--show-toplevel"], cwd=path.resolve())
    return Path(completed.stdout.strip()).resolve()


def _archive_roots(repo: Path, supplied: Iterable[Path] | None) -> tuple[Path, ...]:
    relative_roots = tuple(supplied) if supplied else DEFAULT_ARCHIVE_ROOTS
    return tuple((root if root.is_absolute() else repo / root).resolve() for root in relative_roots)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd(), help="Repository or linked-worktree path")
    parser.add_argument(
        "--archive-root",
        action="append",
        type=Path,
        help="Archive root relative to the repository; repeat to override defaults",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--summary-only", action="store_true", help="Print only aggregate confidence counts")
    parser.add_argument("--rg", default="rg", help=argparse.SUPPRESS)
    return parser


def main(arguments: Sequence[str] | None = None) -> int:
    parser = build_parser()
    options = parser.parse_args(arguments)
    try:
        repo = _resolve_repo(options.repo)
        rg_executable = shutil.which(options.rg)
        if rg_executable is None:
            raise RuntimeError(f"ripgrep executable not found: {options.rg}")
        worktrees = collect_worktrees(repo)
        roots = _archive_roots(repo, options.archive_root)
        hits = search_archives(repo, roots, worktrees, rg_executable)
        correlations = tuple(correlate_worktree(worktree, hits) for worktree in worktrees)
        correlations = tuple(
            sorted(
                correlations,
                key=lambda item: (
                    {"strong": 0, "likely": 1, "possible": 2, "none": 3}[item.confidence],
                    item.worktree.branch or "",
                    str(item.worktree.path),
                ),
            )
        )
        if options.format == "json":
            sys.stdout.write(render_json(repo, correlations))
        else:
            sys.stdout.write(render_text(repo, correlations, summary_only=options.summary_only))
        return SUCCESS_EXIT_CODE
    except (OSError, subprocess.CalledProcessError, RuntimeError, ValueError) as error:
        parser.exit(ERROR_EXIT_CODE, f"error: {error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
