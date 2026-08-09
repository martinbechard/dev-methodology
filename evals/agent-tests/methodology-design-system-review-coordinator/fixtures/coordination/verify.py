"""
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
AI attribution: Generated with AI assistance.
Responsibility: Verifies the fixed coordinator assignment, conflict, and ranking input boundaries.
Design: TASK.md
Tests: evals/agent-tests/methodology-design-system-review-coordinator/test_coordination_simulator.py
"""

from __future__ import annotations

from pathlib import Path

import yaml


def main() -> int:
    """Validate the coordinator-only fixture without executing a model."""

    payload = yaml.safe_load(Path("coordination-inputs.yaml").read_text(encoding="utf-8"))
    if payload.get("schema") != "dev-methodology-documentation-design-system-coordination-inputs":
        raise SystemExit("coordination fixture schema changed")
    if len(payload.get("assignments", [])) != 2:
        raise SystemExit("coordination fixture must retain two assignments")
    if payload.get("runnerOutcomes", {}).get("forms-and-actions.html:Accessibility") != "timeout":
        raise SystemExit("timeout counterexample is missing")
    candidates = payload.get("candidates", [])
    if not any(candidate.get("estimatedCost") is None for candidate in candidates):
        raise SystemExit("unpriced candidate is missing")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
