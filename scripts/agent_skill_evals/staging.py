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
    McpAgentOpsContext,
    McpAgentOpsIdentity,
    junie_mcp_agent_ops_authorization_payload,
    mcp_agent_ops_configuration_payload,
)
from .workspace import TRANSIENT_TREE_NAMES


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
        authorization_payload = junie_mcp_agent_ops_authorization_payload()
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
