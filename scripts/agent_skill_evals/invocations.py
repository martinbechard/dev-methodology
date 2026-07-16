# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Builds Codex and Junie CLI invocations and normalizes their captured event streams.

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
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


@dataclass(frozen=True)
class HarnessIdentity:
    """Record the concrete harness executable, version, and content digest used by a run."""

    harness: str
    executable: Path
    version: str
    content_digest: str


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
            executable,
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
        if resolved_last_message_output is not None:
            argv.extend(["--output-last-message", str(resolved_last_message_output)])
        argv.append(_delegation_prompt(agent_id, prompt))
        return CommandSpec(
            tuple(argv),
            environment=controlled_environment,
            inherit_environment=False,
            host_environment_allowlist=("PATH", *approved_environment),
        )

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
