"""
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
AI attribution: Generated with AI assistance.
Responsibility: Verifies the fixed source and interaction evidence for the synthetic documentation design-system review case.
Design: TASK.md
Tests: evals/agent-tests/methodology-design-system-checklist-runner/test_contract.py
"""

from __future__ import annotations

from pathlib import Path
import re


def main() -> int:
    """Validate that the frozen fixture retains its one seeded version defect."""

    source = Path("sample-page.html").read_text(encoding="utf-8")
    metadata = re.search(r'<meta name="design-system-version" content="([^"]+)">', source)
    footer = re.search(r'<span class="ds-version">Documentation Design System ([^<]+)</span>', source)
    if metadata is None or footer is None:
        raise SystemExit("version evidence is missing")
    if metadata.group(1) != "0.1.0" or footer.group(1) != "0.2.0":
        raise SystemExit("the seeded 0.1.0 versus 0.2.0 inconsistency changed")
    interactions = Path("interaction-evidence.md").read_text(encoding="utf-8")
    for marker in ("first Tab", "360 by 800", "three-pixel outline"):
        if marker not in interactions:
            raise SystemExit(f"interaction evidence is missing {marker}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
