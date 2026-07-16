# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Builds Codex and Junie CLI invocations and normalizes their captured event streams.

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import tempfile
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Iterable, Mapping, Sequence

from .commands import CommandSpec


SUPPORTED_HARNESSES = frozenset({"codex", "junie"})
CODEX_OUTPUT_SCHEMA_SHA256 = "36bd63a02034627ab2798a424f8915bf288265846af6e2aad5f7ec18e424c8fc"
_MAX_EVENT_STREAM_BYTES = 10 * 1024 * 1024
_MAX_MCP_AUDIT_BYTES = 2 * 1024 * 1024
_MCP_STARTUP_TIMEOUT_SECONDS = 15.0
_MCP_TOOL_TIMEOUT_SECONDS = 60.0
_CODEX_NONINTERACTIVE_APPROVAL_POLICY = "never"
_CODEX_EVAL_PERMISSION_PROFILE_NAME = "mcp-eval-git-write"
_CODEX_EVAL_PERMISSION_PROFILE_DESCRIPTION = (
    "Disposable MCP evaluation workspace with Git metadata writes"
)
_CODEX_MCP_AGENT_OPS_ENABLED_TOOLS = (
    "claim_status",
    "claim_acquire",
    "claim_extend",
    "claim_heartbeat",
    "claim_release",
    "skill_list",
    "skill_resource_load",
    "detect_technology_skills",
    "verify_yaml",
    "verify_markdown_links",
)


@dataclass(frozen=True)
class HarnessIdentity:
    """Record the concrete harness executable, version, and content digest used by a run."""

    harness: str
    executable: Path
    version: str
    content_digest: str


@dataclass(frozen=True)
class McpAgentOpsIdentity:
    """Record the pinned MCP executable, package version, and executable digest."""

    executable: Path
    version: str
    launcher_digest: str
    runtime_digest: str
    identity_digest: str


@dataclass(frozen=True)
class McpAgentOpsContext:
    """Describe one isolated evaluator-owned mcp-agent-ops host configuration."""

    server_name: str
    identity: McpAgentOpsIdentity
    skill_root: Path
    detection_registry: Path
    workspace_root: Path
    audit_log: Path
    audit_root: Path
    audit_session_id: str
    configuration_digest: str
    catalog_manifest_digest: str
    configuration_evidence: Path
    catalog_evidence: Path
    evidence_directory: Path
    host_home: Path
    authorization_digest: str | None = None
    authorization_evidence: Path | None = None
    config_location: Path | None = None


def mcp_agent_ops_configuration_payload(
    harness: str,
    server_config: Mapping[str, object],
    *,
    workspace_root: Path | None = None,
    evidence_root: Path | None = None,
    host_home: Path | None = None,
) -> dict[str, object]:
    """Return the complete canonical host configuration represented by one run."""
    if harness not in SUPPORTED_HARNESSES:
        raise ValueError(f"supported harness values are codex and junie, not {harness}")
    server = dict(server_config)
    if harness == "codex":
        if workspace_root is None or evidence_root is None or host_home is None:
            raise ValueError(
                "Codex MCP configuration requires workspace, evidence, and host-home roots"
            )
        server.update({
            "enabled": True,
            "required": True,
            "enabled_tools": list(_CODEX_MCP_AGENT_OPS_ENABLED_TOOLS),
            "default_tools_approval_mode": "approve",
            "startup_timeout_sec": _MCP_STARTUP_TIMEOUT_SECONDS,
            "tool_timeout_sec": _MCP_TOOL_TIMEOUT_SECONDS,
        })
        return {
            "approval_policy": _CODEX_NONINTERACTIVE_APPROVAL_POLICY,
            "default_permissions": _CODEX_EVAL_PERMISSION_PROFILE_NAME,
            "permissions": {
                _CODEX_EVAL_PERMISSION_PROFILE_NAME: (
                    _codex_eval_permission_profile_payload(
                        workspace_root,
                        evidence_root,
                        host_home,
                    )
                )
            },
            "mcp_servers": {"mcp-agent-ops": server},
        }
    return {"mcpServers": {"mcp-agent-ops": server}}


def _codex_eval_permission_profile_payload(
    workspace_root: Path,
    evidence_root: Path,
    host_home: Path,
) -> dict[str, object]:
    """Return the exact least-privilege profile used by the synthetic Git lifecycle case."""

    workspace = workspace_root.resolve()
    evidence = evidence_root.resolve()
    home = host_home.resolve()
    if not workspace.is_absolute() or not evidence.is_absolute() or not home.is_absolute():
        raise ValueError("Codex evaluation permission roots must be absolute")
    return {
        "description": _CODEX_EVAL_PERMISSION_PROFILE_DESCRIPTION,
        "filesystem": {
            ":root": "read",
            ":tmpdir": "write",
            str(home): "deny",
            str(evidence): "deny",
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


def junie_mcp_agent_ops_authorization_payload() -> dict[str, object]:
    """Return the narrow noninteractive policy for the one staged Junie MCP server."""
    return {
        "defaultBehavior": "ask",
        "allowReadonlyCommands": True,
        "rules": {
            "fileEditing": {"rules": []},
            "executables": {
                "rules": [
                    {"prefix": "git add", "action": "allow"},
                    {"prefix": "git commit", "action": "allow"},
                ]
            },
            "mcpTools": {
                "rules": [
                    {
                        "pattern": f"mcp-agent-ops:{tool}",
                        "action": "allow",
                    }
                    for tool in _CODEX_MCP_AGENT_OPS_ENABLED_TOOLS
                ]
            },
            "readOutsideProject": {"rules": []},
        },
    }


def build_harness_command(
    harness: str,
    workspace: Path,
    agent_id: str,
    prompt: str,
    model: str,
    *,
    read_only: bool,
    event_output: Path,
    evidence_root: Path,
    isolated_config_root: Path | None = None,
    output_schema: Path | None = None,
    last_message_output: Path | None = None,
    cache_dir: Path | None = None,
    skill_locations: Sequence[Path] = (),
    agent_locations: Sequence[Path] = (),
    approved_environment_names: Sequence[str] = (),
    harness_executable: Path | None = None,
    mcp_agent_ops: McpAgentOpsContext | None = None,
    codex_home: Path | None = None,
) -> CommandSpec:
    """Build a noninteractive Codex or Junie invocation without executing it.

    Agent naming in the task is a routing request, not proof of attribution. Captured events must
    contain a matching agent-start event before attribution can be marked verified.
    """

    if harness not in SUPPORTED_HARNESSES:
        raise ValueError(f"supported harness values are codex and junie, not {harness}")
    workspace = workspace.resolve()
    if evidence_root.is_symlink():
        raise ValueError("runner-owned evidence root must be an existing non-symlink directory")
    evidence_root = evidence_root.resolve()
    if not evidence_root.is_dir():
        raise ValueError("runner-owned evidence root must be an existing non-symlink directory")
    if (
        evidence_root == workspace
        or workspace in evidence_root.parents
        or evidence_root in workspace.parents
    ):
        raise ValueError("runner-owned evidence root must be disjoint from the product workspace")
    event_output = _runner_owned_output_path(
        event_output,
        evidence_root,
        workspace,
        "harness event output",
    )
    resolved_last_message_output = (
        _runner_owned_output_path(
            last_message_output,
            evidence_root,
            workspace,
            "harness final-response output",
        )
        if last_message_output is not None
        else None
    )
    if isolated_config_root is None:
        raise ValueError("isolated_config_root is required to prevent user-home agent and skill contamination")
    isolated_config_root = isolated_config_root.resolve()
    if isolated_config_root != workspace:
        raise ValueError("isolated_config_root must be the disposable workspace context overlay root")
    approved_environment = _approved_environment_names(approved_environment_names)
    executable = _validated_harness_executable(harness, harness_executable)
    if mcp_agent_ops is not None:
        _validate_mcp_agent_ops_context(mcp_agent_ops, workspace, isolated_config_root)
    controlled_environment = {
        "HOME": str(workspace / ".eval-context" / "home"),
        "TMPDIR": str(event_output.parent / f".eval-tmp-{workspace.name}"),
    }
    if harness == "codex":
        expected_agent = isolated_config_root / ".codex" / "agents" / f"{agent_id}.toml"
        expected_skills = isolated_config_root / ".agents" / "skills"
        if not expected_agent.is_file() or not expected_skills.is_dir():
            raise ValueError("Codex isolated context must contain the selected project agent and skill locations")
        if codex_home is not None:
            resolved_codex_home = _runner_owned_output_path(
                codex_home,
                evidence_root,
                workspace,
                "isolated Codex authentication home",
            )
            controlled_environment["CODEX_HOME"] = str(resolved_codex_home)
        argv = [
            executable,
            "exec",
            "--ignore-user-config",
        ]
        if mcp_agent_ops is None:
            argv.extend((
                "--sandbox",
                "read-only" if read_only else "workspace-write",
            ))
        elif read_only:
            raise ValueError("the MCP Git-lifecycle permission profile requires a mutation case")
        argv.extend((
            "-C",
            str(workspace),
            "--model",
            model,
            "--json",
        ))
        if output_schema is not None:
            resolved_schema = validate_codex_output_schema(output_schema, workspace)
            argv.extend(["--output-schema", str(resolved_schema)])
        if resolved_last_message_output is not None:
            argv.extend(["--output-last-message", str(resolved_last_message_output)])
        if mcp_agent_ops is not None:
            _append_codex_mcp_configuration(argv, mcp_agent_ops)
        argv.append(_delegation_prompt(agent_id, prompt))
        return CommandSpec(
            tuple(argv),
            environment=controlled_environment,
            inherit_environment=False,
            host_environment_allowlist=("PATH", *approved_environment),
        )

    if codex_home is not None:
        raise ValueError("isolated Codex authentication home is valid only for Codex")
    controlled_environment["JUNIE_HOME"] = str(
        event_output.parent / f".junie-home-{workspace.name}"
    )
    if cache_dir is not None:
        resolved_cache = _runner_owned_output_path(
            cache_dir,
            evidence_root,
            workspace,
            "Junie cache_dir",
        )
    else:
        resolved_cache = _runner_owned_output_path(
            evidence_root / ".junie-cache",
            evidence_root,
            workspace,
            "Junie cache_dir",
        )
    if not skill_locations or not agent_locations:
        raise ValueError("Junie requires explicit isolated skill and agent locations")
    for location in [*skill_locations, *agent_locations]:
        resolved_location = location.resolve()
        if resolved_location != isolated_config_root and isolated_config_root not in resolved_location.parents:
            raise ValueError("Junie skill and agent locations must stay inside the isolated context root")
    argv = [
        executable,
        f"--project={workspace}",
        "--output-format=json-stream",
        f"--json-output-file={event_output}",
        f"--cache-dir={resolved_cache}",
        "--skip-update-check",
        "--config-default-locations=false",
        "--model-default-locations=false",
        "--mcp-default-locations=false",
        "--skill-default-locations=false",
        "--agent-default-location=false",
        "--command-default-location=false",
        f"--extensions-default-location={isolated_config_root / '.junie' / 'extensions'}",
        f"--model={model}",
    ]
    argv.extend(f"--skill-location={path.resolve()}" for path in skill_locations)
    argv.extend(f"--agent-location={path.resolve()}" for path in agent_locations)
    if mcp_agent_ops is not None:
        if mcp_agent_ops.config_location is None:
            raise ValueError("Junie MCP context requires one explicit configuration location")
        argv.append(f"--mcp-location={mcp_agent_ops.config_location.resolve()}")
    argv.append(f"--task={_delegation_prompt(agent_id, prompt)}")
    return CommandSpec(
        tuple(argv),
        environment=controlled_environment,
        inherit_environment=False,
        host_environment_allowlist=("PATH", *approved_environment),
    )


def validate_codex_output_schema(path: Path, workspace: Path | None = None) -> Path:
    """Accept only the governed JSON Schema bytes used by Codex evaluations."""

    if path.is_symlink():
        raise ValueError("output schema must be the canonical evaluator-owned Codex JSON Schema")
    resolved = path.resolve()
    if not resolved.is_file() or resolved.suffix != ".json":
        raise ValueError("output schema must be the canonical evaluator-owned Codex JSON Schema")
    if workspace is not None:
        resolved_workspace = workspace.resolve()
        if resolved == resolved_workspace or resolved_workspace in resolved.parents:
            raise ValueError("output schema must be the canonical evaluator-owned Codex JSON Schema")
    try:
        value = json.loads(resolved.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError("output schema must be valid evaluator-owned JSON Schema") from error
    if (
        not isinstance(value, Mapping)
        or value.get("$schema") != "https://json-schema.org/draft/2020-12/schema"
        or value.get("type") != "object"
        or hashlib.sha256(resolved.read_bytes()).hexdigest()
        != CODEX_OUTPUT_SCHEMA_SHA256
    ):
        raise ValueError("output schema must be the canonical evaluator-owned Codex JSON Schema")
    return resolved


def _runner_owned_output_path(
    path: Path,
    evidence_root: Path,
    workspace: Path,
    label: str,
) -> Path:
    """Resolve one output path beneath the disjoint runner-owned evidence root."""

    if path.is_symlink():
        raise ValueError(f"{label} must not be a symlink")
    resolved = path.resolve()
    if resolved == evidence_root or evidence_root not in resolved.parents:
        raise ValueError(f"{label} must stay beneath the runner-owned evidence root")
    if resolved == workspace or workspace in resolved.parents:
        raise ValueError(f"{label} must be outside the product workspace")
    return resolved


def normalize_harness_events(harness: str, lines: Iterable[str]) -> list[dict[str, object]]:
    """Normalize captured JSON Lines while retaining raw event identity and payload digests."""

    if harness not in SUPPORTED_HARNESSES:
        raise ValueError(f"supported harness values are codex and junie, not {harness}")
    normalized: list[dict[str, object]] = []
    for sequence, line in enumerate(lines, start=1):
        try:
            raw = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(raw, Mapping):
            continue
        event = _normalize_event(harness, sequence, raw)
        normalized.append(event)
    return normalized


def read_harness_event_stream(
    harness: str, path: Path
) -> list[dict[str, object]]:
    """Read a complete non-empty JSON Lines event stream without silently dropping records."""

    if harness not in SUPPORTED_HARNESSES:
        raise ValueError(f"supported harness values are codex and junie, not {harness}")
    if path.is_symlink():
        raise ValueError(
            f"captured {harness} event stream must be a regular non-symlink file"
        )
    if not path.is_file():
        raise ValueError(f"captured {harness} event stream is missing: {path}")
    if path.stat().st_size > _MAX_EVENT_STREAM_BYTES:
        raise ValueError(
            f"captured {harness} event stream exceeds the configured capture limit"
        )
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as error:
        raise ValueError(f"captured {harness} event stream is unreadable: {error}") from error
    records: list[dict[str, object]] = []
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValueError(
                f"captured {harness} event stream line {line_number} is invalid JSON"
            ) from error
        if not isinstance(value, dict):
            raise ValueError(
                f"captured {harness} event stream line {line_number} must be a JSON object"
            )
        records.append(value)
    if not records:
        raise ValueError(f"captured {harness} event stream is empty")
    return records


def read_mcp_agent_ops_audit(path: Path) -> list[dict[str, object]]:
    """Read and validate one digest-only mcp-agent-ops tool lifecycle audit."""
    if path.is_symlink() or not path.is_file():
        raise ValueError("captured MCP tool audit must be a regular non-symlink file")
    if path.stat().st_size > _MAX_MCP_AUDIT_BYTES:
        raise ValueError("captured MCP tool audit exceeds the configured capture limit")
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as error:
        raise ValueError("captured MCP tool audit is unreadable") from error
    records: list[dict[str, object]] = []
    allowed_fields = {
        "schema",
        "version",
        "sequence",
        "callId",
        "tool",
        "status",
        "argumentsDigest",
        "resultDigest",
        "streamId",
        "sessionId",
        "outcome",
    }
    for line_number, line in enumerate(lines, start=1):
        try:
            record = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValueError(f"captured MCP tool audit line {line_number} is invalid JSON") from error
        if not isinstance(record, dict):
            raise ValueError(f"captured MCP tool audit line {line_number} must be a JSON object")
        if set(record) - allowed_fields:
            raise ValueError(f"captured MCP tool audit line {line_number} contains forbidden fields")
        version = record.get("version")
        if (
            record.get("schema") != "mcp-agent-ops-tool-audit"
            or version not in {1, 2}
            or not isinstance(record.get("sequence"), int)
            or isinstance(record.get("sequence"), bool)
            or int(record["sequence"]) < 1
            or not isinstance(record.get("callId"), str)
            or not re.fullmatch(
                r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}",
                str(record.get("callId")),
            )
            or not isinstance(record.get("tool"), str)
            or not re.fullmatch(r"[a-z][a-z0-9_]*", str(record.get("tool")))
            or record.get("status") not in {"started", "completed", "failed"}
        ):
            raise ValueError(f"captured MCP tool audit line {line_number} has an invalid contract")
        if version == 1:
            if (
                record["sequence"] != line_number
                or "streamId" in record
                or "sessionId" in record
                or "outcome" in record
            ):
                raise ValueError(
                    f"captured MCP tool audit line {line_number} has invalid version-one evidence"
                )
        elif (
            not isinstance(record.get("streamId"), str)
            or not re.fullmatch(r"[0-9a-f]{32}", str(record.get("streamId")))
            or not isinstance(record.get("sessionId"), str)
            or not re.fullmatch(r"[0-9a-f]{32}", str(record.get("sessionId")))
        ):
            raise ValueError(
                f"captured MCP tool audit line {line_number} has invalid shared-stream evidence"
            )
        digest_field = "argumentsDigest" if record["status"] == "started" else "resultDigest"
        other_digest = "resultDigest" if digest_field == "argumentsDigest" else "argumentsDigest"
        if (
            not isinstance(record.get(digest_field), str)
            or not re.fullmatch(r"[0-9a-f]{64}", str(record[digest_field]))
            or other_digest in record
        ):
            raise ValueError(f"captured MCP tool audit line {line_number} has invalid digest evidence")
        outcome = record.get("outcome")
        if record["status"] == "started" and outcome is not None:
            raise ValueError(
                f"captured MCP tool audit line {line_number} has an outcome before completion"
            )
        if outcome is not None and (
            not isinstance(outcome, str)
            or not re.fullmatch(r"[A-Z][A-Z0-9_]{0,63}", outcome)
        ):
            raise ValueError(
                f"captured MCP tool audit line {line_number} has an invalid outcome"
            )
        records.append(record)
    if not records:
        raise ValueError("captured MCP tool audit is empty")
    versions = {int(record["version"]) for record in records}
    if len(versions) != 1:
        raise ValueError("captured MCP tool audit mixes incompatible schema versions")
    if versions == {2}:
        sessions = {str(record["sessionId"]) for record in records}
        if len(sessions) != 1:
            raise ValueError("captured MCP tool audit mixes evaluation session identities")
        next_sequence: dict[str, int] = {}
        for record in records:
            stream_id = str(record["streamId"])
            expected = next_sequence.get(stream_id, 1)
            if record["sequence"] != expected:
                raise ValueError(
                    "captured MCP tool audit has a non-contiguous process-local sequence"
                )
            next_sequence[stream_id] = expected + 1
    started: dict[tuple[str, str], str] = {}
    terminal: set[tuple[str, str]] = set()
    for record in records:
        stream_id = str(record.get("streamId", "version-one"))
        call_id = str(record["callId"])
        identity = (stream_id, call_id)
        tool = str(record["tool"])
        if record["status"] == "started":
            if identity in started:
                raise ValueError("captured MCP tool audit repeats a started call identity")
            started[identity] = tool
        elif (
            identity not in started
            or identity in terminal
            or started[identity] != tool
        ):
            raise ValueError("captured MCP tool audit has an unmatched terminal record")
        else:
            terminal.add(identity)
    if terminal != set(started):
        raise ValueError("captured MCP tool audit has an incomplete tool lifecycle")
    if any(record["status"] == "failed" for record in records):
        raise ValueError("captured MCP tool audit contains a failed tool call")
    return records


def completed_mcp_tool_sequence(records: Sequence[Mapping[str, object]]) -> list[str]:
    """Return the single completed stream, rejecting ambiguous shared audits."""
    streams = completed_mcp_tool_streams(records)
    if len(streams) != 1:
        raise ValueError("captured MCP tool audit contains multiple process streams")
    return streams[0]


def completed_mcp_tool_streams(
    records: Sequence[Mapping[str, object]],
) -> list[list[str]]:
    """Return completed tool names grouped by process stream in first-seen order."""
    ordered_streams: list[str] = []
    tools_by_stream: dict[str, list[str]] = {}
    for record in records:
        stream_id = str(record.get("streamId", "version-one"))
        if stream_id not in tools_by_stream:
            ordered_streams.append(stream_id)
            tools_by_stream[stream_id] = []
        if record.get("status") == "completed":
            tools_by_stream[stream_id].append(str(record["tool"]))
    return [tools_by_stream[stream_id] for stream_id in ordered_streams]


def completed_mcp_tool_outcomes(
    records: Sequence[Mapping[str, object]],
) -> list[dict[str, list[str]]]:
    """Return bounded terminal outcomes grouped by process stream and tool."""
    ordered_streams: list[str] = []
    outcomes_by_stream: dict[str, dict[str, list[str]]] = {}
    for record in records:
        stream_id = str(record.get("streamId", "version-one"))
        if stream_id not in outcomes_by_stream:
            ordered_streams.append(stream_id)
            outcomes_by_stream[stream_id] = {}
        if record.get("status") != "completed" or not isinstance(record.get("outcome"), str):
            continue
        tool = str(record["tool"])
        outcomes_by_stream[stream_id].setdefault(tool, []).append(str(record["outcome"]))
    return [outcomes_by_stream[stream_id] for stream_id in ordered_streams]


def completed_mcp_tool_calls(
    records: Sequence[Mapping[str, object]],
) -> list[list[dict[str, str | None]]]:
    """Return completed calls with their privacy-safe argument digests by stream."""

    ordered_streams = mcp_audit_stream_ids(records)
    calls_by_stream: dict[str, list[dict[str, str | None]]] = {
        stream_id: [] for stream_id in ordered_streams
    }
    started_arguments: dict[tuple[str, str], str] = {}
    for record in records:
        stream_id = str(record.get("streamId", "version-one"))
        call_id = str(record["callId"])
        identity = (stream_id, call_id)
        if record.get("status") == "started":
            started_arguments[identity] = str(record["argumentsDigest"])
        elif record.get("status") == "completed":
            calls_by_stream[stream_id].append({
                "tool": str(record["tool"]),
                "argumentsDigest": started_arguments[identity],
                "outcome": (
                    str(record["outcome"])
                    if isinstance(record.get("outcome"), str)
                    else None
                ),
            })
    return [calls_by_stream[stream_id] for stream_id in ordered_streams]


def mcp_audit_stream_ids(records: Sequence[Mapping[str, object]]) -> list[str]:
    """Return process stream identities in first-seen order."""
    streams: list[str] = []
    for record in records:
        stream_id = str(record.get("streamId", "version-one"))
        if stream_id not in streams:
            streams.append(stream_id)
    return streams


def select_mcp_tool_stream(
    records: Sequence[Mapping[str, object]],
    required_sequences: Sequence[Sequence[str]],
    required_outcomes: Mapping[str, Sequence[str]],
    required_argument_digests: Mapping[str, str] | None = None,
) -> tuple[str, list[str], dict[str, list[str]]]:
    """Select the one process stream that satisfies the complete tool contract."""
    stream_ids = mcp_audit_stream_ids(records)
    tool_streams = completed_mcp_tool_streams(records)
    outcome_streams = completed_mcp_tool_outcomes(records)
    call_streams = completed_mcp_tool_calls(records)
    candidates: list[tuple[str, list[str], dict[str, list[str]]]] = []
    for stream_id, tools, outcomes, calls in zip(
        stream_ids,
        tool_streams,
        outcome_streams,
        call_streams,
        strict=True,
    ):
        sequences_match = (
            all(
                required_mcp_calls_are_subsequence(
                    sequence,
                    calls,
                    required_argument_digests,
                    required_outcomes,
                )
                for sequence in required_sequences
            )
            if required_argument_digests
            else all(
                required_tools_are_subsequence(sequence, tools)
                for sequence in required_sequences
            )
        )
        if not sequences_match:
            continue
        if not all(
            set(outcomes.get(tool, ())) & set(allowed)
            for tool, allowed in required_outcomes.items()
        ):
            continue
        if required_argument_digests and not all(
            any(
                call["tool"] == tool
                and call["argumentsDigest"] == expected_digest
                and call["outcome"] in set(required_outcomes.get(tool, ()))
                for call in calls
            )
            for tool, expected_digest in required_argument_digests.items()
        ):
            continue
        candidates.append((stream_id, tools, outcomes))
    if not candidates:
        raise ValueError(
            "captured MCP tool audit has no process stream satisfying required sequences and outcomes"
        )
    if len(candidates) != 1:
        raise ValueError(
            "captured MCP tool audit has multiple process streams satisfying the run contract"
        )
    return candidates[0]


def required_mcp_calls_are_subsequence(
    required: Sequence[str],
    observed: Sequence[Mapping[str, str | None]],
    required_argument_digests: Mapping[str, str],
    required_outcomes: Mapping[str, Sequence[str]],
) -> bool:
    """Return whether exact argument-and-outcome calls appear in declared order."""

    iterator = iter(observed)
    for tool in required:
        expected_digest = required_argument_digests.get(tool)
        allowed_outcomes = set(required_outcomes.get(tool, ()))
        if expected_digest is None or not allowed_outcomes:
            return False
        if not any(
            call.get("tool") == tool
            and call.get("argumentsDigest") == expected_digest
            and call.get("outcome") in allowed_outcomes
            for call in iterator
        ):
            return False
    return True


def resolve_mcp_tool_argument_digests(
    required_arguments: Mapping[str, object],
    workspace: Path,
) -> dict[str, str]:
    """Resolve the workspace sentinel and digest exact JSON-compatible tool arguments."""

    resolved_workspace = workspace.resolve()
    if not resolved_workspace.is_absolute():
        raise ValueError("MCP tool argument workspace must be absolute")

    def resolve(value: object) -> object:
        if value == "$WORKSPACE":
            return str(resolved_workspace)
        if isinstance(value, str):
            if "$WORKSPACE" in value:
                raise ValueError("MCP tool argument workspace sentinel must occupy the complete value")
            if re.fullmatch(r"\$[A-Z][A-Z0-9_]*", value):
                raise ValueError(f"unknown MCP tool argument placeholder: {value}")
            return value
        if isinstance(value, Mapping):
            if any(not isinstance(key, str) for key in value):
                raise ValueError("MCP tool argument mappings require string keys")
            return {str(key): resolve(child) for key, child in value.items()}
        if isinstance(value, list):
            return [resolve(child) for child in value]
        if value is None or isinstance(value, (bool, int, float)):
            return value
        raise ValueError("MCP tool arguments must contain only JSON-compatible values")

    digests: dict[str, str] = {}
    for tool, arguments in required_arguments.items():
        if not isinstance(tool, str) or not re.fullmatch(r"[a-z][a-z0-9_]*", tool):
            raise ValueError("MCP required tool argument keys must be normalized tool names")
        if not isinstance(arguments, Mapping):
            raise ValueError(f"MCP required tool arguments for {tool} must be a mapping")
        digests[tool] = mcp_value_digest(resolve(arguments))
    if not digests:
        raise ValueError("MCP required tool arguments must not be empty")
    return digests


def mcp_value_digest(value: object) -> str:
    """Return the MCP audit protocol's canonical JSON digest for a safe value."""

    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def required_tools_are_subsequence(
    required: Sequence[str],
    observed: Sequence[str],
) -> bool:
    """Return whether every required tool appears in order within observed calls."""
    iterator = iter(observed)
    return all(any(candidate == tool for candidate in iterator) for tool in required)


def extract_harness_final_response(
    harness: str, events: Sequence[Mapping[str, object]]
) -> str:
    """Extract the final review document from one supported harness event stream."""

    if harness != "junie":
        raise ValueError("Codex final responses are captured with --output-last-message")
    result_events = [event for event in events if event.get("type") == "result"]
    if not result_events:
        raise ValueError("captured Junie event stream has no final result event")
    if len(result_events) != 1:
        raise ValueError("captured Junie event stream must contain exactly one result event")
    if events[-1] is not result_events[0]:
        raise ValueError("captured Junie result event must be terminal")
    result = result_events[0].get("result")
    if not isinstance(result, str) or not result.strip():
        raise ValueError("captured Junie final result must be a non-empty string")
    return result


def agent_attribution_verified(
    events: Iterable[Mapping[str, object]],
    agent_id: str,
    effective_adapter_digest: str | None = None,
) -> bool:
    """Return whether a normalized event explicitly starts the intended agent identity."""

    return any(
        event.get("type") == "agent-start"
        and event.get("agent") == agent_id
        and (
            effective_adapter_digest is None
            or event.get("contentDigest") == effective_adapter_digest
        )
        for event in events
    )


@lru_cache(maxsize=2)
def capture_harness_identity(harness: str) -> HarnessIdentity:
    """Capture a supported CLI identity without starting an agent or paid model session."""

    if harness not in SUPPORTED_HARNESSES:
        raise ValueError(f"supported harness values are codex and junie, not {harness}")
    executable_name = shutil.which(harness)
    if executable_name is None:
        raise RuntimeError(f"harness executable is not installed: {harness}")
    executable = _resolve_harness_executable(harness, Path(executable_name))
    with tempfile.TemporaryDirectory(prefix=f"dev-methodology-{harness}-identity-") as directory:
        identity_root = Path(directory)
        home = identity_root / "home"
        scratch = identity_root / "tmp"
        home.mkdir()
        scratch.mkdir()
        environment = {
            "HOME": str(home),
            "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
            "TMPDIR": str(scratch),
        }
        for name in ("LANG", "LC_ALL"):
            if name in os.environ:
                environment[name] = os.environ[name]
        if harness == "junie":
            junie_home = identity_root / "junie-home"
            junie_home.mkdir()
            environment["JUNIE_HOME"] = str(junie_home)
        completed = subprocess.run(
            [str(executable), "--version"],
            capture_output=True,
            text=True,
            check=False,
            env=environment,
        )
    if completed.returncode != 0:
        raise RuntimeError(f"unable to capture {harness} version: {completed.stderr.strip()}")
    return HarnessIdentity(
        harness=harness,
        executable=executable,
        version=completed.stdout.strip(),
        content_digest=hashlib.sha256(executable.read_bytes()).hexdigest(),
    )


def capture_mcp_agent_ops_identity(
    executable: Path | None = None,
    *,
    required_version: str | None = None,
    required_runtime_digest: str | None = None,
) -> McpAgentOpsIdentity:
    """Capture and optionally enforce launcher and installed-runtime identity."""
    discovered = executable or (
        Path(value) if (value := shutil.which("mcp-agent-ops")) is not None else None
    )
    if discovered is None:
        raise RuntimeError("mcp-agent-ops executable is not installed")
    resolved = discovered.expanduser().resolve()
    if not resolved.is_file() or not resolved.stat().st_mode & 0o111:
        raise ValueError("mcp-agent-ops executable must be an executable file")
    launcher_before = hashlib.sha256(resolved.read_bytes()).hexdigest()
    with tempfile.TemporaryDirectory(prefix="dev-methodology-mcp-agent-ops-identity-") as directory:
        scratch = Path(directory)
        environment = {
            "HOME": str(scratch / "home"),
            "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
            "TMPDIR": str(scratch / "tmp"),
        }
        Path(environment["HOME"]).mkdir()
        Path(environment["TMPDIR"]).mkdir()
        try:
            version_probe = subprocess.run(
                [str(resolved), "--version"],
                capture_output=True,
                text=True,
                check=False,
                timeout=10,
                env=environment,
            )
            runtime_probe = subprocess.run(
                [str(resolved), "--identity-json"],
                capture_output=True,
                text=True,
                check=False,
                timeout=10,
                env=environment,
            )
        except (OSError, subprocess.TimeoutExpired) as error:
            raise RuntimeError("unable to execute mcp-agent-ops identity probes") from error
    launcher_after = hashlib.sha256(resolved.read_bytes()).hexdigest()
    if launcher_before != launcher_after:
        raise RuntimeError("mcp-agent-ops launcher changed during identity capture")
    version_identity = version_probe.stdout.strip()
    if (
        version_probe.returncode != 0
        or version_probe.stderr
        or not re.fullmatch(
            r"mcp-agent-ops \d+\.\d+\.\d+(?:[-+][A-Za-z0-9.-]+)?",
            version_identity,
        )
    ):
        raise RuntimeError("unable to capture mcp-agent-ops package version")
    try:
        runtime_identity = json.loads(runtime_probe.stdout)
    except json.JSONDecodeError as error:
        raise RuntimeError("unable to capture mcp-agent-ops runtime identity") from error
    expected_fields = {
        "schema",
        "schemaVersion",
        "package",
        "packageVersion",
        "runtimeDigest",
        "fileCount",
    }
    if (
        runtime_probe.returncode != 0
        or runtime_probe.stderr
        or not isinstance(runtime_identity, dict)
        or set(runtime_identity) != expected_fields
        or runtime_identity.get("schema") != "mcp-agent-ops-runtime-identity"
        or runtime_identity.get("schemaVersion") != 1
        or runtime_identity.get("package") != "mcp-agent-ops"
        or not isinstance(runtime_identity.get("packageVersion"), str)
        or not re.fullmatch(
            r"\d+\.\d+\.\d+(?:[-+][A-Za-z0-9.-]+)?",
            str(runtime_identity.get("packageVersion")),
        )
        or not isinstance(runtime_identity.get("runtimeDigest"), str)
        or not re.fullmatch(r"[0-9a-f]{64}", str(runtime_identity.get("runtimeDigest")))
        or not isinstance(runtime_identity.get("fileCount"), int)
        or int(runtime_identity.get("fileCount", 0)) < 1
    ):
        raise RuntimeError("unable to capture mcp-agent-ops runtime identity")
    version_value = version_identity.removeprefix("mcp-agent-ops ")
    runtime_version = str(runtime_identity["packageVersion"])
    runtime_digest = str(runtime_identity["runtimeDigest"])
    if version_value != runtime_version:
        raise RuntimeError("mcp-agent-ops identity probes report different versions")
    if required_version is not None and version_value != required_version:
        raise RuntimeError("mcp-agent-ops version does not match the evaluation contract")
    if required_runtime_digest is not None and runtime_digest != required_runtime_digest:
        raise RuntimeError("mcp-agent-ops runtime digest does not match the evaluation contract")
    identity_digest = hashlib.sha256(
        json.dumps(
            {
                "version": version_value,
                "launcherDigest": launcher_before,
                "runtimeDigest": runtime_digest,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    return McpAgentOpsIdentity(
        executable=resolved,
        version=version_value,
        launcher_digest=launcher_before,
        runtime_digest=runtime_digest,
        identity_digest=identity_digest,
    )


def _resolve_harness_executable(harness: str, discovered: Path) -> Path:
    """Resolve a managed harness shim before a run replaces HOME."""

    executable = discovered.resolve()
    if harness != "junie":
        return executable
    try:
        marker = discovered.read_text(encoding="utf-8", errors="ignore")[:4096]
    except OSError:
        return executable
    if "JUNIE_MANAGED_SHIM" not in marker:
        return executable
    data_root = Path(
        os.environ.get("JUNIE_DATA", str(Path.home() / ".local" / "share" / "junie"))
    ).expanduser()
    current = data_root / "current"
    candidates = (
        current / "Applications" / "junie.app" / "Contents" / "MacOS" / "junie",
        current / "junie" / "bin" / "junie",
        current / "junie",
    )
    for candidate in candidates:
        try:
            resolved = candidate.resolve(strict=True)
        except OSError:
            continue
        if resolved.is_file() and resolved.stat().st_mode & 0o111:
            return resolved
    raise RuntimeError(
        f"managed Junie shim has no executable current runtime beneath {data_root}"
    )


def _validated_harness_executable(
    harness: str, executable: Path | None
) -> str:
    """Return a supported executable name or a pinned absolute harness path."""

    if executable is None:
        return harness
    resolved = executable.resolve()
    if not resolved.is_file() or not resolved.stat().st_mode & 0o111:
        raise ValueError(f"{harness} harness executable must be an executable file")
    return str(resolved)


def _approved_environment_names(values: Sequence[str]) -> tuple[str, ...]:
    names: list[str] = []
    for value in values:
        if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", value):
            raise ValueError("approved environment names must be valid non-empty variable names")
        if value in {"HOME", "TMPDIR", "TEMP", "TMP"}:
            raise ValueError(f"runner-owned environment variable cannot be host-approved: {value}")
        if value not in names and value != "PATH":
            names.append(value)
    return tuple(sorted(names))


def _validate_mcp_agent_ops_context(
    context: McpAgentOpsContext,
    workspace: Path,
    isolated_config_root: Path,
) -> None:
    """Reject MCP paths that escape the disposable workspace or evidence boundary."""
    if context.server_name != "mcp-agent-ops":
        raise ValueError("evaluation MCP server name must be mcp-agent-ops")
    if context.workspace_root.resolve() != workspace:
        raise ValueError("MCP workspace root must be the disposable product workspace")
    if not re.fullmatch(r"[0-9a-f]{32}", context.audit_session_id):
        raise ValueError("MCP audit session identity must be 32 lowercase hexadecimal characters")
    skill_root = context.skill_root.resolve()
    if skill_root != isolated_config_root and isolated_config_root not in skill_root.parents:
        raise ValueError("MCP skill root must stay inside the isolated context root")
    if context.skill_root.is_symlink() or not skill_root.is_dir():
        raise ValueError("MCP skill root must be an existing non-symlink directory")
    for label, digest in (
        ("launcher", context.identity.launcher_digest),
        ("runtime", context.identity.runtime_digest),
        ("identity", context.identity.identity_digest),
        ("configuration", context.configuration_digest),
        ("catalog manifest", context.catalog_manifest_digest),
    ):
        if not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise ValueError(f"MCP {label} digest must be lowercase SHA-256")
    catalog_manifest = skill_root.parent / "catalog-manifest.json"
    if catalog_manifest.is_symlink() or not catalog_manifest.is_file():
        raise ValueError("MCP catalog manifest must stay beside the staged skill root")
    try:
        catalog_value = json.loads(catalog_manifest.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError("MCP catalog manifest must be valid evaluator-owned JSON") from error
    if (
        not isinstance(catalog_value, dict)
        or catalog_value.get("manifestDigest") != context.catalog_manifest_digest
    ):
        raise ValueError("MCP catalog manifest digest does not match its context")
    registry = context.detection_registry.resolve()
    if not registry.is_file() or skill_root not in registry.parents:
        raise ValueError("MCP detection registry must stay inside the staged skill root")
    audit_root = context.audit_root.resolve()
    audit_log = context.audit_log.resolve()
    if context.audit_root.is_symlink() or not audit_root.is_dir():
        raise ValueError("MCP audit root must be an existing non-symlink directory")
    if audit_log == audit_root or audit_root not in audit_log.parents:
        raise ValueError("MCP audit log must stay beneath its runner-owned audit root")
    if audit_root == workspace or workspace in audit_root.parents or audit_root in workspace.parents:
        raise ValueError("MCP audit root must be disjoint from the product workspace")
    if audit_log.exists() or audit_log.is_symlink():
        raise ValueError("MCP audit log must be an unused non-symlink path")
    evidence_directory = context.evidence_directory.resolve()
    if (
        context.evidence_directory.is_symlink()
        or not evidence_directory.is_dir()
        or audit_root not in evidence_directory.parents
    ):
        raise ValueError("MCP evidence directory must stay beneath its runner-owned audit root")
    if stat.S_IMODE(evidence_directory.stat().st_mode) & 0o077:
        raise ValueError("MCP evidence directory must be owner-only")
    evidence_files = {
        "configuration": context.configuration_evidence,
        "catalog": context.catalog_evidence,
    }
    if context.authorization_evidence is not None:
        evidence_files["authorization"] = context.authorization_evidence
    for label, path in evidence_files.items():
        resolved = path.resolve()
        if (
            path.is_symlink()
            or not resolved.is_file()
            or evidence_directory not in resolved.parents
        ):
            raise ValueError(f"MCP {label} evidence must stay beneath its evidence directory")
        if stat.S_IMODE(resolved.stat().st_mode) & 0o077:
            raise ValueError(f"MCP {label} evidence must be owner-only")
    if hashlib.sha256(context.configuration_evidence.read_bytes()).hexdigest() != context.configuration_digest:
        raise ValueError("MCP configuration evidence digest does not match its context")
    if context.catalog_evidence.read_bytes() != catalog_manifest.read_bytes():
        raise ValueError("MCP catalog evidence differs from the staged catalog manifest")
    if context.authorization_evidence is None:
        if context.authorization_digest is not None:
            raise ValueError("MCP authorization digest requires authorization evidence")
    elif (
        context.authorization_digest is None
        or hashlib.sha256(context.authorization_evidence.read_bytes()).hexdigest()
        != context.authorization_digest
    ):
        raise ValueError("MCP authorization evidence digest does not match its context")
    server_config = {
        "command": str(context.identity.executable),
        "args": [],
        "env": {
            "MCP_AGENT_OPS_SKILL_ROOTS": str(context.skill_root),
            "MCP_AGENT_OPS_DETECTION_REGISTRY": str(context.detection_registry),
            "MCP_AGENT_OPS_WORKSPACE_ROOTS": str(context.workspace_root),
            "MCP_AGENT_OPS_AUDIT_LOG": str(context.audit_log),
            "MCP_AGENT_OPS_AUDIT_ROOTS": str(context.audit_root),
            "MCP_AGENT_OPS_AUDIT_SHARED": "true",
            "MCP_AGENT_OPS_AUDIT_SESSION_ID": context.audit_session_id,
            "MCP_AGENT_OPS_REQUIRED_RUNTIME_DIGEST": context.identity.runtime_digest,
        },
    }
    expected_configuration = mcp_agent_ops_configuration_payload(
        "junie" if context.config_location is not None else "codex",
        server_config,
        workspace_root=context.workspace_root,
        evidence_root=context.audit_root,
        host_home=context.host_home,
    )
    try:
        recorded_configuration = json.loads(
            context.configuration_evidence.read_text(encoding="utf-8")
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError("MCP configuration evidence must be valid evaluator-owned JSON") from error
    if recorded_configuration != expected_configuration:
        raise ValueError("MCP configuration evidence differs from the effective host configuration")
    if context.config_location is not None:
        location = context.config_location.resolve()
        if (
            context.config_location.is_symlink()
            or not location.is_dir()
            or location != evidence_directory / "junie"
        ):
            raise ValueError("Junie MCP configuration must stay in its runner-owned evidence directory")
        if context.configuration_evidence.resolve() != location / "mcp.json":
            raise ValueError("Junie MCP configuration location must contain the governed mcp.json")
        if context.authorization_evidence is None:
            raise ValueError("Junie MCP execution requires evaluator-owned authorization evidence")
        try:
            authorization = json.loads(
                context.authorization_evidence.read_text(encoding="utf-8")
            )
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            raise ValueError("Junie MCP authorization evidence must be valid JSON") from error
        expected_authorization = junie_mcp_agent_ops_authorization_payload()
        if authorization != expected_authorization:
            raise ValueError("Junie MCP authorization evidence is not the narrow evaluator policy")
    elif context.authorization_evidence is not None:
        raise ValueError("Codex MCP execution must not use Junie authorization evidence")


def _append_codex_mcp_configuration(
    argv: list[str],
    context: McpAgentOpsContext,
) -> None:
    """Append one complete strict Codex stdio MCP configuration through CLI overrides."""
    prefix = f"mcp_servers.{context.server_name}"
    values: tuple[tuple[str, object], ...] = (
        ("approval_policy", _CODEX_NONINTERACTIVE_APPROVAL_POLICY),
        ("default_permissions", _CODEX_EVAL_PERMISSION_PROFILE_NAME),
        (
            f"permissions.{_CODEX_EVAL_PERMISSION_PROFILE_NAME}",
            _codex_eval_permission_profile_payload(
                context.workspace_root,
                context.audit_root,
                context.host_home,
            ),
        ),
        (f"{prefix}.enabled", True),
        (f"{prefix}.required", True),
        (f"{prefix}.enabled_tools", list(_CODEX_MCP_AGENT_OPS_ENABLED_TOOLS)),
        (f"{prefix}.default_tools_approval_mode", "approve"),
        (f"{prefix}.command", str(context.identity.executable)),
        (f"{prefix}.args", []),
        (f"{prefix}.startup_timeout_sec", _MCP_STARTUP_TIMEOUT_SECONDS),
        (f"{prefix}.tool_timeout_sec", _MCP_TOOL_TIMEOUT_SECONDS),
        (f"{prefix}.env.MCP_AGENT_OPS_SKILL_ROOTS", str(context.skill_root)),
        (f"{prefix}.env.MCP_AGENT_OPS_DETECTION_REGISTRY", str(context.detection_registry)),
        (f"{prefix}.env.MCP_AGENT_OPS_WORKSPACE_ROOTS", str(context.workspace_root)),
        (f"{prefix}.env.MCP_AGENT_OPS_AUDIT_LOG", str(context.audit_log)),
        (f"{prefix}.env.MCP_AGENT_OPS_AUDIT_ROOTS", str(context.audit_root)),
        (f"{prefix}.env.MCP_AGENT_OPS_AUDIT_SHARED", "true"),
        (f"{prefix}.env.MCP_AGENT_OPS_AUDIT_SESSION_ID", context.audit_session_id),
        (
            f"{prefix}.env.MCP_AGENT_OPS_REQUIRED_RUNTIME_DIGEST",
            context.identity.runtime_digest,
        ),
    )
    for key, value in values:
        argv.extend(("-c", f"{key}={_toml_literal(value)}"))


def _toml_literal(value: object) -> str:
    """Serialize the small evaluator-owned value subset accepted by Codex CLI overrides."""

    if isinstance(value, str):
        return json.dumps(value)
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return str(value)
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return "[" + ", ".join(_toml_literal(item) for item in value) + "]"
    if isinstance(value, Mapping):
        entries = (
            f"{json.dumps(str(key))} = {_toml_literal(item)}"
            for key, item in value.items()
        )
        return "{" + ", ".join(entries) + "}"
    raise ValueError("unsupported Codex CLI configuration value")


def _delegation_prompt(agent_id: str, prompt: str) -> str:
    if not agent_id.strip():
        raise ValueError("agent_id must be a non-empty string")
    if not prompt.strip():
        raise ValueError("prompt must be a non-empty string")
    return f"Delegate the following task to the {agent_id} subagent. {prompt}"


def _normalize_event(harness: str, sequence: int, raw: Mapping[str, object]) -> dict[str, object]:
    raw_type = str(raw.get("type", raw.get("event", raw.get("kind", "unknown"))))
    normalized_type = raw_type
    if raw_type in {"agent-start", "agent_started", "subagent-start", "subagent_started"}:
        normalized_type = "agent-start"
    elif raw_type in {"tool", "tool-call", "tool_call", "tool.started", "item.started"}:
        normalized_type = "tool-call"
    event: dict[str, object] = {
        "id": str(raw.get("id", f"{harness}-{sequence}")),
        "type": normalized_type,
        "harness": harness,
        "sequence": sequence,
        "rawType": raw_type,
        "rawDigest": hashlib.sha256(
            json.dumps(raw, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
        ).hexdigest(),
    }
    for field in ("agent", "command", "contentDigest", "model", "skill", "tool"):
        if field in raw:
            event[field] = raw[field]
    return event
