#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Estimates tokens in private and publishable SKILL.md files.

from __future__ import annotations

import argparse
import csv
import sys
from collections.abc import Iterator, Sequence
from contextlib import nullcontext
from pathlib import Path
from typing import TextIO

from estimate_file_tokens import DEFAULT_ENCODING, TokenEncoder, estimate_tokens, load_encoding


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOTS = (
    ("private", Path(".agents/skills")),
    ("publishable", Path("skills")),
)


def iter_skill_files(root: Path) -> Iterator[tuple[str, Path]]:
    """Yield private and publishable SKILL.md files in stable path order."""

    for visibility, relative_root in SKILL_ROOTS:
        skill_root = root / relative_root
        if not skill_root.is_dir():
            continue
        for path in sorted(skill_root.rglob("SKILL.md")):
            if path.is_file():
                yield visibility, path


def estimate_skill_tokens(
    root: Path,
    encoding_name: str = DEFAULT_ENCODING,
    *,
    encoder: TokenEncoder | None = None,
) -> list[tuple[str, Path, int]]:
    """Return visibility, relative path, and token count for each skill file."""

    selected_encoder = encoder or load_encoding(encoding_name)
    return [
        (
            visibility,
            path.relative_to(root),
            estimate_tokens(path, encoding_name, encoder=selected_encoder),
        )
        for visibility, path in iter_skill_files(root)
    ]


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""

    parser = argparse.ArgumentParser(
        description="Estimate tokens in private and publishable repository SKILL.md files."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=ROOT,
        help="Repository root (default: root containing this script)",
    )
    parser.add_argument(
        "--encoding",
        default=DEFAULT_ENCODING,
        help=f"tiktoken encoding name (default: {DEFAULT_ENCODING})",
    )
    parser.add_argument(
        "--csv",
        type=Path,
        metavar="OUTPUT",
        help="Write CSV rows to OUTPUT instead of text; use - for standard output",
    )
    return parser


def write_csv(estimates: Sequence[tuple[str, Path, int]], output: TextIO) -> None:
    """Write one rectangular CSV row per skill file."""

    writer = csv.writer(output)
    writer.writerow(("visibility", "path", "tokens"))
    for visibility, path, count in estimates:
        writer.writerow((visibility, str(path), count))


def write_text(estimates: Sequence[tuple[str, Path, int]], output: TextIO) -> None:
    """Write the human-readable per-file report and aggregate totals."""

    totals = {visibility: 0 for visibility, _relative_root in SKILL_ROOTS}
    for visibility, path, count in estimates:
        totals[visibility] += count
        print(f"{count}\t{visibility}\t{path}", file=output)

    print(file=output)
    for visibility, _relative_root in SKILL_ROOTS:
        file_count = sum(
            1
            for item_visibility, _path, _count in estimates
            if item_visibility == visibility
        )
        print(
            f"{totals[visibility]}\t{visibility} total\t{file_count} files",
            file=output,
        )
    print(
        f"{sum(totals.values())}\tall skills total\t{len(estimates)} files",
        file=output,
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Run the repository skill token estimator."""

    args = build_parser().parse_args(argv)
    root = args.root.resolve()
    try:
        estimates = estimate_skill_tokens(root, args.encoding)
    except (OSError, UnicodeError, RuntimeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    try:
        if args.csv is None:
            write_text(estimates, sys.stdout)
        else:
            output_context = (
                nullcontext(sys.stdout)
                if str(args.csv) == "-"
                else args.csv.open("w", encoding="utf-8", newline="")
            )
            with output_context as output:
                write_csv(estimates, output)
    except OSError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
