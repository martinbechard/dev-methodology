#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Runs the complete verification command for the disposable dependency-routing fixture.
# Governing design: fixture-contract.yaml
# Governing test plan: tests/test_dependency_status.py

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    """Verify the integrated runbook and source tests, returning their exit status."""
    fixture_root = Path(__file__).resolve().parent
    runbook = fixture_root / "docs" / "operator-runbook.md"
    if not runbook.is_file():
        print("missing documentation lane output: docs/operator-runbook.md", file=sys.stderr)
        return 1
    completed = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "tests"],
        cwd=fixture_root,
        check=False,
    )
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
