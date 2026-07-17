# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies all Dev Runtime Diagnostician fixture commands and cleanup boundaries.

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


SUITE_ROOT = Path(__file__).resolve().parent


def run_json(fixture: Path, *arguments: str) -> dict[str, object]:
    """Run one fixture command and return its JSON evidence."""

    completed = subprocess.run(
        [sys.executable, *arguments],
        cwd=fixture,
        capture_output=True,
        text=True,
        check=False,
        timeout=15,
    )
    if completed.returncode != 0:
        raise AssertionError(completed.stdout + completed.stderr)
    return json.loads(completed.stdout)


class DevRuntimeDiagnosticianFixtureTests(unittest.TestCase):
    def test_retained_process_reproduction_cleans_its_child(self) -> None:
        fixture = SUITE_ROOT / "fixtures" / "retained-process-port"

        evidence = run_json(fixture, "lifecycle_probe.py", "reproduce")

        self.assertTrue(evidence["parentExited"])
        self.assertTrue(evidence["portRetainedAfterParentExit"])
        self.assertTrue(evidence["cleanupVerified"])

    def test_clean_shutdown_supports_repeated_restarts(self) -> None:
        fixture = SUITE_ROOT / "fixtures" / "retained-process-port"

        evidence = run_json(fixture, "lifecycle_probe.py", "verify-clean")

        self.assertEqual(3, evidence["cycles"])
        self.assertTrue(evidence["cleanRestartsVerified"])

    def test_worker_stall_exposes_competing_hypothesis_evidence(self) -> None:
        fixture = SUITE_ROOT / "fixtures" / "worker-stall-competing-hypotheses"

        evidence = run_json(fixture, "reproduce.py")

        self.assertEqual(1, evidence["queuedWorkObserved"])
        self.assertTrue(evidence["heartbeatAdvanced"])
        self.assertEqual(0, evidence["availableConnections"])
        self.assertEqual(2, evidence["retainedCancelledLeases"])
        self.assertFalse(evidence["followupCompleted"])

    def test_unavailable_dependency_local_boundary_is_healthy(self) -> None:
        fixture = SUITE_ROOT / "fixtures" / "unavailable-runtime-dependency"
        completed = subprocess.run(
            [sys.executable, "-m", "unittest", "test_app.py"],
            cwd=fixture,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)


if __name__ == "__main__":
    unittest.main()
