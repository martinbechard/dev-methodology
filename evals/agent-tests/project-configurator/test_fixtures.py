# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Verifies the Project Configurator synthetic fixture boundaries.
# Governing design: evals/agent-tests/implementation-plan.md
# Governing test plan: evals/agent-tests/project-configurator/scenarios.yaml

from __future__ import annotations

import subprocess
import unittest
from collections.abc import Collection, Mapping
from pathlib import Path
from typing import Any

import yaml


SUITE_ROOT = Path(__file__).resolve().parent


def _detection_evidence_rows(project: dict[str, Any]) -> list[Any]:
    """Return every detector evidence row without coercing its structure."""
    return [row for loadout in project["technology_skill_loadouts"] for row in loadout["sourceEvidence"]]


def _evaluate_technology_routing_output(
    output: Mapping[str, Any],
    confirmed_skills: Collection[str],
) -> str:
    """Accept only explicit folder rows with exact-name technology skills."""
    catalog = tuple(confirmed_skills)
    if (
        not catalog
        or any(
            not isinstance(skill, str) or not skill or skill != skill.strip()
            for skill in catalog
        )
        or len(set(catalog)) != len(catalog)
    ):
        return "FAIL"
    allowed_skills = set(catalog)
    if set(output) != {"folder_routing"}:
        return "FAIL"
    routes = output["folder_routing"]
    if not isinstance(routes, list) or not routes:
        return "FAIL"
    for route in routes:
        if not isinstance(route, Mapping):
            return "FAIL"
        if set(route) != {"pattern", "required_skills"}:
            return "FAIL"
        if not isinstance(route["pattern"], str) or not route["pattern"]:
            return "FAIL"
        skills = route["required_skills"]
        if (
            not isinstance(skills, list)
            or not skills
            or any(
                not isinstance(skill, str)
                or not skill
                or skill != skill.strip()
                or skill not in allowed_skills
                for skill in skills
            )
            or len(set(skills)) != len(skills)
        ):
            return "FAIL"
    return "PASS"


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

    def test_reuse_fixture_preserves_structured_detection_evidence_rows(self) -> None:
        """The baseline separates structured rows from their scalar evidence values."""
        fixture = SUITE_ROOT / "fixtures" / "valid-configuration-reuse"
        project = yaml.safe_load((fixture / "PROJECT.yaml").read_text(encoding="utf-8"))
        rows = _detection_evidence_rows(project)

        self.assertTrue(rows)
        for row in rows:
            self.assertIsInstance(row, dict)
            self.assertEqual({"skill", "runtimeAvailability", "evidence"}, set(row))
            self.assertIsInstance(row["evidence"], list)
            self.assertTrue(row["evidence"])
            self.assertTrue(all(isinstance(value, str) for value in row["evidence"]))

    def test_reuse_scenario_names_each_authoritative_evidence_gate(self) -> None:
        """The executable scenario cannot silently drop source-integrity checks."""
        scenarios = yaml.safe_load((SUITE_ROOT / "scenarios.yaml").read_text(encoding="utf-8"))["scenarios"]
        scenario = next(item for item in scenarios if item["id"] == "valid-configuration-reuse")

        self.assertIn("authoritative-move-provenance", scenario["deterministicChecks"])
        self.assertIn("protected-input-digests", scenario["deterministicChecks"])
        self.assertIn("structured-source-evidence-fidelity", scenario["deterministicChecks"])
        self.assertIn("scalar-detection-evidence", scenario["deterministicChecks"])
        self.assertIn("source-faithful-guidance", scenario["deterministicChecks"])

        routing = next(item for item in scenarios if item["id"] == "technology-routing")
        invalid = next(item for item in scenarios if item["id"] == "invalid-configuration")
        for unrelated in (routing, invalid):
            self.assertNotIn("authoritative-move-provenance", unrelated["deterministicChecks"])
            self.assertNotIn("structured-source-evidence-fidelity", unrelated["deterministicChecks"])
            self.assertNotIn("source-faithful-guidance", unrelated["deterministicChecks"])

    def test_reuse_supervisor_and_judge_share_the_authority_contract(self) -> None:
        """Both evaluation roles receive the same comparison obligations."""
        supervisor = (SUITE_ROOT / "agents" / "supervisor.toml").read_text(encoding="utf-8")
        judge = (SUITE_ROOT / "agents" / "judge.toml").read_text(encoding="utf-8")

        for contract in (supervisor, judge):
            self.assertIn("selected scenario id is valid-configuration-reuse", contract)
            self.assertIn("protected-input", contract)
            self.assertIn("list of mapping rows", contract)
            self.assertIn("list containing only scalar strings", contract)
            self.assertIn("changed PROJECT.yaml evidence or fact statement", contract)
            self.assertIn("valid-reuse-only", contract)

        self.assertIn("only with evidence and deterministic results applicable to the selected scenario", supervisor)

    def test_suite_contract_scopes_reuse_fidelity_away_from_other_scenarios(self) -> None:
        """The shared skill cannot flatten rows or leak reuse gates across cases."""
        contract = (
            SUITE_ROOT / "skills" / "project-configurator-suite-contract" / "SKILL.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Apply this section only when the selected scenario id is valid-configuration-reuse", contract)
        self.assertIn("sourceEvidence value remains a list of mapping rows", contract)
        self.assertIn("evidence field remains a list whose elements are scalar strings", contract)
        self.assertIn("complete subtree to remain semantically equal", contract)
        self.assertIn("Do not apply valid-configuration-reuse", contract)

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

    def test_routing_fixture_freezes_the_required_worktree_ignore_prerequisite(self) -> None:
        """Generated guidance can state the worktree boundary from fixture evidence."""
        fixture = SUITE_ROOT / "fixtures" / "technology-routing"
        ignore_file = fixture / ".gitignore"

        self.assertEqual("/.worktrees/\n", ignore_file.read_text(encoding="utf-8"))
        result = subprocess.run(
            ["git", "check-ignore", "--no-index", ".worktrees/probe"],
            cwd=fixture,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stderr)

    def test_routing_scenario_requires_canonical_complete_configuration_evidence(self) -> None:
        """The routing verdict cannot accept an invented or incomplete PROJECT.yaml."""
        scenarios = yaml.safe_load((SUITE_ROOT / "scenarios.yaml").read_text(encoding="utf-8"))["scenarios"]
        routing = next(item for item in scenarios if item["id"] == "technology-routing")

        self.assertIn("Preserve the canonical project template structure and every mandatory section", routing["requiredBehaviors"])
        self.assertIn("Select and validate the required conceptual definitions", routing["requiredBehaviors"])
        self.assertIn(
            "Preserve the Project Configurator fixed and conditional skill sets without omissions, duplicates, or reclassification",
            routing["requiredBehaviors"],
        )
        self.assertIn("Evaluate mutation and claim agreement for every selected definition", routing["requiredBehaviors"])
        self.assertIn("configuration-schema", routing["deterministicChecks"])
        self.assertIn("mandatory-project-sections", routing["deterministicChecks"])
        self.assertIn("conceptual-definition-validation", routing["deterministicChecks"])
        self.assertIn("canonical-role-skill-ownership", routing["deterministicChecks"])
        self.assertIn("mutation-claim-consistency", routing["deterministicChecks"])

    def test_routing_scenario_uses_public_setup_procedures_without_an_aggregate(self) -> None:
        """The behavioral case invokes reviewed procedures and rejects aggregate output."""

        scenarios = yaml.safe_load(
            (SUITE_ROOT / "scenarios.yaml").read_text(encoding="utf-8")
        )["scenarios"]
        routing = next(item for item in scenarios if item["id"] == "technology-routing")
        task = (
            SUITE_ROOT / "fixtures" / "technology-routing" / "TASK.md"
        ).read_text(encoding="utf-8")
        combined = "\n".join(
            [
                *routing["requiredBehaviors"],
                *routing["forbiddenBehaviors"],
                task,
            ]
        )

        for procedure in (
            "Detect Technology Skills",
            "Configure Project Agents And Skills",
            "Render Project Guidance",
            "Verify Project Configuration",
        ):
            with self.subTest(procedure=procedure):
                self.assertIn(procedure, combined)

        composed_routes = {
            "folder_routing": [
                {
                    "pattern": "service/**",
                    "required_skills": ["fastapi", "python"],
                },
            ]
        }
        aggregate_output = {
            "aggregate interface": {
                "selected-skill-set": ["python", "typescript"],
            }
        }

        confirmed_skills = (
            SUITE_ROOT / "fixtures" / "technology-routing" / "available-skills.txt"
        ).read_text(encoding="utf-8").splitlines()

        self.assertEqual(
            "PASS",
            _evaluate_technology_routing_output(composed_routes, confirmed_skills),
        )
        self.assertEqual(
            "FAIL",
            _evaluate_technology_routing_output(aggregate_output, confirmed_skills),
        )
        for invalid_skills in (
            [""],
            [" "],
            ["python", " python"],
            ["python", "python"],
            ["unknown-skill"],
            ["selected-skill-set"],
        ):
            with self.subTest(invalid_skills=invalid_skills):
                invalid = {
                    "folder_routing": [
                        {"pattern": "service/**", "required_skills": invalid_skills}
                    ]
                }
                self.assertEqual(
                    "FAIL",
                    _evaluate_technology_routing_output(invalid, confirmed_skills),
                )

    def test_routing_scenario_requires_exact_functional_claude_bridges(self) -> None:
        """Bridge validation must inspect exact imports rather than prose or existence."""
        scenarios = yaml.safe_load((SUITE_ROOT / "scenarios.yaml").read_text(encoding="utf-8"))["scenarios"]
        routing = next(item for item in scenarios if item["id"] == "technology-routing")
        task = (SUITE_ROOT / "fixtures" / "technology-routing" / "TASK.md").read_text(encoding="utf-8")

        self.assertIn(
            "Write every root and nested Claude bridge as the exact functional import of its colocated AGENTS.md",
            routing["requiredBehaviors"],
        )
        self.assertIn("functional-claude-bridges", routing["deterministicChecks"])
        self.assertIn("@AGENTS.md", task)
        self.assertIn("The file must end after that line", task)
        self.assertIn("Descriptive prose", task)

    def test_routing_contracts_name_exact_role_ownership_and_bridge_bytes(self) -> None:
        """Supervisor and Judge must compare the canonical sets and bridge bytes."""
        role = yaml.safe_load(
            (
                SUITE_ROOT.parents[2]
                / "agents"
                / "roles"
                / "project-setup"
                / "project-configurator.role.yaml"
            ).read_text(encoding="utf-8")
        )
        supervisor = (SUITE_ROOT / "agents" / "supervisor.toml").read_text(encoding="utf-8")
        judge = (SUITE_ROOT / "agents" / "judge.toml").read_text(encoding="utf-8")
        task = (SUITE_ROOT / "fixtures" / "technology-routing" / "TASK.md").read_text(encoding="utf-8")
        contract = (
            SUITE_ROOT / "skills" / "project-configurator-suite-contract" / "SKILL.md"
        ).read_text(encoding="utf-8")

        fixed_skills: set[str] = set()
        conditional_skills: dict[str, str] = {}
        for item in role["skills"]:
            skill_name, metadata = next(iter(item.items()))
            condition = metadata.get("condition") if isinstance(metadata, dict) else None
            if condition is None:
                fixed_skills.add(skill_name)
            else:
                conditional_skills[skill_name] = condition

        self.assertEqual(
            {
                "resource-claim",
                "detect-technology-skills",
                "create-project-configuration",
                "route-documentation-work",
                "verify-documentation-page",
            },
            fixed_skills,
        )
        self.assertEqual(
            {"organise-project-files", "bootstrap-project-documentation"},
            set(conditional_skills),
        )
        self.assertTrue(all(condition.strip() for condition in conditional_skills.values()))

        sources = (task, supervisor, judge, contract)
        for source in sources:
            for skill_name in fixed_skills | set(conditional_skills):
                self.assertIn(skill_name, source)
            for bridge_path in (
                "CLAUDE.md",
                "service/CLAUDE.md",
                "ui/CLAUDE.md",
                "infra/CLAUDE.md",
            ):
                self.assertIn(bridge_path, source)
            self.assertIn("@AGENTS.md", source)
            self.assertIn("duplicated", source)
            self.assertIn("reclassified", source)

        for source in (supervisor, judge, contract):
            self.assertIn("one newline", source)
            self.assertIn("canonical condition", source)

        for source in (supervisor, contract):
            self.assertIn("no other content", source)
        self.assertIn("contains only @AGENTS.md", judge)
        self.assertIn("trailing content", judge)
        self.assertIn("The file must end after that line", task)
        self.assertIn("including their canonical conditions", task)
        self.assertIn("canonical-role-skill-ownership", supervisor)
        self.assertIn("functional-claude-bridges", supervisor)

    def test_routing_specific_gates_are_registered_as_critical(self) -> None:
        """Runner evidence must recognize both exact acceptance gates."""
        judges = yaml.safe_load((SUITE_ROOT.parents[1] / "judges.yaml").read_text(encoding="utf-8"))
        checks = {item["id"]: item for item in judges["checks"]}

        for check_id in ("canonical-role-skill-ownership", "functional-claude-bridges"):
            with self.subTest(check_id=check_id):
                self.assertIn(check_id, checks)
                self.assertEqual("deterministic", checks[check_id]["type"])
                self.assertIs(True, checks[check_id]["critical"])

    def test_routing_contracts_share_template_definition_and_mutation_gates(self) -> None:
        """Target, supervisor, and Judge receive the same canonical routing boundary."""
        task = (SUITE_ROOT / "fixtures" / "technology-routing" / "TASK.md").read_text(encoding="utf-8")
        supervisor = (SUITE_ROOT / "agents" / "supervisor.toml").read_text(encoding="utf-8")
        judge = (SUITE_ROOT / "agents" / "judge.toml").read_text(encoding="utf-8")
        contract = (
            SUITE_ROOT / "skills" / "project-configurator-suite-contract" / "SKILL.md"
        ).read_text(encoding="utf-8")

        for source in (task, supervisor, judge, contract):
            self.assertIn("canonical project template", source)
            self.assertIn("mandatory section", source)
            self.assertIn("conceptual definition", source)
            self.assertIn("mutation", source)
            self.assertIn("resource-claim", source)

    def test_invalid_fixture_contains_both_independent_contract_failures(self) -> None:
        """The invalid scenario proves claim and runtime-capability validation."""
        fixture = SUITE_ROOT / "fixtures" / "invalid-configuration"
        role = yaml.safe_load((fixture / "proposed-role.yaml").read_text(encoding="utf-8"))
        project = yaml.safe_load((fixture / "PROJECT.yaml").read_text(encoding="utf-8"))
        loadout = project["technology_skill_loadouts"][0]

        self.assertEqual("required", role["repositoryMutation"])
        self.assertNotIn("resource-claim", role["skills"])
        self.assertIn("unavailable-framework", loadout["skills"])
        self.assertEqual("UNAVAILABLE", loadout["sourceEvidence"][0]["runtimeAvailability"])
        self.assertEqual("READY", loadout["status"])

    def test_invalid_scenario_requires_target_owned_repository_evidence(self) -> None:
        """A truthful BLOCKED result must still come from direct repository inspection."""
        scenarios = yaml.safe_load((SUITE_ROOT / "scenarios.yaml").read_text(encoding="utf-8"))["scenarios"]
        invalid = next(item for item in scenarios if item["id"] == "invalid-configuration")

        self.assertIn("Inspect PROJECT.yaml, proposed-role.yaml, and available-skills.txt directly", invalid["requiredBehaviors"])
        self.assertIn("Distinguish target-owned reasoning from supervisor assertions", invalid["requiredBehaviors"])
        self.assertIn("target-repository-inspection", invalid["deterministicChecks"])
        self.assertIn("independent-target-reasoning", invalid["deterministicChecks"])

    def test_invalid_contracts_reject_repetition_only_reasoning(self) -> None:
        """Every evaluation role preserves the inspection and non-repetition threshold."""
        task = (SUITE_ROOT / "fixtures" / "invalid-configuration" / "TASK.md").read_text(encoding="utf-8")
        supervisor = (SUITE_ROOT / "agents" / "supervisor.toml").read_text(encoding="utf-8")
        judge = (SUITE_ROOT / "agents" / "judge.toml").read_text(encoding="utf-8")
        contract = (
            SUITE_ROOT / "skills" / "project-configurator-suite-contract" / "SKILL.md"
        ).read_text(encoding="utf-8")

        for source in (task, supervisor, judge, contract):
            self.assertIn("direct repository inspection", source)
            self.assertIn("target-owned", source)
            self.assertIn("supervisor", source)
            self.assertIn("repetition", source)


if __name__ == "__main__":
    unittest.main()
