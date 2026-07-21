#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies deterministic claim-transport setup, rendering, invocation behavior, and evaluation staging.

from __future__ import annotations

import importlib.util
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
MCP_CLAIM_TOOLS = frozenset({
    "claim_status",
    "claim_acquire",
    "claim_extend",
    "claim_heartbeat",
    "claim_release",
    "claim_maintain_journal",
    "claim_report",
})
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
    """Provide deterministic schema-v2 claim results and a complete-tool setup probe."""

    def __init__(
        self,
        *,
        available: bool = True,
        tools: frozenset[str] = MCP_CLAIM_TOOLS,
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

    def verify_setup(self) -> None:
        """Reject unavailable, incomplete, or noncanonical MCP claim surfaces."""

        if not self.available:
            raise RuntimeError("CLAIM_TRANSPORT_UNAVAILABLE")
        if self.tools != MCP_CLAIM_TOOLS:
            raise RuntimeError("CLAIM_TRANSPORT_INCOMPLETE")
        if self.result_schema_version != 2:
            raise RuntimeError("CLAIM_TRANSPORT_SCHEMA_UNSUPPORTED")

    def call(self, tool: str) -> dict[str, object]:
        """Record one simulated MCP call and return its configured structured result."""

        if tool not in self.tools:
            raise AssertionError(f"unexpected MCP tool: {tool}")
        self.calls.append(tool)
        if tool == "claim_acquire" and self.ambiguous_acquire:
            raise _AmbiguousDispatch("response lost after dispatch")
        if tool == "claim_status":
            return {
                "exit_code": 0,
                "result": {"schema_version": 2, "outcome": "STATUS"},
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
        response = transport.call("claim_acquire")
    except _AmbiguousDispatch:
        response = transport.call("claim_status")
    result = _canonical_mcp_result(response)
    outcome = result.get("outcome")
    if outcome != "STATUS" and outcome not in CANONICAL_ACQUIRE_OUTCOMES:
        raise RuntimeError("CLAIM_TRANSPORT_OUTCOME_UNSUPPORTED")
    return result


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

                self.assertIn("## Agent Claim Transport", rendered)
                self.assertIn(
                    f"BEGIN INLINED CLAIM TRANSPORT SKILL: {included}",
                    rendered,
                )
                self.assertNotIn(excluded, rendered)
                self.assertIn("does not probe or switch to another transport", rendered)

    def test_renderer_rejects_missing_or_unavailable_transport(self) -> None:
        """Fail deterministically until Project Configurator records an available transport."""

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
        self.assertEqual(6, len(cases))
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
            tools=MCP_CLAIM_TOOLS - {"claim_release"},
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
        self.assertTrue(MCP_CLAIM_TOOLS <= set(contract["enabledTools"]))
        self.assertEqual(
            ["SHARED_CHECKOUT_ACQUIRED"],
            contract["requiredToolOutcomes"]["claim_acquire"],
        )


if __name__ == "__main__":
    unittest.main()
