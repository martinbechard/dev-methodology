# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Verifies bounded scheduling, validation, timing, evidence retention, and cleanup for the agent-suite runner.
# Governing design: evals/agent-tests/implementation-plan.md

from __future__ import annotations

import importlib.util
import json
import os
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
            supervisor_marker = "AGENT_INSTRUCTION_BINDING_suite_supervisor_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
            target_marker = "AGENT_INSTRUCTION_BINDING_target_agent_bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
            self._write_rollout(
                sessions / "rollout-supervisor.jsonl", "suite_supervisor", depth=1, marker=supervisor_marker
            )
            self._write_rollout(sessions / "rollout-generic.jsonl", "scenario_target", depth=2)
            staged = (
                runner._StagedAgent(
                    "suite_supervisor", Path("supervisor.toml"), "instructions", "a" * 64, supervisor_marker
                ),
                runner._StagedAgent("target_agent", Path("target.toml"), "instructions", "b" * 64, target_marker),
            )

            with self.assertRaisesRegex(RuntimeError, "target_agent"):
                runner._audit_identity(staged, codex_home, {"suite_supervisor": 1, "target_agent": 1})

    def test_agent_path_without_instruction_canary_fails_identity_audit(self) -> None:
        """A custom-looking path cannot substitute for observed staged instructions."""
        with tempfile.TemporaryDirectory() as temporary:
            codex_home = Path(temporary)
            sessions = codex_home / "sessions"
            sessions.mkdir()
            self._write_rollout(sessions / "rollout-target.jsonl", "target_agent", depth=2)
            target_marker = "AGENT_INSTRUCTION_BINDING_target_agent_bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
            staged = (
                runner._StagedAgent("target_agent", Path("target.toml"), "instructions", "b" * 64, target_marker),
            )

            with self.assertRaisesRegex(RuntimeError, "instruction binding"):
                runner._audit_identity(staged, codex_home, {"target_agent": 1})

    def test_arbitrary_canary_message_does_not_bind_instructions(self) -> None:
        """The marker must be the first exact tool call with matching output."""
        with tempfile.TemporaryDirectory() as temporary:
            codex_home = Path(temporary)
            sessions = codex_home / "sessions"
            sessions.mkdir()
            marker = "AGENT_INSTRUCTION_BINDING_target_agent_bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
            self._write_rollout(
                sessions / "rollout-target.jsonl", "target_agent", depth=2, marker=marker, arbitrary_message=True
            )
            staged = (runner._StagedAgent("target_agent", Path("target.toml"), "instructions", "b" * 64, marker),)

            with self.assertRaisesRegex(RuntimeError, "instruction binding"):
                runner._audit_identity(staged, codex_home, {"target_agent": 1})

    def test_canary_parser_rejects_wrong_tool_and_command_superset(self) -> None:
        """Only the execution tool's exact command can become binding evidence."""
        command = 'python3 -c "print(\'AGENT_INSTRUCTION_BINDING_target_agent_bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\')"'
        wrong_tool = {
            "type": "custom_tool_call",
            "name": "not_exec",
            "input": f"const r = await tools.exec_command({{cmd:{json.dumps(command)}}}); text(r.output);",
        }
        command_superset = {
            "type": "custom_tool_call",
            "name": "exec",
            "input": (
                "const r = await tools.exec_command({cmd:"
                f"{json.dumps(command + ' extra')}"
                "}); text(r.output);"
            ),
        }

        self.assertIsNone(runner._exact_exec_command(wrong_tool))
        self.assertNotEqual(command, runner._exact_exec_command(command_superset))

    def test_staging_instruments_inline_closing_instruction_delimiter(self) -> None:
        """Generated adapters may close developer instructions after the final text on the same line."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source.toml"
            agent_root = root / "agents"
            agent_root.mkdir()
            source.write_text(
                'name = "target_agent"\ndeveloper_instructions = """governed instructions---"""\n',
                encoding="utf-8",
            )

            staged = runner._copy_agent(source, "target_agent", agent_root)
            loaded = runner.tomllib.loads((agent_root / "target_agent.toml").read_text(encoding="utf-8"))

        self.assertIn(staged.instruction_marker, loaded["developer_instructions"])

    def test_staged_agents_are_registered_as_codex_config_files(self) -> None:
        """A task name alone cannot replace the custom-agent config registration."""
        staged = (
            runner._StagedAgent(
                "target_agent", Path("target.toml"), "instructions", "a" * 64, "binding-marker"
            ),
        )

        arguments = runner._agent_registration_arguments(staged, Path("/tmp/codex-home"))

        self.assertEqual("-c", arguments[0])
        self.assertIn("agents.target_agent.config_file=", arguments[1])
        self.assertIn("/tmp/codex-home/agents/target_agent.toml", arguments[1])

    def test_overlapping_supervisor_children_fail_runtime_audit(self) -> None:
        """Retained session intervals enforce one active child per supervisor."""
        sessions = (
            runner._Session("supervisor", None, "suite_supervisor", 1, 0.0, 10.0, frozenset()),
            runner._Session("target", "supervisor", "target_agent", 2, 1.0, 6.0, frozenset()),
            runner._Session("judge", "supervisor", "suite_judge", 2, 5.0, 9.0, frozenset()),
        )

        with self.assertRaisesRegex(RuntimeError, "overlapping children"):
            runner._audit_session_concurrency(sessions, maximum_threads=9)

    def test_more_than_four_supervisors_fail_runtime_audit(self) -> None:
        """Retained runtime evidence enforces the repository supervisor ceiling."""
        sessions = tuple(
            runner._Session(f"supervisor-{index}", "root", f"suite_{index}", 1, 0.0, 2.0, frozenset())
            for index in range(5)
        )

        with self.assertRaisesRegex(RuntimeError, "Supervisor concurrency limit"):
            runner._audit_session_concurrency(sessions, maximum_threads=9)

    def test_overlapping_nested_dependencies_fail_runtime_audit(self) -> None:
        """Only one depth-three dependency may run anywhere in a batch."""
        sessions = (
            runner._Session("nested-one", "target-one", "dependency", 3, 1.0, 5.0, frozenset()),
            runner._Session("nested-two", "target-two", "dependency", 3, 2.0, 4.0, frozenset()),
        )

        with self.assertRaisesRegex(RuntimeError, "Nested dependency execution"):
            runner._audit_session_concurrency(sessions, maximum_threads=9)

    def test_anonymous_child_fails_runtime_audit(self) -> None:
        """Every non-root session must resolve to a declared custom invocation."""
        batch = (self._run_spec("one", 1),)
        sessions = (
            runner._Session("supervisor", "root", "suite_supervisor", 1, 0.0, 5.0, frozenset()),
            runner._Session("anonymous", "supervisor", None, 2, 1.0, 2.0, frozenset()),
        )

        with self.assertRaisesRegex(RuntimeError, "Anonymous child"):
            runner._audit_session_concurrency(sessions, maximum_threads=9, batch=batch)

    def test_target_target_judge_judge_order_fails_scenario_binding(self) -> None:
        """Each target must be followed by its Judge before the next scenario target."""
        with tempfile.TemporaryDirectory() as temporary:
            codex_home = Path(temporary)
            sessions = codex_home / "sessions"
            sessions.mkdir()
            markers = {
                "suite_supervisor": "AGENT_INSTRUCTION_BINDING_suite_supervisor_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "target_agent": "AGENT_INSTRUCTION_BINDING_target_agent_bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
                "suite_judge": "AGENT_INSTRUCTION_BINDING_suite_judge_cccccccccccccccccccccccccccccccc",
            }
            self._write_rollout(
                sessions / "rollout-supervisor.jsonl",
                "suite_supervisor",
                1,
                markers["suite_supervisor"],
            )
            for name, invocation, second in (
                ("target-one", "target_agent", 3),
                ("target-two", "target_agent", 6),
                ("judge-one", "suite_judge", 9),
                ("judge-two", "suite_judge", 12),
            ):
                self._write_rollout(
                    sessions / f"rollout-{name}.jsonl",
                    invocation,
                    2,
                    markers[invocation],
                    parent="rollout-supervisor",
                    started_second=second,
                )
            suite = self._suite("one")
            run = runner._RunSpec(suite=suite, scenario_ids=("happy", "later"))
            report = {
                "runs": [
                    {
                        "suite": "one",
                        "scenarioResults": [
                            {"scenario": scenario, "targetInvoked": True, "judgeInvoked": True}
                            for scenario in run.scenario_ids
                        ],
                    }
                ]
            }
            staged = tuple(
                runner._StagedAgent(invocation, Path(f"{invocation}.toml"), "instructions", key * 64, marker)
                for invocation, key, marker in (
                    ("suite_supervisor", "a", markers["suite_supervisor"]),
                    ("target_agent", "b", markers["target_agent"]),
                    ("suite_judge", "c", markers["suite_judge"]),
                )
            )

            with self.assertRaisesRegex(RuntimeError, "Scenario child sequence"):
                runner._audit_identity(
                    staged,
                    codex_home,
                    {"suite_supervisor": 1, "target_agent": 2, "suite_judge": 2},
                    (run,),
                    report,
                )

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

    def test_timeout_stops_detached_descendant(self) -> None:
        """A child that starts a new session cannot escape runner cleanup."""
        program = (
            "import subprocess,sys,time; "
            "child=subprocess.Popen([sys.executable,'-c','import time; time.sleep(30)'],start_new_session=True); "
            "print(child.pid,flush=True)"
        )

        result = runner._run_process(
            (sys.executable, "-c", program),
            Path.cwd(),
            runner._controlled_environment(Path("/tmp/home"), Path("/tmp/codex"), Path("/tmp/work")),
            timeout_seconds=1.0,
        )

        detached_pid = int(result["stdout"].strip())
        with self.assertRaises(ProcessLookupError):
            os.kill(detached_pid, 0)
        self.assertNotEqual("clean", result["cleanup"])

    def test_containment_stops_fast_detached_descendant_with_sanitized_environment(self) -> None:
        """Containment also finds a reparented process that removed the cooperative token."""
        program = (
            "import subprocess,sys; "
            "child=subprocess.Popen([sys.executable,'-c','import time; time.sleep(30)'],"
            "start_new_session=True,env={}); print(child.pid,flush=True)"
        )
        with tempfile.TemporaryDirectory() as temporary:
            run_root = Path(temporary)
            workspace = run_root / "workspace"
            workspace.mkdir()
            result = runner._run_process(
                (sys.executable, "-c", program),
                workspace,
                runner._controlled_environment(run_root / "home", run_root / "codex", run_root / "tmp"),
                timeout_seconds=1.0,
                containment_root=run_root,
            )

        detached_pid = int(result["stdout"].strip())
        with self.assertRaises(ProcessLookupError):
            os.kill(detached_pid, 0)
        self.assertNotEqual("clean", result["cleanup"])

    def test_duplicate_scenario_results_fail_report_audit(self) -> None:
        """Set equality cannot hide multiple verdicts for one scenario."""
        batch = (self._run_spec("one", 1),)
        report = {
            "runs": [self._suite_report("one", "PASS")],
            "batchCleanup": "clean",
            "residualRisk": "none",
        }
        report["runs"][0]["scenarioResults"].append(dict(report["runs"][0]["scenarioResults"][0]))

        with self.assertRaisesRegex(RuntimeError, "Duplicate scenario"):
            runner._audit_report(batch, report)

    def test_checkpoint_retains_completed_scenario_without_final_report(self) -> None:
        """A terminal supervisor checkpoint survives a later coordinator interruption."""
        batch = (self._run_spec("one", 1),)
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            checkpoint = workspace / ".agent-suite-results" / "one" / "happy.json"
            checkpoint.parent.mkdir(parents=True)
            checkpoint.write_text(
                json.dumps(
                    {
                        "suite": "one",
                        "scenario": "happy",
                        "status": "PASS",
                        "targetInvoked": True,
                        "judgeInvoked": True,
                        "identityEvidence": ["bound"],
                        "evidence": ["receipt"],
                        "cleanup": "clean",
                        "residualRisk": "none",
                    }
                ),
                encoding="utf-8",
            )

            report = runner._load_checkpoint_report(workspace / ".agent-suite-results", batch)

        assert report is not None
        self.assertEqual("PASS", report["runs"][0]["scenarioResults"][0]["status"])

    def test_final_report_must_agree_with_external_checkpoint(self) -> None:
        """A coordinator cannot omit or rewrite the supervisor's durable scenario result."""
        batch = (self._run_spec("one", 1),)
        final_report = {
            "runs": [self._suite_report("one", "PASS")],
            "batchCleanup": "clean",
            "residualRisk": "none",
        }
        checkpoint_report = json.loads(json.dumps(final_report))
        checkpoint_report["runs"][0]["scenarioResults"][0]["status"] = "FAIL"

        with self.assertRaisesRegex(RuntimeError, "disagrees with checkpoint"):
            runner._audit_checkpoint_agreement(final_report, checkpoint_report, batch)

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
                    "targetInvoked": True,
                    "judgeInvoked": True,
                    "identityEvidence": ["thread-bound"],
                    "cleanup": "clean",
                    "evidence": ["synthetic"],
                }
            ],
            "maximumActiveChildrenObserved": 1,
            "cleanup": "clean",
        }

    @staticmethod
    def _write_rollout(
        path: Path,
        invocation: str,
        depth: int,
        marker: str | None = None,
        arbitrary_message: bool = False,
        parent: str | None = None,
        started_second: int = 0,
    ) -> None:
        session_id = path.stem
        parent = parent or ("root" if depth == 1 else "rollout-supervisor")
        timestamp = lambda offset: f"2026-07-17T00:00:{started_second + offset:02d}Z"
        events: tuple[dict[str, object], ...] = (
            {"timestamp": timestamp(0), "type": "session_meta", "payload": {
                "id": session_id,
                "parent_thread_id": parent,
                "agent_path": f"/root/{invocation}",
                "source": {"subagent": {"thread_spawn": {"depth": depth, "agent_path": f"/root/{invocation}"}}},
            }},
        )
        if marker and not arbitrary_message:
            command = f'python3 -c "print(\'{marker}\')"'
            events += (
                {"timestamp": timestamp(1), "type": "response_item", "payload": {
                    "type": "custom_tool_call",
                    "name": "exec",
                    "call_id": "binding-call",
                    "input": f"const r = await tools.exec_command({{cmd:{json.dumps(command)}}}); text(r.output);",
                }},
                {"timestamp": timestamp(2), "type": "response_item", "payload": {
                    "type": "custom_tool_call_output", "call_id": "binding-call", "output": marker
                }},
            )
        else:
            events += (
                {"timestamp": timestamp(1), "type": "event_msg", "payload": {
                    "type": "agent_message", "message": marker or "no binding evidence"
                }},
            )
        path.write_text("\n".join(json.dumps(event) for event in events) + "\n", encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
