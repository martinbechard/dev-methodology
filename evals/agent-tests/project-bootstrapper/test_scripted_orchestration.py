# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies deterministic Project Bootstrapper orchestration, correction, failure, timeout, and cleanup behavior.
# Governing implementation: evals/agent-tests/project-bootstrapper/scripted_orchestration.py

from __future__ import annotations

import importlib.util
import os
import sys
import unittest
from pathlib import Path


_MODULE_PATH = Path(__file__).with_name("scripted_orchestration.py")
_SPEC = importlib.util.spec_from_file_location("project_bootstrapper_scripted", _MODULE_PATH)
assert _SPEC is not None and _SPEC.loader is not None
scripted = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = scripted
_SPEC.loader.exec_module(scripted)


class ScriptedBootstrapperTests(unittest.TestCase):
    """Protect the required Bootstrapper gate from model and live-pipeline variance."""

    def test_default_trace_is_repeatable_and_complete(self) -> None:
        first = scripted.run_isolated()
        second = scripted.run_isolated()
        self.assertEqual("PASS", first["status"])
        self.assertEqual(first["trace"], second["trace"])
        self.assertEqual(
            [
                "PROJECT.yaml",
                "AGENTS.md",
                "docs/coverage-manifest.yaml",
                "docs/module-catalog.md",
                "docs/module-orders.md",
                "docs/wiki/README.md",
                "docs/wiki/topic-index.md",
            ],
            first["accepted"],
        )
        self.assertEqual("dev-merge-coordinator", first["integrationChoice"])
        self.assertTrue(first["targetContractBound"])
        self.assertTrue(first["finalReview"])
        self.assertTrue(first["finalVerification"])
        self.assertTrue(first["claimCloseout"])
        self.assertTrue(first["workspaceRemoved"])
        self.assertEqual("complete", first["ownedProcessCleanup"])

    def test_isolated_snapshot_contains_only_declared_inputs(self) -> None:
        result = scripted.run_isolated()
        copied = result["copiedInputs"]
        self.assertIn("agents/roles/project-setup/project-bootstrapper.role.yaml", copied)
        self.assertIn("generated/adapters/codex/agents/project-bootstrapper.toml", copied)
        self.assertIn("evals/agent-tests/project-bootstrapper/agents", copied)
        self.assertIn(
            "evals/agent-tests/project-bootstrapper/fixtures/missing-configuration-multi-contribution",
            copied,
        )
        self.assertNotIn("agents", copied)
        self.assertNotIn("skills", copied)
        self.assertNotIn("evals/agent-tests/runner.py", copied)

    def test_both_configuration_outputs_receive_independent_reviews(self) -> None:
        result = scripted.run_isolated()
        reviewed = {
            event["artifact"]
            for event in result["trace"]
            if event["agent"] == "dev-artifact-reviewer" and event["phase"] == "review"
        }
        self.assertTrue({"PROJECT.yaml", "AGENTS.md"}.issubset(reviewed))

    def test_correction_retries_the_owner_and_stops_at_two(self) -> None:
        corrected = scripted.run_isolated(
            {"review:docs/module-catalog.md": ["NEEDS_CORRECTION", "PASS"]}
        )
        relevant = [
            (event["agent"], event["phase"], event["outcome"])
            for event in corrected["trace"]
            if event["artifact"] == "docs/module-catalog.md"
            and event["agent"] != "scripted-claim-double"
        ]
        self.assertEqual(
            [
                ("dev-documentation-writer", "contribute", "PASS"),
                ("dev-artifact-reviewer", "review", "NEEDS_CORRECTION"),
                ("dev-documentation-writer", "correct", "PASS"),
                ("dev-artifact-reviewer", "review", "PASS"),
                ("dev-artifact-reviewer", "post-integration-review", "PASS"),
            ],
            relevant,
        )
        capped = scripted.run_isolated(
            {
                "review:docs/module-catalog.md": [
                    "NEEDS_CORRECTION",
                    "NEEDS_CORRECTION",
                    "NEEDS_CORRECTION",
                ]
            }
        )
        self.assertEqual("BLOCKED", capped["status"])
        self.assertEqual("correction cap reached", capped["reason"])

    def test_integration_review_and_verification_corrections_are_bounded(self) -> None:
        integration = scripted.run_isolated(
            {"integrate:multiple-contributions": ["NEEDS_CORRECTION", "PASS"]}
        )
        self.assertEqual("PASS", integration["status"])
        self.assertIn(
            "correct-integration",
            [event["phase"] for event in integration["trace"]],
        )
        post_review = scripted.run_isolated(
            {"post-integration-review:docs/wiki/topic-index.md": ["NEEDS_CORRECTION", "PASS"]}
        )
        self.assertEqual("PASS", post_review["status"])
        self.assertIn("reintegrate", [event["phase"] for event in post_review["trace"]])
        verification_routes = {
            "AGENTS.md": "project-configurator",
            "docs/module-catalog.md": "dev-documentation-writer",
            "docs/wiki/README.md": "wiki-architect",
            "docs/wiki/topic-index.md": "wiki-writer",
            "integration": "dev-merge-coordinator",
        }
        for finding, owner in verification_routes.items():
            with self.subTest(finding=finding):
                verification = scripted.run_isolated(
                    {
                        "final-verification:integration": ["NEEDS_CORRECTION", "PASS"],
                        "verificationFinding": [finding],
                    }
                )
                self.assertEqual("PASS", verification["status"])
                corrections = [
                    event
                    for event in verification["trace"]
                    if event["phase"] in {"correct", "correct-integration"}
                    and event["artifact"] == finding
                ]
                self.assertEqual(owner, corrections[0]["agent"])

    def test_terminal_dependency_outcomes_are_reproducible(self) -> None:
        for outcome in ("FAIL", "BLOCKED"):
            with self.subTest(outcome=outcome):
                result = scripted.run_isolated({"wiki-writer": [outcome]})
                self.assertEqual(outcome, result["status"])
                self.assertTrue(result["claimCloseout"])
        malformed = scripted.run_isolated({"dev-verifier": ["NOT_A_HANDOFF"]})
        self.assertEqual("INFRASTRUCTURE_FAILED", malformed["status"])
        self.assertIn("malformed handoff", malformed["reason"])

    def test_timeout_kills_the_owned_process_group_and_cleans_workspace(self) -> None:
        result = scripted.run_isolated({"project-configurator": ["TIMEOUT"]}, timeout_seconds=0.1)
        self.assertEqual("INFRASTRUCTURE_FAILED", result["status"])
        self.assertEqual("wall-clock timeout", result["reason"])
        self.assertEqual("complete", result["ownedProcessCleanup"])
        self.assertTrue(result["workspaceRemoved"])
        with self.assertRaises(ProcessLookupError):
            os.kill(result["workerPid"], 0)


if __name__ == "__main__":
    unittest.main()
