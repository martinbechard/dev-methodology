#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies that terminology-negative evidence is preserved byte-for-byte.

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Sequence


_DEFAULT_SOURCE = Path(__file__).with_name("source-evidence.md")


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare a preserved evidence artifact with its source bytes.",
    )
    parser.add_argument(
        "artifact",
        type=Path,
        help="path to the preserved evidence artifact",
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=_DEFAULT_SOURCE,
        help="source evidence path (defaults to the colocated fixture source)",
    )
    return parser.parse_args(argv)


def _sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _build_evidence(source_path: Path, artifact_path: Path) -> dict[str, object]:
    source = source_path.read_bytes()
    try:
        artifact = artifact_path.read_bytes()
    except (FileNotFoundError, IsADirectoryError):
        artifact = None

    return {
        "schemaVersion": 1,
        "sourceByteCount": len(source),
        "sourceSha256": _sha256(source),
        "artifactByteCount": len(artifact) if artifact is not None else None,
        "artifactSha256": _sha256(artifact) if artifact is not None else None,
        "exactBytesPreserved": artifact == source if artifact is not None else False,
    }


def _main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    evidence = _build_evidence(args.source, args.artifact)
    print(json.dumps(evidence, indent=2, sort_keys=True))
    return 0 if evidence["exactBytesPreserved"] else 3


if __name__ == "__main__":
    raise SystemExit(_main())
