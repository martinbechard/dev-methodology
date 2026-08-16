#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Estimates the tiktoken token count of one UTF-8 text file.

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Protocol, Sequence


DEFAULT_ENCODING = "cl100k_base"


class TokenEncoder(Protocol):
    """Describe the tiktoken encoder operation used by this script."""

    def encode(self, text: str, *, disallowed_special: tuple[()] = ()) -> list[int]:
        """Encode text as token identifiers."""


def load_encoding(encoding_name: str) -> TokenEncoder:
    """Load one named tiktoken encoding with a useful dependency error."""

    try:
        import tiktoken
    except ImportError as error:
        raise RuntimeError(
            "tiktoken is required; install it with `python -m pip install tiktoken`."
        ) from error
    return tiktoken.get_encoding(encoding_name)


def estimate_tokens(
    path: Path,
    encoding_name: str = DEFAULT_ENCODING,
    *,
    encoder: TokenEncoder | None = None,
) -> int:
    """Return the number of tokens in one UTF-8 text file."""

    text = path.read_text(encoding="utf-8")
    selected_encoder = encoder or load_encoding(encoding_name)
    return len(selected_encoder.encode(text, disallowed_special=()))


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""

    parser = argparse.ArgumentParser(
        description="Estimate the tiktoken token count of a UTF-8 text file."
    )
    parser.add_argument("file", type=Path, help="File to measure")
    parser.add_argument(
        "--encoding",
        default=DEFAULT_ENCODING,
        help=f"tiktoken encoding name (default: {DEFAULT_ENCODING})",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the file token estimator."""

    args = build_parser().parse_args(argv)
    try:
        count = estimate_tokens(args.file, args.encoding)
    except (OSError, UnicodeError, RuntimeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"{count}\t{args.file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
