# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Builds allowlisted harness context overlays and rejects sensitive model-visible inputs.

from __future__ import annotations

import hashlib
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable, Sequence

from .invocations import SUPPORTED_HARNESSES
from .workspace import TRANSIENT_TREE_NAMES


_SENSITIVE_PATTERNS = (
    ("email address", re.compile(rb"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.IGNORECASE)),
    ("private key", re.compile(rb"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("secret assignment", re.compile(rb"(?:api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]", re.IGNORECASE)),
    ("sensitive marker", re.compile(rb"(?:company|customer)[_ -]?(?:confidential|internal)", re.IGNORECASE)),
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
        directory_names[:] = [
            name for name in sorted(directory_names)
            if name not in TRANSIENT_TREE_NAMES
        ]
        current = Path(directory)
        for name in sorted(file_names):
            path = current / name
            if path.is_file() and not path.is_symlink():
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
    mandated_email = b"Martin.Bechard@DevConsult.ca"
    if mandated_email not in content:
        return content, ()
    return (
        content.replace(mandated_email, b"[redacted-eval-copyright-holder]"),
        ("redacted-mandated-copyright-email",),
    )


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
