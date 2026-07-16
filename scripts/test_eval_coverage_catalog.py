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

from scripts import agent_skill_judge_contract as judge_contract


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "build-support-checklist.py"


class CanonicalCalibrationValidator:
    """Accept only records whose governed fields match their canonical inputs."""

    canonical_judge_identity = staticmethod(judge_contract.canonical_judge_identity)

    @staticmethod
    def validate_calibration_record(
        record: dict[str, object], expected: dict[str, object]
    ) -> list[str]:
        """Model the runner boundary without trusting catalog-owned metrics."""
        errors = [
            f"{name} mismatch"
            for name, value in expected.items()
            if record.get(name) != value
        ]
        if record.get("acceptedByCanonicalValidator") is not True:
            errors.append("record was not canonically accepted")
        return errors


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

    def read_yaml(self, relative_path: str) -> dict[str, object]:
        """Read one temporary catalog for a focused mutation in a test."""
        value = yaml.safe_load((self.root / relative_path).read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise AssertionError(f"Expected a YAML mapping in {relative_path}")
        return value

    def calibration_record(
        self, rubric: dict[str, object], *, accepted: bool = True
    ) -> dict[str, object]:
        """Build a digest-bound record for the fake canonical validator."""
        identity = judge_contract.canonical_judge_identity(rubric)
        return {
            "rubricId": rubric["id"],
            "status": "accepted",
            **identity,
            "harness": "codex",
            "judgeModelIdentity": "judge-model",
            "reasoningProfile": "fixed-reasoning",
            "calibrationSetSha256": "calibration-set-digest",
            "acceptedByCanonicalValidator": accepted,
        }

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
                        "harnessExecutionStatus": {
                            "codex": "runnable",
                            "junie": "runnable",
                        },
                        "risk": {"level": "ordinary", "reasons": []},
                        "executionTier": "local",
                        "securityContainmentRequired": False,
                        "requiredSkills": list(probe_skills),
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
                            "wrongSkillControl": "control-skill",
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
                        "caseCoverageStatus": "partial",
                        "coverageStatus": "declared",
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
                        "type": "model",
                        "dimensions": ["completeness"],
                        "scale": "0-to-4-per-dimension",
                        "passRules": {
                            "noAggregateCompensation": True,
                            "minimumDimensionScore": 3,
                        },
                    }
                ],
                "calibrationPolicy": {
                    "requiredBeforeJudgeCalibrationClaim": True,
                    "status": calibration_status,
                    "promotionStatus": "disabled-pending-provenance",
                    "missingOrPendingResult": "calibration-pending",
                    "humanScoredSet": {
                        "pilotMinimumExamples": 20,
                        "minimumExamples": 25,
                        "minimumExamplesPerClass": 5,
                        "minimumCriticalDefects": 5,
                        "requiredClasses": [
                            "clear-pass",
                            "clear-fail",
                            "boundary",
                            "incomplete-plausible",
                            "adversarially-polished",
                        ],
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
                            "judgeOutputSchemaSha256",
                            "instructionEnvelopeSha256",
                            "harness",
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

    def test_high_risk_cases_are_explicit_and_not_locally_runnable(self) -> None:
        """Only an explicit high-risk contract selects the external tier."""
        self.catalogs()
        catalog = self.read_yaml("evals/cases.yaml")
        case = catalog["cases"][0]
        case["risk"] = {
            "level": "high",
            "reasons": ["executes an untrusted repository hook"],
        }
        case["executionTier"] = "externally-contained"
        case["securityContainmentRequired"] = True
        case["harnessExecutionStatus"] = {
            "codex": "external-runner-required",
            "junie": "external-runner-required",
        }
        self.write_yaml("evals/cases.yaml", catalog)

        snapshot = self.coverage()

        self.assertEqual([], snapshot["runnableCasesByHarness"]["codex"])
        self.assertEqual([], snapshot["runnableCasesByHarness"]["junie"])
        self.assertEqual(0, snapshot["evidenceStatus"]["ordinaryLocalCaseCount"])
        self.assertEqual(1, snapshot["evidenceStatus"]["highRiskExternalCaseCount"])

        case["executionTier"] = "local"
        case["securityContainmentRequired"] = False
        case["harnessExecutionStatus"] = {"codex": "runnable", "junie": "runnable"}
        self.write_yaml("evals/cases.yaml", catalog)
        with self.assertRaisesRegex(ValueError, "High-risk evaluation case"):
            self.coverage()

    def test_snapshot_distinguishes_declaration_fixture_and_pending_judge(self) -> None:
        """A fixture-backed declaration must not become executed, calibrated, or verified."""
        self.catalogs()

        snapshot = self.coverage()
        skill = snapshot["skills"]["skill-a"]
        agent = snapshot["agents"]["agent-a"]

        self.assertTrue(skill["structural"])
        self.assertTrue(skill["probeDeclared"])
        self.assertTrue(skill["positiveCaseBacked"])
        self.assertFalse(skill["negativeCaseBacked"])
        self.assertFalse(skill["pairedControlsExecutable"])
        self.assertFalse(skill["fixtureBacked"])
        self.assertFalse(skill["executableFixture"])
        self.assertEqual("pending", skill["judgeCalibration"])
        self.assertEqual([], skill["executedCases"])
        self.assertEqual([], skill["judgePassedCases"])
        self.assertEqual([], skill["securityContainedCases"])
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
        workflow = snapshot["workflows"]["workflow-a"]
        self.assertTrue(workflow["caseBacked"])
        self.assertEqual("partial", workflow["caseCoverageStatus"])
        self.assertFalse(workflow["fixtureBacked"])
        self.assertFalse(workflow["executableFixture"])
        self.assertEqual(["case-a"], snapshot["runnableCasesByHarness"]["codex"])
        self.assertEqual(["case-a"], snapshot["runnableCasesByHarness"]["junie"])
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
                "caseBackedWorkflowPackCount": 1,
                "partialWorkflowPackCount": 1,
                "endToEndFixtureBackedWorkflowPackCount": 0,
                "fixtureBackedCaseCount": 1,
                "executableCaseCount": 1,
                "codexRunnableCaseCount": 1,
                "junieRunnableCaseCount": 1,
                "ordinaryLocalCaseCount": 1,
                "highRiskExternalCaseCount": 0,
                "caseBackedAgentCount": 1,
                "partialScenarioBackedAgentCount": 0,
                "fixtureBackedAgentCount": 1,
                "positiveCaseBackedSkillCount": 1,
                "negativeCaseBackedSkillCount": 0,
                "pairedControlsExecutableSkillCount": 0,
                "fixtureBackedSkillCount": 0,
                "executableFixtureAgentCount": 1,
                "executableFixtureSkillCount": 0,
                "modelJudgeCalibratedAgentCount": 0,
                "modelJudgeCalibratedSkillCount": 0,
                "modelJudgePendingAgentCount": 1,
                "modelJudgePendingSkillCount": 1,
                "modelJudgeNotRequiredAgentCount": 0,
                "modelJudgeNotRequiredSkillCount": 0,
                "executedRunCount": 0,
                "judgePassedRunCount": 0,
                "securityContainedRunCount": 0,
                "verifiedRunCount": 0,
                "staleByDigestRunCount": 0,
                "judgeCalibrationStatusCounts": {},
                "executedAgentCount": 0,
                "executedSkillCount": 0,
                "judgePassedAgentCount": 0,
                "judgePassedSkillCount": 0,
                "securityContainedAgentCount": 0,
                "securityContainedSkillCount": 0,
                "verifiedAgentCount": 0,
                "verifiedSkillCount": 0,
                "staleByDigestAgentCount": 0,
                "staleByDigestSkillCount": 0,
                "positiveExecutedSkillCount": 0,
                "positiveJudgePassedSkillCount": 0,
                "positiveSecurityContainedSkillCount": 0,
                "positiveVerifiedSkillCount": 0,
                "positiveStaleByDigestSkillCount": 0,
            },
            snapshot["evidenceStatus"],
        )

    def test_calibrated_policy_requires_a_valid_record_for_every_rubric(self) -> None:
        """A status label alone cannot promote a Model Judge to calibrated."""
        self.catalogs(calibration_status="calibrated")

        with self.assertRaisesRegex(
            ValueError,
            r"calibrationPolicy status does not match canonical records: declared calibrated, derived pending",
        ):
            self.coverage()

    def test_diagnostic_calibration_record_cannot_promote_without_provenance(self) -> None:
        """Metric-valid self-reported labels remain diagnostic until provenance is implemented."""
        self.catalogs(calibration_status="pending")
        judges = self.read_yaml("evals/judges.yaml")
        rubric = judges["rubrics"][0]
        judges["calibrationPolicy"]["records"] = [
            self.calibration_record(rubric)
        ]
        self.write_yaml("evals/judges.yaml", judges)

        snapshot = self.coverage(runner=CanonicalCalibrationValidator)

        self.assertEqual("pending", snapshot["judgeStatus"]["calibrationStatus"])
        self.assertEqual([], snapshot["judgeStatus"]["calibratedRubrics"])
        self.assertEqual(["rubric-a"], snapshot["judgeStatus"]["pendingRubrics"])

    def test_fabricated_calibration_record_cannot_promote_a_rubric(self) -> None:
        """Matching status and digest-shaped text do not bypass canonical validation."""
        self.catalogs(calibration_status="calibrated")
        judges = self.read_yaml("evals/judges.yaml")
        rubric = judges["rubrics"][0]
        judges["calibrationPolicy"]["records"] = [
            self.calibration_record(rubric, accepted=False)
        ]
        self.write_yaml("evals/judges.yaml", judges)

        with self.assertRaisesRegex(
            ValueError,
            r"calibrationPolicy status does not match canonical records: declared calibrated, derived pending",
        ):
            self.coverage(runner=CanonicalCalibrationValidator)

    def test_stale_canonical_judge_prompt_cannot_promote_a_rubric(self) -> None:
        """Calibration is invalidated when its governed Judge prompt digest drifts."""
        self.catalogs(calibration_status="calibrated")
        judges = self.read_yaml("evals/judges.yaml")
        rubric = judges["rubrics"][0]
        record = self.calibration_record(rubric)
        record["judgePromptSha256"] = "0" * 64
        judges["calibrationPolicy"]["records"] = [record]
        self.write_yaml("evals/judges.yaml", judges)

        with self.assertRaisesRegex(
            ValueError,
            r"calibrationPolicy status does not match canonical records: declared calibrated, derived pending",
        ):
            self.coverage(runner=CanonicalCalibrationValidator)

    def test_disabled_promotion_keeps_every_rubric_pending(self) -> None:
        """A diagnostic record cannot calibrate any harness, model, or reasoning route."""
        self.catalogs(calibration_status="pending")
        judges = self.read_yaml("evals/judges.yaml")
        first_rubric = judges["rubrics"][0]
        judges["rubrics"].append(
            {
                "id": "rubric-b",
                "type": "model",
                "dimensions": ["correctness"],
                "scale": "0-to-4-per-dimension",
                "passRules": {
                    "noAggregateCompensation": True,
                    "minimumDimensionScore": 3,
                },
            }
        )
        judges["calibrationPolicy"]["records"] = [
            self.calibration_record(first_rubric)
        ]
        self.write_yaml("evals/judges.yaml", judges)

        snapshot = self.coverage(runner=CanonicalCalibrationValidator)

        self.assertEqual("pending", snapshot["judgeStatus"]["calibrationStatus"])
        self.assertEqual([], snapshot["judgeStatus"]["calibratedRubrics"])
        self.assertEqual(
            ["rubric-a", "rubric-b"],
            snapshot["judgeStatus"]["pendingRubrics"],
        )

    def test_partial_agent_case_coverage_is_not_full_fixture_coverage(self) -> None:
        """Backing one of two scenarios cannot promote the whole agent."""
        self.catalogs()
        catalog = self.read_yaml("evals/agent-scenarios.yaml")
        catalog["agents"][0]["scenarios"].append(
            {
                "id": "scenario-agent-a-boundary",
                "kind": "boundary",
                "fixtureProfile": "fixture-a",
                "promptIntent": "refuse out-of-scope work",
                "expectedOutcome": "BLOCKED",
                "requiredBehaviors": ["behavior-a"],
                "forbiddenBehaviors": ["behavior-b"],
                "judgePlan": {
                    "deterministicChecks": ["check-a"],
                    "modelRubric": "rubric-a",
                },
                "executableCases": [],
                "coverageStatus": "declared",
            }
        )
        self.write_yaml("evals/agent-scenarios.yaml", catalog)

        snapshot = self.coverage()
        state = snapshot["agents"]["agent-a"]

        self.assertTrue(state["caseBacked"])
        self.assertTrue(state["partialScenarioCoverage"])
        self.assertFalse(state["fixtureBacked"])
        self.assertFalse(state["executableFixture"])

    def test_wrong_skill_control_cannot_already_be_required_by_the_case(self) -> None:
        """A wrong-skill control must be distinct from both target and base support skills."""
        self.catalogs()
        catalog = self.read_yaml("evals/cases.yaml")
        catalog["cases"][0]["requiredSkills"].append("control-skill")
        self.write_yaml("evals/cases.yaml", catalog)

        with self.assertRaisesRegex(
            ValueError,
            r"wrongSkillControl control-skill is already required by evaluation case case-a",
        ):
            self.coverage()

    def test_receipt_classifier_preserves_independent_claims_and_stale_state(self) -> None:
        """Reporting keeps execution, Judge, security, and digest claims independent."""
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
                    "judgePassed": True,
                    "securityContained": False,
                    "judgeCalibrationStatus": "pending",
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
        self.assertEqual([], snapshot["skills"]["skill-a"]["executedCases"])
        self.assertEqual(
            ["case-a"], snapshot["skills"]["skill-a"]["positiveExecutedCases"]
        )
        self.assertEqual(
            ["case-a"],
            snapshot["skills"]["skill-a"]["positiveStaleByDigestCases"],
        )
        self.assertEqual(
            ["case-a"],
            snapshot["skills"]["skill-a"]["positiveJudgePassedCases"],
        )
        self.assertEqual(
            [],
            snapshot["skills"]["skill-a"]["positiveSecurityContainedCases"],
        )
        self.assertEqual([], snapshot["skills"]["skill-a"]["verifiedCases"])
        self.assertEqual(["case-a"], snapshot["agents"]["agent-a"]["executedCases"])
        self.assertEqual(["case-a"], snapshot["agents"]["agent-a"]["judgePassedCases"])
        self.assertEqual([], snapshot["agents"]["agent-a"]["securityContainedCases"])
        self.assertEqual([], snapshot["agents"]["agent-a"]["verifiedCases"])

    def test_receipt_does_not_credit_support_skills_as_target_probes(self) -> None:
        """A case receipt attributes positive evidence only to explicit target probes."""
        self.catalogs(probe_skills=("skill-a", "skill-support"))
        self.write_yaml(
            "evals/evidence/run-a.yaml",
            {
                "schema": "dev-methodology-eval-evidence",
                "version": 2,
                "case": "case-a",
                "verdict": "verified",
                "run": {"agentId": "agent-a", "harness": "codex"},
                "skills": [
                    {"id": "skill-a", "contentDigest": "current"},
                    {"id": "skill-support", "contentDigest": "current"},
                ],
            },
        )

        class VerifiedClassification:
            """Represents a valid positive-case execution from the runner."""

            def as_dict(self) -> dict[str, object]:
                """Expose the accepted receipt classification."""
                return {
                    "executed": True,
                    "judgePassed": True,
                    "securityContained": False,
                    "judgeCalibrationStatus": "pending",
                    "verified": True,
                    "staleByDigest": False,
                    "errors": [],
                }

        class VerifiedRunner:
            """Returns one accepted positive-case classification."""

            @staticmethod
            def classify_evidence(
                case: dict[str, object], path: Path
            ) -> VerifiedClassification:
                """Classify the synthetic receipt as accepted."""
                return VerifiedClassification()

        snapshot = self.coverage(
            skills=("skill-a", "skill-support"), runner=VerifiedRunner
        )

        target = snapshot["skills"]["skill-a"]
        support = snapshot["skills"]["skill-support"]
        self.assertEqual(["case-a"], target["positiveExecutedCases"])
        self.assertEqual(["case-a"], target["positiveJudgePassedCases"])
        self.assertEqual([], target["positiveSecurityContainedCases"])
        self.assertEqual(["case-a"], target["positiveVerifiedCases"])
        self.assertEqual([], target["executedCases"])
        self.assertEqual([], support["positiveExecutedCases"])
        self.assertEqual([], support["positiveJudgePassedCases"])
        self.assertEqual([], support["positiveSecurityContainedCases"])
        self.assertEqual([], support["positiveVerifiedCases"])
        self.assertEqual([], support["executedCases"])

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
            judge_passed = False
            security_contained = False
            judge_calibration_status = "not-evaluated"
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
        self.assertEqual([], payload["roles"][0]["judgePassedCases"])
        self.assertEqual([], payload["roles"][0]["securityContainedCases"])
        self.assertEqual([], payload["roles"][0]["coverage"]["verifiedCases"])
        self.assertEqual([], payload["skills"][0]["judgePassedCases"])
        self.assertEqual([], payload["skills"][0]["securityContainedCases"])
        self.assertEqual([], payload["skills"][0]["coverage"]["verifiedCases"])
        self.assertEqual("pending", payload["judgeStatus"]["calibrationStatus"])
        self.assertEqual(["codex", "junie"], payload["evaluationHarnesses"])


if __name__ == "__main__":
    unittest.main()
