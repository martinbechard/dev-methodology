# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Verifies bounded scheduling, validation, timing, evidence retention, and cleanup for the agent-suite runner.
# Governing design: evals/agent-tests/implementation-plan.md

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock
from pathlib import Path
from unittest import mock


_RUNNER_PATH = Path(__file__).with_name("runner.py")
_SPEC = importlib.util.spec_from_file_location("agent_suite_runner", _RUNNER_PATH)
assert _SPEC is not None and _SPEC.loader is not None
runner = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = runner
_SPEC.loader.exec_module(runner)


class AgentSuiteRunnerTests(unittest.TestCase):
    """Protect the runner contract without invoking a live model."""

    def test_harness_selection_is_explicit_and_supports_codex_and_junie(self) -> None:
        """Every execution names one supported harness before selection or scheduling."""
        with self.assertRaises(SystemExit):
            runner._argument_parser().parse_args(["--validate-only"])
        self.assertEqual(
            "codex",
            runner._argument_parser().parse_args(["--harness", "codex", "--validate-only"]).harness,
        )
        self.assertEqual(
            "junie",
            runner._argument_parser().parse_args(["--harness", "junie", "--validate-only"]).harness,
        )

    def test_reporting_subcommand_uses_the_repository_owned_runner_entry_point(self) -> None:
        """Operators reach reporting through runner.py without invoking an internal module directly."""
        with mock.patch.object(runner, "_reporting_main", return_value=0) as reporting_main:
            status = runner.main(("reporting", "rebuild", "--harness", "codex"))

        self.assertEqual(0, status)
        reporting_main.assert_called_once_with(("rebuild", "--harness", "codex"))

    def test_real_junie_supervisor_binds_native_authority_and_runtime_names(self) -> None:
        """A real suite supervisor contains only Junie authority and hyphen runtime invocations."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            destination = root / "agents"
            destination.mkdir()
            source = _RUNNER_PATH.parent / "dev-coder" / "agents" / "supervisor.toml"
            bindings = {
                "dev_coder_suite_supervisor": "dev-coder-suite-supervisor",
                "dev_coder": "dev-coder",
                "dev_coder_suite_judge": "dev-coder-suite-judge",
            }

            staged = runner._copy_junie_agent(
                source,
                "dev_coder_suite_supervisor",
                destination,
                bindings,
            )
            rendered = (destination / "dev-coder-suite-supervisor.md").read_text(encoding="utf-8")

        self.assertEqual("dev-coder-suite-supervisor", staged.invocation)
        self.assertIn("name: dev-coder-suite-supervisor", rendered)
        self.assertIn("generated/adapters/junie/agents/dev-coder.md", rendered)
        self.assertNotIn("generated/adapters/codex", rendered)
        self.assertNotIn("dev_coder", rendered)
        self.assertIn("Junie custom agent", rendered)
        self.assertIn(staged.instruction_marker, rendered)

    def test_junie_terminal_event_yields_governed_report(self) -> None:
        """Only one terminal Junie result event can carry the coordinator report."""
        report = {"runs": [], "batchCleanup": "clean", "residualRisk": "none"}
        with tempfile.TemporaryDirectory() as directory:
            events = Path(directory) / "events.jsonl"
            events.write_text(
                json.dumps({"type": "session", "sessionId": "synthetic"})
                + "\n"
                + json.dumps({"type": "result", "result": json.dumps(report)})
                + "\n",
                encoding="utf-8",
            )

            self.assertEqual(report, runner._extract_junie_report(events))

    def test_junie_name_lifecycle_is_retained_but_cannot_prove_definition_or_topology(self) -> None:
        """The actual Junie schema proves names and statuses without inventing stronger attribution."""
        run = runner._RunSpec(suite=self._suite("one", nested_limit=1), scenario_ids=("happy",))
        report = {"runs": [self._suite_report("one", "PASS")]}
        staged = self._staged_junie_agents()
        with tempfile.TemporaryDirectory() as directory:
            junie_home = Path(directory)
            self._write_junie_lifecycles(
                junie_home,
                (
                    ("suite-supervisor", 0, 5),
                    ("target-agent", 1, 2),
                    ("suite-judge", 3, 4),
                ),
            )

            with self.assertRaisesRegex(
                runner._JunieEvidenceInsufficient,
                "cannot bind.*staged definition or parent topology",
            ) as raised:
                runner._audit_junie_agent_lifecycles(junie_home, (run,), report, staged)

        self.assertFalse(raised.exception.diagnostics["definitionDigestBound"])
        self.assertEqual("name-verified", raised.exception.diagnostics["status"])
        self.assertEqual(3, len(raised.exception.diagnostics["lifecycles"]))
        self.assertFalse(raised.exception.diagnostics["parentChildVerified"])

    def test_junie_ledger_rejects_unexpected_agent_and_wrong_outer_identity(self) -> None:
        """Exact runtime names reject agents and event identities outside the controlled lookup set."""
        run = runner._RunSpec(suite=self._suite("one", nested_limit=1), scenario_ids=("happy",))
        report = {"runs": [self._suite_report("one", "PASS")]}
        staged = self._staged_junie_agents()
        with tempfile.TemporaryDirectory() as directory:
            junie_home = Path(directory)
            self._write_junie_lifecycles(
                junie_home,
                (
                    ("suite-supervisor", 0, 6),
                    ("target-agent", 1, 4),
                    ("suite-judge", 3, 5),
                    ("rogue-agent", 1, 2),
                ),
            )
            with self.assertRaisesRegex(RuntimeError, "unexpected custom agent"):
                runner._audit_junie_agent_lifecycles(junie_home, (run,), report, staged)

            self._write_junie_lifecycles(
                junie_home,
                (
                    ("suite-supervisor", 0, 6),
                    ("target-agent", 1, 4),
                    ("suite-judge", 3, 5),
                ),
            )
            event_path = junie_home / "sessions" / "session" / "events.jsonl"
            events = [json.loads(line) for line in event_path.read_text(encoding="utf-8").splitlines()]
            events[0]["event"]["agentEvent"]["name"] = "different-supervisor"
            event_path.write_text(
                "\n".join(json.dumps(event) for event in events) + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(RuntimeError, "identity mismatch"):
                runner._audit_junie_agent_lifecycles(junie_home, (run,), report, staged)

    def test_name_only_junie_lifecycle_evidence_blocks_definition_attribution(self) -> None:
        """Lifecycle names without runtime marker/digest receipts cannot support a governed verdict."""
        run = runner._RunSpec(suite=self._suite("one", nested_limit=1), scenario_ids=("happy",))
        report = {"runs": [self._suite_report("one", "PASS")], "residualRisk": "none"}
        staged = self._staged_junie_agents()
        with tempfile.TemporaryDirectory() as directory:
            junie_home = Path(directory)
            self._write_junie_lifecycles(
                junie_home,
                (
                    ("suite-supervisor", 0, 5),
                    ("target-agent", 1, 2),
                    ("suite-judge", 3, 4),
                ),
            )
            with self.assertRaisesRegex(
                runner._JunieEvidenceInsufficient, "cannot bind.*staged definition"
            ) as raised:
                runner._audit_junie_agent_lifecycles(junie_home, (run,), report, staged)
            retained = runner._junie_lifecycle_evidence(junie_home)

        self.assertEqual(6, len(retained))
        blocked = runner._blocked_junie_report(report, str(raised.exception))
        self.assertEqual("BLOCKED", blocked["runs"][0]["scenarioResults"][0]["status"])

    def test_insufficient_junie_topology_evidence_blocks_governed_result(self) -> None:
        """Missing relationship evidence becomes BLOCKED rather than an attributed PASS."""
        run = runner._RunSpec(suite=self._suite("one", nested_limit=1), scenario_ids=("happy",))
        report = {"runs": [self._suite_report("one", "PASS")], "residualRisk": "none"}
        staged = self._staged_junie_agents()
        with tempfile.TemporaryDirectory() as directory:
            junie_home = Path(directory)
            session = junie_home / "sessions" / "session"
            session.mkdir(parents=True)
            (session / "events.jsonl").write_text(
                json.dumps(
                    {
                        "event": {
                            "agentEvent": {
                                "kind": "CustomAgentBlockUpdatedEvent",
                                "agent": {"id": "custom-suite-supervisor", "name": "suite-supervisor"},
                                "name": "suite-supervisor",
                                "status": "STARTED",
                                "stepId": "supervisor-step",
                                "menuItems": [],
                                "details": None,
                                "model": "opus",
                            }
                        }
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            with self.assertRaises(runner._JunieEvidenceInsufficient) as raised:
                runner._audit_junie_agent_lifecycles(junie_home, (run,), report, staged)

        blocked = runner._blocked_junie_report(report, str(raised.exception))
        self.assertEqual("BLOCKED", blocked["runs"][0]["scenarioResults"][0]["status"])
        self.assertIn("incomplete lifecycle", blocked["residualRisk"])

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

    def test_local_runtime_suite_is_isolated_from_ordinary_batches(self) -> None:
        """Network and browser facilities cannot leak to unrelated supervisors."""
        first = self._run_spec("one", 1)
        privileged_suite = self._suite("local-runtime")
        privileged_suite = runner._Suite(
            suite_id=privileged_suite.suite_id,
            priority=2,
            path=privileged_suite.path,
            manifest=privileged_suite.manifest,
            scenarios=(
                {
                    "id": "happy",
                    "status": "executable",
                    "executableCase": "fixture",
                    "runtimeCapabilities": ["loopback"],
                },
            ),
        )
        privileged = runner._RunSpec(suite=privileged_suite, scenario_ids=("happy",))
        third = self._run_spec("three", 3)

        batches = runner._batch_runs((first, privileged, third), maximum=4)

        self.assertEqual([["one"], ["local-runtime"], ["three"]], [
            [run.suite.suite_id for run in batch] for batch in batches
        ])

    def test_nested_enabled_suites_are_queued_in_separate_batches(self) -> None:
        """Two supervisors that may delegate cannot contend for the one nested-agent slot."""
        first = self._run_spec("one", 1)
        nested_one = runner._RunSpec(suite=self._suite("nested-one", nested_limit=1), scenario_ids=("happy",))
        third = self._run_spec("three", 3)
        nested_two = runner._RunSpec(suite=self._suite("nested-two", nested_limit=1), scenario_ids=("happy",))

        batches = runner._batch_runs((first, nested_one, third, nested_two), maximum=4)

        self.assertEqual([["one", "nested-one", "three"], ["nested-two"]], [
            [run.suite.suite_id for run in batch] for batch in batches
        ])

    def test_coordinator_requires_registered_agent_types_and_fresh_contexts(self) -> None:
        """A task label cannot substitute for a registered role with a fresh fork."""
        prompt = runner._coordinator_prompt(
            (self._run_spec("one", 1),),
            Path("/tmp/checkpoints"),
            Path("/workspace/.agent-suite-fixtures"),
            "codex-batch-01-test",
        )

        self.assertIn("agent_type exactly equal", prompt)
        self.assertIn("fork_context exactly false", prompt)
        self.assertIn('"fixtureRoot": "/workspace/.agent-suite-fixtures/one"', prompt)
        self.assertIn("never under /tmp or /private/tmp", prompt)

    def test_governed_result_contract_separates_identity_deterministic_and_judge_evidence(self) -> None:
        """Coordinator output cannot substitute identity strings for Judge or deterministic evidence."""
        scenario_schema = runner._coordinator_schema()["properties"]["runs"]["items"][
            "properties"
        ]["scenarioResults"]["items"]

        self.assertTrue(
            {
                "identityEvidence",
                "deterministicEvidence",
                "modelJudgeEvidence",
                "evidenceReceipts",
                "evidence",
            }
            <= set(scenario_schema["required"])
        )
        handoff_schema = scenario_schema["properties"]["handoffReceipts"]["items"]
        self.assertEqual(
            [
                "lane",
                "role",
                "commit",
                "review",
                "verification",
                "claimRelease",
            ],
            handoff_schema["required"],
        )

    def test_cleanup_audit_rejects_active_claim_in_nested_fixture_repository(self) -> None:
        """A candidate repository cannot retain a claim outside the workspace registry."""
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            registry = (
                workspace
                / ".agent-suite-fixtures"
                / "dev-coder"
                / "candidate"
                / ".git"
                / "agent-claims.json"
            )
            registry.parent.mkdir(parents=True)
            registry.write_text(
                json.dumps({"claims": [{"claim_id": "retained"}]}) + "\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(
                RuntimeError,
                "Fixture repository retains active claims",
            ):
                runner._audit_workspace_cleanup(workspace)

    def test_cleanup_audit_rejects_fixture_git_common_directory_escape(self) -> None:
        """A linked fixture worktree cannot hide its claim registry outside runner containment."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workspace = root / "workspace"
            fixture = workspace / ".agent-suite-fixtures" / "dev-orchestrator"
            source = root / "external-source"
            candidate = fixture / "candidate"
            workspace.mkdir()
            source.mkdir()
            subprocess.run(["git", "init", "--quiet"], cwd=source, check=True)
            subprocess.run(["git", "config", "user.name", "Fixture"], cwd=source, check=True)
            subprocess.run(
                ["git", "config", "user.email", "fixture@example.invalid"],
                cwd=source,
                check=True,
            )
            (source / "evidence.txt").write_text("synthetic\n", encoding="utf-8")
            subprocess.run(["git", "add", "evidence.txt"], cwd=source, check=True)
            subprocess.run(["git", "commit", "--quiet", "-m", "fixture"], cwd=source, check=True)
            fixture.mkdir(parents=True)
            subprocess.run(
                ["git", "worktree", "add", "--quiet", "--detach", str(candidate)],
                cwd=source,
                check=True,
            )

            with self.assertRaisesRegex(RuntimeError, "Git common directory escapes cleanup containment"):
                runner._audit_workspace_cleanup(workspace)

    def test_cleanup_audit_reads_active_claim_from_contained_common_directory(self) -> None:
        """A .git indirection cannot hide active claims in a contained common directory."""
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "workspace"
            fixture = workspace / ".agent-suite-fixtures" / "dev-orchestrator"
            candidate = fixture / "candidate"
            common = fixture / "candidate.git"
            candidate.mkdir(parents=True)
            subprocess.run(
                ["git", "init", "--quiet", "--separate-git-dir", str(common), str(candidate)],
                check=True,
            )
            (common / "agent-claims.json").write_text(
                json.dumps({"claims": [{"claim_id": "retained"}]}) + "\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(RuntimeError, "Fixture repository retains active claims"):
                runner._audit_workspace_cleanup(workspace)

    def test_release_journal_cannot_escape_fixture_containment(self) -> None:
        """An external linked-worktree journal cannot substantiate a fixture release receipt."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture = root / "fixtures" / "dev-orchestrator"
            source = root / "external-source"
            candidate = fixture / "candidate"
            source.mkdir(parents=True)
            subprocess.run(["git", "init", "--quiet"], cwd=source, check=True)
            subprocess.run(["git", "config", "user.name", "Fixture"], cwd=source, check=True)
            subprocess.run(
                ["git", "config", "user.email", "fixture@example.invalid"],
                cwd=source,
                check=True,
            )
            (source / "evidence.txt").write_text("synthetic\n", encoding="utf-8")
            subprocess.run(["git", "add", "evidence.txt"], cwd=source, check=True)
            subprocess.run(["git", "commit", "--quiet", "-m", "fixture"], cwd=source, check=True)
            fixture.mkdir(parents=True)
            subprocess.run(
                ["git", "worktree", "add", "--quiet", "--detach", str(candidate)],
                cwd=source,
                check=True,
            )
            journal = source / ".git" / "agent-claim-events" / "hot" / "2026-07-19.jsonl"
            journal.parent.mkdir(parents=True)
            journal.write_text(
                json.dumps(
                    {
                        "action": "release",
                        "outcome": "RELEASED",
                        "event_id": "external-release",
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(RuntimeError, "Git common directory escapes fixture containment"):
                runner._release_events(candidate, fixture)

    def test_release_journal_paths_cannot_symlink_outside_contained_common_directory(self) -> None:
        """Contained Git metadata cannot redirect its hot directory or journals outside the fixture."""
        for escape in ("hot-directory", "journal"):
            with self.subTest(escape=escape), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                fixture = root / "fixtures" / "dev-orchestrator"
                candidate = fixture / "candidate"
                outside = root / "outside"
                candidate.mkdir(parents=True)
                outside.mkdir()
                subprocess.run(["git", "init", "--quiet"], cwd=candidate, check=True)
                event_root = candidate / ".git" / "agent-claim-events"
                hot = event_root / "hot"
                if escape == "hot-directory":
                    external_hot = outside / "hot"
                    external_hot.mkdir()
                    (external_hot / "2026-07-19.jsonl").write_text("{}\n", encoding="utf-8")
                    event_root.mkdir()
                    hot.symlink_to(external_hot, target_is_directory=True)
                else:
                    hot.mkdir(parents=True)
                    external_journal = outside / "2026-07-19.jsonl"
                    external_journal.write_text("{}\n", encoding="utf-8")
                    (hot / "2026-07-19.jsonl").symlink_to(external_journal)

                with self.assertRaisesRegex(RuntimeError, "Claim release journal escapes fixture containment"):
                    runner._release_events(candidate, fixture)

    def test_project_bootstrapper_judge_defers_runner_owned_audits(self) -> None:
        """Bootstrapper semantic judgment cannot fail only on evidence owned by the outer runner."""
        contract = (
            _RUNNER_PATH.parent
            / "project-bootstrapper"
            / "skills"
            / "project-bootstrapper-suite-contract"
            / "SKILL.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Do not return BLOCKED solely because runner-owned", contract)

    def test_runtime_uses_role_aware_v1_and_bounds_concurrency(self) -> None:
        """The live runtime must expose role selection and use the declared batch ceiling."""
        arguments = runner._multi_agent_runtime_arguments(10)

        self.assertEqual(
            (
                "--model",
                "gpt-5.5",
                "--enable",
                "multi_agent",
                "--disable",
                "multi_agent_v2",
                "-c",
                "agents.max_threads=10",
            ),
            arguments,
        )

    def test_runtime_uses_current_app_bundled_codex(self) -> None:
        """The runner cannot resolve an older PATH CLI that rejects staged agent models."""
        executable = runner._bundled_codex_executable()

        self.assertEqual(Path("/Applications/ChatGPT.app/Contents/Resources/codex"), executable)
        self.assertTrue(executable.is_file())

    def test_runtime_capabilities_are_collected_only_from_selected_scenarios(self) -> None:
        """A batch receives only the local facilities declared by its selected cases."""
        suite = self._suite("capability-suite")
        suite = runner._Suite(
            suite_id=suite.suite_id,
            priority=suite.priority,
            path=suite.path,
            manifest=suite.manifest,
            scenarios=(
                {
                    "id": "selected",
                    "status": "executable",
                    "executableCase": "fixture",
                    "runtimeCapabilities": ["loopback", "browser-automation"],
                },
                {
                    "id": "excluded",
                    "status": "executable",
                    "executableCase": "fixture",
                    "runtimeCapabilities": ["offline-node-modules"],
                },
                {"id": "third", "status": "executable", "executableCase": "fixture"},
            ),
        )
        batch = (runner._RunSpec(suite=suite, scenario_ids=("selected",)),)

        self.assertEqual(
            frozenset({"loopback", "browser-automation"}),
            runner._runtime_capabilities(batch),
        )

    def test_unknown_runtime_capability_is_rejected(self) -> None:
        """Suite authors cannot silently grant an unreviewed runtime facility."""
        suite = self._suite("invalid-capability")
        suite = runner._Suite(
            suite_id=suite.suite_id,
            priority=suite.priority,
            path=suite.path,
            manifest=suite.manifest,
            scenarios=(
                {
                    "id": "happy",
                    "status": "executable",
                    "executableCase": "fixture",
                    "runtimeCapabilities": ["unbounded-network"],
                },
                {"id": "second", "status": "executable", "executableCase": "fixture"},
                {"id": "third", "status": "executable", "executableCase": "fixture"},
            ),
        )

        with self.assertRaisesRegex(ValueError, "runtime capability"):
            runner._validate_suite(suite, require_executable=False)

    def test_offline_node_dependencies_are_staged_for_selected_fixture(self) -> None:
        """A clean clone receives the fixture's pinned ignored dependency tree without network use."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            repository = root / "repository"
            workspace = root / "workspace"
            source = repository / "evals" / "projects" / "fixture" / "node_modules"
            source.mkdir(parents=True)
            (source / "version.txt").write_text("pinned", encoding="utf-8")
            typescript = source / "typescript"
            typescript.mkdir()
            (typescript / "package.json").write_text('{"version":"7.0.2"}', encoding="utf-8")
            (source.parent / "package-lock.json").write_text(
                '{"packages":{"node_modules/typescript":{"version":"7.0.2"}}}', encoding="utf-8"
            )
            workspace.mkdir()
            suite = self._suite("offline-suite")
            suite = runner._Suite(
                suite_id=suite.suite_id,
                priority=suite.priority,
                path=suite.path,
                manifest=suite.manifest,
                scenarios=(
                    {
                        "id": "happy",
                        "status": "executable",
                        "executableCase": "fixture",
                        "runtimeCapabilities": ["offline-node-modules"],
                    },
                ),
            )
            batch = (runner._RunSpec(suite=suite, scenario_ids=("happy",)),)

            staged = runner._stage_offline_project_dependencies(batch, repository, workspace)

            self.assertEqual(("evals/projects/fixture/node_modules",), staged)
            self.assertEqual(
                "pinned",
                (workspace / "evals" / "projects" / "fixture" / "node_modules" / "version.txt").read_text(
                    encoding="utf-8"
                ),
            )

    def test_wiki_ingester_builder_stages_every_scenario_source(self) -> None:
        """Wiki Ingester cases cannot depend on files created by another concurrent suite."""
        builder = _RUNNER_PATH.parent / "wiki-ingester" / "fixtures" / "stage_fixture.py"
        expected = {
            "raw-ingest": ("raw/retry-policy.md",),
            "destination-collision": ("raw/provider.md", "raw/processed/provider.md"),
            "verifier-failure": ("raw/provider-routing.md",),
        }
        with tempfile.TemporaryDirectory() as temporary:
            for scenario, paths in expected.items():
                with self.subTest(scenario=scenario):
                    destination = Path(temporary) / scenario
                    completed = subprocess.run(
                        (sys.executable, str(builder), "--scenario", scenario, "--destination", str(destination)),
                        check=False,
                        capture_output=True,
                        text=True,
                    )
                    self.assertEqual(0, completed.returncode, completed.stderr)
                    self.assertFalse((destination / "raw" / "2026-07-15-order-cancellation.md").exists())
                    self.assertTrue(
                        (destination / "raw" / "processed" / "2026-07-15-order-cancellation.md").is_file()
                    )
                    for path in paths:
                        self.assertTrue((destination / path).is_file(), path)
                    order_lifecycle = (
                        destination / "docs" / "wiki" / "orders" / "order-lifecycle.md"
                    ).read_text(encoding="utf-8")
                    self.assertIn("raw/processed/2026-07-15-order-cancellation.md", order_lifecycle)

            raw_task = (
                _RUNNER_PATH.parent
                / "wiki-ingester"
                / "fixtures"
                / "scenario-files"
                / "raw-ingest"
                / "TASK.md"
            ).read_text(encoding="utf-8")
            self.assertIn("planned claim closeout in eval-result.md", raw_task)
            self.assertIn("actual release receipt plus final queue state", raw_task)
            self.assertIn("Do not mutate the repository after releasing the claim", raw_task)
            for scenario in ("destination-collision", "verifier-failure"):
                with self.subTest(closeout_contract=scenario):
                    task = (
                        _RUNNER_PATH.parent
                        / "wiki-ingester"
                        / "fixtures"
                        / "scenario-files"
                        / scenario
                        / "TASK.md"
                    ).read_text(encoding="utf-8")
                    self.assertIn("planned claim closeout in eval-result.md", task)
                    self.assertIn("actual release receipt", task)
                    self.assertIn("Do not mutate the repository after releasing the claim", task)

    def test_offline_maven_dependencies_are_checksum_staged_into_isolated_home(self) -> None:
        """A Maven fixture receives only its declared immutable host-cache files."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            repository = root / "repository"
            workspace = root / "workspace"
            home = root / "home"
            maven_repository = root / "host-maven-repository"
            project = repository / "evals" / "projects" / "fixture"
            project.mkdir(parents=True)
            workspace.mkdir()
            artifact = maven_repository / "example" / "fixture" / "1.0" / "fixture-1.0.jar"
            artifact.parent.mkdir(parents=True)
            artifact.write_bytes(b"pinned-maven-artifact")
            manifest = project / "offline-maven-repository.json"
            manifest.write_text(
                json.dumps(
                    {
                        "schema": "dev-methodology-offline-maven-repository",
                        "version": 1,
                        "files": [
                            {
                                "path": "example/fixture/1.0/fixture-1.0.jar",
                                "sha256": runner._sha256(artifact),
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            workspace_manifest = workspace / "evals" / "projects" / "fixture" / manifest.name
            workspace_manifest.parent.mkdir(parents=True)
            workspace_manifest.write_bytes(manifest.read_bytes())
            suite = self._suite("offline-maven-suite")
            suite = runner._Suite(
                suite_id=suite.suite_id,
                priority=suite.priority,
                path=suite.path,
                manifest=suite.manifest,
                scenarios=(
                    {
                        "id": "happy",
                        "status": "executable",
                        "executableCase": "fixture",
                        "runtimeCapabilities": ["offline-maven-repository"],
                    },
                ),
            )
            batch = (runner._RunSpec(suite=suite, scenario_ids=("happy",)),)

            staged = runner._stage_offline_maven_dependencies(
                batch,
                repository,
                workspace,
                home,
                maven_repository,
            )

            destination = home / ".m2" / "repository" / "example" / "fixture" / "1.0" / "fixture-1.0.jar"
            self.assertEqual(("evals/projects/fixture/offline-maven-repository.json",), staged)
            self.assertEqual(b"pinned-maven-artifact", destination.read_bytes())
            self.assertTrue((home / ".m2" / "repository" / ".agent-suite-offline").is_file())

    def test_offline_maven_staging_rejects_host_cache_drift(self) -> None:
        """A changed cache file cannot silently enter a governed fixture."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            repository = root / "repository"
            workspace = root / "workspace"
            home = root / "home"
            maven_repository = root / "host-maven-repository"
            project = repository / "evals" / "projects" / "fixture"
            project.mkdir(parents=True)
            workspace.mkdir()
            artifact = maven_repository / "example" / "fixture" / "1.0" / "fixture-1.0.jar"
            artifact.parent.mkdir(parents=True)
            artifact.write_bytes(b"drifted")
            manifest = project / "offline-maven-repository.json"
            manifest.write_text(
                json.dumps(
                    {
                        "schema": "dev-methodology-offline-maven-repository",
                        "version": 1,
                        "files": [
                            {
                                "path": "example/fixture/1.0/fixture-1.0.jar",
                                "sha256": "0" * 64,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            workspace_manifest = workspace / "evals" / "projects" / "fixture" / manifest.name
            workspace_manifest.parent.mkdir(parents=True)
            workspace_manifest.write_bytes(manifest.read_bytes())
            suite = self._suite("offline-maven-suite")
            suite = runner._Suite(
                suite_id=suite.suite_id,
                priority=suite.priority,
                path=suite.path,
                manifest=suite.manifest,
                scenarios=(
                    {
                        "id": "happy",
                        "status": "executable",
                        "executableCase": "fixture",
                        "runtimeCapabilities": ["offline-maven-repository"],
                    },
                ),
            )

            with self.assertRaisesRegex(RuntimeError, "checksum drift"):
                runner._stage_offline_maven_dependencies(
                    (runner._RunSpec(suite=suite, scenario_ids=("happy",)),),
                    repository,
                    workspace,
                    home,
                    maven_repository,
                )

    def test_capability_arguments_use_local_only_profile_and_in_app_browser(self) -> None:
        """Local capabilities use the managed proxy and never select an external browser."""
        with tempfile.TemporaryDirectory() as temporary:
            codex_home = Path(temporary)
            arguments = runner._capability_runtime_arguments(
                frozenset({"loopback", "browser-automation"}), codex_home
            )
            profile = (codex_home / "agent-suite-local-runtime.config.toml").read_text(encoding="utf-8")

        self.assertIn("network_proxy", arguments)
        self.assertIn("in_app_browser", arguments)
        self.assertIn("browser_use", arguments)
        self.assertNotIn("browser_use_external", arguments)
        self.assertNotIn("sandbox_workspace_write.network_access=true", arguments)
        self.assertIn('mode = "limited"', profile)
        self.assertIn('"localhost" = "allow"', profile)
        self.assertNotIn("example.com", profile)

    def test_offline_typescript_launcher_uses_bundled_node(self) -> None:
        """The staged compiler cannot fall back to an older Node from a target login shell."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            repository = root / "repository"
            workspace = root / "workspace"
            modules = repository / "evals" / "projects" / "fixture" / "node_modules"
            typescript = modules / "typescript"
            (typescript / "bin").mkdir(parents=True)
            (typescript / "bin" / "tsc").write_text("fixture", encoding="utf-8")
            (typescript / "package.json").write_text('{"version":"7.0.2"}', encoding="utf-8")
            (modules / ".bin").mkdir()
            (modules / ".bin" / "tsc").symlink_to("../typescript/bin/tsc")
            (modules.parent / "package-lock.json").write_text(
                '{"packages":{"node_modules/typescript":{"version":"7.0.2"}}}', encoding="utf-8"
            )
            bundled_node = root / "runtime" / "bin" / "node"
            bundled_node.parent.mkdir(parents=True)
            bundled_node.write_text("fixture", encoding="utf-8")
            workspace.mkdir()
            suite = self._suite("offline-suite")
            suite = runner._Suite(
                suite_id=suite.suite_id,
                priority=suite.priority,
                path=suite.path,
                manifest=suite.manifest,
                scenarios=(
                    {
                        "id": "happy",
                        "status": "executable",
                        "executableCase": "fixture",
                        "runtimeCapabilities": ["offline-node-modules"],
                    },
                ),
            )

            runner._stage_offline_project_dependencies(
                (runner._RunSpec(suite=suite, scenario_ids=("happy",)),),
                repository,
                workspace,
                bundled_node,
            )

            launcher = workspace / "evals" / "projects" / "fixture" / "node_modules" / ".bin" / "tsc"
            self.assertFalse(launcher.is_symlink())
            self.assertIn(str(bundled_node), launcher.read_text(encoding="utf-8"))
            self.assertTrue(launcher.stat().st_mode & 0o100)

    def test_offline_fixture_rejects_parent_path_traversal(self) -> None:
        """Executable-case metadata cannot copy host content outside the project root."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            repository = root / "repository"
            workspace = root / "workspace"
            repository.mkdir()
            workspace.mkdir()
            suite = self._suite("offline-suite")
            suite = runner._Suite(
                suite_id=suite.suite_id,
                priority=suite.priority,
                path=suite.path,
                manifest=suite.manifest,
                scenarios=({
                    "id": "happy",
                    "status": "executable",
                    "executableCase": "../escape",
                    "runtimeCapabilities": ["offline-node-modules"],
                },),
            )
            batch = (runner._RunSpec(suite=suite, scenario_ids=("happy",)),)

            with self.assertRaisesRegex(RuntimeError, "one project directory name"):
                runner._stage_offline_project_dependencies(batch, repository, workspace)

    def test_offline_fixture_rejects_lockfile_version_drift(self) -> None:
        """Mutable ignored dependencies must match the tracked lock evidence."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            repository = root / "repository"
            workspace = root / "workspace"
            source = repository / "evals" / "projects" / "fixture" / "node_modules" / "typescript"
            source.mkdir(parents=True)
            (source / "package.json").write_text('{"version":"7.0.1"}', encoding="utf-8")
            (source.parent.parent / "package-lock.json").write_text(
                '{"packages":{"node_modules/typescript":{"version":"7.0.2"}}}', encoding="utf-8"
            )
            workspace.mkdir()
            suite = self._suite("offline-suite")
            suite = runner._Suite(
                suite_id=suite.suite_id,
                priority=suite.priority,
                path=suite.path,
                manifest=suite.manifest,
                scenarios=({
                    "id": "happy",
                    "status": "executable",
                    "executableCase": "fixture",
                    "runtimeCapabilities": ["offline-node-modules"],
                },),
            )
            batch = (runner._RunSpec(suite=suite, scenario_ids=("happy",)),)

            with self.assertRaisesRegex(RuntimeError, "does not match its lockfile"):
                runner._stage_offline_project_dependencies(batch, repository, workspace)

    def test_offline_fixture_rejects_escaping_dependency_symlink(self) -> None:
        """Only package-internal relative links survive offline dependency staging."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            repository = root / "repository"
            workspace = root / "workspace"
            modules = repository / "evals" / "projects" / "fixture" / "node_modules"
            typescript = modules / "typescript"
            typescript.mkdir(parents=True)
            (typescript / "package.json").write_text('{"version":"7.0.2"}', encoding="utf-8")
            (modules.parent / "package-lock.json").write_text(
                '{"packages":{"node_modules/typescript":{"version":"7.0.2"}}}', encoding="utf-8"
            )
            outside = root / "outside.txt"
            outside.write_text("host", encoding="utf-8")
            (modules / "escape").symlink_to(outside)
            workspace.mkdir()
            suite = self._suite("offline-suite")
            suite = runner._Suite(
                suite_id=suite.suite_id,
                priority=suite.priority,
                path=suite.path,
                manifest=suite.manifest,
                scenarios=({
                    "id": "happy",
                    "status": "executable",
                    "executableCase": "fixture",
                    "runtimeCapabilities": ["offline-node-modules"],
                },),
            )
            batch = (runner._RunSpec(suite=suite, scenario_ids=("happy",)),)

            with self.assertRaisesRegex(RuntimeError, "escaping symlink"):
                runner._stage_offline_project_dependencies(batch, repository, workspace)

    def test_browser_runtime_is_copied_and_bound_to_isolated_home(self) -> None:
        """Browser instructions and Node REPL trust stay inside the isolated home."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            plugin = root / "plugin"
            (plugin / "scripts").mkdir(parents=True)
            (plugin / "scripts" / "browser-client.mjs").write_text("export {};", encoding="utf-8")
            source_skill = plugin / "skills" / "control-in-app-browser"
            source_skill.mkdir(parents=True)
            (source_skill / "SKILL.md").write_text(
                "Use <plugin root>/scripts/browser-client.mjs", encoding="utf-8"
            )
            codex_home = root / "codex-home"
            skill_root = codex_home / "skills"
            skill_root.mkdir(parents=True)
            app_resources = root / "ChatGPT.app" / "Contents" / "Resources"
            (app_resources / "cua_node" / "bin").mkdir(parents=True)
            for relative in ("cua_node/bin/node_repl", "cua_node/bin/node", "codex"):
                executable = app_resources / relative
                executable.write_text("fixture", encoding="utf-8")
            computer_use_service = root / "plugin-cache" / "Codex Computer Use.app"
            computer_use_service.mkdir(parents=True)
            (computer_use_service / "fixture").write_text("service", encoding="utf-8")

            runtime = runner._stage_browser_runtime(
                plugin,
                codex_home,
                skill_root,
                app_resources,
                computer_use_service,
            )
            staged_skill = skill_root / "control-in-app-browser" / "SKILL.md"
            config = (codex_home / "config.toml").read_text(encoding="utf-8")

            self.assertEqual(codex_home / "browser-runtime", runtime)
            self.assertIn(str(runtime), staged_skill.read_text(encoding="utf-8"))
            self.assertNotIn("<plugin root>", staged_skill.read_text(encoding="utf-8"))
            self.assertIn('[mcp_servers.node_repl]', config)
            self.assertIn('BROWSER_USE_AVAILABLE_BACKENDS = "iab"', config)
            self.assertIn(f'CODEX_HOME = "{codex_home}"', config)
            self.assertIn(f'NODE_REPL_TRUSTED_CODE_PATHS = "{codex_home}"', config)
            self.assertIn(runner._sha256(runtime / "scripts" / "browser-client.mjs"), config)
            self.assertIn(f'SKY_CUA_SERVICE_PATH = "{codex_home / "computer-use-service.app"}"', config)
            self.assertTrue((codex_home / "computer-use-service.app" / "fixture").is_file())
            self.assertNotIn("extension", config)
            self.assertNotIn(str(Path.home()), config)

    def test_browser_activity_audit_requires_iab_interaction_and_cleanup(self) -> None:
        """A browser verdict needs an observed in-app tab interaction and close."""
        with tempfile.TemporaryDirectory() as temporary:
            codex_home = Path(temporary)
            session_id = "target-session"
            rollout = codex_home / f"rollout-{session_id}.jsonl"
            events = [
                {"timestamp": "2026-07-17T00:00:00Z", "type": "session_meta", "payload": {"id": session_id}},
                {
                    "timestamp": "2026-07-17T00:00:01Z",
                    "type": "response_item",
                    "payload": {
                        "type": "custom_tool_call",
                        "name": "exec",
                        "input": (
                            "await tools.mcp__node_repl__js({code: `"
                            "globalThis.iab = await agent.browsers.get('iab'); "
                            "globalThis.tab = await iab.tabs.new(); "
                            "await tab.goto('http://127.0.0.1:43117/'); "
                            "await tab.playwright.domSnapshot(); await tab.close();`});"
                        ),
                    },
                },
            ]
            rollout.write_text("\n".join(json.dumps(event) for event in events) + "\n", encoding="utf-8")
            batch = (self._browser_run_spec("browser-suite"),)
            identity = {
                "scenarioBindings": [
                    {
                        "suite": "browser-suite",
                        "scenario": "happy",
                        "kind": "target",
                        "sessionId": session_id,
                    }
                ]
            }

            audit = runner._audit_browser_activity(
                codex_home,
                batch,
                identity,
                {"runs": [self._suite_report("browser-suite", "PASS")]},
            )

            self.assertEqual(1, audit["targetSessions"])
            self.assertEqual(1, audit["nodeReplCalls"])
            self.assertEqual(0, audit["blockedTargetSessions"])

    def test_browser_activity_audit_preserves_verified_unavailable_backend_block(self) -> None:
        """A detached CLI can report BLOCKED from the retained unavailable-backend result."""
        with tempfile.TemporaryDirectory() as temporary:
            codex_home = Path(temporary)
            session_id = "target-session"
            rollout = codex_home / f"rollout-{session_id}.jsonl"
            events = [
                {"timestamp": "2026-07-17T00:00:00Z", "type": "session_meta", "payload": {"id": session_id}},
                {
                    "timestamp": "2026-07-17T00:00:01Z",
                    "type": "response_item",
                    "payload": {
                        "type": "custom_tool_call",
                        "name": "exec",
                        "input": (
                            "const r = await tools.mcp__node_repl__js({\"code\":\""
                            "await agent.browsers.get(\\\"iab\\\");\"});"
                        ),
                    },
                },
                {
                    "timestamp": "2026-07-17T00:00:02Z",
                    "type": "response_item",
                    "payload": {
                        "type": "custom_tool_call_output",
                        "output": "Browser is not available: iab",
                    },
                },
            ]
            rollout.write_text("\n".join(json.dumps(event) for event in events) + "\n", encoding="utf-8")

            audit = runner._audit_browser_activity(
                codex_home,
                (self._browser_run_spec("browser-suite"),),
                {
                    "scenarioBindings": [
                        {
                            "suite": "browser-suite",
                            "scenario": "happy",
                            "kind": "target",
                            "sessionId": session_id,
                        }
                    ]
                },
                {"runs": [self._suite_report("browser-suite", "BLOCKED")]},
            )

            self.assertEqual(1, audit["blockedTargetSessions"])

    def test_browser_activity_audit_rejects_external_browser_selection(self) -> None:
        """Browser evidence cannot select Chrome or an external destination."""
        with tempfile.TemporaryDirectory() as temporary:
            codex_home = Path(temporary)
            session_id = "target-session"
            rollout = codex_home / f"rollout-{session_id}.jsonl"
            events = [
                {"timestamp": "2026-07-17T00:00:00Z", "type": "session_meta", "payload": {"id": session_id}},
                {
                    "timestamp": "2026-07-17T00:00:01Z",
                    "type": "response_item",
                    "payload": {
                        "type": "function_call",
                        "name": "mcp__node_repl__js",
                        "arguments": json.dumps(
                            {"code": "await agent.browsers.get('extension'); await tab.goto('https://example.com')"}
                        ),
                    },
                },
            ]
            rollout.write_text("\n".join(json.dumps(event) for event in events) + "\n", encoding="utf-8")

            with self.assertRaisesRegex(RuntimeError, "external browser or destination"):
                runner._audit_browser_activity(
                    codex_home,
                    (self._browser_run_spec("browser-suite"),),
                    {
                        "scenarioBindings": [
                            {
                                "suite": "browser-suite",
                                "scenario": "happy",
                                "kind": "target",
                                "sessionId": session_id,
                            }
                        ]
                    },
                    {"runs": [self._suite_report("browser-suite", "BLOCKED")]},
                )

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

    def test_malformed_checkpoint_receipts_retain_bounded_live_batch_evidence(self) -> None:
        """Checkpoint fallback reports malformed receipts without losing retained evidence paths."""
        malformed_receipts = {
            "missing-lane": {},
            "wrong-type-lane": {"lane": []},
            "missing-role": {"lane": "source"},
            "wrong-type-role": {"lane": "source", "role": []},
            "missing-commit": {
                "lane": "source",
                "role": {"invocation": "dev_coder", "sessionIds": ["producer"]},
            },
        }
        for name, receipt in malformed_receipts.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                result_root = root / "results"
                run = self._checkpoint_handoff_run_spec()
                target = runner._Session(
                    "target", "supervisor", "target_agent", 2, 1.0, 8.0, frozenset()
                )
                producer = runner._Session(
                    "producer", "target", "dev_coder", 3, 2.0, 3.0, frozenset()
                )

                def stage_batch(batch: object, run_root: Path) -> tuple[Path, Path, tuple[object, ...]]:
                    workspace = run_root / "workspace"
                    codex_home = run_root / "codex-home"
                    (workspace / ".git").mkdir(parents=True)
                    codex_home.mkdir()
                    return workspace, codex_home, ()

                def run_process(command: object, *arguments: object, **keywords: object) -> dict[str, object]:
                    values = list(command)
                    add_dirs = [Path(values[index + 1]) for index, value in enumerate(values) if value == "--add-dir"]
                    checkpoint_root = add_dirs[-1]
                    checkpoint = checkpoint_root / "checkpoint-suite" / "happy.json"
                    checkpoint.parent.mkdir()
                    checkpoint.write_text(
                        json.dumps(
                            {
                                "suite": "checkpoint-suite",
                                "scenario": "happy",
                                "status": "PASS",
                                "targetInvoked": True,
                                "judgeInvoked": True,
                                "identityEvidence": ["bound"],
                                "deterministicEvidence": [],
                                "modelJudgeEvidence": ["judge-bound"],
                                "evidenceReceipts": [],
                                "evidence": ["receipt"],
                                "cleanup": "clean",
                                "residualRisk": "none",
                                "handoffReceipts": [receipt],
                            }
                        ),
                        encoding="utf-8",
                    )
                    return {"exitCode": 1, "stdout": "", "stderr": "coordinator failed", "cleanup": "clean"}

                with (
                    mock.patch.object(runner, "_stage_batch", side_effect=stage_batch),
                    mock.patch.object(runner, "_bundled_codex_executable", return_value=Path("/bin/false")),
                    mock.patch.object(runner, "_controlled_environment", return_value={}),
                    mock.patch.object(runner, "_preflight_runtime_capabilities", return_value=()),
                    mock.patch.object(runner, "_run_process", side_effect=run_process),
                    mock.patch.object(runner, "_audit_identity", return_value={"scenarioBindings": []}),
                    mock.patch.object(runner, "_audit_browser_activity", return_value={}),
                    mock.patch.object(runner, "_load_sessions", return_value=(target, producer)),
                    mock.patch.object(runner, "_audit_session_concurrency", return_value={}),
                    mock.patch.object(
                        runner,
                        "_bind_target_sessions",
                        return_value={("checkpoint-suite", "happy"): target},
                    ),
                ):
                    results = runner._execute_batches(
                        ((run,),),
                        lambda batch, batch_number: runner._run_live_batch(
                            batch,
                            batch_number,
                            result_root,
                            timeout_seconds=1,
                        ),
                    )

                result = results[0]
                self.assertEqual("infrastructure-failed", result["status"])
                self.assertNotIn("error", result)
                self.assertIn("checkpoint", " ".join(result["infrastructureErrors"]))
                self.assertIn("handoff receipt", " ".join(result["infrastructureErrors"]))
                for evidence_name, evidence_path in result["evidence"].items():
                    if evidence_name.endswith("Sha256"):
                        continue
                    self.assertTrue(Path(evidence_path).exists(), evidence_path)

    def test_partial_results_inside_one_batch_remain_addressable(self) -> None:
        """A failed scenario does not erase completed scenario results from the same batch."""
        batch = (self._run_spec("one", 1), self._run_spec("two", 2))
        run_identity = "codex-batch-01-test"
        report = {
            "runs": [
                self._suite_report("one", "PASS"),
                self._suite_report("two", "FAIL"),
            ],
            "batchCleanup": "clean",
            "residualRisk": "none",
        }
        with tempfile.TemporaryDirectory() as temporary:
            checkpoint_root = Path(temporary)
            first = self._write_receipt_checkpoint(checkpoint_root, batch[0], run_identity)
            second = self._write_receipt_checkpoint(
                checkpoint_root,
                batch[1],
                run_identity,
                status="FAIL",
            )
            checkpoint_report = runner._load_checkpoint_report(
                checkpoint_root,
                batch,
                run_identity,
            )
            assert checkpoint_report is not None
            self._bind_checkpoint_judges(
                checkpoint_root,
                checkpoint_report,
                batch,
            )
        assert checkpoint_report is not None
        report["runs"][0]["scenarioResults"][0]["evidenceReceipts"] = first["evidenceReceipts"]
        report["runs"][1]["scenarioResults"][0]["evidenceReceipts"] = second["evidenceReceipts"]

        audited = runner._audit_report(batch, report, checkpoint_report)

        self.assertEqual(["PASS", "FAIL"], [item["scenarioResults"][0]["status"] for item in audited])

    @classmethod
    def _checkpoint_handoff_run_spec(cls) -> object:
        """Build one scenario whose checkpoint requires a structured source receipt."""
        suite = cls._suite("checkpoint-suite")
        scenario = dict(suite.scenarios[0])
        scenario["requiredHandoffReceiptLanes"] = ["source"]
        scenario["requiredHandoffReceiptFields"] = [
            "lane",
            "role",
            "commit",
            "review",
            "verification",
            "claimRelease",
        ]
        suite = runner._Suite(
            suite.suite_id,
            suite.priority,
            suite.path,
            suite.manifest,
            (scenario,),
        )
        return runner._RunSpec(suite, ("happy",))

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

    def test_agent_path_without_runtime_developer_binding_fails_identity_audit(self) -> None:
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

    def test_arbitrary_agent_message_does_not_bind_instructions(self) -> None:
        """A marker outside the runtime developer input cannot bind a definition."""
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

    def test_nested_use_of_a_direct_role_does_not_inflate_direct_identity_count(self) -> None:
        """A validated depth-three dependency may share an invocation with direct suite targets."""
        with tempfile.TemporaryDirectory() as temporary:
            codex_home = Path(temporary)
            sessions = codex_home / "sessions"
            sessions.mkdir()
            marker = "AGENT_INSTRUCTION_BINDING_dev_merge_coordinator_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
            for index in range(3):
                self._write_rollout(
                    sessions / f"rollout-direct-{index}.jsonl",
                    "dev_merge_coordinator",
                    depth=2,
                    marker=marker,
                    started_second=index * 3,
                )
            self._write_rollout(
                sessions / "rollout-nested.jsonl",
                "dev_merge_coordinator",
                depth=3,
                marker=marker,
                started_second=12,
            )
            staged = (
                runner._StagedAgent(
                    "dev_merge_coordinator", Path("merge.toml"), "instructions", "a" * 64, marker
                ),
            )

            identity = runner._audit_identity(staged, codex_home, {"dev_merge_coordinator": 3})

        self.assertEqual(3, identity["agents"][0]["requiredSessionCount"])
        self.assertEqual(4, len(identity["agents"][0]["boundSessionIds"]))

    def test_immediately_closed_default_noop_is_excluded_from_suite_identity(self) -> None:
        """An inert coordinator discovery child cannot become a second suite supervisor."""
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
                sessions / "rollout-supervisor.jsonl", "suite_supervisor", 1, markers["suite_supervisor"]
            )
            self._write_rollout(
                sessions / "rollout-target.jsonl",
                "target_agent",
                2,
                markers["target_agent"],
                parent="rollout-supervisor",
                started_second=2,
            )
            self._write_rollout(
                sessions / "rollout-judge.jsonl",
                "suite_judge",
                2,
                markers["suite_judge"],
                parent="rollout-supervisor",
                started_second=5,
            )
            self._write_noop_rollout(sessions / "rollout-default-noop.jsonl")
            run = runner._RunSpec(self._suite("one"), ("happy",))
            report = {
                "runs": [{
                    "suite": "one",
                    "scenarioResults": [{
                        "scenario": "happy", "targetInvoked": True, "judgeInvoked": True
                    }],
                }]
            }
            staged = tuple(
                runner._StagedAgent(invocation, Path(f"{invocation}.toml"), "instructions", key * 64, marker)
                for invocation, key, marker in (
                    ("suite_supervisor", "a", markers["suite_supervisor"]),
                    ("target_agent", "b", markers["target_agent"]),
                    ("suite_judge", "c", markers["suite_judge"]),
                )
            )

            identity = runner._audit_identity(
                staged,
                codex_home,
                {"suite_supervisor": 1, "target_agent": 1, "suite_judge": 1},
                (run,),
                report,
            )
            concurrency = runner._audit_session_concurrency(
                runner._load_sessions(codex_home), 9, (run,), report
            )

        self.assertEqual(4, identity["rolloutCount"])
        self.assertEqual(3, identity["suiteLifecycleRolloutCount"])
        self.assertEqual("rollout-default-noop", identity["excludedSessions"][0]["sessionId"])
        self.assertIn("turn-aborted", identity["excludedSessions"][0]["reason"])
        self.assertRegex(identity["excludedSessions"][0]["rolloutSha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(1, concurrency["excludedSessionCount"])

    def test_default_identity_with_agent_work_remains_participating(self) -> None:
        """A default child that produces agent output still fails strict supervisor attribution."""
        run = runner._RunSpec(self._suite("one"), ("happy",))
        sessions = (
            runner._Session("supervisor", "root", "suite_supervisor", 1, 0.0, 8.0, frozenset()),
            runner._Session("default", "root", "default", 1, 1.0, 2.0, frozenset()),
        )

        with self.assertRaisesRegex(RuntimeError, "Supervisor identity mismatch"):
            runner._audit_session_concurrency(sessions, 9, (run,))

    def test_malformed_default_noop_evidence_remains_participating(self) -> None:
        """Incomplete rollout parsing cannot prove that a default child performed no work."""
        with tempfile.TemporaryDirectory() as temporary:
            codex_home = Path(temporary)
            sessions = codex_home / "sessions"
            sessions.mkdir()
            noop_path = sessions / "rollout-default-noop.jsonl"
            self._write_noop_rollout(noop_path)
            noop_path.write_text(
                noop_path.read_text(encoding="utf-8") + '{"timestamp":"2026-07-17T00:00:03Z",broken}\n',
                encoding="utf-8",
            )
            loaded = runner._load_sessions(codex_home)
            run = runner._RunSpec(self._suite("one"), ("happy",))
            participating, excluded = runner._suite_lifecycle_sessions(loaded, (run,))

        self.assertEqual((), tuple(excluded))
        self.assertEqual(("rollout-default-noop",), tuple(session.session_id for session in participating))

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

            python_executable = Path("/runtime/python3.11")
            staged = runner._copy_agent(source, "target_agent", agent_root, python_executable)
            loaded = runner.tomllib.loads((agent_root / "target_agent.toml").read_text(encoding="utf-8"))

        self.assertIn(staged.instruction_marker, loaded["developer_instructions"])
        self.assertIn(str(python_executable), loaded["developer_instructions"])
        self.assertIn("instead of python or python3", loaded["developer_instructions"])
        self.assertEqual("gpt-5.6-sol", loaded["model"])

    def test_staging_preserves_an_explicit_agent_model(self) -> None:
        """A generated target profile keeps its declared model during instrumentation."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source.toml"
            agent_root = root / "agents"
            agent_root.mkdir()
            source.write_text(
                'name = "target_agent"\nmodel = "gpt-5.6-terra"\ndeveloper_instructions = """governed"""\n',
                encoding="utf-8",
            )

            runner._copy_agent(source, "target_agent", agent_root)
            loaded = runner.tomllib.loads((agent_root / "target_agent.toml").read_text(encoding="utf-8"))

        self.assertEqual("gpt-5.6-terra", loaded["model"])

    def test_staged_agents_are_registered_as_codex_config_files(self) -> None:
        """A task name alone cannot replace the custom-agent config registration."""
        with tempfile.TemporaryDirectory() as temporary:
            codex_home = Path(temporary)
            agent_root = codex_home / "agents"
            agent_root.mkdir()
            (agent_root / "target_agent.toml").write_text(
                'name = "target_agent"\ndescription = "Target description."\n', encoding="utf-8"
            )
            staged = (
                runner._StagedAgent(
                    "target_agent", Path("target.toml"), "instructions", "a" * 64, "binding-marker"
                ),
            )

            arguments = runner._agent_registration_arguments(staged, codex_home)

        self.assertEqual("-c", arguments[0])
        self.assertIn("agents.target_agent.description=", arguments[1])
        self.assertIn("agents.target_agent.config_file=", arguments[3])
        self.assertIn("/agents/target_agent.toml", arguments[3])

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

    def test_declared_nested_dependency_order_is_audited(self) -> None:
        """A task-selected dependency cannot run before its declared predecessor."""
        suite = self._suite("ordered", nested_limit=1)
        scenario = dict(suite.scenarios[0])
        scenario["taskSelectedAgentDependencies"] = ["reviewer"]
        scenario["requiredDependencyOrder"] = ["dependency", "reviewer"]
        suite = runner._Suite(suite.suite_id, suite.priority, suite.path, suite.manifest, (scenario,))
        run = runner._RunSpec(suite, ("happy",))
        sessions = (
            runner._Session("supervisor", "root", "suite_supervisor", 1, 0.0, 10.0, frozenset()),
            runner._Session("target", "supervisor", "target_agent", 2, 1.0, 8.0, frozenset()),
            runner._Session("reviewer", "target", "reviewer", 3, 2.0, 3.0, frozenset()),
            runner._Session("dependency", "target", "dependency", 3, 4.0, 5.0, frozenset()),
        )
        report = {
            "runs": [
                {
                    "suite": "ordered",
                    "scenarioResults": [
                        {"scenario": "happy", "targetInvoked": True, "judgeInvoked": False}
                    ],
                }
            ]
        }

        with self.assertRaisesRegex(RuntimeError, "Dependency order mismatch for ordered:happy"):
            runner._audit_session_concurrency(
                sessions,
                maximum_threads=9,
                batch=(run,),
                report=report,
            )

    def test_task_selected_dependency_cannot_leak_into_fixed_only_scenario(self) -> None:
        """Full-suite registration cannot authorize a selected role under another scenario target."""
        suite = self._suite("mixed-scenarios", nested_limit=1)
        fixed = dict(suite.scenarios[0], id="fixed")
        selected = dict(
            suite.scenarios[0],
            id="selected",
            taskSelectedAgentDependencies=["reviewer"],
        )
        suite = runner._Suite(suite.suite_id, suite.priority, suite.path, suite.manifest, (fixed, selected))
        run = runner._RunSpec(suite, ("fixed", "selected"))
        sessions = (
            runner._Session("supervisor", "root", "suite_supervisor", 1, 0.0, 20.0, frozenset()),
            runner._Session("fixed-target", "supervisor", "target_agent", 2, 1.0, 8.0, frozenset()),
            runner._Session("leaked", "fixed-target", "reviewer", 3, 2.0, 3.0, frozenset()),
            runner._Session("selected-target", "supervisor", "target_agent", 2, 10.0, 18.0, frozenset()),
            runner._Session("allowed", "selected-target", "reviewer", 3, 11.0, 12.0, frozenset()),
        )
        report = {
            "runs": [
                {
                    "suite": "mixed-scenarios",
                    "scenarioResults": [
                        {"scenario": "fixed", "targetInvoked": True, "judgeInvoked": False},
                        {"scenario": "selected", "targetInvoked": True, "judgeInvoked": False},
                    ],
                }
            ]
        }

        with self.assertRaisesRegex(
            RuntimeError,
            "Nested dependency reviewer is not allowed for mixed-scenarios:fixed",
        ):
            runner._audit_session_concurrency(
                sessions,
                maximum_threads=9,
                batch=(run,),
                report=report,
            )

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

    def test_workspace_inventory_requires_the_matching_mutation_gate(self) -> None:
        """A scenario cannot request structured inventory without its deterministic gate."""
        suite = runner._load_catalog(include_ids={"dev-code-reviewer"})["dev-code-reviewer"]
        scenario = dict(suite.scenarios[0])
        scenario["requiresWorkspaceInventory"] = True
        scenario["deterministicChecks"] = [
            check for check in scenario["deterministicChecks"] if check != "no-forbidden-mutation"
        ]
        scenarios = (scenario, *suite.scenarios[1:])
        suite = runner._Suite(suite.suite_id, suite.priority, suite.path, suite.manifest, scenarios)

        with self.assertRaisesRegex(ValueError, "workspace inventory requires no-forbidden-mutation"):
            runner._validate_suite(suite, require_executable=False)

    def test_controlled_environment_does_not_inherit_host_credentials(self) -> None:
        """Only process-location and locale values cross the host boundary."""
        bundled_node = Path("/tmp/runtime/bin/node")
        bundled_python = Path("/tmp/python/bin/python3.11")
        environment = runner._controlled_environment(
            Path("/tmp/home"),
            Path("/tmp/codex"),
            Path("/tmp/work"),
            bundled_node,
            bundled_python,
        )

        self.assertNotIn("CODEX_AUTH_FILE", environment)
        self.assertNotIn("OPENAI_API_KEY", environment)
        self.assertEqual("/tmp/codex", environment["CODEX_HOME"])
        self.assertEqual("1", environment["PYTHONDONTWRITEBYTECODE"])
        self.assertEqual(
            ["/tmp/python/bin", "/tmp/runtime/bin"],
            environment["PATH"].split(os.pathsep)[:2],
        )

    def test_controlled_environment_forces_staged_maven_repository_offline(self) -> None:
        """Targets cannot bypass the isolated repository or reach Maven Central."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            home = root / "home"
            repository = home / ".m2" / "repository"
            repository.mkdir(parents=True)
            (repository / ".agent-suite-offline").write_text("governed\n", encoding="utf-8")

            environment = runner._controlled_environment(
                home,
                root / "codex",
                root / "tmp",
                Path("/tmp/runtime/bin/node"),
                Path("/tmp/python/bin/python3.11"),
            )

        self.assertEqual(
            f"--offline -Dmaven.repo.local={repository}",
            environment["MAVEN_ARGS"],
        )

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

    def test_critical_deterministic_failure_may_skip_judge(self) -> None:
        """An exact failed critical-check receipt can authorize the matching Judge skip."""
        run = self._run_spec("one", 1)
        manifest = dict(run.suite.manifest)
        manifest["acceptance"] = {"criticalFailureSkipsJudge": True}
        suite = runner._Suite(
            suite_id=run.suite.suite_id,
            priority=run.suite.priority,
            path=run.suite.path,
            manifest=manifest,
            scenarios=run.suite.scenarios,
        )
        batch = (runner._RunSpec(suite=suite, scenario_ids=run.scenario_ids),)
        run_identity = "codex-batch-01-test"
        with tempfile.TemporaryDirectory() as temporary:
            checkpoint_root = Path(temporary)
            self._write_receipt_checkpoint(
                checkpoint_root,
                batch[0],
                run_identity,
                status="FAIL",
                judge_invoked=False,
            )
            checkpoint_report = runner._load_checkpoint_report(
                checkpoint_root,
                batch,
                run_identity,
            )
            assert checkpoint_report is not None
            self._bind_checkpoint_judges(
                checkpoint_root,
                checkpoint_report,
                batch,
            )

        assert checkpoint_report is not None
        report = json.loads(json.dumps(checkpoint_report))
        report["batchCleanup"] = "clean"
        runner._audit_report(batch, report, checkpoint_report)
        receipt_audit = checkpoint_report["runs"][0]["scenarioResults"][0]["receiptAudit"]
        self.assertEqual("skipped-critical-failure", receipt_audit["judgeDisposition"])
        self.assertEqual("harness-agent-identity", receipt_audit["failedCriticalCheck"])

    def test_model_authored_evidence_strings_cannot_substitute_for_receipts(self) -> None:
        """Repeated checkpoint prose cannot prove deterministic checks or a Judge disposition."""
        batch = (self._run_spec("one", 1),)
        report = {
            "runs": [self._suite_report("one", "PASS")],
            "batchCleanup": "clean",
            "residualRisk": "none",
        }

        with self.assertRaisesRegex(RuntimeError, "validated evidence receipts"):
            runner._audit_report(batch, report)

    def test_retained_receipts_bind_exact_checks_and_actual_judge_disposition(self) -> None:
        """A terminal result passes only with selected-identity receipts and retained digest-bound artifacts."""
        batch = (self._run_spec("one", 1),)
        run_identity = "codex-batch-01-test"
        with tempfile.TemporaryDirectory() as temporary:
            checkpoint_root = Path(temporary)
            checkpoint = self._write_receipt_checkpoint(checkpoint_root, batch[0], run_identity)
            checkpoint_report = runner._load_checkpoint_report(
                checkpoint_root,
                batch,
                run_identity,
            )
            assert checkpoint_report is not None
            self._bind_checkpoint_judges(
                checkpoint_root,
                checkpoint_report,
                batch,
            )

        assert checkpoint_report is not None
        result = checkpoint_report["runs"][0]["scenarioResults"][0]
        self.assertEqual("PASS", result["status"])
        self.assertEqual("verified", result["receiptAudit"]["status"])
        self.assertEqual("passed", result["receiptAudit"]["judgeDisposition"])
        report = {
            "runs": [self._suite_report("one", "PASS")],
            "batchCleanup": "clean",
            "residualRisk": "none",
        }
        report["runs"][0]["scenarioResults"][0]["evidenceReceipts"] = checkpoint["evidenceReceipts"]
        runner._audit_report(batch, report, checkpoint_report)
        runner._attach_receipt_audits(report, checkpoint_report)
        self.assertEqual(
            "verified",
            report["runs"][0]["scenarioResults"][0]["receiptAudit"]["status"],
        )

    def test_supervisor_judge_output_without_bound_child_response_is_non_passing(
        self,
    ) -> None:
        """A supervisor-authored receipt and output cannot prove what the Judge child returned."""
        batch = (self._run_spec("one", 1),)
        run_identity = "codex-batch-01-test"
        with tempfile.TemporaryDirectory() as temporary:
            checkpoint_root = Path(temporary)
            self._write_receipt_checkpoint(
                checkpoint_root,
                batch[0],
                run_identity,
            )
            checkpoint_report = runner._load_checkpoint_report(
                checkpoint_root,
                batch,
                run_identity,
            )

        assert checkpoint_report is not None
        result = checkpoint_report["runs"][0]["scenarioResults"][0]
        self.assertEqual("BLOCKED", result["status"])
        self.assertNotEqual("verified", result["receiptAudit"]["status"])
        self.assertIsNone(result["receiptAudit"].get("judgeProvenance"))

    def test_judge_child_provenance_rejects_runtime_substitution_boundaries(self) -> None:
        """Only the exact selected Judge session and its exact terminal bytes can restore PASS."""
        cases = (
            "absent",
            "malformed",
            "mismatched-session",
            "mismatched-digest",
            "supervisor-substitute",
        )
        for case in cases:
            with self.subTest(case=case), tempfile.TemporaryDirectory() as temporary:
                checkpoint_root = Path(temporary)
                batch = (self._run_spec("one", 1),)
                run_identity = "codex-batch-01-test"
                self._write_receipt_checkpoint(
                    checkpoint_root,
                    batch[0],
                    run_identity,
                )
                checkpoint_report = runner._load_checkpoint_report(
                    checkpoint_root,
                    batch,
                    run_identity,
                )
                assert checkpoint_report is not None
                scenario = checkpoint_report["runs"][0]["scenarioResults"][0]
                output_reference = scenario["receiptAudit"]["judgeOutput"]
                output_path = checkpoint_root / output_reference["path"]
                valid_response = output_path.read_bytes()
                sessions = checkpoint_root / ".sessions"
                sessions.mkdir()
                expected_invocation = str(
                    batch[0].suite.manifest["execution"]["judgeInvocation"]
                )
                bound_session_id = "rollout-judge"
                if case == "mismatched-session":
                    bound_session_id = "rollout-target"
                    self._write_rollout(
                        sessions / "rollout-target.jsonl",
                        "target_agent",
                        depth=2,
                        parent="rollout-supervisor",
                        final_response=valid_response,
                    )
                elif case == "supervisor-substitute":
                    bound_session_id = "rollout-supervisor-substitute"
                    self._write_rollout(
                        sessions / "rollout-supervisor-substitute.jsonl",
                        "suite_supervisor",
                        depth=2,
                        parent="rollout-supervisor",
                        final_response=valid_response,
                    )
                elif case != "absent":
                    self._write_rollout(
                        sessions / "rollout-judge.jsonl",
                        expected_invocation,
                        depth=2,
                        parent="rollout-supervisor",
                        final_response=(
                            b"not-json" if case == "malformed" else valid_response
                        ),
                    )
                if case == "mismatched-digest":
                    output_path.write_bytes(b"post-audit supervisor substitution")
                identity = {
                    "scenarioBindings": [
                        {
                            "suite": "one",
                            "scenario": "happy",
                            "kind": "judge",
                            "invocation": expected_invocation,
                            "sessionId": bound_session_id,
                            "parentSessionId": "rollout-supervisor",
                        }
                    ]
                }

                runner._bind_codex_judge_provenance(
                    checkpoint_report,
                    identity,
                    batch,
                    checkpoint_root,
                    sessions,
                    checkpoint_root,
                )

                self.assertEqual("BLOCKED", scenario["status"])
                self.assertEqual("invalid", scenario["receiptAudit"]["status"])
                self.assertIsNone(scenario["receiptAudit"]["judgeProvenance"])
                self.assertTrue(scenario["receiptAudit"]["diagnostics"])

    def test_invalid_receipts_are_retained_diagnostically_and_block_terminal_status(self) -> None:
        """Missing, malformed, mismatched, duplicate, unretained, and incompatible receipts never pass."""
        batch = (self._run_spec("one", 1),)
        run_identity = "codex-batch-01-test"

        def mutate_case(case: str, root: Path, checkpoint: dict[str, object]) -> None:
            references = checkpoint["evidenceReceipts"]
            assert isinstance(references, list)
            if case == "missing":
                references.pop()
            elif case == "malformed":
                references[0]["sha256"] = "not-a-digest"
            elif case == "mismatched":
                self._rewrite_receipt(
                    root,
                    checkpoint,
                    "deterministic-check-disposition",
                    lambda receipt: receipt.__setitem__("scenario", "wrong-scenario"),
                )
            elif case == "duplicate":
                references.append(dict(references[0]))
            elif case == "unretained":
                references[-1] = {
                    "path": "one/happy/receipts/missing.json",
                    "sha256": "0" * 64,
                }
            elif case == "incompatible":
                self._rewrite_receipt(
                    root,
                    checkpoint,
                    "judge-disposition",
                    lambda receipt: receipt.__setitem__("disposition", "failed"),
                )
            else:
                raise AssertionError(case)

        for case in (
            "missing",
            "malformed",
            "mismatched",
            "duplicate",
            "unretained",
            "incompatible",
        ):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as temporary:
                checkpoint_root = Path(temporary)
                checkpoint = self._write_receipt_checkpoint(checkpoint_root, batch[0], run_identity)
                mutate_case(case, checkpoint_root, checkpoint)
                path = checkpoint_root / "one" / "happy.json"
                path.write_text(json.dumps(checkpoint, indent=2, sort_keys=True) + "\n", encoding="utf-8")
                checkpoint_report = runner._load_checkpoint_report(
                    checkpoint_root,
                    batch,
                    run_identity,
                )

            assert checkpoint_report is not None
            result = checkpoint_report["runs"][0]["scenarioResults"][0]
            self.assertEqual("BLOCKED", result["status"])
            self.assertEqual("invalid", result["receiptAudit"]["status"])
            self.assertTrue(result["receiptAudit"]["diagnostics"])

    def test_required_workspace_inventory_rejects_prose_and_unrestored_mutation(self) -> None:
        """Read-only mutation receipts bind complete inventory evidence and a restored baseline."""
        suite = self._suite("one")
        scenario = dict(suite.scenarios[0])
        scenario["deterministicChecks"] = ["no-forbidden-mutation"]
        scenario["requiresWorkspaceInventory"] = True
        suite = runner._Suite(suite.suite_id, suite.priority, suite.path, suite.manifest, (scenario,))
        run = runner._RunSpec(suite=suite, scenario_ids=("happy",))
        run_identity = "codex-batch-01-test"

        for case in ("prose", "unrestored"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as temporary:
                checkpoint_root = Path(temporary)
                checkpoint = self._write_receipt_checkpoint(checkpoint_root, run, run_identity)
                if case == "unrestored":
                    self._replace_deterministic_artifact(
                        checkpoint_root,
                        checkpoint,
                        "no-forbidden-mutation",
                        self._workspace_mutation_evidence(final_matches=False),
                    )
                path = checkpoint_root / "one" / "happy.json"
                path.write_text(json.dumps(checkpoint, indent=2, sort_keys=True) + "\n", encoding="utf-8")
                report = runner._load_checkpoint_report(
                    checkpoint_root,
                    (run,),
                    run_identity,
                    require_runtime_judge_provenance=False,
                )

            assert report is not None
            result = report["runs"][0]["scenarioResults"][0]
            self.assertEqual("BLOCKED", result["status"])
            self.assertEqual("invalid", result["receiptAudit"]["status"])

    def test_required_workspace_inventory_accepts_detected_cleaned_side_effects(self) -> None:
        """Owned ignored artifacts remain visible even after exact cleanup restores the baseline."""
        suite = self._suite("one")
        scenario = dict(suite.scenarios[0])
        scenario["deterministicChecks"] = ["no-forbidden-mutation"]
        scenario["requiresWorkspaceInventory"] = True
        suite = runner._Suite(suite.suite_id, suite.priority, suite.path, suite.manifest, (scenario,))
        run = runner._RunSpec(suite=suite, scenario_ids=("happy",))
        run_identity = "codex-batch-01-test"
        with tempfile.TemporaryDirectory() as temporary:
            checkpoint_root = Path(temporary)
            checkpoint = self._write_receipt_checkpoint(checkpoint_root, run, run_identity)
            self._replace_deterministic_artifact(
                checkpoint_root,
                checkpoint,
                "no-forbidden-mutation",
                self._workspace_mutation_evidence(final_matches=True),
            )
            path = checkpoint_root / "one" / "happy.json"
            path.write_text(json.dumps(checkpoint, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            report = runner._load_checkpoint_report(
                checkpoint_root,
                (run,),
                run_identity,
                require_runtime_judge_provenance=False,
            )

        assert report is not None
        result = report["runs"][0]["scenarioResults"][0]
        self.assertEqual("PASS", result["status"])
        self.assertEqual("verified", result["receiptAudit"]["status"])

    def test_workspace_inventory_rejects_wrong_roots_and_unsafe_entries(self) -> None:
        """Retained inventory structure cannot escape or substitute the protected workspace."""
        for case in ("wrong-root", "unsafe-path", "malformed-entry", "invented-preexisting"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as temporary:
                evidence = self._workspace_mutation_evidence(final_matches=True)
                if case == "unsafe-path":
                    evidence["observed"]["entries"][-1]["path"] = "../../outside"
                elif case == "malformed-entry":
                    evidence["final"]["entries"] = ["not-an-entry"]
                elif case == "invented-preexisting":
                    evidence["preExisting"] = {
                        "ignored": ["invented.pyc"],
                        "untracked": ["invented.txt"],
                    }
                diagnostics: list[str] = []
                runner._validate_workspace_mutation_evidence(
                    evidence,
                    "inventory",
                    diagnostics,
                    None if case != "wrong-root" else Path(temporary),
                )

            self.assertTrue(diagnostics)

    def test_runner_owned_baseline_rejects_a_late_self_consistent_snapshot(self) -> None:
        """A supervisor cannot hide a mutation by capturing its baseline after target work."""
        suite = runner._load_catalog(include_ids={"dev-code-reviewer"})["dev-code-reviewer"]
        run = runner._RunSpec(suite=suite, scenario_ids=("incomplete-review-evidence",))
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixture_root = root / "fixtures"
            checkpoint_root = root / "checkpoints"
            fixture_root.mkdir()
            checkpoint_root.mkdir()
            baselines = runner._stage_workspace_inventory_fixtures(
                (run,), fixture_root, checkpoint_root
            )
            protected = fixture_root / "dev-code-reviewer" / "incomplete-review-evidence"
            baseline_file = (
                checkpoint_root
                / "dev-code-reviewer"
                / "incomplete-review-evidence"
                / "artifacts"
                / "workspace-baseline.json"
            )
            prompt = runner._coordinator_prompt(
                (run,), checkpoint_root, fixture_root, "test-run", baselines
            )
            self.assertIn(runner._sha256(baseline_file), prompt)
            (protected / "late-created.pyc").write_bytes(b"hidden mutation")
            late_baseline_path = root / "late-baseline.json"
            runner.workspace_inventory_support._write_json(
                late_baseline_path,
                runner.workspace_inventory_support._inventory(protected),
            )
            evidence = runner.workspace_inventory_support._mutation_evidence(
                protected,
                late_baseline_path,
                False,
                runner.workspace_inventory_support._file_sha256(late_baseline_path),
            )
            diagnostics: list[str] = []
            runner._validate_workspace_mutation_evidence(
                evidence,
                "inventory",
                diagnostics,
                protected,
                baselines[("dev-code-reviewer", "incomplete-review-evidence")],
            )

        self.assertTrue(diagnostics)

    def test_wrong_identity_critical_skip_rows_remain_non_passing(self) -> None:
        """Every structured skip field must match the failed selected critical gate exactly."""
        run = self._run_spec("one", 1)
        manifest = dict(run.suite.manifest)
        manifest["acceptance"] = {"criticalFailureSkipsJudge": True}
        suite = runner._Suite(run.suite.suite_id, run.suite.priority, run.suite.path, manifest, run.suite.scenarios)
        batch = (runner._RunSpec(suite=suite, scenario_ids=run.scenario_ids),)
        run_identity = "codex-batch-01-test"
        mutations = {
            "eventType": lambda receipt: receipt.__setitem__("eventType", "critical-skip-prose"),
            "suite": lambda receipt: receipt.__setitem__("suite", "wrong-suite"),
            "scenario": lambda receipt: receipt.__setitem__("scenario", "wrong-scenario"),
            "checkId": lambda receipt: receipt.__setitem__("checkId", "test-state-transition"),
            "critical": lambda receipt: receipt.__setitem__("critical", False),
            "deterministicVerdict": lambda receipt: receipt.__setitem__("deterministicVerdict", "passed"),
            "disposition": lambda receipt: receipt.__setitem__("disposition", "skipped-by-prose"),
        }
        for field, mutation in mutations.items():
            with self.subTest(field=field), tempfile.TemporaryDirectory() as temporary:
                checkpoint_root = Path(temporary)
                checkpoint = self._write_receipt_checkpoint(
                    checkpoint_root,
                    batch[0],
                    run_identity,
                    status="FAIL",
                    judge_invoked=False,
                )
                self._rewrite_receipt(
                    checkpoint_root,
                    checkpoint,
                    "judge-skip-disposition",
                    mutation,
                )
                path = checkpoint_root / "one" / "happy.json"
                path.write_text(json.dumps(checkpoint, indent=2, sort_keys=True) + "\n", encoding="utf-8")
                checkpoint_report = runner._load_checkpoint_report(
                    checkpoint_root,
                    batch,
                    run_identity,
                )

            assert checkpoint_report is not None
            result = checkpoint_report["runs"][0]["scenarioResults"][0]
            self.assertEqual("BLOCKED", result["status"])
            self.assertEqual("invalid", result["receiptAudit"]["status"])

    def test_unproved_critical_failure_skip_does_not_bypass_judge_requirement(self) -> None:
        """A missing Judge is rejected unless both manifest authority and explicit skip evidence are present."""
        batch = (self._run_spec("one", 1),)
        report = {
            "runs": [self._suite_report("one", "FAIL")],
            "batchCleanup": "clean",
            "residualRisk": "none",
        }
        report["runs"][0]["scenarioResults"][0]["judgeInvoked"] = False
        report["runs"][0]["scenarioResults"][0]["modelJudgeEvidence"] = []

        with self.assertRaisesRegex(RuntimeError, "validated evidence receipts"):
            runner._audit_report(batch, report)

    def test_judge_skip_rejects_model_judge_evidence(self) -> None:
        """A critical skip cannot retain evidence attributed to a Judge that did not run."""
        run = self._run_spec("one", 1)
        manifest = dict(run.suite.manifest)
        manifest["acceptance"] = {"criticalFailureSkipsJudge": True}
        suite = runner._Suite(run.suite.suite_id, run.suite.priority, run.suite.path, manifest, run.suite.scenarios)
        batch = (runner._RunSpec(suite=suite, scenario_ids=run.scenario_ids),)
        report = {
            "runs": [self._suite_report("one", "FAIL")],
            "batchCleanup": "clean",
            "residualRisk": "none",
        }
        result = report["runs"][0]["scenarioResults"][0]
        result["judgeInvoked"] = False
        result["evidence"] = ["criticalFailureSkipsJudge"]

        with self.assertRaisesRegex(RuntimeError, "Unexpected model-Judge evidence"):
            runner._audit_report(batch, report)

    def test_final_governed_evidence_must_match_checkpoint(self) -> None:
        """Coordinator evidence cannot replace deterministic or Judge supervisor receipts."""
        batch = (self._run_spec("one", 1),)
        run_identity = "codex-batch-01-test"
        with tempfile.TemporaryDirectory() as temporary:
            checkpoint_root = Path(temporary)
            checkpoint = self._write_receipt_checkpoint(checkpoint_root, batch[0], run_identity)
            checkpoint_report = runner._load_checkpoint_report(checkpoint_root, batch, run_identity)
        assert checkpoint_report is not None
        report = {
            "runs": [self._suite_report("one", "PASS")],
            "batchCleanup": "clean",
            "residualRisk": "none",
        }
        report_receipts = json.loads(json.dumps(checkpoint["evidenceReceipts"]))
        report_receipts[0]["path"] = "one/happy/receipts/repeated-prose.json"
        report["runs"][0]["scenarioResults"][0]["evidenceReceipts"] = report_receipts

        with self.assertRaisesRegex(RuntimeError, "evidenceReceipts disagree with checkpoint"):
            runner._audit_report(batch, report, checkpoint_report)

    def test_checkpoint_retains_completed_scenario_without_final_report(self) -> None:
        """A terminal supervisor checkpoint survives a later coordinator interruption."""
        batch = (self._run_spec("one", 1),)
        run_identity = "codex-batch-01-test"
        with tempfile.TemporaryDirectory() as temporary:
            checkpoint_root = Path(temporary) / ".agent-suite-results"
            self._write_receipt_checkpoint(checkpoint_root, batch[0], run_identity)
            report = runner._load_checkpoint_report(checkpoint_root, batch, run_identity)
            assert report is not None
            self._bind_checkpoint_judges(checkpoint_root, report, batch)

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

    def test_final_report_may_summarize_checkpoint_evidence_without_rewriting_verdict(self) -> None:
        """The durable supervisor record stays primary while the coordinator may compress its evidence prose."""
        batch = (self._run_spec("one", 1),)
        final_report = {
            "runs": [self._suite_report("one", "PASS")],
            "batchCleanup": "clean",
            "residualRisk": "none",
        }
        checkpoint_report = json.loads(json.dumps(final_report))
        checkpoint_result = checkpoint_report["runs"][0]["scenarioResults"][0]
        checkpoint_result["identityEvidence"] = ["exact target receipt", "exact Judge receipt"]
        checkpoint_result["evidence"] = ["complete governed packet"]

        runner._audit_checkpoint_agreement(final_report, checkpoint_report, batch)

    def test_checkpoint_rejects_nested_evidence_objects(self) -> None:
        """Durable checkpoints use the same compact scalar contract as the coordinator report."""
        batch = (self._run_spec("one", 1),)
        with tempfile.TemporaryDirectory() as temporary:
            checkpoint = Path(temporary) / "one" / "happy.json"
            checkpoint.parent.mkdir()
            checkpoint.write_text(
                json.dumps(
                    {
                        "suite": "one",
                        "scenario": "happy",
                        "status": "PASS",
                        "targetInvoked": True,
                        "judgeInvoked": True,
                        "identityEvidence": {"target": "bound"},
                        "deterministicEvidence": ["gates"],
                        "modelJudgeEvidence": ["verdict"],
                        "evidence": ["receipt"],
                        "cleanup": "clean",
                        "residualRisk": "none",
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(RuntimeError, "array of strings"):
                runner._load_checkpoint_report(Path(temporary), batch, "codex-batch-01-test")

    def test_checkpoint_rejects_non_boolean_invocation_flags(self) -> None:
        """Truth-like strings cannot become invocation evidence after coordinator failure."""
        batch = (self._run_spec("one", 1),)
        with tempfile.TemporaryDirectory() as temporary:
            checkpoint = Path(temporary) / "one" / "happy.json"
            checkpoint.parent.mkdir()
            checkpoint.write_text(
                json.dumps(
                    {
                        "suite": "one",
                        "scenario": "happy",
                        "status": "PASS",
                        "targetInvoked": "false",
                        "judgeInvoked": True,
                        "identityEvidence": ["bound"],
                        "deterministicEvidence": ["gates"],
                        "modelJudgeEvidence": ["verdict"],
                        "evidence": ["receipt"],
                        "cleanup": "clean",
                        "residualRisk": "none",
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(RuntimeError, "must be booleans"):
                runner._load_checkpoint_report(Path(temporary), batch, "codex-batch-01-test")

    def test_task_selected_dependencies_extend_fixed_dependencies(self) -> None:
        """A scenario can stage bounded task roles without changing the canonical manifest."""
        suite = self._suite("dependency-selection")
        scenario = dict(suite.scenarios[0])
        scenario["taskSelectedAgentDependencies"] = [
            "dev-documentation-writer",
            "dev-artifact-reviewer",
        ]
        suite = runner._Suite(
            suite.suite_id,
            suite.priority,
            suite.path,
            suite.manifest,
            (scenario,),
        )

        observed = runner._agent_dependencies(
            runner._RunSpec(suite=suite, scenario_ids=("happy",))
        )

        self.assertEqual(
            (
                "dependency",
                "dev-artifact-reviewer",
                "dev-documentation-writer",
            ),
            observed,
        )

    def test_fixture_contract_reports_exact_missing_dotted_field(self) -> None:
        """Fixture omissions identify the suite, scenario, and exact dotted field."""
        with tempfile.TemporaryDirectory() as directory:
            suite = self._dependency_routing_suite(Path(directory))
            contract = Path(directory) / "fixture-contract.yaml"
            contract.write_text("schema: dependency-routing-fixture\n", encoding="utf-8")

            with self.assertRaisesRegex(
                ValueError,
                r"dependency-routing:dependency-routing missing fixture field lanes\.source\.owner",
            ):
                runner._validate_fixture_contract(suite, suite.scenarios[0])

    def test_report_reports_exact_missing_handoff_receipt_field(self) -> None:
        """Receipt omissions identify the scenario, lane, and exact required field."""
        suite = self._suite("dependency-routing")
        scenario = dict(suite.scenarios[0])
        scenario["requiredHandoffReceiptFields"] = [
            "lane",
            "role",
            "commit",
            "review",
            "verification",
            "claimRelease",
        ]
        scenario["requiredHandoffReceiptLanes"] = ["source"]
        suite = runner._Suite(
            suite.suite_id,
            suite.priority,
            suite.path,
            suite.manifest,
            (scenario,),
        )
        run = runner._RunSpec(suite=suite, scenario_ids=("happy",))
        report = {
            "runs": [self._suite_report("dependency-routing", "PASS")],
            "batchCleanup": "clean",
            "residualRisk": "",
        }
        report["runs"][0]["scenarioResults"][0]["status"] = "BLOCKED"
        report["runs"][0]["scenarioResults"][0]["handoffReceipts"] = [
            {
                "lane": "source",
                "role": "dev-coder",
                "commit": "abc123",
                "review": "accepted",
                "verification": "pass",
            }
        ]

        with self.assertRaisesRegex(
            RuntimeError,
            "dependency-routing:happy handoff receipt source missing field claimRelease",
        ):
            runner._audit_report((run,), report)

    def test_dependency_receipt_schema_requires_and_rejects_missing_lane(self) -> None:
        """Dependency receipts cannot satisfy the schema or report contract without a lane."""
        handoff_schema = runner._coordinator_schema()["properties"]["runs"]["items"][
            "properties"
        ]["scenarioResults"]["items"]["properties"]["handoffReceipts"]["items"]
        self.assertIn("lane", handoff_schema["required"])

        suite = self._suite("dependency-routing")
        scenario = dict(suite.scenarios[0])
        scenario["requiredHandoffReceiptFields"] = list(handoff_schema["required"])
        scenario["requiredHandoffReceiptLanes"] = ["source"]
        suite = runner._Suite(
            suite.suite_id,
            suite.priority,
            suite.path,
            suite.manifest,
            (scenario,),
        )
        run = runner._RunSpec(suite=suite, scenario_ids=("happy",))
        report = {
            "runs": [self._suite_report("dependency-routing", "BLOCKED")],
            "batchCleanup": "clean",
            "residualRisk": "",
        }
        report["runs"][0]["scenarioResults"][0]["handoffReceipts"] = [
            {
                "role": {"invocation": "dev-coder", "sessionIds": ["source-session"]},
                "commit": {"repository": "candidate", "sha": "abc123"},
                "review": {"sessionIds": ["review-session"]},
                "verification": {"sessionIds": ["verification-session"]},
                "claimRelease": {"eventIds": ["release-event"]},
            }
        ]

        with self.assertRaisesRegex(
            RuntimeError,
            "dependency-routing:happy missing handoff receipt lane source",
        ):
            runner._audit_report((run,), report)

    @staticmethod
    def _dependency_routing_suite(path: Path) -> object:
        """Build the smallest suite that exercises fixture-contract validation."""
        return runner._Suite(
            suite_id="dependency-routing",
            priority=1,
            path=path,
            manifest={"target": {"allowedAgentDependencies": ["dev-coder"]}},
            scenarios=(
                {
                    "id": "dependency-routing",
                    "fixtureContract": "fixture-contract.yaml",
                },
            ),
        )

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
            scenarios=(
                {
                    "id": "happy",
                    "status": "executable",
                    "executableCase": "fixture",
                    "deterministicChecks": [
                        "harness-agent-identity",
                        "test-state-transition",
                    ],
                },
            ),
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

    @classmethod
    def _browser_run_spec(cls, suite_id: str) -> object:
        suite = cls._suite(suite_id)
        suite = runner._Suite(
            suite_id=suite.suite_id,
            priority=suite.priority,
            path=suite.path,
            manifest=suite.manifest,
            scenarios=(
                {
                    "id": "happy",
                    "status": "executable",
                    "executableCase": "fixture",
                    "runtimeCapabilities": ["browser-automation"],
                },
            ),
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
                    "deterministicEvidence": ["deterministic-gates"],
                    "modelJudgeEvidence": ["judge-verdict"],
                    "evidenceReceipts": [],
                    "cleanup": "clean",
                    "evidence": ["synthetic"],
                }
            ],
            "maximumActiveChildrenObserved": 1,
            "cleanup": "clean",
        }

    @classmethod
    def _write_receipt_checkpoint(
        cls,
        checkpoint_root: Path,
        run: object,
        run_identity: str,
        *,
        status: str = "PASS",
        judge_invoked: bool = True,
    ) -> dict[str, object]:
        suite_id = run.suite.suite_id
        scenario_id = run.scenario_ids[0]
        scenario_root = checkpoint_root / suite_id / scenario_id
        artifacts = scenario_root / "artifacts"
        receipts = scenario_root / "receipts"
        artifacts.mkdir(parents=True)
        receipts.mkdir()
        references: list[dict[str, str]] = []
        selected_scenario = next(
            scenario for scenario in run.suite.scenarios if scenario["id"] == scenario_id
        )
        catalog = runner._deterministic_check_catalog()
        criticality = {
            check_id: catalog[check_id]
            for check_id in selected_scenario["deterministicChecks"]
        }
        failed_check = "harness-agent-identity" if status == "FAIL" and not judge_invoked else None
        for check_id, critical in criticality.items():
            artifact = artifacts / f"{check_id}.log"
            artifact.write_text(f"{check_id} retained evidence\n", encoding="utf-8")
            receipt = receipts / f"deterministic-{check_id}.json"
            receipt.write_text(
                json.dumps(
                    {
                        "schema": "dev-methodology-agent-suite-evidence-receipt",
                        "version": 1,
                        "eventType": "deterministic-check-disposition",
                        "runIdentity": run_identity,
                        "suite": suite_id,
                        "scenario": scenario_id,
                        "checkId": check_id,
                        "critical": critical,
                        "verdict": "failed" if check_id == failed_check else "passed",
                        "evidence": {
                            "path": artifact.relative_to(checkpoint_root).as_posix(),
                            "sha256": runner._sha256(artifact),
                        },
                    },
                    indent=2,
                    sort_keys=True,
                )
                + "\n",
                encoding="utf-8",
            )
            references.append(
                {
                    "path": receipt.relative_to(checkpoint_root).as_posix(),
                    "sha256": runner._sha256(receipt),
                }
            )
        judge_invocation = str(run.suite.manifest["execution"]["judgeInvocation"])
        if judge_invoked:
            judge_output = artifacts / "judge-output.json"
            judge_output.write_text(
                json.dumps(
                    {
                        "schema": "dev-methodology-agent-suite-judge-output",
                        "version": 1,
                        "runIdentity": run_identity,
                        "suite": suite_id,
                        "scenario": scenario_id,
                        "judgeInvocation": judge_invocation,
                        "disposition": {"PASS": "passed", "FAIL": "failed"}.get(status, status.lower()),
                    },
                    indent=2,
                    sort_keys=True,
                )
                + "\n",
                encoding="utf-8",
            )
            receipt = receipts / "judge-disposition.json"
            receipt.write_text(
                json.dumps(
                    {
                        "schema": "dev-methodology-agent-suite-evidence-receipt",
                        "version": 1,
                        "eventType": "judge-disposition",
                        "runIdentity": run_identity,
                        "suite": suite_id,
                        "scenario": scenario_id,
                        "judgeInvocation": judge_invocation,
                        "disposition": {"PASS": "passed", "FAIL": "failed"}.get(status, status.lower()),
                        "evidence": {
                            "path": judge_output.relative_to(checkpoint_root).as_posix(),
                            "sha256": runner._sha256(judge_output),
                        },
                    },
                    indent=2,
                    sort_keys=True,
                )
                + "\n",
                encoding="utf-8",
            )
            references.append(
                {
                    "path": receipt.relative_to(checkpoint_root).as_posix(),
                    "sha256": runner._sha256(receipt),
                }
            )
        else:
            evidence = artifacts / f"{failed_check}.log"
            receipt = receipts / "judge-skip-disposition.json"
            receipt.write_text(
                json.dumps(
                    {
                        "schema": "dev-methodology-agent-suite-evidence-receipt",
                        "version": 1,
                        "eventType": "judge-skip-disposition",
                        "runIdentity": run_identity,
                        "suite": suite_id,
                        "scenario": scenario_id,
                        "checkId": failed_check,
                        "critical": True,
                        "deterministicVerdict": "failed",
                        "disposition": "skipped-critical-failure",
                        "evidence": {
                            "path": evidence.relative_to(checkpoint_root).as_posix(),
                            "sha256": runner._sha256(evidence),
                        },
                    },
                    indent=2,
                    sort_keys=True,
                )
                + "\n",
                encoding="utf-8",
            )
            references.append(
                {
                    "path": receipt.relative_to(checkpoint_root).as_posix(),
                    "sha256": runner._sha256(receipt),
                }
            )
        checkpoint = checkpoint_root / suite_id / f"{scenario_id}.json"
        document: dict[str, object] = {
            "suite": suite_id,
            "scenario": scenario_id,
            "status": status,
            "targetInvoked": True,
            "judgeInvoked": judge_invoked,
            "identityEvidence": ["runtime identity diagnostics"],
            "deterministicEvidence": ["diagnostic summary only"],
            "modelJudgeEvidence": ["diagnostic summary only"] if judge_invoked else [],
            "evidenceReceipts": references,
            "evidence": ["diagnostic summary only"],
            "cleanup": "clean",
            "residualRisk": "none",
        }
        checkpoint.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return document

    @staticmethod
    def _workspace_mutation_evidence(*, final_matches: bool) -> dict[str, object]:
        git = {
            "head": "a" * 40,
            "symbolicHead": "refs/heads/main",
            "indexSha256": "b" * 64,
            "refsSha256": "c" * 64,
        }
        baseline = {
            "schema": "dev-methodology-workspace-inventory",
            "version": 1,
            "root": "/synthetic/candidate",
            "git": git,
            "entries": [
                {
                    "path": "existing.pyc",
                    "kind": "file",
                    "mode": "0644",
                    "sha256": "4" * 64,
                    "gitState": "ignored",
                },
                {
                    "path": "notes.txt",
                    "kind": "file",
                    "mode": "0644",
                    "sha256": "5" * 64,
                    "gitState": "untracked",
                },
            ],
        }
        created = [
            {
                "path": "__pycache__/migration.cpython-311.pyc",
                "kind": "file",
                "mode": "0644",
                "sha256": "1" * 64,
                "gitState": "ignored",
            }
        ]
        observed = json.loads(json.dumps(baseline))
        observed["entries"] = [*observed["entries"], *created]
        final = json.loads(json.dumps(baseline if final_matches else observed))
        detected = runner.workspace_inventory_support._changes(baseline, observed)
        remaining = runner.workspace_inventory_support._changes(baseline, final)
        final = {
            **final,
        }
        return {
            "schema": "dev-methodology-workspace-mutation-evidence",
            "version": 1,
            "root": "/synthetic/candidate",
            "baselineFileSha256": hashlib.sha256(
                (json.dumps(baseline, indent=2, sort_keys=True) + "\n").encode("utf-8")
            ).hexdigest(),
            "baseline": baseline,
            "baselineSha256": hashlib.sha256(
                json.dumps(baseline, sort_keys=True, separators=(",", ":")).encode("utf-8")
            ).hexdigest(),
            "observed": observed,
            "observedSha256": hashlib.sha256(
                json.dumps(observed, sort_keys=True, separators=(",", ":")).encode("utf-8")
            ).hexdigest(),
            "detected": detected,
            "derivedMutationClaim": "side-effects-detected",
            "preExisting": {"ignored": ["existing.pyc"], "untracked": ["notes.txt"]},
            "cleanup": {
                "requested": True,
                "removed": ["__pycache__/migration.cpython-311.pyc"] if final_matches else [],
                "preserved": [] if final_matches else ["__pycache__/migration.cpython-311.pyc"],
            },
            "final": final,
            "finalSha256": hashlib.sha256(
                json.dumps(final, sort_keys=True, separators=(",", ":")).encode("utf-8")
            ).hexdigest(),
            "remaining": remaining,
            "finalMatchesBaseline": final_matches,
        }

    @staticmethod
    def _replace_deterministic_artifact(
        checkpoint_root: Path,
        checkpoint: dict[str, object],
        check_id: str,
        evidence: object,
    ) -> None:
        references = checkpoint["evidenceReceipts"]
        assert isinstance(references, list)
        for reference in references:
            receipt_path = checkpoint_root / str(reference["path"])
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            if receipt.get("eventType") != "deterministic-check-disposition" or receipt.get("checkId") != check_id:
                continue
            artifact_path = checkpoint_root / receipt["evidence"]["path"]
            artifact_path.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            receipt["evidence"]["sha256"] = runner._sha256(artifact_path)
            receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            reference["sha256"] = runner._sha256(receipt_path)
            return
        raise AssertionError(f"Missing deterministic receipt {check_id}")

    @staticmethod
    def _rewrite_receipt(
        checkpoint_root: Path,
        checkpoint: dict[str, object],
        event_type: str,
        mutate: object,
    ) -> None:
        references = checkpoint["evidenceReceipts"]
        assert isinstance(references, list)
        for reference in references:
            assert isinstance(reference, dict)
            path = checkpoint_root / str(reference["path"])
            loaded = json.loads(path.read_text(encoding="utf-8"))
            if loaded.get("eventType") != event_type:
                continue
            mutate(loaded)
            path.write_text(json.dumps(loaded, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            reference["sha256"] = runner._sha256(path)
            return
        raise AssertionError(f"Missing receipt {event_type}")

    @staticmethod
    def _write_junie_lifecycles(
        junie_home: Path,
        lifecycles: tuple[tuple[str, int, int], ...],
    ) -> None:
        session = junie_home / "sessions" / "session"
        session.mkdir(parents=True, exist_ok=True)
        events: list[dict[str, object]] = []
        for index, (name, started, finished) in enumerate(lifecycles):
            step_id = f"step-{index:08d}"
            for status, second in (("STARTED", started), ("FINISHED", finished)):
                events.append(
                    {
                        "timestamp": f"2026-07-19T00:00:{second:02d}Z",
                        "event": {
                            "agentEvent": {
                                "kind": "CustomAgentBlockUpdatedEvent",
                                "agent": {"id": f"custom-{name}", "name": name},
                                "name": name,
                                "status": status,
                                "stepId": step_id,
                                "menuItems": [],
                                "details": None,
                                "model": "opus",
                            }
                        },
                    }
                )
        events.sort(key=lambda event: str(event["timestamp"]))
        (session / "events.jsonl").write_text(
            "\n".join(json.dumps(event) for event in events) + "\n",
            encoding="utf-8",
        )

    @staticmethod
    def _staged_junie_agents() -> tuple[object, ...]:
        return tuple(
            runner._StagedAgent(
                name,
                Path(f"{name}.md"),
                "instructions",
                character * 64,
                f"AGENT-INSTRUCTION-BINDING-{name}-{character * 32}",
            )
            for name, character in (
                ("suite-supervisor", "a"),
                ("target-agent", "b"),
                ("suite-judge", "c"),
                ("dependency", "d"),
            )
        )

    @staticmethod
    def _write_rollout(
        path: Path,
        invocation: str,
        depth: int,
        marker: str | None = None,
        arbitrary_message: bool = False,
        parent: str | None = None,
        started_second: int = 0,
        final_response: bytes | None = None,
    ) -> None:
        session_id = path.stem
        parent = parent or ("root" if depth == 1 else "rollout-supervisor")

        def timestamp(offset: int) -> str:
            return f"2026-07-17T00:00:{started_second + offset:02d}Z"

        events: tuple[dict[str, object], ...] = (
            {"timestamp": timestamp(0), "type": "session_meta", "payload": {
                "id": session_id,
                "parent_thread_id": parent,
                "agent_path": f"/root/{invocation}",
                "agent_role": invocation,
                "source": {"subagent": {"thread_spawn": {
                    "depth": depth,
                    "agent_path": f"/root/{invocation}",
                    "agent_role": invocation,
                }}},
            }},
        )
        if marker and not arbitrary_message:
            events += (
                {"timestamp": timestamp(1), "type": "response_item", "payload": {
                    "type": "message",
                    "role": "developer",
                    "content": [{"type": "input_text", "text": f"Runtime instruction binding marker: {marker}."}],
                }},
            )
        else:
            events += (
                {"timestamp": timestamp(1), "type": "event_msg", "payload": {
                    "type": "agent_message", "message": marker or "no binding evidence"
                }},
            )
        if final_response is not None:
            events += (
                {"timestamp": timestamp(2), "type": "response_item", "payload": {
                    "type": "message",
                    "role": "assistant",
                    "content": [{"type": "output_text", "text": final_response.decode("utf-8")}],
                    "phase": "final_answer",
                }},
            )
        path.write_text("\n".join(json.dumps(event) for event in events) + "\n", encoding="utf-8")

    @staticmethod
    def _write_noop_rollout(path: Path) -> None:
        events = (
            {"timestamp": "2026-07-17T00:00:00Z", "type": "session_meta", "payload": {
                "id": path.stem,
                "parent_thread_id": "root",
                "agent_role": "default",
                "source": {"subagent": {"thread_spawn": {
                    "depth": 1, "agent_path": None, "agent_role": "default",
                }}},
            }},
            {"timestamp": "2026-07-17T00:00:00.001Z", "type": "event_msg", "payload": {
                "type": "task_started", "turn_id": "turn-noop",
            }},
            {"timestamp": "2026-07-17T00:00:00.500Z", "type": "response_item", "payload": {
                "type": "message", "role": "developer",
                "content": [{"type": "input_text", "text": "global runtime context"}],
            }},
            {"timestamp": "2026-07-17T00:00:00.600Z", "type": "response_item", "payload": {
                "type": "message", "role": "user",
                "content": [
                    {"type": "input_text", "text": "<recommended_plugins>runtime catalog</recommended_plugins>"},
                    {"type": "input_text", "text": "# AGENTS.md instructions for /workspace\ncontract"},
                    {"type": "input_text", "text": "<environment_context>workspace</environment_context>"},
                ],
                "internal_chat_message_metadata_passthrough": {"turn_id": "turn-noop"},
            }},
            {"timestamp": "2026-07-17T00:00:00.700Z", "type": "world_state", "payload": {
                "full": True, "state": {},
            }},
            {"timestamp": "2026-07-17T00:00:00.800Z", "type": "turn_context", "payload": {
                "turn_id": "turn-noop",
            }},
            {"timestamp": "2026-07-17T00:00:01Z", "type": "response_item", "payload": {
                "type": "message", "role": "user",
                "content": [{"type": "input_text", "text": "noop"}],
                "internal_chat_message_metadata_passthrough": {"turn_id": "turn-noop"},
            }},
            {"timestamp": "2026-07-17T00:00:01.001Z", "type": "event_msg", "payload": {
                "type": "user_message", "message": "noop",
            }},
            {"timestamp": "2026-07-17T00:00:01.500Z", "type": "event_msg", "payload": {
                "type": "token_count", "info": None,
            }},
            {"timestamp": "2026-07-17T00:00:01.900Z", "type": "response_item", "payload": {
                "type": "message", "role": "user",
                "content": [{"type": "input_text", "text": "<turn_aborted>interrupted</turn_aborted>"}],
                "internal_chat_message_metadata_passthrough": {"turn_id": "turn-noop"},
            }},
            {"timestamp": "2026-07-17T00:00:02Z", "type": "event_msg", "payload": {
                "type": "turn_aborted", "reason": "interrupted",
            }},
        )
        path.write_text("\n".join(json.dumps(event) for event in events) + "\n", encoding="utf-8")

    def _bind_checkpoint_judges(
        self,
        checkpoint_root: Path,
        checkpoint_report: dict[str, object],
        batch: tuple[object, ...],
    ) -> None:
        retained_sessions = checkpoint_root / ".sessions"
        retained_sessions.mkdir(parents=True, exist_ok=True)
        bindings: list[dict[str, str]] = []
        for index, raw_run in enumerate(batch):
            run = raw_run
            suite_id = run.suite.suite_id
            scenario_id = run.scenario_ids[0]
            scenario_result = checkpoint_report["runs"][index]["scenarioResults"][0]
            if not scenario_result["judgeInvoked"]:
                continue
            output_reference = scenario_result["receiptAudit"]["judgeOutput"]
            output_path = checkpoint_root / output_reference["path"]
            session_id = f"rollout-judge-{suite_id}"
            invocation = str(run.suite.manifest["execution"]["judgeInvocation"])
            self._write_rollout(
                retained_sessions / f"{session_id}.jsonl",
                invocation,
                depth=2,
                parent=f"rollout-supervisor-{suite_id}",
                final_response=output_path.read_bytes(),
            )
            bindings.append(
                {
                    "suite": suite_id,
                    "scenario": scenario_id,
                    "kind": "judge",
                    "invocation": invocation,
                    "sessionId": session_id,
                    "parentSessionId": f"rollout-supervisor-{suite_id}",
                }
            )
        runner._bind_codex_judge_provenance(
            checkpoint_report,
            {"scenarioBindings": bindings},
            batch,
            checkpoint_root,
            retained_sessions,
            checkpoint_root,
        )


if __name__ == "__main__":
    unittest.main()
