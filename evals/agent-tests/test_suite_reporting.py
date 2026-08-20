# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Verifies bounded agent-suite scheduling and durable deterministic HTML aggregation.
# Governing design: backlog/feature-backlog/automate-parallel-agent-test-reporting.md

from __future__ import annotations

import importlib.util
import contextlib
import hashlib
import json
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest import mock


_MODULE_PATH = Path(__file__).with_name("suite_reporting.py")
_SPEC = importlib.util.spec_from_file_location("agent_suite_reporting", _MODULE_PATH)
assert _SPEC is not None and _SPEC.loader is not None
reporting = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = reporting
_SPEC.loader.exec_module(reporting)


class AgentSuiteReportingTests(unittest.TestCase):
    """Protect selection, resource, scheduling, rendering, and aggregation contracts."""

    def test_dev_orchestrator_target_rollout_gets_observational_token_report(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            renderer = root / "render-token-ledger.py"
            renderer.write_text("# test renderer\n", encoding="utf-8")
            rollout = root / "sessions" / "target.jsonl"
            rollout.parent.mkdir()
            rollout.write_text(
                json.dumps(
                    {
                        "type": "session_meta",
                        "payload": {
                            "id": "target-session",
                            "agent_role": "dev_orchestrator",
                        },
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            with (
                mock.patch.object(reporting, "_TOKEN_LEDGER_RENDERER", renderer),
                mock.patch.object(
                    reporting.subprocess,
                    "run",
                    return_value=mock.Mock(returncode=0, stderr=""),
                ) as process,
            ):
                diagnostic = reporting._generate_target_token_ledgers(
                    root, "dev_orchestrator"
                )

            self.assertIsNone(diagnostic)
            process.assert_called_once()
            manifest = json.loads(
                (root / "token-ledgers" / "index.json").read_text(encoding="utf-8")
            )
            self.assertEqual("target-session", manifest["reports"][0]["sessionId"])
            self.assertEqual(
                "token-ledgers/target-session.html",
                manifest["reports"][0]["html"],
            )

    def test_selection_supports_one_many_and_default_all(self) -> None:
        catalog = ("alpha", "beta", "gamma")

        self.assertEqual(("beta",), reporting.select_suites(catalog, ("beta",)))
        self.assertEqual(
            ("alpha", "gamma"), reporting.select_suites(catalog, ("gamma", "alpha"))
        )
        self.assertEqual(catalog, reporting.select_suites(catalog, ()))

    def test_selection_rejects_unknown_and_duplicate_before_execution(self) -> None:
        with self.assertRaisesRegex(ValueError, "unknown suite selections: missing"):
            reporting.select_suites(("alpha",), ("missing",))
        with self.assertRaisesRegex(ValueError, "duplicate suite selections: alpha"):
            reporting.select_suites(("alpha",), ("alpha", "alpha"))

    def test_resource_bounds_use_processors_memory_override_and_suite_count(
        self,
    ) -> None:
        resources = reporting.HostResources(
            processor_count=16, available_memory_bytes=20 * 1024**3
        )

        self.assertEqual(3, reporting.resolve_workers(3, resources))
        self.assertEqual(2, reporting.resolve_workers(10, resources, override=2))
        with self.assertRaisesRegex(ValueError, "below the .* per-worker safety bound"):
            reporting.resolve_workers(
                10,
                reporting.HostResources(
                    processor_count=2, available_memory_bytes=1024**3
                ),
            )
        with self.assertRaisesRegex(ValueError, "could not be measured"):
            reporting.resolve_workers(
                10,
                reporting.HostResources(processor_count=2, available_memory_bytes=0),
            )
        with self.assertRaisesRegex(ValueError, "between 1 and 4"):
            reporting.resolve_workers(2, resources, override=5)

    def test_unknown_or_insufficient_memory_stops_before_suite_execution(self) -> None:
        executor = mock.Mock()
        with (
            tempfile.TemporaryDirectory() as directory,
            self._stable_sources(),
            mock.patch.object(
                reporting,
                "discover_resources",
                return_value=reporting.HostResources(8, 0),
            ),
        ):
            with self.assertRaisesRegex(ValueError, "could not be measured"):
                reporting.run_suites(
                    "codex", ("dev-coder",), Path(directory), executor=executor
                )
        executor.assert_not_called()

        with self.assertRaisesRegex(ValueError, "below the .* per-worker safety bound"):
            reporting.resolve_workers(
                1, reporting.HostResources(8, reporting._MEMORY_BYTES_PER_WORKER - 1)
            )

    def test_parallel_execution_is_bounded_and_destinations_are_disjoint(self) -> None:
        active = 0
        maximum_active = 0
        destinations: list[Path] = []
        lock = threading.Lock()

        def executor(
            harness: str, suite_id: str, destination: Path, timeout: int
        ) -> object:
            nonlocal active, maximum_active
            with lock:
                active += 1
                maximum_active = max(maximum_active, active)
                destinations.append(destination)
            time.sleep(0.02)
            with lock:
                active -= 1
            return self._execution(suite_id, destination)

        with tempfile.TemporaryDirectory() as directory, self._stable_sources():
            results = reporting.run_suites(
                "codex",
                ("dev-coder", "dev-code-reviewer", "dev-verifier"),
                Path(directory),
                maximum_workers=2,
                executor=executor,
                resources=reporting.HostResources(16, 32 * 1024**3),
            )

        self.assertEqual(2, maximum_active)
        self.assertEqual(3, len(set(destinations)))
        self.assertEqual(
            ["PASS", "PASS", "PASS"], [value["status"] for value in results]
        )

    def test_global_safety_stop_preserves_completed_reports_and_stops_new_work(
        self,
    ) -> None:
        probes = iter((True, False, False))
        executed: list[str] = []

        def executor(
            harness: str, suite_id: str, destination: Path, timeout: int
        ) -> object:
            executed.append(suite_id)
            return self._execution(suite_id, destination)

        with (
            tempfile.TemporaryDirectory() as directory,
            self._stable_sources(),
            mock.patch.object(
                reporting,
                "discover_resources",
                return_value=reporting.HostResources(8, 16 * 1024**3),
            ),
        ):
            results = reporting.run_suites(
                "codex",
                ("dev-coder", "dev-code-reviewer", "dev-verifier"),
                Path(directory),
                maximum_workers=1,
                executor=executor,
                safety_probe=lambda _: next(probes),
            )

            self.assertTrue(
                (
                    Path(directory) / "suites" / "codex" / "dev-coder.manifest.json"
                ).is_file()
            )
        self.assertEqual(["dev-coder"], executed)
        self.assertEqual(
            ["PASS", "NOT_SCHEDULED"], [value["status"] for value in results]
        )

    def test_suite_executor_failure_gets_a_report_without_erasing_other_results(
        self,
    ) -> None:
        def executor(
            harness: str, suite_id: str, destination: Path, timeout: int
        ) -> object:
            if suite_id == "dev-code-reviewer":
                raise RuntimeError("synthetic harness failure")
            return self._execution(suite_id, destination)

        with tempfile.TemporaryDirectory() as directory, self._stable_sources():
            root = Path(directory)
            results = reporting.run_suites(
                "codex",
                ("dev-coder", "dev-code-reviewer"),
                root,
                executor=executor,
                resources=reporting.HostResources(8, 16 * 1024**3),
            )

            _, failed_path = self._current_generation(
                root, "codex", "dev-code-reviewer"
            )
            failed = json.loads(failed_path.read_text(encoding="utf-8"))
        self.assertEqual(
            ["PASS", "INFRASTRUCTURE_FAILED"], [value["status"] for value in results]
        )
        self.assertIn("synthetic harness failure", failed["runnerStderr"])

    def test_suite_report_is_self_contained_and_carries_machine_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            metadata = self._metadata(
                "codex", "dev-coder", "PASS", Path(directory)
            )

            rendered = reporting.render_suite_html(metadata)

        self.assertIn('<script id="report-metadata" type="application/json">', rendered)
        self.assertIn('<meta name="viewport"', rendered)
        self.assertIn('<th scope="col">Scenario</th>', rendered)
        self.assertNotIn("http://", rendered)
        self.assertNotIn("https://", rendered)

    def test_atomic_report_replacement_does_not_leave_temporary_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            reporting.write_suite_report(
                root, self._metadata("codex", "dev-coder", "PASS", root / "pass-evidence")
            )
            html_path, metadata_path = reporting.write_suite_report(
                root, self._metadata("codex", "dev-coder", "FAIL", root / "fail-evidence")
            )

            self.assertIn("FAIL", html_path.read_text(encoding="utf-8"))
            self.assertEqual(
                "FAIL", json.loads(metadata_path.read_text(encoding="utf-8"))["status"]
            )
            self.assertEqual([], list(root.rglob(".*.tmp")))

    def test_publication_reopens_missing_runner_evidence_before_preserving_pass(
        self,
    ) -> None:
        """A serialized runner audit cannot preserve PASS after its receipt disappears."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            evidence_root = root / "runner-result"
            metadata = self._metadata(
                "codex", "dev-coder", "PASS", evidence_root
            )
            receipt_path = Path(
                metadata["scenarioResults"][0]["_checkpointRoot"]
            ) / metadata["scenarioResults"][0]["evidenceReceipts"][0]["path"]
            receipt_path.unlink()

            _, metadata_path = reporting.write_suite_report(root, metadata)
            published = json.loads(metadata_path.read_text(encoding="utf-8"))

        self.assertEqual("INFRASTRUCTURE_FAILED", published["status"])
        self.assertEqual("invalid", published["evidenceBundle"]["status"])
        self.assertTrue(
            any("missing" in value for value in published["evidenceBundle"]["diagnostics"])
        )

    def test_publication_rejects_post_audit_receipt_and_artifact_mutation(self) -> None:
        """Receipt and bound-artifact bytes remain authoritative through publication."""
        for kind in ("receipt", "artifact"):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                evidence_root = root / "runner-result"
                metadata = self._metadata(
                    "codex", "dev-coder", "PASS", evidence_root
                )
                scenario = metadata["scenarioResults"][0]
                checkpoint_root = Path(scenario["_checkpointRoot"])
                receipt_path = checkpoint_root / scenario["evidenceReceipts"][0]["path"]
                if kind == "receipt":
                    receipt_path.write_text("{}\n", encoding="utf-8")
                else:
                    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
                    artifact_path = checkpoint_root / receipt["evidence"]["path"]
                    artifact_path.write_text("mutated after runner audit\n", encoding="utf-8")

                _, metadata_path = reporting.write_suite_report(root, metadata)
                published = json.loads(metadata_path.read_text(encoding="utf-8"))

            self.assertEqual("INFRASTRUCTURE_FAILED", published["status"])
            self.assertEqual("invalid", published["evidenceBundle"]["status"])
            self.assertTrue(
                any("digest mismatch" in value for value in published["evidenceBundle"]["diagnostics"])
            )

    def test_publication_rejects_duplicate_terminal_judge_response_with_current_digest(
        self,
    ) -> None:
        """A current rollout digest cannot legitimize two eligible Judge finals."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            metadata = self._metadata(
                "codex", "dev-coder", "PASS", root / "runner-result"
            )
            self._mutate_terminal_judge_responses(metadata, "duplicate")

            _, metadata_path = reporting.write_suite_report(root, metadata)
            published = json.loads(metadata_path.read_text(encoding="utf-8"))

        self.assertEqual("INFRASTRUCTURE_FAILED", published["status"])
        self.assertEqual("invalid", published["evidenceBundle"]["status"])
        self.assertTrue(
            any(
                "exactly one eligible terminal" in value
                for value in published["evidenceBundle"]["diagnostics"]
            )
        )

    def test_publication_rejects_zero_or_mismatched_judge_terminal_response(self) -> None:
        """Publication requires one exact terminal response at the declared event index."""
        for mutation, diagnostic in (
            ("remove", "exactly one eligible terminal"),
            ("mismatch-index", "responseEventIndex"),
        ):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                metadata = self._metadata(
                    "codex", "dev-coder", "PASS", root / "runner-result"
                )
                self._mutate_terminal_judge_responses(metadata, mutation)

                _, metadata_path = reporting.write_suite_report(root, metadata)
                published = json.loads(metadata_path.read_text(encoding="utf-8"))

            self.assertEqual("INFRASTRUCTURE_FAILED", published["status"])
            self.assertTrue(
                any(
                    diagnostic in value
                    for value in published["evidenceBundle"]["diagnostics"]
                )
            )

    def test_aggregate_independently_rejects_published_duplicate_judge_terminal(
        self,
    ) -> None:
        """Aggregation re-enumerates Judge finals instead of trusting publication state."""
        for mutation, diagnostic in (
            ("duplicate", "exactly one eligible terminal"),
            ("remove", "exactly one eligible terminal"),
            ("mismatch-index", "responseEventIndex"),
        ):
            with (
                self.subTest(mutation=mutation),
                tempfile.TemporaryDirectory() as directory,
                mock.patch.object(reporting, "_suite_digest", return_value="digest"),
            ):
                root = Path(directory)
                metadata = self._metadata(
                    "codex", "dev-coder", "PASS", root / "runner-result"
                )
                self._mutate_terminal_judge_responses(metadata, mutation)
                with mock.patch.object(
                    reporting,
                    "_judge_rollout_binding_error",
                    return_value=None,
                    create=True,
                ):
                    reporting.write_suite_report(root, metadata)

                entries = reporting.aggregate_entries(
                    root, ("dev-coder",), "codex", "revision"
                )

            states = {entry["inputState"] for entry in entries}
            self.assertNotIn("CURRENT", states)
            self.assertTrue({"MISSING", "MALFORMED"} <= states)
            malformed = next(
                entry for entry in entries if entry["inputState"] == "MALFORMED"
            )
            self.assertTrue(
                any(diagnostic in value for value in malformed["diagnostics"])
            )
            self.assertEqual(
                ["suites/codex/dev-coder.manifest.json"],
                malformed["evidencePaths"],
            )
            self.assertFalse(
                any(
                    entry.get("status") == "PASS"
                    and entry.get("inputState") == "CURRENT"
                    for entry in entries
                )
            )

    def test_aggregate_classifies_null_scenario_results_as_missing_and_malformed(
        self,
    ) -> None:
        """Digest-consistent malformed metadata is bounded at the aggregate edge."""
        with (
            tempfile.TemporaryDirectory() as directory,
            mock.patch.object(reporting, "_suite_digest", return_value="digest"),
        ):
            root = Path(directory)
            reporting.write_suite_report(
                root,
                self._metadata(
                    "codex", "dev-coder", "PASS", root / "runner-result"
                ),
            )
            pointer_path = root / "suites" / "codex" / "dev-coder.manifest.json"
            pointer = json.loads(pointer_path.read_text(encoding="utf-8"))
            generation_root = (root / pointer["metadata"]).parent
            metadata_path = generation_root / "metadata.json"
            html_path = generation_root / "report.html"
            manifest_path = generation_root / "evidence" / "manifest.json"
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            original_embedded = reporting._embedded_metadata(metadata)
            metadata["scenarioResults"] = None
            metadata_content = json.dumps(metadata, indent=2, sort_keys=True) + "\n"
            html_content = html_path.read_text(encoding="utf-8").replace(
                original_embedded, reporting._embedded_metadata(metadata)
            )
            manifest_content = manifest_path.read_text(encoding="utf-8")
            generation = hashlib.sha256(
                metadata_content.encode("utf-8")
                + html_content.encode("utf-8")
                + manifest_content.encode("utf-8")
            ).hexdigest()
            replacement_root = generation_root.with_name(generation)
            generation_root.rename(replacement_root)
            metadata_path = replacement_root / "metadata.json"
            html_path = replacement_root / "report.html"
            metadata_path.write_text(metadata_content, encoding="utf-8")
            html_path.write_text(html_content, encoding="utf-8")
            pointer.update(
                {
                    "generation": generation,
                    "metadata": metadata_path.relative_to(root).as_posix(),
                    "metadataSha256": hashlib.sha256(
                        metadata_content.encode("utf-8")
                    ).hexdigest(),
                    "html": html_path.relative_to(root).as_posix(),
                    "htmlSha256": hashlib.sha256(
                        html_content.encode("utf-8")
                    ).hexdigest(),
                    "evidenceManifest": (
                        replacement_root / "evidence" / "manifest.json"
                    ).relative_to(root).as_posix(),
                }
            )
            pointer_path.write_text(
                json.dumps(pointer, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )

            entries = reporting.aggregate_entries(
                root, ("dev-coder",), "codex", "revision"
            )

        self.assertEqual(
            {"MISSING", "MALFORMED"},
            {entry["inputState"] for entry in entries},
        )

    def test_publication_requires_response_index_to_name_the_sole_judge_terminal(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            metadata = self._metadata(
                "codex", "dev-coder", "PASS", root / "runner-result"
            )
            metadata["scenarioResults"][0]["receiptAudit"]["judgeProvenance"][
                "responseEventIndex"
            ] = 0

            _, metadata_path = reporting.write_suite_report(root, metadata)
            published = json.loads(metadata_path.read_text(encoding="utf-8"))

        self.assertEqual("INFRASTRUCTURE_FAILED", published["status"])
        self.assertTrue(
            any(
                "responseEventIndex" in value
                for value in published["evidenceBundle"]["diagnostics"]
            )
        )

    def test_junie_blocked_remains_a_truthful_current_terminal_result(self) -> None:
        with (
            tempfile.TemporaryDirectory() as directory,
            mock.patch.object(reporting, "_suite_digest", return_value="digest"),
        ):
            root = Path(directory)
            reporting.write_suite_report(
                root,
                self._metadata(
                    "junie", "dev-coder", "BLOCKED", root / "runner-result"
                ),
            )

            entries = reporting.aggregate_entries(
                root, ("dev-coder",), "junie", "revision"
            )

        self.assertEqual("CURRENT", entries[0]["inputState"])
        self.assertEqual("BLOCKED", entries[0]["status"])

    def test_aggregate_revalidates_bundle_objects_before_counting_current_pass(
        self,
    ) -> None:
        """A bundle mutation after publication is visible and cannot count as CURRENT PASS."""
        with (
            tempfile.TemporaryDirectory() as directory,
            mock.patch.object(reporting, "_suite_digest", return_value="digest"),
        ):
            root = Path(directory)
            reporting.write_suite_report(
                root,
                self._metadata(
                    "codex", "dev-coder", "PASS", root / "runner-result"
                ),
            )
            pointer = json.loads(
                (root / "suites" / "codex" / "dev-coder.manifest.json").read_text(
                    encoding="utf-8"
                )
            )
            manifest = json.loads(
                (root / pointer["evidenceManifest"]).read_text(encoding="utf-8")
            )
            object_entry = next(
                entry for entry in manifest["entries"] if entry.get("bundlePath")
            )
            bundle_object = (root / pointer["metadata"]).parent / object_entry["bundlePath"]
            bundle_object.write_bytes(b"mutated after publication")

            entries = reporting.aggregate_entries(
                root, ("dev-coder",), "codex", "revision"
            )

        states = {entry["inputState"] for entry in entries}
        self.assertNotIn("CURRENT", states)
        self.assertTrue({"MISSING", "MALFORMED"} <= states)
        self.assertFalse(
            any(
                entry.get("status") == "PASS" and entry.get("inputState") == "CURRENT"
                for entry in entries
            )
        )

    def test_interrupted_generation_keeps_previous_pointer_and_report_consistent(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            reporting.write_suite_report(
                root, self._metadata("codex", "dev-coder", "PASS", root / "pass-evidence")
            )
            pointer = root / "suites" / "codex" / "dev-coder.manifest.json"
            before = pointer.read_bytes()
            real_atomic_write = reporting._atomic_write

            def fail_new_html(path: Path, content: str) -> None:
                if path.name == "report.html" and "FAIL" in content:
                    raise OSError("synthetic interruption")
                real_atomic_write(path, content)

            with mock.patch.object(
                reporting, "_atomic_write", side_effect=fail_new_html
            ):
                with self.assertRaisesRegex(OSError, "synthetic interruption"):
                    reporting.write_suite_report(
                        root, self._metadata("codex", "dev-coder", "FAIL", root / "fail-evidence")
                    )

            self.assertEqual(before, pointer.read_bytes())
            current, _ = self._current_generation(root, "codex", "dev-coder")
            self.assertIn("PASS", current.read_text(encoding="utf-8"))

    def test_aggregation_displays_missing_stale_malformed_and_mixed_harness(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            stale = self._metadata("codex", "dev-coder", "PASS", root / "codex-evidence")
            stale["sourceRevision"] = "older"
            reporting.write_suite_report(root, stale)
            reporting.write_suite_report(
                root, self._metadata("junie", "dev-coder", "BLOCKED", root / "junie-evidence")
            )
            malformed = root / "suites" / "codex" / "broken.manifest.json"
            malformed.write_text("not-json", encoding="utf-8")

            entries = reporting.aggregate_entries(
                root, ("dev-coder", "dev-verifier"), "codex", "revision"
            )

        states = {value["inputState"] for value in entries}
        self.assertTrue({"STALE", "MISSING", "MALFORMED", "MIXED_HARNESS"} <= states)

    def test_metadata_without_its_independent_html_report_is_missing(self) -> None:
        with (
            tempfile.TemporaryDirectory() as directory,
            mock.patch.object(reporting, "_suite_digest", return_value="digest"),
        ):
            root = Path(directory)
            html_path, _ = reporting.write_suite_report(
                root, self._metadata("codex", "dev-coder", "PASS", root / "evidence")
            )
            html_path.unlink()

            entries = reporting.aggregate_entries(
                root, ("dev-coder",), "codex", "revision"
            )

        self.assertEqual("MISSING", entries[0]["inputState"])

    def test_aggregation_displays_duplicate_and_incompatible_revision(self) -> None:
        with (
            tempfile.TemporaryDirectory() as directory,
            mock.patch.object(
                reporting, "_suite_digest", return_value="governed-digest"
            ),
        ):
            root = Path(directory)
            incompatible = self._metadata("codex", "dev-coder", "PASS", root / "evidence")
            incompatible["suiteDigest"] = "other-digest"
            reporting.write_suite_report(root, incompatible)
            source_pointer = root / "suites" / "codex" / "dev-coder.manifest.json"
            duplicate = root / "suites" / "archive" / "dev-coder.manifest.json"
            duplicate.parent.mkdir(parents=True)
            duplicate.write_bytes(source_pointer.read_bytes())

            entries = reporting.aggregate_entries(
                root, ("dev-coder",), "codex", "revision"
            )

        self.assertEqual("DUPLICATE", entries[0]["inputState"])

    def test_incompatible_suite_digest_is_visible_when_not_duplicate(self) -> None:
        with (
            tempfile.TemporaryDirectory() as directory,
            mock.patch.object(
                reporting, "_suite_digest", return_value="governed-digest"
            ),
        ):
            root = Path(directory)
            incompatible = self._metadata("codex", "dev-coder", "PASS", root / "evidence")
            incompatible["suiteDigest"] = "other-digest"
            reporting.write_suite_report(root, incompatible)

            entries = reporting.aggregate_entries(
                root, ("dev-coder",), "codex", "revision"
            )

        self.assertEqual("INCOMPATIBLE_REVISION", entries[0]["inputState"])

    def test_incremental_suite_replacement_preserves_unrelated_metadata(self) -> None:
        with (
            tempfile.TemporaryDirectory() as directory,
            mock.patch.object(reporting, "_suite_digest", return_value="digest"),
        ):
            root = Path(directory)
            reporting.write_suite_report(
                root, self._metadata("codex", "dev-coder", "PASS", root / "coder-pass-evidence")
            )
            _, unrelated = reporting.write_suite_report(
                root, self._metadata("codex", "dev-verifier", "PASS", root / "verifier-evidence")
            )
            before = unrelated.read_bytes()
            reporting.write_suite_report(
                root, self._metadata("codex", "dev-coder", "FAIL", root / "coder-fail-evidence")
            )
            reporting.rebuild_global(
                root, ("dev-coder", "dev-verifier"), "codex", "revision"
            )

            self.assertEqual(before, unrelated.read_bytes())
            aggregate = self._embedded_json(
                (root / "index.html").read_text(encoding="utf-8")
            )
            self.assertEqual({"CURRENT": 2}, aggregate["counts"])
            self.assertEqual(1, aggregate["terminalStatusCounts"]["PASS"])
            self.assertEqual(1, aggregate["terminalStatusCounts"]["FAIL"])

    def test_incremental_terminal_totals_follow_fail_blocked_and_stale(self) -> None:
        with (
            tempfile.TemporaryDirectory() as directory,
            mock.patch.object(reporting, "_suite_digest", return_value="digest"),
        ):
            root = Path(directory)
            for status in ("PASS", "FAIL", "BLOCKED", "STALE"):
                reporting.write_suite_report(
                    root, self._metadata("codex", "dev-coder", status, root / f"{status.lower()}-evidence")
                )
                reporting.rebuild_global(root, ("dev-coder",), "codex", "revision")
                aggregate = self._embedded_json(
                    (root / "index.html").read_text(encoding="utf-8")
                )
                with self.subTest(status=status):
                    self.assertEqual(1, aggregate["terminalStatusCounts"][status])
                    self.assertEqual(
                        1,
                        sum(aggregate["terminalStatusCounts"].values()),
                    )

    def test_report_only_rebuild_never_executes_a_harness(self) -> None:
        with (
            tempfile.TemporaryDirectory() as directory,
            mock.patch.object(reporting, "_suite_digest", return_value="digest"),
            mock.patch.object(reporting.subprocess, "run") as process,
        ):
            root = Path(directory)
            reporting.write_suite_report(
                root, self._metadata("codex", "dev-coder", "PASS", root / "evidence")
            )

            output = reporting.rebuild_global(root, ("dev-coder",), "codex", "revision")

            process.assert_not_called()
            self.assertTrue(output.is_file())

    def test_full_junie_selection_requires_explicit_operator_choice(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "requires --allow-full-junie"):
                reporting.run_suites(
                    "junie", (), Path(directory), executor=lambda *args: None
                )
            with self.assertRaisesRegex(ValueError, "requires --allow-full-junie"):
                reporting.run_suites(
                    "junie",
                    reporting.catalog_suite_ids(),
                    Path(directory),
                    executor=lambda *args: None,
                )

    def test_identity_evidence_is_not_reported_as_model_judge_evidence(self) -> None:
        execution = reporting.SuiteExecution(
            0,
            {
                "results": [
                    {
                        "report": {
                            "runs": [
                                {
                                    "suite": "dev-coder",
                                    "scenarioResults": [
                                        {
                                            "scenario": "happy",
                                            "status": "PASS",
                                            "targetInvoked": True,
                                            "judgeInvoked": True,
                                            "identityEvidence": ["identity-only"],
                                            "evidence": ["general"],
                                        }
                                    ],
                                }
                            ]
                        }
                    }
                ]
            },
        )

        with tempfile.TemporaryDirectory() as directory:
            metadata = reporting.suite_metadata(
                "codex",
                "dev-coder",
                execution,
                source_revision="revision",
                suite_digest="digest",
                started_at="2026-07-19T00:00:00Z",
                finished_at="2026-07-19T00:00:01Z",
                elapsed_seconds=1,
                evidence_root=Path(directory),
            )

        self.assertEqual([], metadata["modelJudgeEvidence"])
        self.assertNotIn("identity-only", metadata["modelJudgeEvidence"])
        self.assertTrue(
            any(
                "Judge receipts unavailable" in value
                for value in metadata["omissions"]
            )
        )

    @classmethod
    def _execution(cls, suite_id: str, evidence_root: Path) -> object:
        metadata = cls._metadata("codex", suite_id, "PASS", evidence_root)
        return reporting.SuiteExecution(
            0,
            {
                "results": [
                    {
                        "runIdentity": metadata["scenarioResults"][0]["_runIdentity"],
                        "evidence": {
                            "checkpoints": metadata["scenarioResults"][0]["_checkpointRoot"],
                            "identity": metadata["scenarioResults"][0]["_identityAudit"]["path"],
                            "identitySha256": metadata["scenarioResults"][0]["_identityAudit"]["sha256"],
                        },
                        "report": {
                            "runs": [
                                {
                                    "suite": suite_id,
                                    "scenarioResults": metadata["scenarioResults"],
                                }
                            ]
                        }
                    }
                ]
            },
        )

    def test_suite_metadata_demotes_unsupported_pass_and_preserves_critical_skip(self) -> None:
        """Aggregate reporting cannot turn missing governed receipts into a PASS."""
        with tempfile.TemporaryDirectory() as directory:
            evidence_root = Path(directory)
            unsupported = self._execution("dev-coder", evidence_root)
            unsupported.summary["results"][0]["report"]["runs"][0]["scenarioResults"][0][
                "receiptAudit"
            ]["status"] = "invalid"
            metadata = reporting.suite_metadata(
                "codex", "dev-coder", unsupported,
                source_revision="revision", suite_digest="digest",
                started_at="2026-07-19T00:00:00Z", finished_at="2026-07-19T00:00:01Z",
                elapsed_seconds=1, evidence_root=evidence_root,
            )
        self.assertEqual("INFRASTRUCTURE_FAILED", metadata["status"])
        self.assertEqual("INFRASTRUCTURE_FAILED", metadata["scenarioResults"][0]["status"])
        self.assertTrue(any("unsupported terminal verdicts demoted" in value for value in metadata["omissions"]))

        with tempfile.TemporaryDirectory() as directory:
            evidence_root = Path(directory)
            critical_skip = self._execution("dev-coder", evidence_root)
            scenario = critical_skip.summary["results"][0]["report"]["runs"][0]["scenarioResults"][0]
            scenario["status"] = "FAIL"
            scenario["judgeInvoked"] = False
            scenario["modelJudgeEvidence"] = []
            scenario["receiptAudit"]["deterministicChecks"][0]["verdict"] = "failed"
            scenario["receiptAudit"]["judgeDisposition"] = "skipped-critical-failure"
            scenario["receiptAudit"]["failedCriticalCheck"] = "harness-agent-identity"
            metadata = reporting.suite_metadata(
                "codex", "dev-coder", critical_skip,
                source_revision="revision", suite_digest="digest",
                started_at="2026-07-19T00:00:00Z", finished_at="2026-07-19T00:00:01Z",
                elapsed_seconds=1, evidence_root=evidence_root,
            )
        self.assertEqual("FAIL", metadata["status"])
        self.assertFalse(any("unsupported terminal verdicts" in value for value in metadata["omissions"]))

    @staticmethod
    def _metadata(
        harness: str,
        suite_id: str,
        status: str,
        evidence_root: Path,
    ) -> dict[str, object]:
        run_identity = f"{harness}-batch-01-test"
        scenario_id = "happy"
        checkpoint_root = evidence_root / "batch-01.checkpoints"
        artifacts = checkpoint_root / suite_id / scenario_id / "artifacts"
        receipts = checkpoint_root / suite_id / scenario_id / "receipts"
        sessions = evidence_root / "batch-01.sessions"
        artifacts.mkdir(parents=True)
        receipts.mkdir()
        sessions.mkdir(parents=True)
        deterministic_artifact = artifacts / "harness-agent-identity.log"
        deterministic_artifact.write_text("retained deterministic evidence\n", encoding="utf-8")
        deterministic_receipt = receipts / "deterministic-harness-agent-identity.json"
        deterministic_receipt.write_text(
            json.dumps(
                {
                    "schema": "dev-methodology-agent-suite-evidence-receipt",
                    "version": 1,
                    "eventType": "deterministic-check-disposition",
                    "runIdentity": run_identity,
                    "suite": suite_id,
                    "scenario": scenario_id,
                    "checkId": "harness-agent-identity",
                    "critical": True,
                    "verdict": "passed",
                    "evidence": {
                        "path": deterministic_artifact.relative_to(checkpoint_root).as_posix(),
                        "sha256": hashlib.sha256(deterministic_artifact.read_bytes()).hexdigest(),
                    },
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        disposition = {
            "PASS": "passed",
            "FAIL": "failed",
            "BLOCKED": "blocked",
            "STALE": "stale",
        }[status]
        judge_invocation = f"{suite_id.replace('-', '_')}_suite_judge"
        judge_output = artifacts / "judge-output.json"
        judge_response = json.dumps(
            {
                "schema": "dev-methodology-agent-suite-judge-output",
                "version": 1,
                "runIdentity": run_identity,
                "suite": suite_id,
                "scenario": scenario_id,
                "judgeInvocation": judge_invocation,
                "disposition": disposition,
            },
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        judge_output.write_bytes(judge_response)
        judge_receipt = receipts / "judge-disposition.json"
        judge_receipt.write_text(
            json.dumps(
                {
                    "schema": "dev-methodology-agent-suite-evidence-receipt",
                    "version": 1,
                    "eventType": "judge-disposition",
                    "runIdentity": run_identity,
                    "suite": suite_id,
                    "scenario": scenario_id,
                    "judgeInvocation": judge_invocation,
                    "disposition": disposition,
                    "evidence": {
                        "path": judge_output.relative_to(checkpoint_root).as_posix(),
                        "sha256": hashlib.sha256(judge_response).hexdigest(),
                    },
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        session_id = f"judge-session-{suite_id}-{status.lower()}"
        parent_session_id = f"supervisor-session-{suite_id}"
        rollout = sessions / f"rollout-{session_id}.jsonl"
        rollout.write_text(
            "\n".join(
                json.dumps(event)
                for event in (
                    {
                        "timestamp": "2026-07-19T00:00:00Z",
                        "type": "session_meta",
                        "payload": {
                            "id": session_id,
                            "parent_thread_id": parent_session_id,
                            "agent_role": judge_invocation,
                            "source": {
                                "subagent": {
                                    "thread_spawn": {
                                        "depth": 2,
                                        "agent_role": judge_invocation,
                                    }
                                }
                            },
                        },
                    },
                    {
                        "timestamp": "2026-07-19T00:00:01Z",
                        "type": "response_item",
                        "payload": {
                            "type": "message",
                            "role": "assistant",
                            "content": [
                                {
                                    "type": "output_text",
                                    "text": judge_response.decode("utf-8"),
                                }
                            ],
                            "phase": "final_answer",
                        },
                    },
                )
            )
            + "\n",
            encoding="utf-8",
        )
        response_digest = hashlib.sha256(judge_response).hexdigest()
        response_path = sessions / "responses" / f"{response_digest}.json"
        response_path.parent.mkdir()
        response_path.write_bytes(judge_response)
        references = [
            {
                "path": deterministic_receipt.relative_to(checkpoint_root).as_posix(),
                "sha256": hashlib.sha256(deterministic_receipt.read_bytes()).hexdigest(),
            },
            {
                "path": judge_receipt.relative_to(checkpoint_root).as_posix(),
                "sha256": hashlib.sha256(judge_receipt.read_bytes()).hexdigest(),
            },
        ]
        provenance = {
            "status": "verified",
            "sessionId": session_id,
            "parentSessionId": parent_session_id,
            "invocation": judge_invocation,
            "runIdentity": run_identity,
            "suite": suite_id,
            "scenario": scenario_id,
            "rolloutPath": rollout.relative_to(evidence_root).as_posix(),
            "rolloutSha256": hashlib.sha256(rollout.read_bytes()).hexdigest(),
            "responseEventIndex": 1,
            "responsePath": response_path.relative_to(evidence_root).as_posix(),
            "responseSha256": response_digest,
            "outputPath": judge_output.relative_to(evidence_root).as_posix(),
            "outputSha256": response_digest,
            "disposition": disposition,
        }
        identity_path = evidence_root / "batch-01.identity.json"
        identity_path.write_text(
            json.dumps(
                {
                    "scenarioBindings": [
                        {
                            "suite": suite_id,
                            "scenario": scenario_id,
                            "kind": "judge",
                            "invocation": judge_invocation,
                            "sessionId": session_id,
                            "parentSessionId": parent_session_id,
                        }
                    ]
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        receipt_audit = {
            "status": "verified",
            "runIdentity": run_identity,
            "deterministicChecks": [
                {
                    "checkId": "harness-agent-identity",
                    "critical": True,
                    "verdict": "passed",
                }
            ],
            "judgeDisposition": disposition,
            "judgeOutput": {
                "path": judge_output.relative_to(checkpoint_root).as_posix(),
                "sha256": response_digest,
            },
            "judgeProvenance": provenance,
            "failedCriticalCheck": None,
            "diagnostics": [],
        }
        return {
            "schema": reporting._SCHEMA,
            "version": 1,
            "identity": f"{harness}:{suite_id}",
            "harness": harness,
            "suite": suite_id,
            "sourceRevision": "revision",
            "suiteDigest": "digest",
            "startedAtUtc": "2026-07-19T00:00:00Z",
            "finishedAtUtc": "2026-07-19T00:00:01Z",
            "elapsedSeconds": 1.0,
            "status": status,
            "scenarioResults": [
                {
                    "scenario": "happy",
                    "status": status,
                    "targetInvoked": True,
                    "judgeInvoked": True,
                    "evidence": ["proof"],
                    "deterministicEvidence": ["gates"],
                    "modelJudgeEvidence": ["judge-verdict"],
                    "evidenceReceipts": references,
                    "receiptAudit": receipt_audit,
                    "_checkpointRoot": str(checkpoint_root),
                    "_runIdentity": run_identity,
                    "_identityAudit": {
                        "path": str(identity_path),
                        "sha256": hashlib.sha256(identity_path.read_bytes()).hexdigest(),
                    },
                }
            ],
            "deterministicEvidence": ["proof"],
            "modelJudgeEvidence": ["judge"],
            "evidenceReceipts": references,
            "receiptAudits": [receipt_audit],
            "omissions": [],
            "evidenceRoot": str(evidence_root),
            "runnerExitCode": 0,
            "runnerStderr": "",
            "machine": {
                "platform": "synthetic",
                "architecture": "test",
                "python": "3.11",
            },
        }

    @staticmethod
    def _mutate_terminal_judge_responses(
        metadata: dict[str, object], mutation: str
    ) -> None:
        scenario = metadata["scenarioResults"][0]
        provenance = scenario["receiptAudit"]["judgeProvenance"]
        rollout = Path(str(metadata["evidenceRoot"])) / provenance["rolloutPath"]
        events = [
            json.loads(line)
            for line in rollout.read_text(encoding="utf-8").splitlines()
        ]
        response_index = provenance["responseEventIndex"]
        if mutation == "duplicate":
            duplicate = json.loads(json.dumps(events[response_index]))
            duplicate["timestamp"] = "2026-07-19T00:00:02Z"
            events.append(duplicate)
        elif mutation == "remove":
            events.pop(response_index)
        elif mutation == "mismatch-index":
            provenance["responseEventIndex"] = 0
        else:
            raise ValueError(f"unsupported terminal response mutation: {mutation}")
        rollout.write_text(
            "\n".join(json.dumps(event) for event in events) + "\n",
            encoding="utf-8",
        )
        provenance["rolloutSha256"] = hashlib.sha256(
            rollout.read_bytes()
        ).hexdigest()

    @staticmethod
    def _embedded_json(rendered: str) -> dict[str, object]:
        prefix = '<script id="report-metadata" type="application/json">'
        return json.loads(rendered.split(prefix, 1)[1].split("</script>", 1)[0])

    @staticmethod
    def _current_generation(
        root: Path, harness: str, suite_id: str
    ) -> tuple[Path, Path]:
        pointer = json.loads(
            (root / "suites" / harness / f"{suite_id}.manifest.json").read_text(
                encoding="utf-8"
            )
        )
        return root / pointer["html"], root / pointer["metadata"]

    @staticmethod
    @contextlib.contextmanager
    def _stable_sources() -> object:
        with (
            mock.patch.object(reporting, "_source_revision", return_value="revision"),
            mock.patch.object(reporting, "_suite_digest", return_value="digest"),
        ):
            yield


if __name__ == "__main__":
    unittest.main()
