# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Builds allowlisted harness context overlays and rejects sensitive model-visible inputs.

from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import secrets
import shutil
import stat
from dataclasses import dataclass, replace
from pathlib import Path, PurePosixPath
from typing import Iterable, Mapping, Sequence

from .invocations import (
    SUPPORTED_HARNESSES,
    _CODEX_MCP_AGENT_OPS_ENABLED_TOOLS,
    McpAgentOpsContext,
    McpAgentOpsIdentity,
    junie_mcp_agent_ops_authorization_payload,
    mcp_agent_ops_configuration_payload,
)
from .workspace import (
    TRANSIENT_TREE_NAMES,
    snapshot_digest,
)


_EMAIL_PATTERN = re.compile(
    rb"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.IGNORECASE
)
_SENSITIVE_PATTERNS = (
    ("email address", _EMAIL_PATTERN),
    ("private key", re.compile(rb"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("secret assignment", re.compile(rb"(?:api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]", re.IGNORECASE)),
    (
        "sensitive classification",
        re.compile(
            rb"^(?:data[_ -]?classification|classification)\s*[:=]\s*(?:company|customer)[_ -]?(?:confidential|internal)\b",
            re.IGNORECASE | re.MULTILINE,
        ),
    ),
)
_RUNNER_OWNED_ROOTS = frozenset({
    ".agents",
    ".codex",
    ".eval-context",
    ".git",
    ".junie",
})
_RUNNER_OWNED_FILES = frozenset({".eval-prepared.json", ".eval-workspace.json"})
_MAX_PROJECTION_OUTPUT_FILES = 512
_MAX_PROJECTION_OUTPUT_BYTES = 20 * 1024 * 1024


@dataclass(frozen=True)
class ContextFile:
    """Describe one explicitly allowlisted file copied into a harness context overlay."""

    source_path: str
    destination_path: str
    content_digest: str
    effective_digest: str
    size: int
    context_role: str
    sanitizations: tuple[str, ...]


@dataclass(frozen=True)
class ContextPack:
    """Describe the selected agent and skills staged for one harness invocation."""

    root: Path
    harness: str
    agent_id: str
    files: tuple[ContextFile, ...]
    manifest_digest: str
    agent_location: Path
    skill_location: Path


@dataclass(frozen=True)
class InputManifest:
    """Record the approved effective model-visible input set and its content digest."""

    files: tuple[ContextFile, ...]
    manifest_digest: str


@dataclass(frozen=True)
class ProjectedFile:
    """Record one typed filesystem entry copied into a model-visible workspace."""

    path: str
    type: str
    mode: str
    digest: str | None
    size: int | None


@dataclass(frozen=True)
class ProjectionMutation:
    """Record one allowlisted model-created file synchronized to the full fixture."""

    path: str
    action: str
    before_digest: str | None
    after_digest: str
    size: int
    mode: str
    retained_evidence: str


@dataclass(frozen=True)
class ModelVisibleProjection:
    """Bind an isolated harness workspace to its complete fixture partition."""

    source_root: Path
    root: Path
    files: tuple[ProjectedFile, ...]
    manifest_digest: str
    prepared_snapshot_digest: str
    source_identity_digest: str
    source_files: tuple[ProjectedFile, ...]
    model_visible_paths: tuple[str, ...]
    evaluator_only_paths: tuple[str, ...]
    sync_paths: tuple[str, ...]
    initial_directories: tuple[str, ...]
    sealed_entries: tuple[ProjectedFile, ...] = ()

    @property
    def entries(self) -> tuple[ProjectedFile, ...]:
        """Return every projected file and directory in deterministic path order."""

        return self.files


@dataclass(frozen=True)
class ProjectionSyncManifest:
    """Describe the applied projection mutations and their durable evidence file."""

    evidence_path: Path
    manifest_digest: str
    mutations: tuple[ProjectionMutation, ...]
    mutation_records: tuple[dict[str, object], ...]
    created_directories: tuple[dict[str, str], ...]
    post_sync_source_identity_digest: str


@dataclass(frozen=True)
class ProjectionManifestEvidence:
    """Describe a retained replayable projection-manifest artifact."""

    evidence_path: Path
    content_digest: str
    manifest_digest: str
    prepared_entries: tuple[dict[str, object], ...]
    projected_inputs: tuple[dict[str, object], ...]


@dataclass(frozen=True)
class ProjectionEvidenceDirectory:
    """Own one private directory whose artifacts remain relative to a future receipt."""

    root: Path

    def path(self, name: str) -> Path:
        """Resolve one normalized artifact name beneath the private directory."""

        relative = _safe_relative_path(name)
        candidate = self.root.joinpath(*relative.parts)
        if candidate == self.root or self.root not in candidate.parents:
            raise ValueError("projection evidence artifact escapes its private directory")
        return candidate

    def reference(self, artifact: Path, marker: str) -> str:
        """Return a stable file-marker reference relative to a receipt in this directory."""

        if not marker or "#" in marker or "\n" in marker:
            raise ValueError("projection evidence marker must be a non-empty single-line value")
        resolved = artifact.resolve()
        if self.root not in resolved.parents or not resolved.is_file():
            raise ValueError("projection evidence reference must identify a retained artifact")
        return f"{resolved.relative_to(self.root).as_posix()}#{marker}"


class ContextPackBuilder:
    """Stage only one generated agent definition and explicitly selected skill files."""

    def __init__(self, source_root: Path) -> None:
        self.source_root = source_root.resolve()

    def stage(
        self,
        harness: str,
        agent_id: str,
        skill_ids: Sequence[str],
        destination_root: Path,
        *,
        additional_files: Sequence[str] = (),
        skill_files: dict[str, Sequence[str]] | None = None,
    ) -> ContextPack:
        """Validate and copy the allowlisted context into repository-native project locations."""

        if harness not in SUPPORTED_HARNESSES:
            raise ValueError(f"supported harness values are codex and junie, not {harness}")
        if not agent_id or any(not skill_id for skill_id in skill_ids):
            raise ValueError("agent and skill identifiers must be non-empty")
        destination_root = destination_root.resolve()
        agent_suffix = ".toml" if harness == "codex" else ".md"
        agent_source = PurePosixPath("generated") / "adapters" / harness / "agents" / f"{agent_id}{agent_suffix}"
        if harness == "codex":
            agent_location = destination_root / ".codex" / "agents"
            skill_location = destination_root / ".agents" / "skills"
        else:
            agent_location = destination_root / ".junie" / "agents"
            skill_location = destination_root / ".junie" / "skills"
        selections: list[tuple[PurePosixPath, Path, str]] = [
            (agent_source, agent_location / f"{agent_id}{agent_suffix}", "agent-definition"),
        ]
        agent_source_path = (self.source_root / agent_source).resolve()
        if harness == "codex" and agent_source_path.is_file():
            agent_text = agent_source_path.read_text(encoding="utf-8")
            if "codex-harness-directives" in agent_text:
                harness_skill_source = (
                    PurePosixPath("adapters") / "codex" / "skills" / "codex-harness-directives" / "SKILL.md"
                )
                selections.append((
                    harness_skill_source,
                    skill_location / "codex-harness-directives" / "SKILL.md",
                    "harness-required-skill",
                ))
        selected_skill_files = skill_files or {}
        for skill_id in sorted(set(skill_ids)):
            relative_files = selected_skill_files.get(skill_id, (".",))
            if "." not in relative_files and "SKILL.md" not in relative_files:
                raise ValueError(f"skill allowlist must include SKILL.md: {skill_id}")
            for relative_file in relative_files:
                relative = _safe_relative_path(relative_file)
                source_entry = self.source_root / "skills" / skill_id / relative
                if source_entry.is_dir():
                    for child in _walk_pruned(source_entry):
                        child_relative = child.relative_to(self.source_root)
                        destination_relative = child.relative_to(self.source_root / "skills" / skill_id)
                        selections.append((
                            PurePosixPath(child_relative.as_posix()),
                            skill_location / skill_id / destination_relative,
                            "treatment-skill",
                        ))
                else:
                    selections.append((
                        PurePosixPath("skills") / skill_id / relative,
                        skill_location / skill_id / relative,
                        "treatment-skill",
                    ))
        for relative_file in additional_files:
            relative = _safe_relative_path(relative_file)
            selections.append((
                relative,
                destination_root / ".eval-context" / "additional" / relative,
                "additional-allowlisted-input",
            ))

        files: list[ContextFile] = []
        for source_relative, destination, context_role in selections:
            source = (self.source_root / source_relative).resolve()
            if self.source_root not in source.parents or not source.is_file():
                raise ValueError(f"allowlisted context file is missing or outside the source root: {source_relative}")
            content, effective_content, sanitizations = selected_context_identity(source, context_role)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(effective_content)
            shutil.copymode(source, destination)
            files.append(ContextFile(
                source_path=source_relative.as_posix(),
                destination_path=destination.relative_to(destination_root).as_posix(),
                content_digest=hashlib.sha256(content).hexdigest(),
                effective_digest=hashlib.sha256(destination.read_bytes()).hexdigest(),
                size=len(effective_content),
                context_role=context_role,
                sanitizations=sanitizations,
            ))
        manifest_digest = _manifest_digest(files)
        manifest_path = destination_root / ".eval-context" / "context-manifest.json"
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(
            json.dumps({
                "harness": harness,
                "agent": agent_id,
                "manifestDigest": manifest_digest,
                "files": [file.__dict__ for file in files],
            }, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return ContextPack(
            root=destination_root,
            harness=harness,
            agent_id=agent_id,
            files=tuple(files),
            manifest_digest=manifest_digest,
            agent_location=agent_location,
            skill_location=skill_location,
        )


def stage_mcp_agent_ops_context(
    harness: str,
    destination_root: Path,
    identity: McpAgentOpsIdentity,
    source_root: Path,
    treatment_skill_root: Path,
    available_skill_ids: Sequence[str],
    treatment_skill_ids: Sequence[str],
    audit_log: Path,
    audit_root: Path,
    *,
    catalog_resource_allowlist: Mapping[str, Sequence[str]],
    mcp_only_skill_ids: Sequence[str] = (),
) -> McpAgentOpsContext:
    """Create one isolated Codex or Junie MCP configuration for an evaluation run."""
    if harness not in SUPPORTED_HARNESSES:
        raise ValueError(f"supported harness values are codex and junie, not {harness}")
    destination_root = destination_root.resolve()
    source_root = source_root.resolve()
    treatment_skill_root = treatment_skill_root.resolve()
    audit_root = audit_root.resolve()
    if audit_root.is_symlink() or not audit_root.is_dir():
        raise ValueError("MCP audit root must be an existing non-symlink directory")
    if (
        audit_root == destination_root
        or destination_root in audit_root.parents
        or audit_root in destination_root.parents
    ):
        raise ValueError("MCP audit root must be disjoint from the product workspace")
    evidence_directory = (
        audit_root
        / f".mcp-agent-ops-{harness}-{destination_root.name}-{secrets.token_hex(8)}"
    )
    evidence_directory.mkdir(mode=0o700)
    if (
        treatment_skill_root != destination_root
        and destination_root not in treatment_skill_root.parents
    ):
        raise ValueError("MCP treatment skill root must stay inside the disposable context root")
    available = tuple(available_skill_ids)
    treatment = frozenset(treatment_skill_ids)
    mcp_only = frozenset(mcp_only_skill_ids)
    catalog_treatment = treatment | mcp_only
    if (
        not available
        or len(available) != len(set(available))
        or any(not re.fullmatch(r"[a-z0-9][a-z0-9-]*", skill) for skill in available)
    ):
        raise ValueError("MCP available skill ids must be unique normalized skill names")
    if len(mcp_only_skill_ids) != len(mcp_only) or any(
        not re.fullmatch(r"[a-z0-9][a-z0-9-]*", skill)
        for skill in mcp_only_skill_ids
    ):
        raise ValueError("MCP-only skill ids must be unique normalized skill names")
    if treatment & mcp_only:
        raise ValueError("MCP-only skills must not be harness-preloaded treatment skills")
    if not catalog_treatment.issubset(available):
        raise ValueError("MCP treatment skills must be present in the complete available catalog")
    if set(catalog_resource_allowlist) - catalog_treatment:
        raise ValueError("MCP catalog resources may be staged only for treatment skills")
    skill_root = destination_root / ".eval-context" / "mcp-agent-ops" / "skills"
    if skill_root.exists():
        raise ValueError("MCP skill catalog destination must be unused")
    catalog_records: list[dict[str, object]] = []
    for skill_id in sorted(available):
        destination_skill = skill_root / skill_id
        if skill_id in catalog_treatment:
            source_skill = (
                source_root / "skills" / skill_id
                if skill_id in mcp_only
                else treatment_skill_root / skill_id
            )
            if source_skill.is_symlink() or not source_skill.is_dir():
                raise ValueError(f"staged MCP treatment skill is missing: {skill_id}")
            source_manifest = source_skill / "SKILL.md"
            if source_manifest.is_symlink() or not source_manifest.is_file():
                raise ValueError(f"staged MCP treatment skill lacks SKILL.md: {skill_id}")
            selected_files: list[tuple[Path, PurePosixPath, str]] = [
                (source_manifest, PurePosixPath("SKILL.md"), "treatment-skill")
            ]
            declared_resources = catalog_resource_allowlist.get(skill_id, ())
            if len(declared_resources) != len(set(declared_resources)):
                raise ValueError(f"MCP catalog resource allowlist repeats a path: {skill_id}")
            bundle_skill = source_root / "skills" / skill_id
            if bundle_skill.is_symlink() or not bundle_skill.is_dir():
                raise ValueError(f"MCP bundle treatment skill is missing or unsafe: {skill_id}")
            for resource_path in declared_resources:
                relative = _safe_relative_path(resource_path)
                if relative in {PurePosixPath("."), PurePosixPath("SKILL.md")}:
                    raise ValueError(
                        f"MCP catalog resource must be a supporting file: {skill_id}/{relative}"
                    )
                resource = bundle_skill / relative
                resolved_resource = resource.resolve()
                resolved_bundle_skill = bundle_skill.resolve()
                if (
                    resource.is_symlink()
                    or not resolved_resource.is_file()
                    or resolved_bundle_skill not in resolved_resource.parents
                ):
                    raise ValueError(
                        f"MCP catalog resource is missing or unsafe: {skill_id}/{relative}"
                    )
                selected_files.append((resolved_resource, relative, "mcp-resource"))
            for source, relative, role in selected_files:
                destination = destination_skill / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                _source_content, content, _sanitizations = selected_context_identity(
                    source,
                    "treatment-skill",
                )
                destination.write_bytes(content)
                shutil.copymode(source, destination)
                catalog_records.append({
                    "skill": skill_id,
                    "path": relative.as_posix(),
                    "role": role,
                    "digest": hashlib.sha256(content).hexdigest(),
                    "size": len(content),
                })
        else:
            source_skill_dir = source_root / "skills" / skill_id
            source_manifest = source_skill_dir / "SKILL.md"
            if (
                source_skill_dir.is_symlink()
                or source_manifest.is_symlink()
                or not source_manifest.is_file()
                or source_root not in source_manifest.resolve().parents
            ):
                raise ValueError(f"MCP available skill is missing or unsafe: {skill_id}")
            _source, effective, _sanitizations = selected_context_identity(
                source_manifest,
                "treatment-skill",
            )
            content = _catalog_only_skill(effective)
            destination = destination_skill / "SKILL.md"
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content)
            catalog_records.append({
                "skill": skill_id,
                "path": "SKILL.md",
                "role": "catalog-metadata-only",
                "digest": hashlib.sha256(content).hexdigest(),
                "size": len(content),
            })
    staged_ids = {
        path.name for path in skill_root.iterdir() if path.is_dir()
    }
    if staged_ids != set(available):
        raise ValueError("staged MCP skill catalog differs from declared runtime availability")
    catalog_manifest_digest = hashlib.sha256(
        json.dumps(
            catalog_records,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    manifest_path = destination_root / ".eval-context" / "mcp-agent-ops" / "catalog-manifest.json"
    manifest_bytes = (
        json.dumps(
            {
                "schema": "dev-methodology-eval-mcp-skill-catalog",
                "version": 1,
                "manifestDigest": catalog_manifest_digest,
                "skills": list(sorted(available)),
                "files": catalog_records,
            },
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")
    manifest_path.write_bytes(manifest_bytes)
    catalog_evidence = evidence_directory / "catalog-manifest.json"
    catalog_evidence.write_bytes(manifest_bytes)
    os.chmod(catalog_evidence, 0o600)
    detection_registry = (
        skill_root
        / "detect-technology-skills"
        / "references"
        / "technology-skill-detection-registry.yaml"
    ).resolve()
    if detection_registry.is_symlink() or not detection_registry.is_file():
        raise ValueError("staged MCP technology detection registry is missing")
    audit_log = audit_log.resolve()
    if audit_log == audit_root or audit_root not in audit_log.parents:
        raise ValueError("MCP audit log must stay beneath the runner-owned audit root")
    if audit_log.exists() or audit_log.is_symlink():
        raise ValueError("MCP audit log must be an unused non-symlink path")
    audit_session_id = secrets.token_hex(16)
    environment = {
        "MCP_AGENT_OPS_SKILL_ROOTS": str(skill_root),
        "MCP_AGENT_OPS_DETECTION_REGISTRY": str(detection_registry),
        "MCP_AGENT_OPS_WORKSPACE_ROOTS": str(destination_root),
        "MCP_AGENT_OPS_AUDIT_LOG": str(audit_log),
        "MCP_AGENT_OPS_AUDIT_ROOTS": str(audit_root),
        "MCP_AGENT_OPS_AUDIT_SHARED": "true",
        "MCP_AGENT_OPS_AUDIT_SESSION_ID": audit_session_id,
        "MCP_AGENT_OPS_REQUIRED_RUNTIME_DIGEST": identity.runtime_digest,
    }
    server_config = {
        "command": str(identity.executable),
        "args": [],
        "env": environment,
    }
    host_home = Path.home().resolve()
    configuration_payload = mcp_agent_ops_configuration_payload(
        harness,
        server_config,
        workspace_root=destination_root,
        evidence_root=audit_root,
        host_home=host_home,
        enabled_tools=_CODEX_MCP_AGENT_OPS_ENABLED_TOOLS,
        codex_permission_profile=True,
    )
    config_location: Path | None = None
    if harness == "junie":
        config_location = evidence_directory / "junie"
        config_location.mkdir(mode=0o700)
        configuration_evidence = config_location / "mcp.json"
    else:
        configuration_evidence = evidence_directory / "codex-mcp-config.json"
    configuration_bytes = (
        json.dumps(configuration_payload, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")
    configuration_evidence.write_bytes(configuration_bytes)
    os.chmod(configuration_evidence, 0o600)
    configuration_digest = hashlib.sha256(configuration_bytes).hexdigest()
    authorization_digest: str | None = None
    authorization_evidence: Path | None = None
    if harness == "junie":
        authorization_payload = junie_mcp_agent_ops_authorization_payload(
            _CODEX_MCP_AGENT_OPS_ENABLED_TOOLS
        )
        authorization_bytes = (
            json.dumps(authorization_payload, sort_keys=True, separators=(",", ":"))
            + "\n"
        ).encode("utf-8")
        authorization_evidence = evidence_directory / "junie-allowlist.json"
        authorization_evidence.write_bytes(authorization_bytes)
        os.chmod(authorization_evidence, 0o600)
        authorization_digest = hashlib.sha256(authorization_bytes).hexdigest()
    return McpAgentOpsContext(
        server_name="mcp-agent-ops",
        identity=identity,
        skill_root=skill_root,
        detection_registry=detection_registry,
        workspace_root=destination_root,
        audit_log=audit_log,
        audit_root=audit_root,
        audit_session_id=audit_session_id,
        configuration_digest=configuration_digest,
        catalog_manifest_digest=catalog_manifest_digest,
        configuration_evidence=configuration_evidence,
        catalog_evidence=catalog_evidence,
        evidence_directory=evidence_directory,
        host_home=host_home,
        enabled_tools=tuple(_CODEX_MCP_AGENT_OPS_ENABLED_TOOLS),
        server_environment=tuple(environment.items()),
        codex_permission_profile=True,
        authorization_digest=authorization_digest,
        authorization_evidence=authorization_evidence,
        config_location=config_location,
    )


def stage_mcp_reference_context(
    harness: str,
    destination_root: Path,
    identity: McpAgentOpsIdentity,
    audit_log: Path,
    audit_root: Path,
    *,
    reference_names: Sequence[str],
    enabled_tools: Sequence[str],
) -> McpAgentOpsContext:
    """Stage one isolated reference-only MCP context for an evaluation treatment.

    The destination is the disposable workspace. Each reference name must identify one
    regular top-level workspace file. The function copies only those files, records their
    digests, writes an isolated host configuration and audit identity, and returns their
    runner-owned context. Invalid paths, duplicate names or tools, unsafe roots, and existing
    destinations raise ``ValueError``.
    """

    if harness not in SUPPORTED_HARNESSES:
        raise ValueError(f"supported harness values are codex and junie, not {harness}")
    destination_root = destination_root.resolve()
    audit_root = audit_root.resolve()
    if audit_root.is_symlink() or not audit_root.is_dir():
        raise ValueError("MCP audit root must be an existing non-symlink directory")
    if (
        audit_root == destination_root
        or destination_root in audit_root.parents
        or audit_root in destination_root.parents
    ):
        raise ValueError("MCP audit root must be disjoint from the product workspace")
    names = tuple(reference_names)
    tools = tuple(enabled_tools)
    if (
        not names
        or len(names) != len(set(names))
        or any(
            PurePosixPath(name).name != name
            or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", name)
            for name in names
        )
    ):
        raise ValueError("MCP reference names must be unique safe filenames")
    if (
        not tools
        or len(tools) != len(set(tools))
        or any(not re.fullmatch(r"[a-z][a-z0-9_]*", tool) for tool in tools)
    ):
        raise ValueError("MCP enabled tools must be unique normalized names")

    evidence_directory = (
        audit_root
        / f".mcp-agent-ops-{harness}-{destination_root.name}-{secrets.token_hex(8)}"
    )
    evidence_directory.mkdir(mode=0o700)
    reference_root = evidence_directory / "references"
    if reference_root.exists() or reference_root.is_symlink():
        raise ValueError("MCP reference destination must be unused")
    reference_root.mkdir(mode=0o700)
    reference_records: list[dict[str, object]] = []
    for name in names:
        source = destination_root / name
        if source.is_symlink() or not source.is_file():
            raise ValueError(f"MCP reference source is missing or unsafe: {name}")
        _source, effective, sanitizations = selected_context_identity(
            source,
            "model-visible-input",
        )
        if sanitizations:
            raise ValueError("MCP reference context must preserve exact source bytes")
        destination = reference_root / name
        destination.write_bytes(effective)
        os.chmod(destination, 0o400)
        reference_records.append({
            "name": name,
            "path": name,
            "digest": hashlib.sha256(effective).hexdigest(),
            "size": len(effective),
        })
    catalog_manifest_digest = hashlib.sha256(
        json.dumps(
            reference_records,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    manifest_path = reference_root.parent / "reference-manifest.json"
    manifest_bytes = (
        json.dumps(
            {
                "schema": "dev-methodology-eval-mcp-reference-catalog",
                "version": 1,
                "manifestDigest": catalog_manifest_digest,
                "names": list(names),
                "files": reference_records,
            },
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")
    manifest_path.write_bytes(manifest_bytes)
    catalog_evidence = manifest_path
    os.chmod(catalog_evidence, 0o600)

    audit_log = audit_log.resolve()
    if audit_log == audit_root or audit_root not in audit_log.parents:
        raise ValueError("MCP audit log must stay beneath the runner-owned audit root")
    if audit_log.exists() or audit_log.is_symlink():
        raise ValueError("MCP audit log must be an unused non-symlink path")
    audit_session_id = secrets.token_hex(16)
    environment = {
        "MCP_AGENT_OPS_WORKSPACE_ROOTS": str(destination_root),
        "MCP_AGENT_OPS_REFERENCE_ROOTS": str(reference_root),
        "MCP_AGENT_OPS_REFERENCE_NAMES": os.pathsep.join(names),
        "MCP_AGENT_OPS_AUDIT_LOG": str(audit_log),
        "MCP_AGENT_OPS_AUDIT_ROOTS": str(audit_root),
        "MCP_AGENT_OPS_AUDIT_SHARED": "true",
        "MCP_AGENT_OPS_AUDIT_SESSION_ID": audit_session_id,
        "MCP_AGENT_OPS_REQUIRED_RUNTIME_DIGEST": identity.runtime_digest,
    }
    server_config = {
        "command": str(identity.executable),
        "args": [],
        "env": environment,
    }
    host_home = Path.home().resolve()
    configuration_payload = mcp_agent_ops_configuration_payload(
        harness,
        server_config,
        workspace_root=destination_root,
        evidence_root=audit_root,
        host_home=host_home,
        enabled_tools=tools,
        codex_permission_profile=False,
    )
    config_location: Path | None = None
    if harness == "junie":
        config_location = evidence_directory / "junie"
        config_location.mkdir(mode=0o700)
        configuration_evidence = config_location / "mcp.json"
    else:
        configuration_evidence = evidence_directory / "codex-mcp-config.json"
    configuration_bytes = (
        json.dumps(configuration_payload, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")
    configuration_evidence.write_bytes(configuration_bytes)
    os.chmod(configuration_evidence, 0o600)
    configuration_digest = hashlib.sha256(configuration_bytes).hexdigest()
    authorization_digest: str | None = None
    authorization_evidence: Path | None = None
    if harness == "junie":
        authorization_payload = junie_mcp_agent_ops_authorization_payload(tools)
        authorization_bytes = (
            json.dumps(authorization_payload, sort_keys=True, separators=(",", ":"))
            + "\n"
        ).encode("utf-8")
        authorization_evidence = evidence_directory / "junie-allowlist.json"
        authorization_evidence.write_bytes(authorization_bytes)
        os.chmod(authorization_evidence, 0o600)
        authorization_digest = hashlib.sha256(authorization_bytes).hexdigest()
    return McpAgentOpsContext(
        server_name="mcp-agent-ops",
        identity=identity,
        skill_root=None,
        detection_registry=None,
        workspace_root=destination_root,
        audit_log=audit_log,
        audit_root=audit_root,
        audit_session_id=audit_session_id,
        configuration_digest=configuration_digest,
        catalog_manifest_digest=catalog_manifest_digest,
        configuration_evidence=configuration_evidence,
        catalog_evidence=catalog_evidence,
        evidence_directory=evidence_directory,
        host_home=host_home,
        enabled_tools=tools,
        server_environment=tuple(environment.items()),
        codex_permission_profile=False,
        reference_root=reference_root,
        reference_names=names,
        authorization_digest=authorization_digest,
        authorization_evidence=authorization_evidence,
        config_location=config_location,
    )


def read_mcp_skill_catalog(
    workspace: Path,
    relative_path: str,
    source_root: Path,
) -> tuple[str, ...]:
    """Read and validate one exact evaluator-owned runtime-availability catalog."""
    workspace = workspace.resolve()
    relative = _safe_relative_path(relative_path)
    path = workspace / relative
    if path.is_symlink():
        raise ValueError("MCP skill catalog source must be a regular non-symlink file")
    resolved = path.resolve()
    if workspace not in resolved.parents or not resolved.is_file():
        raise ValueError("MCP skill catalog source must stay inside the disposable workspace")
    lines = resolved.read_text(encoding="utf-8").splitlines()
    if (
        not lines
        or any(not line or line.strip() != line for line in lines)
        or any(not re.fullmatch(r"[a-z0-9][a-z0-9-]*", line) for line in lines)
        or len(lines) != len(set(lines))
    ):
        raise ValueError("MCP skill catalog must contain unique normalized skill ids")
    bundle_root = source_root.resolve() / "skills"
    for skill_id in lines:
        directory = bundle_root / skill_id
        manifest = directory / "SKILL.md"
        if (
            directory.is_symlink()
            or manifest.is_symlink()
            or not manifest.is_file()
            or bundle_root not in manifest.resolve().parents
        ):
            raise ValueError(f"MCP skill catalog references an unavailable bundle skill: {skill_id}")
    return tuple(lines)


def _catalog_only_skill(effective_manifest: bytes) -> bytes:
    """Retain only safe frontmatter for a catalog entry that is not an execution skill."""
    try:
        lines = effective_manifest.decode("utf-8").splitlines()
    except UnicodeError as error:
        raise ValueError("MCP skill manifest must be UTF-8") from error
    if not lines or lines[0] != "---":
        raise ValueError("MCP skill manifest must start with YAML frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError as error:
        raise ValueError("MCP skill manifest frontmatter is not closed") from error
    frontmatter = "\n".join(lines[: end + 1])
    return (
        frontmatter
        + "\n\n# Evaluation catalog entry\n\n"
        + "The complete instructions are intentionally unavailable in this isolated evaluation.\n"
    ).encode("utf-8")


def selected_context_identity(path: Path, context_role: str) -> tuple[bytes, bytes, tuple[str, ...]]:
    """Return source and effective bytes plus deterministic sanitization actions for one file."""

    source = path.resolve()
    if not source.is_file():
        raise ValueError(f"selected context file is missing: {source}")
    content = source.read_bytes()
    effective_content, sanitizations = _sanitize_selected_context(context_role, content)
    _reject_sensitive(source.as_posix(), effective_content)
    return content, effective_content, sanitizations


def stage_model_visible_projection(
    source_root: Path,
    destination_root: Path,
    model_visible_paths: Sequence[str],
    *,
    evaluator_only_paths: Sequence[str],
    sync_paths: Sequence[str],
    prepared_snapshot_digest: str | None = None,
) -> ModelVisibleProjection:
    """Copy one complete, explicitly partitioned fixture into an isolated harness root."""

    if source_root.is_symlink() or not source_root.is_dir():
        raise ValueError("model-visible projection source must be an existing non-symlink directory")
    source_root = source_root.resolve()
    if destination_root.exists() or destination_root.is_symlink():
        raise ValueError("model-visible projection destination must be an unused non-symlink path")
    destination_parent = destination_root.parent.resolve()
    destination_root = destination_parent / destination_root.name
    if (
        destination_root == source_root
        or source_root in destination_root.parents
        or destination_root in source_root.parents
    ):
        raise ValueError("model-visible projection destination must be disjoint from its source")

    visible = _normalized_disjoint_paths(model_visible_paths, "model-visible")
    evaluator_only = _normalized_disjoint_paths(
        evaluator_only_paths,
        "evaluator-only",
    )
    synchronized = _normalized_disjoint_paths(sync_paths, "projection sync")
    _reject_projection_path_overlap(visible, evaluator_only, "model-visible", "evaluator-only")
    _reject_projection_path_overlap(visible, synchronized, "model-visible", "sync")
    _reject_projection_path_overlap(evaluator_only, synchronized, "evaluator-only", "sync")

    source_entries = _projection_product_entries(
        source_root,
        include_runner_owned=False,
    )
    source_entry_map = {entry.path: entry for entry in source_entries}
    visible_entries = _selected_projection_entries(
        source_root,
        visible,
        "model-visible",
        source_entry_map,
    )
    evaluator_entries = _selected_projection_entries(
        source_root,
        evaluator_only,
        "evaluator-only",
        source_entry_map,
        allow_empty_selection=True,
    )
    all_source_entries = set(source_entry_map)
    partitioned = set(visible_entries) | set(evaluator_entries)
    undeclared = sorted(all_source_entries - partitioned)
    if undeclared:
        raise ValueError(f"model-visible projection has undeclared source entry: {undeclared[0]}")
    if partitioned - all_source_entries:
        raise ValueError("model-visible projection partition contains an unavailable source entry")
    for relative in synchronized:
        _validate_unused_sync_destination(source_root, relative)

    source_identity_digest = _projection_entries_digest(source_entries)
    if prepared_snapshot_digest is None:
        prepared_snapshot_digest = source_identity_digest
    if prepared_snapshot_digest != source_identity_digest:
        raise ValueError(
            "model-visible projection source differs from the prepared full-fixture snapshot"
        )

    destination_root.mkdir(mode=0o700)
    projected_entries: list[ProjectedFile] = []
    try:
        for relative, expected in sorted(visible_entries.items()):
            source = source_root / relative
            destination = destination_root / relative
            if expected.type == "directory":
                destination.mkdir(parents=True, exist_ok=False)
                os.chmod(destination, int(expected.mode, 8))
            else:
                destination.parent.mkdir(parents=True, exist_ok=True)
                content = source.read_bytes()
                if (
                    len(content) != expected.size
                    or hashlib.sha256(content).hexdigest() != expected.digest
                    or _entry_mode(source) != expected.mode
                ):
                    raise ValueError(
                        f"model-visible projection source changed during copy: {relative}"
                    )
                destination.write_bytes(content)
                os.chmod(destination, int(expected.mode, 8))
            projected_entries.append(expected)
        if _projection_source_identity(source_root) != source_identity_digest:
            raise ValueError("model-visible projection source changed during staging")
    except Exception:
        shutil.rmtree(destination_root, ignore_errors=True)
        raise

    initial_directories = tuple(
        entry.path for entry in projected_entries if entry.type == "directory"
    )
    payload = {
        "schema": "dev-methodology-eval-model-visible-projection",
        "version": 3,
        "preparedSnapshotDigest": prepared_snapshot_digest,
        "sourceIdentityDigest": source_identity_digest,
        "preparedEntries": [entry.__dict__ for entry in source_entries],
        "modelVisiblePaths": [path.as_posix() for path in visible],
        "evaluatorOnlyPaths": [path.as_posix() for path in evaluator_only],
        "syncPaths": [path.as_posix() for path in synchronized],
        "projectedInputs": [entry.__dict__ for entry in projected_entries],
    }
    manifest_digest = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return ModelVisibleProjection(
        source_root=source_root,
        root=destination_root,
        files=tuple(projected_entries),
        manifest_digest=manifest_digest,
        prepared_snapshot_digest=prepared_snapshot_digest,
        source_identity_digest=source_identity_digest,
        source_files=source_entries,
        model_visible_paths=tuple(path.as_posix() for path in visible),
        evaluator_only_paths=tuple(path.as_posix() for path in evaluator_only),
        sync_paths=tuple(path.as_posix() for path in synchronized),
        initial_directories=initial_directories,
        sealed_entries=tuple(projected_entries),
    )


def seal_model_visible_projection(
    projection: ModelVisibleProjection,
) -> ModelVisibleProjection:
    """Seal the exact pre-model workspace, including runner-owned staged context."""

    entries = _projection_product_entries(
        projection.root,
        include_runner_owned=True,
    )
    return replace(projection, sealed_entries=entries)


def create_projection_evidence_directory(
    directory: Path,
    source_root: Path,
    projection_root: Path,
) -> ProjectionEvidenceDirectory:
    """Create an unused owner-only artifact directory outside both disposable workspaces."""

    if directory.exists() or directory.is_symlink():
        raise ValueError("projection evidence directory must be an unused non-symlink path")
    if directory.parent.is_symlink():
        raise ValueError("projection evidence directory parent must not be a symlink")
    directory.parent.mkdir(parents=True, exist_ok=True)
    parent = directory.parent.resolve()
    directory = parent / directory.name
    for workspace in (source_root.resolve(), projection_root.resolve()):
        if directory == workspace or workspace in directory.parents or directory in workspace.parents:
            raise ValueError("projection evidence directory must stay outside both workspaces")
    directory.mkdir(mode=0o700)
    os.chmod(directory, 0o700)
    return ProjectionEvidenceDirectory(directory.resolve())


def open_projection_evidence_directory(
    directory: Path,
    source_root: Path,
    projection_root: Path,
) -> ProjectionEvidenceDirectory:
    """Open one existing owner-only artifact package outside both workspaces."""

    if directory.is_symlink() or not directory.is_dir():
        raise ValueError(
            "projection evidence directory must be an existing non-symlink directory"
        )
    directory = directory.resolve()
    if stat.S_IMODE(directory.stat().st_mode) != 0o700:
        raise ValueError("projection evidence directory must have owner-only mode 0700")
    if directory.stat().st_uid != os.getuid():
        raise ValueError("projection evidence directory must be owned by the current user")
    for workspace in (source_root.resolve(), projection_root.resolve()):
        if directory == workspace or workspace in directory.parents or directory in workspace.parents:
            raise ValueError("projection evidence directory must stay outside both workspaces")
    return ProjectionEvidenceDirectory(directory)


def synchronize_model_visible_projection(
    projection: ModelVisibleProjection,
    evidence_path: Path,
    *,
    projection_manifest: ProjectionManifestEvidence | None = None,
) -> ProjectionSyncManifest:
    """Fail closed or atomically copy allowlisted model-created files to the full fixture."""

    source_root = projection.source_root
    projection_root = projection.root
    if source_root.is_symlink() or projection_root.is_symlink():
        raise ValueError("projection sync roots must not be symlinks")
    if not source_root.is_dir() or not projection_root.is_dir():
        raise ValueError("projection sync roots must remain existing directories")
    if (
        source_root == projection_root
        or source_root in projection_root.parents
        or projection_root in source_root.parents
    ):
        raise ValueError("projection sync roots must remain disjoint")

    initial_entries = {entry.path: entry for entry in projection.files}
    sealed_entries = {entry.path: entry for entry in projection.sealed_entries}
    original_source_entries = {entry.path: entry for entry in projection.source_files}
    current_source_entries = {
        entry.path: entry
        for entry in _projection_product_entries(
            source_root,
            include_runner_owned=False,
        )
    }
    if current_source_entries != original_source_entries:
        changed = sorted(
            relative
            for relative in set(current_source_entries) | set(original_source_entries)
            if current_source_entries.get(relative) != original_source_entries.get(relative)
        )
        detail = changed[0] if changed else "unknown"
        raise ValueError(f"ambiguous sync state: fixture source changed: {detail}")
    if _projection_source_identity(source_root) != projection.source_identity_digest:
        raise ValueError("ambiguous sync state: fixture source identity changed")
    for relative, expected in initial_entries.items():
        source = source_root / relative
        _reject_relative_symlinks(source_root, PurePosixPath(relative), "projection source")
        if expected.type == "file" and not source.is_file():
            raise ValueError(f"ambiguous sync state: projected source changed: {relative}")
        if expected.type == "directory" and not source.is_dir():
            raise ValueError(f"ambiguous sync state: projected source changed: {relative}")
        if _projection_entry(source, source_root) != expected:
            raise ValueError(f"ambiguous sync state: projected source changed: {relative}")

    synchronized = tuple(PurePosixPath(path) for path in projection.sync_paths)
    for relative in synchronized:
        _validate_unused_sync_destination(source_root, relative)

    current_entries = {
        entry.path: entry
        for entry in _projection_product_entries(
            projection_root,
            include_runner_owned=True,
        )
    }
    mutations: list[ProjectionMutation] = []
    mutation_content: dict[str, bytes] = {}
    mutation_bytes = 0
    added_directories: list[ProjectedFile] = []
    for relative in sorted(set(sealed_entries) | set(current_entries)):
        before = sealed_entries.get(relative)
        after = current_entries.get(relative)
        if before == after:
            continue
        if before is not None:
            label = "runner-owned context" if _is_runner_owned(Path(relative)) else "projected input"
            raise ValueError(f"ambiguous sync state: {label} was modified: {relative}")
        if after is None or _is_runner_owned(Path(relative)):
            raise ValueError(f"unexpected model output in projected workspace: {relative}")
        if after.type == "directory":
            added_directories.append(after)
            continue
        if not any(_path_is_selected(Path(relative), selected) for selected in synchronized):
            raise ValueError(f"unexpected model output in projected workspace: {relative}")
        if len(mutations) >= _MAX_PROJECTION_OUTPUT_FILES:
            raise ValueError("projected workspace exceeded the output file limit")
        assert after.size is not None and after.digest is not None
        mutation_bytes += after.size
        if mutation_bytes > _MAX_PROJECTION_OUTPUT_BYTES:
            raise ValueError("projected workspace exceeded the output byte limit")
        source_content = (projection_root / relative).read_bytes()
        if hashlib.sha256(source_content).hexdigest() != after.digest:
            raise ValueError(f"ambiguous sync state: projected output changed during capture: {relative}")
        mutations.append(ProjectionMutation(
            path=relative,
            action="create",
            before_digest=None,
            after_digest=after.digest,
            size=after.size,
            mode=after.mode,
            retained_evidence="",
        ))
        mutation_content[relative] = source_content

    required_directories: set[str] = set()
    for mutation in mutations:
        for parent in PurePosixPath(mutation.path).parents:
            if parent.as_posix() == ".":
                continue
            if parent.as_posix() not in original_source_entries:
                required_directories.add(parent.as_posix())
    observed_directories = {entry.path for entry in added_directories}
    if observed_directories != required_directories:
        unexplained = sorted(observed_directories - required_directories)
        missing = sorted(required_directories - observed_directories)
        detail = unexplained[0] if unexplained else missing[0]
        raise ValueError(
            "unexpected model output directory in projected workspace: "
            f"{detail}"
        )

    evidence_path = _validate_projection_evidence_path(
        evidence_path,
        source_root,
        projection_root,
    )
    projection_manifest_digest = (
        projection_manifest.manifest_digest
        if projection_manifest is not None
        else projection.manifest_digest
    )
    projected_inputs = (
        list(projection_manifest.projected_inputs)
        if projection_manifest is not None
        else [entry.__dict__ for entry in projection.files]
    )
    prepared_entries = (
        list(projection_manifest.prepared_entries)
        if projection_manifest is not None
        else [entry.__dict__ for entry in projection.source_files]
    )
    retained_paths: list[Path] = []
    mutation_records: list[dict[str, object]] = []
    mutation_values: list[ProjectionMutation] = []
    for mutation in mutations:
        retained_path, retained_reference = _retain_projection_bytes(
            evidence_path.parent,
            "synchronized-output",
            mutation.path,
            mutation.mode,
            mutation_content[mutation.path],
        )
        retained_paths.append(retained_path)
        retained_mutation = replace(mutation, retained_evidence=retained_reference)
        mutation_values.append(retained_mutation)
        mutation_records.append(_projection_mutation_record(retained_mutation))

    created_files: list[Path] = []
    created_directories: list[Path] = []
    try:
        directory_modes = {
            entry.path: entry.mode for entry in added_directories
        }
        for mutation in mutation_values:
            destination = source_root / mutation.path
            created_directories.extend(
                _create_safe_destination_parents(
                    source_root,
                    destination.parent,
                    directory_modes,
                    original_source_entries,
                    {
                        path.relative_to(source_root).as_posix()
                        for path in created_directories
                    },
                )
            )
            try:
                _write_projection_output_exclusive(
                    destination,
                    mutation_content[mutation.path],
                    mutation.mode,
                )
            except FileExistsError as error:
                raise ValueError(
                    f"ambiguous sync state: source changed at destination: {mutation.path}"
                ) from error
            created_files.append(destination)

        expected_post_entries = dict(original_source_entries)
        expected_post_entries.update({entry.path: entry for entry in added_directories})
        for mutation in mutation_values:
            expected_post_entries[mutation.path] = ProjectedFile(
                path=mutation.path,
                type="file",
                mode=mutation.mode,
                digest=mutation.after_digest,
                size=mutation.size,
            )
        actual_post_entries = {
            entry.path: entry
            for entry in _projection_product_entries(
                source_root,
                include_runner_owned=False,
            )
        }
        if actual_post_entries != expected_post_entries:
            changed = sorted(
                relative
                for relative in set(actual_post_entries) | set(expected_post_entries)
                if actual_post_entries.get(relative) != expected_post_entries.get(relative)
            )
            detail = changed[0] if changed else "unknown"
            raise ValueError(
                "ambiguous sync state: concurrent fixture post-state change: "
                f"{detail}"
            )
        post_sync_source_identity_digest = _projection_entries_digest(
            tuple(expected_post_entries[path] for path in sorted(expected_post_entries))
        )
        directory_payload = [
            {"path": entry.path, "mode": entry.mode}
            for entry in sorted(added_directories, key=lambda item: item.path)
        ]
        payload = {
            "schema": "dev-methodology-eval-model-visible-projection-sync",
            "version": 3,
            "preparedSnapshotDigest": projection.prepared_snapshot_digest,
            "sourceIdentityDigest": projection.source_identity_digest,
            "postSyncSourceIdentityDigest": post_sync_source_identity_digest,
            "projectionManifestDigest": projection_manifest_digest,
            "preparedEntries": prepared_entries,
            "modelVisiblePaths": list(projection.model_visible_paths),
            "evaluatorOnlyPaths": list(projection.evaluator_only_paths),
            "projectedInputs": projected_inputs,
            "syncPaths": list(projection.sync_paths),
            "createdDirectories": directory_payload,
            "mutations": mutation_records,
        }
        manifest_digest = hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        _write_json_exclusive(
            evidence_path,
            {**payload, "manifestDigest": manifest_digest},
        )
    except Exception:
        for created in reversed(created_files):
            if created.is_file() and not created.is_symlink():
                created.unlink()
        for created in reversed(created_directories):
            try:
                created.rmdir()
            except OSError:
                pass
        evidence_path.unlink(missing_ok=True)
        for retained in retained_paths:
            retained.unlink(missing_ok=True)
        raise

    return ProjectionSyncManifest(
        evidence_path=evidence_path,
        manifest_digest=manifest_digest,
        mutations=tuple(mutation_values),
        mutation_records=tuple(mutation_records),
        created_directories=tuple(directory_payload),
        post_sync_source_identity_digest=post_sync_source_identity_digest,
    )


def write_model_visible_projection_manifest(
    projection: ModelVisibleProjection,
    evidence_path: Path,
) -> ProjectionManifestEvidence:
    """Retain the exact source partition and copied input identities outside both workspaces."""

    evidence_path = _validate_projection_evidence_path(
        evidence_path,
        projection.source_root,
        projection.root,
    )
    projected_inputs: list[dict[str, object]] = []
    retained_paths: list[Path] = []
    for entry in projection.files:
        record = dict(entry.__dict__)
        retained_evidence: str | None = None
        if entry.type == "file":
            retained_path, retained_evidence = _retain_projection_bytes(
                evidence_path.parent,
                "projected-input",
                entry.path,
                entry.mode,
                (projection.root / entry.path).read_bytes(),
            )
            retained_paths.append(retained_path)
        record["retainedEvidence"] = retained_evidence
        projected_inputs.append(record)
    payload = {
        "schema": "dev-methodology-eval-model-visible-projection",
        "version": 3,
        "preparedSnapshotDigest": projection.prepared_snapshot_digest,
        "sourceIdentityDigest": projection.source_identity_digest,
        "preparedEntries": [entry.__dict__ for entry in projection.source_files],
        "modelVisiblePaths": list(projection.model_visible_paths),
        "evaluatorOnlyPaths": list(projection.evaluator_only_paths),
        "syncPaths": list(projection.sync_paths),
        "projectedInputs": projected_inputs,
    }
    manifest_digest = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    try:
        _write_json_exclusive(
            evidence_path,
            {**payload, "manifestDigest": manifest_digest},
        )
    except Exception:
        for retained in retained_paths:
            retained.unlink(missing_ok=True)
        raise
    return ProjectionManifestEvidence(
        evidence_path=evidence_path,
        content_digest=hashlib.sha256(evidence_path.read_bytes()).hexdigest(),
        manifest_digest=manifest_digest,
        prepared_entries=tuple(entry.__dict__ for entry in projection.source_files),
        projected_inputs=tuple(projected_inputs),
    )


def build_input_manifest(root: Path, allowed_paths: Sequence[str]) -> InputManifest:
    """Inventory and scan the effective allowlisted model-visible files before invocation."""

    root = root.resolve()
    allowed = tuple(_safe_relative_path(path) for path in allowed_paths)
    files: list[ContextFile] = []
    for path in _iter_allowed_files(root, allowed):
        relative = path.relative_to(root).as_posix()
        content = path.read_bytes()
        _reject_sensitive(relative, content)
        files.append(ContextFile(
            source_path=relative,
            destination_path=relative,
            content_digest=hashlib.sha256(content).hexdigest(),
            effective_digest=hashlib.sha256(content).hexdigest(),
            size=len(content),
            context_role="model-visible-input",
            sanitizations=(),
        ))
    uncovered = [
        path.relative_to(root).as_posix()
        for path in _walk_pruned(root)
        if not _is_runner_owned(path.relative_to(root))
        and not any(_path_is_selected(path.relative_to(root), selected) for selected in allowed)
    ]
    if uncovered:
        raise ValueError(f"model-visible allowlist omits workspace file: {sorted(uncovered)[0]}")
    if not files:
        raise ValueError("model-visible input allowlist selected no files")
    return InputManifest(tuple(files), _manifest_digest(files))


def _normalized_disjoint_paths(
    values: Sequence[str],
    label: str,
) -> tuple[PurePosixPath, ...]:
    normalized = tuple(_safe_relative_path(value) for value in values)
    if label == "model-visible" and not normalized:
        raise ValueError("model-visible projection must select at least one source path")
    if len(normalized) != len(set(normalized)):
        raise ValueError(f"{label} projection paths contain a duplicate destination collision")
    for index, path in enumerate(normalized):
        for other in normalized[index + 1:]:
            if _relative_projection_paths_overlap(path, other):
                raise ValueError(f"{label} projection paths overlap: {path} and {other}")
    return normalized


def _reject_projection_path_overlap(
    left: Sequence[PurePosixPath],
    right: Sequence[PurePosixPath],
    left_label: str,
    right_label: str,
) -> None:
    for left_path in left:
        for right_path in right:
            if _relative_projection_paths_overlap(left_path, right_path):
                raise ValueError(
                    f"model-visible projection {left_label} and {right_label} paths overlap: "
                    f"{left_path} and {right_path}"
                )


def _relative_projection_paths_overlap(
    left: PurePosixPath,
    right: PurePosixPath,
) -> bool:
    return left == right or left in right.parents or right in left.parents


def _selected_projection_entries(
    root: Path,
    selected_paths: Sequence[PurePosixPath],
    label: str,
    available: Mapping[str, ProjectedFile],
    *,
    allow_empty_selection: bool = False,
) -> dict[str, ProjectedFile]:
    entries: dict[str, ProjectedFile] = {}
    for relative in selected_paths:
        _reject_relative_symlinks(root, relative, label)
        selected = root / relative
        if not selected.exists():
            raise ValueError(f"declared {label} projection path is missing: {relative}")
        selected_entries = {
            path: entry
            for path, entry in available.items()
            if _path_is_selected(Path(path), relative)
        }
        if not selected_entries and not allow_empty_selection:
            raise ValueError(f"declared {label} projection path selected no entries: {relative}")
        overlap = set(entries) & set(selected_entries)
        if overlap:
            raise ValueError(
                f"{label} projection destination collision: {sorted(overlap)[0]}"
            )
        entries.update(selected_entries)
    return entries


def _reject_relative_symlinks(
    root: Path,
    relative: PurePosixPath,
    label: str,
) -> None:
    current = root
    for part in relative.parts:
        current /= part
        if current.is_symlink():
            raise ValueError(f"{label} path contains a symlink: {relative}")


def _validate_unused_sync_destination(root: Path, relative: PurePosixPath) -> None:
    _reject_relative_symlinks(root, relative, "projection sync")
    destination = root / relative
    if destination.exists() or destination.is_symlink():
        raise ValueError(f"projection sync destination collision: {relative}")
    current = root
    for part in relative.parts[:-1]:
        current /= part
        if current.exists() and not current.is_dir():
            raise ValueError(f"projection sync destination collision: {relative}")


def _projection_source_identity(root: Path) -> str:
    return _projection_entries_digest(
        _projection_product_entries(root, include_runner_owned=False)
    )


def _projection_product_entries(
    root: Path,
    *,
    include_runner_owned: bool,
) -> tuple[ProjectedFile, ...]:
    entries: list[ProjectedFile] = []
    for directory, directory_names, file_names in os.walk(
        root,
        topdown=True,
        followlinks=False,
    ):
        current = Path(directory)
        retained_directories: list[str] = []
        for name in sorted(directory_names):
            path = current / name
            relative = path.relative_to(root)
            if not include_runner_owned and _is_runner_owned(relative):
                continue
            if path.is_symlink():
                raise ValueError(
                    f"projected workspace contains a directory symlink: {relative}"
                )
            if not path.is_dir():
                raise ValueError(
                    f"projected workspace contains an unsupported entry: {relative}"
                )
            retained_directories.append(name)
            entries.append(_projection_entry(path, root))
        directory_names[:] = retained_directories
        for name in sorted(file_names):
            path = current / name
            relative = path.relative_to(root)
            if not include_runner_owned and _is_runner_owned(relative):
                continue
            if path.is_symlink():
                raise ValueError(
                    f"projected workspace contains a file symlink: {relative}"
                )
            if not path.is_file():
                raise ValueError(
                    f"projected workspace contains an unsupported entry: {relative}"
                )
            entries.append(_projection_entry(path, root))
    return tuple(sorted(entries, key=lambda entry: entry.path))


def _projection_entry(path: Path, root: Path) -> ProjectedFile:
    relative = path.relative_to(root).as_posix()
    mode = _entry_mode(path)
    if path.is_dir():
        return ProjectedFile(relative, "directory", mode, None, None)
    content = path.read_bytes()
    return ProjectedFile(
        relative,
        "file",
        mode,
        hashlib.sha256(content).hexdigest(),
        len(content),
    )


def _entry_mode(path: Path) -> str:
    return format(stat.S_IMODE(path.lstat().st_mode), "03o")


def _projection_entries_digest(entries: Sequence[ProjectedFile]) -> str:
    snapshot = {
        entry.path: (
            f"dir:{entry.mode}"
            if entry.type == "directory"
            else f"file:{entry.mode}:{entry.digest}"
        )
        for entry in entries
    }
    return snapshot_digest(snapshot)


def _validate_projection_evidence_path(
    evidence_path: Path,
    source_root: Path,
    projection_root: Path,
) -> Path:
    if evidence_path.exists() or evidence_path.is_symlink():
        raise ValueError("projection sync evidence destination must be unused")
    if evidence_path.parent.is_symlink():
        raise ValueError("projection sync evidence parent must not be a symlink")
    evidence_path.parent.mkdir(parents=True, mode=0o700, exist_ok=True)
    os.chmod(evidence_path.parent, 0o700)
    evidence_path = evidence_path.resolve()
    if (
        evidence_path == source_root
        or source_root in evidence_path.parents
        or evidence_path == projection_root
        or projection_root in evidence_path.parents
    ):
        raise ValueError("projection sync evidence must stay outside both workspaces")
    return evidence_path


def _create_safe_destination_parents(
    root: Path,
    destination_parent: Path,
    directory_modes: Mapping[str, str],
    original_source_entries: Mapping[str, ProjectedFile],
    task_created_directories: set[str],
) -> list[Path]:
    if destination_parent == root:
        return []
    try:
        relative = destination_parent.relative_to(root)
    except ValueError as error:
        raise ValueError("projection sync destination escapes the source root") from error
    current = root
    created: list[Path] = []
    for part in relative.parts:
        current /= part
        relative_current = current.relative_to(root).as_posix()
        if relative_current in original_source_entries:
            expected = original_source_entries[relative_current]
            if (
                current.is_symlink()
                or not current.is_dir()
                or expected.type != "directory"
                or _projection_entry(current, root) != expected
            ):
                raise ValueError("projection sync destination parent is unsafe")
            continue
        if relative_current in task_created_directories:
            if current.is_symlink() or not current.is_dir():
                raise ValueError("projection sync destination parent is unsafe")
            continue
        try:
            current.mkdir(mode=int(directory_modes[relative_current], 8))
        except FileExistsError as error:
            raise ValueError(
                "ambiguous sync state: concurrent source parent appeared: "
                f"{relative_current}"
            ) from error
        os.chmod(current, int(directory_modes[relative_current], 8))
        created.append(current)
        task_created_directories.add(relative_current)
    return created


def _write_projection_output_exclusive(
    destination: Path,
    content: bytes,
    mode: str,
) -> None:
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(destination, flags, int(mode, 8))
    try:
        with os.fdopen(descriptor, "wb") as stream:
            descriptor = -1
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(destination, int(mode, 8))
    except Exception:
        if descriptor >= 0:
            os.close(descriptor)
        destination.unlink(missing_ok=True)
        raise


def _retain_projection_bytes(
    evidence_root: Path,
    kind: str,
    relative: str,
    mode: str,
    content: bytes,
) -> tuple[Path, str]:
    retained_root = evidence_root / "retained-bytes"
    retained_root.mkdir(mode=0o700, exist_ok=True)
    os.chmod(retained_root, 0o700)
    identity = hashlib.sha256(f"{kind}\0{relative}".encode("utf-8")).hexdigest()
    artifact = retained_root / f"{identity}.json"
    digest = hashlib.sha256(content).hexdigest()
    marker = "dev-methodology-eval-projection-retained-bytes"
    _write_json_exclusive(
        artifact,
        {
            "schema": marker,
            "version": 1,
            "kind": kind,
            "path": relative,
            "mode": mode,
            "digest": digest,
            "size": len(content),
            "contentBase64": base64.b64encode(content).decode("ascii"),
        },
    )
    reference = f"{artifact.relative_to(evidence_root).as_posix()}#{marker}"
    return artifact, reference


def _projection_mutation_record(mutation: ProjectionMutation) -> dict[str, object]:
    return {
        "path": mutation.path,
        "action": mutation.action,
        "beforeDigest": mutation.before_digest,
        "afterDigest": mutation.after_digest,
        "size": mutation.size,
        "mode": mutation.mode,
        "retainedEvidence": mutation.retained_evidence,
    }


def _write_json_exclusive(path: Path, value: Mapping[str, object]) -> None:
    content = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags, 0o600)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            descriptor = -1
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
    except Exception:
        if descriptor >= 0:
            os.close(descriptor)
        path.unlink(missing_ok=True)
        raise
    os.chmod(path, 0o600)


def _path_is_selected(path: Path, selected: PurePosixPath) -> bool:
    selected_path = Path(selected.as_posix())
    return selected_path == Path(".") or path == selected_path or selected_path in path.parents


def _is_runner_owned(path: Path) -> bool:
    return path.name in _RUNNER_OWNED_FILES or bool(path.parts and path.parts[0] in _RUNNER_OWNED_ROOTS)


def _iter_allowed_files(root: Path, allowed: tuple[PurePosixPath, ...]) -> Iterable[Path]:
    seen: set[Path] = set()
    for relative in allowed:
        selected = (root / relative).resolve()
        if selected != root and root not in selected.parents:
            raise ValueError(f"model-visible input path escapes the workspace: {relative}")
        if selected.is_file():
            candidates: Iterable[Path] = (selected,)
        elif selected.is_dir():
            candidates = _walk_pruned(selected)
        else:
            raise ValueError(f"model-visible input path is missing: {relative}")
        for path in candidates:
            if path not in seen:
                seen.add(path)
                yield path


def _walk_pruned(root: Path) -> Iterable[Path]:
    import os

    for directory, directory_names, file_names in os.walk(root, topdown=True, followlinks=False):
        current = Path(directory)
        retained_directories: list[str] = []
        for name in sorted(directory_names):
            path = current / name
            if path.is_symlink():
                raise ValueError(
                    f"model-visible input contains a directory symlink: {path.relative_to(root)}"
                )
            if name not in TRANSIENT_TREE_NAMES:
                retained_directories.append(name)
        directory_names[:] = retained_directories
        for name in sorted(file_names):
            path = current / name
            if path.is_symlink():
                raise ValueError(
                    f"model-visible input contains a file symlink: {path.relative_to(root)}"
                )
            if path.is_file():
                yield path


def _safe_relative_path(value: str | PurePosixPath) -> PurePosixPath:
    path = PurePosixPath(value)
    if path.is_absolute() or not path.parts or any(part in {"", ".", ".."} for part in path.parts):
        if str(path) != ".":
            raise ValueError(f"context paths must be normalized relative paths: {value}")
    return path


def _reject_sensitive(path: str, content: bytes) -> None:
    for label, pattern in _SENSITIVE_PATTERNS:
        if pattern.search(content):
            raise ValueError(f"sensitive input rejected in {path}: {label}")


def _sanitize_selected_context(context_role: str, content: bytes) -> tuple[bytes, tuple[str, ...]]:
    if context_role not in {"agent-definition", "harness-required-skill", "treatment-skill"}:
        return content, ()
    sanitized = content
    actions: list[str] = []
    mandated_email = b"Martin.Bechard@DevConsult.ca"
    if mandated_email in sanitized:
        sanitized = sanitized.replace(
            mandated_email, b"[redacted-eval-copyright-holder]"
        )
        actions.append("redacted-mandated-copyright-email")
    if _EMAIL_PATTERN.search(sanitized):
        sanitized = _EMAIL_PATTERN.sub(b"[redacted-eval-email]", sanitized)
        actions.append("redacted-context-email")
    return sanitized, tuple(actions)


def _manifest_digest(files: Sequence[ContextFile]) -> str:
    payload = [
        {
            "sourcePath": file.source_path,
            "destinationPath": file.destination_path,
            "contentDigest": file.content_digest,
            "effectiveDigest": file.effective_digest,
            "size": file.size,
            "contextRole": file.context_role,
            "sanitizations": list(file.sanitizations),
        }
        for file in sorted(files, key=lambda item: (item.destination_path, item.source_path))
    ]
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
