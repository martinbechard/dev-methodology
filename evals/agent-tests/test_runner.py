# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Verifies bounded scheduling, validation, timing, evidence retention, and cleanup for the agent-suite runner.
# Governing design: evals/agent-tests/implementation-plan.md

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
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
        )

        self.assertIn("agent_type exactly equal", prompt)
        self.assertIn("fork_context exactly false", prompt)
        self.assertIn('"fixtureRoot": "/workspace/.agent-suite-fixtures/one"', prompt)
        self.assertIn("never under /tmp or /private/tmp", prompt)

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
        """A manifest-authorized critical gate failure remains a governed FAIL without semantic judging."""
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
        report = {
            "runs": [self._suite_report("one", "FAIL")],
            "batchCleanup": "clean",
            "residualRisk": "none",
        }
        result = report["runs"][0]["scenarioResults"][0]
        result["judgeInvoked"] = False
        result["evidence"] = [
            "A critical deterministic gate failed.",
            "criticalFailureSkipsJudge applied, so no semantic Judge scoring was performed.",
        ]

        runner._audit_report(batch, report)

    def test_checkpoint_may_prove_critical_skip_when_final_evidence_is_summarized(self) -> None:
        """Coordinator compression cannot erase a supervisor checkpoint's authorized Judge skip."""
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
        result["evidence"] = ["The deterministic gate failed before semantic scoring."]
        checkpoint_report = json.loads(json.dumps(report))
        checkpoint_report["runs"][0]["scenarioResults"][0]["evidence"] = [
            "criticalFailureSkipsJudge applied after the proved critical deterministic failure."
        ]

        runner._audit_report(batch, report, checkpoint_report)

    def test_unproved_critical_failure_skip_does_not_bypass_judge_requirement(self) -> None:
        """A missing Judge is rejected unless both manifest authority and explicit skip evidence are present."""
        batch = (self._run_spec("one", 1),)
        report = {
            "runs": [self._suite_report("one", "FAIL")],
            "batchCleanup": "clean",
            "residualRisk": "none",
        }
        report["runs"][0]["scenarioResults"][0]["judgeInvoked"] = False

        with self.assertRaisesRegex(RuntimeError, "Terminal verdict lacks target and Judge"):
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
                        "evidence": ["receipt"],
                        "cleanup": "clean",
                        "residualRisk": "none",
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(RuntimeError, "array of strings"):
                runner._load_checkpoint_report(Path(temporary), batch)

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
                        "evidence": ["receipt"],
                        "cleanup": "clean",
                        "residualRisk": "none",
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(RuntimeError, "must be booleans"):
                runner._load_checkpoint_report(Path(temporary), batch)

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
        path.write_text("\n".join(json.dumps(event) for event in events) + "\n", encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
