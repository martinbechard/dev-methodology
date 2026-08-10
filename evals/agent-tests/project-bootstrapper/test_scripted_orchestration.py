# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies deterministic Project Bootstrapper orchestration, correction, failure, timeout, and cleanup behavior.
# Governing implementation: evals/agent-tests/project-bootstrapper/scripted_orchestration.py

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock


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
        self.assertNotIn("wiki-ingester", {event["agent"] for event in first["trace"]})

    def test_isolated_snapshot_contains_only_declared_inputs(self) -> None:
        result = scripted.run_isolated()
        copied = result["copiedInputs"]
        self.assertIn("agents/roles/project-setup/project-bootstrapper.role.yaml", copied)
        self.assertIn("agents/roles/wiki-activities/wiki-ingester.role.yaml", copied)
        self.assertNotIn("generated/adapters/codex/agents/project-bootstrapper.toml", copied)
        self.assertNotIn("generated/adapters/codex/agents/wiki-ingester.toml", copied)
        self.assertIn("evals/agent-tests/project-bootstrapper/agents", copied)
        self.assertIn(
            "evals/agent-tests/project-bootstrapper/fixtures/missing-configuration-multi-contribution",
            copied,
        )
        self.assertIn("skills/set-solo-mode", copied)
        self.assertIn("skills/set-multitask-mode", copied)
        self.assertIn("skills/resource-claim", copied)
        self.assertIn("skills/resource-claim-helper-command", copied)
        self.assertIn("skills/structured-explanation", copied)
        self.assertIn("skills/document-provenance", copied)
        self.assertIn("PROJECT.yaml", copied)
        self.assertIn("scripts/render-agents-technology-skills.py", copied)
        self.assertNotIn("agents", copied)
        self.assertNotIn("skills", copied)
        self.assertNotIn("evals/agent-tests/runner.py", copied)

        generated = result["generatedProjectionIntegration"]
        self.assertEqual("authoritative-source-only", generated["candidateSnapshot"])
        self.assertEqual(
            [
                "python3 scripts/build-skill-docs.py",
                "python3 scripts/build-skill-docs.py --check",
                "python3.11 evals/agent-tests/project-bootstrapper/scripted_orchestration.py",
            ],
            generated["requiredFreshMainCommands"],
        )
        self.assertEqual(
            [
                "generated/adapters/codex/agents/project-bootstrapper.toml",
                "generated/adapters/codex/agents/wiki-ingester.toml",
            ],
            generated["excludedGeneratedProjections"],
        )
        for projection in generated["excludedGeneratedProjections"]:
            self.assertNotIn(projection, scripted._TARGET_DIGESTS)

    def test_both_configuration_outputs_receive_independent_reviews(self) -> None:
        result = scripted.run_isolated()
        reviewed = {
            event["artifact"]
            for event in result["trace"]
            if event["agent"] == "dev-artifact-reviewer" and event["phase"] == "review"
        }
        self.assertTrue({"PROJECT.yaml", "AGENTS.md"}.issubset(reviewed))

    def test_configuration_dependency_invokes_each_public_setup_procedure(self) -> None:
        """Bootstrap delegates the three configuration procedures in their public order."""

        result = scripted.run_isolated()
        phases = [
            event["phase"]
            for event in result["configurationExecution"]["trace"]
            if event["agent"] == "project-configurator"
        ]

        self.assertEqual(
            [
                "Configure Project Agents And Skills",
                "Render Project Guidance",
                "Verify Project Configuration",
            ],
            phases,
        )
        self.assertNotIn("configure", phases)

    def test_missing_configuration_uses_primary_claim_free_handoff_then_resumes(self) -> None:
        """Keep the missing-file run terminal and resume only in a separate configured run."""

        result = scripted.run_isolated()
        self.assertEqual("PASS", result["status"])
        initial = result["initialExecution"]
        configuration = result["configurationExecution"]
        resumed = result["resumedExecution"]

        self.assertEqual("initial-project-bootstrapper", initial["executionId"])
        self.assertEqual("BLOCKED", initial["status"])
        self.assertEqual(
            "PRIMARY_PROJECT_CONFIGURATOR_HANDOFF_REQUIRED",
            initial["reason"],
        )
        self.assertTrue(initial["preconfigurationClaimStateUntouched"])
        self.assertEqual("SOLO", initial["effectiveCoordinationMode"])
        self.assertEqual(1, len(initial["trace"]))
        self.assertEqual(
            "require-primary-project-configurator",
            initial["trace"][0]["phase"],
        )
        self.assertEqual("primary", initial["trace"][0]["dispatchContext"])
        self.assertFalse(
            any(event["agent"] == "scripted-claim-double" for event in initial["trace"])
        )
        self.assertFalse(
            any(event["dispatchContext"] == "secondary" for event in initial["trace"])
        )

        self.assertEqual("primary-project-configurator", configuration["executionId"])
        self.assertEqual("PASS", configuration["status"])
        self.assertEqual("repository-render-validator", configuration["validationGate"])
        configurator_events = configuration["trace"]
        self.assertEqual(3, len(configurator_events))
        self.assertTrue(
            all(event["dispatchContext"] == "primary" for event in configurator_events)
        )
        self.assertFalse(
            any(event["agent"] == "scripted-claim-double" for event in configurator_events)
        )

        self.assertEqual("resumed-project-bootstrapper", resumed["executionId"])
        self.assertEqual("PASS", resumed["status"])
        self.assertEqual("repository-render-validator", resumed["validationGate"])
        self.assertEqual("PASS", result["status"])
        self.assertEqual(resumed["trace"], result["trace"])
        self.assertEqual("resource-claim", resumed["configuredCoordination"])
        self.assertTrue(resumed["secondaryDispatchEnabled"])
        self.assertTrue(
            any(event["agent"] == "scripted-claim-double" for event in resumed["trace"])
        )
        self.assertTrue(
            any(event["dispatchContext"] == "secondary" for event in resumed["trace"])
        )

    def test_validated_configuration_selectors_cover_solo_multitask_and_legacy(self) -> None:
        """Derive dispatch, coordination, and workflow behavior through the real validator."""

        expected = {
            "canonical-solo": {
                "concurrentTasking": False,
                "dispatchSelector": "DISABLED_BY_PROJECT_CONFIGURATION",
                "secondaryDispatchEnabled": False,
                "resourceCoordination": "none",
                "claimStackEnabled": False,
                "legacyConfiguration": False,
            },
            "canonical-multitask": {
                "concurrentTasking": True,
                "dispatchSelector": "ENABLED_BY_PROJECT_CONFIGURATION",
                "secondaryDispatchEnabled": True,
                "resourceCoordination": "resource-claim",
                "claimStackEnabled": True,
                "legacyConfiguration": False,
            },
            "legacy": {
                "concurrentTasking": None,
                "dispatchSelector": "PRESERVE_VALID_LEGACY_CONFIGURATION",
                "secondaryDispatchEnabled": None,
                "resourceCoordination": "resource-claim",
                "claimStackEnabled": True,
                "legacyConfiguration": True,
            },
        }

        for case, selectors in expected.items():
            with self.subTest(case=case):
                observed = scripted.validated_configuration_case(case)
                self.assertEqual("PASS", observed["validation"])
                for key, value in selectors.items():
                    self.assertEqual(value, observed[key])
                self.assertEqual("file", observed["persistence"])
                self.assertEqual("main-branch", observed["commit"])
                self.assertEqual(
                    "deliver-work-item-main-branch",
                    observed["commitProviderSkill"],
                )

        solo = scripted.validated_configuration_case("canonical-solo")
        self.assertEqual(
            ["create-work-item-file", "manage-work-items-file"],
            solo["persistenceProviderSkills"],
        )
        self.assertEqual([], solo["resourceCoordinationProviderSkills"])
        self.assertEqual(
            "deliver-work-item-main-branch",
            solo["commitProviderSkill"],
        )

    def test_resumed_execution_obeys_canonical_solo_and_legacy_selectors(self) -> None:
        """Apply validated selector results instead of hard-coding multitask claims."""

        solo = scripted.run_isolated(configuration_case="canonical-solo")
        self.assertEqual("PASS", solo["status"])
        self.assertEqual("none", solo["configuredCoordination"])
        self.assertFalse(solo["secondaryDispatchEnabled"])
        self.assertEqual("file", solo["persistence"])
        self.assertFalse(
            any(event["agent"] == "scripted-claim-double" for event in solo["trace"])
        )
        self.assertFalse(
            any(event["dispatchContext"] == "secondary" for event in solo["trace"])
        )

        with self.assertRaisesRegex(
            ValueError,
            "legacy configuration requires an explicit existing runtime dispatch setting",
        ):
            scripted.run_isolated(configuration_case="legacy")

        for runtime_dispatch in (False, True):
            with self.subTest(runtime_dispatch=runtime_dispatch):
                legacy = scripted.run_isolated(
                    configuration_case="legacy",
                    legacy_runtime_dispatch=runtime_dispatch,
                )
                self.assertEqual("PASS", legacy["status"])
                self.assertEqual("resource-claim", legacy["configuredCoordination"])
                self.assertIsNone(legacy["secondaryDispatchEnabled"])
                self.assertEqual(runtime_dispatch, legacy["effectiveSecondaryDispatchEnabled"])
                self.assertEqual(runtime_dispatch, legacy["legacyRuntimeDispatchBefore"])
                self.assertEqual(runtime_dispatch, legacy["legacyRuntimeDispatchAfter"])
                self.assertEqual(
                    "PRESERVE_VALID_LEGACY_CONFIGURATION",
                    legacy["dispatchSelector"],
                )
                self.assertTrue(
                    any(
                        event["agent"] == "scripted-claim-double"
                        for event in legacy["trace"]
                    )
                )
                self.assertEqual(
                    runtime_dispatch,
                    any(
                        event["dispatchContext"] == "secondary"
                        for event in legacy["trace"]
                    ),
                )

    def test_configuration_output_rejects_an_aggregate_selected_skill_set(self) -> None:
        """Bootstrap accepts exact routes but rejects the forbidden aggregate shortcut."""

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
        confirmed_skills = {"fastapi", "python"}

        self.assertEqual(
            "PASS",
            scripted._evaluate_project_configuration_output(
                composed_routes, confirmed_skills
            ),
        )
        self.assertEqual(
            "FAIL",
            scripted._evaluate_project_configuration_output(
                aggregate_output, confirmed_skills
            ),
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
                    scripted._evaluate_project_configuration_output(
                        invalid, confirmed_skills
                    ),
                )

    def test_reverse_engineering_audit_routes_corrections_and_reaches_steady_state(self) -> None:
        result = scripted.run_isolated(reverse_engineering=True)

        self.assertEqual("PASS", result["status"])
        audit_events = [
            event
            for event in result["trace"]
            if event["agent"] == "wiki-ingester"
            and event["phase"] == "final-evidence-audit"
        ]
        self.assertEqual(["NEEDS_CORRECTION", "PASS"], [event["outcome"] for event in audit_events])
        self.assertTrue(result["auditFindings"])
        for finding in result["auditFindings"]:
            self.assertEqual(
                {
                    "artifact",
                    "owner",
                    "reason",
                    "authoritativeEvidence",
                    "requiredWork",
                },
                set(finding),
            )
        ownership_finding = next(
            finding
            for finding in result["auditFindings"]
            if finding["artifact"] == "docs/wiki/topic-index.md"
        )
        self.assertIn("contradicts wiki-writer", ownership_finding["reason"])
        self.assertEqual([], result["finalAuditFindings"])
        self.assertIn("docs/module-catalog-design.md", result["accepted"])

        routed = {
            (event["artifact"], event["agent"], event["phase"])
            for event in result["trace"]
            if event["phase"] in {"create", "correct-steady-state"}
        }
        self.assertIn(
            ("docs/module-catalog-design.md", "dev-documentation-writer", "create"),
            routed,
        )
        self.assertIn(("PROJECT.yaml", "project-configurator", "correct-steady-state"), routed)
        self.assertIn(("docs/wiki/README.md", "wiki-architect", "correct-steady-state"), routed)
        self.assertIn(("docs/wiki/topic-index.md", "wiki-writer", "correct-steady-state"), routed)
        self.assertNotIn(
            "wiki-ingester",
            {
                event["agent"]
                for event in result["trace"]
                if event["phase"] in {"create", "correct-steady-state"}
            },
        )
        self.assertFalse(
            any(
                event["agent"] == "scripted-claim-double"
                and event["artifact"] == "integrated-tree"
                for event in result["trace"]
            )
        )

        reintegration_index = next(
            event["index"]
            for event in result["trace"]
            if event["agent"] == "dev-merge-coordinator"
            and event["phase"] == "reintegrate"
            and event["artifact"] == "audit-corrections"
        )
        post_integration_reviews = [
            event
            for event in result["trace"]
            if event["phase"] == "post-audit-integration-review"
        ]
        self.assertTrue(post_integration_reviews)
        self.assertTrue(
            all(reintegration_index < event["index"] for event in post_integration_reviews)
        )

        final_text = "\n".join(result["finalArtifacts"].values()).lower()
        for marker in scripted._STALE_MARKERS:
            with self.subTest(marker=marker):
                self.assertNotIn(marker, final_text)
        self.assertIn("module-catalog-design.md", result["finalArtifacts"]["docs/module-catalog.md"])
        self.assertIn("docs/module-catalog-design.md", result["finalArtifacts"]["docs/coverage-manifest.yaml"])
        self.assertIn("Owner: wiki-writer", result["finalArtifacts"]["docs/wiki/topic-index.md"])
        final_verification_index = next(
            event["index"]
            for event in result["trace"]
            if event["agent"] == "dev-verifier" and event["phase"] == "final-verification"
        )
        self.assertLess(audit_events[-1]["index"], final_verification_index)

    def test_reverse_engineering_audit_blocks_without_required_ledger(self) -> None:
        result = scripted.run_isolated(
            {"omitAuditEvidence": ["path-coverage-ledger.json"]},
            reverse_engineering=True,
        )

        self.assertEqual("BLOCKED", result["status"])
        self.assertEqual("path-coverage-ledger.json is unavailable", result["reason"])
        audit_events = [
            event
            for event in result["trace"]
            if event["agent"] == "wiki-ingester"
            and event["phase"] == "final-evidence-audit"
        ]
        self.assertEqual(["BLOCKED"], [event["outcome"] for event in audit_events])
        self.assertFalse(
            any(
                event["artifact"] == "integrated-tree"
                for event in result["trace"]
                if event["agent"] == "scripted-claim-double"
            )
        )

    def test_reverse_engineering_audit_blocks_without_coverage_manifest_evidence(self) -> None:
        result = scripted.run_isolated(
            {"removeAuditArtifact": ["docs/coverage-manifest.yaml"]},
            reverse_engineering=True,
        )

        self.assertEqual("BLOCKED", result["status"])
        self.assertEqual("coverage manifest is unavailable", result["reason"])

    def test_reverse_engineering_audit_routes_missing_auditable_artifacts(self) -> None:
        for artifact, owner in (
            ("docs/module-catalog.md", "dev-documentation-writer"),
            ("docs/wiki/topic-index.md", "wiki-writer"),
        ):
            with self.subTest(artifact=artifact):
                result = scripted.run_isolated(
                    {"removeAuditArtifact": [artifact]},
                    reverse_engineering=True,
                )

                self.assertEqual("PASS", result["status"])
                finding = next(
                    item for item in result["auditFindings"] if item["artifact"] == artifact
                )
                self.assertIn("missing from the final integrated tree", finding["reason"])
                self.assertEqual(owner, finding["owner"])
                self.assertIn(artifact, result["finalArtifacts"])

    def test_reverse_engineering_audit_owner_corrections_are_bounded(self) -> None:
        corrected = scripted.run_isolated(
            {"correct-steady-state:PROJECT.yaml": ["NEEDS_CORRECTION", "PASS"]},
            reverse_engineering=True,
        )
        self.assertEqual("PASS", corrected["status"])
        project_corrections = [
            event
            for event in corrected["trace"]
            if event["agent"] == "project-configurator"
            and event["phase"] == "correct-steady-state"
            and event["artifact"] == "PROJECT.yaml"
        ]
        self.assertEqual(
            ["NEEDS_CORRECTION", "PASS"],
            [event["outcome"] for event in project_corrections],
        )

        capped = scripted.run_isolated(
            {
                "correct-steady-state:PROJECT.yaml": [
                    "NEEDS_CORRECTION",
                    "NEEDS_CORRECTION",
                ]
            },
            reverse_engineering=True,
        )
        self.assertEqual("BLOCKED", capped["status"])
        self.assertEqual(
            "audit owner correction cap reached: PROJECT.yaml",
            capped["reason"],
        )

        reset_probe = scripted.run_isolated(
            {
                "correct-steady-state:PROJECT.yaml": ["NEEDS_CORRECTION", "PASS"],
                "post-audit-integration-review:PROJECT.yaml": ["NEEDS_CORRECTION"],
            },
            reverse_engineering=True,
        )
        self.assertEqual("BLOCKED", reset_probe["status"])
        self.assertEqual(
            "audit owner correction cap reached: PROJECT.yaml",
            reset_probe["reason"],
        )
        self.assertEqual(
            2,
            sum(
                event["agent"] == "project-configurator"
                and event["phase"] == "correct-steady-state"
                and event["artifact"] == "PROJECT.yaml"
                for event in reset_probe["trace"]
            ),
        )

    def test_reverse_engineering_audit_rejects_incomplete_path_classifications(self) -> None:
        result = scripted.run_isolated(
            {"emptyTrackedClassifications": ["true"]},
            reverse_engineering=True,
        )

        self.assertEqual("BLOCKED", result["status"])
        self.assertIn(
            "tracked path classifications do not match baseline",
            result["reason"],
        )

    def test_reverse_engineering_audit_requires_hashed_baseline_for_every_source(self) -> None:
        result = scripted.run_isolated(
            {"addUnmappedSource": ["src/payments.py"]},
            reverse_engineering=True,
        )

        self.assertEqual("BLOCKED", result["status"])
        self.assertIn(
            "MUST_DOCUMENT paths do not match hashed source baseline",
            result["reason"],
        )
        self.assertIn("src/payments.py", result["reason"])

    def test_reverse_engineering_audit_rejects_baseline_classification_mismatch(self) -> None:
        result = scripted.run_isolated(
            {"baselineClassificationMismatch": ["src/catalog.py"]},
            reverse_engineering=True,
        )

        self.assertEqual("BLOCKED", result["status"])
        self.assertIn(
            "source baseline classification contradicts tracked ledger: src/catalog.py",
            result["reason"],
        )

    def test_reverse_engineering_audit_detects_swapped_manifest_mappings(self) -> None:
        result = scripted.run_isolated(
            {"swapCoverageManifestMappings": ["true"]},
            reverse_engineering=True,
        )

        self.assertEqual("PASS", result["status"])
        finding = next(
            item
            for item in result["auditFindings"]
            if item["artifact"] == "docs/coverage-manifest.yaml"
        )
        self.assertIn("source-to-design mappings contradict", finding["reason"])

    def test_reverse_engineering_audit_parses_the_exact_owner_field(self) -> None:
        result = scripted.run_isolated(
            {"ownershipSubstringTrap": ["docs/wiki/topic-index.md"]},
            reverse_engineering=True,
        )

        self.assertEqual("PASS", result["status"])
        finding = next(
            item
            for item in result["auditFindings"]
            if item["artifact"] == "docs/wiki/topic-index.md"
        )
        self.assertIn("contribution-agent", finding["reason"])
        self.assertIn("contradicts wiki-writer", finding["reason"])

    def test_verification_correction_is_reviewed_and_reaudited_before_retry(self) -> None:
        result = scripted.run_isolated(
            {
                "final-verification:integration": ["NEEDS_CORRECTION", "PASS"],
                "verificationFinding": ["AGENTS.md"],
                "verificationMutationMarker": ["AGENTS.md"],
            },
            reverse_engineering=True,
        )

        self.assertEqual("PASS", result["status"])
        audits = [
            event
            for event in result["trace"]
            if event["agent"] == "wiki-ingester"
            and event["phase"] == "final-evidence-audit"
        ]
        self.assertEqual(
            ["NEEDS_CORRECTION", "PASS", "NEEDS_CORRECTION", "PASS"],
            [event["outcome"] for event in audits],
        )
        verifications = [
            event
            for event in result["trace"]
            if event["agent"] == "dev-verifier"
            and event["phase"] == "final-verification"
        ]
        correction_review = next(
            event
            for event in result["trace"]
            if event["phase"] == "post-verification-correction-review"
            and event["artifact"] == "AGENTS.md"
        )
        self.assertLess(correction_review["index"], audits[-1]["index"])
        self.assertLess(audits[-1]["index"], verifications[-1]["index"])
        verification_audit_correction = next(
            event
            for event in result["trace"]
            if event["agent"] == "project-configurator"
            and event["phase"] == "correct-steady-state"
            and correction_review["index"] < event["index"] < audits[-1]["index"]
        )
        self.assertLess(verification_audit_correction["index"], audits[-1]["index"])

    def test_verification_correction_uses_persistent_owner_for_audit_created_document(self) -> None:
        result = scripted.run_isolated(
            {
                "final-verification:integration": ["NEEDS_CORRECTION", "PASS"],
                "verificationFinding": ["docs/module-catalog-design.md"],
            },
            reverse_engineering=True,
        )

        self.assertEqual("PASS", result["status"])
        correction = next(
            event
            for event in result["trace"]
            if event["phase"] == "correct"
            and event["artifact"] == "docs/module-catalog-design.md"
        )
        self.assertEqual("dev-documentation-writer", correction["agent"])

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
        self.assertTrue(callable(getattr(scripted, "_start_owned_process", None)))
        self.assertTrue(callable(getattr(scripted, "_terminate_owned_process_tree", None)))
        timed_out_process = mock.Mock(pid=12345)
        timed_out_process.wait.side_effect = subprocess.TimeoutExpired(
            [sys.executable, "worker"],
            0.1,
        )
        with (
            mock.patch.object(
                scripted,
                "_start_owned_process",
                return_value=timed_out_process,
            ),
            mock.patch.object(scripted, "_terminate_owned_process_tree") as terminate,
        ):
            result = scripted.run_isolated(timeout_seconds=0.1)
        terminate.assert_called_once_with(timed_out_process)
        self.assertEqual("INFRASTRUCTURE_FAILED", result["status"])
        self.assertEqual("wall-clock timeout", result["reason"])
        self.assertEqual("complete", result["ownedProcessCleanup"])
        self.assertTrue(result["workspaceRemoved"])

        with tempfile.TemporaryDirectory(prefix="project-bootstrapper-timeout-test-") as directory:
            root = Path(directory)
            descendant_started = root / "descendant-started"
            descendant_completed = root / "descendant-completed"
            descendant_script = (
                "import pathlib, time; "
                f"pathlib.Path({str(descendant_started)!r}).write_text('started', encoding='utf-8'); "
                "time.sleep(0.5); "
                f"pathlib.Path({str(descendant_completed)!r}).write_text('survived', encoding='utf-8')"
            )
            root_script = (
                "import subprocess, sys, time; "
                f"subprocess.Popen([sys.executable, '-c', {descendant_script!r}]); "
                "time.sleep(3600)"
            )
            process = scripted._start_owned_process([sys.executable, "-c", root_script])
            try:
                for _ in range(100):
                    if descendant_started.exists():
                        break
                    time.sleep(0.01)
                else:
                    self.fail("owned descendant did not start")
                scripted._terminate_owned_process_tree(process)
            finally:
                if process.poll() is None:
                    process.kill()
                    process.wait(timeout=10)
            self.assertIsNotNone(process.returncode)
            time.sleep(0.75)
            self.assertFalse(
                descendant_completed.exists(),
                "timeout cleanup left its owned descendant running",
            )


if __name__ == "__main__":
    unittest.main()
