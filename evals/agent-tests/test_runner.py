# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Verifies bounded scheduling, validation, timing, evidence retention, and cleanup for the agent-suite runner.
# Governing design: evals/agent-tests/implementation-plan.md

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import time
import unittest
from pathlib import Path


_RUNNER_PATH = Path(__file__).with_name("runner.py")
_SPEC = importlib.util.spec_from_file_location("agent_suite_runner", _RUNNER_PATH)
assert _SPEC is not None and _SPEC.loader is not None
runner = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = runner
_SPEC.loader.exec_module(runner)


class AgentSuiteRunnerTests(unittest.TestCase):
    """Protect the runner contract without invoking a live model."""

    def test_selects_one_suite_and_one_scenario(self) -> None:
        """A caller can narrow execution to one declared scenario."""
        catalog = {
            "alpha": runner._Suite(
                suite_id="alpha",
                priority=1,
                path=Path("alpha"),
                manifest={"execution": {"maximumActiveChildren": 1, "nestedAgentLimit": 0}},
                scenarios=({"id": "happy", "status": "executable", "executableCase": "fixture"},),
            )
        }

        selected = runner._select_runs(catalog, ("alpha",), ("alpha:happy",))

        self.assertEqual(["alpha"], [run.suite.suite_id for run in selected])
        self.assertEqual(("happy",), selected[0].scenario_ids)

    def test_fifth_supervisor_is_queued_in_a_second_batch(self) -> None:
        """No batch can exceed the four-supervisor repository limit."""
        runs = tuple(self._run_spec(f"suite-{index}", index) for index in range(1, 6))

        batches = runner._batch_runs(runs, maximum=4)

        self.assertEqual([4, 1], [len(batch) for batch in batches])

    def test_nested_child_limit_rejects_more_than_temporary_tenth_agent(self) -> None:
        """A suite cannot declare more than one nested canonical dependency."""
        invalid = self._suite("invalid", nested_limit=2)

        with self.assertRaisesRegex(ValueError, "nestedAgentLimit"):
            runner._validate_suite(invalid)

    def test_partial_batch_failure_is_retained_with_later_results(self) -> None:
        """One failed batch does not erase earlier evidence or prevent later batches."""
        batches = (
            (self._run_spec("one", 1),),
            (self._run_spec("two", 2),),
            (self._run_spec("three", 3),),
        )

        def execute(batch: tuple[object, ...], batch_number: int) -> dict[str, object]:
            if batch_number == 2:
                raise RuntimeError("synthetic failure")
            return {"batch": batch_number, "status": "completed", "count": len(batch)}

        results = runner._execute_batches(batches, execute)

        self.assertEqual(["completed", "infrastructure-failed", "completed"], [result["status"] for result in results])
        self.assertIn("synthetic failure", str(results[1]["error"]))
        self.assertTrue(all(str(result["startedAtUtc"]).endswith("Z") for result in results))
        self.assertTrue(all(float(result["elapsedSeconds"]) >= 0 for result in results))

    def test_partial_results_inside_one_batch_remain_addressable(self) -> None:
        """A failed scenario does not erase completed scenario results from the same batch."""
        batch = (self._run_spec("one", 1), self._run_spec("two", 2))
        report = {
            "runs": [
                self._suite_report("one", "PASS"),
                self._suite_report("two", "FAIL"),
            ],
            "batchCleanup": "clean",
            "residualRisk": "none",
        }

        audited = runner._audit_report(batch, report)

        self.assertEqual(["PASS", "FAIL"], [item["scenarioResults"][0]["status"] for item in audited])

    def test_temporary_run_directory_is_removed_after_failure(self) -> None:
        """Disposable authentication, agents, and workspace state do not survive a run."""
        retained_path: Path | None = None
        with self.assertRaisesRegex(RuntimeError, "stop"):
            with runner._temporary_run_root("cleanup-test") as run_root:
                retained_path = run_root
                (run_root / "marker").write_text("synthetic", encoding="utf-8")
                raise RuntimeError("stop")

        assert retained_path is not None
        self.assertFalse(retained_path.exists())

    def test_extracts_coordinator_report_from_jsonl(self) -> None:
        """The last structured agent message becomes the governed batch report."""
        report = {"runs": [{"suite": "alpha", "status": "PASS"}]}
        stream = "\n".join(
            (
                json.dumps({"type": "thread.started", "thread_id": "thread-1"}),
                json.dumps({"type": "item.completed", "item": {"type": "agent_message", "text": json.dumps(report)}}),
            )
        )

        self.assertEqual(report, runner._extract_coordinator_report(stream))

    def test_exact_custom_agent_session_is_required(self) -> None:
        """A scenario task label cannot satisfy the staged target identity gate."""
        with tempfile.TemporaryDirectory() as temporary:
            codex_home = Path(temporary)
            sessions = codex_home / "sessions"
            sessions.mkdir()
            self._write_rollout(sessions / "rollout-supervisor.jsonl", "suite_supervisor", depth=1)
            self._write_rollout(sessions / "rollout-generic.jsonl", "scenario_target", depth=2)
            staged = (
                runner._StagedAgent("suite_supervisor", Path("supervisor.toml"), "instructions", "a" * 64),
                runner._StagedAgent("target_agent", Path("target.toml"), "instructions", "b" * 64),
            )

            with self.assertRaisesRegex(RuntimeError, "target_agent"):
                runner._audit_identity(staged, codex_home, {"suite_supervisor", "target_agent"})

    def test_overlapping_supervisor_children_fail_runtime_audit(self) -> None:
        """Retained session intervals enforce one active child per supervisor."""
        sessions = (
            runner._Session("supervisor", None, "suite_supervisor", 1, 0.0, 10.0),
            runner._Session("target", "supervisor", "target_agent", 2, 1.0, 6.0),
            runner._Session("judge", "supervisor", "suite_judge", 2, 5.0, 9.0),
        )

        with self.assertRaisesRegex(RuntimeError, "overlapping children"):
            runner._audit_session_concurrency(sessions, maximum_threads=9)

    def test_missing_applicable_skill_is_a_preflight_error(self) -> None:
        """Target staging fails closed when an applicable skill package is absent."""
        suite = self._suite("missing-skill")
        scenario = dict(suite.scenarios[0])
        scenario["targetSkills"] = ["definitely-missing-skill"]
        suite = runner._Suite(suite.suite_id, suite.priority, suite.path, suite.manifest, (scenario, scenario, scenario))

        with self.assertRaisesRegex(ValueError, "definitely-missing-skill"):
            runner._validate_target_skills(suite, ("happy",), Path("/definitely/missing"))

    def test_controlled_environment_does_not_inherit_host_credentials(self) -> None:
        """Only process-location and locale values cross the host boundary."""
        environment = runner._controlled_environment(Path("/tmp/home"), Path("/tmp/codex"), Path("/tmp/work"))

        self.assertNotIn("CODEX_AUTH_FILE", environment)
        self.assertNotIn("OPENAI_API_KEY", environment)
        self.assertEqual("/tmp/codex", environment["CODEX_HOME"])

    def test_timeout_retains_output_and_stops_the_process_group(self) -> None:
        """A timed-out harness returns bounded evidence instead of raising before retention."""
        started = time.monotonic()
        result = runner._run_process(
            (sys.executable, "-c", "import time; print('started', flush=True); time.sleep(5)"),
            Path.cwd(),
            runner._controlled_environment(Path("/tmp/home"), Path("/tmp/codex"), Path("/tmp/work")),
            timeout_seconds=0.1,
        )

        self.assertEqual(124, result["exitCode"])
        self.assertIn("started", result["stdout"])
        self.assertLess(time.monotonic() - started, 2.0)

    @staticmethod
    def _suite(suite_id: str, nested_limit: int = 0) -> object:
        return runner._Suite(
            suite_id=suite_id,
            priority=1,
            path=Path(suite_id),
            manifest={
                "id": suite_id,
                "execution": {
                    "maximumActiveChildren": 1,
                    "nestedAgentLimit": nested_limit,
                    "scenarioCatalog": "scenarios.yaml",
                    "supervisorInvocation": "suite_supervisor",
                    "targetInvocation": "target_agent",
                    "judgeInvocation": "suite_judge",
                },
                "target": {"allowedAgentDependencies": ["dependency"]},
            },
            scenarios=({"id": "happy", "status": "executable", "executableCase": "fixture"},),
        )

    @classmethod
    def _run_spec(cls, suite_id: str, priority: int) -> object:
        suite = cls._suite(suite_id)
        suite = runner._Suite(
            suite_id=suite.suite_id,
            priority=priority,
            path=suite.path,
            manifest=suite.manifest,
            scenarios=suite.scenarios,
        )
        return runner._RunSpec(suite=suite, scenario_ids=("happy",))

    @staticmethod
    def _suite_report(suite_id: str, status: str) -> dict[str, object]:
        return {
            "suite": suite_id,
            "scenarioResults": [
                {
                    "scenario": "happy",
                    "status": status,
                    "identityEvidence": ["thread-bound"],
                    "cleanup": "clean",
                    "evidence": ["synthetic"],
                }
            ],
            "maximumActiveChildrenObserved": 1,
            "cleanup": "clean",
        }

    @staticmethod
    def _write_rollout(path: Path, invocation: str, depth: int) -> None:
        session_id = path.stem
        parent = "root" if depth == 1 else "rollout-supervisor"
        events = (
            {"timestamp": "2026-07-17T00:00:00Z", "type": "session_meta", "payload": {
                "id": session_id,
                "parent_thread_id": parent,
                "agent_path": f"/root/{invocation}",
                "source": {"subagent": {"thread_spawn": {"depth": depth, "agent_path": f"/root/{invocation}"}}},
            }},
            {"timestamp": "2026-07-17T00:00:01Z", "type": "event_msg", "payload": {"type": "turn_complete"}},
        )
        path.write_text("\n".join(json.dumps(event) for event in events) + "\n", encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
