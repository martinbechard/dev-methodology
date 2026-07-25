#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies deterministic claim transport, deadline-policy rendering, invocation behavior, and evaluation staging.

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
RENDER_SCRIPT = ROOT / "scripts" / "render-agents-technology-skills.py"
SHARED_SKILL = ROOT / "skills" / "agent-claim" / "SKILL.md"
MCP_SKILL = ROOT / "skills" / "agent-claim-mcp" / "SKILL.md"
COMMAND_SKILL = ROOT / "skills" / "agent-claim-command" / "SKILL.md"
COMMAND_SCRIPT = ROOT / "skills" / "agent-claim-command" / "scripts" / "claim.py"
LEGACY_COMMAND_SCRIPT = ROOT / "skills" / "agent-claim" / "scripts" / "claim.py"
CASES_PATH = ROOT / "evals" / "cases.yaml"
PROJECT_CONFIGURATION_FIXTURE = ROOT / "evals" / "projects" / "project-configuration-routing"
LIVE_MCP_CLAIM_TOOLS = frozenset({
    "claim_status",
    "claim_acquire",
    "claim_extend",
    "claim_heartbeat",
    "claim_release",
    "claim_maintain_journal",
    "claim_report",
})
REQUIRED_FUTURE_MCP_CLAIM_TOOLS = LIVE_MCP_CLAIM_TOOLS | {"claim_extend_deadline"}
MCP_DEADLINE_PARITY = "UNRESOLVED_EXTERNAL_PROVIDER"
CANONICAL_ACQUIRE_OUTCOMES = frozenset({
    "SHARED_CHECKOUT_ACQUIRED",
    "ISOLATED_CHECKOUT_ACQUIRED",
    "DIRTY_CHECKOUT_RECOVERY_ACQUIRED",
    "CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED",
    "SHARED_CHECKOUT_REQUIRED",
    "SHARED_CHECKOUT_RELEASE_REQUIRED",
    "ISOLATED_CHECKOUT_SETUP_REQUIRED",
    "DIRTY_CHECKOUT_RECOVERY_AUTHORIZATION_REQUIRED",
    "INVALID_SCOPE",
})


class _AmbiguousDispatch(RuntimeError):
    """Represent a mutating MCP dispatch whose completion was not observed."""


class _SimulatedMcpTransport:
    """Provide deterministic schema-v2 results for the MCP claim boundary."""

    def __init__(
        self,
        *,
        available: bool = True,
        tools: frozenset[str] = REQUIRED_FUTURE_MCP_CLAIM_TOOLS,
        result_schema_version: int = 2,
        acquire_result: dict[str, object] | None = None,
        ambiguous_acquire: bool = False,
    ) -> None:
        self.available = available
        self.tools = tools
        self.result_schema_version = result_schema_version
        self.acquire_result = acquire_result or {
            "exit_code": 0,
            "result": {
                "schema_version": 2,
                "outcome": "SHARED_CHECKOUT_ACQUIRED",
                "legacy_outcome": "PRIMARY",
            },
        }
        self.ambiguous_acquire = ambiguous_acquire
        self.calls: list[str] = []
        self.claim_calls: list[tuple[str, str, tuple[str, ...]]] = []
        self.deadline_calls: list[dict[str, object]] = []
        self.active_claim_id: str | None = None

    def verify_setup(self) -> None:
        """Reject unavailable, incomplete, or noncanonical MCP claim surfaces."""

        if not self.available:
            raise RuntimeError("CLAIM_TRANSPORT_UNAVAILABLE")
        if self.tools != REQUIRED_FUTURE_MCP_CLAIM_TOOLS:
            raise RuntimeError("CLAIM_TRANSPORT_INCOMPLETE")
        if self.result_schema_version != 2:
            raise RuntimeError("CLAIM_TRANSPORT_SCHEMA_UNSUPPORTED")

    def call(
        self,
        tool: str,
        *,
        claim_id: str | None = None,
        resources: tuple[str, ...] = (),
        resource_class: str | None = None,
        resource_id: str | None = None,
        expected_duration_seconds: int | None = None,
        requested_hard_stop_duration_seconds: int | None = None,
        extension_evidence: str | None = None,
    ) -> dict[str, object]:
        """Record one simulated MCP call and return its configured structured result."""

        if tool not in self.tools:
            raise AssertionError(f"unexpected MCP tool: {tool}")
        self.calls.append(tool)
        if tool in {"claim_acquire", "claim_extend_deadline", "claim_release"}:
            if not claim_id:
                raise AssertionError(f"{tool} requires claim_id")
            if tool == "claim_acquire" and not resources:
                raise AssertionError("claim_acquire requires named resources")
            if tool == "claim_acquire" and (
                len(resources) != 1
                or resource_class is None
                or resource_id != resources[0]
                or expected_duration_seconds is None
                or requested_hard_stop_duration_seconds is None
            ):
                raise AssertionError("claim_acquire requires one complete timed resource request")
            if tool == "claim_extend_deadline" and (
                claim_id != self.active_claim_id
                or requested_hard_stop_duration_seconds is None
                or not extension_evidence
            ):
                raise AssertionError("claim_extend_deadline requires active ownership and extension evidence")
            if tool == "claim_release" and claim_id != self.active_claim_id:
                raise AssertionError("claim_release must use the acquired claim_id")
            self.claim_calls.append((tool, claim_id, resources))
            if tool in {"claim_acquire", "claim_extend_deadline"}:
                self.deadline_calls.append({
                    "tool": tool,
                    "claim_id": claim_id,
                    "resource_class": resource_class,
                    "resource_id": resource_id,
                    "expected_duration_seconds": expected_duration_seconds,
                    "requested_hard_stop_duration_seconds": requested_hard_stop_duration_seconds,
                    "extension_evidence": extension_evidence,
                })
            if tool == "claim_acquire":
                self.active_claim_id = claim_id
        if tool == "claim_acquire" and self.ambiguous_acquire:
            raise _AmbiguousDispatch("response lost after dispatch")
        if tool == "claim_status":
            return {
                "exit_code": 0,
                "result": {"schema_version": 2, "outcome": "STATUS"},
            }
        if tool == "claim_release":
            self.active_claim_id = None
            return {
                "exit_code": 0,
                "result": {"schema_version": 2, "outcome": "CLAIM_RELEASED"},
            }
        if tool == "claim_extend_deadline":
            return {
                "exit_code": 0,
                "result": {"schema_version": 2, "outcome": "DEADLINE_EXTENDED"},
            }
        return self.acquire_result


def _canonical_mcp_result(response: dict[str, object]) -> dict[str, object]:
    """Validate one simulated MCP result envelope and return its nested result."""

    if set(response) != {"exit_code", "result"}:
        raise RuntimeError("CLAIM_TRANSPORT_RESULT_INVALID")
    result = response.get("result")
    if not isinstance(result, dict) or result.get("schema_version") != 2:
        raise RuntimeError("CLAIM_TRANSPORT_SCHEMA_UNSUPPORTED")
    return result


def _run_mcp_acquire(transport: _SimulatedMcpTransport) -> dict[str, object]:
    """Execute acquisition or reconcile an ambiguous dispatch through the same MCP surface."""

    transport.verify_setup()
    try:
        response = transport.call(
            "claim_acquire",
            claim_id="mcp-acquire-test",
            resources=("database:test",),
            resource_class="database-port",
            resource_id="database:test",
            expected_duration_seconds=300,
            requested_hard_stop_duration_seconds=900,
        )
    except _AmbiguousDispatch:
        response = transport.call("claim_status")
    result = _canonical_mcp_result(response)
    outcome = result.get("outcome")
    if outcome != "STATUS" and outcome not in CANONICAL_ACQUIRE_OUTCOMES:
        raise RuntimeError("CLAIM_TRANSPORT_OUTCOME_UNSUPPORTED")
    return result


def _run_none_resource_lifecycle(project: dict[str, object]) -> dict[str, object]:
    """Validate one renderer-valid none selection without invoking a transport."""

    load_renderer_module().render(project)
    coordination = project.get("resource_coordination")
    if not isinstance(coordination, dict) or coordination.get("selected") != "none":
        raise ValueError("resource_coordination.selected must be none")
    return {"resource_coordination": "none"}


def _run_selected_mcp_lifecycle(
    project: dict[str, object],
    transport: _SimulatedMcpTransport,
    claim_id: str,
    resources: tuple[str, ...],
) -> dict[str, object]:
    """Exercise an MCP-selected acquire and release through its simulated tool boundary."""

    load_renderer_module().render(project)
    coordination = project.get("resource_coordination")
    if not isinstance(coordination, dict):
        raise ValueError("resource_coordination is required")
    selected = coordination.get("selected")
    if selected != "agent-claim":
        raise ValueError("resource_coordination.selected must be agent-claim")

    transport_configuration = project.get("agent_claim_transport")
    if not isinstance(transport_configuration, dict):
        raise ValueError("agent_claim_transport is required")
    configured_transport = transport_configuration.get("selected")
    if configured_transport != "mcp":
        raise RuntimeError("CLAIM_TRANSPORT_BINDING_MISMATCH")

    transport.verify_setup()
    if len(resources) != 1:
        raise ValueError("MCP lifecycle requires exactly one named resource")
    acquired = _canonical_mcp_result(transport.call(
        "claim_acquire",
        claim_id=claim_id,
        resources=resources,
        resource_class="database-port",
        resource_id=resources[0],
        expected_duration_seconds=300,
        requested_hard_stop_duration_seconds=900,
    ))
    extended = _canonical_mcp_result(transport.call(
        "claim_extend_deadline",
        claim_id=claim_id,
        requested_hard_stop_duration_seconds=1200,
        extension_evidence="future MCP deadline parity contract",
    ))
    released = _canonical_mcp_result(
        transport.call("claim_release", claim_id=claim_id)
    )
    return {
        "resource_coordination": "agent-claim",
        "transport": "mcp",
        "claim_id": claim_id,
        "resources": list(resources),
        "acquire_outcome": acquired["outcome"],
        "extend_deadline_outcome": extended["outcome"],
        "release_outcome": released["outcome"],
    }


def _command_result(
    completed: subprocess.CompletedProcess[str],
) -> dict[str, object]:
    """Decode one successful command-adapter JSON result."""

    if completed.returncode != 0:
        raise RuntimeError(
            f"command claim invocation failed with {completed.returncode}: {completed.stderr}"
        )
    result = json.loads(completed.stdout)
    if not isinstance(result, dict) or result.get("schema_version") != 2:
        raise RuntimeError("CLAIM_TRANSPORT_SCHEMA_UNSUPPORTED")
    return result


def _run_command_resource_lifecycle(
    project: dict[str, object],
    repository: Path,
    claim_id: str,
    resources: tuple[str, ...],
) -> dict[str, object]:
    """Exercise a command-selected acquire and release through actual process argv."""

    load_renderer_module().render(project)
    transport_configuration = project.get("agent_claim_transport")
    if not isinstance(transport_configuration, dict):
        raise ValueError("agent_claim_transport is required")
    if transport_configuration.get("selected") != "command":
        raise RuntimeError("CLAIM_TRANSPORT_BINDING_MISMATCH")
    if len(resources) != 1:
        raise ValueError("command lifecycle requires exactly one named resource")

    acquire_argv = [
        sys.executable,
        str(COMMAND_SCRIPT),
        "--repo",
        str(repository),
        "acquire",
        "--claim-id",
        claim_id,
        "--agent",
        "claim-transport-test",
        "--task",
        "command resource lifecycle",
        "--root-task-id",
        claim_id,
    ]
    for resource in resources:
        acquire_argv.extend(("--resource", resource))
    acquire_argv.extend((
        "--resource-class",
        "database-port",
        "--resource-id",
        resources[0],
        "--expected-duration-seconds",
        "300",
        "--requested-hard-stop-duration-seconds",
        "900",
    ))
    release_argv = [
        sys.executable,
        str(COMMAND_SCRIPT),
        "--repo",
        str(repository),
        "release",
        "--claim-id",
        claim_id,
        "--no-change",
    ]
    acquire_process = subprocess.run(
        acquire_argv,
        check=False,
        text=True,
        capture_output=True,
    )
    acquire_result = _command_result(acquire_process)
    release_process = subprocess.run(
        release_argv,
        check=False,
        text=True,
        capture_output=True,
    )
    release_result = _command_result(release_process)
    return {
        "resource_coordination": "agent-claim",
        "transport": "command",
        "claim_id": claim_id,
        "resources": list(resources),
        "acquire_argv": acquire_argv,
        "release_argv": release_argv,
        "acquire_returncode": acquire_process.returncode,
        "release_returncode": release_process.returncode,
        "acquire_outcome": acquire_result["outcome"],
        "release_outcome": release_result["outcome"],
    }


def load_renderer_module():
    """Load the PROJECT.yaml renderer so tests exercise its configuration boundary."""

    specification = importlib.util.spec_from_file_location(
        "render_agents_claim_transport",
        RENDER_SCRIPT,
    )
    if specification is None or specification.loader is None:
        raise RuntimeError(f"Unable to load {RENDER_SCRIPT}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def project_with_transport(selected: str, availability: str = "AVAILABLE") -> dict[str, object]:
    """Return the smallest renderable project fixture with one verified claim transport."""

    return {
        "resource_coordination": {
            "selected": "agent-claim",
            "deadline_policy": {
                "resource_classes": {
                    "backlog-mutation": {
                        "maximum_duration_seconds": 600,
                        "cleanup_grace_seconds": 120,
                    },
                    "main-integration": {
                        "maximum_duration_seconds": 2700,
                        "cleanup_grace_seconds": 600,
                    },
                    "browser-server": {
                        "maximum_duration_seconds": 3600,
                        "cleanup_grace_seconds": 600,
                    },
                    "database-port": {
                        "maximum_duration_seconds": 1800,
                        "cleanup_grace_seconds": 300,
                    },
                    "live-model-evaluation": {
                        "maximum_duration_seconds": 14400,
                        "cleanup_grace_seconds": 1800,
                    },
                },
                "resource_overrides": {},
            },
        },
        "agent_claim_transport": {
            "selected": selected,
            "availability": availability,
            "verification": [f"{selected} transport fixture evidence"],
        },
        "workflow_selection": {
            "provider": {"default": "UNSET"},
            "completion": {"default": "UNSET"},
        },
        "technology_skill_loadouts": [],
    }


class AgentClaimTransportTests(unittest.TestCase):
    """Protect standalone claim-adapter composition and failure behavior."""

    def test_renderer_inlines_only_selected_transport_adapter(self) -> None:
        """Compose shared role semantics with exactly one setup-selected adapter."""

        renderer = load_renderer_module()
        for selected, included, excluded in (
            ("mcp", "agent-claim-mcp", "agent-claim-command"),
            ("command", "agent-claim-command", "agent-claim-mcp"),
        ):
            with self.subTest(selected=selected):
                rendered = renderer.render(project_with_transport(selected))

                self.assertIn("## Resource Coordination Skill Reference", rendered)
                self.assertIn("selected resource-coordination skill agent-claim", rendered)
                self.assertIn("## Agent Claim Transport", rendered)
                self.assertIn(
                    f"BEGIN INLINED CLAIM TRANSPORT SKILL: {included}",
                    rendered,
                )
                self.assertNotIn(excluded, rendered)
                self.assertIn("does not probe or switch to another transport", rendered)

    def test_renderer_validates_and_renders_deadline_classes_and_exact_id_overrides(self) -> None:
        """Expose every configured deadline value without hidden class inference."""

        renderer = load_renderer_module()
        project = project_with_transport("command")
        policy = project["resource_coordination"]["deadline_policy"]
        policy["resource_overrides"] = {
            "browser-profile:release": {
                "resource_class": "browser-server",
                "maximum_duration_seconds": 2400,
                "cleanup_grace_seconds": 420,
            }
        }

        rendered = renderer.render(project)

        for resource_class, maximum, cleanup in (
            ("backlog-mutation", 600, 120),
            ("main-integration", 2700, 600),
            ("browser-server", 3600, 600),
            ("database-port", 1800, 300),
            ("live-model-evaluation", 14400, 1800),
        ):
            with self.subTest(resource_class=resource_class):
                self.assertIn(
                    f"{resource_class}: maximum {maximum} seconds; cleanup grace {cleanup} seconds",
                    rendered,
                )
        self.assertIn(
            "browser-profile:release: class browser-server; maximum 2400 seconds; cleanup grace 420 seconds",
            rendered,
        )

    def test_renderer_rejects_incomplete_or_invalid_deadline_policy(self) -> None:
        """Reject missing classes, invalid seconds, and unknown override classes."""

        renderer = load_renderer_module()
        cases = []
        missing_class = project_with_transport("command")
        missing_class["resource_coordination"]["deadline_policy"]["resource_classes"].pop(
            "database-port"
        )
        cases.append((missing_class, "resource_classes keys must be exactly"))
        invalid_seconds = project_with_transport("command")
        invalid_seconds["resource_coordination"]["deadline_policy"]["resource_classes"][
            "database-port"
        ]["maximum_duration_seconds"] = 0
        cases.append((invalid_seconds, "maximum_duration_seconds must be a positive integer"))
        unknown_override = project_with_transport("command")
        unknown_override["resource_coordination"]["deadline_policy"]["resource_overrides"] = {
            "port:production": {
                "resource_class": "unknown",
                "maximum_duration_seconds": 60,
                "cleanup_grace_seconds": 10,
            }
        }
        cases.append((unknown_override, "resource_class must name a configured resource class"))
        noncanonical_override = project_with_transport("command")
        noncanonical_override["resource_coordination"]["deadline_policy"]["resource_overrides"] = {
            " port:production ": {
                "resource_class": "database-port",
                "maximum_duration_seconds": 60,
                "cleanup_grace_seconds": 10,
            }
        }
        cases.append((noncanonical_override, "resource override ids must be canonical"))

        for project, message in cases:
            with self.subTest(message=message):
                with self.assertRaisesRegex(ValueError, message):
                    renderer.render(project)

    def test_none_rejects_claim_deadline_policy(self) -> None:
        """Keep disabled coordination free of stale claim-specific policy."""

        renderer = load_renderer_module()
        project = project_with_transport("command")
        project["resource_coordination"]["selected"] = "none"
        project.pop("agent_claim_transport")

        with self.assertRaisesRegex(
            ValueError,
            "resource_coordination keys must be exactly: selected",
        ):
            renderer.render(project)

    def test_renderer_rejects_missing_or_unsupported_resource_coordination(self) -> None:
        """Require one supported project-wide coordination selector without a fallback."""

        renderer = load_renderer_module()
        missing = project_with_transport("mcp")
        missing.pop("resource_coordination")
        unsupported = project_with_transport("mcp")
        unsupported["resource_coordination"] = {"selected": "claims-broker"}

        with self.assertRaisesRegex(
            ValueError,
            "resource_coordination is required",
        ):
            renderer.render(missing)
        with self.assertRaisesRegex(
            ValueError,
            "resource_coordination.selected must be none or agent-claim",
        ):
            renderer.render(unsupported)

    def test_none_renders_no_coordination_or_transport_guidance(self) -> None:
        """Omit implementation, procedure, transport, and evidence when coordination is disabled."""

        renderer = load_renderer_module()
        project = project_with_transport("mcp")
        project["resource_coordination"] = {"selected": "none"}
        project.pop("agent_claim_transport")

        rendered = renderer.render(project)

        self.assertNotIn("## Resource Coordination Skill Reference", rendered)
        self.assertNotIn("## Agent Claim Transport", rendered)
        self.assertNotIn("agent-claim", rendered)
        self.assertNotIn("CLAIM_TRANSPORT", rendered)
        self.assertNotIn("transport fixture evidence", rendered)

    def test_none_rejects_every_present_claim_transport_value(self) -> None:
        """Reject stale transport configuration instead of silently ignoring its value."""

        renderer = load_renderer_module()
        stale_values = (
            project_with_transport("mcp")["agent_claim_transport"],
            {"selected": "mcp"},
            "mcp",
        )

        for stale_value in stale_values:
            with self.subTest(stale_value=stale_value):
                project = project_with_transport("mcp")
                project["resource_coordination"] = {"selected": "none"}
                project["agent_claim_transport"] = stale_value

                with self.assertRaisesRegex(
                    ValueError,
                    "agent_claim_transport must be omitted when resource_coordination.selected is none",
                ):
                    renderer.render(project)

    def test_selected_resource_lifecycle_pairs_none_with_agent_claim(self) -> None:
        """Validate none without calls and keep MCP operations on the MCP boundary."""

        none_project = project_with_transport("mcp")
        none_project["resource_coordination"] = {"selected": "none"}
        none_project.pop("agent_claim_transport")
        unavailable_transport = _SimulatedMcpTransport(available=False)

        none_evidence = _run_none_resource_lifecycle(none_project)

        self.assertEqual({"resource_coordination": "none"}, none_evidence)
        self.assertEqual([], unavailable_transport.calls)
        self.assertEqual([], unavailable_transport.claim_calls)

        selected_transport = _SimulatedMcpTransport()
        claim_evidence = _run_selected_mcp_lifecycle(
            project_with_transport("mcp"),
            selected_transport,
            "resource-lifecycle-agent-claim",
            ("database:integration",),
        )

        self.assertEqual(
            ["claim_acquire", "claim_extend_deadline", "claim_release"],
            selected_transport.calls,
        )
        self.assertEqual(
            [
                (
                    "claim_acquire",
                    "resource-lifecycle-agent-claim",
                    ("database:integration",),
                ),
                ("claim_extend_deadline", "resource-lifecycle-agent-claim", ()),
                ("claim_release", "resource-lifecycle-agent-claim", ()),
            ],
            selected_transport.claim_calls,
        )
        self.assertEqual("database-port", selected_transport.deadline_calls[0]["resource_class"])
        self.assertEqual("database:integration", selected_transport.deadline_calls[0]["resource_id"])
        self.assertEqual(300, selected_transport.deadline_calls[0]["expected_duration_seconds"])
        self.assertEqual(900, selected_transport.deadline_calls[0]["requested_hard_stop_duration_seconds"])
        self.assertEqual(
            "future MCP deadline parity contract",
            selected_transport.deadline_calls[1]["extension_evidence"],
        )
        self.assertEqual("mcp", claim_evidence["transport"])
        self.assertEqual("resource-lifecycle-agent-claim", claim_evidence["claim_id"])
        self.assertEqual("SHARED_CHECKOUT_ACQUIRED", claim_evidence["acquire_outcome"])
        self.assertEqual("DEADLINE_EXTENDED", claim_evidence["extend_deadline_outcome"])
        self.assertEqual("CLAIM_RELEASED", claim_evidence["release_outcome"])

        mismatched_transport = _SimulatedMcpTransport()
        with self.assertRaisesRegex(
            RuntimeError,
            "CLAIM_TRANSPORT_BINDING_MISMATCH",
        ):
            _run_selected_mcp_lifecycle(
                project_with_transport("command"),
                mismatched_transport,
                "resource-lifecycle-mismatch",
                ("database:integration",),
            )
        self.assertEqual([], mismatched_transport.calls)
        self.assertEqual([], mismatched_transport.claim_calls)

    def test_command_lifecycle_uses_actual_argv_and_structured_results(self) -> None:
        """Bind command selection to the bundled script and one claim identifier."""

        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory) / "repository"
            repository.mkdir()
            subprocess.run(
                ["git", "init", "--initial-branch=main", str(repository)],
                check=True,
                text=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "-C", str(repository), "config", "user.email", "test@example.invalid"],
                check=True,
                text=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "-C", str(repository), "config", "user.name", "Claim Transport Test"],
                check=True,
                text=True,
                capture_output=True,
            )
            project = project_with_transport("command")
            (repository / "PROJECT.yaml").write_text(
                yaml.safe_dump(project, sort_keys=False),
                encoding="utf-8",
            )
            subprocess.run(
                ["git", "-C", str(repository), "add", "PROJECT.yaml"],
                check=True,
                text=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "-C", str(repository), "commit", "-m", "baseline"],
                check=True,
                text=True,
                capture_output=True,
            )

            evidence = _run_command_resource_lifecycle(
                project,
                repository,
                "resource-lifecycle-command",
                ("database:integration",),
            )
            with self.assertRaisesRegex(
                RuntimeError,
                "CLAIM_TRANSPORT_BINDING_MISMATCH",
            ):
                _run_command_resource_lifecycle(
                    project_with_transport("mcp"),
                    repository,
                    "resource-lifecycle-command-mismatch",
                    ("database:integration",),
                )

        self.assertEqual("command", evidence["transport"])
        self.assertEqual("resource-lifecycle-command", evidence["claim_id"])
        self.assertEqual(["database:integration"], evidence["resources"])
        self.assertEqual("SHARED_CHECKOUT_ACQUIRED", evidence["acquire_outcome"])
        self.assertEqual("RELEASED", evidence["release_outcome"])
        self.assertEqual(0, evidence["acquire_returncode"])
        self.assertEqual(0, evidence["release_returncode"])
        self.assertEqual(sys.executable, evidence["acquire_argv"][0])
        self.assertEqual(str(COMMAND_SCRIPT), evidence["acquire_argv"][1])
        self.assertEqual("acquire", evidence["acquire_argv"][4])
        self.assertIn("--resource", evidence["acquire_argv"])
        self.assertIn("database:integration", evidence["acquire_argv"])
        self.assertIn("--resource-class", evidence["acquire_argv"])
        self.assertIn("--requested-hard-stop-duration-seconds", evidence["acquire_argv"])
        self.assertNotIn("--configured-maximum-duration-seconds", evidence["acquire_argv"])
        self.assertEqual("resource-lifecycle-command", evidence["release_argv"][-2])
        self.assertEqual("--no-change", evidence["release_argv"][-1])

    def test_command_transport_reports_existing_linked_checkout_topology(self) -> None:
        """Verify the selected command reports physical topology without changing primary state."""

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repository = root / "repository"
            linked_path = root / "private-checkout"
            repository.mkdir()
            subprocess.run(
                ["git", "init", "--initial-branch=main", str(repository)],
                check=True,
                text=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "-C", str(repository), "config", "user.email", "test@example.invalid"],
                check=True,
                text=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "-C", str(repository), "config", "user.name", "Claim Transport Test"],
                check=True,
                text=True,
                capture_output=True,
            )
            (repository / "PROJECT.yaml").write_text(
                yaml.safe_dump(project_with_transport("command"), sort_keys=False),
                encoding="utf-8",
            )
            (repository / "README.md").write_text("baseline\n", encoding="utf-8")
            subprocess.run(
                ["git", "-C", str(repository), "add", "."],
                check=True,
                text=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "-C", str(repository), "commit", "-m", "baseline"],
                check=True,
                text=True,
                capture_output=True,
            )
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(repository),
                    "worktree",
                    "add",
                    "-b",
                    "codex/private",
                    str(linked_path),
                    "HEAD",
                ],
                check=True,
                text=True,
                capture_output=True,
            )
            primary_head = subprocess.run(
                ["git", "-C", str(repository), "rev-parse", "HEAD"],
                check=True,
                text=True,
                capture_output=True,
            ).stdout
            primary_status = subprocess.run(
                ["git", "-C", str(repository), "status", "--porcelain=v1"],
                check=True,
                text=True,
                capture_output=True,
            ).stdout

            completed = subprocess.run(
                [
                    sys.executable,
                    str(COMMAND_SCRIPT),
                    "--repo",
                    str(linked_path),
                    "acquire",
                    "--claim-id",
                    "private",
                    "--agent",
                    "private",
                    "--task",
                    "linked topology",
                    "--root-task-id",
                    "private",
                    "--file",
                    "README.md",
                ],
                check=False,
                text=True,
                capture_output=True,
            )

            self.assertEqual(0, completed.returncode, completed.stderr)
            result = json.loads(completed.stdout)
            self.assertEqual("SHARED_CHECKOUT_ACQUIRED", result["outcome"])
            self.assertEqual("PRIMARY", result["legacy_outcome"])
            self.assertEqual("primary", result["claim"]["mode"])
            self.assertEqual("linked", result["claim"]["checkout_topology"])
            self.assertEqual("linked", result["target"]["checkout_topology"])
            self.assertEqual(
                primary_head,
                subprocess.run(
                    ["git", "-C", str(repository), "rev-parse", "HEAD"],
                    check=True,
                    text=True,
                    capture_output=True,
                ).stdout,
            )
            self.assertEqual(
                primary_status,
                subprocess.run(
                    ["git", "-C", str(repository), "status", "--porcelain=v1"],
                    check=True,
                    text=True,
                    capture_output=True,
                ).stdout,
            )
            event_path = next(
                (repository / ".git" / "agent-claim-events" / "hot").glob("*.jsonl")
            )
            event = json.loads(event_path.read_text(encoding="utf-8").splitlines()[-1])
            self.assertEqual("linked", event["checkout_topology"])
            self.assertEqual("codex/private", event["worktree_id"])
            self.assertNotIn(str(root), json.dumps(event))

    def test_renderer_reserves_coordination_skills_from_alternate_loading(self) -> None:
        """Prevent project extensions and technology loadouts from bypassing the selector."""

        renderer = load_renderer_module()
        reserved = ("agent-claim", "agent-claim-mcp", "agent-claim-command")
        for coordination in ("none", "agent-claim"):
            for skill in reserved:
                with self.subTest(
                    coordination=coordination,
                    route="project_skill_extensions",
                    skill=skill,
                ):
                    project = project_with_transport("mcp")
                    if coordination == "none":
                        project["resource_coordination"] = {"selected": "none"}
                        project.pop("agent_claim_transport")
                    project["project_skill_extensions"] = [skill]
                    with self.assertRaisesRegex(
                        ValueError,
                        "reserved for resource_coordination",
                    ):
                        renderer.render(project)

                with self.subTest(
                    coordination=coordination,
                    route="technology_skill_loadouts",
                    skill=skill,
                ):
                    project = project_with_transport("mcp")
                    if coordination == "none":
                        project["resource_coordination"] = {"selected": "none"}
                        project.pop("agent_claim_transport")
                    project["technology_skill_loadouts"] = [
                        {
                            "pathPattern": "src/**",
                            "skills": [skill],
                            "sourceEvidence": [],
                        }
                    ]
                    with self.assertRaisesRegex(
                        ValueError,
                        "reserved for resource_coordination",
                    ):
                        renderer.render(project)

    def test_agent_claim_rejects_missing_or_unavailable_transport(self) -> None:
        """Require a verified transport only when agent-claim is selected."""

        renderer = load_renderer_module()
        project = project_with_transport("mcp", availability="UNAVAILABLE")
        missing = dict(project)
        missing.pop("agent_claim_transport")

        with self.assertRaisesRegex(
            ValueError,
            "agent_claim_transport is required",
        ):
            renderer.render(missing)
        with self.assertRaisesRegex(
            ValueError,
            "configured claim transport mcp is unavailable; run Project Configurator",
        ):
            renderer.render(project)

    def test_shared_semantics_and_transport_mechanics_are_separate(self) -> None:
        """Keep policy neutral while each adapter owns one complete invocation surface."""

        shared = SHARED_SKILL.read_text(encoding="utf-8")
        mcp = MCP_SKILL.read_text(encoding="utf-8")
        command = COMMAND_SKILL.read_text(encoding="utf-8")

        self.assertNotIn("## Operation Selection", shared)
        self.assertNotIn("CLAIM_SCRIPT", shared)
        self.assertNotIn("claim_status", shared)
        self.assertIn("claim_status", mcp)
        self.assertNotIn("CLAIM_SCRIPT", mcp)
        self.assertIn("CLAIM_SCRIPT", command)
        self.assertNotIn("claim_status", command)
        self.assertIn("exit_code", mcp)
        self.assertIn("exit_code", command)
        self.assertIn("result.outcome", mcp)
        self.assertIn("result.outcome", command)

    def test_adapters_preserve_rejections_and_reconcile_ambiguous_dispatch_in_place(self) -> None:
        """Prohibit fallback both for valid rejections and uncertain mutating dispatches."""

        for path in (MCP_SKILL, COMMAND_SKILL):
            with self.subTest(adapter=path.parent.name):
                adapter = path.read_text(encoding="utf-8")

                self.assertIn("structured rejection", adapter)
                self.assertIn("do not switch transports", adapter)
                self.assertIn("ambiguous", adapter)
                self.assertIn("status", adapter)
                self.assertIn("CLAIM_TRANSPORT_UNAVAILABLE", adapter)

    def test_portable_command_is_owned_by_command_adapter(self) -> None:
        """Ship the command implementation only with its independently distributable adapter."""

        self.assertTrue(COMMAND_SCRIPT.is_file())
        self.assertFalse(LEGACY_COMMAND_SCRIPT.exists())

    def test_standard_codex_install_uses_current_user_skill_root(self) -> None:
        """Resolve the command from the current user-scope Codex bundle location."""

        command = COMMAND_SKILL.read_text(encoding="utf-8")
        self.assertIn(
            '${HOME}/.agents/skills/agent-claim-command/scripts/claim.py',
            command,
        )
        self.assertNotIn('${CODEX_HOME:-$HOME/.codex}/skills', command)

    def test_mutating_eval_cases_stage_one_matching_claim_adapter(self) -> None:
        """Stage shared semantics plus exactly the transport used by each mutating fixture."""

        catalog = yaml.safe_load(CASES_PATH.read_text(encoding="utf-8"))
        cases = [
            case
            for case in catalog["cases"]
            if "agent-claim" in case.get("requiredSkills", [])
            and not case.get("readOnly", False)
        ]
        self.assertEqual(8, len(cases))
        for case in cases:
            selected = "agent-claim-mcp" if "mcpAgentOps" in case else "agent-claim-command"
            unused = "agent-claim-command" if selected == "agent-claim-mcp" else "agent-claim-mcp"
            with self.subTest(case=case["id"], selected=selected):
                required = case["requiredSkills"]
                staged = case["contextPack"]["stagedSkillPackages"]
                resources = case["skillResourceAllowlist"]
                self.assertIn(selected, required)
                self.assertIn(selected, staged)
                self.assertNotIn(unused, required)
                self.assertNotIn(unused, staged)
                self.assertEqual(["SKILL.md"], resources["agent-claim"])
                expected = (
                    ["SKILL.md"]
                    if selected == "agent-claim-mcp"
                    else ["SKILL.md", "scripts/claim.py"]
                )
                self.assertEqual(expected, resources[selected])
                self.assertNotIn(unused, resources)

    def test_mcp_setup_requires_complete_schema_v2_surface(self) -> None:
        """Reject an incomplete tool surface or legacy result schema during setup."""

        incomplete = _SimulatedMcpTransport(
            tools=REQUIRED_FUTURE_MCP_CLAIM_TOOLS - {"claim_release"},
        )
        legacy = _SimulatedMcpTransport(result_schema_version=1)
        with self.assertRaisesRegex(RuntimeError, "CLAIM_TRANSPORT_INCOMPLETE"):
            _run_mcp_acquire(incomplete)
        with self.assertRaisesRegex(RuntimeError, "CLAIM_TRANSPORT_SCHEMA_UNSUPPORTED"):
            _run_mcp_acquire(legacy)

    def test_mcp_schema_v2_success_and_structured_rejection_are_authoritative(self) -> None:
        """Accept canonical success and rejection outcomes without probing another transport."""

        success = _SimulatedMcpTransport()
        rejection = _SimulatedMcpTransport(
            acquire_result={
                "exit_code": 1,
                "result": {"schema_version": 2, "outcome": "INVALID_SCOPE"},
            }
        )

        self.assertEqual("SHARED_CHECKOUT_ACQUIRED", _run_mcp_acquire(success)["outcome"])
        self.assertEqual("INVALID_SCOPE", _run_mcp_acquire(rejection)["outcome"])
        self.assertEqual(["claim_acquire"], success.calls)
        self.assertEqual(["claim_acquire"], rejection.calls)

    def test_mcp_unavailable_and_ambiguous_dispatch_have_deterministic_actions(self) -> None:
        """Fail unavailable setup and reconcile ambiguity only through MCP claim_status."""

        unavailable = _SimulatedMcpTransport(available=False)
        ambiguous = _SimulatedMcpTransport(ambiguous_acquire=True)
        with self.assertRaisesRegex(RuntimeError, "CLAIM_TRANSPORT_UNAVAILABLE"):
            _run_mcp_acquire(unavailable)
        self.assertEqual([], unavailable.calls)

        self.assertEqual("STATUS", _run_mcp_acquire(ambiguous)["outcome"])
        self.assertEqual(["claim_acquire", "claim_status"], ambiguous.calls)

    def test_project_configuration_fixture_selects_its_mcp_adapter(self) -> None:
        """Expose and require the adapter matching the fixture's MCP claim sequence."""

        available = (
            PROJECT_CONFIGURATION_FIXTURE / "available-skills.txt"
        ).read_text(encoding="utf-8").splitlines()
        task = (PROJECT_CONFIGURATION_FIXTURE / "TASK.md").read_text(encoding="utf-8")
        self.assertIn("agent-claim-mcp", available)
        self.assertIn("Select the MCP claim transport", task)
        self.assertIn("result schema version 2", task)
        self.assertIn("Do not probe or fall back to the command transport", task)

    def test_mcp_eval_contract_pins_canonical_schema_v2_runtime(self) -> None:
        """Replace the retired MCP fixture identity and legacy acquisition outcome."""

        catalog = yaml.safe_load(CASES_PATH.read_text(encoding="utf-8"))
        case = next(
            item
            for item in catalog["cases"]
            if item["id"] == "project-configuration-routing"
        )
        contract = case["mcpAgentOps"]
        self.assertEqual(2, contract["claimResultSchemaVersion"])
        self.assertEqual("0.4.0", contract["requiredVersion"])
        self.assertEqual(
            "b4abdd4054a3b6181d2cc48d4c9de6b4fbbc29eb6fd256e0427d861e2ae1620d",
            contract["requiredRuntimeDigest"],
        )
        enabled_tools = set(contract["enabledTools"])
        self.assertTrue(LIVE_MCP_CLAIM_TOOLS <= enabled_tools)
        self.assertNotIn("claim_extend_deadline", enabled_tools)
        self.assertFalse(REQUIRED_FUTURE_MCP_CLAIM_TOOLS <= enabled_tools)
        self.assertEqual("UNRESOLVED_EXTERNAL_PROVIDER", MCP_DEADLINE_PARITY)
        self.assertEqual(
            ["SHARED_CHECKOUT_ACQUIRED"],
            contract["requiredToolOutcomes"]["claim_acquire"],
        )


if __name__ == "__main__":
    unittest.main()
