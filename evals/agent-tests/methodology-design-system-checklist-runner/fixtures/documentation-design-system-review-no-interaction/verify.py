"""
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
AI attribution: Generated with AI assistance.
Responsibility: Verifies the fixed source for the synthetic design-system review case where interaction evidence is unavailable.
Design: TASK.md
Tests: evals/agent-tests/methodology-design-system-checklist-runner/test_contract.py
"""

from __future__ import annotations

from pathlib import Path
import re


def main() -> int:
    """Validate the seeded defect and the intentional absence of interaction evidence."""

    source = Path("sample-page.html").read_text(encoding="utf-8")
    metadata = re.search(r'<meta name="design-system-version" content="([^"]+)">', source)
    footer = re.search(r'<span class="ds-version">Documentation Design System ([^<]+)</span>', source)
    if metadata is None or footer is None:
        raise SystemExit("version evidence is missing")
    if metadata.group(1) != "0.1.0" or footer.group(1) != "0.2.0":
        raise SystemExit("the seeded 0.1.0 versus 0.2.0 inconsistency changed")
    if Path("interaction-evidence.md").exists():
        raise SystemExit("interaction evidence must remain unavailable in this fixture")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
