# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Modified with AI assistance.
# Summary: Verifies receipt-backed agent and skill evaluation evidence contracts.

from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import os
import shutil
import sys
import threading
import tempfile
import time
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

    def test_successful_command_terminates_remaining_process_group_members(self) -> None:
        child_pid: int | None = None
        try:
            with tempfile.TemporaryDirectory() as directory:
                script = (
                    "import subprocess, sys\n"
                    "child = subprocess.Popen("
                    "[sys.executable, '-c', 'import time; time.sleep(60)'], "
                    "stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)\n"
                    "print(child.pid, flush=True)\n"
                )
                result = self.module.run_command(
                    self.module.command_spec([sys.executable, "-c", script]),
                    Path(directory),
                )
            self.assertTrue(result.passed)
            child_pid = int(result.stdout.strip())
            for _ in range(100):
                try:
                    os.kill(child_pid, 0)
                except ProcessLookupError:
                    break
                time.sleep(0.01)
            else:
                self.fail("successful command left a child process running")
        finally:
            if child_pid is not None:
                try:
                    os.kill(child_pid, 9)
                except ProcessLookupError:
                    pass

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
                    "mode": next(
                        profile
                        for profile in self.module.load_framework_catalogs()[
                            "sandbox-profiles.yaml"
                        ]["profiles"]
                        if profile["id"] == self.case["sandboxProfiles"]["codex"]
                    )["copyOnWriteWorkspace"]["productWorkspaceMode"],
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

    def junie_receipt(self) -> dict[str, object]:
        receipt = self.receipt()
        adapter_identity = self.module.build_agent_evidence_identity(
            "junie", "dev-coder"
        )
        receipt["captureProvenance"]["kind"] = "local-runner"
        receipt["run"].update({
            "harness": "junie",
            "harnessVersion": "Junie test",
            **adapter_identity,
        })
        receipt["skills"] = [
            {
                **self.module.build_skill_evidence_identity(
                    self.case, "junie", skill
                ),
                "readEvidence": [{
                    "type": "tool-call",
                    "reference": f"events.jsonl#read-{skill}",
                }],
            }
            for skill in self.case["requiredSkills"]
        ]
        profile_id = self.case["sandboxProfiles"]["junie"]
        profile = next(
            item
            for item in self.module.load_framework_catalogs()[
                "sandbox-profiles.yaml"
            ]["profiles"]
            if item["id"] == profile_id
        )
        receipt["isolation"] = {
            "workspacePreparation": "copy-on-write",
            "sandboxProfile": profile_id,
            "sandboxProfileDigest": self.module.case_definition_digest(profile),
            "sandboxProfileEvidence": "isolation.json#sandbox-profile",
            "functional": receipt["isolation"]["functional"],
            "containment": {
                "level": "containment-unverified",
                "status": "unverified",
                "enforcedBy": "local-runner",
            },
        }
        return receipt

    def classify(
        self,
        receipt: dict[str, object],
        *,
        include_agent_start: bool = True,
        case: dict[str, object] | None = None,
        extra_files: dict[str, bytes | str] | None = None,
    ) -> object:
        selected_case = case or self.case
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "evidence.yaml"
            run = receipt["run"]
            harness = run.get("harness", "codex")
            events = [{
                "id": "ledger-start",
                "type": "ledger",
            }, {
                "id": "invocation",
                "type": "invocation",
                "agent": "dev-coder",
                "harness": harness,
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
            } for skill in selected_case["requiredSkills"])
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
            for name, content in (extra_files or {}).items():
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                if isinstance(content, bytes):
                    target.write_bytes(content)
                else:
                    target.write_text(content, encoding="utf-8")
            path.write_text(yaml.safe_dump(receipt), encoding="utf-8")
            return self.module.classify_evidence(selected_case, path)

    def test_local_receipt_reports_execution_judge_and_security_claims_independently(self) -> None:
        classification = self.classify(self.receipt())
        self.assertTrue(classification.executed)
        self.assertTrue(classification.judge_passed)
        self.assertFalse(classification.security_contained)
        self.assertEqual("not-required", classification.judge_calibration_status)
        self.assertFalse(classification.stale_by_digest)

    def test_recorded_receipt_label_does_not_override_derived_claims(self) -> None:
        receipt = self.receipt()
        receipt["verdict"] = "recorded"
        classification = self.classify(receipt)
        self.assertTrue(classification.executed)
        self.assertTrue(classification.judge_passed)
        self.assertFalse(classification.security_contained)
        self.assertFalse(any("receipt verdict" in item for item in classification.errors))

    def test_failed_judge_does_not_erase_a_captured_execution(self) -> None:
        receipt = self.receipt()
        receipt["judges"]["deterministic"]["verdict"] = "failed"
        receipt["judges"]["deterministic"]["records"][0]["verdict"] = "failed"
        receipt["judges"]["model"] = {"status": "skipped-deterministic-failure"}
        classification = self.classify(receipt)
        self.assertTrue(classification.executed)
        self.assertFalse(classification.judge_passed)
        self.assertFalse(classification.security_contained)

    def test_invalid_governed_evidence_cannot_receive_judge_credit(self) -> None:
        receipt = self.receipt()
        receipt["verdict"] = "recorded"
        receipt["skills"][0]["readEvidence"] = []
        classification = self.classify(receipt)
        self.assertTrue(classification.executed)
        self.assertFalse(classification.judge_passed)
        self.assertTrue(any(
            "missing skill read tool evidence" in item
            for item in classification.errors
        ))

    def test_ordinary_local_junie_receipt_needs_no_external_containment_mapping(self) -> None:
        classification = self.classify(self.junie_receipt())
        self.assertTrue(classification.executed)
        self.assertTrue(classification.judge_passed)
        self.assertFalse(classification.security_contained)
        self.assertFalse(any(
            "junieExternalContainment" in item for item in classification.errors
        ))
        self.assertFalse(any(
            "captureProvenance.kind" in item for item in classification.errors
        ))

    def test_failed_model_judge_is_not_reported_as_calibrated(self) -> None:
        case = dict(self.case)
        case["judgePlan"] = {
            "deterministicChecks": ["required-command-outcome"],
            "modelRubric": "artifact-contract",
        }
        receipt = self.receipt()
        receipt["run"]["caseDefinitionDigest"] = self.module.case_definition_digest(case)
        receipt["judges"]["model"] = {"status": "failed"}
        classification = self.classify(receipt, case=case)
        self.assertTrue(classification.executed)
        self.assertFalse(classification.judge_passed)
        self.assertEqual("pending", classification.judge_calibration_status)

    def test_passed_model_judge_is_accepted_while_calibration_remains_pending(self) -> None:
        rubric = next(
            item
            for item in self.module.load_framework_catalogs()["judges.yaml"]["rubrics"]
            if item["id"] == "artifact-contract"
        )
        case = dict(self.case)
        case["judgePlan"] = {
            "deterministicChecks": ["required-command-outcome"],
            "modelRubric": rubric["id"],
        }
        candidate = "The artifact satisfies the governed requirements."
        requirements = "The governed requirements define the acceptance boundary."
        request = judge_contract.build_judge_request(
            case_id=str(case["id"]),
            run_id="run-1",
            harness="codex",
            rubric=rubric,
            candidate_output=candidate,
            evidence={"requirements": requirements},
        )
        critical_dimensions = set(rubric["passRules"]["criticalDimensions"])
        dimension_scores = [
            {
                "id": dimension["id"],
                "score": 4,
                "critical": dimension["id"] in critical_dimensions,
                "evidenceReferences": [
                    {"documentId": "requirements", "locator": "sentence:1"}
                ],
                "rationale": "The governed evidence supports this dimension.",
            }
            for dimension in rubric["dimensions"]
        ]
        output = {
            "schema": "dev-methodology-model-judge-output",
            "version": 1,
            "contractVersion": judge_contract.CONTRACT_VERSION,
            "rubricId": rubric["id"],
            "rubricSha256": request.rubric_sha256,
            "instructionEnvelopeSha256": request.instruction_envelope_sha256,
            "inputManifestSha256": request.input_manifest_sha256,
            "dimensionScores": dimension_scores,
            "overall": {"verdict": "pass", "criticalFailure": False},
        }
        receipt = self.receipt()
        receipt["run"]["caseDefinitionDigest"] = self.module.case_definition_digest(case)
        receipt["judges"]["model"] = {
            "status": "passed",
            "caseId": case["id"],
            "evaluatedRunId": "run-1",
            "evaluatedHarness": "codex",
            "contractVersion": judge_contract.CONTRACT_VERSION,
            "rubricId": rubric["id"],
            "rubricSha256": request.rubric_sha256,
            "judgePromptSha256": request.prompt_sha256,
            "judgeOutputSchemaSha256": request.output_schema_sha256,
            "instructionEnvelopeSha256": request.instruction_envelope_sha256,
            "inputManifestSha256": request.input_manifest_sha256,
            "candidateOutputSha256": hashlib.sha256(candidate.encode("utf-8")).hexdigest(),
            "candidateOutputEvidence": "candidate.txt#artifact",
            "governedEvidence": [{
                "documentId": "requirements",
                "sha256": hashlib.sha256(requirements.encode("utf-8")).hexdigest(),
                "evidence": "requirements.txt#requirements",
            }],
            "dimensionScores": dimension_scores,
            "overall": output["overall"],
            "judgeModelIdentity": "judge-model-1",
            "judgeModelIdentityEvidence": "judge-model.txt#judge-model-1",
            "reasoningProfile": "independent",
            "reasoningProfileEvidence": "reasoning.txt#independent",
            "judgePromptEvidence": "judge-prompt.txt#Model Judge Contract Version 1",
            "evidence": "output.json#model-judge-v1",
            "contractArtifacts": {
                "instructionEnvelopeEvidence": "instructions.json#model-judge-v1",
                "inputManifestEvidence": "manifest.json#model-judge-v1",
                "outputEvidence": "output.json#model-judge-v1",
            },
        }
        receipt["independentJudge"].update({
            "kind": "Model Judge",
            "judgePromptSha256": request.prompt_sha256,
            "judgePromptEvidence": "judge-prompt.txt#Model Judge Contract Version 1",
            "inputManifestDigest": request.input_manifest_sha256,
        })
        classification = self.classify(
            receipt,
            case=case,
            extra_files={
                "candidate.txt": candidate,
                "requirements.txt": requirements,
                "instructions.json": request.instruction_envelope_bytes,
                "manifest.json": request.input_manifest_bytes,
                "output.json": judge_contract.canonical_json_bytes(output),
                "judge-prompt.txt": judge_contract.PROMPT_PATH.read_bytes(),
                "judge-model.txt": "judge-model-1\n",
                "reasoning.txt": "independent\n",
            },
        )
        self.assertTrue(classification.executed)
        self.assertTrue(classification.judge_passed, classification)
        self.assertEqual("pending", classification.judge_calibration_status)
        self.assertEqual((), classification.errors)

    def test_agent_source_drift_is_classified_separately(self) -> None:
        receipt = self.receipt()
        receipt["run"]["conceptualAgentDigest"] = "f" * 64
        classification = self.classify(receipt)
        self.assertTrue(classification.executed)
        self.assertFalse(classification.verified)
        self.assertTrue(classification.stale_by_digest)
        self.assertTrue(any("conceptual agent digest mismatch" in item for item in classification.stale_reasons))

    def test_external_runner_required_case_cannot_promote_local_receipt(self) -> None:
        high_risk_case = dict(self.case)
        high_risk_case["risk"] = {
            "level": "high",
            "reasons": ["executes an untrusted repository hook"],
        }
        high_risk_case["executionTier"] = "externally-contained"
        high_risk_case["securityContainmentRequired"] = True
        high_risk_case["harnessExecutionStatus"] = {
            "codex": "external-runner-required",
            "junie": "external-runner-required",
        }
        receipt = self.receipt()
        receipt["captureProvenance"]["kind"] = "trusted-ci"
        receipt["run"]["caseDefinitionDigest"] = self.module.case_definition_digest(
            high_risk_case
        )
        classification = self.classify(receipt, case=high_risk_case)
        self.assertTrue(classification.executed)
        self.assertTrue(classification.judge_passed)
        self.assertFalse(classification.verified)
        self.assertFalse(classification.security_contained)
        self.assertTrue(
            any("governed external verification" in item for item in classification.errors)
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

    def test_junie_event_stream_must_be_valid_and_exposes_the_final_result(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "junie.jsonl"
            with self.assertRaisesRegex(ValueError, "missing"):
                self.module.read_harness_event_stream("junie", path)
            path.write_text("\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "empty"):
                self.module.read_harness_event_stream("junie", path)
            path.write_text('{"kind":"AgentStartedEvent"}\nnot-json\n', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "line 2"):
                self.module.read_harness_event_stream("junie", path)
            target = Path(directory) / "target.jsonl"
            target.write_text('{"type":"result","result":"done"}\n', encoding="utf-8")
            path.unlink()
            path.symlink_to(target)
            with self.assertRaisesRegex(ValueError, "non-symlink"):
                self.module.read_harness_event_stream("junie", path)
            path.unlink()
            path.write_bytes(b"x" * (10 * 1024 * 1024 + 1))
            with self.assertRaisesRegex(ValueError, "capture limit"):
                self.module.read_harness_event_stream("junie", path)
            path.write_text(
                "\n".join(
                    (
                        json.dumps({"type": "session", "sessionId": "session-1"}),
                        json.dumps({
                            "type": "result",
                            "result": "## Skills Used\n\ncareful-coding",
                        }),
                    )
                )
                + "\n",
                encoding="utf-8",
            )
            events = self.module.read_harness_event_stream("junie", path)
        self.assertEqual(2, len(events))
        self.assertEqual(
            "## Skills Used\n\ncareful-coding",
            self.module.extract_harness_final_response("junie", events),
        )

    def test_junie_final_response_requires_a_result_event(self) -> None:
        with self.assertRaisesRegex(ValueError, "final result"):
            self.module.extract_harness_final_response(
                "junie", [{"type": "step", "message": "working"}]
            )
        with self.assertRaisesRegex(ValueError, "exactly one"):
            self.module.extract_harness_final_response(
                "junie",
                [
                    {"type": "result", "result": "first"},
                    {"type": "result", "result": "second"},
                ],
            )
        with self.assertRaisesRegex(ValueError, "terminal"):
            self.module.extract_harness_final_response(
                "junie",
                [
                    {"type": "result", "result": "done"},
                    {"type": "system", "message": "late"},
                ],
            )

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
            self.assertNotIn("--ephemeral", codex.argv)
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
            self.assertIn("JUNIE_HOME", junie.environment)
            self.assertNotEqual(junie.environment["HOME"], junie.environment["JUNIE_HOME"])
            self.assertTrue(
                str(evidence_root.resolve()) in junie.environment["JUNIE_HOME"]
            )
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

    def test_harness_identity_pins_the_managed_junie_runtime(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shim = root / "bin" / "junie"
            shim.parent.mkdir()
            shim.write_text(
                "#!/bin/sh\n# JUNIE_MANAGED_SHIM\nexit 99\n", encoding="utf-8"
            )
            shim.chmod(0o700)
            data = root / "share" / "junie"
            version = data / "versions" / "test-version"
            version.mkdir(parents=True)
            concrete = version / "junie"
            concrete.write_text(
                "#!/bin/sh\n"
                "[ -n \"${JUNIE_HOME:-}\" ] || exit 42\n"
                "[ \"${HOME:-}\" != \"${HOST_HOME_SENTINEL:-}\" ] || exit 43\n"
                "printf 'Junie version: test-version\\n'\n",
                encoding="utf-8",
            )
            concrete.chmod(0o700)
            (data / "current").symlink_to(version, target_is_directory=True)
            concrete_digest = digest(concrete)
            self.module.capture_harness_identity.cache_clear()
            try:
                with mock.patch.object(
                    self.module.shutil, "which", return_value=str(shim)
                ), mock.patch.dict(
                    os.environ,
                    {
                        "JUNIE_DATA": str(data),
                        "HOST_HOME_SENTINEL": os.environ.get("HOME", "host-home"),
                    },
                    clear=False,
                ):
                    identity = self.module.capture_harness_identity("junie")
            finally:
                self.module.capture_harness_identity.cache_clear()
        self.assertEqual(concrete.resolve(), identity.executable)
        self.assertEqual("Junie version: test-version", identity.version)
        self.assertEqual(concrete_digest, identity.content_digest)

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

    def test_case_risk_selects_local_or_external_execution_without_implicit_escalation(self) -> None:
        ordinary = dict(self.module.load_cases()["typescript-order-pricing"])
        ordinary.pop("postRunVerificationStatus", None)
        ordinary.pop("minimumContainment", None)
        ordinary.update({
            "risk": {"level": "ordinary", "reasons": []},
            "executionTier": "local",
            "securityContainmentRequired": False,
            "harnessExecutionStatus": {"codex": "runnable", "junie": "runnable"},
        })
        self.assertEqual([], self.module.validate_case_definition(ordinary))

        high_without_reason = {
            **ordinary,
            "risk": {"level": "high", "reasons": []},
            "executionTier": "externally-contained",
            "securityContainmentRequired": True,
            "harnessExecutionStatus": {
                "codex": "external-runner-required",
                "junie": "external-runner-required",
            },
        }
        self.assertTrue(any(
            "high-risk case must declare at least one reason" in error
            for error in self.module.validate_case_definition(high_without_reason)
        ))

        high_on_local_tier = {
            **high_without_reason,
            "risk": {"level": "high", "reasons": ["untrusted-third-party-code"]},
            "executionTier": "local",
            "securityContainmentRequired": False,
            "harnessExecutionStatus": {"codex": "runnable", "junie": "runnable"},
        }
        self.assertTrue(any(
            "high-risk case must use the externally-contained tier" in error
            for error in self.module.validate_case_definition(high_on_local_tier)
        ))

        ordinary_on_external_tier = {
            **ordinary,
            "executionTier": "externally-contained",
            "securityContainmentRequired": True,
            "harnessExecutionStatus": {
                "codex": "external-runner-required",
                "junie": "external-runner-required",
            },
        }
        self.assertTrue(any(
            "ordinary case must use the local tier" in error
            for error in self.module.validate_case_definition(ordinary_on_external_tier)
        ))

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
            mutation = self.module.build_harness_command(
                "codex",
                root,
                "dev-coder",
                "Implement the change",
                "test-model",
                read_only=False,
                event_output=evidence_root / "mutation-events.jsonl",
                evidence_root=evidence_root,
                isolated_config_root=root,
                last_message_output=evidence_root / "mutation-result.md",
            )
            self.assertIn("--output-last-message", mutation.argv)
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

    def test_codex_authentication_uses_an_ephemeral_auth_only_home(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            workspace = base / "workspace"
            evidence = base / "evidence"
            evidence.mkdir()
            (workspace / ".codex" / "agents").mkdir(parents=True)
            (workspace / ".codex" / "agents" / "dev-coder.toml").write_text(
                'name = "dev-coder"\n',
                encoding="utf-8",
            )
            (workspace / ".agents" / "skills").mkdir(parents=True)
            auth_source = base / "auth.json"
            auth_source.write_text('{"auth_mode":"test"}\n', encoding="utf-8")
            auth_source.chmod(0o600)
            content = self.module._load_codex_auth_file(
                auth_source,
                workspace,
                evidence,
            )
            self.assertEqual(auth_source.read_bytes(), content)
            isolated_home = evidence / ".codex-home-test"
            command = self.module.build_harness_command(
                "codex",
                workspace,
                "dev-coder",
                "Do the task",
                "test-model",
                read_only=False,
                event_output=evidence / "events.jsonl",
                evidence_root=evidence,
                isolated_config_root=workspace,
                codex_home=isolated_home,
            )
            self.assertEqual(
                str(isolated_home.resolve()),
                command.environment["CODEX_HOME"],
            )
            self.assertNotIn(str(auth_source), json.dumps(command.environment))
            auth_source.chmod(0o644)
            with self.assertRaisesRegex(ValueError, "group or other"):
                self.module._load_codex_auth_file(
                    auth_source,
                    workspace,
                    evidence,
                )

    def test_junie_read_only_result_path_is_runner_owned(self) -> None:
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
                "Review the source",
                "test-model",
                read_only=True,
                event_output=evidence_root / "events.jsonl",
                evidence_root=evidence_root,
                isolated_config_root=root,
                last_message_output=evidence_root / "review.md",
                skill_locations=[root / ".junie" / "skills"],
                agent_locations=[root / ".junie" / "agents"],
            )
            self.assertIn("--output-format=json-stream", command.argv)
            with self.assertRaisesRegex(ValueError, "runner-owned evidence root"):
                self.module.build_harness_command(
                    "junie",
                    root,
                    "dev-coder",
                    "Review the source",
                    "test-model",
                    read_only=True,
                    event_output=evidence_root / "events.jsonl",
                    evidence_root=evidence_root,
                    isolated_config_root=root,
                    last_message_output=root / "review.md",
                    skill_locations=[root / ".junie" / "skills"],
                    agent_locations=[root / ".junie" / "agents"],
                )

    def test_local_junie_run_writes_result_and_cleans_run_scratch(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "workspace"
            root.mkdir()
            (root / "TASK.md").write_text("Return the requested evidence packet.\n", encoding="utf-8")
            (root / ".eval-workspace.json").write_text("{}\n", encoding="utf-8")
            evidence_root = base / "dev-methodology-evals" / "evidence"
            result_path = evidence_root / "review.md"
            event_path = evidence_root / "events.jsonl"
            case = dict(self.module.load_cases()["typescript-order-pricing"])
            case.update({
                "id": "junie-handler-test",
                "task": "TASK.md",
                "readOnly": True,
                "allowedWritePaths": [],
                "ephemeralWritePaths": [],
                "modelVisiblePaths": ["TASK.md"],
            })
            args = self.module._argument_parser().parse_args([
                "--case",
                case["id"],
                "--harness",
                "junie",
                "--invoke-harness",
                "--result",
                str(result_path),
                "--event-output",
                str(event_path),
                "--approved-env-name",
                "EVAL_API_TOKEN",
            ])
            identity = self.module.HarnessIdentity(
                "junie",
                Path(sys.executable),
                "Junie test",
                digest(Path(sys.executable)),
            )
            observed_cache: list[Path] = []
            observed_scratch: list[Path] = []
            observed_junie_home: list[Path] = []
            secret = "eval-secret-token-123456"

            def capture(command: object, cwd: Path) -> object:
                cache = Path(next(
                    item.split("=", 1)[1]
                    for item in command.argv
                    if item.startswith("--cache-dir=")
                ))
                scratch = Path(command.environment["TMPDIR"])
                junie_home = Path(command.environment["JUNIE_HOME"])
                cache.mkdir(parents=True)
                scratch.mkdir(parents=True, exist_ok=True)
                junie_home.mkdir(parents=True, exist_ok=True)
                (cache / "state").write_text("temporary\n", encoding="utf-8")
                (junie_home / "state").write_text("temporary\n", encoding="utf-8")
                observed_cache.append(cache)
                observed_scratch.append(scratch)
                observed_junie_home.append(junie_home)
                event_path.parent.mkdir(parents=True, exist_ok=True)
                event_path.write_text(
                    json.dumps({
                        "type": "result",
                        "result": f"## Skills Used\n\ncareful-coding\n\ntoken={secret}\n",
                    })
                    + "\n",
                    encoding="utf-8",
                )
                return self.module.CommandResult(
                    command.argv,
                    0,
                    "",
                    f"diagnostic token={secret}\n",
                )

            captured_stderr = io.StringIO()
            with mock.patch.dict(
                os.environ, {"EVAL_API_TOKEN": secret}
            ), mock.patch.object(
                self.module.tempfile, "gettempdir", return_value=str(base)
            ), mock.patch.object(
                self.module, "capture_harness_identity", return_value=identity
            ), mock.patch.object(
                self.module, "run_command", side_effect=capture
            ), redirect_stderr(captured_stderr):
                error = self.module._handle_harness_invocation(args, case, root)
            self.assertIsNone(error)
            self.assertEqual(
                "## Skills Used\n\ncareful-coding\n\n"
                "token=[REDACTED_APPROVED_ENV:EVAL_API_TOKEN]\n",
                result_path.read_text(encoding="utf-8"),
            )
            self.assertTrue(event_path.is_file())
            self.assertNotIn(secret, event_path.read_text(encoding="utf-8"))
            self.assertNotIn(secret, captured_stderr.getvalue())
            self.assertIn(
                "[REDACTED_APPROVED_ENV:EVAL_API_TOKEN]",
                captured_stderr.getvalue(),
            )
            self.assertTrue(observed_cache)
            self.assertTrue(observed_scratch)
            self.assertTrue(observed_junie_home)
            self.assertFalse(observed_cache[0].exists())
            self.assertFalse(observed_scratch[0].exists())
            self.assertFalse(observed_junie_home[0].exists())

    def test_mcp_handler_preserves_governed_evidence_and_selects_agent_stream(self) -> None:
        case = self.module.load_cases()["project-configuration-routing"]
        contract = case["mcpAgentOps"]
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            workspace = base / "workspace"
            shutil.copytree(
                ROOT / case["project"],
                workspace,
            )
            (workspace / ".eval-workspace.json").write_text(
                "{}\n", encoding="utf-8"
            )
            evidence_root = base / "dev-methodology-evals" / "evidence"
            event_path = evidence_root / "events.jsonl"
            result_path = evidence_root / "result.md"
            args = self.module._argument_parser().parse_args([
                "--case",
                case["id"],
                "--harness",
                "codex",
                "--invoke-harness",
                "--event-output",
                str(event_path),
                "--result",
                str(result_path),
            ])
            identity = self.module.McpAgentOpsIdentity(
                Path(sys.executable).resolve(),
                contract["requiredVersion"],
                "1" * 64,
                contract["requiredRuntimeDigest"],
                "2" * 64,
            )
            harness_identity = self.module.HarnessIdentity(
                "codex",
                Path(sys.executable).resolve(),
                "Codex test",
                digest(Path(sys.executable)),
            )
            real_stage = self.module.stage_mcp_agent_ops_context
            staged: list[object] = []

            def stage(*stage_args: object, **stage_kwargs: object) -> object:
                context = real_stage(*stage_args, **stage_kwargs)
                staged.append(context)
                return context

            def execute(command: object, cwd: Path) -> object:
                context = staged[0]
                for relative in case["allowedWritePaths"]:
                    output = cwd / relative
                    output.parent.mkdir(parents=True, exist_ok=True)
                    output.write_text(f"synthetic output for {relative}\n", encoding="utf-8")
                result_path.write_text("synthetic final response\n", encoding="utf-8")
                outcome_by_tool = {
                    "skill_list": "CATALOG",
                    "skill_load": "LOADED",
                    "skill_resource_load": "LOADED",
                    "skill_validate": "VALID",
                    "skill_refresh": "CATALOG",
                    "detect_technology_skills": "NO_VARIANT",
                    "claim_acquire": "PRIMARY",
                    "claim_status": "STATUS",
                    "claim_extend": "EXTENDED",
                    "claim_heartbeat": "HEARTBEAT",
                    "verify_yaml": "OK",
                    "verify_markdown_links": "OK",
                    "claim_release": "RELEASED",
                }
                argument_digests = self.module.resolve_mcp_tool_argument_digests(
                    contract["requiredToolArguments"],
                    cwd,
                    skill_root=context.skill_root,
                )
                records: list[dict[str, object]] = []
                for index, (tool, outcome) in enumerate(outcome_by_tool.items(), start=1):
                    completed_record = {
                        "schema": "mcp-agent-ops-tool-audit",
                        "version": 2,
                        "sequence": len(records) + 2,
                        "streamId": "3" * 32,
                        "sessionId": context.audit_session_id,
                        "callId": str(index),
                        "tool": tool,
                        "status": "completed",
                        "resultDigest": "5" * 64,
                    }
                    if outcome is not None:
                        completed_record["outcome"] = outcome
                    records.extend((
                        {
                            "schema": "mcp-agent-ops-tool-audit",
                            "version": 2,
                            "sequence": len(records) + 1,
                            "streamId": "3" * 32,
                            "sessionId": context.audit_session_id,
                            "callId": str(index),
                            "tool": tool,
                            "status": "started",
                            "argumentsDigest": argument_digests[tool],
                        },
                        completed_record,
                    ))
                context.audit_log.write_text(
                    "\n".join(json.dumps(record) for record in records) + "\n",
                    encoding="utf-8",
                )
                return self.module.CommandResult(
                    command.argv,
                    0,
                    json.dumps({"type": "turn.completed"}) + "\n",
                    "",
                )

            captured = io.StringIO()
            with mock.patch.object(
                self.module.tempfile, "gettempdir", return_value=str(base)
            ), mock.patch.object(
                self.module,
                "capture_mcp_agent_ops_identity",
                return_value=identity,
            ), mock.patch.object(
                self.module,
                "capture_harness_identity",
                return_value=harness_identity,
            ), mock.patch.object(
                self.module,
                "stage_mcp_agent_ops_context",
                side_effect=stage,
            ), mock.patch.object(
                self.module,
                "run_command",
                side_effect=execute,
            ), redirect_stdout(captured):
                error = self.module._handle_harness_invocation(args, case, workspace)
            self.assertIsNone(error)
            self.assertEqual(1, len(staged))
            context = staged[0]
            manifest_path = context.evidence_directory / "outputs-manifest.json"
            self.assertTrue(manifest_path.is_file())
            evidence_records = [
                json.loads(line)
                for line in captured.getvalue().splitlines()
                if line.startswith("{")
            ]
            mcp_record = next(
                record["mcpAgentOps"]
                for record in evidence_records
                if "mcpAgentOps" in record
            )
            self.assertEqual("3" * 32, mcp_record["auditStreamId"])
            self.assertEqual("verified", mcp_record["toolEvidenceStatus"])
            self.assertEqual(
                contract["requiredToolOutcomes"],
                mcp_record["requiredToolOutcomes"],
            )
            self.assertEqual(
                self.module.resolve_mcp_tool_argument_digests(
                    contract["requiredToolArguments"],
                    workspace,
                    skill_root=context.skill_root,
                ),
                mcp_record["requiredToolArgumentDigests"],
            )
            self.assertEqual(
                self.module.mcp_value_digest(str(Path.home().resolve())),
                mcp_record["permissionProfileHostHomeDigest"],
            )
            shutil.rmtree(workspace)
            self.assertTrue(manifest_path.is_file())
            self.assertTrue(
                (context.evidence_directory / "outputs" / "PROJECT.yaml").is_file()
            )

    def test_junie_session_ledger_yields_name_level_not_digest_bound_attribution(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            junie_home = root / "junie-home"
            session = junie_home / "sessions" / "session-1"
            session.mkdir(parents=True)
            evidence = root / "evidence"
            evidence.mkdir()
            events: list[dict[str, object]] = []
            for status in ("STARTED", "STARTED", "FINISHED"):
                events.append({
                    "kind": "SessionA2uxEvent",
                    "event": {
                        "state": "IN_PROGRESS",
                        "agentEvent": {
                            "kind": "CustomAgentBlockUpdatedEvent",
                            "agent": {
                                "kind": "CustomAgent",
                                "id": "agent-1",
                                "name": "project-configurator",
                            },
                            "name": "project-configurator",
                            "status": status,
                            "stepId": "step-12345678",
                        },
                    },
                })
            (session / "events.jsonl").write_text(
                "\n".join(json.dumps(event) for event in events) + "\n",
                encoding="utf-8",
            )
            status, path, content_digest = self.module._preserve_junie_agent_attribution(
                junie_home,
                "project-configurator",
                evidence,
            )
            self.assertEqual("name-verified", status)
            self.assertEqual(digest(path), content_digest)
            payload = json.loads(path.read_text(encoding="utf-8"))
            self.assertFalse(payload["definitionDigestBound"])
            self.assertEqual(
                ["STARTED", "FINISHED"],
                payload["lifecycle"]["statuses"],
            )

    def test_capture_paths_are_exclusively_reserved_and_never_overwritten(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "events.jsonl"
            with self.module._reserve_capture_paths([output]):
                with self.assertRaisesRegex(ValueError, "already reserved"):
                    with self.module._reserve_capture_paths([output]):
                        pass
            output.write_text("existing evidence\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "already exists"):
                with self.module._reserve_capture_paths([output]):
                    pass
            self.assertEqual(
                "existing evidence\n",
                output.read_text(encoding="utf-8"),
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

    def test_junie_local_command_uses_the_pinned_harness_directly(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "workspace"
            evidence_root = base / "evidence"
            evidence_root.mkdir()
            (root / ".junie" / "agents").mkdir(parents=True)
            (root / ".junie" / "skills").mkdir(parents=True)
            executable = base / "junie-runtime"
            executable.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            executable.chmod(0o700)
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
                harness_executable=executable,
            )
        self.assertEqual(str(executable.resolve()), command.argv[0])
        self.assertTrue(any(item.startswith("--project=") for item in command.argv))
        self.assertFalse(any("attestation" in item for item in command.argv))

    def test_cli_runs_standard_junie_locally_and_blocks_high_risk_cases(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "TASK.md").write_text("Synthetic task.\n", encoding="utf-8")
            standard_case = {
                "id": "local-junie",
                "project": "evals/projects/local-junie",
                "task": "TASK.md",
                "verify": ["true"],
                "risk": {"level": "ordinary", "reasons": []},
                "executionTier": "local",
                "securityContainmentRequired": False,
                "harnesses": ["codex", "junie"],
                "harnessExecutionStatus": {"codex": "runnable", "junie": "runnable"},
                "requiredAgents": ["dev-coder"],
                "requiredSkills": ["careful-coding"],
                "requiredEvidence": ["SAFE"],
                "allowedWritePaths": [],
                "ephemeralWritePaths": [],
                "modelVisiblePaths": ["TASK.md"],
            }
            with mock.patch.object(
                self.module, "load_cases", return_value={standard_case["id"]: standard_case}
            ), mock.patch.object(
                self.module, "_workspace_manager", return_value=None
            ), mock.patch.object(
                self.module, "validate_case", return_value=[]
            ), mock.patch.object(
                self.module, "_handle_harness_invocation", return_value=None
            ) as invoke, mock.patch.object(
                self.module, "classify_evidence"
            ) as classify:
                exit_code = self.module.main([
                    "--case",
                    standard_case["id"],
                    "--project-root",
                    str(root),
                    "--harness",
                    "junie",
                    "--invoke-harness",
                    "--result",
                    str(Path(directory) / "live-result.md"),
                ])
            self.assertEqual(0, exit_code)
            invoke.assert_called_once()
            classify.assert_not_called()

            high_risk_case = {
                **standard_case,
                "id": "high-risk-junie",
                "risk": {"level": "high", "reasons": ["untrusted-third-party-code"]},
                "executionTier": "externally-contained",
                "securityContainmentRequired": True,
                "harnessExecutionStatus": {
                    "codex": "external-runner-required",
                    "junie": "external-runner-required",
                },
            }
            with mock.patch.object(
                self.module, "load_cases", return_value={high_risk_case["id"]: high_risk_case}
            ), mock.patch.object(self.module, "_handle_harness_invocation") as invoke:
                with redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit):
                        self.module.main([
                            "--case",
                            high_risk_case["id"],
                            "--project-root",
                            str(root),
                            "--harness",
                            "junie",
                            "--invoke-harness",
                        ])
            invoke.assert_not_called()

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
                Path(sys.executable),
                "codex test",
                digest(Path(sys.executable)),
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

    def test_backlog_lifecycle_context_selects_the_current_fixture_paths(self) -> None:
        case = self.module.load_cases()["backlog-lifecycle"]
        fixture_root = ROOT / case["project"]
        expected_paths = ["TASK.md", "backlog", ".backlog-state"]

        self.assertEqual(expected_paths, case["contextPack"]["include"])
        self.assertEqual(expected_paths, case["modelVisiblePaths"])
        manifest = self.module.build_input_manifest(
            fixture_root,
            case["modelVisiblePaths"],
        )
        self.assertIn(
            "backlog/feature-backlog/retry-policy.md",
            {item.source_path for item in manifest.files},
        )

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

    def _write_fake_mcp_agent_ops(
        self,
        path: Path,
        runtime_digest: str,
    ) -> None:
        path.write_text(
            f"#!{sys.executable}\n"
            "import json, sys\n"
            "if sys.argv[1:] == ['--version']:\n"
            "    print('mcp-agent-ops 0.2.3')\n"
            "elif sys.argv[1:] == ['--identity-json']:\n"
            "    print(json.dumps({\n"
            "        'schema': 'mcp-agent-ops-runtime-identity',\n"
            "        'schemaVersion': 1,\n"
            "        'package': 'mcp-agent-ops',\n"
            "        'packageVersion': '0.2.3',\n"
            f"        'runtimeDigest': '{runtime_digest}',\n"
            "        'fileCount': 3,\n"
            "    }, sort_keys=True))\n"
            "else:\n"
            "    raise SystemExit(2)\n",
            encoding="utf-8",
        )
        path.chmod(0o700)

    def test_mcp_identity_binds_launcher_and_runtime_and_fails_on_drift(self) -> None:
        runtime_digest = "a" * 64
        with tempfile.TemporaryDirectory() as directory:
            executable = Path(directory) / "mcp-agent-ops"
            self._write_fake_mcp_agent_ops(executable, runtime_digest)
            identity = self.module.capture_mcp_agent_ops_identity(
                executable,
                required_version="0.2.3",
                required_runtime_digest=runtime_digest,
            )
            self.assertEqual(executable.resolve(), identity.executable)
            self.assertEqual(digest(executable), identity.launcher_digest)
            self.assertEqual(runtime_digest, identity.runtime_digest)
            self.assertRegex(identity.identity_digest, r"^[0-9a-f]{64}$")
            with self.assertRaisesRegex(RuntimeError, "runtime digest"):
                self.module.capture_mcp_agent_ops_identity(
                    executable,
                    required_version="0.2.3",
                    required_runtime_digest="b" * 64,
                )

    def test_mcp_catalog_and_host_configuration_are_exact_and_isolated(self) -> None:
        case = self.module.load_cases()["project-configuration-routing"]
        fixture = ROOT / "evals" / "projects" / "project-configuration-routing"
        available_source = fixture / "available-skills.txt"
        expected_skills = tuple(
            available_source.read_text(encoding="utf-8").splitlines()
        )
        identity = self.module.McpAgentOpsIdentity(
            Path(sys.executable).resolve(),
            "0.2.3",
            "1" * 64,
            "2" * 64,
            "3" * 64,
        )
        for harness in ("codex", "junie"):
            with self.subTest(harness=harness), tempfile.TemporaryDirectory() as directory:
                base = Path(directory)
                workspace = base / "workspace"
                workspace.mkdir()
                shutil.copy2(available_source, workspace / "available-skills.txt")
                evidence = base / "evidence"
                evidence.mkdir()
                context = self.module.ContextPackBuilder(ROOT).stage(
                    harness,
                    "project-configurator",
                    case["executionSkills"],
                    workspace,
                    skill_files=case["skillResourceAllowlist"],
                )
                self.assertFalse(
                    (
                        context.skill_location
                        / "development-methodology"
                        / "assets"
                        / "templates"
                        / "project-template.yaml"
                    ).exists()
                )
                available = self.module.read_mcp_skill_catalog(
                    workspace,
                    "available-skills.txt",
                    ROOT,
                )
                self.assertEqual(expected_skills, available)
                mcp = self.module.stage_mcp_agent_ops_context(
                    harness,
                    workspace,
                    identity,
                    ROOT,
                    context.skill_location,
                    available,
                    case["executionSkills"],
                    evidence / "audit.jsonl",
                    evidence,
                    catalog_resource_allowlist=case["mcpAgentOps"][
                        "catalogResourceAllowlist"
                    ],
                    mcp_only_skill_ids=case["mcpAgentOps"]["mcpOnlySkills"],
                )
                staged_names = {
                    path.name for path in mcp.skill_root.iterdir() if path.is_dir()
                }
                self.assertEqual(set(expected_skills), staged_names)
                self.assertNotIn("codex-harness-directives", staged_names)
                self.assertIn(
                    "# Create Project Configuration",
                    (
                        mcp.skill_root
                        / "create-project-configuration"
                        / "SKILL.md"
                    ).read_text(encoding="utf-8"),
                )
                for skill_id in case["mcpAgentOps"]["mcpOnlySkills"]:
                    self.assertFalse((context.skill_location / skill_id).exists())
                    self.assertNotIn(
                        "# Evaluation catalog entry",
                        (mcp.skill_root / skill_id / "SKILL.md").read_text(
                            encoding="utf-8"
                        ),
                    )
                self.assertTrue(
                    (
                        mcp.skill_root
                        / "development-methodology"
                        / "assets"
                        / "templates"
                        / "project-template.yaml"
                    ).is_file()
                )
                catalog_only = (
                    mcp.skill_root / "fastapi" / "SKILL.md"
                ).read_text(encoding="utf-8")
                self.assertIn("# Evaluation catalog entry", catalog_only)
                self.assertNotIn("Application Boundaries", catalog_only)
                command = self.module.build_harness_command(
                    harness,
                    workspace,
                    "project-configurator",
                    "Configure the project",
                    "test-model",
                    read_only=False,
                    event_output=evidence / "events.jsonl",
                    evidence_root=evidence,
                    isolated_config_root=workspace,
                    skill_locations=[context.skill_location],
                    agent_locations=[context.agent_location],
                    harness_executable=Path(sys.executable),
                    mcp_agent_ops=mcp,
                )
                if harness == "codex":
                    joined = "\n".join(command.argv)
                    self.assertIn("--ignore-user-config", command.argv)
                    self.assertNotIn("--sandbox", command.argv)
                    self.assertIn('approval_policy="never"', joined)
                    self.assertIn(
                        'default_permissions="mcp-eval-git-write"',
                        joined,
                    )
                    self.assertIn(
                        "permissions.mcp-eval-git-write",
                        joined,
                    )
                    self.assertIn("mcp_servers.mcp-agent-ops.command", joined)
                    self.assertIn(
                        "mcp_servers.mcp-agent-ops.enabled_tools",
                        joined,
                    )
                    self.assertIn(
                        'mcp_servers.mcp-agent-ops.default_tools_approval_mode="approve"',
                        joined,
                    )
                    self.assertIn(
                        "MCP_AGENT_OPS_REQUIRED_RUNTIME_DIGEST",
                        joined,
                    )
                    codex_configuration = json.loads(
                        mcp.configuration_evidence.read_text(encoding="utf-8")
                    )
                    self.assertEqual(
                        "never",
                        codex_configuration["approval_policy"],
                    )
                    self.assertEqual(
                        "mcp-eval-git-write",
                        codex_configuration["default_permissions"],
                    )
                    codex_profile = codex_configuration["permissions"][
                        "mcp-eval-git-write"
                    ]
                    self.assertEqual(
                        "write",
                        codex_profile["filesystem"][":workspace_roots"][".git"],
                    )
                    self.assertEqual(
                        "read",
                        codex_profile["filesystem"][":workspace_roots"][".codex"],
                    )
                    self.assertFalse(codex_profile["network"]["enabled"])
                    self.assertEqual(
                        case["mcpAgentOps"]["enabledTools"],
                        codex_configuration["mcp_servers"]["mcp-agent-ops"][
                            "enabled_tools"
                        ],
                    )
                    self.assertIsNone(mcp.config_location)
                else:
                    self.assertIsNotNone(mcp.config_location)
                    expected_location = mcp.config_location.resolve()
                    self.assertNotIn(workspace.resolve(), expected_location.parents)
                    self.assertIn(evidence.resolve(), expected_location.parents)
                    self.assertIn(
                        f"--mcp-location={expected_location}",
                        command.argv,
                    )
                    self.assertIn("--mcp-default-locations=false", command.argv)
                    config = json.loads(
                        (expected_location / "mcp.json").read_text(
                            encoding="utf-8"
                        )
                    )
                    self.assertEqual(
                        ["mcp-agent-ops"],
                        list(config["mcpServers"]),
                    )
                    self.assertIsNotNone(mcp.authorization_evidence)
                    allowlist = json.loads(
                        mcp.authorization_evidence.read_text(encoding="utf-8")
                    )
                    self.assertEqual(
                        [
                            {
                                "pattern": f"mcp-agent-ops:{tool}",
                                "action": "allow",
                            }
                            for tool in case["mcpAgentOps"]["enabledTools"]
                        ],
                        allowlist["rules"]["mcpTools"]["rules"],
                    )
                    self.assertEqual(
                        [
                            {"prefix": "git add", "action": "allow"},
                            {"prefix": "git commit", "action": "allow"},
                        ],
                        allowlist["rules"]["executables"]["rules"],
                    )
                    self.assertEqual("ask", allowlist["defaultBehavior"])
                    self.assertTrue(allowlist["allowReadonlyCommands"])
                self.assertEqual(
                    mcp.configuration_digest,
                    digest(mcp.configuration_evidence),
                )
                self.assertEqual(
                    mcp.catalog_evidence.read_bytes(),
                    (mcp.skill_root.parent / "catalog-manifest.json").read_bytes(),
                )

    def test_mcp_audit_parser_rejects_untrusted_or_incomplete_lifecycles(self) -> None:
        valid = [
            {
                "schema": "mcp-agent-ops-tool-audit",
                "version": 1,
                "sequence": 1,
                "callId": "1",
                "tool": "skill_list",
                "status": "started",
                "argumentsDigest": "a" * 64,
            },
            {
                "schema": "mcp-agent-ops-tool-audit",
                "version": 1,
                "sequence": 2,
                "callId": "1",
                "tool": "skill_list",
                "status": "completed",
                "resultDigest": "b" * 64,
            },
            {
                "schema": "mcp-agent-ops-tool-audit",
                "version": 1,
                "sequence": 3,
                "callId": "2",
                "tool": "detect_technology_skills",
                "status": "started",
                "argumentsDigest": "c" * 64,
            },
            {
                "schema": "mcp-agent-ops-tool-audit",
                "version": 1,
                "sequence": 4,
                "callId": "2",
                "tool": "detect_technology_skills",
                "status": "completed",
                "resultDigest": "d" * 64,
            },
        ]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "audit.jsonl"

            def write(records: list[dict[str, object]]) -> None:
                path.write_text(
                    "\n".join(json.dumps(record) for record in records) + "\n",
                    encoding="utf-8",
                )

            write(valid)
            records = self.module.read_mcp_agent_ops_audit(path)
            completed = self.module.completed_mcp_tool_sequence(records)
            self.assertEqual(
                ["skill_list", "detect_technology_skills"],
                completed,
            )
            self.assertTrue(
                self.module.required_tools_are_subsequence(
                    ["skill_list", "detect_technology_skills"],
                    ["claim_status", *completed, "verify_yaml"],
                )
            )
            self.assertFalse(
                self.module.required_tools_are_subsequence(
                    ["detect_technology_skills", "skill_list"],
                    completed,
                )
            )
            invalid_variants: list[tuple[list[dict[str, object]], str]] = []
            forbidden = [dict(record) for record in valid]
            forbidden[0]["path"] = "/private/example"
            invalid_variants.append((forbidden, "forbidden fields"))
            empty_call = [dict(record) for record in valid]
            empty_call[0]["callId"] = ""
            invalid_variants.append((empty_call, "invalid contract"))
            failed = [dict(record) for record in valid]
            failed[1]["status"] = "failed"
            invalid_variants.append((failed, "failed tool call"))
            invalid_variants.append((valid[:-1], "incomplete tool lifecycle"))
            for variant, message in invalid_variants:
                with self.subTest(message=message):
                    write(variant)
                    with self.assertRaisesRegex(ValueError, message):
                        self.module.read_mcp_agent_ops_audit(path)

    def test_mcp_shared_audit_rejects_calls_across_process_streams(self) -> None:
        session_id = "a" * 32
        parent_stream = "b" * 32
        agent_stream = "c" * 32
        tools = [
            ("skill_list", "CATALOG"),
            ("detect_technology_skills", "READY"),
            ("claim_acquire", "PRIMARY"),
            ("verify_yaml", "OK"),
            ("verify_markdown_links", "OK"),
            ("claim_release", "RELEASED"),
        ]
        records: list[dict[str, object]] = [
            {
                "schema": "mcp-agent-ops-tool-audit",
                "version": 2,
                "sequence": 1,
                "streamId": parent_stream,
                "sessionId": session_id,
                "callId": "1",
                "tool": "skill_list",
                "status": "started",
                "argumentsDigest": "1" * 64,
            }
        ]
        sequence = 0
        for index, (tool, outcome) in enumerate(tools, start=1):
            sequence += 1
            records.append({
                "schema": "mcp-agent-ops-tool-audit",
                "version": 2,
                "sequence": sequence,
                "streamId": agent_stream,
                "sessionId": session_id,
                "callId": str(index),
                "tool": tool,
                "status": "started",
                "argumentsDigest": "2" * 64,
            })
            sequence += 1
            records.append({
                "schema": "mcp-agent-ops-tool-audit",
                "version": 2,
                "sequence": sequence,
                "streamId": agent_stream,
                "sessionId": session_id,
                "callId": str(index),
                "tool": tool,
                "status": "completed",
                "resultDigest": "3" * 64,
                "outcome": outcome,
            })
        records.append({
            "schema": "mcp-agent-ops-tool-audit",
            "version": 2,
            "sequence": 2,
            "streamId": parent_stream,
            "sessionId": session_id,
            "callId": "1",
            "tool": "skill_list",
            "status": "completed",
            "resultDigest": "4" * 64,
            "outcome": "CATALOG",
        })
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "audit.jsonl"
            path.write_text(
                "\n".join(json.dumps(record) for record in records) + "\n",
                encoding="utf-8",
            )
            validated = self.module.read_mcp_agent_ops_audit(path)
            with self.assertRaisesRegex(ValueError, "one call-bearing process stream"):
                self.module.select_mcp_tool_stream(
                    validated,
                    [[tool for tool, _outcome in tools]],
                    {tool: [outcome] for tool, outcome in tools},
                )

            mixed = [dict(record) for record in records]
            mixed[-1]["sessionId"] = "d" * 32
            path.write_text(
                "\n".join(json.dumps(record) for record in mixed) + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "mixes evaluation session"):
                self.module.read_mcp_agent_ops_audit(path)

            missing_outcome = [
                dict(record)
                for record in records
                if record["streamId"] == agent_stream
            ]
            missing_outcome[-1].pop("outcome")
            path.write_text(
                "\n".join(json.dumps(record) for record in missing_outcome) + "\n",
                encoding="utf-8",
            )
            validated = self.module.read_mcp_agent_ops_audit(path)
            with self.assertRaisesRegex(ValueError, "no process stream"):
                self.module.select_mcp_tool_stream(
                    validated,
                    [[tool for tool, _outcome in tools]],
                    {tool: [outcome] for tool, outcome in tools},
                )

    def test_mcp_stream_selection_binds_outcome_to_expected_arguments(self) -> None:
        session_id = "a" * 32
        wrong_stream = "b" * 32
        expected_stream = "c" * 32
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "workspace"
            workspace.mkdir()
            expected_digests = self.module.resolve_mcp_tool_argument_digests(
                {
                    "verify_yaml": {
                        "repository_root": "$WORKSPACE",
                        "paths": ["PROJECT.yaml"],
                    }
                },
                workspace,
            )
            expected_digest = expected_digests["verify_yaml"]
            records: list[dict[str, object]] = []
            for stream_id, argument_digest, outcome in (
                (wrong_stream, "d" * 64, "OK"),
                (expected_stream, expected_digest, "OK"),
            ):
                records.extend((
                    {
                        "schema": "mcp-agent-ops-tool-audit",
                        "version": 2,
                        "sequence": 1,
                        "streamId": stream_id,
                        "sessionId": session_id,
                        "callId": "1",
                        "tool": "verify_yaml",
                        "status": "started",
                        "argumentsDigest": argument_digest,
                    },
                    {
                        "schema": "mcp-agent-ops-tool-audit",
                        "version": 2,
                        "sequence": 2,
                        "streamId": stream_id,
                        "sessionId": session_id,
                        "callId": "1",
                        "tool": "verify_yaml",
                        "status": "completed",
                        "resultDigest": "e" * 64,
                        "outcome": outcome,
                    },
                ))
            path = Path(directory) / "audit.jsonl"
            path.write_text(
                "\n".join(json.dumps(record) for record in records) + "\n",
                encoding="utf-8",
            )
            validated = self.module.read_mcp_agent_ops_audit(path)
            with self.assertRaisesRegex(ValueError, "one call-bearing process stream"):
                self.module.select_mcp_tool_stream(
                    validated,
                    [["verify_yaml"]],
                    {"verify_yaml": ["OK"]},
                    expected_digests,
                )

            exact_but_rejected = [dict(record) for record in records[:2]]
            exact_but_rejected[0]["argumentsDigest"] = expected_digest
            exact_but_rejected[1]["outcome"] = "FINDINGS"
            path.write_text(
                "\n".join(json.dumps(record) for record in exact_but_rejected) + "\n",
                encoding="utf-8",
            )
            validated = self.module.read_mcp_agent_ops_audit(path)
            with self.assertRaisesRegex(ValueError, "no process stream"):
                self.module.select_mcp_tool_stream(
                    validated,
                    [["verify_yaml"]],
                    {"verify_yaml": ["OK"]},
                    expected_digests,
                )

    def test_mcp_argument_digest_matches_protocol_and_rejects_placeholders(self) -> None:
        self.assertEqual(
            "6d9eb45284090145dc16661b06abe01185a16a7dabba07c992a131bffa6b8114",
            self.module.mcp_value_digest({"b": 1, "a": "é"}),
        )
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            skill_root = workspace / ".eval-context" / "mcp-agent-ops" / "skills"
            self.assertEqual(
                self.module.mcp_value_digest({"paths": [str(skill_root.resolve())]}),
                self.module.resolve_mcp_tool_argument_digests(
                    {"skill_validate": {"paths": ["$SKILL_ROOT"]}},
                    workspace,
                    skill_root=skill_root,
                )["skill_validate"],
            )
            with self.assertRaisesRegex(ValueError, "complete value"):
                self.module.resolve_mcp_tool_argument_digests(
                    {"verify_yaml": {"repository_root": "$WORKSPACE/child"}},
                    workspace,
                )
            with self.assertRaisesRegex(ValueError, "unknown.*placeholder"):
                self.module.resolve_mcp_tool_argument_digests(
                    {"verify_yaml": {"repository_root": "$PROJECT_ROOT"}},
                    workspace,
                )

    def test_mcp_case_requires_every_integrated_operation_under_exact_policy(self) -> None:
        case = self.module.load_cases()["project-configuration-routing"]
        contract = case["mcpAgentOps"]
        expected_tools = [
            "claim_status",
            "claim_acquire",
            "claim_extend",
            "claim_heartbeat",
            "claim_release",
            "skill_list",
            "skill_load",
            "skill_resource_load",
            "skill_refresh",
            "skill_validate",
            "detect_technology_skills",
            "verify_yaml",
            "verify_markdown_links",
        ]
        self.assertEqual(expected_tools, contract["enabledTools"])
        self.assertEqual("0.2.3", contract["requiredVersion"])
        self.assertEqual(
            "86e8d2b0af7fe421e88e3aec18e035b005c33474c4351332c9d31830908e5193",
            contract["requiredRuntimeDigest"],
        )
        self.assertEqual(
            ["PRIMARY"],
            contract["requiredToolOutcomes"]["claim_acquire"],
        )
        required = {
            tool
            for sequence in contract["requiredToolSequences"]
            for tool in sequence
        }
        self.assertTrue(
            {
                "skill_load",
                "skill_validate",
                "skill_refresh",
                "claim_status",
                "claim_extend",
                "claim_heartbeat",
            }.issubset(required)
        )
        self.assertEqual(
            ["skill-authoring", "maintain-methodology-documentation"],
            contract["mcpOnlySkills"],
        )
        self.assertEqual(set(contract["enabledTools"]), required)
        self.assertEqual(
            [[
                "skill_list",
                "skill_load",
                "skill_resource_load",
                "skill_validate",
                "skill_refresh",
                "detect_technology_skills",
                "claim_acquire",
                "claim_status",
                "claim_extend",
                "claim_heartbeat",
                "verify_yaml",
                "verify_markdown_links",
                "claim_release",
            ]],
            contract["requiredToolSequences"],
        )
        escaping_skill_root = yaml.safe_load(yaml.safe_dump(case))
        escaping_skill_root["mcpAgentOps"]["requiredToolArguments"][
            "skill_validate"
        ]["paths"] = ["$SKILL_ROOT/child"]
        self.assertTrue(
            any(
                "path sentinels as complete values" in error
                for error in self.module.validate_case_definition(
                    escaping_skill_root
                )
            )
        )

    def test_completed_mcp_call_without_safe_outcome_is_not_semantic_evidence(self) -> None:
        records = [
            {
                "schema": "mcp-agent-ops-tool-audit",
                "version": 2,
                "sequence": 1,
                "streamId": "a" * 32,
                "sessionId": "b" * 32,
                "callId": "1",
                "tool": "skill_validate",
                "status": "started",
                "argumentsDigest": "c" * 64,
            },
            {
                "schema": "mcp-agent-ops-tool-audit",
                "version": 2,
                "sequence": 2,
                "streamId": "a" * 32,
                "sessionId": "b" * 32,
                "callId": "1",
                "tool": "skill_validate",
                "status": "completed",
                "resultDigest": "d" * 64,
            },
        ]
        self.assertEqual(
            [{}],
            self.module.completed_mcp_tool_outcomes(records),
        )
        self.assertEqual(
            [[{
                "tool": "skill_validate",
                "argumentsDigest": "c" * 64,
                "outcome": None,
            }]],
            self.module.completed_mcp_tool_calls(records),
        )
        with self.assertRaisesRegex(ValueError, "no process stream"):
            self.module.select_mcp_tool_stream(
                records,
                [["skill_validate"]],
                {"skill_validate": ["VALID"]},
                {"skill_validate": "c" * 64},
            )

    def test_mcp_stream_requires_the_exact_calls_in_declared_order(self) -> None:
        session_id = "a" * 32
        stream_id = "b" * 32
        expected = {
            "verify_yaml": "1" * 64,
            "verify_markdown_links": "2" * 64,
        }
        calls = [
            ("verify_markdown_links", expected["verify_markdown_links"]),
            ("verify_yaml", expected["verify_yaml"]),
            ("verify_yaml", "3" * 64),
            ("verify_markdown_links", "4" * 64),
        ]
        records: list[dict[str, object]] = []
        for call_index, (tool, argument_digest) in enumerate(calls, start=1):
            records.extend((
                {
                    "schema": "mcp-agent-ops-tool-audit",
                    "version": 2,
                    "sequence": len(records) + 1,
                    "streamId": stream_id,
                    "sessionId": session_id,
                    "callId": str(call_index),
                    "tool": tool,
                    "status": "started",
                    "argumentsDigest": argument_digest,
                },
                {
                    "schema": "mcp-agent-ops-tool-audit",
                    "version": 2,
                    "sequence": len(records) + 2,
                    "streamId": stream_id,
                    "sessionId": session_id,
                    "callId": str(call_index),
                    "tool": tool,
                    "status": "completed",
                    "resultDigest": "5" * 64,
                    "outcome": "OK",
                },
            ))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "audit.jsonl"
            path.write_text(
                "\n".join(json.dumps(record) for record in records) + "\n",
                encoding="utf-8",
            )
            validated = self.module.read_mcp_agent_ops_audit(path)
            with self.assertRaisesRegex(ValueError, "no process stream"):
                self.module.select_mcp_tool_stream(
                    validated,
                    [["verify_yaml", "verify_markdown_links"]],
                    {
                        "verify_yaml": ["OK"],
                        "verify_markdown_links": ["OK"],
                    },
                    expected,
                )

    def test_mcp_stream_rejects_extra_or_repeated_enabled_calls(self) -> None:
        session_id = "a" * 32
        stream_id = "b" * 32
        expected = {
            "skill_validate": "1" * 64,
            "skill_refresh": "2" * 64,
        }
        calls = [
            ("skill_validate", expected["skill_validate"], "VALID"),
            ("skill_refresh", expected["skill_refresh"], "CATALOG"),
            ("skill_validate", expected["skill_validate"], "VALID"),
        ]
        records: list[dict[str, object]] = []
        for call_index, (tool, argument_digest, outcome) in enumerate(calls, start=1):
            records.extend((
                {
                    "schema": "mcp-agent-ops-tool-audit",
                    "version": 2,
                    "sequence": len(records) + 1,
                    "streamId": stream_id,
                    "sessionId": session_id,
                    "callId": str(call_index),
                    "tool": tool,
                    "status": "started",
                    "argumentsDigest": argument_digest,
                },
                {
                    "schema": "mcp-agent-ops-tool-audit",
                    "version": 2,
                    "sequence": len(records) + 2,
                    "streamId": stream_id,
                    "sessionId": session_id,
                    "callId": str(call_index),
                    "tool": tool,
                    "status": "completed",
                    "resultDigest": "3" * 64,
                    "outcome": outcome,
                },
            ))
        with self.assertRaisesRegex(ValueError, "no process stream"):
            self.module.select_mcp_tool_stream(
                records,
                [["skill_validate", "skill_refresh"]],
                {
                    "skill_validate": ["VALID"],
                    "skill_refresh": ["CATALOG"],
                },
                expected,
            )

    def test_mcp_case_contract_is_valid_and_probe_variants_disable_mcp(self) -> None:
        case = self.module.load_cases()["project-configuration-routing"]
        self.assertEqual([], self.module.validate_case_definition(case))
        duplicated = yaml.safe_load(yaml.safe_dump(case))
        duplicated["mcpAgentOps"]["requiredToolSequences"][0].append(
            "verify_yaml"
        )
        self.assertTrue(
            any(
                "must not repeat" in error
                for error in self.module.validate_case_definition(duplicated)
            )
        )
        missing_arguments = yaml.safe_load(yaml.safe_dump(case))
        del missing_arguments["mcpAgentOps"]["requiredToolArguments"][
            "verify_yaml"
        ]
        self.assertTrue(
            any(
                "must cover exactly" in error
                for error in self.module.validate_case_definition(missing_arguments)
            )
        )
        derived = self.module._apply_probe_variant(
            case,
            "probe-create-project-configuration",
            "treatment",
        )
        self.assertNotIn("mcpAgentOps", derived)
        self.assertFalse(self.module._case_uses_mcp_agent_ops(derived))

    def test_mcp_cli_requires_explicit_executable_only_for_the_base_case(self) -> None:
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.module.main([
                "--case",
                "project-configuration-routing",
                "--harness",
                "codex",
                "--print-invocation",
            ])
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.module.main([
                "--case",
                "typescript-order-pricing",
                "--harness",
                "codex",
                "--mcp-agent-ops-executable",
                sys.executable,
                "--print-invocation",
            ])
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.module.main([
                "--skill-probe",
                "probe-create-project-configuration",
                "--probe-variant",
                "treatment",
                "--harness",
                "codex",
                "--mcp-agent-ops-executable",
                sys.executable,
                "--print-invocation",
            ])

    def test_mcp_receipt_evidence_replays_identity_and_audit_contract(self) -> None:
        case = self.module.load_cases()["project-configuration-routing"]
        contract = case["mcpAgentOps"]
        validation_module = sys.modules[self.module.validate_evidence.__module__]
        outcomes = {
            "skill_list": "CATALOG",
            "skill_load": "LOADED",
            "skill_resource_load": "LOADED",
            "skill_validate": "VALID",
            "skill_refresh": "CATALOG",
            "detect_technology_skills": "READY",
            "claim_acquire": "PRIMARY",
            "claim_status": "STATUS",
            "claim_extend": "EXTENDED",
            "claim_heartbeat": "HEARTBEAT",
            "verify_yaml": "OK",
            "verify_markdown_links": "OK",
            "claim_release": "RELEASED",
        }
        tools = list(outcomes)
        session_id = "5" * 32
        stream_id = "6" * 32
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            argument_digests = self.module.resolve_mcp_tool_argument_digests(
                contract["requiredToolArguments"],
                root / "workspace",
                skill_root=(
                    root
                    / "workspace"
                    / ".eval-context"
                    / "mcp-agent-ops"
                    / "skills"
                ),
            )
            records: list[dict[str, object]] = []
            for call_index, tool in enumerate(tools, start=1):
                completed_record = {
                    "schema": "mcp-agent-ops-tool-audit",
                    "version": 2,
                    "sequence": len(records) + 2,
                    "streamId": stream_id,
                    "sessionId": session_id,
                    "callId": str(call_index),
                    "tool": tool,
                    "status": "completed",
                    "resultDigest": "b" * 64,
                }
                completed_record["outcome"] = outcomes[tool]
                records.extend((
                    {
                        "schema": "mcp-agent-ops-tool-audit",
                        "version": 2,
                        "sequence": len(records) + 1,
                        "streamId": stream_id,
                        "sessionId": session_id,
                        "callId": str(call_index),
                        "tool": tool,
                        "status": "started",
                        "argumentsDigest": argument_digests[tool],
                    },
                    completed_record,
                ))
            evidence_path = root / "evidence.yaml"
            evidence_path.write_text("receipt\n", encoding="utf-8")
            audit_path = root / "audit.jsonl"
            audit_path.write_text(
                "\n".join(json.dumps(record) for record in records) + "\n",
                encoding="utf-8",
            )
            configuration_path = root / "configuration.json"
            configuration = {
                "approval_policy": "never",
                "default_permissions": "mcp-eval-git-write",
                "permissions": {
                    "mcp-eval-git-write": {
                        "description": "Disposable MCP evaluation workspace with Git metadata writes",
                        "filesystem": {
                            ":root": "read",
                            ":tmpdir": "write",
                            str(Path.home().resolve()): "deny",
                            str(root.resolve()): "deny",
                            ":workspace_roots": {
                                ".": "write",
                                ".agents": "read",
                                ".codex": "read",
                                ".eval-context": "read",
                                ".git": "write",
                                ".junie": "read",
                            },
                        },
                        "network": {"enabled": False},
                    }
                },
                "mcp_servers": {
                    "mcp-agent-ops": {
                        "command": str(Path(sys.executable).resolve()),
                        "args": [],
                        "env": {
                            "MCP_AGENT_OPS_SKILL_ROOTS": str(
                                root
                                / "workspace"
                                / ".eval-context"
                                / "mcp-agent-ops"
                                / "skills"
                            ),
                            "MCP_AGENT_OPS_DETECTION_REGISTRY": str(root / "registry.yaml"),
                            "MCP_AGENT_OPS_WORKSPACE_ROOTS": str(root / "workspace"),
                            "MCP_AGENT_OPS_AUDIT_LOG": str(audit_path),
                            "MCP_AGENT_OPS_AUDIT_ROOTS": str(root),
                            "MCP_AGENT_OPS_AUDIT_SHARED": "true",
                            "MCP_AGENT_OPS_AUDIT_SESSION_ID": session_id,
                            "MCP_AGENT_OPS_REQUIRED_RUNTIME_DIGEST": contract["requiredRuntimeDigest"],
                        },
                        "enabled": True,
                        "required": True,
                        "enabled_tools": contract["enabledTools"],
                        "default_tools_approval_mode": "approve",
                        "startup_timeout_sec": 15.0,
                        "tool_timeout_sec": 60.0,
                    }
                }
            }
            configuration_path.write_text(
                json.dumps(configuration, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            catalog_files = [{
                "skill": "example",
                "path": "SKILL.md",
                "role": "catalog-metadata-only",
                "digest": "7" * 64,
                "size": 10,
            }]
            catalog_manifest_digest = hashlib.sha256(
                json.dumps(
                    catalog_files,
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode("utf-8")
            ).hexdigest()
            catalog_path = root / "catalog.json"
            catalog_path.write_text(
                json.dumps({
                    "schema": "dev-methodology-eval-mcp-skill-catalog",
                    "version": 1,
                    "manifestDigest": catalog_manifest_digest,
                    "skills": ["example"],
                    "files": catalog_files,
                }, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            (root / "outputs").mkdir()
            output_manifest_path = root / "outputs-manifest.json"
            output_manifest_path.write_text(
                json.dumps({
                    "schema": "dev-methodology-eval-output-manifest",
                    "version": 1,
                    "allowedWritePaths": case["allowedWritePaths"],
                    "files": [],
                }, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            mcp_run: dict[str, object] = {
                "serverName": contract["serverName"],
                "version": contract["requiredVersion"],
                "launcherDigest": "1" * 64,
                "runtimeDigest": contract["requiredRuntimeDigest"],
                "identityDigest": "2" * 64,
                "configurationDigest": digest(configuration_path),
                "catalogManifestDigest": catalog_manifest_digest,
                "configurationEvidence": "configuration.json#mcp_servers",
                "catalogEvidence": "catalog.json#dev-methodology-eval-mcp-skill-catalog",
                "catalogEvidenceDigest": digest(catalog_path),
                "authorizationEvidence": None,
                "authorizationDigest": None,
                "junieAgentAttributionStatus": None,
                "junieAgentAttributionEvidence": None,
                "junieAgentAttributionDigest": None,
                "identityEvidence": "identity.json#mcp-identity",
                "identityEvidenceDigest": "0" * 64,
                "auditSessionId": session_id,
                "auditStreamId": stream_id,
                "auditDigest": digest(audit_path),
                "auditEvidence": "audit.jsonl#mcp-agent-ops-tool-audit",
                "outputManifestDigest": digest(output_manifest_path),
                "outputManifestEvidence": "outputs-manifest.json#dev-methodology-eval-output-manifest",
                "completedTools": tools,
                "toolOutcomes": {
                    tool: [outcome] for tool, outcome in outcomes.items()
                },
                "requiredToolSequences": contract["requiredToolSequences"],
                "requiredToolOutcomes": contract["requiredToolOutcomes"],
                "requiredToolArgumentDigests": argument_digests,
                "permissionProfileHostHomeDigest": self.module.mcp_value_digest(
                    str(Path.home().resolve())
                ),
                "toolEvidenceStatus": "verified",
            }
            identity = {
                "schema": "dev-methodology-eval-mcp-identity",
                "version": 3,
                "serverName": mcp_run["serverName"],
                "packageVersion": mcp_run["version"],
                "launcherDigest": mcp_run["launcherDigest"],
                "runtimeDigest": mcp_run["runtimeDigest"],
                "identityDigest": mcp_run["identityDigest"],
                "configurationDigest": mcp_run["configurationDigest"],
                "catalogManifestDigest": mcp_run["catalogManifestDigest"],
                "auditSessionId": session_id,
                "configurationEvidenceDigest": mcp_run["configurationDigest"],
                "catalogEvidenceDigest": mcp_run["catalogEvidenceDigest"],
                "authorizationDigest": None,
                "requiredToolArgumentDigests": argument_digests,
                "permissionProfileHostHomeDigest": mcp_run[
                    "permissionProfileHostHomeDigest"
                ],
            }
            identity_path = root / "identity.json"
            identity_path.write_text(
                json.dumps(identity, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            mcp_run["identityEvidenceDigest"] = digest(identity_path)
            errors: list[str] = []
            stale: list[str] = []
            validation_module._validate_mcp_agent_ops_run(
                case,
                {"harness": "codex", "mcpAgentOps": mcp_run},
                evidence_path,
                errors,
                stale,
            )
            self.assertEqual([], errors)
            self.assertEqual([], stale)
            server_environment = configuration["mcp_servers"]["mcp-agent-ops"][
                "env"
            ]
            staged_skill_root = server_environment["MCP_AGENT_OPS_SKILL_ROOTS"]
            server_environment["MCP_AGENT_OPS_SKILL_ROOTS"] = str(
                root / "unrelated-skills"
            )
            configuration_path.write_text(
                json.dumps(configuration, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            mcp_run["configurationDigest"] = digest(configuration_path)
            identity["configurationDigest"] = mcp_run["configurationDigest"]
            identity["configurationEvidenceDigest"] = mcp_run[
                "configurationDigest"
            ]
            identity_path.write_text(
                json.dumps(identity, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            mcp_run["identityEvidenceDigest"] = digest(identity_path)
            skill_root_errors: list[str] = []
            validation_module._validate_mcp_agent_ops_run(
                case,
                {"harness": "codex", "mcpAgentOps": mcp_run},
                evidence_path,
                skill_root_errors,
                [],
            )
            self.assertTrue(
                any("staged workspace catalog" in error for error in skill_root_errors)
            )
            server_environment["MCP_AGENT_OPS_SKILL_ROOTS"] = staged_skill_root
            home_key = str(Path.home().resolve())
            filesystem = configuration["permissions"]["mcp-eval-git-write"][
                "filesystem"
            ]
            del filesystem[home_key]
            filesystem[str((root / "unrelated-denial").resolve())] = "deny"
            configuration_path.write_text(
                json.dumps(configuration, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            mcp_run["configurationDigest"] = digest(configuration_path)
            identity["configurationDigest"] = mcp_run["configurationDigest"]
            identity["configurationEvidenceDigest"] = mcp_run[
                "configurationDigest"
            ]
            identity_path.write_text(
                json.dumps(identity, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            mcp_run["identityEvidenceDigest"] = digest(identity_path)
            denial_errors: list[str] = []
            validation_module._validate_mcp_agent_ops_run(
                case,
                {"harness": "codex", "mcpAgentOps": mcp_run},
                evidence_path,
                denial_errors,
                [],
            )
            self.assertTrue(
                any("host-home denial" in error for error in denial_errors)
            )

            del filesystem[str((root / "unrelated-denial").resolve())]
            filesystem[home_key] = "deny"
            configuration_path.write_text(
                json.dumps(configuration, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            mcp_run["configurationDigest"] = digest(configuration_path)
            identity["configurationDigest"] = mcp_run["configurationDigest"]
            identity["configurationEvidenceDigest"] = mcp_run[
                "configurationDigest"
            ]
            identity_path.write_text(
                json.dumps(identity, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            mcp_run["identityEvidenceDigest"] = digest(identity_path)
            wrong_argument_records = [dict(record) for record in records]
            wrong_argument_records[0]["argumentsDigest"] = "f" * 64
            audit_path.write_text(
                "\n".join(
                    json.dumps(record) for record in wrong_argument_records
                )
                + "\n",
                encoding="utf-8",
            )
            mcp_run["auditDigest"] = digest(audit_path)
            argument_errors: list[str] = []
            validation_module._validate_mcp_agent_ops_run(
                case,
                {"harness": "codex", "mcpAgentOps": mcp_run},
                evidence_path,
                argument_errors,
                [],
            )
            self.assertTrue(
                any("no process stream" in error for error in argument_errors)
            )
            audit_path.write_text(
                "\n".join(json.dumps(record) for record in records) + "\n",
                encoding="utf-8",
            )
            mcp_run["auditDigest"] = digest(audit_path)
            audit_path.write_text(
                audit_path.read_text(encoding="utf-8") + "{}\n",
                encoding="utf-8",
            )
            drift_errors: list[str] = []
            validation_module._validate_mcp_agent_ops_run(
                case,
                {"harness": "codex", "mcpAgentOps": mcp_run},
                evidence_path,
                drift_errors,
                [],
            )
            self.assertTrue(
                any("content digest" in error or "audit is invalid" in error for error in drift_errors)
            )


if __name__ == "__main__":
    unittest.main()
