# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Verifies the Project Configurator synthetic fixture boundaries.
# Governing design: evals/agent-tests/implementation-plan.md
# Governing test plan: evals/agent-tests/project-configurator/scenarios.yaml

from __future__ import annotations

import unittest
from pathlib import Path
from typing import Any

import yaml


SUITE_ROOT = Path(__file__).resolve().parent


def _all_detection_evidence(project: dict[str, Any]) -> list[Any]:
    """Return every detector evidence element without coercing its type."""
    return [
        evidence
        for loadout in project["technology_skill_loadouts"]
        for source in loadout["sourceEvidence"]
        for evidence in source["evidence"]
    ]


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

    def test_reuse_authority_explicitly_proves_only_the_folder_move(self) -> None:
        """Frozen task and README text are the move-provenance authority."""
        fixture = SUITE_ROOT / "fixtures" / "valid-configuration-reuse"
        task = (fixture / "TASK.md").read_text(encoding="utf-8")
        readme = (fixture / "README.md").read_text(encoding="utf-8")

        self.assertIn("worker-old moved to worker", task)
        self.assertIn("source directory moved from worker-old to worker", readme)
        self.assertIn("Preserve the existing project summary", task)
        self.assertIn("without replacing the configuration wholesale", readme)

    def test_reuse_fixture_detection_evidence_elements_are_scalar_strings(self) -> None:
        """The baseline models the detector's portable scalar evidence contract."""
        fixture = SUITE_ROOT / "fixtures" / "valid-configuration-reuse"
        project = yaml.safe_load((fixture / "PROJECT.yaml").read_text(encoding="utf-8"))
        evidence = _all_detection_evidence(project)

        self.assertTrue(evidence)
        self.assertTrue(all(isinstance(value, str) for value in evidence))

    def test_reuse_scenario_names_each_authoritative_evidence_gate(self) -> None:
        """The executable scenario cannot silently drop source-integrity checks."""
        scenarios = yaml.safe_load((SUITE_ROOT / "scenarios.yaml").read_text(encoding="utf-8"))["scenarios"]
        scenario = next(item for item in scenarios if item["id"] == "valid-configuration-reuse")

        self.assertIn("authoritative-move-provenance", scenario["deterministicChecks"])
        self.assertIn("protected-input-digests", scenario["deterministicChecks"])
        self.assertIn("scalar-detection-evidence", scenario["deterministicChecks"])
        self.assertIn("source-faithful-guidance", scenario["deterministicChecks"])

    def test_reuse_supervisor_and_judge_share_the_authority_contract(self) -> None:
        """Both evaluation roles receive the same comparison obligations."""
        supervisor = (SUITE_ROOT / "agents" / "supervisor.toml").read_text(encoding="utf-8")
        judge = (SUITE_ROOT / "agents" / "judge.toml").read_text(encoding="utf-8")

        for contract in (supervisor, judge):
            self.assertIn("frozen TASK.md and README.md", contract)
            self.assertIn("protected-input", contract)
            self.assertIn("scalar string", contract)
            self.assertIn("changed PROJECT.yaml evidence or fact statement", contract)

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
