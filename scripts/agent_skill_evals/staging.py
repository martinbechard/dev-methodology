# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Builds allowlisted harness context overlays and rejects sensitive model-visible inputs.

from __future__ import annotations

import hashlib
import json
import os
import re
import secrets
import shutil
from dataclasses import dataclass
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
    snapshot_tree,
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
    """Record one source file copied into an isolated model-visible workspace."""

    path: str
    digest: str
    size: int


@dataclass(frozen=True)
class ProjectionMutation:
    """Record one allowlisted model-created file synchronized to the full fixture."""

    path: str
    action: str
    before_digest: str | None
    after_digest: str
    size: int


@dataclass(frozen=True)
class ModelVisibleProjection:
    """Bind an isolated harness workspace to its complete fixture partition."""

    source_root: Path
    root: Path
    files: tuple[ProjectedFile, ...]
    manifest_digest: str
    source_identity_digest: str
    source_files: tuple[ProjectedFile, ...]
    model_visible_paths: tuple[str, ...]
    evaluator_only_paths: tuple[str, ...]
    sync_paths: tuple[str, ...]
    initial_directories: tuple[str, ...]


@dataclass(frozen=True)
class ProjectionSyncManifest:
    """Describe the applied projection mutations and their durable evidence file."""

    evidence_path: Path
    manifest_digest: str
    mutations: tuple[ProjectionMutation, ...]


@dataclass(frozen=True)
class ProjectionManifestEvidence:
    """Describe a retained replayable projection-manifest artifact."""

    evidence_path: Path
    content_digest: str


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

    visible_files = _selected_projection_files(source_root, visible, "model-visible")
    evaluator_files = _selected_projection_files(
        source_root,
        evaluator_only,
        "evaluator-only",
        allow_empty_selection=True,
    )
    all_source_files = {
        path.relative_to(source_root).as_posix()
        for path in _walk_pruned(source_root)
        if not _is_runner_owned(path.relative_to(source_root))
    }
    partitioned = set(visible_files) | set(evaluator_files)
    undeclared = sorted(all_source_files - partitioned)
    if undeclared:
        raise ValueError(f"model-visible projection has undeclared source file: {undeclared[0]}")
    if partitioned - all_source_files:
        raise ValueError("model-visible projection partition contains an unavailable source file")
    for relative in synchronized:
        _validate_unused_sync_destination(source_root, relative)

    source_files = tuple(
        ProjectedFile(
            path=relative,
            digest=hashlib.sha256((source_root / relative).read_bytes()).hexdigest(),
            size=(source_root / relative).stat().st_size,
        )
        for relative in sorted(all_source_files)
    )
    source_file_map = {file.path: file for file in source_files}
    source_identity_digest = _projection_source_identity(source_root)

    destination_root.mkdir(mode=0o700)
    projected_files: list[ProjectedFile] = []
    try:
        for relative in sorted(visible_files):
            source = source_root / relative
            destination = destination_root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            content = source.read_bytes()
            expected = source_file_map[relative]
            if (
                len(content) != expected.size
                or hashlib.sha256(content).hexdigest() != expected.digest
            ):
                raise ValueError(
                    f"model-visible projection source changed during copy: {relative}"
                )
            destination.write_bytes(content)
            shutil.copymode(source, destination)
            projected_files.append(ProjectedFile(
                path=relative,
                digest=hashlib.sha256(content).hexdigest(),
                size=len(content),
            ))
        if _projection_source_identity(source_root) != source_identity_digest:
            raise ValueError("model-visible projection source changed during staging")
    except Exception:
        shutil.rmtree(destination_root, ignore_errors=True)
        raise

    initial_directories = tuple(sorted({
        parent.as_posix()
        for file in projected_files
        for parent in PurePosixPath(file.path).parents
        if parent.as_posix() != "."
    }))
    payload = {
        "schema": "dev-methodology-eval-model-visible-projection",
        "version": 1,
        "sourceIdentityDigest": source_identity_digest,
        "modelVisiblePaths": [path.as_posix() for path in visible],
        "evaluatorOnlyPaths": [path.as_posix() for path in evaluator_only],
        "syncPaths": [path.as_posix() for path in synchronized],
        "projectedInputs": [file.__dict__ for file in projected_files],
    }
    manifest_digest = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return ModelVisibleProjection(
        source_root=source_root,
        root=destination_root,
        files=tuple(projected_files),
        manifest_digest=manifest_digest,
        source_identity_digest=source_identity_digest,
        source_files=source_files,
        model_visible_paths=tuple(path.as_posix() for path in visible),
        evaluator_only_paths=tuple(path.as_posix() for path in evaluator_only),
        sync_paths=tuple(path.as_posix() for path in synchronized),
        initial_directories=initial_directories,
    )


def synchronize_model_visible_projection(
    projection: ModelVisibleProjection,
    evidence_path: Path,
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

    initial_files = {file.path: file for file in projection.files}
    original_source_files = {file.path: file for file in projection.source_files}
    current_source_files = {
        path.relative_to(source_root).as_posix(): ProjectedFile(
            path=path.relative_to(source_root).as_posix(),
            digest=hashlib.sha256(path.read_bytes()).hexdigest(),
            size=path.stat().st_size,
        )
        for path in _walk_pruned(source_root)
        if not _is_runner_owned(path.relative_to(source_root))
    }
    if current_source_files != original_source_files:
        changed = sorted(
            relative
            for relative in set(current_source_files) | set(original_source_files)
            if current_source_files.get(relative) != original_source_files.get(relative)
        )
        detail = changed[0] if changed else "unknown"
        raise ValueError(f"ambiguous sync state: fixture source changed: {detail}")
    if _projection_source_identity(source_root) != projection.source_identity_digest:
        raise ValueError("ambiguous sync state: fixture source identity changed")
    for relative, expected in initial_files.items():
        source = source_root / relative
        _reject_relative_symlinks(source_root, PurePosixPath(relative), "projection source")
        if not source.is_file():
            raise ValueError(f"ambiguous sync state: projected source changed: {relative}")
        content = source.read_bytes()
        if (
            len(content) != expected.size
            or hashlib.sha256(content).hexdigest() != expected.digest
        ):
            raise ValueError(f"ambiguous sync state: projected source changed: {relative}")

    synchronized = tuple(PurePosixPath(path) for path in projection.sync_paths)
    for relative in synchronized:
        _validate_unused_sync_destination(source_root, relative)

    current_files, current_directories = _projection_product_snapshot(projection_root)
    mutations: list[ProjectionMutation] = []
    mutation_content: dict[str, bytes] = {}
    mutation_bytes = 0
    for relative in sorted(set(initial_files) | set(current_files)):
        before = initial_files.get(relative)
        after = current_files.get(relative)
        if before == after:
            continue
        if after is None or not any(
            _path_is_selected(Path(relative), selected) for selected in synchronized
        ):
            raise ValueError(f"unexpected model output in projected workspace: {relative}")
        if before is not None:
            raise ValueError(f"ambiguous sync state: projected input was modified: {relative}")
        if len(mutations) >= _MAX_PROJECTION_OUTPUT_FILES:
            raise ValueError("projected workspace exceeded the output file limit")
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
        ))
        mutation_content[relative] = source_content

    initial_directories = set(projection.initial_directories)
    added_directories = current_directories - initial_directories
    mutation_paths = tuple(PurePosixPath(item.path) for item in mutations)
    for relative in sorted(added_directories):
        directory = PurePosixPath(relative)
        if not any(directory in path.parents for path in mutation_paths):
            raise ValueError(f"unexpected model output directory in projected workspace: {relative}")

    projected_inputs = [file.__dict__ for file in projection.files]
    mutation_payload = [
        {
            "path": item.path,
            "action": item.action,
            "beforeDigest": item.before_digest,
            "afterDigest": item.after_digest,
            "size": item.size,
        }
        for item in mutations
    ]
    payload = {
        "schema": "dev-methodology-eval-model-visible-projection-sync",
        "version": 1,
        "sourceIdentityDigest": projection.source_identity_digest,
        "projectionManifestDigest": projection.manifest_digest,
        "modelVisiblePaths": list(projection.model_visible_paths),
        "evaluatorOnlyPaths": list(projection.evaluator_only_paths),
        "projectedInputs": projected_inputs,
        "syncPaths": list(projection.sync_paths),
        "mutations": mutation_payload,
    }
    manifest_digest = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    evidence = {**payload, "manifestDigest": manifest_digest}
    evidence_path = _validate_projection_evidence_path(
        evidence_path,
        source_root,
        projection_root,
    )
    temporary_evidence = evidence_path.with_name(
        f".{evidence_path.name}.pending-{secrets.token_hex(8)}"
    )
    temporary_evidence.write_text(
        json.dumps(evidence, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.chmod(temporary_evidence, 0o600)

    created_files: list[Path] = []
    created_directories: list[Path] = []
    try:
        for mutation in mutations:
            destination = source_root / mutation.path
            created_directories.extend(
                _create_safe_destination_parents(source_root, destination.parent)
            )
            if destination.exists() or destination.is_symlink():
                raise ValueError(
                    f"ambiguous sync state: source changed at destination: {mutation.path}"
                )
            temporary_destination = destination.with_name(
                f".{destination.name}.pending-{secrets.token_hex(8)}"
            )
            try:
                temporary_destination.write_bytes(mutation_content[mutation.path])
                os.chmod(temporary_destination, 0o600)
                os.replace(temporary_destination, destination)
            finally:
                if temporary_destination.exists():
                    temporary_destination.unlink()
            created_files.append(destination)
        os.link(temporary_evidence, evidence_path)
        temporary_evidence.unlink()
    except Exception:
        for created in reversed(created_files):
            if created.is_file() and not created.is_symlink():
                created.unlink()
        for created in reversed(created_directories):
            try:
                created.rmdir()
            except OSError:
                pass
        if temporary_evidence.exists():
            temporary_evidence.unlink()
        raise

    return ProjectionSyncManifest(
        evidence_path=evidence_path,
        manifest_digest=manifest_digest,
        mutations=tuple(mutations),
    )


def write_model_visible_projection_manifest(
    projection: ModelVisibleProjection,
    evidence_path: Path,
) -> ProjectionManifestEvidence:
    """Retain the exact source partition and copied input identities outside both workspaces."""

    payload = {
        "schema": "dev-methodology-eval-model-visible-projection",
        "version": 1,
        "sourceIdentityDigest": projection.source_identity_digest,
        "modelVisiblePaths": list(projection.model_visible_paths),
        "evaluatorOnlyPaths": list(projection.evaluator_only_paths),
        "syncPaths": list(projection.sync_paths),
        "projectedInputs": [file.__dict__ for file in projection.files],
        "manifestDigest": projection.manifest_digest,
    }
    evidence_path = _validate_projection_evidence_path(
        evidence_path,
        projection.source_root,
        projection.root,
    )
    temporary = evidence_path.with_name(
        f".{evidence_path.name}.pending-{secrets.token_hex(8)}"
    )
    try:
        temporary.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        os.chmod(temporary, 0o600)
        os.link(temporary, evidence_path)
        temporary.unlink()
    finally:
        if temporary.exists():
            temporary.unlink()
    return ProjectionManifestEvidence(
        evidence_path=evidence_path,
        content_digest=hashlib.sha256(evidence_path.read_bytes()).hexdigest(),
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


def _selected_projection_files(
    root: Path,
    selected_paths: Sequence[PurePosixPath],
    label: str,
    *,
    allow_empty_selection: bool = False,
) -> dict[str, Path]:
    files: dict[str, Path] = {}
    for relative in selected_paths:
        _reject_relative_symlinks(root, relative, label)
        selected = root / relative
        if not selected.exists():
            raise ValueError(f"declared {label} projection path is missing: {relative}")
        candidates = (selected,) if selected.is_file() else _walk_pruned(selected)
        selected_file_count = 0
        for path in candidates:
            if not path.is_file():
                continue
            relative_file = path.relative_to(root).as_posix()
            if _is_runner_owned(Path(relative_file)):
                continue
            if relative_file in files:
                raise ValueError(f"{label} projection destination collision: {relative_file}")
            files[relative_file] = path
            selected_file_count += 1
        if not allow_empty_selection and selected_file_count == 0:
            raise ValueError(f"declared {label} projection path selected no files: {relative}")
    return files


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


def _projection_product_snapshot(
    root: Path,
) -> tuple[dict[str, ProjectedFile], set[str]]:
    files: dict[str, ProjectedFile] = {}
    directories: set[str] = set()
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
            if _is_runner_owned(relative) or name in TRANSIENT_TREE_NAMES:
                continue
            if path.is_symlink():
                raise ValueError(
                    f"projected workspace contains a directory symlink: {relative}"
                )
            retained_directories.append(name)
            directories.add(relative.as_posix())
        directory_names[:] = retained_directories
        for name in sorted(file_names):
            path = current / name
            relative = path.relative_to(root)
            if _is_runner_owned(relative):
                continue
            if path.is_symlink():
                raise ValueError(
                    f"projected workspace contains a file symlink: {relative}"
                )
            if not path.is_file():
                raise ValueError(f"projected workspace contains an unsupported entry: {relative}")
            content = path.read_bytes()
            files[relative.as_posix()] = ProjectedFile(
                path=relative.as_posix(),
                digest=hashlib.sha256(content).hexdigest(),
                size=len(content),
            )
    return files, directories


def _projection_source_identity(root: Path) -> str:
    snapshot = snapshot_tree(
        root,
        exclude_transient=True,
        excluded_top_level_names=_RUNNER_OWNED_ROOTS,
    )
    for marker in _RUNNER_OWNED_FILES:
        snapshot.pop(marker, None)
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
    evidence_path.parent.mkdir(parents=True, exist_ok=True)
    evidence_path = evidence_path.resolve()
    if (
        evidence_path == source_root
        or source_root in evidence_path.parents
        or evidence_path == projection_root
        or projection_root in evidence_path.parents
    ):
        raise ValueError("projection sync evidence must stay outside both workspaces")
    return evidence_path


def _create_safe_destination_parents(root: Path, destination_parent: Path) -> list[Path]:
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
        if current.is_symlink() or (current.exists() and not current.is_dir()):
            raise ValueError("projection sync destination parent is unsafe")
        if not current.exists():
            current.mkdir()
            created.append(current)
    return created


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
