# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Builds Codex and Junie CLI invocations and normalizes their captured event streams.

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Iterable, Mapping, Sequence

from .commands import CommandSpec


SUPPORTED_HARNESSES = frozenset({"codex", "junie"})
CODEX_OUTPUT_SCHEMA_SHA256 = "36bd63a02034627ab2798a424f8915bf288265846af6e2aad5f7ec18e424c8fc"


@dataclass(frozen=True)
class HarnessIdentity:
    """Record the concrete harness executable, version, and content digest used by a run."""

    harness: str
    executable: Path
    version: str
    content_digest: str


@dataclass(frozen=True)
class ExternalRunnerInvocation:
    """Record a self-attested, unverified wrapper around a Junie command."""

    command: CommandSpec
    runner_digest: str
    attestation_digest: str
    trust_status: str


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
) -> CommandSpec:
    """Build a noninteractive Codex or Junie invocation without executing it.

    Junie has no filesystem sandbox flag. Its command therefore describes only the harness
    invocation; runner-owned external containment must be established and recorded separately.
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
    if isolated_config_root is None:
        raise ValueError("isolated_config_root is required to prevent user-home agent and skill contamination")
    isolated_config_root = isolated_config_root.resolve()
    if isolated_config_root != workspace:
        raise ValueError("isolated_config_root must be the disposable workspace context overlay root")
    approved_environment = _approved_environment_names(approved_environment_names)
    controlled_environment = {
        "HOME": str(workspace / ".eval-context" / "home"),
        "TMPDIR": str(event_output.parent / f".eval-tmp-{workspace.name}"),
    }
    if harness == "codex":
        expected_agent = isolated_config_root / ".codex" / "agents" / f"{agent_id}.toml"
        expected_skills = isolated_config_root / ".agents" / "skills"
        if not expected_agent.is_file() or not expected_skills.is_dir():
            raise ValueError("Codex isolated context must contain the selected project agent and skill locations")
        argv = [
            "codex",
            "exec",
            "--ephemeral",
            "--ignore-user-config",
            "--sandbox",
            "read-only" if read_only else "workspace-write",
            "-C",
            str(workspace),
            "--model",
            model,
            "--json",
        ]
        if output_schema is not None:
            resolved_schema = validate_codex_output_schema(output_schema, workspace)
            argv.extend(["--output-schema", str(resolved_schema)])
        if last_message_output is not None:
            resolved_output = _runner_owned_output_path(
                last_message_output,
                evidence_root,
                workspace,
                "Codex last-message output",
            )
            argv.extend(["--output-last-message", str(resolved_output)])
        argv.append(_delegation_prompt(agent_id, prompt))
        return CommandSpec(
            tuple(argv),
            environment=controlled_environment,
            inherit_environment=False,
            host_environment_allowlist=("PATH", *approved_environment),
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
        "junie",
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
    executable = Path(executable_name).resolve()
    completed = subprocess.run(
        [str(executable), "--version"],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"unable to capture {harness} version: {completed.stderr.strip()}")
    return HarnessIdentity(
        harness=harness,
        executable=executable,
        version=completed.stdout.strip(),
        content_digest=hashlib.sha256(executable.read_bytes()).hexdigest(),
    )


def wrap_junie_external_runner(
    command: CommandSpec,
    runner_path: Path,
    attestation_path: Path,
) -> ExternalRunnerInvocation:
    """Wrap Junie with an identity-bound self-attestation that does not establish containment trust."""

    if not command.argv or command.argv[0] != "junie":
        raise ValueError("external Junie containment can wrap only a Junie command")
    runner = runner_path.resolve()
    attestation = attestation_path.resolve()
    project_arguments = [argument for argument in command.argv if argument.startswith("--project=")]
    if len(project_arguments) != 1:
        raise ValueError("Junie command must identify exactly one project workspace")
    workspace = Path(project_arguments[0].split("=", 1)[1]).resolve()
    if runner == workspace or workspace in runner.parents or attestation == workspace or workspace in attestation.parents:
        raise ValueError("Junie external runner and attestation must be outside the disposable workspace")
    if not runner.is_file() or not runner.stat().st_mode & 0o111:
        raise ValueError("Junie external runner must be an executable file")
    if not attestation.is_file():
        raise ValueError("Junie external containment attestation is missing")
    try:
        value = json.loads(attestation.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise ValueError(f"Junie external containment attestation is invalid: {error}") from error
    if not isinstance(value, Mapping):
        raise ValueError("Junie external containment attestation must be a JSON object")
    runner_digest = hashlib.sha256(runner.read_bytes()).hexdigest()
    if (
        value.get("schema") != "dev-methodology-junie-containment-attestation"
        or value.get("version") != 1
        or value.get("status") != "self-attested-unverified"
        or value.get("runnerDigest") != runner_digest
    ):
        raise ValueError("Junie external containment attestation must be identity-bound and explicitly unverified")
    capabilities = value.get("capabilities")
    required = {"filesystem", "process", "network", "cpu", "memory", "time"}
    if not isinstance(capabilities, list) or not required.issubset(set(capabilities)):
        raise ValueError("Junie external containment attestation lacks required capabilities")
    wrapped = CommandSpec(
        argv=(str(runner), "--", *command.argv),
        environment=command.environment,
        timeout_seconds=command.timeout_seconds,
        maximum_output_bytes=command.maximum_output_bytes,
        inherit_environment=command.inherit_environment,
        host_environment_allowlist=command.host_environment_allowlist,
    )
    return ExternalRunnerInvocation(
        command=wrapped,
        runner_digest=runner_digest,
        attestation_digest=hashlib.sha256(attestation.read_bytes()).hexdigest(),
        trust_status="self-attested-unverified",
    )


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


def _delegation_prompt(agent_id: str, prompt: str) -> str:
    if not agent_id.strip():
        raise ValueError("agent_id must be a non-empty string")
    if not prompt.strip():
        raise ValueError("prompt must be a non-empty string")
    return f"Delegate the following task to the {agent_id} subagent. {prompt}"


def _normalize_event(harness: str, sequence: int, raw: Mapping[str, object]) -> dict[str, object]:
    raw_type = str(raw.get("type", raw.get("event", "unknown")))
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
