# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Verifies bounded agent-suite scheduling and durable deterministic HTML aggregation.
# Governing design: backlog/feature-backlog/automate-parallel-agent-test-reporting.md

from __future__ import annotations

import importlib.util
import contextlib
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
        self.assertEqual(
            1,
            reporting.resolve_workers(
                10,
                reporting.HostResources(
                    processor_count=2, available_memory_bytes=1024**3
                ),
            ),
        )
        with self.assertRaisesRegex(ValueError, "between 1 and 4"):
            reporting.resolve_workers(2, resources, override=5)

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
            return self._execution(suite_id)

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
            return self._execution(suite_id)

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
                (Path(directory) / "suites" / "codex" / "dev-coder.html").is_file()
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
            return self._execution(suite_id)

        with tempfile.TemporaryDirectory() as directory, self._stable_sources():
            root = Path(directory)
            results = reporting.run_suites(
                "codex",
                ("dev-coder", "dev-code-reviewer"),
                root,
                executor=executor,
                resources=reporting.HostResources(8, 16 * 1024**3),
            )

            failed = json.loads(
                (
                    root / "suites" / "codex" / "dev-code-reviewer.metadata.json"
                ).read_text(encoding="utf-8")
            )
        self.assertEqual(
            ["PASS", "INFRASTRUCTURE_FAILED"], [value["status"] for value in results]
        )
        self.assertIn("synthetic harness failure", failed["runnerStderr"])

    def test_suite_report_is_self_contained_and_carries_machine_metadata(self) -> None:
        metadata = self._metadata("codex", "dev-coder", "PASS")

        rendered = reporting.render_suite_html(metadata)

        self.assertIn('<script id="report-metadata" type="application/json">', rendered)
        self.assertIn('<meta name="viewport"', rendered)
        self.assertIn('<th scope="col">Scenario</th>', rendered)
        self.assertNotIn("http://", rendered)
        self.assertNotIn("https://", rendered)

    def test_atomic_report_replacement_does_not_leave_temporary_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            html_path, metadata_path = reporting.write_suite_report(
                root, self._metadata("codex", "dev-coder", "PASS")
            )
            reporting.write_suite_report(
                root, self._metadata("codex", "dev-coder", "FAIL")
            )

            self.assertIn("FAIL", html_path.read_text(encoding="utf-8"))
            self.assertEqual(
                "FAIL", json.loads(metadata_path.read_text(encoding="utf-8"))["status"]
            )
            self.assertEqual([], list(metadata_path.parent.glob(".*.metadata.json.*")))

    def test_aggregation_displays_missing_stale_malformed_and_mixed_harness(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            stale = self._metadata("codex", "dev-coder", "PASS")
            stale["sourceRevision"] = "older"
            reporting.write_suite_report(root, stale)
            reporting.write_suite_report(
                root, self._metadata("junie", "dev-coder", "PASS")
            )
            malformed = root / "suites" / "codex" / "broken.metadata.json"
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
            _, metadata = reporting.write_suite_report(
                root, self._metadata("codex", "dev-coder", "PASS")
            )
            metadata.with_name("dev-coder.html").unlink()

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
            incompatible = self._metadata("codex", "dev-coder", "PASS")
            incompatible["suiteDigest"] = "other-digest"
            reporting.write_suite_report(root, incompatible)
            duplicate = root / "suites" / "archive" / "dev-coder.metadata.json"
            duplicate.parent.mkdir(parents=True)
            duplicate.write_text(json.dumps(incompatible), encoding="utf-8")

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
            incompatible = self._metadata("codex", "dev-coder", "PASS")
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
                root, self._metadata("codex", "dev-coder", "PASS")
            )
            _, unrelated = reporting.write_suite_report(
                root, self._metadata("codex", "dev-verifier", "PASS")
            )
            before = unrelated.read_bytes()
            reporting.write_suite_report(
                root, self._metadata("codex", "dev-coder", "FAIL")
            )
            reporting.rebuild_global(
                root, ("dev-coder", "dev-verifier"), "codex", "revision"
            )

            self.assertEqual(before, unrelated.read_bytes())
            aggregate = self._embedded_json(
                (root / "index.html").read_text(encoding="utf-8")
            )
            self.assertEqual({"CURRENT": 2}, aggregate["counts"])

    def test_report_only_rebuild_never_executes_a_harness(self) -> None:
        with (
            tempfile.TemporaryDirectory() as directory,
            mock.patch.object(reporting, "_suite_digest", return_value="digest"),
            mock.patch.object(reporting.subprocess, "run") as process,
        ):
            root = Path(directory)
            reporting.write_suite_report(
                root, self._metadata("codex", "dev-coder", "PASS")
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

    @staticmethod
    def _execution(suite_id: str) -> object:
        return reporting.SuiteExecution(
            0,
            {
                "results": [
                    {
                        "report": {
                            "runs": [
                                {
                                    "suite": suite_id,
                                    "scenarioResults": [
                                        {
                                            "scenario": "happy",
                                            "status": "PASS",
                                            "evidence": ["deterministic"],
                                            "identityEvidence": ["judge"],
                                        }
                                    ],
                                }
                            ]
                        }
                    }
                ]
            },
        )

    @staticmethod
    def _metadata(harness: str, suite_id: str, status: str) -> dict[str, object]:
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
                {"scenario": "happy", "status": status, "evidence": ["proof"]}
            ],
            "deterministicEvidence": ["proof"],
            "modelJudgeEvidence": ["judge"],
            "omissions": [],
            "evidenceRoot": "/synthetic/evidence",
            "runnerExitCode": 0,
            "runnerStderr": "",
            "machine": {
                "platform": "synthetic",
                "architecture": "test",
                "python": "3.11",
            },
        }

    @staticmethod
    def _embedded_json(rendered: str) -> dict[str, object]:
        prefix = '<script id="report-metadata" type="application/json">'
        return json.loads(rendered.split(prefix, 1)[1].split("</script>", 1)[0])

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
