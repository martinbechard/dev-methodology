#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Verifies fail-closed route selection for the Dev Security Reviewer suite.
# Governing design: evals/agent-tests/dev-security-reviewer/skills/dev-security-reviewer-suite-contract/SKILL.md
# Governing test plan: evals/agent-tests/dev-security-reviewer/test_route_selection.py

from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

import yaml

from route_selection import main, select_route


SUITE_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = SUITE_ROOT.parents[2]
CATALOG = SUITE_ROOT / "fixtures" / "policy-compatible-routes.yaml"


class RouteSelectionTests(unittest.TestCase):
    """Exercise supported, prohibited, unavailable, and malformed route evidence."""

    def test_junie_opus_route_is_selected_for_bounded_synthetic_review(self) -> None:
        decision = select_route(CATALOG, REPOSITORY_ROOT, "junie", frozenset({"junie"}))

        self.assertEqual("SELECTED", decision.status)
        self.assertEqual("POLICY_COMPATIBLE_ROUTE", decision.reason)
        self.assertEqual("bounded-synthetic-security-review", decision.scope)
        self.assertEqual("opus", decision.model_family)
        self.assertRegex(decision.native_agent_sha256 or "", r"^[0-9a-f]{64}$")
        self.assertRegex(decision.catalog_sha256, r"^[0-9a-f]{64}$")

    def test_codex_sol_route_is_prohibited_without_fallback(self) -> None:
        decision = select_route(CATALOG, REPOSITORY_ROOT, "codex", frozenset({"codex", "junie"}))

        self.assertEqual("INFRASTRUCTURE_BLOCKED", decision.status)
        self.assertEqual("MODEL_FAMILY_PROHIBITED", decision.reason)
        self.assertEqual("codex", decision.harness)
        self.assertEqual("sol", decision.model_family)

    def test_permitted_route_must_be_available(self) -> None:
        decision = select_route(CATALOG, REPOSITORY_ROOT, "junie", frozenset({"codex"}))

        self.assertEqual("INFRASTRUCTURE_BLOCKED", decision.status)
        self.assertEqual("ROUTE_UNAVAILABLE", decision.reason)

    def test_malformed_route_evidence_blocks_before_dispatch(self) -> None:
        malformed = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))
        del malformed["routes"]["junie"]["permittedModelFamilies"]
        with tempfile.TemporaryDirectory() as temporary_directory:
            catalog = Path(temporary_directory) / "routes.yaml"
            catalog.write_text(yaml.safe_dump(malformed, sort_keys=False), encoding="utf-8")

            decision = select_route(catalog, REPOSITORY_ROOT, "junie", frozenset({"junie"}))

        self.assertEqual("INFRASTRUCTURE_BLOCKED", decision.status)
        self.assertEqual("MALFORMED_ROUTE_EVIDENCE", decision.reason)

    def test_wrong_scope_blocks_before_dispatch(self) -> None:
        malformed = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))
        malformed["scope"] = "unbounded-security-review"
        with tempfile.TemporaryDirectory() as temporary_directory:
            catalog = Path(temporary_directory) / "routes.yaml"
            catalog.write_text(yaml.safe_dump(malformed, sort_keys=False), encoding="utf-8")

            decision = select_route(catalog, REPOSITORY_ROOT, "junie", frozenset({"junie"}))

        self.assertEqual("INFRASTRUCTURE_BLOCKED", decision.status)
        self.assertEqual("MALFORMED_ROUTE_EVIDENCE", decision.reason)

    def test_missing_catalog_emits_a_fail_closed_decision(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            catalog = Path(temporary_directory) / "missing-routes.yaml"
            output = io.StringIO()

            with redirect_stdout(output):
                exit_code = main(
                    [
                        "--harness",
                        "junie",
                        "--available-harness",
                        "junie",
                        "--catalog",
                        str(catalog),
                        "--repository-root",
                        str(REPOSITORY_ROOT),
                    ]
                )

        decision = json.loads(output.getvalue())
        self.assertEqual(2, exit_code)
        self.assertEqual("INFRASTRUCTURE_BLOCKED", decision["status"])
        self.assertEqual("MALFORMED_ROUTE_EVIDENCE", decision["reason"])
        self.assertIsNone(decision["catalog_sha256"])


if __name__ == "__main__":
    unittest.main()
