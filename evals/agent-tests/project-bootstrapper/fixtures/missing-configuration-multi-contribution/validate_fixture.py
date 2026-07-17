# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Validates initial absence and final completeness for multi-contribution bootstrap.

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def required_paths() -> list[str]:
    """Return every setup path named by the fixture contract."""

    requirements = json.loads((ROOT / "bootstrap-requirements.json").read_text())
    return [
        path
        for group in ("configuration", "nonWikiDocumentation", "wikiDocumentation")
        for path in requirements[group]
    ]


def main() -> int:
    """Validate the selected setup phase and print path evidence."""

    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("initial", "final"))
    args = parser.parse_args()
    presence = {path: (ROOT / path).is_file() for path in required_paths()}
    print(json.dumps(presence, sort_keys=True))
    if args.phase == "initial":
        return 0 if not any(presence.values()) else 2
    return 0 if all(presence.values()) else 3


if __name__ == "__main__":
    raise SystemExit(main())
