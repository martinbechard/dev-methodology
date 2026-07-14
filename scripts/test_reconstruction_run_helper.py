# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies reconstruction seed isolation, hashing, archive sealing, and retention.
# Governing design: skills/documentation-reverse-engineer/SKILL.md

from __future__ import annotations

import contextlib
import importlib.util
import hashlib
import io
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from types import ModuleType


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
HELPER_PATH = (
    REPOSITORY_ROOT
    / "skills"
    / "documentation-reverse-engineer"
    / "scripts"
    / "reconstruction_run.py"
)
HELPER_MODULE_NAME = "documentation_reconstruction_run"


def load_helper() -> ModuleType:
    """Load the portable reconstruction helper from its distributed skill package."""
    specification = importlib.util.spec_from_file_location(
        HELPER_MODULE_NAME,
        HELPER_PATH,
    )
    if specification is None or specification.loader is None:
        raise RuntimeError(f"Unable to load reconstruction helper from {HELPER_PATH}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


class ReconstructionRunHelperTests(unittest.TestCase):
    """Exercise the helper at filesystem boundaries using disposable repositories."""

    @classmethod
    def setUpClass(cls) -> None:
        """Load the helper once so each test exercises the same public module surface."""
        cls.helper = load_helper()

    def setUp(self) -> None:
        """Create a temporary source project with a closed documentation link graph."""
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.workspace = Path(self.temporary_directory.name)
        self.source = self.workspace / "source-project"
        self.build_root = self.workspace / "reconstructed-project"
        self.archive_root = self.workspace / "archives"
        self._write(
            self.source / "docs" / "wiki" / "index.md",
            "# Wiki\n\n[Architecture](../architecture/system.md)\n",
        )
        self._write(
            self.source / "docs" / "architecture" / "system.md",
            "# Architecture\n\n[Workflow](../functional/workflow.md)\n",
        )
        self._write(
            self.source / "docs" / "functional" / "workflow.md",
            "# Workflow\n",
        )
        self._write(
            self.source / "docs" / "modules" / "unlinked.md",
            "# Unlinked module\n",
        )
        self._write(self.source / "PROJECT.yaml", "project: fixture\n")
        self._write(self.source / "AGENTS.md", "# Fixture guidance\n")
        self._write(
            self.source / "src" / "feature" / "AGENTS.md",
            "# Nested fixture guidance\n",
        )

    def _write(self, path: Path, content: str) -> None:
        """Write one UTF-8 fixture file after creating its parent directory."""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def _write_json(self, path: Path, payload: object) -> None:
        """Write one stable JSON fixture through the test's filesystem boundary."""
        self._write(path, json.dumps(payload, indent=2, sort_keys=True) + "\n")

    def _sha256(self, path: Path) -> str:
        """Return the SHA-256 digest used by fixture evidence references."""
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def _binding_digest(self, *values: str) -> str:
        """Reproduce the helper's documented null-delimited binding digest."""
        digest = hashlib.sha256()
        for value in values:
            digest.update(value.encode("utf-8"))
            digest.update(b"\0")
        return digest.hexdigest()

    def _initialize(self) -> dict[str, object]:
        """Initialize the standard fixture run through the helper's public API."""
        return self.helper.initialize_run(
            source_project=self.source,
            build_root=self.build_root,
            run_id="run-004",
            source_baseline="abc123",
        )

    def _create_archive_fixture(self, run_id: str) -> Path:
        """Create one semantically complete schema-v2 archive candidate."""
        archive = self.archive_root / run_id
        execution_nonce = f"nonce-{run_id}-1234567890"
        run_started_at = "2026-07-14T00:00:00Z"
        run_finished_at = "2026-07-14T00:00:30Z"
        self._write_json(
            archive / "RUN.json",
            {
                "executionNonce": execution_nonce,
                "finishedAt": run_finished_at,
                "runId": run_id,
                "schemaVersion": 2,
                "sourceBaseline": "a" * 40,
                "startedAt": run_started_at,
                "status": "READY",
            },
        )

        documentation = {
            "docs/architecture/system.md": "# Architecture\n\nAccepted system boundary.\n",
            "docs/functional/workflow.md": "# Workflow\n\nAccepted actor workflow.\n",
            "docs/high-level/application.md": "# Application subsystem\n\nAccepted grouping.\n",
            "docs/modules/core.md": "# Core module\n\nAccepted runtime responsibility.\n",
            "docs/wiki/index.md": "# Wiki\n\nComplete documentation navigation.\n",
        }
        configuration = {
            "AGENTS.md": "# Root guidance\n",
            "PROJECT.yaml": "project: fixture\n",
            "src/feature/AGENTS.md": "# Nested feature guidance\n",
        }
        seed_entries: list[dict[str, object]] = []
        for relative_path, content in documentation.items():
            archived_path = archive / "documentation" / relative_path
            self._write(archived_path, content)
            seed_entries.append(
                {
                    "path": relative_path,
                    "phase": "wiki-first" if relative_path.startswith("docs/wiki/") else "linked-docs-and-config",
                    "sha256": self._sha256(archived_path),
                    "size": archived_path.stat().st_size,
                }
            )
        for relative_path, content in configuration.items():
            archived_path = archive / "configuration" / relative_path
            self._write(archived_path, content)
            seed_entries.append(
                {
                    "path": relative_path,
                    "phase": "linked-docs-and-config",
                    "sha256": self._sha256(archived_path),
                    "size": archived_path.stat().st_size,
                }
            )
        self._write_json(
            archive / "seed" / "seed-manifest.json",
            {
                "files": seed_entries,
                "runId": run_id,
                "schemaVersion": 1,
                "sourceBaseline": "a" * 40,
                "validation": {"status": "PASS"},
            },
        )
        self._write(
            archive / "reviews" / (
                "reconstruction-readiness."
                "review-checklist-reconstruction-readiness.md"
            ),
            "# Reconstruction readiness review\n\nStatus: PASS\n\nEvidence: complete fixture evidence.\n",
        )
        self._write(archive / "reconstruction" / "README.md", "# Reconstructed project\n")

        evidence_root = archive / "execution" / "evidence"
        native_evidence = evidence_root / "native-build.json"
        raw_report = evidence_root / "cypress-raw.json"
        observation = evidence_root / "cypress-observation.json"
        parity_evidence = evidence_root / "parity-case.json"
        native_command = "fixture native verification"
        cypress_command = "fixture cypress verification"
        native_command_digest = hashlib.sha256(native_command.encode("utf-8")).hexdigest()
        cypress_command_digest = hashlib.sha256(cypress_command.encode("utf-8")).hexdigest()
        native_artifact_digest = "2" * 64
        native_target_digest = "4" * 64
        native_process_identity = f"process-{run_id}"
        report_artifact_digest = "5" * 64
        report_target_digest = "7" * 64
        report_process_identity = f"cypress-process-{run_id}"
        self._write_json(
            native_evidence,
            {
                "artifactDigest": native_artifact_digest,
                "commandSha256": native_command_digest,
                "executionNonce": execution_nonce,
                "processIdentity": native_process_identity,
                "runId": run_id,
                "status": "PASS",
                "targetDigest": native_target_digest,
            },
        )
        self._write_json(raw_report, {"executionNonce": execution_nonce, "runId": run_id, "tests": 1})
        self._write_json(
            observation,
            {
                "artifactDigest": report_artifact_digest,
                "caseIds": ["CASE-001"],
                "commandSha256": cypress_command_digest,
                "executionNonce": execution_nonce,
                "processIdentity": report_process_identity,
                "rawReportSha256": self._sha256(raw_report),
                "runId": run_id,
                "targetDigest": report_target_digest,
            },
        )
        self._write_json(parity_evidence, {"caseId": "CASE-001", "runId": run_id, "status": "PASS"})

        cases = {
            "cases": [
                {
                    "comparisonPolicy": "exact normalized result",
                    "id": "CASE-001",
                    "inputs": ["synthetic fixture"],
                    "mandatoryExecutionStrength": "NATIVE",
                    "originalCommand": "fixture original command",
                    "owner": "observable fixture workflow",
                    "preconditions": ["fixture server is running"],
                    "reconstructionCommand": "fixture reconstruction command",
                    "requiredEvidence": ["raw Cypress report", "normalized observation"],
                    "requiredNativeProofId": "native-build",
                    "requiredProbeKind": "cypress-report",
                    "requiredReportKind": "cypress",
                }
            ],
            "requiredCaseCount": 1,
            "runId": run_id,
            "schemaVersion": 2,
            "status": "SEALED",
        }
        self._write_json(archive / "parity" / "cases.json", cases)
        self._write_json(
            archive / "oracle" / "original-baseline.json",
            {
                "artifactDigest": "1" * 64,
                "runId": run_id,
                "schemaVersion": 2,
                "status": "CAPTURED",
            },
        )
        self._write_json(
            archive / "parity" / "evaluator.json",
            {"name": "fixture evaluator", "schemaVersion": 1},
        )
        self._write_json(
            archive / "parity" / "contract.json",
            {"requiredCaseCount": 1, "schemaVersion": 1},
        )
        self._write_json(
            archive / "parity" / "probe-inventory.json",
            {"probeKinds": ["cypress-report"], "schemaVersion": 1},
        )
        binding_paths = {
            "caseCatalog": "parity/cases.json",
            "contract": "parity/contract.json",
            "evaluator": "parity/evaluator.json",
            "oracle": "oracle/original-baseline.json",
            "probeInventory": "parity/probe-inventory.json",
        }
        bindings = {
            name: {"path": path, "sha256": self._sha256(archive / path)}
            for name, path in binding_paths.items()
        }
        sealed_digest = self._binding_digest(
            *(f"{name}:{bindings[name]['sha256']}" for name in sorted(bindings))
        )
        self._write_json(
            archive / "parity" / "evaluator-manifest.json",
            {
                "bindings": bindings,
                "caseCount": 1,
                "executionNonce": execution_nonce,
                "requiredNativeProofIds": ["native-build"],
                "requiredReportKinds": ["cypress"],
                "runId": run_id,
                "schemaVersion": 2,
                "sealedDigest": sealed_digest,
                "status": "SEALED",
            },
        )

        native_digest = self._sha256(native_evidence)
        raw_digest = self._sha256(raw_report)
        observation_digest = self._sha256(observation)
        provenance = {
            "executionNonce": execution_nonce,
            "nativeProofs": [
                {
                    "artifactDigest": native_artifact_digest,
                    "commandId": "native-build-command",
                    "commandSha256": native_command_digest,
                    "evidence": "execution/evidence/native-build.json",
                    "evidenceSha256": native_digest,
                    "executionNonce": execution_nonce,
                    "finishedAt": "2026-07-14T00:00:20Z",
                    "id": "native-build",
                    "processIdentity": native_process_identity,
                    "proofBindingSha256": self._binding_digest(
                        run_id,
                        execution_nonce,
                        "native",
                        "native-build",
                        native_digest,
                    ),
                    "runId": run_id,
                    "startedAt": "2026-07-14T00:00:10Z",
                    "status": "PASS",
                    "targetDigest": native_target_digest,
                    "targetIdentity": f"target-{run_id}",
                }
            ],
            "reportProofs": [
                {
                    "artifactDigest": report_artifact_digest,
                    "commandId": "cypress-command",
                    "commandSha256": cypress_command_digest,
                    "executionNonce": execution_nonce,
                    "finishedAt": "2026-07-14T00:00:25Z",
                    "kind": "cypress",
                    "observation": "execution/evidence/cypress-observation.json",
                    "observationSha256": observation_digest,
                    "processIdentity": report_process_identity,
                    "proofBindingSha256": self._binding_digest(
                        run_id,
                        execution_nonce,
                        "report",
                        "cypress",
                        raw_digest,
                        observation_digest,
                    ),
                    "rawReport": "execution/evidence/cypress-raw.json",
                    "rawReportSha256": raw_digest,
                    "reporter": {"name": "cypress-json", "version": "1.0"},
                    "runId": run_id,
                    "startedAt": "2026-07-14T00:00:15Z",
                    "status": "PASS",
                    "targetDigest": report_target_digest,
                    "targetIdentity": f"browser-target-{run_id}",
                }
            ],
            "runId": run_id,
            "schemaVersion": 2,
            "status": "PASS",
        }
        self._write_json(archive / "execution" / "provenance.json", provenance)

        parity_digest = self._sha256(parity_evidence)
        self._write_json(
            archive / "parity" / "reconciliation.json",
            {
                "counts": {"attempted": 1, "failed": 0, "notRun": 0, "passed": 1, "required": 1},
                "evaluatorDigest": sealed_digest,
                "results": [
                    {
                        "caseId": "CASE-001",
                        "evidence": "execution/evidence/parity-case.json",
                        "evidenceSha256": parity_digest,
                        "probeKind": "cypress-report",
                        "status": "PASS",
                    }
                ],
                "runId": run_id,
                "schemaVersion": 2,
                "status": "PASS",
            },
        )

        isolation_environments = []
        for role in ("builder", "verifier"):
            probes = []
            for channel in sorted(self.helper._REQUIRED_ISOLATION_CHANNELS):
                probe_evidence = evidence_root / f"{role}-{channel}.json"
                self._write_json(
                    probe_evidence,
                    {"channel": channel, "role": role, "runId": run_id, "status": "DENIED"},
                )
                probe_digest = self._sha256(probe_evidence)
                evidence_path = probe_evidence.relative_to(archive).as_posix()
                probes.append(
                    {
                        "channel": channel,
                        "readers": [
                            {
                                "attemptedByteRead": True,
                                "evidence": evidence_path,
                                "evidenceSha256": probe_digest,
                                "name": "python-open",
                                "status": "DENIED",
                            },
                            {
                                "attemptedByteRead": True,
                                "evidence": evidence_path,
                                "evidenceSha256": probe_digest,
                                "name": "posix-head",
                                "status": "DENIED",
                            },
                        ],
                        "status": "DENIED",
                    }
                )
            isolation_environments.append(
                {
                    "deniedAccessProbes": probes,
                    "environmentSha256": ("8" if role == "builder" else "9") * 64,
                    "mountInventory": [{"mode": "read-only", "target": "/work"}],
                    "originalSourceMounted": False,
                    "role": role,
                    "sandboxIdentity": f"{role}-sandbox-{run_id}",
                    "status": "PASS",
                }
            )
        self._write_json(
            archive / "contamination" / "ledger.json",
            {
                "environments": isolation_environments,
                "findings": [],
                "runId": run_id,
                "schemaVersion": 2,
                "status": "PASS",
                "unresolvedContaminationFindings": 0,
            },
        )

        self._write_json(
            archive / "reset" / "source-baseline.json",
            {
                "inventorySha256": "a" * 64,
                "runId": run_id,
                "schemaVersion": 2,
                "status": "PASS",
            },
        )
        git_snapshot = {
            "gitMetadataSha256": "b" * 64,
            "head": "a" * 40,
            "statusSha256": "c" * 64,
            "tree": "d" * 40,
        }
        self._write_json(
            archive / "reset" / "git-reconciliation.json",
            {
                "claimLifecycle": {
                    "acquired": True,
                    "registryAfterSha256": "d" * 64,
                    "registryBeforeSha256": "e" * 64,
                    "released": True,
                    "status": "PASS",
                },
                "runId": run_id,
                "schemaVersion": 2,
                "stages": [
                    {
                        "after": git_snapshot,
                        "before": git_snapshot,
                        "changes": [],
                        "commandId": "reconstruction-generator",
                        "id": "generator",
                        "unexpectedChanges": [],
                    }
                ],
                "status": "PASS",
                "transientChanges": [
                    {"path": ".git/agent-claims.json", "resolution": "RELEASED"}
                ],
            },
        )
        self._write_json(
            archive / "generators" / "delta-ledger.json",
            {
                "rows": [{"generatorId": "fixture", "path": "README.md", "status": "PASS"}],
                "runId": run_id,
                "schemaVersion": 2,
                "status": "PASS",
            },
        )
        self._write(
            archive / "execution" / "commands.jsonl",
            "".join(
                json.dumps(record, sort_keys=True) + "\n"
                for record in (
                    {
                        "command": native_command,
                        "commandSha256": native_command_digest,
                        "executionNonce": execution_nonce,
                        "id": "native-build-command",
                        "runId": run_id,
                    },
                    {
                        "command": cypress_command,
                        "commandSha256": cypress_command_digest,
                        "executionNonce": execution_nonce,
                        "id": "cypress-command",
                        "runId": run_id,
                    },
                )
            )
        )
        self._write_json(
            archive / "execution" / "results.json",
            {
                "activities": [{"id": "native-build", "status": "PASS"}],
                "runId": run_id,
                "schemaVersion": 2,
                "status": "PASS",
            },
        )
        self._write_json(
            archive / "metrics" / "usage.json",
            {
                "activities": [
                    {
                        "costStatus": "UNAVAILABLE",
                        "elapsedSeconds": 10.0,
                        "id": "native-build",
                        "tokenStatus": "UNAVAILABLE",
                    }
                ],
                "runId": run_id,
                "schemaVersion": 2,
                "status": "COMPLETE",
            },
        )
        return archive

    def _create_legacy_archive_fixture(self, run_id: str) -> Path:
        """Create and seal the minimal schema-v1 shape retained for read compatibility."""
        archive = self.archive_root / run_id
        required_files = {
            "RUN.json": json.dumps({"runId": run_id}) + "\n",
            "reset/source-baseline.json": "{}\n",
            "configuration/PROJECT.yaml": "project: legacy\n",
            "configuration/AGENTS.md": "# Legacy guidance\n",
            "documentation/docs/wiki/index.md": "# Legacy wiki\n",
            "reviews/reconstruction-readiness.review-checklist-reconstruction-readiness.md": "# Review\n",
            "seed/seed-manifest.json": "{}\n",
            "oracle/original-baseline.json": "{}\n",
            "reconstruction/README.md": "# Legacy reconstruction\n",
            "parity/cases.json": "[]\n",
            "parity/reconciliation.json": "[]\n",
            "generators/delta-ledger.json": "[]\n",
            "contamination/ledger.json": "[]\n",
            "execution/commands.jsonl": "{}\n",
            "execution/results.json": "{}\n",
            "metrics/usage.json": "{}\n",
        }
        for relative_path, content in required_files.items():
            self._write(archive / relative_path, content)
        entries = []
        for path in sorted(path for path in archive.rglob("*") if path.is_file()):
            entries.append(
                {
                    "path": path.relative_to(archive).as_posix(),
                    "sha256": self._sha256(path),
                    "size": path.stat().st_size,
                }
            )
        self._write_json(
            archive / "archive-manifest.json",
            {
                "completedAt": "2026-07-14T00:00:00Z",
                "files": entries,
                "requiredDirectories": ["documentation/docs/wiki", "reconstruction"],
                "requiredFiles": list(self.helper._REQUIRED_ARCHIVE_FILES),
                "runId": run_id,
                "schemaVersion": 1,
                "status": "VALID",
            },
        )
        return archive

    def _convert_to_failed_not_run_fixture(self, archive: Path) -> None:
        """Convert a complete fixture into an honest early failed schema-v2 attempt."""
        run_id = archive.name
        run_path = archive / "RUN.json"
        run_data = json.loads(run_path.read_text(encoding="utf-8"))
        run_data["status"] = "FAILED"
        self._write_json(run_path, run_data)
        execution_nonce = run_data["executionNonce"]
        failure_path = archive / "execution" / "evidence" / "early-failure.json"
        self._write_json(
            failure_path,
            {
                "code": "DOCUMENTATION_GATE_FAILED",
                "runId": run_id,
                "status": "FAIL",
            },
        )
        failure_reference = {
            "failureEvidence": failure_path.relative_to(archive).as_posix(),
            "failureEvidenceSha256": self._sha256(failure_path),
            "unmetGate": "Pass 1 documentation acceptance",
        }
        documentation_root = archive / "documentation" / "docs"
        shutil.rmtree(documentation_root)
        for relative_directory in self.helper._REQUIRED_V2_DOCUMENTATION_DIRECTORIES:
            self._write_json(
                archive / relative_directory / "NOT_RUN.json",
                {
                    **failure_reference,
                    "runId": run_id,
                    "schemaVersion": 2,
                    "status": "NOT_RUN",
                },
            )
        shutil.rmtree(archive / "configuration")
        self._write(
            archive / "configuration" / "PROJECT.yaml",
            f"runId: {run_id}\nstatus: NOT_RUN\n",
        )
        self._write(
            archive / "configuration" / "AGENTS.md",
            f"# Project guidance\n\nRun: {run_id}\n\nStatus: NOT_RUN\n",
        )
        self._write_json(
            archive / "seed" / "seed-manifest.json",
            {
                **failure_reference,
                "runId": run_id,
                "schemaVersion": 1,
                "status": "NOT_RUN",
            },
        )
        self._write_json(
            archive / "parity" / "cases.json",
            {
                **failure_reference,
                "cases": [],
                "requiredCaseCount": 0,
                "runId": run_id,
                "schemaVersion": 2,
                "status": "NOT_RUN",
            },
        )
        evaluator_digest = self._binding_digest(
            run_id,
            execution_nonce,
            "evaluator-not-run",
        )
        self._write_json(
            archive / "parity" / "evaluator-manifest.json",
            {
                **failure_reference,
                "caseCount": 0,
                "executionNonce": execution_nonce,
                "requiredNativeProofIds": [],
                "requiredReportKinds": [],
                "runId": run_id,
                "schemaVersion": 2,
                "sealedDigest": evaluator_digest,
                "status": "NOT_RUN",
            },
        )
        self._write_json(
            archive / "execution" / "provenance.json",
            {
                **failure_reference,
                "executionNonce": execution_nonce,
                "nativeProofs": [],
                "reportProofs": [],
                "runId": run_id,
                "schemaVersion": 2,
                "status": "NOT_RUN",
            },
        )
        self._write_json(
            archive / "parity" / "reconciliation.json",
            {
                **failure_reference,
                "counts": {"attempted": 0, "failed": 0, "notRun": 0, "passed": 0, "required": 0},
                "evaluatorDigest": evaluator_digest,
                "results": [],
                "runId": run_id,
                "schemaVersion": 2,
                "status": "NOT_RUN",
            },
        )
        for relative_path in (
            "oracle/original-baseline.json",
            "generators/delta-ledger.json",
        ):
            self._write_json(
                archive / relative_path,
                {
                    **failure_reference,
                    "runId": run_id,
                    "schemaVersion": 2,
                    "status": "NOT_RUN",
                },
            )
        contamination_path = archive / "contamination" / "ledger.json"
        contamination = json.loads(contamination_path.read_text(encoding="utf-8"))
        contamination["environments"][1].update(
            {**failure_reference, "status": "NOT_RUN"}
        )
        self._write_json(contamination_path, contamination)
        results_path = archive / "execution" / "results.json"
        results = json.loads(results_path.read_text(encoding="utf-8"))
        results["status"] = "FAILED"
        results["activities"].append(
            {"id": "parity-verification", "status": "NOT_RUN"}
        )
        self._write_json(results_path, results)

    def _archive_directory_names(self) -> set[str]:
        """Return run-folder names without detached attestation sidecars."""
        return {path.name for path in self.archive_root.iterdir() if path.is_dir()}

    def test_initialize_copies_wiki_first_then_linked_docs_and_configuration(self) -> None:
        """A valid run records wiki-first copy order and complete seed hashes."""
        result = self._initialize()

        manifest_path = self.build_root / ".reconstruction" / "seed-manifest.json"
        run_metadata_path = self.build_root / ".reconstruction" / "run-metadata.json"
        contamination_path = (
            self.build_root / ".reconstruction" / "contamination-ledger.json"
        )
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        run_metadata = json.loads(run_metadata_path.read_text(encoding="utf-8"))
        contamination = json.loads(contamination_path.read_text(encoding="utf-8"))

        self.assertEqual("PASS", result["validationStatus"])
        self.assertEqual(
            ["wiki-first", "linked-docs-and-config"],
            [phase["name"] for phase in manifest["copyPhases"]],
        )
        copied_paths = {entry["path"] for entry in manifest["files"]}
        self.assertEqual(
            {
                "AGENTS.md",
                "PROJECT.yaml",
                "docs/architecture/system.md",
                "docs/functional/workflow.md",
                "docs/modules/unlinked.md",
                "docs/wiki/index.md",
                "src/feature/AGENTS.md",
            },
            copied_paths,
        )
        self.assertTrue(all(len(entry["sha256"]) == 64 for entry in manifest["files"]))
        self.assertEqual("SEED_VALIDATED", run_metadata["status"])
        self.assertEqual("PASS", contamination["status"])
        self.assertEqual(
            {
                "absolute-source-paths",
                "hard-links",
                "symbolic-links",
                "workstation-home-paths",
            },
            {check["name"] for check in contamination["checks"]},
        )
        self.assertNotIn(str(self.source), manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(
            "PASS",
            self.helper.validate_seed(self.build_root, exact=True)["status"],
        )

    def test_validate_seed_detects_post_copy_tampering(self) -> None:
        """Independent validation fails when a copied input changes after initialization."""
        self._initialize()
        self._write(
            self.build_root / "docs" / "functional" / "workflow.md",
            "# Workfl0w\n",
        )

        with self.assertRaisesRegex(
            self.helper.ReconstructionRunError,
            "hash mismatch",
        ):
            self.helper.validate_seed(self.build_root, exact=True)

    def test_initialize_rejects_an_existing_build_root(self) -> None:
        """Initialization never overlays an existing destination."""
        self.build_root.mkdir()

        with self.assertRaisesRegex(
            self.helper.ReconstructionRunError,
            "brand-new build root",
        ):
            self._initialize()

    def test_initialize_records_source_evidence_links_without_copying_source(self) -> None:
        """Relative source links remain path-ledger references and never become seed files."""
        self._write(
            self.source / "docs" / "wiki" / "index.md",
            "# Wiki\n\n[Application source](../../src/main.py)\n",
        )
        self._write(self.source / "src" / "main.py", "print('source')\n")

        self._initialize()

        manifest = json.loads(
            (
                self.build_root / ".reconstruction" / "seed-manifest.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(
            [
                {
                    "document": "docs/wiki/index.md",
                    "kind": "source-evidence",
                    "target": "src/main.py",
                }
            ],
            manifest["evidenceReferences"],
        )
        self.assertFalse((self.build_root / "src" / "main.py").exists())

    def test_initialize_rejects_an_unresolved_local_link(self) -> None:
        """A missing local target is neither a valid seed dependency nor source evidence."""
        self._write(
            self.source / "docs" / "wiki" / "index.md",
            "# Wiki\n\n[Missing](../missing.md)\n",
        )

        with self.assertRaisesRegex(
            self.helper.ReconstructionRunError,
            "Unresolved local documentation link",
        ):
            self._initialize()

    @unittest.skipUnless(hasattr(os, "symlink"), "symbolic links are unavailable")
    def test_initialize_rejects_symbolic_links(self) -> None:
        """No seed file may alias source content through a symbolic link."""
        target = self.source / "docs" / "functional" / "workflow.md"
        target.unlink()
        target.symlink_to(self.source / "PROJECT.yaml")

        with self.assertRaisesRegex(
            self.helper.ReconstructionRunError,
            "symbolic link",
        ):
            self._initialize()

    @unittest.skipUnless(hasattr(os, "link"), "hard links are unavailable")
    def test_initialize_rejects_hard_links(self) -> None:
        """No seed file may retain inode identity with another source path."""
        workflow = self.source / "docs" / "functional" / "workflow.md"
        linked_copy = self.source / "docs" / "functional" / "linked-copy.md"
        os.link(workflow, linked_copy)
        self._write(
            self.source / "docs" / "architecture" / "system.md",
            "# Architecture\n\n[Workflow](../functional/linked-copy.md)\n",
        )

        with self.assertRaisesRegex(
            self.helper.ReconstructionRunError,
            "hard link",
        ):
            self._initialize()

    def test_initialize_rejects_absolute_source_paths(self) -> None:
        """Portable seed text cannot disclose or depend on the original project path."""
        self._write(
            self.source / "docs" / "functional" / "workflow.md",
            f"# Workflow\n\nOriginal source: {self.source}/src/main.py\n",
        )

        with self.assertRaisesRegex(
            self.helper.ReconstructionRunError,
            "absolute source path",
        ):
            self._initialize()

    def test_initialize_rejects_unrelated_posix_workstation_paths(self) -> None:
        """Portable configuration cannot retain another checkout's user-home path."""
        self._write(
            self.source / "PROJECT.yaml",
            "project: fixture\nevidence: /Users/example/dev/other-repo/pom.xml\n",
        )

        with self.assertRaisesRegex(
            self.helper.ReconstructionRunError,
            "workstation-specific path",
        ):
            self._initialize()

    def test_initialize_rejects_windows_workstation_paths(self) -> None:
        """Windows user-home paths are as non-portable as POSIX user-home paths."""
        self._write(
            self.source / "PROJECT.yaml",
            "project: fixture\nevidence: C:\\Users\\example\\dev\\repo\\pom.xml\n",
        )

        with self.assertRaisesRegex(
            self.helper.ReconstructionRunError,
            "workstation-specific path",
        ):
            self._initialize()

    def test_initialize_rejects_linux_workstation_paths(self) -> None:
        """Common Linux checkout roots cannot leak from an unrelated workstation."""
        self._write(
            self.source / "PROJECT.yaml",
            "project: fixture\nevidence: /home/example/dev/other-repo/pom.xml\n",
        )

        with self.assertRaisesRegex(
            self.helper.ReconstructionRunError,
            "workstation-specific path",
        ):
            self._initialize()

    def test_initialize_allows_declared_runtime_absolute_paths(self) -> None:
        """Runtime routes and portable container paths are not workstation leakage."""
        self._write(
            self.source / "PROJECT.yaml",
            (
                "project: fixture\n"
                "api_route: /management/health\n"
                "container_root: /workspace\n"
                "generator_root: /home/jhipster/app\n"
                "portable_home: ${HOME}/.cache\n"
                "scanner_pattern: '/Users/|/home/|C:\\\\Users\\\\'\n"
            ),
        )

        self.assertEqual("PASS", self._initialize()["validationStatus"])

    def test_invalid_new_archive_never_triggers_retention_pruning(self) -> None:
        """An incomplete new archive leaves every existing run untouched."""
        for index in range(1, 4):
            archive = self._create_archive_fixture(f"run-00{index}")
            self.helper.seal_archive_and_prune(
                new_archive=archive,
                archive_root=self.archive_root,
                retain=10,
                completed_at=f"2026-07-14T00:0{index}:00Z",
            )
        invalid_archive = self._create_archive_fixture("run-004")
        (invalid_archive / "parity" / "reconciliation.json").unlink()

        with self.assertRaisesRegex(
            self.helper.ReconstructionRunError,
            "required archive entry",
        ):
            self.helper.seal_archive_and_prune(
                new_archive=invalid_archive,
                archive_root=self.archive_root,
                retain=3,
                completed_at="2026-07-14T00:04:00Z",
            )

        self.assertEqual(
            {"run-001", "run-002", "run-003", "run-004"},
            self._archive_directory_names(),
        )

    def test_schema_v1_archive_remains_readable_but_cannot_be_newly_sealed(self) -> None:
        """Legacy manifests remain verifiable while new sealing requires semantic evidence."""
        archive = self._create_legacy_archive_fixture("run-legacy")

        self.assertEqual(1, self.helper.validate_archive(archive)["schemaVersion"])
        (archive / "archive-manifest.json").unlink()
        with self.assertRaisesRegex(
            self.helper.ReconstructionRunError,
            "validation-only",
        ):
            self.helper.seal_archive_and_prune(
                new_archive=archive,
                archive_root=self.archive_root,
                retain=3,
            )

    def test_schema_v2_rejects_hollow_required_evidence(self) -> None:
        """A non-empty filename cannot disguise an empty machine-readable result."""
        archive = self._create_archive_fixture("run-hollow")
        self._write(archive / "metrics" / "usage.json", "{}\n")

        with self.assertRaisesRegex(
            self.helper.ReconstructionRunError,
            "non-empty JSON object",
        ):
            self.helper.seal_archive_and_prune(
                new_archive=archive,
                archive_root=self.archive_root,
                retain=3,
            )

    def test_schema_v2_seals_failed_attempt_with_bound_not_run_records(self) -> None:
        """An early failure remains archivable without fabricating unexecuted stages."""
        archive = self._create_archive_fixture("run-failed-not-run")
        self._convert_to_failed_not_run_fixture(archive)

        result = self.helper.seal_archive_and_prune(
            new_archive=archive,
            archive_root=self.archive_root,
            retain=3,
        )

        self.assertEqual("VALID", result["status"])
        self.assertEqual(2, self.helper.validate_archive(archive)["schemaVersion"])

    def test_schema_v2_rejects_missing_documentation_hierarchy(self) -> None:
        """A wiki cannot substitute for a missing module or subsystem documentation level."""
        archive = self._create_archive_fixture("run-missing-modules")
        (archive / "documentation" / "docs" / "modules" / "core.md").unlink()

        with self.assertRaisesRegex(
            self.helper.ReconstructionRunError,
            "documentation hierarchy|required archive entry",
        ):
            self.helper.seal_archive_and_prune(
                new_archive=archive,
                archive_root=self.archive_root,
                retain=3,
            )

    def test_schema_v2_rejects_missing_nested_guidance(self) -> None:
        """Nested AGENTS guidance in the seed must appear unchanged in the archive."""
        archive = self._create_archive_fixture("run-missing-guidance")
        (archive / "configuration" / "src" / "feature" / "AGENTS.md").unlink()

        with self.assertRaisesRegex(
            self.helper.ReconstructionRunError,
            "nested seed guidance",
        ):
            self.helper.seal_archive_and_prune(
                new_archive=archive,
                archive_root=self.archive_root,
                retain=3,
            )

    def test_schema_v2_rejects_missing_cypress_raw_report_provenance(self) -> None:
        """A normalized Cypress observation is insufficient without its raw report binding."""
        archive = self._create_archive_fixture("run-missing-cypress-provenance")
        provenance_path = archive / "execution" / "provenance.json"
        provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
        del provenance["reportProofs"][0]["rawReport"]
        self._write_json(provenance_path, provenance)

        with self.assertRaisesRegex(
            self.helper.ReconstructionRunError,
            "rawReport must be a non-empty string",
        ):
            self.helper.seal_archive_and_prune(
                new_archive=archive,
                archive_root=self.archive_root,
                retain=3,
            )

    def test_schema_v2_rejects_forged_command_provenance(self) -> None:
        """A proof envelope cannot substitute a command digest absent from commands.jsonl."""
        archive = self._create_archive_fixture("run-forged-command")
        evidence_path = archive / "execution" / "evidence" / "native-build.json"
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        evidence["commandSha256"] = "0" * 64
        self._write_json(evidence_path, evidence)
        provenance_path = archive / "execution" / "provenance.json"
        provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
        native_proof = provenance["nativeProofs"][0]
        evidence_digest = self._sha256(evidence_path)
        native_proof["commandSha256"] = "0" * 64
        native_proof["evidenceSha256"] = evidence_digest
        native_proof["proofBindingSha256"] = self._binding_digest(
            archive.name,
            f"nonce-{archive.name}-1234567890",
            "native",
            "native-build",
            evidence_digest,
        )
        self._write_json(provenance_path, provenance)

        with self.assertRaisesRegex(
            self.helper.ReconstructionRunError,
            "differs from commands.jsonl",
        ):
            self.helper.seal_archive_and_prune(
                new_archive=archive,
                archive_root=self.archive_root,
                retain=3,
            )

    def test_schema_v2_rejects_missing_git_claim_reconciliation(self) -> None:
        """Git proof must include the transient claim registry and released lifecycle."""
        archive = self._create_archive_fixture("run-missing-git-reconciliation")
        reconciliation_path = archive / "reset" / "git-reconciliation.json"
        reconciliation = json.loads(reconciliation_path.read_text(encoding="utf-8"))
        reconciliation["transientChanges"] = []
        self._write_json(reconciliation_path, reconciliation)

        with self.assertRaisesRegex(
            self.helper.ReconstructionRunError,
            "transientChanges must be a non-empty list",
        ):
            self.helper.seal_archive_and_prune(
                new_archive=archive,
                archive_root=self.archive_root,
                retain=3,
            )

    def test_schema_v2_rejects_incomplete_isolation_probes(self) -> None:
        """Builder and verifier isolation must cover every channel with two byte readers."""
        archive = self._create_archive_fixture("run-incomplete-isolation")
        ledger_path = archive / "contamination" / "ledger.json"
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        ledger["environments"][0]["deniedAccessProbes"][0]["readers"].pop()
        self._write_json(ledger_path, ledger)

        with self.assertRaisesRegex(
            self.helper.ReconstructionRunError,
            "two independent readers",
        ):
            self.helper.seal_archive_and_prune(
                new_archive=archive,
                archive_root=self.archive_root,
                retain=3,
            )

    def test_schema_v2_rejects_duplicate_manifest_paths(self) -> None:
        """Exact archive validation never collapses duplicate paths into a dictionary."""
        archive = self._create_archive_fixture("run-duplicate-manifest")
        self.helper.seal_archive_and_prune(
            new_archive=archive,
            archive_root=self.archive_root,
            retain=3,
        )
        manifest_path = archive / "archive-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["files"].append(dict(manifest["files"][0]))
        self._write_json(manifest_path, manifest)

        with self.assertRaisesRegex(
            self.helper.ReconstructionRunError,
            "duplicate path",
        ):
            self.helper.validate_archive(archive)

    def test_schema_v2_rejects_report_mutation_after_sealing(self) -> None:
        """Raw report bytes cannot change after provenance and archive hashes are sealed."""
        archive = self._create_archive_fixture("run-report-mutation")
        self.helper.seal_archive_and_prune(
            new_archive=archive,
            archive_root=self.archive_root,
            retain=3,
        )
        self._write_json(
            archive / "execution" / "evidence" / "cypress-raw.json",
            {"tests": 999},
        )

        with self.assertRaisesRegex(
            self.helper.ReconstructionRunError,
            "evidence hash mismatch",
        ):
            self.helper.validate_archive(archive)

    def test_schema_v2_rejects_detached_attestation_mutation(self) -> None:
        """Changing a detached attestation invalidates the otherwise unchanged archive."""
        archive = self._create_archive_fixture("run-attestation-mutation")
        result = self.helper.seal_archive_and_prune(
            new_archive=archive,
            archive_root=self.archive_root,
            retain=3,
        )
        attestation_path = self.archive_root / result["detachedAttestation"]
        attestation = json.loads(attestation_path.read_text(encoding="utf-8"))
        attestation["manifestSha256"] = "0" * 64
        self._write_json(attestation_path, attestation)

        with self.assertRaisesRegex(
            self.helper.ReconstructionRunError,
            "does not match the manifest",
        ):
            self.helper.validate_archive(archive)

    def test_compare_archive_uses_independently_stored_attestation(self) -> None:
        """Archive transfer comparison requires an exact independently stored sidecar."""
        archive = self._create_archive_fixture("run-compare-attestation")
        result = self.helper.seal_archive_and_prune(
            new_archive=archive,
            archive_root=self.archive_root,
            retain=3,
        )
        expected_attestation = self.workspace / "independent-attestation.json"
        expected_attestation.write_bytes(
            (self.archive_root / result["detachedAttestation"]).read_bytes()
        )

        comparison = self.helper.compare_archive_attestation(
            archive,
            expected_attestation,
        )

        self.assertEqual("MATCH", comparison["status"])

    def test_archive_validation_and_comparison_cli_paths_succeed(self) -> None:
        """Portable CLI routes expose the same schema and attestation validation."""
        archive = self._create_archive_fixture("run-cli-archive")
        result = self.helper.seal_archive_and_prune(
            new_archive=archive,
            archive_root=self.archive_root,
            retain=3,
        )
        expected_attestation = self.workspace / "cli-attestation.json"
        expected_attestation.write_bytes(
            (self.archive_root / result["detachedAttestation"]).read_bytes()
        )

        with contextlib.redirect_stdout(io.StringIO()):
            validate_status = self.helper.main(
                ["validate-archive", "--archive", str(archive)]
            )
            compare_status = self.helper.main(
                [
                    "compare-archive",
                    "--archive",
                    str(archive),
                    "--expected-attestation",
                    str(expected_attestation),
                ]
            )

        self.assertEqual(0, validate_status)
        self.assertEqual(0, compare_status)

    def test_schema_v2_rejects_reused_native_or_report_evidence(self) -> None:
        """A later archive cannot relabel proof bytes retained from an earlier run."""
        first = self._create_archive_fixture("run-proof-001")
        self.helper.seal_archive_and_prune(
            new_archive=first,
            archive_root=self.archive_root,
            retain=10,
        )
        second = self._create_archive_fixture("run-proof-002")
        first_native = first / "execution" / "evidence" / "native-build.json"
        second_native = second / "execution" / "evidence" / "native-build.json"
        second_native.write_bytes(first_native.read_bytes())
        provenance_path = second / "execution" / "provenance.json"
        provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
        native_proof = provenance["nativeProofs"][0]
        reused_digest = self._sha256(second_native)
        native_proof["evidenceSha256"] = reused_digest
        native_proof["proofBindingSha256"] = self._binding_digest(
            "run-proof-002",
            "nonce-run-proof-002-1234567890",
            "native",
            "native-build",
            reused_digest,
        )
        self._write_json(provenance_path, provenance)

        with self.assertRaisesRegex(
            self.helper.ReconstructionRunError,
            "belongs to another run|reuse native or report evidence",
        ):
            self.helper.seal_archive_and_prune(
                new_archive=second,
                archive_root=self.archive_root,
                retain=10,
            )

    def test_valid_new_archive_is_sealed_before_newest_three_are_retained(self) -> None:
        """A verified exact-content manifest gates deletion of the oldest valid run."""
        for index in range(1, 5):
            archive = self._create_archive_fixture(f"run-00{index}")
            result = self.helper.seal_archive_and_prune(
                new_archive=archive,
                archive_root=self.archive_root,
                retain=10 if index < 4 else 3,
                completed_at=f"2026-07-14T00:0{index}:00Z",
            )

        self.assertEqual(["run-001"], result["prunedArchives"])
        self.assertEqual(
            {"run-002", "run-003", "run-004"},
            self._archive_directory_names(),
        )
        archive_manifest = json.loads(
            (
                self.archive_root / "run-004" / "archive-manifest.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual("VALID", archive_manifest["status"])
        self.assertEqual(2, archive_manifest["schemaVersion"])
        self.assertTrue(archive_manifest["files"])
        self.assertTrue(
            (self.archive_root / "run-004.attestation.json").is_file()
        )
        self.assertFalse(
            (self.archive_root / "run-001.attestation.json").exists()
        )

    def test_unsealed_existing_run_blocks_retention_pruning(self) -> None:
        """Retention never ignores an incomplete sibling run in the archive root."""
        for index in range(1, 4):
            archive = self._create_archive_fixture(f"run-00{index}")
            self.helper.seal_archive_and_prune(
                new_archive=archive,
                archive_root=self.archive_root,
                retain=10,
                completed_at=f"2026-07-14T00:0{index}:00Z",
            )
        self._write(self.archive_root / "run-unsealed" / "failure.txt", "partial\n")
        new_archive = self._create_archive_fixture("run-004")

        with self.assertRaisesRegex(
            self.helper.ReconstructionRunError,
            "unsealed run",
        ):
            self.helper.seal_archive_and_prune(
                new_archive=new_archive,
                archive_root=self.archive_root,
                retain=3,
                completed_at="2026-07-14T00:04:00Z",
            )

        self.assertTrue((self.archive_root / "run-001").is_dir())
        self.assertFalse((new_archive / "archive-manifest.json").exists())


if __name__ == "__main__":
    unittest.main()
