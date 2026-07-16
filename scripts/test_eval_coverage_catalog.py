# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies evaluation catalog completeness and evidence-state reporting without depending on the repository catalogs.

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from types import ModuleType

import yaml


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "build-support-checklist.py"


def load_module() -> ModuleType:
    """Load the coverage generator so tests exercise its source directly."""
    spec = importlib.util.spec_from_file_location(
        "build_support_checklist_for_test", SCRIPT_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class EvalCoverageCatalogTests(unittest.TestCase):
    """Protects catalog completeness and the separation of evaluation states."""

    def setUp(self) -> None:
        """Create a disposable catalog root for each test."""
        self.module = load_module()
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.root = Path(self.temporary_directory.name)
        (self.root / "evals" / "evidence").mkdir(parents=True)
        fixture = self.root / "evals" / "projects" / "fixture-a"
        fixture.mkdir(parents=True)
        (fixture / "TASK.md").write_text("# Task\n", encoding="utf-8")

    def write_yaml(self, relative_path: str, value: object) -> None:
        """Write one temporary YAML catalog used by an isolated test."""
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")

    def catalogs(
        self,
        *,
        probe_skills: tuple[str, ...] = ("skill-a",),
        scenario_agents: tuple[str, ...] = ("agent-a",),
        probe_harnesses: tuple[str, ...] = ("codex", "junie"),
        calibration_status: str = "pending",
    ) -> None:
        """Write the minimum version-two catalog set accepted by the reporter."""
        probe_ids = {skill: f"probe-{skill}" for skill in probe_skills}
        scenario_ids = {agent: f"scenario-{agent}" for agent in scenario_agents}
        executable_probe = probe_ids.get("skill-a")
        executable_scenario = scenario_ids.get("agent-a")
        self.write_yaml(
            "evals/cases.yaml",
            {
                "schema": "dev-methodology-agent-skill-evals",
                "version": 2,
                "coverageStatus": "fixture-backed",
                "supportedHarnesses": ["codex", "junie"],
                "catalogs": {},
                "cases": [
                    {
                        "id": "case-a",
                        "project": "evals/projects/fixture-a",
                        "task": "TASK.md",
                        "executionStatus": "runnable",
                        "verify": {"argv": ["test-command"]},
                        "coverageStatus": "fixture-backed",
                        "harnesses": ["codex", "junie"],
                        "agentScenarios": (
                            [executable_scenario] if executable_scenario else []
                        ),
                        "skillProbes": [executable_probe] if executable_probe else [],
                        "fixtureBackedProbeClaims": (
                            [executable_probe] if executable_probe else []
                        ),
                        "workflowPack": "workflow-a",
                        "sandboxProfiles": {
                            "codex": ["codex-write"],
                            "junie": ["junie-write"],
                        },
                        "judgePlan": {
                            "deterministicChecks": ["check-a"],
                            "modelRubric": "rubric-a",
                        },
                    }
                ],
            },
        )
        self.write_yaml(
            "evals/skill-probes.yaml",
            {
                "schema": "dev-methodology-skill-probes",
                "version": 2,
                "coverageStatus": "declared",
                "sourceDigestPolicy": "sha256-at-run",
                "harnesses": list(probe_harnesses),
                "evaluationCategoryVocabulary": ["behavior"],
                "sourceCategoryPolicy": "derive from source SKILL.md",
                "defaults": {},
                "probes": [
                    {
                        "id": probe_ids[skill],
                        "skill": skill,
                        "source": f"skills/{skill}/SKILL.md",
                        "evaluationCategory": "behavior",
                        "evaluationKind": "behavior",
                        "activationCondition": "matching task",
                        "negativeCondition": "unrelated task",
                        "expectedBehavior": "bounded behavior",
                        "judgePlan": {
                            "deterministicChecks": ["check-a"],
                            "modelRubric": "rubric-a",
                        },
                        "scenarioAssociations": (
                            [executable_scenario] if executable_scenario else []
                        ),
                        "workflowAssociations": ["workflow-a"],
                        "executableCases": ["case-a"] if skill == "skill-a" else [],
                        "coverageStatus": (
                            "fixture-backed" if skill == "skill-a" else "declared"
                        ),
                        "ablation": {
                            "omitTargetSkill": True,
                            "wrongSkillControl": "skill-a",
                        },
                    }
                    for skill in probe_skills
                ],
            },
        )
        self.write_yaml(
            "evals/agent-scenarios.yaml",
            {
                "schema": "dev-methodology-agent-scenarios",
                "version": 2,
                "coverageStatus": "declared",
                "sourceDigestPolicy": "sha256-at-run",
                "harnessPolicy": {"supported": ["codex", "junie"]},
                "agents": [
                    {
                        "id": agent,
                        "source": f"agents/roles/test/{agent}.role.yaml",
                        "scenarioFamily": "test",
                        "repositoryMutation": "conditional",
                        "harnesses": ["codex", "junie"],
                        "outputContractFields": ["status"],
                        "judgePlan": {
                            "deterministicChecks": ["check-a"],
                            "modelRubric": "rubric-a",
                        },
                        "workflowAssociations": ["workflow-a"],
                        "scenarios": [
                            {
                                "id": scenario_ids[agent],
                                "kind": "happy-path",
                                "fixtureProfile": "fixture-a",
                                "promptIntent": "perform bounded work",
                                "expectedOutcome": "READY",
                                "requiredBehaviors": ["behavior-a"],
                                "forbiddenBehaviors": ["behavior-b"],
                                "judgePlan": {
                                    "deterministicChecks": ["check-a"],
                                    "modelRubric": "rubric-a",
                                },
                                "executableCases": (
                                    ["case-a"] if agent == "agent-a" else []
                                ),
                                "coverageStatus": (
                                    "fixture-backed"
                                    if agent == "agent-a"
                                    else "declared"
                                ),
                            }
                        ],
                    }
                    for agent in scenario_agents
                ],
            },
        )
        self.write_yaml(
            "evals/workflow-packs.yaml",
            {
                "schema": "dev-methodology-workflow-packs",
                "version": 2,
                "coverageStatus": "declared",
                "sourceDigestPolicy": "sha256-at-run",
                "controls": {
                    "skill-ablation": {},
                    "wrong-skill-negative-control": {},
                },
                "packs": [
                    {
                        "id": "workflow-a",
                        "agents": list(scenario_agents),
                        "skillProbes": list(probe_ids.values()),
                        "phases": [
                            {
                                "id": "phase-a",
                                "agents": list(scenario_agents),
                                "requiredEvidence": ["evidence-a"],
                            }
                        ],
                        "judgePlan": {
                            "deterministicChecks": ["check-a"],
                            "modelRubric": "rubric-a",
                        },
                        "sandboxProfiles": {
                            "codex": ["codex-write"],
                            "junie": ["junie-write"],
                        },
                        "executableCases": ["case-a"],
                        "coverageStatus": "fixture-backed",
                    }
                ],
            },
        )
        self.write_yaml(
            "evals/judges.yaml",
            {
                "schema": "dev-methodology-judges",
                "version": 2,
                "coverageStatus": "declared",
                "sourceDigestPolicy": "sha256-at-run",
                "judgeTypes": {
                    "deterministic": {},
                    "model": {},
                    "human": {},
                },
                "executionOrder": ["deterministic", "model", "human"],
                "checks": [
                    {
                        "id": "check-a",
                        "type": "deterministic",
                        "description": "Exact check",
                        "critical": True,
                    }
                ],
                "rubrics": [
                    {
                        "id": "rubric-a",
                        "dimensions": ["completeness"],
                        "scale": [0, 1],
                    }
                ],
                "calibrationPolicy": {
                    "requiredBeforeVerifiedEvidence": True,
                    "status": calibration_status,
                    "missingOrPendingResult": "unverified",
                    "humanScoredSet": {
                        "minimumExamples": 20,
                        "requiredClasses": ["clear-pass", "clear-fail"],
                        "ambiguousExamples": {
                            "independentHumanJudges": 2,
                            "adjudicationRequired": True,
                        },
                    },
                    "agreementMetrics": {
                        "binary": ["precision", "recall", "f1"],
                        "ordered": ["weighted-kappa"],
                        "critical": ["recall"],
                    },
                    "thresholds": {
                        "binaryF1": 0.85,
                        "orderedWeightedKappa": 0.70,
                        "criticalDefectRecall": 1.0,
                    },
                    "recordedDigests": {
                        "required": [
                            "judgePromptSha256",
                            "judgeModelIdentity",
                            "reasoningProfile",
                            "rubricSha256",
                            "calibrationSetSha256",
                        ]
                    },
                    "records": [],
                },
            },
        )
        self.write_yaml(
            "evals/sandbox-profiles.yaml",
            {
                "schema": "dev-methodology-sandbox-profiles",
                "version": 2,
                "coverageStatus": "declared",
                "sourceDigestPolicy": "sha256-at-run",
                "snapshotPolicy": {},
                "containmentStatusVocabulary": {
                    "externally-contained": "externally attested",
                    "workspace-isolated-only": "workspace evidence only",
                    "containment-unverified": "no containment attestation",
                },
                "profiles": [
                    {
                        "id": f"{harness}-write",
                        "harness": harness,
                        "repositoryMutation": "required",
                        "implementationStatus": "planned",
                        "preparedSnapshot": True,
                        "copyOnWriteWorkspace": True,
                        "warmWorker": True,
                        "workspaceIsolation": "declared",
                        "containment": {
                            "filesystem": "planned",
                            "process": "planned",
                            "network": "planned",
                            "resources": "planned",
                            "reportedStatus": "containment-unverified",
                        },
                        "digestInputs": ["source"],
                    }
                    for harness in ("codex", "junie")
                ],
            },
        )

    def coverage(
        self,
        *,
        skills: tuple[str, ...] = ("skill-a",),
        agents: tuple[str, ...] = ("agent-a",),
        runner: object | None = None,
    ) -> dict[str, object]:
        """Build a snapshot against the temporary catalogs and declared inventory."""
        role_values = {
            agent: {
                "name": agent,
                "modelProfile": "default",
                "sourcePath": f"agents/roles/test/{agent}.role.yaml",
            }
            for agent in agents
        }
        return self.module.build_evaluation_coverage(
            self.root,
            {skill: "test" for skill in skills},
            role_values,
            eval_runner=runner,
        )

    def test_missing_catalog_is_an_exact_error(self) -> None:
        """Missing catalog files must stop generation instead of becoming empty coverage."""
        self.write_yaml(
            "evals/cases.yaml",
            {
                "schema": "dev-methodology-agent-skill-evals",
                "version": 2,
                "coverageStatus": "fixture-backed",
                "supportedHarnesses": ["codex", "junie"],
                "cases": [],
            },
        )

        with self.assertRaisesRegex(
            ValueError,
            r"Missing required evaluation catalogs: .*agent-scenarios\.yaml.*judges\.yaml.*sandbox-profiles\.yaml.*skill-probes\.yaml.*workflow-packs\.yaml",
        ):
            self.coverage()

    def test_every_skill_and_agent_requires_a_declaration(self) -> None:
        """The current inventories must be exactly represented in probe and scenario catalogs."""
        self.catalogs()

        with self.assertRaisesRegex(
            ValueError, r"Skills missing probe declarations: skill-b"
        ):
            self.coverage(skills=("skill-a", "skill-b"))

        with self.assertRaisesRegex(
            ValueError, r"Conceptual agents missing scenario declarations: agent-b"
        ):
            self.coverage(agents=("agent-a", "agent-b"))

    def test_evaluation_harnesses_are_codex_and_junie_only(self) -> None:
        """Catalog declarations cannot silently add an unsupported evaluation harness."""
        self.catalogs(probe_harnesses=("codex", "junie", "claude"))

        with self.assertRaisesRegex(
            ValueError,
            r"evals/skill-probes\.yaml harnesses must be exactly codex, junie; found claude, codex, junie",
        ):
            self.coverage()

    def test_snapshot_distinguishes_declaration_fixture_and_pending_judge(self) -> None:
        """A fixture-backed declaration must not become executed, calibrated, or verified."""
        self.catalogs()

        snapshot = self.coverage()
        skill = snapshot["skills"]["skill-a"]
        agent = snapshot["agents"]["agent-a"]

        self.assertTrue(skill["structural"])
        self.assertTrue(skill["probeDeclared"])
        self.assertTrue(skill["fixtureBacked"])
        self.assertTrue(skill["executableFixture"])
        self.assertEqual("pending", skill["judgeCalibration"])
        self.assertEqual([], skill["executedCases"])
        self.assertEqual([], skill["verifiedCases"])
        self.assertEqual([], skill["staleByDigestCases"])
        self.assertTrue(agent["structural"])
        self.assertTrue(agent["scenarioDeclared"])
        self.assertTrue(agent["fixtureBacked"])
        self.assertTrue(agent["executableFixture"])
        self.assertEqual("pending", agent["judgeCalibration"])
        self.assertEqual(["codex", "junie"], snapshot["harnesses"])
        self.assertEqual(
            {"codex", "junie"},
            {profile["harness"] for profile in snapshot["sandboxProfiles"]},
        )
        self.assertTrue(
            all(
                profile["containmentStatus"] == "containment-unverified"
                for profile in snapshot["sandboxProfiles"]
            )
        )
        self.assertEqual(
            {
                "structuralAgentCount": 1,
                "structuralSkillCount": 1,
                "probeDeclaredSkillCount": 1,
                "scenarioDeclaredAgentCount": 1,
                "declaredScenarioCount": 1,
                "workflowPackCount": 1,
                "fixtureBackedCaseCount": 1,
                "executableCaseCount": 1,
                "fixtureBackedAgentCount": 1,
                "fixtureBackedSkillCount": 1,
                "executableFixtureAgentCount": 1,
                "executableFixtureSkillCount": 1,
                "modelJudgeCalibratedAgentCount": 0,
                "modelJudgeCalibratedSkillCount": 0,
                "modelJudgePendingAgentCount": 1,
                "modelJudgePendingSkillCount": 1,
                "modelJudgeNotRequiredAgentCount": 0,
                "modelJudgeNotRequiredSkillCount": 0,
                "executedRunCount": 0,
                "verifiedRunCount": 0,
                "staleByDigestRunCount": 0,
                "executedAgentCount": 0,
                "executedSkillCount": 0,
                "verifiedAgentCount": 0,
                "verifiedSkillCount": 0,
                "staleByDigestAgentCount": 0,
                "staleByDigestSkillCount": 0,
            },
            snapshot["evidenceStatus"],
        )

    def test_calibrated_policy_requires_a_valid_record_for_every_rubric(self) -> None:
        """A status label alone cannot promote a Model Judge to calibrated."""
        self.catalogs(calibration_status="calibrated")

        with self.assertRaisesRegex(
            ValueError,
            r"calibrationPolicy status is calibrated but valid records are missing for: rubric-a",
        ):
            self.coverage()

    def test_receipt_classifier_controls_executed_verified_and_stale_states(self) -> None:
        """Reporting must preserve the runner verdict and keep stale evidence unverified."""
        self.catalogs()
        receipt = {
            "schema": "dev-methodology-eval-evidence",
            "version": 2,
            "case": "case-a",
            "verdict": "verified",
            "run": {"agentId": "agent-a", "harness": "codex"},
            "skills": [{"id": "skill-a", "contentDigest": "old"}],
        }
        self.write_yaml("evals/evidence/run-a.yaml", receipt)

        class Classification:
            """Mirrors the runner's stable receipt classification object."""

            def as_dict(self) -> dict[str, object]:
                """Expose conservative evidence state through the runner contract."""
                return {
                    "executed": True,
                    "verified": False,
                    "staleByDigest": True,
                    "errors": [],
                    "staleReasons": ["skill digest is stale"],
                }

        class StaleRunner:
            """Provides the runner classification boundary used by the reporter."""

            calls: list[str] = []

            @classmethod
            def classify_evidence(
                cls, case: dict[str, object], path: Path
            ) -> Classification:
                """Return a stale execution while recording validation use."""
                cls.calls.append(str(case["id"]))
                return Classification()

        snapshot = self.coverage(runner=StaleRunner)

        self.assertEqual(["case-a"], StaleRunner.calls)
        self.assertEqual(["case-a"], snapshot["skills"]["skill-a"]["executedCases"])
        self.assertEqual(
            ["case-a"], snapshot["skills"]["skill-a"]["staleByDigestCases"]
        )
        self.assertEqual([], snapshot["skills"]["skill-a"]["verifiedCases"])
        self.assertEqual(["case-a"], snapshot["agents"]["agent-a"]["executedCases"])
        self.assertEqual([], snapshot["agents"]["agent-a"]["verifiedCases"])

    def test_classifier_tuple_errors_are_not_dropped(self) -> None:
        """Runner validation errors remain blocking even when represented as tuples."""
        self.catalogs()
        self.write_yaml(
            "evals/evidence/run-a.yaml",
            {
                "schema": "dev-methodology-eval-evidence",
                "version": 2,
                "case": "case-a",
                "verdict": "verified",
                "run": {"agentId": "agent-a", "harness": "codex"},
                "skills": [{"id": "skill-a", "contentDigest": "current"}],
            },
        )

        class InvalidClassification:
            """Matches the attribute form of the runner classification."""

            executed = True
            verified = False
            stale_by_digest = False
            errors = ("missing captured agent attribution",)

        class InvalidRunner:
            """Returns a non-stale validator failure."""

            @staticmethod
            def classify_evidence(
                case: dict[str, object], path: Path
            ) -> InvalidClassification:
                """Return the validator failure for the supplied receipt."""
                return InvalidClassification()

        with self.assertRaisesRegex(
            ValueError, r"missing captured agent attribution"
        ):
            self.coverage(runner=InvalidRunner)

    def test_explorer_payload_exposes_status_without_promoting_verification(self) -> None:
        """Generated explorer data must carry the same conservative coverage snapshot."""
        self.catalogs()
        snapshot = self.coverage()

        payload = self.module.build_explorer_payload(
            {"skill-a": "test"},
            {
                "agent-a": {
                    "name": "agent-a",
                    "label": "Agent A",
                    "description": "Test agent",
                    "modelProfile": "default",
                    "skills": [],
                }
            },
            {},
            snapshot,
        )

        self.assertEqual(2, payload["version"])
        self.assertEqual([], payload["roles"][0]["coverage"]["verifiedCases"])
        self.assertEqual([], payload["skills"][0]["coverage"]["verifiedCases"])
        self.assertEqual("pending", payload["judgeStatus"]["calibrationStatus"])
        self.assertEqual(["codex", "junie"], payload["evaluationHarnesses"])


if __name__ == "__main__":
    unittest.main()
