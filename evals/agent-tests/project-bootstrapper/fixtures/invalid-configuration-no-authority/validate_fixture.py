# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Reports the two governed validation errors in the invalid bootstrap fixture.

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
AVAILABLE_AGENTS = {"dev-documentation-writer", "dev-artifact-reviewer", "dev-verifier"}


def validation_errors() -> list[str]:
    """Return exact source-backed configuration errors."""

    project_text = (ROOT / "PROJECT.yaml").read_text()
    errors: list[str] = []
    if "missing-conceptual-agent" in project_text and "missing-conceptual-agent" not in AVAILABLE_AGENTS:
        errors.append("conceptual agent does not exist: missing-conceptual-agent")
    if not (ROOT / "src" / "missing-module").is_dir():
        errors.append("configured folder does not exist: src/missing-module")
    return errors


def main() -> int:
    """Print validation errors and fail when the invalid configuration is observed."""

    errors = validation_errors()
    print(json.dumps({"errors": errors}, sort_keys=True))
    return 2 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
