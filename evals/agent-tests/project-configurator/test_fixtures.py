# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Verifies the Project Configurator synthetic fixture boundaries.
# Governing design: evals/agent-tests/implementation-plan.md
# Governing test plan: evals/agent-tests/project-configurator/scenarios.yaml

from __future__ import annotations

import unittest
from pathlib import Path

import yaml


SUITE_ROOT = Path(__file__).resolve().parent


class ProjectConfiguratorFixtureTests(unittest.TestCase):
    """Keep every executable scenario backed by a concrete synthetic project."""

    def test_every_scenario_uses_a_fixture_directory(self) -> None:
        """Manifest-only cases cannot reach a configuration target."""
        scenarios = yaml.safe_load((SUITE_ROOT / "scenarios.yaml").read_text(encoding="utf-8"))["scenarios"]

        for scenario in scenarios:
            with self.subTest(scenario=scenario["id"]):
                fixture = SUITE_ROOT / scenario["executableCase"]
                self.assertTrue(fixture.is_dir())
                self.assertTrue((fixture / "TASK.md").is_file())
                self.assertTrue((fixture / "available-skills.txt").is_file())

    def test_reuse_fixture_contains_current_source_and_stale_routing(self) -> None:
        """The target can reconcile a real move while preserving valid intent."""
        fixture = SUITE_ROOT / "fixtures" / "valid-configuration-reuse"
        project = yaml.safe_load((fixture / "PROJECT.yaml").read_text(encoding="utf-8"))

        self.assertTrue((fixture / "worker" / "main.py").is_file())
        self.assertFalse((fixture / "worker-old" / "main.py").exists())
        self.assertTrue((fixture / "worker-old" / "AGENTS.md").is_file())
        self.assertEqual("worker-old/**", project["folder_routing"][0]["pattern"])
        self.assertIn("python", (fixture / "available-skills.txt").read_text(encoding="utf-8").splitlines())

    def test_routing_fixture_exposes_two_supported_and_one_unknown_scope(self) -> None:
        """Detection can distinguish Python, TypeScript, and NO_VARIANT."""
        fixture = SUITE_ROOT / "fixtures" / "technology-routing"
        available = (fixture / "available-skills.txt").read_text(encoding="utf-8").splitlines()

        self.assertTrue((fixture / "service" / "main.py").is_file())
        self.assertTrue((fixture / "ui" / "app.ts").is_file())
        self.assertTrue((fixture / "infra" / "pipeline.synthetic").is_file())
        self.assertIn("python", available)
        self.assertIn("typescript", available)
        self.assertNotIn("syntheticdsl", available)

    def test_invalid_fixture_contains_both_independent_contract_failures(self) -> None:
        """The invalid scenario proves claim and runtime-capability validation."""
        fixture = SUITE_ROOT / "fixtures" / "invalid-configuration"
        role = yaml.safe_load((fixture / "proposed-role.yaml").read_text(encoding="utf-8"))
        project = yaml.safe_load((fixture / "PROJECT.yaml").read_text(encoding="utf-8"))
        loadout = project["technology_skill_loadouts"][0]

        self.assertEqual("required", role["repositoryMutation"])
        self.assertNotIn("agent-claim", role["skills"])
        self.assertIn("unavailable-framework", loadout["skills"])
        self.assertEqual("UNAVAILABLE", loadout["sourceEvidence"][0]["runtimeAvailability"])
        self.assertEqual("READY", loadout["status"])


if __name__ == "__main__":
    unittest.main()
