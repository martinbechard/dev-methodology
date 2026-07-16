# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Modified with AI assistance.
# Summary: Verifies receipt-backed agent and skill evaluation evidence contracts.

from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import os
import sys
import threading
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from types import ModuleType
from unittest import mock

import yaml

from scripts import agent_skill_judge_contract as judge_contract


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "run-agent-skill-evals.py"


def load_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location("run_agent_skill_evals", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load evaluation runner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _calibration_samples() -> list[dict[str, object]]:
    classes = (
        "clear-pass",
        "clear-fail",
        "boundary",
        "incomplete-plausible",
        "adversarially-polished",
    )
    samples: list[dict[str, object]] = []
    critical_failures = {1, 3, 4, 6, 8}
    for index in range(25):
        sample_class = classes[index % len(classes)]
        human_label = "pass" if sample_class in {"clear-pass", "boundary"} else "fail"
        human_score = 4 if sample_class == "clear-pass" else 2 if sample_class == "boundary" else 0
        sample: dict[str, object] = {
            "id": f"sample-{index}",
            "sampleClass": sample_class,
            "humanLabel": human_label,
            "modelLabel": human_label,
            "humanScore": human_score,
            "modelScore": human_score,
            "criticalDefect": index in critical_failures,
        }
        if sample_class == "boundary":
            sample["humanJudgments"] = [
                {"judgeId": "human-a", "label": human_label, "score": human_score},
                {"judgeId": "human-b", "label": human_label, "score": human_score},
            ]
            sample["adjudication"] = {
                "adjudicatorId": "human-c",
                "label": human_label,
                "score": human_score,
            }
        samples.append(sample)
    return samples


class AgentSkillEvidenceTests(unittest.TestCase):
    """Verify compatibility and receipt trust boundaries."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_module()
        cls.case = cls.module.load_cases()["typescript-order-pricing"]

    def receipt(self) -> dict[str, object]:
        return {
            "schema": "dev-methodology-eval-evidence",
            "version": 1,
            "case": "typescript-order-pricing",
            "verdict": "verified",
            "captureProvenance": {
                "kind": "human-attested-harness-export",
                "reference": "attestation.json#capture",
            },
            "agent": {
                "id": "dev-coder",
                "harness": "codex",
                "model": "test-model",
                "invocationEvidence": "events.jsonl#invocation",
            },
            "skills": [
                {
                    "id": skill,
                    "contentDigest": digest(ROOT / "skills" / skill / "SKILL.md"),
                    "readEvidence": [{"type": "tool-call", "reference": f"events.jsonl#read-{skill}"}],
                }
                for skill in self.case["requiredSkills"]
            ],
            "behaviorAssertions": [
                {"id": assertion, "verdict": "passed", "evidence": f"assertions.json#{assertion}"}
                for assertion in self.case["requiredEvidence"]
            ],
            "commands": [
                {"command": "npm test", "exitCode": 0, "expectation": "success", "evidence": "commands.log#test"}
            ],
            "independentVerifier": {"kind": "deterministic", "reference": "verifier.json#verdict"},
        }

    def validate(self, receipt: dict[str, object]) -> list[str]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "evidence.yaml"
            events = [{
                "id": "invocation",
                "type": "invocation",
                "agent": receipt["agent"]["id"],
                "harness": receipt["agent"]["harness"],
                "model": receipt["agent"]["model"],
            }]
            events.extend({
                "id": f"read-{skill}",
                "type": "tool-call",
                "skill": skill,
                "contentDigest": digest(ROOT / "skills" / skill / "SKILL.md"),
            } for skill in self.case["requiredSkills"])
            references = ["test", "verdict"]
            references.extend(str(assertion) for assertion in self.case["requiredEvidence"])
            (root / "events.jsonl").write_text("\n".join(json.dumps(event) for event in events) + "\n", encoding="utf-8")
            (root / "assertions.json").write_text("\n".join(references) + "\n", encoding="utf-8")
            (root / "commands.log").write_text("test\n", encoding="utf-8")
            (root / "verifier.json").write_text("verdict\n", encoding="utf-8")
            (root / "attestation.json").write_text("capture\n", encoding="utf-8")
            path.write_text(yaml.safe_dump(receipt), encoding="utf-8")
            return self.module.validate_evidence(self.case, path)

    def test_complete_receipt_is_accepted(self) -> None:
        self.assertEqual([], self.validate(self.receipt()))

    def test_declared_agent_is_not_enough_without_matching_identity(self) -> None:
        receipt = self.receipt()
        receipt["agent"]["id"] = "dev-code-reviewer"
        self.assertIn("evidence agent id does not match a required agent", self.validate(receipt))

    def test_skill_claim_is_not_enough_without_tool_call_evidence(self) -> None:
        receipt = self.receipt()
        receipt["skills"][0]["readEvidence"] = []
        errors = self.validate(receipt)
        self.assertTrue(any("missing skill read tool evidence" in error for error in errors))

    def test_skill_digest_must_match_the_loaded_source(self) -> None:
        receipt = self.receipt()
        receipt["skills"][0]["contentDigest"] = "wrong"
        errors = self.validate(receipt)
        self.assertTrue(any("skill digest mismatch" in error for error in errors))

    def test_reference_claim_is_not_enough_without_a_captured_artifact(self) -> None:
        receipt = self.receipt()
        receipt["agent"]["invocationEvidence"] = "missing.jsonl#invocation"
        errors = self.validate(receipt)
        self.assertTrue(any("reference target is missing" in error for error in errors))

    def test_escaped_reference_is_rejected_before_any_artifact_read(self) -> None:
        validation_module = sys.modules[self.module.validate_evidence.__module__]
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            receipt_root = base / "receipt"
            receipt_root.mkdir()
            outside = base / "outside.jsonl"
            outside.write_text(
                json.dumps({"id": "invocation", "type": "invocation"}) + "\n",
                encoding="utf-8",
            )
            evidence_path = receipt_root / "evidence.yaml"
            evidence_path.write_text("receipt\n", encoding="utf-8")
            reference = "../outside.jsonl#invocation"
            errors: list[str] = []
            self.module.validate_reference(reference, "test", evidence_path, errors)
            events = validation_module._events_for_reference(reference, evidence_path)
            all_events = validation_module._all_events_for_reference(reference, evidence_path)
        self.assertTrue(any("escapes" in error for error in errors))
        self.assertIsNone(events)
        self.assertEqual([], all_events)

    def test_plain_marker_is_not_accepted_as_a_harness_event(self) -> None:
        receipt = self.receipt()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "events.jsonl").write_text("invocation\n", encoding="utf-8")
            path = root / "evidence.yaml"
            path.write_text(yaml.safe_dump(receipt), encoding="utf-8")
            errors = self.module.validate_evidence(self.case, path)
        self.assertTrue(any("JSON harness event" in error for error in errors))

    def test_unattested_capture_is_not_accepted(self) -> None:
        receipt = self.receipt()
        receipt.pop("captureProvenance")
        errors = self.validate(receipt)
        self.assertIn("evidence captureProvenance must be a mapping", errors)

    def test_every_behavior_assertion_needs_independent_evidence(self) -> None:
        receipt = self.receipt()
        receipt["behaviorAssertions"][0]["evidence"] = ""
        errors = self.validate(receipt)
        self.assertTrue(any("behavior assertion lacks passed evidence" in error for error in errors))

    def test_read_only_case_requires_unchanged_hash(self) -> None:
        case = self.module.load_cases()["typescript-code-review"]
        receipt = self.receipt()
        receipt["case"] = case["id"]
        receipt["agent"]["id"] = "dev-code-reviewer"
        receipt["skills"] = [
            {
                "id": skill,
                "contentDigest": digest(ROOT / "skills" / skill / "SKILL.md"),
                "readEvidence": [{"type": "tool-call", "reference": f"events.jsonl#read-{skill}"}],
            }
            for skill in case["requiredSkills"]
        ]
        receipt["behaviorAssertions"] = [
            {"id": assertion, "verdict": "passed", "evidence": f"assertions.json#{assertion}"}
            for assertion in case["requiredEvidence"]
        ]
        receipt["findings"] = [
            {"id": finding, "evidence": f"review.md#{finding}"}
            for finding in case["requiredFindings"]
        ]
        receipt["projectHashBefore"] = "before"
        receipt["projectHashAfter"] = "after"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "evidence.yaml"
            path.write_text(yaml.safe_dump(receipt), encoding="utf-8")
            errors = self.module.validate_evidence(case, path)
        self.assertIn("read-only evaluation changed the project hash", errors)

    def test_forbidden_skill_read_is_detected_from_the_event_ledger(self) -> None:
        case = dict(self.case)
        case["forbiddenSkills"] = ["application-security"]
        receipt = self.receipt()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "evidence.yaml"
            events = [{
                "id": "invocation",
                "type": "invocation",
                "agent": receipt["agent"]["id"],
                "harness": receipt["agent"]["harness"],
                "model": receipt["agent"]["model"],
            }]
            events.extend({
                "id": f"read-{skill}",
                "type": "tool-call",
                "skill": skill,
                "contentDigest": digest(ROOT / "skills" / skill / "SKILL.md"),
            } for skill in self.case["requiredSkills"])
            events.append({
                "id": "read-forbidden",
                "type": "tool-call",
                "skill": "application-security",
                "contentDigest": digest(ROOT / "skills" / "application-security" / "SKILL.md"),
            })
            (root / "events.jsonl").write_text("\n".join(json.dumps(event) for event in events) + "\n", encoding="utf-8")
            (root / "assertions.json").write_text(
                "\n".join(str(assertion) for assertion in self.case["requiredEvidence"]) + "\n",
                encoding="utf-8",
            )
            (root / "commands.log").write_text("test\n", encoding="utf-8")
            (root / "verifier.json").write_text("verdict\n", encoding="utf-8")
            (root / "attestation.json").write_text("capture\n", encoding="utf-8")
            path.write_text(yaml.safe_dump(receipt), encoding="utf-8")
            errors = self.module.validate_evidence(case, path)
        self.assertIn("evidence observed forbidden skill read: application-security", errors)

    def test_only_codex_and_junie_harnesses_are_supported(self) -> None:
        receipt = self.receipt()
        receipt["agent"]["harness"] = "claude"
        errors = self.validate(receipt)
        self.assertIn("evidence agent.harness must be codex or junie", errors)

    def test_legacy_cases_remain_valid_and_commands_are_shell_free(self) -> None:
        cases = self.module.load_cases()
        for case in cases.values():
            self.assertEqual([], self.module.validate_case_definition(case))
            command = self.module.command_spec(case["verify"])
            self.assertGreater(len(command.argv), 0)
            self.assertFalse(command.uses_shell)


class PreparedWorkspaceTests(unittest.TestCase):
    """Verify content-addressed preparation and disposable workspace behavior."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_module()

    def test_fixture_key_changes_only_when_addressed_inputs_change(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory) / "fixture"
            fixture.mkdir()
            (fixture / "source.txt").write_text("first\n", encoding="utf-8")
            key = self.module.prepared_fixture_key(fixture, {"python": "3.11"})
            self.assertEqual(key, self.module.prepared_fixture_key(fixture, {"python": "3.11"}))
            self.assertNotEqual(key, self.module.prepared_fixture_key(fixture, {"python": "3.12"}))
            (fixture / "source.txt").write_text("second\n", encoding="utf-8")
            self.assertNotEqual(key, self.module.prepared_fixture_key(fixture, {"python": "3.11"}))

    def test_fixture_key_tracks_modes_empty_directories_and_command_environment_policy(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory) / "fixture"
            fixture.mkdir()
            source = fixture / "source.txt"
            source.write_text("source\n", encoding="utf-8")
            key = self.module.prepared_fixture_key(fixture, {"runtime": "1"})
            source.chmod(0o700)
            self.assertNotEqual(key, self.module.prepared_fixture_key(fixture, {"runtime": "1"}))
            mode_key = self.module.prepared_fixture_key(fixture, {"runtime": "1"})
            (fixture / "empty").mkdir()
            self.assertNotEqual(mode_key, self.module.prepared_fixture_key(fixture, {"runtime": "1"}))
            first = {"argv": ["prepare"], "hostEnvironmentAllowlist": ["PATH"]}
            second = {"argv": ["prepare"], "hostEnvironmentAllowlist": ["PATH", "LANG"]}
            self.assertNotEqual(
                self.module.prepared_fixture_key(fixture, {"runtime": "1"}, first),
                self.module.prepared_fixture_key(fixture, {"runtime": "1"}, second),
            )

    def test_fixture_key_excludes_transient_trees_but_includes_lockfiles(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory) / "fixture"
            fixture.mkdir()
            (fixture / "package-lock.json").write_text('{"lockfileVersion": 3}\n', encoding="utf-8")
            (fixture / "node_modules").mkdir()
            (fixture / "node_modules" / "transient.js").write_text("first\n", encoding="utf-8")
            (fixture / "dist").mkdir()
            (fixture / "dist" / "bundle.js").write_text("first\n", encoding="utf-8")
            key = self.module.prepared_fixture_key(fixture, {"node": "24"})
            (fixture / "node_modules" / "transient.js").write_text("second\n", encoding="utf-8")
            (fixture / "dist" / "bundle.js").write_text("second\n", encoding="utf-8")
            self.assertEqual(key, self.module.prepared_fixture_key(fixture, {"node": "24"}))
            (fixture / "package-lock.json").write_text('{"lockfileVersion": 4}\n', encoding="utf-8")
            self.assertNotEqual(key, self.module.prepared_fixture_key(fixture, {"node": "24"}))

    def test_fixture_key_prunes_transient_directories_before_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory) / "fixture"
            fixture.mkdir()
            (fixture / "source.txt").write_text("source\n", encoding="utf-8")
            (fixture / "node_modules").mkdir()
            (fixture / "node_modules" / "must-not-be-visited").write_text("sentinel\n", encoding="utf-8")
            with mock.patch.object(Path, "rglob", side_effect=AssertionError("unpruned traversal")):
                key = self.module.prepared_fixture_key(fixture, {"node": "24"})
        self.assertEqual(64, len(key))

    def test_fixture_key_includes_automatic_platform_identity(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory) / "fixture"
            fixture.mkdir()
            (fixture / "source.txt").write_text("source\n", encoding="utf-8")
            with mock.patch("platform.system", return_value="System-A"), mock.patch(
                "platform.release", return_value="Release-A",
            ), mock.patch("platform.machine", return_value="arch-a"):
                first = self.module.prepared_fixture_key(fixture, {"runtime": "1"})
            with mock.patch("platform.system", return_value="System-B"), mock.patch(
                "platform.release", return_value="Release-B",
            ), mock.patch("platform.machine", return_value="arch-b"):
                second = self.module.prepared_fixture_key(fixture, {"runtime": "1"})
        self.assertNotEqual(first, second)

    def test_preparation_is_cached_and_install_does_not_run_per_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture = root / "fixture"
            fixture.mkdir()
            (fixture / "source.txt").write_text("fixture\n", encoding="utf-8")
            calls: list[tuple[str, ...]] = []

            def record(command: object, cwd: Path) -> object:
                calls.append(tuple(command.argv))
                return self.module.CommandResult(tuple(command.argv), 0, "", "")

            manager = self.module.PreparedWorkspaceManager(root / "cache", root / "runs", command_runner=record)
            prepared = manager.prepare(fixture, {"runtime": "test"}, ["prepare", "fixture"])
            same = manager.prepare(fixture, {"runtime": "test"}, ["prepare", "fixture"])
            self.assertEqual(prepared.key, same.key)
            self.assertEqual(64, len(prepared.prepared_snapshot_digest))
            self.assertEqual(1, len(calls))
            with manager.workspace(prepared) as first:
                self.assertTrue((first.path / "source.txt").is_file())
                self.assertTrue((first.path / ".git").is_dir())
                status = self.module.run_command(self.module.command_spec(["git", "status", "--porcelain"]), first.path)
                self.assertEqual("", status.stdout)
            with manager.workspace(prepared) as second:
                self.assertTrue((second.path / "source.txt").is_file())
            self.assertEqual(1, len(calls))

    def test_tampered_prepared_source_is_rebuilt_before_cache_reuse(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture = root / "fixture"
            fixture.mkdir()
            (fixture / "source.txt").write_text("trusted\n", encoding="utf-8")
            manager = self.module.PreparedWorkspaceManager(root / "cache", root / "runs")
            prepared = manager.prepare(fixture, {"runtime": "1"})
            (prepared.path / "source.txt").write_text("tampered\n", encoding="utf-8")
            rebuilt = manager.prepare(fixture, {"runtime": "1"})
            self.assertFalse(rebuilt.cache_hit)
            self.assertEqual("trusted\n", (rebuilt.path / "source.txt").read_text(encoding="utf-8"))

    def test_full_integrity_mode_rebuilds_a_tampered_prepared_dependency(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture = root / "fixture"
            fixture.mkdir()
            (fixture / "source.txt").write_text("trusted\n", encoding="utf-8")
            calls = 0

            def install(command: object, cwd: Path) -> object:
                nonlocal calls
                calls += 1
                dependency = cwd / "node_modules" / "dependency.txt"
                dependency.parent.mkdir(parents=True, exist_ok=True)
                dependency.write_text("trusted dependency\n", encoding="utf-8")
                return self.module.CommandResult(tuple(command.argv), 0, "", "")

            manager = self.module.PreparedWorkspaceManager(
                root / "cache",
                root / "runs",
                command_runner=install,
                integrity_mode="full",
            )
            prepared = manager.prepare(fixture, {"runtime": "1"}, ["install"])
            (prepared.path / "node_modules" / "dependency.txt").write_text(
                "tampered dependency\n", encoding="utf-8"
            )
            rebuilt = manager.prepare(fixture, {"runtime": "1"}, ["install"])
            self.assertFalse(rebuilt.cache_hit)
            self.assertEqual(2, calls)
            self.assertEqual(
                "trusted dependency\n",
                (rebuilt.path / "node_modules" / "dependency.txt").read_text(
                    encoding="utf-8"
                ),
            )

    def test_preparation_may_not_mutate_fixture_source_identity(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture = root / "fixture"
            fixture.mkdir()
            (fixture / "source.txt").write_text("trusted\n", encoding="utf-8")

            def mutate_source(command: object, cwd: Path) -> object:
                (cwd / "source.txt").write_text("changed during install\n", encoding="utf-8")
                return self.module.CommandResult(tuple(command.argv), 0, "", "")

            manager = self.module.PreparedWorkspaceManager(
                root / "cache", root / "runs", command_runner=mutate_source
            )
            with self.assertRaisesRegex(RuntimeError, "changed fixture source identity"):
                manager.prepare(fixture, {"runtime": "1"}, ["install"])

    def test_live_cache_requirement_never_runs_a_missing_install(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture = root / "fixture"
            fixture.mkdir()
            (fixture / "source.txt").write_text("trusted\n", encoding="utf-8")

            def must_not_run(command: object, cwd: Path) -> object:
                raise AssertionError("install command executed")

            manager = self.module.PreparedWorkspaceManager(
                root / "cache", root / "runs", command_runner=must_not_run
            )
            with self.assertRaisesRegex(RuntimeError, "trusted prepared fixture"):
                manager.prepare(
                    fixture,
                    {"runtime": "1"},
                    ["install"],
                    allow_create=False,
                )

    def test_old_live_lock_is_not_stolen_and_dead_stale_lock_is_reclaimed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            live_path = root / "live.lock"
            live_path.write_text(json.dumps({"pid": os.getpid(), "token": "owner"}), encoding="utf-8")
            os.utime(live_path, (0, 0))
            with self.assertRaises(TimeoutError):
                with self.module.CacheKeyLock(live_path, timeout_seconds=0.05, stale_seconds=0):
                    pass
            self.assertTrue(live_path.is_file())
            dead_path = root / "dead.lock"
            dead_path.write_text(json.dumps({"pid": 2_147_483_647, "token": "dead"}), encoding="utf-8")
            os.utime(dead_path, (0, 0))
            with self.module.CacheKeyLock(dead_path, timeout_seconds=0.2, stale_seconds=0):
                self.assertTrue(dead_path.is_file())
            self.assertFalse(dead_path.exists())

    def test_controlled_command_environment_excludes_unapproved_host_secrets(self) -> None:
        with tempfile.TemporaryDirectory() as directory, mock.patch.dict(
            os.environ,
            {"SEEDED_COMPANY_SECRET": "must-not-leak"},
        ):
            command = self.module.command_spec([
                sys.executable,
                "-c",
                "import os; print('SEEDED_COMPANY_SECRET' in os.environ)",
            ])
            result = self.module.run_command(command, Path(directory))
        self.assertEqual("False", result.stdout.strip())

    def test_command_output_cap_terminates_the_process_group_while_draining_pipes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            command = self.module.command_spec({
                "argv": [sys.executable, "-c", "print('x' * 10000)"],
                "maximumOutputBytes": 128,
            })
            result = self.module.run_command(command, Path(directory))
        self.assertEqual(125, result.exit_code)
        self.assertLessEqual(len(result.stdout.encode("utf-8")), 128)
        self.assertIn("capture cap", result.stderr)

    def test_workspace_is_removed_after_context_exit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture = root / "fixture"
            fixture.mkdir()
            (fixture / "source.txt").write_text("fixture\n", encoding="utf-8")
            manager = self.module.PreparedWorkspaceManager(root / "cache", root / "runs")
            prepared = manager.prepare(fixture, {"runtime": "test"})
            workspace_path: Path | None = None
            with self.assertRaisesRegex(RuntimeError, "stop"):
                with manager.workspace(prepared) as workspace:
                    workspace_path = workspace.path
                    raise RuntimeError("stop")
            self.assertIsNotNone(workspace_path)
            self.assertFalse(workspace_path.exists())

    def test_parallel_preparation_runs_the_install_once(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture = root / "fixture"
            fixture.mkdir()
            (fixture / "source.txt").write_text("fixture\n", encoding="utf-8")
            started = threading.Event()
            release = threading.Event()
            call_count = 0
            call_lock = threading.Lock()

            def record(command: object, cwd: Path) -> object:
                nonlocal call_count
                with call_lock:
                    call_count += 1
                started.set()
                release.wait(timeout=2)
                return self.module.CommandResult(tuple(command.argv), 0, "", "")

            manager = self.module.PreparedWorkspaceManager(root / "cache", root / "runs", command_runner=record)
            with ThreadPoolExecutor(max_workers=2) as executor:
                first = executor.submit(manager.prepare, fixture, {"runtime": "test"}, ["prepare"])
                self.assertTrue(started.wait(timeout=2))
                second = executor.submit(manager.prepare, fixture, {"runtime": "test"}, ["prepare"])
                release.set()
                first_result = first.result(timeout=3)
                second_result = second.result(timeout=3)
            self.assertEqual(first_result.key, second_result.key)
            self.assertEqual(1, call_count)

    def test_read_only_audit_reports_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "source.txt").write_text("before\n", encoding="utf-8")
            before = self.module.snapshot_tree(root)
            (root / "source.txt").write_text("after\n", encoding="utf-8")
            audit = self.module.audit_functional_isolation(before, self.module.snapshot_tree(root), read_only=True)
        self.assertEqual("violated", audit.status)
        self.assertEqual(("source.txt",), audit.changed_paths)

    def test_product_audit_includes_dependency_and_build_trees(self) -> None:
        """A model cannot hide workspace mutation under dependency or build directories."""

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "node_modules" / "tool").mkdir(parents=True)
            (root / "node_modules" / "tool" / "index.js").write_text(
                "before\n", encoding="utf-8"
            )
            (root / "dist").mkdir()
            (root / "dist" / "bundle.js").write_text("before\n", encoding="utf-8")
            before = self.module.snapshot_product_tree(root)
            (root / "node_modules" / "tool" / "index.js").write_text(
                "after\n", encoding="utf-8"
            )
            (root / "dist" / "bundle.js").write_text("after\n", encoding="utf-8")
            audit = self.module.audit_functional_isolation(
                before,
                self.module.snapshot_product_tree(root),
                read_only=False,
                allowed_write_paths=["src"],
                ephemeral_write_paths=["dist"],
            )
        self.assertEqual("violated", audit.status)
        self.assertEqual(
            ("node_modules/tool/index.js",),
            audit.changed_paths,
        )
        self.assertEqual(("dist/bundle.js",), audit.ephemeral_changed_paths)

    def test_declared_build_output_is_recorded_without_becoming_product_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "src").mkdir()
            (root / "src" / "index.ts").write_text("source\n", encoding="utf-8")
            before = self.module.snapshot_product_tree(root)
            (root / "dist").mkdir()
            (root / "dist" / "index.js").write_text("compiled\n", encoding="utf-8")
            audit = self.module.audit_functional_isolation(
                before,
                self.module.snapshot_product_tree(root),
                read_only=True,
                ephemeral_write_paths=["dist"],
            )
        self.assertEqual("verified", audit.status)
        self.assertEqual((), audit.changed_paths)
        self.assertEqual(("dist", "dist/index.js"), audit.ephemeral_changed_paths)
        self.assertEqual(audit.before_digest, audit.after_digest)
        self.assertNotEqual(audit.workspace_before_digest, audit.workspace_after_digest)

    def test_ephemeral_ancestor_never_masks_nested_dependency_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tool = root / "packages" / "app" / "node_modules" / "tool.js"
            tool.parent.mkdir(parents=True)
            tool.write_text("before\n", encoding="utf-8")
            before = self.module.snapshot_product_tree(root)
            tool.write_text("after\n", encoding="utf-8")
            audit = self.module.audit_functional_isolation(
                before,
                self.module.snapshot_product_tree(root),
                read_only=False,
                ephemeral_write_paths=["packages/app"],
            )
        self.assertEqual("violated", audit.status)
        self.assertEqual(
            ("packages/app/node_modules/tool.js",), audit.changed_paths
        )
        self.assertNotIn(
            "packages/app/node_modules/tool.js", audit.ephemeral_changed_paths
        )


class EvidenceVersionTwoTests(unittest.TestCase):
    """Verify the current receipt contract and digest-staleness classifier."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_module()
        cls.case = dict(cls.module.load_cases()["typescript-order-pricing"])
        cls.case["id"] = "synthetic-deterministic-receipt"
        cls.case["judgePlan"] = {
            "deterministicChecks": ["required-command-outcome"],
            "modelRubric": None,
        }

    def receipt(self) -> dict[str, object]:
        agent_source = next((ROOT / "agents" / "roles").glob("**/dev-coder.role.yaml"))
        digest_value = "0" * 64
        adapter_identity = self.module.build_agent_evidence_identity("codex", "dev-coder")
        fixture_root = ROOT / str(self.case["project"])
        source_digest = self.module.snapshot_digest(
            self.module.snapshot_tree(fixture_root, exclude_transient=True),
        )
        dependency_digest = self.module.dependency_inputs_digest(fixture_root)
        preparation_environment_digest = self.module.command_environment_digest(
            self.module.command_spec(self.case.get("install")),
        )
        prepared_key = self.module.prepared_fixture_identity_key(
            source_digest,
            dependency_digest,
            digest_value,
            self.case.get("install"),
            preparation_environment_digest,
        )
        return {
            "schema": "dev-methodology-eval-evidence",
            "version": 2,
            "case": self.case["id"],
            "verdict": "verified",
            "captureProvenance": {
                "kind": "human-attested-harness-export",
                "reference": "attestation.json#capture",
            },
            "run": {
                "id": "run-1",
                "harness": "codex",
                "harnessVersion": "codex 1",
                "harnessDigest": digest_value,
                "harnessIdentityEvidence": "identities.json#harness",
                "model": "test-model",
                "modelDigest": digest_value,
                "modelIdentityEvidence": "identities.json#model",
                "agentId": "dev-coder",
                "conceptualAgentDigest": digest(agent_source),
                **adapter_identity,
                "invocationEvidence": "events.jsonl#invocation",
                "agentStartEvidence": "events.jsonl#agent-start",
                "attributionStatus": "verified",
                "eventLedger": "events.jsonl#ledger-start",
                "contextPackDigest": digest_value,
                "contextPackEvidence": "context.json#manifest",
                "approvedInputManifestDigest": digest_value,
                "caseDefinitionDigest": self.module.case_definition_digest(self.case),
                "installExecuted": False,
            },
            "skills": [
                {
                    **self.module.build_skill_evidence_identity(self.case, "codex", skill),
                    "readEvidence": [{"type": "tool-call", "reference": f"events.jsonl#read-{skill}"}],
                }
                for skill in self.case["requiredSkills"]
            ],
            "budgets": {
                "limits": {"turns": 20, "tokens": 10000, "seconds": 600, "toolCalls": 100},
                "usage": {"turns": 5, "tokens": 1000, "seconds": 60, "toolCalls": 10},
            },
            "preparedFixture": {
                "key": prepared_key,
                "sourceDigest": source_digest,
                "preparedSnapshotDigest": "3" * 64,
                "preparedSnapshotEvidence": "prepared-snapshot.json#prepared-snapshot",
                "dependencyDigest": dependency_digest,
                "toolchainDigest": digest_value,
                "preparationEnvironmentDigest": preparation_environment_digest,
                "platform": {"system": "test", "release": "1", "machine": "test-arch"},
                "toolchainEvidence": "identities.json#toolchain",
                "preparationEnvironmentEvidence": "identities.json#preparation-environment",
            },
            "isolation": {
                "workspacePreparation": "copy-on-write",
                "sandboxProfile": self.case["sandboxProfiles"]["codex"],
                "sandboxProfileDigest": self.module.case_definition_digest(
                    next(
                        profile
                        for profile in self.module.load_framework_catalogs()[
                            "sandbox-profiles.yaml"
                        ]["profiles"]
                        if profile["id"]
                        == self.case["sandboxProfiles"]["codex"]
                    )
                ),
                "sandboxProfileEvidence": "isolation.json#sandbox-profile",
                "functional": {
                    "status": "verified",
                    "projectHashBefore": "product-same",
                    "projectHashAfter": "product-same",
                    "workspaceHashBefore": "workspace-same",
                    "workspaceHashAfter": "workspace-same",
                    "allowedWritePaths": self.case["allowedWritePaths"],
                    "ephemeralWritePaths": self.case.get("ephemeralWritePaths", []),
                    "changedPaths": [],
                    "ephemeralChangedPaths": [],
                    "evidence": "isolation.json#functional",
                },
                "containment": {
                    "level": "workspace-isolated-only",
                    "status": "verified",
                    "enforcedBy": "codex-native-plus-runner",
                    "evidence": "isolation.json#containment",
                },
                "codexNativeSandbox": {
                    "mode": "workspace-write",
                    "evidence": "isolation.json#codex-native",
                },
            },
            "judges": {
                "deterministic": {
                    "verdict": "passed",
                    "records": [{
                        "id": "required-command-outcome",
                        "critical": True,
                        "verdict": "passed",
                        "evidence": "judges.json#required-command-outcome",
                    }],
                },
                "model": {"status": "not-required"},
            },
            "behaviorAssertions": [
                {"id": assertion, "verdict": "passed", "evidence": f"assertions.json#{assertion}"}
                for assertion in self.case["requiredEvidence"]
            ],
            "commands": [{
                "argv": ["npm", "test"],
                "exitCode": 0,
                "expectation": "success",
                "evidence": "commands.log#test",
            }],
            "independentJudge": {
                "kind": "Deterministic Judge",
                "reference": "judges.json#independent",
                "invocationId": "judge-run-1",
                "contextIdentity": "1" * 64,
                "modelIdentity": "deterministic-runner-v1",
                "reasoningProfile": "deterministic",
                "judgePromptSha256": hashlib.sha256(b"judge-prompt\n").hexdigest(),
                "judgePromptEvidence": "judge-prompt.txt#judge-prompt",
                "inputManifestDigest": "2" * 64,
                "inputManifestEvidence": "judge-input.json#manifest",
                "invocationEvidence": "judges.json#judge-invocation",
                "contextEvidence": "judges.json#judge-context",
                "evaluatedRunId": "run-1",
                "blindTo": ["treatment", "expected-winner", "evaluated-model-identity"],
            },
        }

    def classify(self, receipt: dict[str, object], *, include_agent_start: bool = True) -> object:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "evidence.yaml"
            events = [{
                "id": "ledger-start",
                "type": "ledger",
            }, {
                "id": "invocation",
                "type": "invocation",
                "agent": "dev-coder",
                "harness": "codex",
                "model": "test-model",
            }]
            if include_agent_start:
                events.append({
                    "id": "agent-start",
                    "type": "agent-start",
                    "agent": "dev-coder",
                    "contentDigest": receipt["run"].get("nativeAdapterEffectiveDigest"),
                })
            events.extend({
                "id": f"read-{skill}",
                "type": "tool-call",
                "skill": skill,
                "contentDigest": next(
                    item["effectiveDigest"] for item in receipt["skills"] if item["id"] == skill
                ),
            } for skill in self.case["requiredSkills"])
            (root / "events.jsonl").write_text("\n".join(json.dumps(event) for event in events) + "\n", encoding="utf-8")
            (root / "attestation.json").write_text("capture\n", encoding="utf-8")
            (root / "identities.json").write_text(
                "harness\nmodel\ntoolchain\npreparation-environment\n",
                encoding="utf-8",
            )
            (root / "prepared-snapshot.json").write_text(
                json.dumps(
                    {
                        "id": "prepared-snapshot",
                        "preparedKey": receipt["preparedFixture"]["key"],
                        "preparedSnapshotDigest": "3" * 64,
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            (root / "context.json").write_text("manifest\n", encoding="utf-8")
            (root / "isolation.json").write_text(
                "sandbox-profile\nfunctional\ncontainment\ncodex-native\n",
                encoding="utf-8",
            )
            (root / "judges.json").write_text(
                "required-command-outcome\nindependent\njudge-invocation\njudge-context\n",
                encoding="utf-8",
            )
            (root / "judge-prompt.txt").write_text("judge-prompt\n", encoding="utf-8")
            (root / "judge-input.json").write_text("manifest\n", encoding="utf-8")
            (root / "assertions.json").write_text(
                "\n".join(str(item) for item in self.case["requiredEvidence"]) + "\n", encoding="utf-8",
            )
            (root / "commands.log").write_text("test\n", encoding="utf-8")
            path.write_text(yaml.safe_dump(receipt), encoding="utf-8")
            return self.module.classify_evidence(self.case, path)

    def test_complete_self_attested_receipt_is_recorded_but_not_verified(self) -> None:
        """A same-directory attestation is not an external trust anchor."""

        classification = self.classify(self.receipt())
        self.assertTrue(classification.executed)
        self.assertFalse(classification.verified)
        self.assertFalse(classification.stale_by_digest)
        self.assertTrue(
            any("external" in item and "verification" in item for item in classification.errors)
        )

    def test_agent_source_drift_is_classified_separately(self) -> None:
        receipt = self.receipt()
        receipt["run"]["conceptualAgentDigest"] = "f" * 64
        classification = self.classify(receipt)
        self.assertTrue(classification.executed)
        self.assertFalse(classification.verified)
        self.assertTrue(classification.stale_by_digest)
        self.assertTrue(any("conceptual agent digest mismatch" in item for item in classification.stale_reasons))

    def test_external_runner_required_case_cannot_promote_local_receipt(self) -> None:
        receipt = self.receipt()
        receipt["captureProvenance"]["kind"] = "trusted-ci"
        classification = self.classify(receipt)
        self.assertTrue(classification.executed)
        self.assertFalse(classification.verified)
        self.assertTrue(
            any("trusted external post-run verification" in item for item in classification.errors)
        )

    def test_codex_attribution_requires_a_digest_bound_agent_start_event(self) -> None:
        classification = self.classify(self.receipt(), include_agent_start=False)
        self.assertFalse(classification.executed)
        self.assertFalse(classification.verified)
        self.assertTrue(any("agent-start event" in item for item in classification.errors))

    def test_header_only_receipt_does_not_count_as_executed(self) -> None:
        receipt = {
            "schema": "dev-methodology-eval-evidence",
            "version": 2,
            "case": self.case["id"],
            "verdict": "verified",
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "evidence.yaml"
            path.write_text(yaml.safe_dump(receipt), encoding="utf-8")
            classification = self.module.classify_evidence(self.case, path)
        self.assertFalse(classification.executed)
        self.assertFalse(classification.verified)

    def test_unverified_workspace_containment_cannot_verify(self) -> None:
        receipt = self.receipt()
        receipt["isolation"]["containment"]["status"] = "unverified"
        receipt["isolation"]["containment"].pop("evidence")
        classification = self.classify(receipt)
        self.assertFalse(classification.verified)
        self.assertTrue(
            any("workspace-isolated-only" in item for item in classification.errors)
        )

    def test_deterministic_only_case_requires_model_not_required_status(self) -> None:
        receipt = self.receipt()
        receipt["judges"]["model"] = {"status": "failed"}
        classification = self.classify(receipt)
        self.assertFalse(classification.verified)
        self.assertTrue(any("not-required" in item for item in classification.errors))

    def test_prepared_snapshot_digest_is_required(self) -> None:
        receipt = self.receipt()
        receipt["preparedFixture"].pop("preparedSnapshotDigest", None)
        classification = self.classify(receipt)
        self.assertFalse(classification.verified)
        self.assertTrue(
            any("preparedSnapshotDigest" in item for item in classification.errors)
        )

    def test_prepared_snapshot_digest_must_match_its_capture(self) -> None:
        receipt = self.receipt()
        receipt["preparedFixture"]["preparedSnapshotDigest"] = "4" * 64
        classification = self.classify(receipt)
        self.assertFalse(classification.verified)
        self.assertTrue(
            any("prepared snapshot capture" in item for item in classification.errors)
        )

    def test_conceptual_agent_digest_cannot_replace_native_adapter_identity(self) -> None:
        receipt = self.receipt()
        receipt["run"].pop("nativeAdapterEffectiveDigest")
        classification = self.classify(receipt)
        self.assertFalse(classification.verified)
        self.assertTrue(any("nativeAdapterEffectiveDigest" in item for item in classification.errors))

    def test_fixture_and_case_definition_drift_are_stale(self) -> None:
        receipt = self.receipt()
        receipt["preparedFixture"]["sourceDigest"] = "f" * 64
        receipt["run"]["caseDefinitionDigest"] = "e" * 64
        classification = self.classify(receipt)
        self.assertFalse(classification.verified)
        self.assertTrue(classification.stale_by_digest)
        self.assertTrue(any("fixture sourceDigest" in item for item in classification.stale_reasons))
        self.assertTrue(any("case definition" in item for item in classification.stale_reasons))

    def test_unrelated_command_cannot_stand_in_for_case_verification(self) -> None:
        receipt = self.receipt()
        receipt["commands"][0]["argv"] = ["true"]
        classification = self.classify(receipt)
        self.assertFalse(classification.verified)
        self.assertTrue(any("case.verify" in item for item in classification.errors))

    def test_independent_judge_cannot_reuse_the_evaluated_context(self) -> None:
        receipt = self.receipt()
        receipt["independentJudge"]["contextIdentity"] = receipt["run"]["contextPackDigest"]
        classification = self.classify(receipt)
        self.assertFalse(classification.verified)
        self.assertTrue(any("context must differ" in item for item in classification.errors))


class HarnessAndJudgeTests(unittest.TestCase):
    """Verify harness command safety, Judge ordering, and calibration freshness."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_module()

    def test_harness_builders_support_only_codex_and_junie(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "workspace"
            evidence_root = base / "evidence"
            evidence_root.mkdir()
            (root / ".codex" / "agents").mkdir(parents=True)
            (root / ".codex" / "agents" / "dev-coder.toml").write_text('name = "dev-coder"\n', encoding="utf-8")
            (root / ".agents" / "skills").mkdir(parents=True)
            (root / ".junie" / "agents").mkdir(parents=True)
            (root / ".junie" / "skills").mkdir(parents=True)
            codex = self.module.build_harness_command(
                "codex", root, "dev-coder", "Do the task", "test-model", read_only=True,
                event_output=evidence_root / "codex.jsonl",
                evidence_root=evidence_root,
                isolated_config_root=root,
            )
            self.assertIn("--sandbox", codex.argv)
            self.assertIn("read-only", codex.argv)
            self.assertIn("--ephemeral", codex.argv)
            junie = self.module.build_harness_command(
                "junie", root, "dev-coder", "Do the task", "test-model", read_only=False,
                event_output=evidence_root / "junie.jsonl",
                evidence_root=evidence_root,
                isolated_config_root=root,
                skill_locations=[root / ".junie" / "skills"],
                agent_locations=[root / ".junie" / "agents"],
            )
            self.assertTrue(any(value.startswith("--task=Delegate the following task") for value in junie.argv))
            self.assertFalse(any("sandbox" in value.lower() for value in junie.argv))
            with self.assertRaisesRegex(ValueError, "supported harness"):
                self.module.build_harness_command(
                    "claude", root, "dev-coder", "Do the task", "test-model", read_only=False,
                    event_output=evidence_root / "other.jsonl",
                    evidence_root=evidence_root,
                    isolated_config_root=root,
                )
            with self.assertRaisesRegex(ValueError, "runner-owned evidence root"):
                self.module.build_harness_command(
                    "codex",
                    root,
                    "dev-coder",
                    "Do the task",
                    "test-model",
                    read_only=True,
                    event_output=root / "events.jsonl",
                    evidence_root=evidence_root,
                    isolated_config_root=root,
                )
            with self.assertRaisesRegex(ValueError, "runner-owned evidence root"):
                self.module.build_harness_command(
                    "codex",
                    root,
                    "dev-coder",
                    "Do the task",
                    "test-model",
                    read_only=True,
                    event_output=base / "arbitrary-host-output.jsonl",
                    evidence_root=evidence_root,
                    isolated_config_root=root,
                )
            with self.assertRaisesRegex(ValueError, "runner-owned evidence root"):
                self.module.build_harness_command(
                    "junie",
                    root,
                    "dev-coder",
                    "Do the task",
                    "test-model",
                    read_only=False,
                    event_output=evidence_root / "junie-cache-check.jsonl",
                    evidence_root=evidence_root,
                    isolated_config_root=root,
                    cache_dir=base / "arbitrary-host-cache",
                    skill_locations=[root / ".junie" / "skills"],
                    agent_locations=[root / ".junie" / "agents"],
                )

    def test_harness_builder_requires_an_isolated_context_root(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "workspace"
            root.mkdir()
            evidence_root = base / "evidence"
            evidence_root.mkdir()
            with self.assertRaisesRegex(ValueError, "isolated_config_root"):
                self.module.build_harness_command(
                    "codex", root, "dev-coder", "Do the task", "test-model", read_only=False,
                    event_output=evidence_root / "events.jsonl",
                    evidence_root=evidence_root,
                )

    def test_codex_read_only_final_response_is_captured_outside_the_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "workspace"
            evidence_root = base / "evidence"
            evidence_root.mkdir()
            (root / ".codex" / "agents").mkdir(parents=True)
            (root / ".codex" / "agents" / "dev-coder.toml").write_text('name = "dev-coder"\n', encoding="utf-8")
            (root / ".agents" / "skills").mkdir(parents=True)
            output = evidence_root / "review.md"
            command = self.module.build_harness_command(
                "codex",
                root,
                "dev-coder",
                "Review the source",
                "test-model",
                read_only=True,
                event_output=evidence_root / "events.jsonl",
                evidence_root=evidence_root,
                isolated_config_root=root,
                last_message_output=output,
            )
            self.assertIn("--output-last-message", command.argv)
            self.assertIn(str(output.resolve()), command.argv)
            with self.assertRaisesRegex(ValueError, "runner-owned evidence root"):
                self.module.build_harness_command(
                    "codex",
                    root,
                    "dev-coder",
                    "Review the source",
                    "test-model",
                    read_only=True,
                    event_output=evidence_root / "events.jsonl",
                    evidence_root=evidence_root,
                    isolated_config_root=root,
                    last_message_output=root / "review.md",
                )

    def test_output_schema_must_be_the_evaluator_owned_codex_json_schema(self) -> None:
        schema_path = ROOT / "evals" / "codex-agent-output-schema.json"
        self.assertEqual(
            schema_path.resolve(),
            self.module._trusted_output_schema(schema_path),
        )
        for rejected in (
            ROOT / "evals" / "cases.yaml",
            ROOT / "evals" / "judge-output-schema.yaml",
        ):
            with self.subTest(rejected=rejected.name):
                with self.assertRaisesRegex(ValueError, "canonical evaluator-owned Codex JSON Schema"):
                    self.module._trusted_output_schema(rejected)
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            external = base / "schema.json"
            external.write_text("{}\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "canonical evaluator-owned Codex JSON Schema"):
                self.module._trusted_output_schema(external)
            workspace = base / "workspace"
            evidence_root = base / "evidence"
            evidence_root.mkdir()
            (workspace / ".codex" / "agents").mkdir(parents=True)
            (workspace / ".codex" / "agents" / "dev-coder.toml").write_text(
                'name = "dev-coder"\n', encoding="utf-8"
            )
            (workspace / ".agents" / "skills").mkdir(parents=True)
            with self.assertRaisesRegex(ValueError, "canonical evaluator-owned Codex JSON Schema"):
                self.module.build_harness_command(
                    "codex",
                    workspace,
                    "dev-coder",
                    "Do the task",
                    "test-model",
                    read_only=True,
                    event_output=evidence_root / "events.jsonl",
                    evidence_root=evidence_root,
                    isolated_config_root=workspace,
                    output_schema=external,
                )

    def test_junie_live_command_requires_an_attested_external_runner(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "workspace"
            evidence_root = base / "evidence"
            evidence_root.mkdir()
            (root / ".junie" / "agents").mkdir(parents=True)
            (root / ".junie" / "skills").mkdir(parents=True)
            command = self.module.build_harness_command(
                "junie",
                root,
                "dev-coder",
                "Do the task",
                "test-model",
                read_only=False,
                event_output=evidence_root / "junie.jsonl",
                evidence_root=evidence_root,
                isolated_config_root=root,
                skill_locations=[root / ".junie" / "skills"],
                agent_locations=[root / ".junie" / "agents"],
            )
            runner = base / "external-runner"
            runner.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            runner.chmod(0o700)
            attestation = base / "attestation.json"
            with self.assertRaisesRegex(ValueError, "attestation"):
                self.module.wrap_junie_external_runner(command, runner, attestation)
            attestation.write_text(json.dumps({
                "schema": "dev-methodology-junie-containment-attestation",
                "version": 1,
                "status": "verified",
                "runnerDigest": digest(runner),
                "capabilities": ["filesystem", "process", "network", "cpu", "memory", "time"],
            }), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "explicitly unverified"):
                self.module.wrap_junie_external_runner(command, runner, attestation)
            attestation.write_text(json.dumps({
                "schema": "dev-methodology-junie-containment-attestation",
                "version": 1,
                "status": "self-attested-unverified",
                "runnerDigest": digest(runner),
                "capabilities": ["filesystem", "process", "network", "cpu", "memory", "time"],
            }), encoding="utf-8")
            wrapped = self.module.wrap_junie_external_runner(command, runner, attestation)
            self.assertEqual(str(runner.resolve()), wrapped.command.argv[0])
            self.assertEqual("--", wrapped.command.argv[1])
            self.assertEqual("junie", wrapped.command.argv[2])
            self.assertEqual("self-attested-unverified", wrapped.trust_status)

    def test_cli_never_executes_junie_directly(self) -> None:
        with mock.patch.object(self.module, "run_command") as execute:
            with redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    self.module.main([
                        "--case",
                        "typescript-code-review",
                        "--harness",
                        "junie",
                        "--invoke-harness",
                    ])
        execute.assert_not_called()

    def test_live_harness_path_never_runs_host_verification(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            fixture = base / "fixture"
            fixture.mkdir()
            (fixture / "TASK.md").write_text("Synthetic task.\n", encoding="utf-8")
            case = {
                "id": "host-verification-gate",
                "project": "evals/projects/host-verification-gate",
                "task": "TASK.md",
                "verify": [sys.executable, "-c", "raise SystemExit('must not run')"],
                "harnesses": ["codex", "junie"],
                "requiredAgents": ["dev-coder"],
                "requiredSkills": ["careful-coding"],
                "requiredEvidence": ["SAFE"],
                "allowedWritePaths": [],
                "modelVisiblePaths": ["TASK.md"],
            }
            with mock.patch.object(
                self.module, "load_cases", return_value={case["id"]: case}
            ), mock.patch.object(
                self.module, "_handle_harness_invocation", return_value=None
            ), mock.patch.object(
                self.module,
                "run",
                side_effect=AssertionError("host verification executed"),
            ) as verify:
                exit_code = self.module.main([
                    "--case",
                    case["id"],
                    "--project-root",
                    str(fixture),
                    "--prepared-cache",
                    str(base / "cache"),
                    "--workspace-root",
                    str(base / "runs"),
                    "--harness",
                    "codex",
                    "--invoke-harness",
                ])
        self.assertEqual(0, exit_code)
        verify.assert_not_called()

    def test_isolation_failure_still_never_runs_host_verification(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            fixture = base / "fixture"
            fixture.mkdir()
            (fixture / "TASK.md").write_text("Synthetic task.\n", encoding="utf-8")
            case = {
                "id": "isolation-verification-gate",
                "project": "evals/projects/isolation-verification-gate",
                "task": "TASK.md",
                "verify": [sys.executable, "-c", "raise SystemExit('must not run')"],
                "harnesses": ["codex", "junie"],
                "requiredAgents": ["dev-coder"],
                "requiredSkills": ["careful-coding"],
                "requiredEvidence": ["SAFE"],
                "allowedWritePaths": [],
                "modelVisiblePaths": ["TASK.md"],
            }

            def mutate_outside_contract(
                args: object, selected: object, active_root: Path
            ) -> None:
                (active_root / "unexpected.txt").write_text("mutation\n", encoding="utf-8")
                return None

            with mock.patch.object(
                self.module, "load_cases", return_value={case["id"]: case}
            ), mock.patch.object(
                self.module,
                "_handle_harness_invocation",
                side_effect=mutate_outside_contract,
            ), mock.patch.object(
                self.module,
                "run",
                side_effect=AssertionError("host verification executed"),
            ) as verify, redirect_stderr(io.StringIO()):
                exit_code = self.module.main([
                    "--case",
                    case["id"],
                    "--project-root",
                    str(fixture),
                    "--prepared-cache",
                    str(base / "cache"),
                    "--workspace-root",
                    str(base / "runs"),
                    "--harness",
                    "codex",
                    "--invoke-harness",
                ])
        self.assertEqual(1, exit_code)
        verify.assert_not_called()

    def test_live_install_is_refused_before_workspace_or_command_execution(self) -> None:
        with mock.patch.object(
            self.module,
            "_workspace_manager",
            side_effect=AssertionError("workspace preparation started"),
        ):
            with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                self.module.main([
                    "--case",
                    "typescript-code-review",
                    "--harness",
                    "codex",
                    "--invoke-harness",
                    "--install",
                ])

    def test_invalid_fixture_contract_never_reaches_host_verification(self) -> None:
        case = {
            "id": "invalid-fixture-contract",
            "project": "../outside",
            "task": "missing.md",
            "verify": [sys.executable, "-c", "raise SystemExit('must not run')"],
            "harnesses": ["codex", "junie"],
            "requiredAgents": ["dev-coder"],
            "requiredSkills": ["careful-coding"],
            "requiredEvidence": ["SAFE"],
            "modelVisiblePaths": ["missing.md"],
        }
        with mock.patch.object(
            self.module, "load_cases", return_value={case["id"]: case}
        ), mock.patch.object(
            self.module,
            "run",
            side_effect=AssertionError("host verification executed"),
        ) as verify, redirect_stderr(io.StringIO()):
            exit_code = self.module.main(["--case", case["id"]])
        self.assertEqual(1, exit_code)
        verify.assert_not_called()

    def test_print_invocation_is_preflight_only_for_a_generation_case(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory) / "fixture"
            fixture.mkdir()
            (fixture / "TASK.md").write_text("Generate output.md.\n", encoding="utf-8")
            case = {
                "id": "generation-preflight",
                "project": "evals/projects/generation-preflight",
                "task": "TASK.md",
                "install": None,
                "verify": [
                    sys.executable,
                    "-c",
                    "from pathlib import Path; raise SystemExit(0 if Path('output.md').is_file() else 1)",
                ],
                "harnesses": ["codex", "junie"],
                "requiredAgents": ["dev-coder"],
                "requiredSkills": ["careful-coding"],
                "requiredEvidence": ["OUTPUT"],
                "modelVisiblePaths": ["TASK.md"],
            }
            output = io.StringIO()
            harness_identity = self.module.HarnessIdentity(
                "codex",
                SCRIPT_PATH,
                "codex test",
                digest(SCRIPT_PATH),
            )
            with mock.patch.object(self.module, "load_cases", return_value={case["id"]: case}), mock.patch.object(
                self.module,
                "capture_harness_identity",
                return_value=harness_identity,
            ), mock.patch.object(self.module, "run", side_effect=AssertionError("fixture verification ran")):
                with redirect_stdout(output):
                    exit_code = self.module.main([
                        "--case",
                        case["id"],
                        "--project-root",
                        str(fixture),
                        "--harness",
                        "codex",
                        "--print-invocation",
                    ])
        self.assertEqual(0, exit_code)
        self.assertIn("PREFLIGHT PASS generation-preflight", output.getvalue())

    def test_skill_probe_plan_freezes_treatment_omission_and_wrong_skill_variants(self) -> None:
        case = {
            "id": "case-1",
            "requiredSkills": ["target-skill", "shared-skill"],
        }
        catalogs = {
            "skill-probes.yaml": {
                "probes": [{
                    "id": "probe-target",
                    "skill": "target-skill",
                    "ablation": {"wrongSkillControl": "wrong-skill"},
                }],
            },
        }
        with mock.patch.object(self.module, "load_framework_catalogs", return_value=catalogs):
            treatment = self.module._apply_probe_variant(case, "probe-target", "treatment")
            omitted = self.module._apply_probe_variant(case, "probe-target", "target-omitted")
            wrong = self.module._apply_probe_variant(case, "probe-target", "wrong-skill")
        self.assertEqual(["target-skill", "shared-skill"], treatment["executionSkills"])
        self.assertEqual(["shared-skill"], omitted["executionSkills"])
        self.assertEqual(["shared-skill", "wrong-skill"], wrong["executionSkills"])
        self.assertEqual(treatment["probeComparisonKey"], omitted["probeComparisonKey"])
        self.assertEqual(omitted["probeComparisonKey"], wrong["probeComparisonKey"])

    def test_context_pack_stages_only_allowlisted_files_and_records_digest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            (source / "generated" / "adapters" / "codex" / "agents").mkdir(parents=True)
            (source / "skills" / "careful-coding").mkdir(parents=True)
            (source / "generated" / "adapters" / "codex" / "agents" / "dev-coder.toml").write_text(
                'name = "dev-coder"\ndeveloper_instructions = "load codex-harness-directives"\n', encoding="utf-8",
            )
            (source / "adapters" / "codex" / "skills" / "codex-harness-directives").mkdir(parents=True)
            (source / "adapters" / "codex" / "skills" / "codex-harness-directives" / "SKILL.md").write_text(
                "# Codex Harness Directives\n", encoding="utf-8",
            )
            (source / "skills" / "careful-coding" / "SKILL.md").write_text(
                "# Careful Coding\n", encoding="utf-8",
            )
            (source / "skills" / "careful-coding" / "private.txt").write_text(
                "must not be staged\n", encoding="utf-8",
            )
            (source / "skills" / "careful-coding" / "scripts").mkdir()
            (source / "skills" / "careful-coding" / "scripts" / "helper.py").write_text(
                "# Copyright (c) 2026 Martin.Bechard@DevConsult.ca\nprint('helper')\n",
                encoding="utf-8",
            )
            pack = self.module.ContextPackBuilder(source).stage(
                "codex",
                "dev-coder",
                ["careful-coding"],
                root / "staged",
                skill_files={"careful-coding": ["SKILL.md", "scripts"]},
            )
            self.assertEqual(64, len(pack.manifest_digest))
            staged_files = {item.source_path for item in pack.files}
            self.assertEqual({
                "generated/adapters/codex/agents/dev-coder.toml",
                "adapters/codex/skills/codex-harness-directives/SKILL.md",
                "skills/careful-coding/SKILL.md",
                "skills/careful-coding/scripts/helper.py",
            }, staged_files)
            harness_files = {item.source_path for item in pack.files if item.context_role == "harness-required-skill"}
            self.assertEqual({"adapters/codex/skills/codex-harness-directives/SKILL.md"}, harness_files)
            helper = next(item for item in pack.files if item.source_path.endswith("helper.py"))
            self.assertNotEqual(helper.content_digest, helper.effective_digest)
            self.assertEqual(("redacted-mandated-copyright-email",), helper.sanitizations)
            staged_helper = pack.root / helper.destination_path
            self.assertNotIn("Martin.Bechard@DevConsult.ca", staged_helper.read_text(encoding="utf-8"))
            self.assertFalse(any(path.name == "private.txt" for path in pack.root.rglob("*")))

    def test_context_pack_rejects_sensitive_additional_input(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            (source / "generated" / "adapters" / "junie" / "agents").mkdir(parents=True)
            (source / "skills" / "careful-coding").mkdir(parents=True)
            (source / "generated" / "adapters" / "junie" / "agents" / "dev-coder.md").write_text(
                "# dev-coder\n", encoding="utf-8",
            )
            (source / "skills" / "careful-coding" / "SKILL.md").write_text(
                "# Careful Coding\n", encoding="utf-8",
            )
            (source / "fixture.txt").write_text("contact seeded.person@example.com\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "sensitive input"):
                self.module.ContextPackBuilder(source).stage(
                    "junie",
                    "dev-coder",
                    ["careful-coding"],
                    root / "staged",
                    additional_files=["fixture.txt"],
                )

    def test_sensitive_policy_language_is_not_misclassified_as_payload(self) -> None:
        """A safety instruction may name forbidden data without containing that data."""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "SKILL.md"
            path.write_text(
                "Do not send company-internal material to an external service.\n",
                encoding="utf-8",
            )
            source, effective, actions = self.module.selected_context_identity(
                path, "treatment-skill"
            )
            self.assertEqual(source, effective)
            self.assertEqual((), actions)
            path.write_text(
                "Copyright holder: example.author@example.com\n",
                encoding="utf-8",
            )
            source, effective, actions = self.module.selected_context_identity(
                path, "treatment-skill"
            )
            self.assertNotEqual(source, effective)
            self.assertEqual(("redacted-context-email",), actions)
            self.assertNotIn(b"example.author@example.com", effective)
            path.write_text(
                "classification: company-internal\nsynthetic payload\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "sensitive input"):
                self.module.selected_context_identity(path, "treatment-skill")

    def test_model_visible_allowlist_rejects_an_omitted_workspace_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "TASK.md").write_text("synthetic task\n", encoding="utf-8")
            (root / "hidden.txt").write_text("unlisted input\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "allowlist omits workspace file"):
                self.module.build_input_manifest(root, ["TASK.md"])

    def test_model_visible_inventory_rejects_file_and_directory_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "workspace"
            outside = base / "outside"
            root.mkdir()
            outside.mkdir()
            (root / "TASK.md").write_text("Synthetic task.\n", encoding="utf-8")
            (outside / "secret.txt").write_text("must not be readable\n", encoding="utf-8")
            (root / "file-link").symlink_to(outside / "secret.txt")
            with self.assertRaisesRegex(ValueError, "symlink"):
                self.module.build_input_manifest(root, ["."])
            (root / "file-link").unlink()
            (root / "directory-link").symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "symlink"):
                self.module.build_input_manifest(root, ["."])

    def test_case_paths_must_stay_inside_the_fixture_catalog(self) -> None:
        case = {
            "id": "unsafe-paths",
            "project": "../outside",
            "task": "TASK.md",
            "verify": ["true"],
            "requiredAgents": ["dev-coder"],
            "requiredSkills": ["careful-coding"],
            "requiredEvidence": ["SAFE"],
            "harnesses": ["codex", "junie"],
            "modelVisiblePaths": ["TASK.md"],
        }
        errors = self.module.validate_case_definition(case)
        self.assertTrue(any("case.project" in error for error in errors))
        case["project"] = "evals/projects/synthetic"
        case["task"] = "../outside.md"
        errors = self.module.validate_case_definition(case)
        self.assertTrue(any("case.task" in error for error in errors))

    def test_dependency_trees_cannot_be_declared_ephemeral(self) -> None:
        for path in (
            "node_modules",
            "packages/app/node_modules",
            "services/api/.venv",
            "third_party/vendor/generated",
        ):
            with self.subTest(path=path):
                case = dict(self.module.load_cases()["typescript-order-pricing"])
                case["ephemeralWritePaths"] = [path]
                errors = self.module.validate_case_definition(case)
                self.assertTrue(
                    any("dependency or tool tree" in error for error in errors)
                )

    def test_ephemeral_paths_require_a_recognized_generated_output_leaf(self) -> None:
        case = dict(self.module.load_cases()["typescript-order-pricing"])
        case["ephemeralWritePaths"] = ["packages/app"]
        errors = self.module.validate_case_definition(case)
        self.assertTrue(
            any("recognized generated-output leaf" in error for error in errors)
        )

    def test_agent_scenario_contract_must_match_its_conceptual_source(self) -> None:
        validation_module = sys.modules[
            self.module.validate_framework_catalogs.__module__
        ]
        catalogs = self.module.load_framework_catalogs()
        mutated = json.loads(json.dumps(catalogs))
        project_configurator = next(
            agent
            for agent in mutated["agent-scenarios.yaml"]["agents"]
            if agent["id"] == "project-configurator"
        )
        project_configurator["outputContractFields"] = ["rewritten contract"]
        project_configurator["repositoryMutation"] = "never"
        errors: list[str] = []
        validation_module._validate_catalog_cross_references(
            mutated,
            self.module.load_cases(),
            ROOT / "evals",
            errors,
        )
        self.assertTrue(any("outputContractFields" in error for error in errors))
        self.assertTrue(any("repositoryMutation" in error for error in errors))

    def test_skill_resource_receipt_records_source_effective_and_sanitization_identity(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill = root / "skills" / "sample-skill"
            (skill / "scripts").mkdir(parents=True)
            (skill / "SKILL.md").write_text("# Sample Skill\n", encoding="utf-8")
            (skill / "scripts" / "helper.py").write_text(
                "# Copyright (c) 2026 Martin.Bechard@DevConsult.ca\n",
                encoding="utf-8",
            )
            case = {
                "skillResourceAllowlist": {
                    "sample-skill": ["SKILL.md", "scripts/helper.py"],
                },
            }
            identity = self.module.build_skill_evidence_identity(
                case,
                "codex",
                "sample-skill",
                source_root=root,
            )
        helper = next(item for item in identity["resources"] if item["path"] == "scripts/helper.py")
        self.assertNotEqual(helper["sourceDigest"], helper["effectiveDigest"])
        self.assertEqual(["redacted-mandated-copyright-email"], helper["sanitizations"])
        self.assertEqual(64, len(identity["resourceManifestDigest"]))

    def test_calibration_accepts_current_record_and_rejects_digest_drift(self) -> None:
        samples = _calibration_samples()
        expected = {
            "rubricId": "test-rubric",
            "judgePromptSha256": "prompt",
            "judgeOutputSchemaSha256": "schema",
            "instructionEnvelopeSha256": "envelope",
            "harness": "codex",
            "judgeModelIdentity": "model",
            "reasoningProfile": "advanced",
            "rubricSha256": "rubric",
            "calibrationSetSha256": self.module.calibration_set_digest(samples),
        }
        record = {
            **expected,
            "status": "accepted",
            "samples": samples,
            "metrics": {
                "binaryF1": 1.0,
                "weightedKappa": 1.0,
                "criticalDefectRecall": 1.0,
                "sampleCount": 25,
            },
        }
        record["recordDigest"] = self.module.calibration_record_digest(record)
        self.assertEqual([], self.module.validate_calibration_record(record, expected))
        for field in expected:
            stale = dict(expected)
            stale[field] = "changed"
            errors = self.module.validate_calibration_record(record, stale)
            self.assertTrue(any(field in error for error in errors))

    def test_calibration_rejects_weak_critical_recall(self) -> None:
        samples = _calibration_samples()
        expected = {
            "rubricId": "test-rubric",
            "judgePromptSha256": "prompt",
            "judgeOutputSchemaSha256": "schema",
            "instructionEnvelopeSha256": "envelope",
            "harness": "codex",
            "judgeModelIdentity": "model",
            "reasoningProfile": "advanced",
            "rubricSha256": "rubric",
            "calibrationSetSha256": self.module.calibration_set_digest(samples),
        }
        record = {
            **expected,
            "status": "accepted",
            "samples": samples,
            "metrics": {
                "binaryF1": 1.0,
                "weightedKappa": 1.0,
                "criticalDefectRecall": 0.8,
                "sampleCount": 25,
            },
        }
        record["recordDigest"] = self.module.calibration_record_digest(record)
        errors = self.module.validate_calibration_record(record, expected)
        self.assertTrue(any("criticalDefectRecall" in error for error in errors))

    def test_calibration_rejects_fabricated_metrics(self) -> None:
        samples = _calibration_samples()
        expected = {
            "rubricId": "test-rubric",
            "judgePromptSha256": "prompt",
            "judgeOutputSchemaSha256": "schema",
            "instructionEnvelopeSha256": "envelope",
            "harness": "codex",
            "judgeModelIdentity": "model",
            "reasoningProfile": "advanced",
            "rubricSha256": "rubric",
            "calibrationSetSha256": self.module.calibration_set_digest(samples),
        }
        record = {
            **expected,
            "status": "accepted",
            "samples": samples,
            "metrics": {
                "binaryF1": 0.9,
                "weightedKappa": 1.0,
                "criticalDefectRecall": 1.0,
                "sampleCount": 25,
            },
        }
        record["recordDigest"] = self.module.calibration_record_digest(record)
        errors = self.module.validate_calibration_record(record, expected)
        self.assertIn("Model Judge calibration metric does not match samples: binaryF1", errors)

    def test_calibration_requires_twenty_five_samples_and_all_classes(self) -> None:
        with self.assertRaisesRegex(ValueError, "at least 25"):
            self.module.compute_calibration_metrics(_calibration_samples()[:2])
        samples = _calibration_samples()
        for sample in samples:
            if sample["sampleClass"] == "adversarially-polished":
                sample["sampleClass"] = "incomplete-plausible"
        with self.assertRaisesRegex(ValueError, "missing required classes"):
            self.module.compute_calibration_metrics(samples)

    def test_boundary_calibration_requires_two_humans_and_adjudicated_gold(self) -> None:
        samples = _calibration_samples()
        boundary = next(sample for sample in samples if sample["sampleClass"] == "boundary")
        boundary["humanJudgments"] = boundary["humanJudgments"][:1]
        with self.assertRaisesRegex(ValueError, "two independent Human Judges"):
            self.module.compute_calibration_metrics(samples)

    def test_calibration_requires_failed_and_critical_gold_examples(self) -> None:
        samples = _calibration_samples()
        for sample in samples:
            sample["criticalDefect"] = False
        with self.assertRaisesRegex(ValueError, "critical defect"):
            self.module.compute_calibration_metrics(samples)
        samples = _calibration_samples()
        for sample in samples:
            sample["humanLabel"] = "pass"
            sample["modelLabel"] = "pass"
            if sample["sampleClass"] == "boundary":
                sample["adjudication"]["label"] = "pass"
        samples[0]["humanLabel"] = "fail"
        samples[0]["modelLabel"] = "fail"
        with self.assertRaisesRegex(ValueError, "at least 2"):
            self.module.compute_calibration_metrics(samples)

    def test_calibration_set_digest_is_recomputed_from_samples(self) -> None:
        samples = _calibration_samples()
        expected = {
            "rubricId": "test-rubric",
            "judgePromptSha256": "prompt",
            "judgeOutputSchemaSha256": "schema",
            "instructionEnvelopeSha256": "envelope",
            "harness": "codex",
            "judgeModelIdentity": "model",
            "reasoningProfile": "advanced",
            "rubricSha256": "rubric",
            "calibrationSetSha256": self.module.calibration_set_digest(samples),
        }
        record = {
            **expected,
            "status": "accepted",
            "samples": samples,
            "metrics": self.module.compute_calibration_metrics(samples),
        }
        record["recordDigest"] = self.module.calibration_record_digest(record)
        record["samples"][0]["modelScore"] = 3
        record["recordDigest"] = self.module.calibration_record_digest(record)
        errors = self.module.validate_calibration_record(record, expected)
        self.assertTrue(any("calibrationSetSha256 does not match samples" in error for error in errors))

    def test_weighted_kappa_uses_the_fixed_zero_to_four_scale(self) -> None:
        samples = _calibration_samples()
        human_scores = [0, 1, 4, 0, 4] * 5
        model_scores = [0, 4, 1, 4, 4] * 5
        for sample, human_score, model_score in zip(samples, human_scores, model_scores):
            sample["humanScore"] = human_score
            sample["modelScore"] = model_score
            if sample["sampleClass"] == "boundary":
                for judgment in sample["humanJudgments"]:
                    judgment["score"] = human_score
                sample["adjudication"]["score"] = human_score
        metrics = self.module.compute_calibration_metrics(samples)
        self.assertAlmostEqual(0.0, metrics["weightedKappa"], places=12)
        samples[0]["humanScore"] = 5
        with self.assertRaisesRegex(ValueError, "0 through 4"):
            self.module.compute_calibration_metrics(samples)

    def test_cli_validates_calibration_from_labeled_samples(self) -> None:
        samples = _calibration_samples()
        rubric = self.module.load_framework_catalogs()["judges.yaml"]["rubrics"][0]
        identity = self.module.canonical_judge_identity(rubric)
        record = {
            "rubricId": rubric["id"],
            **identity,
            "harness": "codex",
            "judgeModelIdentity": "model",
            "reasoningProfile": "advanced",
            "calibrationSetSha256": self.module.calibration_set_digest(samples),
            "status": "accepted",
            "samples": samples,
            "metrics": {
                "binaryF1": 1.0,
                "weightedKappa": 1.0,
                "criticalDefectRecall": 1.0,
                "sampleCount": 25,
            },
        }
        record["recordDigest"] = self.module.calibration_record_digest(record)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "calibration.yaml"
            path.write_text(yaml.safe_dump(record), encoding="utf-8")
            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = self.module.main(["--validate-calibration", str(path)])
        self.assertEqual(0, exit_code)
        self.assertIn('"calibration": "diagnostic-valid"', output.getvalue())
        self.assertIn('"promotionEligible": false', output.getvalue())

    def test_deterministic_judge_failure_short_circuits_model_judge(self) -> None:
        calls: list[str] = []

        def deterministic() -> object:
            calls.append("deterministic")
            return self.module.JudgeResult("deterministic", "failed", "deterministic.json#failure")

        def model() -> object:
            calls.append("model")
            return self.module.JudgeResult("model", "passed", "model.json#pass")

        result = self.module.run_judge_pipeline([deterministic], model)
        self.assertEqual(["deterministic"], calls)
        self.assertEqual("skipped-deterministic-failure", result.model_status)

    def test_noncritical_deterministic_failure_does_not_skip_model_judge(self) -> None:
        calls: list[str] = []

        def noncritical() -> object:
            calls.append("noncritical")
            return self.module.JudgeResult(
                "deterministic", "failed", "deterministic.json#failure", check_id="style", critical=False,
            )

        def passing() -> object:
            calls.append("passing")
            return self.module.JudgeResult(
                "deterministic", "passed", "deterministic.json#pass", check_id="tests", critical=True,
            )

        def model() -> object:
            calls.append("model")
            return self.module.JudgeResult("model", "passed", "model.json#pass")

        result = self.module.run_judge_pipeline([noncritical, passing], model)
        self.assertEqual(["noncritical", "passing", "model"], calls)
        self.assertEqual("passed", result.model_status)

    def test_judge_plan_requires_every_known_check_with_catalog_criticality(self) -> None:
        validation_module = sys.modules[self.module.validate_evidence.__module__]
        case = {
            "judgePlan": {"deterministicChecks": ["check-a", "check-b"], "modelRubric": None},
        }
        catalog = {
            "judges.yaml": {
                "checks": [
                    {"id": "check-a", "critical": True},
                    {"id": "check-b", "critical": False},
                ],
                "rubrics": [],
            },
        }
        judges = {
            "deterministic": {
                "verdict": "passed",
                "records": [{
                    "checkId": "check-a",
                    "critical": False,
                    "verdict": "passed",
                    "evidence": "judges.txt#check-a",
                }],
            },
            "model": {"status": "not-required"},
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            evidence_path = root / "evidence.yaml"
            evidence_path.write_text("receipt\n", encoding="utf-8")
            (root / "judges.txt").write_text("check-a\n", encoding="utf-8")
            errors: list[str] = []
            with mock.patch.object(validation_module, "load_framework_catalogs", return_value=catalog):
                validation_module._validate_judges(case, judges, evidence_path, errors, [])
        self.assertTrue(any("missing required check: check-b" in error for error in errors))
        self.assertTrue(any("critical flag does not match" in error for error in errors))

    def test_model_rubric_cannot_be_bypassed_and_low_dimensions_do_not_compensate(self) -> None:
        validation_module = sys.modules[self.module.validate_evidence.__module__]
        case = {
            "judgePlan": {"deterministicChecks": ["check-a"], "modelRubric": "quality"},
        }
        catalog = {
            "judges.yaml": {
                "checks": [{"id": "check-a", "critical": True}],
                "rubrics": [{
                    "id": "quality",
                    "dimensions": ["correctness", "completeness"],
                    "passRules": {"noAggregateCompensation": True, "minimumDimensionScore": 3},
                }],
            },
        }
        deterministic = {
            "verdict": "passed",
            "records": [{
                "checkId": "check-a",
                "critical": True,
                "verdict": "passed",
                "evidence": "judges.txt#check-a",
            }],
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            evidence_path = root / "evidence.yaml"
            evidence_path.write_text("receipt\n", encoding="utf-8")
            (root / "judges.txt").write_text("check-a\ncorrectness\ncompleteness\n", encoding="utf-8")
            bypass_errors: list[str] = []
            with mock.patch.object(validation_module, "load_framework_catalogs", return_value=catalog):
                validation_module._validate_judges(
                    case,
                    {"deterministic": deterministic, "model": {"status": "not-required"}},
                    evidence_path,
                    bypass_errors,
                    [],
                )
            low_score_model = {
                "status": "passed",
                "rubricId": "quality",
                "dimensionScores": [
                    {
                        "id": "correctness",
                        "score": 4,
                        "critical": False,
                        "evidenceReferences": [{"documentId": "candidate-output", "locator": "correctness"}],
                        "rationale": "Correct claims are supported.",
                    },
                    {
                        "id": "completeness",
                        "score": 2,
                        "critical": False,
                        "evidenceReferences": [{"documentId": "candidate-output", "locator": "completeness"}],
                        "rationale": "Required content is missing.",
                    },
                ],
                "overall": {"verdict": "pass", "criticalFailure": False},
            }
            low_errors: list[str] = []
            with mock.patch.object(validation_module, "load_framework_catalogs", return_value=catalog):
                validation_module._validate_judges(
                    case,
                    {"deterministic": deterministic, "model": low_score_model},
                    evidence_path,
                    low_errors,
                    [],
                )
        self.assertIn("case requires a passed Model Judge", bypass_errors)
        self.assertTrue(any("status must be failed" in error for error in low_errors))

    def test_model_receipt_must_match_canonical_judge_artifacts(self) -> None:
        """Receipt summaries cannot replace the bound canonical Judge request and output."""
        validation_module = sys.modules[self.module.validate_evidence.__module__]
        rubric = {
            "id": "quality",
            "type": "model",
            "scale": "0-to-4-per-dimension",
            "dimensions": ["correctness"],
            "passRules": {
                "noAggregateCompensation": True,
                "minimumDimensionScore": 3,
            },
        }
        request = judge_contract.build_judge_request(
            case_id="canonical-model-receipt",
            run_id="run-canonical-model-receipt",
            harness="codex",
            rubric=rubric,
            candidate_output="The requirement is satisfied.",
            evidence={"requirements": "The candidate must satisfy the requirement."},
        )
        output = {
            "schema": "dev-methodology-model-judge-output",
            "version": 1,
            "contractVersion": judge_contract.CONTRACT_VERSION,
            "rubricId": "quality",
            "rubricSha256": request.rubric_sha256,
            "instructionEnvelopeSha256": request.instruction_envelope_sha256,
            "inputManifestSha256": request.input_manifest_sha256,
            "dimensionScores": [
                {
                    "id": "correctness",
                    "score": 3,
                    "critical": False,
                    "evidenceReferences": [
                        {"documentId": "requirements", "locator": "sentence:1"}
                    ],
                    "rationale": "The supplied requirement supports the conclusion.",
                }
            ],
            "overall": {"verdict": "pass", "criticalFailure": False},
        }
        model = {
            "status": "passed",
            "caseId": "canonical-model-receipt",
            "evaluatedRunId": "run-canonical-model-receipt",
            "evaluatedHarness": "codex",
            "contractVersion": judge_contract.CONTRACT_VERSION,
            "rubricId": "quality",
            "rubricSha256": request.rubric_sha256,
            "judgePromptSha256": request.prompt_sha256,
            "judgeOutputSchemaSha256": request.output_schema_sha256,
            "instructionEnvelopeSha256": request.instruction_envelope_sha256,
            "inputManifestSha256": request.input_manifest_sha256,
            "candidateOutputSha256": hashlib.sha256(
                b"The requirement is satisfied."
            ).hexdigest(),
            "candidateOutputEvidence": "candidate.txt#requirement",
            "governedEvidence": [
                {
                    "documentId": "requirements",
                    "sha256": hashlib.sha256(
                        b"The candidate must satisfy the requirement."
                    ).hexdigest(),
                    "evidence": "requirements.txt#candidate",
                }
            ],
            "dimensionScores": output["dimensionScores"],
            "overall": output["overall"],
            "contractArtifacts": {
                "instructionEnvelopeEvidence": "instructions.json#model-judge-v1",
                "inputManifestEvidence": "manifest.json#model-judge-v1",
                "outputEvidence": "output.json#model-judge-v1",
            },
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            evidence_path = root / "evidence.yaml"
            evidence_path.write_text("receipt\n", encoding="utf-8")
            (root / "candidate.txt").write_text(
                "The requirement is satisfied.", encoding="utf-8"
            )
            (root / "requirements.txt").write_text(
                "The candidate must satisfy the requirement.", encoding="utf-8"
            )
            (root / "instructions.json").write_bytes(
                request.instruction_envelope_bytes
            )
            (root / "manifest.json").write_bytes(request.input_manifest_bytes)
            (root / "output.json").write_bytes(
                judge_contract.canonical_json_bytes(output)
            )
            errors: list[str] = []
            validation_module._validate_canonical_model_contract(
                model,
                rubric,
                {"id": "canonical-model-receipt"},
                {"id": "run-canonical-model-receipt", "harness": "codex"},
                evidence_path,
                errors,
            )
            self.assertEqual([], errors)
            stale_summary = dict(model)
            stale_summary["inputManifestSha256"] = "0" * 64
            stale_errors: list[str] = []
            validation_module._validate_canonical_model_contract(
                stale_summary,
                rubric,
                {"id": "canonical-model-receipt"},
                {"id": "run-canonical-model-receipt", "harness": "codex"},
                evidence_path,
                stale_errors,
            )
            replay_errors: list[str] = []
            validation_module._validate_canonical_model_contract(
                model,
                rubric,
                {"id": "wrong-case"},
                {"id": "wrong-run", "harness": "junie"},
                evidence_path,
                replay_errors,
            )
            (root / "candidate.txt").write_text(
                "A different candidate output.", encoding="utf-8"
            )
            candidate_errors: list[str] = []
            validation_module._validate_canonical_model_contract(
                model,
                rubric,
                {"id": "canonical-model-receipt"},
                {"id": "run-canonical-model-receipt", "harness": "codex"},
                evidence_path,
                candidate_errors,
            )
        self.assertTrue(
            any("inputManifestSha256" in error for error in stale_errors)
        )
        self.assertTrue(any("case" in error.lower() for error in replay_errors))
        self.assertTrue(any("run" in error.lower() for error in replay_errors))
        self.assertTrue(any("harness" in error.lower() for error in replay_errors))
        self.assertTrue(any("candidate" in error.lower() for error in candidate_errors))


if __name__ == "__main__":
    unittest.main()
