#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies claim-helper interfaces, deadline-policy rendering, invocation behavior, and evaluation staging.
# Design: design/work-item-provider-and-completion-contracts.md

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from collections.abc import Iterator
from pathlib import Path

import yaml

from scripts.agent_skill_evals import validation as eval_validation
from scripts.skill_sources import (
    directory_has_maintained_source,
    iter_maintained_source_files,
)


ROOT = Path(__file__).resolve().parents[1]
RENDER_SCRIPT = ROOT / "scripts" / "render-agents-technology-skills.py"
POLICY_SKILL = ROOT / "skills" / "resource-claim" / "SKILL.md"
INTERFACE_SKILL = ROOT / "skills" / "resource-claim-helper" / "SKILL.md"
MCP_SKILL = ROOT / "skills" / "resource-claim-helper-mcp" / "SKILL.md"
COMMAND_SKILL = ROOT / "skills" / "resource-claim-helper-command" / "SKILL.md"
COMMAND_SCRIPT = ROOT / "skills" / "resource-claim-helper-command" / "scripts" / "claim.py"
LEGACY_COMMAND_SCRIPT = ROOT / "skills" / "resource-claim" / "scripts" / "claim.py"
CASES_PATH = ROOT / "evals" / "cases.yaml"
PROJECT_CONFIGURATION_FIXTURE = ROOT / "evals" / "projects" / "project-configuration-routing"
SKILL_GROUP_MODEL = ROOT / "design" / "object-oriented-skill-group-models.md"
LIVE_MCP_CLAIM_TOOLS = frozenset({
    "claim_status",
    "claim_acquire",
    "claim_extend",
    "claim_heartbeat",
    "claim_release",
    "claim_maintain_journal",
    "claim_report",
})
REQUIRED_MCP_CLAIM_TOOLS = LIVE_MCP_CLAIM_TOOLS | {
    "claim_extend_deadline",
    "claim_reset",
}
MCP_DEADLINE_PARITY = "UNRESOLVED_EXTERNAL_PROVIDER"
CANONICAL_ACQUIRE_OUTCOMES = frozenset({
    "SHARED_CHECKOUT_ACQUIRED",
    "ISOLATED_CHECKOUT_ACQUIRED",
    "CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED",
    "SHARED_CHECKOUT_REQUIRED",
    "INVALID_SCOPE",
})
LEGACY_ONLY_CANONICAL_OUTCOMES = frozenset({
    "DIRTY_CHECKOUT_RECOVERY_ACQUIRED",
    "SHARED_CHECKOUT_RELEASE_REQUIRED",
    "ISOLATED_CHECKOUT_SETUP_REQUIRED",
    "DIRTY_CHECKOUT_RECOVERY_AUTHORIZATION_REQUIRED",
})
CANONICAL_OPERATION_OUTCOMES = {
    "Read Claim Status": ("STATUS",),
    "Acquire Claim": (
        "SHARED_CHECKOUT_ACQUIRED",
        "ISOLATED_CHECKOUT_ACQUIRED",
        "CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED",
        "SHARED_CHECKOUT_REQUIRED",
        "CLAIM_ID_EXISTS",
        "INVALID_SCOPE",
        "INVALID_WORK_ITEM_SCOPE",
        "INVALID_DEADLINE_POLICY",
        "INVALID_IDENTIFIER",
        "INVALID_WORKTREE_PATH",
        "WORKTREE_ROOT_NOT_IGNORED",
        "WORKTREE_CREATE_FAILED",
    ),
    "Extend Claim": (
        "EXTENDED",
        "CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED",
        "SHARED_CHECKOUT_REQUIRED",
        "CLAIM_NOT_FOUND",
        "INVALID_SCOPE",
        "INVALID_WORK_ITEM_SCOPE",
        "INVALID_DEADLINE_POLICY",
    ),
    "Extend Claim Deadline": (
        "DEADLINE_EXTENDED",
        "CLAIM_NOT_FOUND",
        "INVALID_DEADLINE_EXTENSION",
    ),
    "Heartbeat Claim": ("HEARTBEAT", "CLAIM_NOT_FOUND"),
    "Release Claim": (
        "RELEASED",
        "CLAIM_NOT_FOUND",
        "INVALID_WORK_ITEM_RELEASE",
        "RELEASE_ERROR",
    ),
    "Reset Claim Registry": ("RESET",),
    "Maintain Claim Journal": (
        "JOURNAL_MAINTAINED",
        "INVALID_HOT_DAYS",
        "JOURNAL_MAINTENANCE_FAILED",
    ),
    "Report Claim Contention": ("REPORT", "INVALID_SINCE"),
}
WORK_ITEM_REPORT_SEGMENT_FIELDS = (
    "claim_id",
    "incarnation_id",
    "owner",
    "root_task_id",
    "activity",
    "acquired_at",
    "released_at",
    "disposition",
    "blocker_reference",
    "duration_seconds",
    "open",
    "live",
    "acquisition_event_id",
    "release_event_id",
)
RETIRED_PROVIDER_IDENTITIES = (
    "resource-claim-" + "command",
    "resource-claim-" + "mcp",
)
MAINTAINED_TEXT_SUFFIXES = frozenset({
    ".html",
    ".js",
    ".json",
    ".md",
    ".py",
    ".svg",
    ".toml",
    ".yaml",
    ".yml",
})
_MAINTAINED_SURFACE_RELATIVE_PATHS = (
    Path(".agents"),
    Path(".codex/config.toml"),
    Path("adapters"),
    Path("agents"),
    Path("design"),
    Path("evals"),
    Path("generated"),
    Path("legacy_procedures"),
    Path("scripts"),
    Path("skills"),
    Path("AGENTS.md"),
    Path("PROJECT.yaml"),
    Path("README.md"),
    Path("index.html"),
)


def _maintained_text_files(repository_root: Path) -> Iterator[Path]:
    """Yield maintained text artifacts without entering operational repository state."""

    for relative_root in _MAINTAINED_SURFACE_RELATIVE_PATHS:
        for path in iter_maintained_source_files(repository_root / relative_root):
            if path.suffix not in MAINTAINED_TEXT_SUFFIXES:
                continue
            relative = path.relative_to(repository_root)
            relative_text = relative.as_posix()
            if relative_text.startswith("evals/results/") or ".review-" in path.name:
                continue
            yield path


def _markdown_section(document: str, heading: str, *, level: int = 2) -> str:
    """Return one Markdown section without content from same-level siblings."""

    marker = f"{'#' * level} {heading}\n"
    start = document.index(marker) + len(marker)
    end = document.find(f"\n{'#' * level} ", start)
    return document[start:] if end < 0 else document[start:end]


def _fenced_examples(section: str, language: str) -> list[str]:
    """Return fenced examples from one already isolated Markdown section."""

    return re.findall(rf"```{language}\n(.*?)\n```", section, flags=re.DOTALL)


class _AmbiguousDispatch(RuntimeError):
    """Represent a mutating MCP dispatch whose completion was not observed."""


class _SimulatedMcpHelper:
    """Provide deterministic schema-v2 results for the MCP claim boundary."""

    def __init__(
        self,
        *,
        available: bool = True,
        tools: frozenset[str] = REQUIRED_MCP_CLAIM_TOOLS,
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
            raise RuntimeError("CLAIM_HELPER_UNAVAILABLE")
        if self.tools != REQUIRED_MCP_CLAIM_TOOLS:
            raise RuntimeError("CLAIM_HELPER_INCOMPLETE")
        if self.result_schema_version != 2:
            raise RuntimeError("CLAIM_HELPER_SCHEMA_UNSUPPORTED")

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
                "result": {"schema_version": 2, "outcome": "RELEASED"},
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
        raise RuntimeError("CLAIM_HELPER_RESULT_INVALID")
    result = response.get("result")
    if not isinstance(result, dict) or result.get("schema_version") != 2:
        raise RuntimeError("CLAIM_HELPER_SCHEMA_UNSUPPORTED")
    return result


def _run_mcp_acquire(helper: _SimulatedMcpHelper) -> dict[str, object]:
    """Execute acquisition or reconcile an ambiguous dispatch through the same MCP surface."""

    helper.verify_setup()
    try:
        response = helper.call(
            "claim_acquire",
            claim_id="mcp-acquire-test",
            resources=("database:test",),
            resource_class="database-port",
            resource_id="database:test",
            expected_duration_seconds=300,
            requested_hard_stop_duration_seconds=900,
        )
    except _AmbiguousDispatch:
        response = helper.call("claim_status")
    result = _canonical_mcp_result(response)
    outcome = result.get("outcome")
    if outcome != "STATUS" and outcome not in CANONICAL_ACQUIRE_OUTCOMES:
        raise RuntimeError("CLAIM_HELPER_OUTCOME_UNSUPPORTED")
    return result


def _run_none_resource_lifecycle(project: dict[str, object]) -> dict[str, object]:
    """Validate one renderer-valid none selection without invoking a helper."""

    load_renderer_module().render(project)
    coordination = project.get("resource_coordination")
    if not isinstance(coordination, dict) or coordination.get("selected") != "none":
        raise ValueError("resource_coordination.selected must be none")
    return {"resource_coordination": "none"}


def _run_selected_mcp_lifecycle(
    project: dict[str, object],
    helper: _SimulatedMcpHelper,
    claim_id: str,
    resources: tuple[str, ...],
) -> dict[str, object]:
    """Exercise an MCP-selected acquire and release through its simulated tool boundary."""

    load_renderer_module().render(project)
    coordination = project.get("resource_coordination")
    if not isinstance(coordination, dict):
        raise ValueError("resource_coordination is required")
    selected = coordination.get("selected")
    if selected != "resource-claim":
        raise ValueError("resource_coordination.selected must be resource-claim")

    helper_configuration = project.get("agent_claim_transport")
    if not isinstance(helper_configuration, dict):
        raise ValueError("agent_claim_transport is required")
    configured_helper = helper_configuration.get("selected")
    if configured_helper != "mcp":
        raise RuntimeError("CLAIM_HELPER_BINDING_MISMATCH")

    helper.verify_setup()
    if len(resources) != 1:
        raise ValueError("MCP lifecycle requires exactly one named resource")
    acquired = _canonical_mcp_result(helper.call(
        "claim_acquire",
        claim_id=claim_id,
        resources=resources,
        resource_class="database-port",
        resource_id=resources[0],
        expected_duration_seconds=300,
        requested_hard_stop_duration_seconds=900,
    ))
    extended = _canonical_mcp_result(helper.call(
        "claim_extend_deadline",
        claim_id=claim_id,
        requested_hard_stop_duration_seconds=1200,
        extension_evidence="future MCP deadline parity contract",
    ))
    released = _canonical_mcp_result(
        helper.call("claim_release", claim_id=claim_id)
    )
    return {
        "resource_coordination": "resource-claim",
        "helper": "mcp",
        "claim_id": claim_id,
        "resources": list(resources),
        "acquire_outcome": acquired["outcome"],
        "extend_deadline_outcome": extended["outcome"],
        "release_outcome": released["outcome"],
    }


def _command_result(
    completed: subprocess.CompletedProcess[str],
) -> dict[str, object]:
    """Decode one successful command-provider JSON result."""

    if completed.returncode != 0:
        raise RuntimeError(
            f"command claim invocation failed with {completed.returncode}: {completed.stderr}"
        )
    result = json.loads(completed.stdout)
    if not isinstance(result, dict) or result.get("schema_version") != 2:
        raise RuntimeError("CLAIM_HELPER_SCHEMA_UNSUPPORTED")
    return result


def _run_command_resource_lifecycle(
    project: dict[str, object],
    repository: Path,
    claim_id: str,
    resources: tuple[str, ...],
) -> dict[str, object]:
    """Exercise a command-selected acquire and release through actual process argv."""

    load_renderer_module().render(project)
    helper_configuration = project.get("agent_claim_transport")
    if not isinstance(helper_configuration, dict):
        raise ValueError("agent_claim_transport is required")
    if helper_configuration.get("selected") != "command":
        raise RuntimeError("CLAIM_HELPER_BINDING_MISMATCH")
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
        "claim-helper-test",
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
        "resource_coordination": "resource-claim",
        "helper": "command",
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
        "render_agents_claim_helper",
        RENDER_SCRIPT,
    )
    if specification is None or specification.loader is None:
        raise RuntimeError(f"Unable to load {RENDER_SCRIPT}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def load_command_module():
    """Load the command provider so its legacy normalization table stays documented."""

    specification = importlib.util.spec_from_file_location(
        "resource_claim_helper_command_contract",
        COMMAND_SCRIPT,
    )
    if specification is None or specification.loader is None:
        raise RuntimeError(f"Unable to load {COMMAND_SCRIPT}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def project_with_helper(selected: str, availability: str = "AVAILABLE") -> dict[str, object]:
    """Return the smallest project fixture with one verified claim helper."""

    return {
        "resource_coordination": {
            "selected": "resource-claim",
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
            "verification": [f"{selected} claim-helper fixture evidence"],
        },
        "workflow_selection": {
            "provider": {"default": "UNSET"},
            "completion": {"default": "UNSET"},
        },
        "technology_skill_loadouts": [],
    }


class ResourceClaimHelperTests(unittest.TestCase):
    """Protect standalone claim-helper composition and failure behavior."""

    def test_reset_clears_live_claims_and_preserves_audit_event(self) -> None:
        """Prove crisis entry can empty ownership without erasing history."""

        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            subprocess.run(
                ["git", "init", "-q", str(repository)],
                check=True,
                text=True,
                capture_output=True,
            )
            (repository / "seed.txt").write_text("seed\n", encoding="utf-8")
            subprocess.run(
                ["git", "-C", str(repository), "add", "seed.txt"],
                check=True,
                text=True,
                capture_output=True,
            )
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(repository),
                    "-c",
                    "user.name=Fixture",
                    "-c",
                    "user.email=fixture@example.invalid",
                    "commit",
                    "-q",
                    "-m",
                    "seed",
                ],
                check=True,
                text=True,
                capture_output=True,
            )
            base = [sys.executable, str(COMMAND_SCRIPT), "--repo", str(repository)]
            acquire = _command_result(
                subprocess.run(
                    base
                    + [
                        "acquire",
                        "--claim-id",
                        "crisis-entry-fixture",
                        "--agent",
                        "coordinator",
                        "--task",
                        "crisis-entry-fixture",
                        "--root-task-id",
                        "crisis-entry-fixture",
                        "--work-item-id",
                        "crisis-entry-fixture",
                        "--activity",
                        "work",
                    ],
                    check=False,
                    text=True,
                    capture_output=True,
                )
            )
            reset = _command_result(
                subprocess.run(
                    base + ["reset"],
                    check=False,
                    text=True,
                    capture_output=True,
                )
            )
            status = _command_result(
                subprocess.run(
                    base + ["status"],
                    check=False,
                    text=True,
                    capture_output=True,
                )
            )

            self.assertEqual("SHARED_CHECKOUT_ACQUIRED", acquire["outcome"])
            self.assertEqual("RESET", reset["outcome"])
            self.assertEqual([], status["claims"])
            journals = list(
                (repository / ".agent-ops" / "resource-claim" / "agent-claim-events").rglob("*.jsonl")
            )
            history = "".join(path.read_text(encoding="utf-8") for path in journals)
            self.assertIn('"action":"acquire"', history)
            self.assertIn('"action":"reset"', history)

    def test_renderer_inlines_only_selected_claim_helper_provider(self) -> None:
        """Compose shared role semantics with exactly one setup-selected provider."""

        renderer = load_renderer_module()
        for selected, included, excluded in (
            ("mcp", "resource-claim-helper-mcp", "resource-claim-helper-command"),
            ("command", "resource-claim-helper-command", "resource-claim-helper-mcp"),
        ):
            with self.subTest(selected=selected):
                rendered = renderer.render(project_with_helper(selected))

                self.assertIn("## Resource Coordination Skill Reference", rendered)
                self.assertIn("selected resource-coordination skill resource-claim", rendered)
                self.assertIn("## Resource Claim Helper", rendered)
                self.assertIn(
                    f"BEGIN INLINED CLAIM HELPER SKILL: {included}",
                    rendered,
                )
                self.assertNotIn(excluded, rendered)
                self.assertIn("Use only this configured claim helper", rendered)

    def test_renderer_validates_and_renders_deadline_classes_and_exact_id_overrides(self) -> None:
        """Expose every configured deadline value without hidden class inference."""

        renderer = load_renderer_module()
        project = project_with_helper("command")
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
        missing_class = project_with_helper("command")
        missing_class["resource_coordination"]["deadline_policy"]["resource_classes"].pop(
            "database-port"
        )
        cases.append((missing_class, "resource_classes keys must be exactly"))
        invalid_seconds = project_with_helper("command")
        invalid_seconds["resource_coordination"]["deadline_policy"]["resource_classes"][
            "database-port"
        ]["maximum_duration_seconds"] = 0
        cases.append((invalid_seconds, "maximum_duration_seconds must be a positive integer"))
        unknown_override = project_with_helper("command")
        unknown_override["resource_coordination"]["deadline_policy"]["resource_overrides"] = {
            "port:production": {
                "resource_class": "unknown",
                "maximum_duration_seconds": 60,
                "cleanup_grace_seconds": 10,
            }
        }
        cases.append((unknown_override, "resource_class must name a configured resource class"))
        noncanonical_override = project_with_helper("command")
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
        project = project_with_helper("command")
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
        missing = project_with_helper("mcp")
        missing.pop("resource_coordination")
        unsupported = project_with_helper("mcp")
        unsupported["resource_coordination"] = {"selected": "claims-broker"}

        with self.assertRaisesRegex(
            ValueError,
            "resource_coordination is required",
        ):
            renderer.render(missing)
        with self.assertRaisesRegex(
            ValueError,
            "resource_coordination.selected must be none or resource-claim",
        ):
            renderer.render(unsupported)

    def test_none_renders_no_coordination_or_claim_helper_guidance(self) -> None:
        """Omit implementation, procedure, invocation interface, and evidence when coordination is disabled."""

        renderer = load_renderer_module()
        project = project_with_helper("mcp")
        project["resource_coordination"] = {"selected": "none"}
        project.pop("agent_claim_transport")

        rendered = renderer.render(project)

        self.assertNotIn("## Resource Coordination Skill Reference", rendered)
        self.assertNotIn("## Resource Claim Helper", rendered)
        self.assertNotIn("resource-claim", rendered)
        self.assertNotIn("claim-helper fixture evidence", rendered)

    def test_none_rejects_every_present_claim_interface_value(self) -> None:
        """Reject a stale claim-helper interface selection instead of ignoring it."""

        renderer = load_renderer_module()
        stale_values = (
            project_with_helper("mcp")["agent_claim_transport"],
            {"selected": "mcp"},
            "mcp",
        )

        for stale_value in stale_values:
            with self.subTest(stale_value=stale_value):
                project = project_with_helper("mcp")
                project["resource_coordination"] = {"selected": "none"}
                project["agent_claim_transport"] = stale_value

                with self.assertRaisesRegex(
                    ValueError,
                    "agent_claim_transport must be omitted when resource_coordination.selected is none",
                ):
                    renderer.render(project)

    def test_selected_resource_lifecycle_pairs_none_with_resource_claim(self) -> None:
        """Validate none without calls and keep MCP operations on the MCP boundary."""

        none_project = project_with_helper("mcp")
        none_project["resource_coordination"] = {"selected": "none"}
        none_project.pop("agent_claim_transport")
        unavailable_helper = _SimulatedMcpHelper(available=False)

        none_evidence = _run_none_resource_lifecycle(none_project)

        self.assertEqual({"resource_coordination": "none"}, none_evidence)
        self.assertEqual([], unavailable_helper.calls)
        self.assertEqual([], unavailable_helper.claim_calls)

        selected_helper = _SimulatedMcpHelper()
        claim_evidence = _run_selected_mcp_lifecycle(
            project_with_helper("mcp"),
            selected_helper,
            "resource-lifecycle-resource-claim",
            ("database:integration",),
        )

        self.assertEqual(
            ["claim_acquire", "claim_extend_deadline", "claim_release"],
            selected_helper.calls,
        )
        self.assertEqual(
            [
                (
                    "claim_acquire",
                    "resource-lifecycle-resource-claim",
                    ("database:integration",),
                ),
                ("claim_extend_deadline", "resource-lifecycle-resource-claim", ()),
                ("claim_release", "resource-lifecycle-resource-claim", ()),
            ],
            selected_helper.claim_calls,
        )
        self.assertEqual("database-port", selected_helper.deadline_calls[0]["resource_class"])
        self.assertEqual("database:integration", selected_helper.deadline_calls[0]["resource_id"])
        self.assertEqual(300, selected_helper.deadline_calls[0]["expected_duration_seconds"])
        self.assertEqual(900, selected_helper.deadline_calls[0]["requested_hard_stop_duration_seconds"])
        self.assertEqual(
            "future MCP deadline parity contract",
            selected_helper.deadline_calls[1]["extension_evidence"],
        )
        self.assertEqual("mcp", claim_evidence["helper"])
        self.assertEqual("resource-lifecycle-resource-claim", claim_evidence["claim_id"])
        self.assertEqual("SHARED_CHECKOUT_ACQUIRED", claim_evidence["acquire_outcome"])
        self.assertEqual("DEADLINE_EXTENDED", claim_evidence["extend_deadline_outcome"])
        self.assertEqual("RELEASED", claim_evidence["release_outcome"])

        mismatched_helper = _SimulatedMcpHelper()
        with self.assertRaisesRegex(
            RuntimeError,
            "CLAIM_HELPER_BINDING_MISMATCH",
        ):
            _run_selected_mcp_lifecycle(
                project_with_helper("command"),
                mismatched_helper,
                "resource-lifecycle-mismatch",
                ("database:integration",),
            )
        self.assertEqual([], mismatched_helper.calls)
        self.assertEqual([], mismatched_helper.claim_calls)

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
                ["git", "-C", str(repository), "config", "user.name", "Claim Helper Test"],
                check=True,
                text=True,
                capture_output=True,
            )
            project = project_with_helper("command")
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
                "CLAIM_HELPER_BINDING_MISMATCH",
            ):
                _run_command_resource_lifecycle(
                    project_with_helper("mcp"),
                    repository,
                    "resource-lifecycle-command-mismatch",
                    ("database:integration",),
                )

        self.assertEqual("command", evidence["helper"])
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
        self.assertEqual("resource-lifecycle-command", evidence["release_argv"][-1])

    def test_claim_command_reports_existing_linked_checkout_topology(self) -> None:
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
                ["git", "-C", str(repository), "config", "user.name", "Claim Helper Test"],
                check=True,
                text=True,
                capture_output=True,
            )
            (repository / "PROJECT.yaml").write_text(
                yaml.safe_dump(project_with_helper("command"), sort_keys=False),
                encoding="utf-8",
            )
            (repository / ".gitignore").write_text(
                "/.worktrees/\n/.agent-ops/resource-claim/\n",
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
                (
                    repository
                    / ".agent-ops"
                    / "resource-claim"
                    / "agent-claim-events"
                    / "hot"
                ).glob("*.jsonl")
            )
            event = json.loads(event_path.read_text(encoding="utf-8").splitlines()[-1])
            self.assertEqual("linked", event["checkout_topology"])
            self.assertEqual("codex/private", event["worktree_id"])
            self.assertNotIn(str(root), json.dumps(event))

    def test_renderer_reserves_coordination_skills_from_alternate_loading(self) -> None:
        """Prevent project extensions and technology loadouts from bypassing the selector."""

        renderer = load_renderer_module()
        reserved = (
            "resource-claim",
            "resource-claim-helper",
            "resource-claim-helper-mcp",
            "resource-claim-helper-command",
        )
        for coordination in ("none", "resource-claim"):
            for skill in reserved:
                with self.subTest(
                    coordination=coordination,
                    route="project_skill_extensions",
                    skill=skill,
                ):
                    project = project_with_helper("mcp")
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
                    project = project_with_helper("mcp")
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

    def test_resource_claim_rejects_missing_or_unavailable_helper(self) -> None:
        """Require a verified claim helper only when resource-claim is selected."""

        renderer = load_renderer_module()
        project = project_with_helper("mcp", availability="UNAVAILABLE")
        missing = dict(project)
        missing.pop("agent_claim_transport")

        with self.assertRaisesRegex(
            ValueError,
            "agent_claim_transport is required",
        ):
            renderer.render(missing)
        with self.assertRaisesRegex(
            ValueError,
            "configured claim helper mcp is unavailable; run Project Configurator",
        ):
            renderer.render(project)

    def test_policy_interface_and_provider_responsibilities_are_separate(self) -> None:
        """Keep policy, helper contract, and provider invocation responsibilities distinct."""

        policy = POLICY_SKILL.read_text(encoding="utf-8")
        interface = INTERFACE_SKILL.read_text(encoding="utf-8")
        mcp = MCP_SKILL.read_text(encoding="utf-8")
        command = COMMAND_SKILL.read_text(encoding="utf-8")

        self.assertNotIn("## Operations", policy)
        self.assertNotIn("CLAIM_SCRIPT", policy)
        self.assertNotIn("claim_status", policy)
        self.assertIn("## Structured Outcomes", interface)
        self.assertIn("## Operation Contract", interface)
        for operation in (
            "Read Claim Status",
            "Acquire Claim",
            "Extend Claim",
            "Extend Claim Deadline",
            "Heartbeat Claim",
            "Release Claim",
            "Reset Claim Registry",
            "Maintain Claim Journal",
            "Report Claim Contention",
        ):
            self.assertRegex(interface, rf"(?m)^\| {re.escape(operation)} \|")
        self.assertNotIn("defined by the helper implementation", interface)
        self.assertIn("REPORT", interface)
        self.assertIn("window, event_count, metrics, work_items, coverage_gaps", interface)
        segment_contract = re.search(
            r"Every report segment contains exactly (?P<fields>[^.]+)\.",
            interface,
        )
        self.assertIsNotNone(segment_contract)
        assert segment_contract is not None
        self.assertEqual(
            WORK_ITEM_REPORT_SEGMENT_FIELDS,
            tuple(re.findall(r"`([^`]+)`", segment_contract.group("fields"))),
        )
        self.assertIn("## Reconcile an Uncertain Outcome", interface)
        self.assertIn("claim_status", mcp)
        self.assertIn("canonical outcome `RELEASED`", mcp)
        self.assertNotIn("CLAIM_SCRIPT", mcp)
        self.assertIn("CLAIM_SCRIPT", command)
        self.assertNotIn("claim_status", command)
        self.assertIn("exit_code", mcp)
        self.assertIn("process exit code", command)
        self.assertIn("explicit human-readable exception", command)
        self.assertIn("result.outcome", mcp)
        self.assertIn("Read `outcome`", command)

    def test_retired_provider_identities_are_absent_from_maintained_artifacts(self) -> None:
        """Keep old provider package names only in historical review and result records."""

        for retired_identity in RETIRED_PROVIDER_IDENTITIES:
            self.assertFalse(
                directory_has_maintained_source(ROOT / "skills" / retired_identity)
            )

        stale_references: list[str] = []
        for path in _maintained_text_files(ROOT):
            if path == Path(__file__).resolve():
                continue
            relative = path.relative_to(ROOT)
            relative_text = relative.as_posix()
            text = path.read_text(encoding="utf-8")
            for retired_identity in RETIRED_PROVIDER_IDENTITIES:
                if retired_identity in text:
                    stale_references.append(f"{relative_text}: {retired_identity}")

        self.assertEqual([], stale_references)

    def test_maintained_source_discovery_ignores_cache_only_retired_paths(
        self,
    ) -> None:
        """Exclude retired directory shells that contain only ignored Python caches."""

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            stale_identity = "resource-claim-" + "command"
            for retired_directory_name in ("agent-claim", "agent-claim-command"):
                cache = (
                    root
                    / "skills"
                    / retired_directory_name
                    / "scripts"
                    / "__pycache__"
                )
                cache.mkdir(parents=True)
                (cache / "claim.cpython-311.pyc").write_bytes(
                    stale_identity.encode("utf-8")
                )
            maintained_file = root / "skills" / "intended-skill" / "scripts" / "helper.py"
            maintained_file.parent.mkdir(parents=True)
            maintained_file.write_text(
                f'PROVIDER = "{stale_identity}"\n',
                encoding="utf-8",
            )
            operational_file = root / ".worktrees" / "other" / "stale.py"
            operational_file.parent.mkdir(parents=True)
            operational_file.write_text(
                f'PROVIDER = "{stale_identity}"\n',
                encoding="utf-8",
            )

            maintained_files = list(_maintained_text_files(root))
            stale_references = [
                path
                for path in maintained_files
                if stale_identity in path.read_text(encoding="utf-8")
            ]

            self.assertEqual([maintained_file], maintained_files)
            self.assertEqual([maintained_file], stale_references)
            self.assertTrue(
                directory_has_maintained_source(root / "skills" / "intended-skill")
            )
            for retired_identity in ("agent-claim", "agent-claim-command"):
                self.assertFalse(
                    directory_has_maintained_source(
                        root / "skills" / retired_identity
                    )
                )

    def test_skill_group_inventory_prose_matches_the_registry_total(self) -> None:
        """Keep the maintained inventory total aligned with its registry rows."""

        model = SKILL_GROUP_MODEL.read_text(encoding="utf-8")
        registry = _markdown_section(model, "3.2 Skill Group Registry", level=3)
        counts = [
            int(match.group("count"))
            for line in registry.splitlines()
            if (match := re.search(r"\| (?P<count>\d+) \|$", line))
        ]

        self.assertEqual(51, sum(counts))
        self.assertEqual(1, model.count("fifty-one"))
        self.assertEqual(3, model.count("fifty-five"))
        self.assertNotIn("forty-seven", model)
        self.assertNotIn("forty-four", model)

    def test_providers_read_results_and_reconcile_uncertain_calls_in_place(self) -> None:
        """Keep result handling and uncertain-call recovery with the configured helper."""

        for path in (MCP_SKILL, COMMAND_SKILL):
            with self.subTest(provider=path.parent.name):
                provider = path.read_text(encoding="utf-8")

                expected_outcome_reference = (
                    "result.outcome" if path == MCP_SKILL else "Read `outcome`"
                )
                self.assertIn(expected_outcome_reference, provider)
                self.assertIn("Do not repeat", provider)
                self.assertIn("Uncertain", provider)
                self.assertIn("status", provider)
                self.assertIn("Do not use another helper", provider)

    def test_command_and_mcp_providers_realize_the_same_helper_interface(self) -> None:
        """Keep common operations in the interface and provider mappings complete."""

        interface = INTERFACE_SKILL.read_text(encoding="utf-8")
        command = COMMAND_SKILL.read_text(encoding="utf-8")
        mcp = MCP_SKILL.read_text(encoding="utf-8")
        operation_headings = (
            "Read Claim Status",
            "Acquire Claim",
            "Extend Claim",
            "Extend Claim Deadline",
            "Heartbeat Claim",
            "Release Claim",
            "Reset Claim Registry",
            "Maintain Claim Journal",
            "Report Claim Contention",
        )
        for heading in operation_headings:
            with self.subTest(heading=heading):
                self.assertIn(heading, interface)
                self.assertIn(f"## {heading}", command)
                self.assertIn(f"## {heading}", mcp)

        for outcome in (
            "STATUS",
            "EXTENDED",
            "DEADLINE_EXTENDED",
            "HEARTBEAT",
            "RELEASED",
            "RESET",
            "INVALID_WORK_ITEM_SCOPE",
            "INVALID_WORK_ITEM_RELEASE",
        ):
            with self.subTest(outcome=outcome):
                self.assertIn(outcome, interface)

        structured_contract = _markdown_section(interface, "Structured Outcomes")
        outcome_rows = {
            cells[0]: tuple(item.strip() for item in cells[1].split(","))
            for line in structured_contract.splitlines()
            if line.startswith("| ") and not line.startswith("| Operation ")
            for cells in ([cell.strip() for cell in line.strip("|").split("|")],)
        }
        self.assertEqual(CANONICAL_OPERATION_OUTCOMES, outcome_rows)
        current_outcomes = {
            outcome
            for outcomes in outcome_rows.values()
            for outcome in outcomes
        }
        self.assertTrue(current_outcomes.isdisjoint(LEGACY_ONLY_CANONICAL_OUTCOMES))

        command_module = load_command_module()
        legacy_normalization = _markdown_section(interface, "Legacy Event Normalization")
        self.assertEqual(
            LEGACY_ONLY_CANONICAL_OUTCOMES - {"SHARED_CHECKOUT_RELEASE_REQUIRED"},
            set(command_module.LEGACY_OUTCOME_ALIASES.values()) - current_outcomes,
        )
        self.assertEqual(
            "SHARED_CHECKOUT_RELEASE_REQUIRED",
            command_module._canonical_outcome(
                "PRIMARY_REQUIRED",
                shared_checkout_claimed=True,
            ),
        )
        for legacy, canonical in command_module.LEGACY_OUTCOME_ALIASES.items():
            with self.subTest(legacy=legacy):
                self.assertIn(f"| {legacy} | {canonical} |", legacy_normalization)

        self.assertIn("--work-item-id", command)
        self.assertIn("--project-files", command)
        for command_option in ("--tree", "--backlog", "--all-files", "--branch"):
            self.assertIn(command_option, command)
        self.assertIn("claim_status", mcp)
        self.assertIn("claim_acquire", mcp)
        self.assertIn("claim_extend_deadline", mcp)
        self.assertIn("claim_reset", mcp)
        for mcp_field in ("trees", "backlog", "all_files", "branch"):
            self.assertIn(f"`{mcp_field}`", mcp)
        current_availability = _markdown_section(mcp, "Current Availability")
        self.assertIn(
            "The current mcp-agent-ops provider exposes the complete Resource Claim Helper tool surface:",
            current_availability,
        )
        for tool in REQUIRED_MCP_CLAIM_TOOLS:
            with self.subTest(tool=tool):
                self.assertIn(f"`{tool}`", current_availability)
        self.assertIn(
            "Availability in one live runtime does not prove availability in another runtime or configuration.",
            current_availability,
        )

    def test_command_work_item_contract_fixtures_match_actual_helper_results(self) -> None:
        """Execute the command contract while MCP remains documentation-only."""

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
                ["git", "-C", str(repository), "config", "user.name", "Claim Helper Test"],
                check=True,
                text=True,
                capture_output=True,
            )
            (repository / "PROJECT.yaml").write_text(
                yaml.safe_dump(project_with_helper("command"), sort_keys=False),
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
            registry_path = (
                repository / ".agent-ops" / "resource-claim" / "agent-claims.json"
            )

            def run_claim(*arguments: str) -> tuple[int, dict[str, object]]:
                completed = subprocess.run(
                    [
                        sys.executable,
                        str(COMMAND_SCRIPT),
                        "--repo",
                        str(repository),
                        *arguments,
                    ],
                    check=False,
                    text=True,
                    capture_output=True,
                )
                return completed.returncode, json.loads(completed.stdout)

            def acquire(
                claim_id: str,
                work_item_id: str,
                activity: str = "work",
            ) -> tuple[int, dict[str, object]]:
                return run_claim(
                    "acquire",
                    "--claim-id",
                    claim_id,
                    "--agent",
                    claim_id,
                    "--task",
                    f"contract {claim_id}",
                    "--root-task-id",
                    "contract-root",
                    "--work-item-id",
                    work_item_id,
                    "--activity",
                    activity,
                )

            acquire_code, acquired = acquire("owner", "item-contract")
            conflict_code, conflict = acquire("contender", "item-contract", "update")
            status_code, status = run_claim("status")
            registry_before_invalid = registry_path.read_bytes()
            invalid_acquire_code, invalid_acquire = run_claim(
                "acquire",
                "--claim-id",
                "invalid-acquire",
                "--agent",
                "invalid-acquire",
                "--task",
                "invalid acquire",
                "--root-task-id",
                "contract-root",
                "--work-item-id",
                "item-invalid",
                "--activity",
                "work",
                "--file",
                "PROJECT.yaml",
            )
            self.assertEqual(registry_before_invalid, registry_path.read_bytes())
            invalid_release_code, invalid_release = run_claim(
                "release",
                "--claim-id",
                "owner",
                "--disposition",
                "done",
                "--blocker-reference",
                "not-allowed",
            )
            self.assertEqual(registry_before_invalid, registry_path.read_bytes())
            blocked_code, blocked = run_claim(
                "release",
                "--claim-id",
                "owner",
                "--disposition",
                "blocked",
            )
            acquire("blocked-reference", "item-blocked-reference")
            blocked_reference_code, blocked_reference = run_claim(
                "release",
                "--claim-id",
                "blocked-reference",
                "--disposition",
                "blocked",
                "--blocker-reference",
                "dependency-456",
            )
            acquire("done", "item-done")
            done_code, done = run_claim(
                "release", "--claim-id", "done", "--disposition", "done"
            )
            acquire("handoff", "item-handoff")
            handoff_code, handoff = run_claim(
                "release", "--claim-id", "handoff", "--disposition", "handoff"
            )
            report_code, report = run_claim("report", "--since", "1d")

        self.assertEqual((0, "SHARED_CHECKOUT_ACQUIRED"), (acquire_code, acquired["outcome"]))
        self.assertEqual("item-contract", acquired["claim"]["work_item_id"])
        self.assertEqual("work", acquired["claim"]["activity"])
        self.assertEqual((3, "CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED"), (conflict_code, conflict["outcome"]))
        self.assertEqual(["owner"], conflict["conflicting_claim_ids"])
        self.assertEqual("work_item", conflict["overlaps"][0]["scope_kind"])
        self.assertEqual((0, "STATUS"), (status_code, status["outcome"]))
        live_claim = status["claims"][0]
        for field in (
            "work_item_id",
            "activity",
            "claim_id",
            "incarnation_id",
            "agent",
            "root_task_id",
            "claimed_at",
            "heartbeat",
            "acquisition_outcome",
        ):
            self.assertIn(field, live_claim)
        self.assertEqual((1, "INVALID_WORK_ITEM_SCOPE"), (invalid_acquire_code, invalid_acquire["outcome"]))
        self.assertEqual((1, "INVALID_WORK_ITEM_RELEASE"), (invalid_release_code, invalid_release["outcome"]))
        self.assertEqual((0, "RELEASED"), (blocked_code, blocked["outcome"]))
        self.assertEqual("blocked", blocked["disposition"])
        self.assertIsNone(blocked["blocker_reference"])
        self.assertEqual((0, "RELEASED"), (blocked_reference_code, blocked_reference["outcome"]))
        self.assertEqual("dependency-456", blocked_reference["blocker_reference"])
        self.assertEqual((0, "RELEASED"), (done_code, done["outcome"]))
        self.assertEqual((0, "RELEASED"), (handoff_code, handoff["outcome"]))
        self.assertEqual(0, report_code)
        self.assertEqual(2, report["schema_version"])
        self.assertEqual(1, report["work_items"]["schema_version"])
        report_segments = [
            segment
            for item in report["work_items"]["items"]
            for segment in item["segments"]
        ]
        for segment in report_segments:
            self.assertEqual(set(WORK_ITEM_REPORT_SEGMENT_FIELDS), set(segment))
        self.assertEqual(
            ["blocked", "blocked", "done", "handoff"],
            sorted(
                segment["disposition"]
                for item in report["work_items"]["items"]
                for segment in item["segments"]
            ),
        )
        self.assertEqual(
            {
                "missing_release_event_ids": [],
                "release_without_acquisition_event_ids": [],
                "contradictory_event_ids": [],
                "historical_non_work_item_event_ids": [],
            },
            report["work_items"]["diagnostics"],
        )

    def test_portable_command_is_owned_by_command_provider(self) -> None:
        """Ship the command implementation only with its independently distributable provider."""

        self.assertTrue(COMMAND_SCRIPT.is_file())
        self.assertFalse(LEGACY_COMMAND_SCRIPT.exists())

    def test_standard_codex_install_uses_current_user_skill_root(self) -> None:
        """Resolve the command from the current user-scope Codex bundle location."""

        command = COMMAND_SKILL.read_text(encoding="utf-8")
        self.assertIn(
            '${HOME}/.agents/skills/resource-claim-helper-command/scripts/claim.py',
            command,
        )
        self.assertNotIn('${CODEX_HOME:-$HOME/.codex}/skills', command)

    def test_mutating_eval_cases_stage_one_matching_claim_provider(self) -> None:
        """Stage shared semantics plus exactly the claim-helper interface used by each mutating fixture."""

        catalog = yaml.safe_load(CASES_PATH.read_text(encoding="utf-8"))
        cases = [
            case
            for case in catalog["cases"]
            if "resource-claim" in case.get("requiredSkills", [])
            and not case.get("readOnly", False)
        ]
        self.assertEqual(8, len(cases))
        for case in cases:
            selected = "resource-claim-helper-mcp" if "mcpAgentOps" in case else "resource-claim-helper-command"
            unused = "resource-claim-helper-command" if selected == "resource-claim-helper-mcp" else "resource-claim-helper-mcp"
            with self.subTest(case=case["id"], selected=selected):
                required = case["requiredSkills"]
                staged = case["contextPack"]["stagedSkillPackages"]
                resources = case["skillResourceAllowlist"]
                self.assertIn(selected, required)
                self.assertIn(selected, staged)
                self.assertIn("resource-claim-helper", required)
                self.assertIn("resource-claim-helper", staged)
                self.assertNotIn(unused, required)
                self.assertNotIn(unused, staged)
                self.assertEqual(["SKILL.md"], resources["resource-claim"])
                self.assertEqual(["SKILL.md"], resources["resource-claim-helper"])
                expected = (
                    ["SKILL.md"]
                    if selected == "resource-claim-helper-mcp"
                    else ["SKILL.md", "scripts/claim.py"]
                )
                self.assertEqual(expected, resources[selected])
                self.assertNotIn(unused, resources)

    def test_mcp_setup_requires_complete_schema_v2_surface(self) -> None:
        """Reject an incomplete tool surface or legacy result schema during setup."""

        incomplete = _SimulatedMcpHelper(
            tools=REQUIRED_MCP_CLAIM_TOOLS - {"claim_release"},
        )
        legacy = _SimulatedMcpHelper(result_schema_version=1)
        with self.assertRaisesRegex(RuntimeError, "CLAIM_HELPER_INCOMPLETE"):
            _run_mcp_acquire(incomplete)
        with self.assertRaisesRegex(RuntimeError, "CLAIM_HELPER_SCHEMA_UNSUPPORTED"):
            _run_mcp_acquire(legacy)

    def test_mcp_schema_v2_success_and_structured_rejection_are_authoritative(self) -> None:
        """Accept canonical success and rejection outcomes without probing another helper."""

        success = _SimulatedMcpHelper()
        rejection = _SimulatedMcpHelper(
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

        unavailable = _SimulatedMcpHelper(available=False)
        ambiguous = _SimulatedMcpHelper(ambiguous_acquire=True)
        with self.assertRaisesRegex(RuntimeError, "CLAIM_HELPER_UNAVAILABLE"):
            _run_mcp_acquire(unavailable)
        self.assertEqual([], unavailable.calls)

        self.assertEqual("STATUS", _run_mcp_acquire(ambiguous)["outcome"])
        self.assertEqual(["claim_acquire", "claim_status"], ambiguous.calls)

    def test_project_configuration_fixture_selects_its_mcp_provider(self) -> None:
        """Expose and require the provider matching the fixture's MCP claim sequence."""

        available = (
            PROJECT_CONFIGURATION_FIXTURE / "available-skills.txt"
        ).read_text(encoding="utf-8").splitlines()
        task = (PROJECT_CONFIGURATION_FIXTURE / "TASK.md").read_text(encoding="utf-8")
        self.assertIn("resource-claim-helper-mcp", available)
        self.assertIn("MCP claim-helper provider as UNAVAILABLE", task)
        self.assertIn("report BLOCKED", task)
        self.assertNotIn("record it as AVAILABLE", task)
        self.assertIn("result schema version 2", task)
        self.assertIn("Do not probe or fall back to the command-line provider", task)
        self.assertIn("Acquire one project-files claim", task)
        self.assertIn("Omit exact files", task)
        self.assertNotIn("Extend the same claim", task)

    def test_mcp_eval_contract_requires_a_supported_installed_runtime(self) -> None:
        """Require a minimum supported version without manufacturing a runtime."""

        catalog = yaml.safe_load(CASES_PATH.read_text(encoding="utf-8"))
        case = next(
            item
            for item in catalog["cases"]
            if item["id"] == "project-configuration-routing"
        )
        contract = case["mcpAgentOps"]
        self.assertEqual(4, contract["schemaVersion"])
        self.assertEqual(2, contract["claimResultSchemaVersion"])
        self.assertEqual("UNAVAILABLE", contract["claimHelperAvailability"])
        self.assertEqual("0.5.1", contract["minimumVersion"])
        enabled_tools = set(contract["enabledTools"])
        self.assertTrue(
            REQUIRED_MCP_CLAIM_TOOLS
            <= eval_validation._MCP_AGENT_OPS_TOOL_NAMES
        )
        self.assertTrue(
            REQUIRED_MCP_CLAIM_TOOLS
            <= eval_validation._MCP_AGENT_OPS_CLAIM_TOOL_NAMES
        )
        self.assertTrue(LIVE_MCP_CLAIM_TOOLS <= enabled_tools)
        self.assertNotIn("claim_extend_deadline", enabled_tools)
        self.assertNotIn("claim_reset", enabled_tools)
        self.assertFalse(REQUIRED_MCP_CLAIM_TOOLS <= enabled_tools)
        self.assertEqual(
            {"claim_extend_deadline", "claim_reset"},
            REQUIRED_MCP_CLAIM_TOOLS - enabled_tools,
        )
        self.assertEqual("UNRESOLVED_EXTERNAL_PROVIDER", MCP_DEADLINE_PARITY)
        self.assertEqual(
            ["SHARED_CHECKOUT_ACQUIRED"],
            contract["requiredToolOutcomes"]["claim_acquire"],
        )
        self.assertTrue(contract["requiredToolArguments"]["claim_acquire"]["project_files"])
        self.assertNotIn("files", contract["requiredToolArguments"]["claim_acquire"])
        self.assertNotIn("claim_extend", contract["requiredToolOutcomes"])
        self.assertNotIn("claim_extend", contract["requiredToolArguments"])


if __name__ == "__main__":
    unittest.main()
