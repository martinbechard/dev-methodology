#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Modified with AI assistance.
# Summary: Installs or removes bundle-owned skills and agents at scoped or explicit destinations.

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
from collections.abc import Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import NamedTuple, Optional


SUCCESS_EXIT_CODE = 0
ERROR_EXIT_CODE = 1
MANIFEST_SCHEMA_VERSION = 1
DEFAULT_SKILLS_FOLDER_NAME = "skills"
DEFAULT_ADAPTER_NAME = "generic"
USER_SCOPE = "user"
PROJECT_SCOPE = "project"
DEPLOYMENT_SCOPES = (USER_SCOPE, PROJECT_SCOPE)
GENERIC_ADAPTER_NAME = "generic"
CODEX_ADAPTER_NAME = "codex"
GEMINI_ADAPTER_NAME = "gemini"
CLAUDE_ADAPTER_NAME = "claude"
JUNIE_ADAPTER_NAME = "junie"
SKILL_MANIFEST_FILE_NAME = "SKILL.md"
GENERATED_CACHE_FOLDER_NAME = "__pycache__"
PYTHON_BYTECODE_PATTERN = "*.pyc"
MACOS_METADATA_FILE_NAME = ".DS_Store"
INSTALL_MANIFEST_FILE_NAME = ".dev-methodology-install.json"
BUNDLE_ID = "dev-methodology"
MANIFEST_SCHEMA_VERSION_KEY = "schema_version"
MANIFEST_BUNDLE_ID_KEY = "bundle_id"
MANIFEST_ADAPTER_KEY = "adapter"
MANIFEST_SOURCE_KEY = "source"
MANIFEST_UPDATED_AT_KEY = "updated_at"
MANIFEST_ARTIFACTS_KEY = "artifacts"
MANIFEST_ARTIFACT_TYPE_KEY = "type"
MANIFEST_ARTIFACT_NAME_KEY = "name"
MANIFEST_ARTIFACT_PATH_KEY = "path"
MANIFEST_ARTIFACT_DIGEST_KEY = "sha256"
MANIFEST_SKILL_ARTIFACT_TYPE = "skill"
MANIFEST_AGENT_ARTIFACT_TYPE = "agent"
DEFAULT_AGENTS_FOLDER_NAME = "agents"
GENERATED_ADAPTERS_RELATIVE_PATH = Path("generated") / "adapters"
ADAPTERS_RELATIVE_PATH = Path("adapters")
AGENT_FILE_EXTENSIONS = {
    CODEX_ADAPTER_NAME: ".toml",
    GEMINI_ADAPTER_NAME: ".md",
    CLAUDE_ADAPTER_NAME: ".md",
    JUNIE_ADAPTER_NAME: ".md",
}
CLEANUP_SKIPPED_NO_MANIFEST_MESSAGE = "cleanup skipped; no ownership manifest"
SHA256_HEXDIGEST_LENGTH = 64
LOWERCASE_HEXADECIMAL_DIGITS = frozenset("0123456789abcdef")


class Adapter(NamedTuple):
    name: str
    skills_directory: Path
    agents_directory: Optional[Path]


class SkillInstallResult(NamedTuple):
    message: str
    skill_name: str
    owns_destination: bool


class _SkillInstallPlan(NamedTuple):
    resolved_source: Path
    source_roots: tuple[Path, ...]
    source_skills: tuple[Path, ...]
    current_skill_names: set[str]
    previous_manifest: Optional[dict[str, object]]


class _AgentInstallPlan(NamedTuple):
    resolved_source: Path
    source_agents: tuple[Path, ...]
    current_agent_names: set[str]
    previous_manifest: Optional[dict[str, object]]


class _StagedDestination(NamedTuple):
    destination: Path
    transaction_root: Path
    staged: Path
    backup: Path
    existed: bool
    created_parents: tuple[Path, ...]


class _InstallationRollbackError(OSError):
    def __init__(
        self,
        original_error: BaseException,
        rollback_errors: Sequence[BaseException],
        recovery_roots: Sequence[Path],
    ) -> None:
        original_detail = f"{type(original_error).__name__}: {original_error}"
        rollback_detail = "; ".join(
            f"{type(error).__name__}: {error}" for error in rollback_errors
        )
        recovery_detail = ", ".join(str(path) for path in recovery_roots)
        super().__init__(
            f"installation transaction failed ({original_detail}); "
            f"rollback failed ({rollback_detail}); manual recovery required from "
            f"transaction root(s): {recovery_detail}"
        )
        self.recovery_roots = tuple(recovery_roots)


ADAPTERS = {
    GENERIC_ADAPTER_NAME: Adapter(GENERIC_ADAPTER_NAME, Path(".agents/skills"), None),
    CODEX_ADAPTER_NAME: Adapter(CODEX_ADAPTER_NAME, Path(".agents/skills"), Path(".codex/agents")),
    GEMINI_ADAPTER_NAME: Adapter(GEMINI_ADAPTER_NAME, Path(".gemini/skills"), Path(".gemini/agents")),
    CLAUDE_ADAPTER_NAME: Adapter(CLAUDE_ADAPTER_NAME, Path(".claude/skills"), Path(".claude/agents")),
    JUNIE_ADAPTER_NAME: Adapter(JUNIE_ADAPTER_NAME, Path(".junie/skills"), Path(".junie/agents")),
}


def default_source() -> Path:
    return Path(__file__).resolve().parents[1] / DEFAULT_SKILLS_FOLDER_NAME


def parse_boolean(value: str) -> bool:
    normalized = value.lower()
    if normalized == "true":
        return True
    if normalized == "false":
        return False
    raise argparse.ArgumentTypeError("expected true or false")


def parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install the bundled development methodology skills.")
    parser.add_argument(
        "--adapter",
        choices=sorted(ADAPTERS),
        default=DEFAULT_ADAPTER_NAME,
        help="Target agent adapter. Defaults to generic.",
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=default_source(),
        help="Skill bundle source directory. Defaults to this repository's skills folder.",
    )
    parser.add_argument(
        "--adapter-skills-source",
        type=Path,
        default=None,
        help="Optional harness-specific skill source. The repository default is adapters/<adapter>/skills.",
    )
    parser.add_argument(
        "--dest",
        type=Path,
        default=None,
        help="Skills destination. Defaults from --scope when supplied.",
    )
    parser.add_argument(
        "--scope",
        choices=DEPLOYMENT_SCOPES,
        default=None,
        help="Default destinations to the current user or current project.",
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Replace existing destination skill folders with the bundled versions.",
    )
    parser.add_argument(
        "--replace-customized",
        action="store_true",
        help="Replace customized owned artifacts only after discrepancy analysis and user approval.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the install plan without copying files.",
    )
    parser.add_argument(
        "--cleanup",
        type=parse_boolean,
        default=True,
        metavar="true|false",
        help="Remove obsolete bundle-owned skills and agents. Defaults to true.",
    )
    parser.add_argument(
        "--prune-owned",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--install-agents",
        action="store_true",
        help="Install generated native agent definitions for supported adapters.",
    )
    parser.add_argument(
        "--agents-source",
        type=Path,
        default=None,
        help="Generated native agent source. Defaults to generated/adapters/<adapter>/agents.",
    )
    parser.add_argument(
        "--agents-dest",
        type=Path,
        default=None,
        help="Native agent destination. Defaults from --scope when supplied.",
    )
    parser.add_argument(
        "--remove-owned",
        action="store_true",
        help="Remove only artifacts recorded by this bundle's ownership manifest.",
    )
    args = parser.parse_args(argv)
    if args.prune_owned:
        args.cleanup = True
    return args


def default_agents_source(adapter_name: str) -> Path:
    return (
        Path(__file__).resolve().parents[1]
        / GENERATED_ADAPTERS_RELATIVE_PATH
        / adapter_name
        / DEFAULT_AGENTS_FOLDER_NAME
    )


def default_destinations(
    adapter: Adapter,
    scope: str,
    *,
    home: Path | None = None,
    project_root: Path | None = None,
) -> tuple[Path, Optional[Path]]:
    if scope == USER_SCOPE:
        base = Path.home() if home is None else home
    elif scope == PROJECT_SCOPE:
        base = Path.cwd() if project_root is None else project_root
    else:
        raise ValueError(f"Unknown deployment scope: {scope}")
    agents_destination = (
        base / adapter.agents_directory if adapter.agents_directory is not None else None
    )
    return base / adapter.skills_directory, agents_destination


def default_adapter_skills_source(adapter_name: str) -> Path:
    return (
        Path(__file__).resolve().parents[1]
        / ADAPTERS_RELATIVE_PATH
        / adapter_name
        / DEFAULT_SKILLS_FOLDER_NAME
    )


def _paths_overlap(first: Path, second: Path) -> bool:
    return first == second or first in second.parents or second in first.parents


def _resolve_source_root(source: Path, source_kind: str) -> Path:
    expanded_source = source.expanduser()
    if expanded_source.is_symlink():
        raise ValueError(f"{source_kind} source root must not be a symlink: {source}")
    return expanded_source.resolve()


def _resolve_destination_root(destination: Path, destination_kind: str) -> Path:
    expanded_destination = destination.expanduser()
    if expanded_destination.is_symlink():
        raise ValueError(
            f"{destination_kind} destination root must not be a symlink: {destination}"
        )
    if expanded_destination.exists() and not expanded_destination.is_dir():
        raise ValueError(
            f"{destination_kind} destination root must be a directory: {destination}"
        )
    return expanded_destination.resolve()


def _create_missing_parent_directories(parent: Path) -> tuple[Path, ...]:
    missing: list[Path] = []
    candidate = parent
    while not candidate.exists():
        missing.append(candidate)
        candidate = candidate.parent
    parent.mkdir(parents=True, exist_ok=True)
    return tuple(missing)


def _remove_created_parent_directories(parents: Sequence[Path]) -> None:
    for parent in parents:
        try:
            parent.rmdir()
        except OSError:
            pass


def _stage_destination_tree(destination: Path, destination_kind: str) -> _StagedDestination:
    destination_root = _resolve_destination_root(destination, destination_kind)
    created_parents = _create_missing_parent_directories(destination_root.parent)
    transaction_root: Path | None = None
    try:
        transaction_root = Path(
            tempfile.mkdtemp(
                prefix=f"{INSTALL_MANIFEST_FILE_NAME}.{destination_kind}-transaction-",
                dir=destination_root.parent,
            )
        )
        staged = transaction_root / "staged"
        backup = transaction_root / "backup"
        existed = destination_root.exists()
        if existed:
            shutil.copytree(destination_root, staged, symlinks=True)
        else:
            staged.mkdir()
        return _StagedDestination(
            destination=destination_root,
            transaction_root=transaction_root,
            staged=staged,
            backup=backup,
            existed=existed,
            created_parents=created_parents,
        )
    except BaseException:
        if transaction_root is not None:
            shutil.rmtree(transaction_root, ignore_errors=True)
        _remove_created_parent_directories(created_parents)
        raise


def _path_exists(path: Path) -> bool:
    return path.exists() or path.is_symlink()


def _rollback_staged_destination(staged_destination: _StagedDestination) -> None:
    destination_exists = _path_exists(staged_destination.destination)
    staged_exists = _path_exists(staged_destination.staged)
    backup_exists = _path_exists(staged_destination.backup)

    if staged_destination.existed:
        if not backup_exists:
            if not destination_exists:
                raise OSError(
                    f"original destination and backup are both missing: "
                    f"{staged_destination.destination}"
                )
            return
        if destination_exists:
            if staged_exists:
                raise OSError(
                    f"destination rollback state is ambiguous: "
                    f"{staged_destination.transaction_root}"
                )
            os.replace(staged_destination.destination, staged_destination.staged)
        os.replace(staged_destination.backup, staged_destination.destination)
        return

    if destination_exists:
        if staged_exists:
            raise OSError(
                f"new destination rollback state is ambiguous: "
                f"{staged_destination.transaction_root}"
            )
        os.replace(staged_destination.destination, staged_destination.staged)


def _commit_staged_destinations(
    staged_destinations: Sequence[_StagedDestination],
) -> None:
    try:
        for staged_destination in staged_destinations:
            if staged_destination.existed:
                os.replace(
                    staged_destination.destination,
                    staged_destination.backup,
                )
            os.replace(
                staged_destination.staged,
                staged_destination.destination,
            )
    except BaseException as error:
        rollback_errors: list[BaseException] = []
        for staged_destination in reversed(staged_destinations):
            try:
                _rollback_staged_destination(staged_destination)
            except BaseException as rollback_error:
                rollback_errors.append(rollback_error)
        if rollback_errors:
            raise _InstallationRollbackError(
                error,
                rollback_errors,
                [
                    staged_destination.transaction_root
                    for staged_destination in staged_destinations
                ],
            ) from error
        raise


def _discard_destination_stages(
    staged_destinations: Sequence[_StagedDestination],
    *,
    remove_created_parents: bool,
) -> None:
    for staged_destination in reversed(staged_destinations):
        shutil.rmtree(staged_destination.transaction_root, ignore_errors=True)
    if remove_created_parents:
        for staged_destination in reversed(staged_destinations):
            _remove_created_parent_directories(staged_destination.created_parents)


def is_skill_directory(path: Path) -> bool:
    skill_manifest = path / SKILL_MANIFEST_FILE_NAME
    return path.is_dir() and skill_manifest.is_file() and skill_manifest.stat().st_size > 0


def _is_ignored_source_entry(path: Path) -> bool:
    return (
        path.name in {GENERATED_CACHE_FOLDER_NAME, MACOS_METADATA_FILE_NAME}
        or path.match(PYTHON_BYTECODE_PATTERN)
    )


def iter_skill_directories(source: Path) -> list[Path]:
    if not source.is_dir():
        raise FileNotFoundError(f"Skill source directory does not exist: {source}")

    all_source_entries = sorted(source.iterdir())
    source_symlinks = [path.name for path in all_source_entries if path.is_symlink()]
    if source_symlinks:
        raise ValueError("skill source contains symlink entries: " + ", ".join(source_symlinks))
    source_entries = [path for path in all_source_entries if not _is_ignored_source_entry(path)]
    unexpected_entries = [path.name for path in source_entries if not path.is_dir()]
    if unexpected_entries:
        raise ValueError(
            "skill source contains unexpected top-level entries: "
            + ", ".join(unexpected_entries)
        )
    source_directories = [path for path in source_entries if path.is_dir()]
    reserved_names = [
        path.name
        for path in source_directories
        if path.name == INSTALL_MANIFEST_FILE_NAME
    ]
    if reserved_names:
        raise ValueError(
            "skill source contains reserved destination names: "
            + ", ".join(reserved_names)
        )
    nested_symlinks = [
        item.relative_to(source).as_posix()
        for source_directory in source_directories
        for item in source_directory.rglob("*")
        if item.is_symlink()
    ]
    if nested_symlinks:
        raise ValueError("skill source contains symlinks: " + ", ".join(nested_symlinks))
    incomplete_directories = [
        path.name for path in source_directories if not is_skill_directory(path)
    ]
    if incomplete_directories:
        raise ValueError(
            "skill source contains incomplete skill directories: "
            + ", ".join(incomplete_directories)
        )
    if not source_directories:
        raise ValueError(f"skill source contains no skill directories: {source}")
    return source_directories


def remove_existing_destination(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
        return

    shutil.rmtree(path)


def manifest_path(destination: Path) -> Path:
    return destination / INSTALL_MANIFEST_FILE_NAME


def _validate_manifest_component(value: object, field: str, path: Path) -> str:
    if not isinstance(value, str) or not value or "\x00" in value:
        raise ValueError(f"install manifest artifact {field} is invalid: {path}")
    relative_path = Path(value)
    if (
        relative_path.is_absolute()
        or bool(relative_path.drive)
        or len(relative_path.parts) != 1
        or relative_path.name != value
        or value in {".", ".."}
    ):
        raise ValueError(
            f"install manifest artifact {field} must be one relative destination child: {path}"
        )
    return value


def _validate_install_manifest(
    data: dict[str, object],
    path: Path,
    *,
    expected_adapter: str | None,
    expected_artifact_type: str | None,
) -> None:
    schema_version = data.get(MANIFEST_SCHEMA_VERSION_KEY)
    if type(schema_version) is not int or schema_version != MANIFEST_SCHEMA_VERSION:
        raise ValueError(f"install manifest has an unsupported schema version: {path}")
    if data.get(MANIFEST_BUNDLE_ID_KEY) != BUNDLE_ID:
        raise ValueError(f"install manifest belongs to a different bundle: {path}")

    adapter_name = data.get(MANIFEST_ADAPTER_KEY)
    if not isinstance(adapter_name, str) or adapter_name not in ADAPTERS:
        raise ValueError(f"install manifest has an unsupported adapter: {path}")
    if expected_adapter is not None and adapter_name != expected_adapter:
        raise ValueError(
            f"install manifest adapter {adapter_name} does not match {expected_adapter}: {path}"
        )
    if not isinstance(data.get(MANIFEST_SOURCE_KEY), str) or not data[MANIFEST_SOURCE_KEY]:
        raise ValueError(f"install manifest source is missing: {path}")
    if not isinstance(data.get(MANIFEST_UPDATED_AT_KEY), str) or not data[MANIFEST_UPDATED_AT_KEY]:
        raise ValueError(f"install manifest updated_at is missing: {path}")

    artifacts = data.get(MANIFEST_ARTIFACTS_KEY)
    if not isinstance(artifacts, list):
        raise ValueError(f"install manifest artifacts must be a list: {path}")
    seen_names: set[str] = set()
    seen_paths: set[str] = set()
    for index, artifact in enumerate(artifacts):
        if not isinstance(artifact, dict):
            raise ValueError(f"install manifest artifact {index} must be an object: {path}")
        artifact_type = artifact.get(MANIFEST_ARTIFACT_TYPE_KEY)
        if artifact_type not in {MANIFEST_SKILL_ARTIFACT_TYPE, MANIFEST_AGENT_ARTIFACT_TYPE}:
            raise ValueError(f"install manifest artifact {index} has an unsupported type: {path}")
        if expected_artifact_type is not None and artifact_type != expected_artifact_type:
            raise ValueError(
                f"install manifest artifact {index} does not belong in this destination: {path}"
            )

        artifact_name = _validate_manifest_component(
            artifact.get(MANIFEST_ARTIFACT_NAME_KEY),
            "name",
            path,
        )
        artifact_path = _validate_manifest_component(
            artifact.get(MANIFEST_ARTIFACT_PATH_KEY),
            "path",
            path,
        )
        artifact_digest_value = artifact.get(MANIFEST_ARTIFACT_DIGEST_KEY)
        if (
            not isinstance(artifact_digest_value, str)
            or len(artifact_digest_value) != SHA256_HEXDIGEST_LENGTH
            or not set(artifact_digest_value).issubset(LOWERCASE_HEXADECIMAL_DIGITS)
        ):
            raise ValueError(f"install manifest artifact {index} has an invalid sha256: {path}")

        if artifact_type == MANIFEST_SKILL_ARTIFACT_TYPE:
            expected_path = artifact_name
        else:
            extension = AGENT_FILE_EXTENSIONS.get(adapter_name)
            if extension is None:
                raise ValueError(
                    f"install manifest adapter {adapter_name} cannot own native agents: {path}"
                )
            expected_path = f"{artifact_name}{extension}"
        if artifact_path != expected_path:
            raise ValueError(
                f"install manifest artifact path {artifact_path} does not match "
                f"{expected_path}: {path}"
            )
        if artifact_name in seen_names or artifact_path in seen_paths:
            raise ValueError(f"install manifest contains duplicate artifact ownership: {path}")
        seen_names.add(artifact_name)
        seen_paths.add(artifact_path)


def _artifact_destination_path(destination: Path, artifact_path: str) -> Path:
    validated_path = _validate_manifest_component(
        artifact_path,
        "path",
        manifest_path(destination),
    )
    destination_root = _resolve_destination_root(destination, "artifact")
    candidate = destination_root / validated_path
    if candidate.parent.resolve() != destination_root:
        raise ValueError(f"install manifest artifact path escapes destination: {candidate}")
    return candidate


def load_install_manifest(
    destination: Path,
    *,
    expected_adapter: str | None = None,
    expected_artifact_type: str | None = None,
) -> Optional[dict[str, object]]:
    destination_root = _resolve_destination_root(destination, "install manifest")
    path = manifest_path(destination_root)
    if path.is_symlink():
        raise ValueError(f"install manifest must not be a symlink: {path}")
    if not path.exists():
        return None
    if not path.is_file():
        raise ValueError(f"install manifest must be a regular file: {path}")

    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"install manifest is not an object: {path}")
    _validate_install_manifest(
        data,
        path,
        expected_adapter=expected_adapter,
        expected_artifact_type=expected_artifact_type,
    )
    return data


def _write_install_manifest_data(destination: Path, data: dict[str, object]) -> None:
    destination = _resolve_destination_root(destination, "install manifest")
    path = manifest_path(destination)
    if path.is_symlink():
        raise ValueError(f"install manifest must not be a symlink: {path}")
    serialized_manifest = json.dumps(data, indent=2, sort_keys=True) + "\n"
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=destination,
            prefix=f".{INSTALL_MANIFEST_FILE_NAME}.",
            suffix=".tmp",
            delete=False,
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            temporary_file.write(serialized_manifest)
            temporary_file.flush()
            os.fsync(temporary_file.fileno())
        os.replace(temporary_path, path)
        temporary_path = None
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


def manifest_skill_names(manifest: Optional[dict[str, object]]) -> set[str]:
    if manifest is None:
        return set()

    artifacts = manifest.get(MANIFEST_ARTIFACTS_KEY)
    if not isinstance(artifacts, list):
        return set()

    skill_names: set[str] = set()
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            continue
        if artifact.get(MANIFEST_ARTIFACT_TYPE_KEY) != MANIFEST_SKILL_ARTIFACT_TYPE:
            continue
        name = artifact.get(MANIFEST_ARTIFACT_NAME_KEY)
        if isinstance(name, str):
            skill_names.add(name)

    return skill_names


def manifest_skill_paths(manifest: Optional[dict[str, object]]) -> dict[str, str]:
    if manifest is None:
        return {}
    artifacts = manifest.get(MANIFEST_ARTIFACTS_KEY)
    if not isinstance(artifacts, list):
        return {}
    skill_paths: dict[str, str] = {}
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            continue
        if artifact.get(MANIFEST_ARTIFACT_TYPE_KEY) != MANIFEST_SKILL_ARTIFACT_TYPE:
            continue
        name = artifact.get(MANIFEST_ARTIFACT_NAME_KEY)
        path = artifact.get(MANIFEST_ARTIFACT_PATH_KEY)
        if isinstance(name, str) and isinstance(path, str):
            skill_paths[name] = path
    return skill_paths


def artifact_digest(path: Path) -> str:
    digest = hashlib.sha256()
    paths = [path] if path.is_file() else sorted(item for item in path.rglob("*") if item.is_file())
    for item in paths:
        relative_path = item.name if path.is_file() else item.relative_to(path).as_posix()
        if MACOS_METADATA_FILE_NAME in item.parts or GENERATED_CACHE_FOLDER_NAME in item.parts:
            continue
        if item.match(PYTHON_BYTECODE_PATTERN):
            continue
        digest.update(relative_path.encode("utf-8"))
        digest.update(item.read_bytes())
    return digest.hexdigest()


def skill_artifact(skill_name: str, destination: Path) -> dict[str, str]:
    return {
        MANIFEST_ARTIFACT_TYPE_KEY: MANIFEST_SKILL_ARTIFACT_TYPE,
        MANIFEST_ARTIFACT_NAME_KEY: skill_name,
        MANIFEST_ARTIFACT_PATH_KEY: skill_name,
        MANIFEST_ARTIFACT_DIGEST_KEY: artifact_digest(destination / skill_name),
    }


def agent_artifact(agent_name: str, agent_path: str, destination: Path) -> dict[str, str]:
    return {
        MANIFEST_ARTIFACT_TYPE_KEY: MANIFEST_AGENT_ARTIFACT_TYPE,
        MANIFEST_ARTIFACT_NAME_KEY: agent_name,
        MANIFEST_ARTIFACT_PATH_KEY: agent_path,
        MANIFEST_ARTIFACT_DIGEST_KEY: artifact_digest(destination / agent_path),
    }


def manifest_artifact_digests(
    manifest: Optional[dict[str, object]],
    artifact_type: str,
) -> dict[str, str]:
    if manifest is None:
        return {}
    artifacts = manifest.get(MANIFEST_ARTIFACTS_KEY)
    if not isinstance(artifacts, list):
        return {}
    digests: dict[str, str] = {}
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            continue
        if artifact.get(MANIFEST_ARTIFACT_TYPE_KEY) != artifact_type:
            continue
        name = artifact.get(MANIFEST_ARTIFACT_NAME_KEY)
        digest = artifact.get(MANIFEST_ARTIFACT_DIGEST_KEY)
        if isinstance(name, str) and isinstance(digest, str):
            digests[name] = digest
    return digests


def customized_owned_artifacts(
    destination: Path,
    previous_manifest: Optional[dict[str, object]],
    artifact_type: str,
    artifact_paths: dict[str, str],
) -> list[str]:
    previous_digests = manifest_artifact_digests(previous_manifest, artifact_type)
    customized: list[str] = []
    for artifact_name, artifact_path in artifact_paths.items():
        installed_path = _artifact_destination_path(destination, artifact_path)
        previous_digest = previous_digests.get(artifact_name)
        if previous_digest is None or not installed_path.exists():
            continue
        if artifact_digest(installed_path) != previous_digest:
            customized.append(artifact_name)
    return sorted(customized)


def remove_owned_artifacts(
    destination: Path,
    artifact_type: str,
    artifact_paths: dict[str, str],
    dry_run: bool,
) -> list[str]:
    """Remove manifest-owned artifacts while preserving customized and unowned content.

    The destination is an explicit skill or agent folder. Artifact paths must come from
    that destination's validated dev-methodology ownership manifest. Dry runs report the
    removal plan without changing files. Customized owned artifacts raise ValueError so
    callers cannot silently discard local work.
    """
    destination = destination.expanduser()
    previous_manifest = load_install_manifest(
        destination,
        expected_artifact_type=artifact_type,
    )
    if previous_manifest is None:
        return [f"no {artifact_type} ownership manifest at {destination}"]

    customized = customized_owned_artifacts(
        destination,
        previous_manifest,
        artifact_type,
        artifact_paths,
    )
    if customized:
        raise ValueError(
            f"customized owned {artifact_type}s require discrepancy analysis: "
            + ", ".join(customized)
        )

    results: list[str] = []
    for artifact_name, artifact_path in sorted(artifact_paths.items()):
        installed_path = _artifact_destination_path(destination, artifact_path)
        if dry_run:
            results.append(f"would remove owned {artifact_type} {artifact_name}")
            continue
        if installed_path.exists() or installed_path.is_symlink():
            remove_existing_destination(installed_path)
            results.append(f"removed owned {artifact_type} {artifact_name}")
        else:
            results.append(f"owned {artifact_type} already absent {artifact_name}")

    if dry_run:
        results.append(f"would remove {artifact_type} ownership manifest")
    else:
        manifest_path(destination).unlink()
        results.append(f"removed {artifact_type} ownership manifest")
    return results


def _prevalidate_owned_removal(
    destination: Path,
    artifact_type: str,
    adapter: Adapter,
) -> Optional[dict[str, object]]:
    destination = destination.expanduser()
    previous_manifest = load_install_manifest(
        destination,
        expected_adapter=adapter.name,
        expected_artifact_type=artifact_type,
    )
    artifact_paths = (
        manifest_skill_paths(previous_manifest)
        if artifact_type == MANIFEST_SKILL_ARTIFACT_TYPE
        else manifest_agent_paths(previous_manifest)
    )
    customized = customized_owned_artifacts(
        destination,
        previous_manifest,
        artifact_type,
        artifact_paths,
    )
    if customized:
        raise ValueError(
            f"customized owned {artifact_type}s require discrepancy analysis: "
            + ", ".join(customized)
        )
    return previous_manifest


def manifest_agent_paths(manifest: Optional[dict[str, object]]) -> dict[str, str]:
    if manifest is None:
        return {}
    artifacts = manifest.get(MANIFEST_ARTIFACTS_KEY)
    if not isinstance(artifacts, list):
        return {}
    agent_paths: dict[str, str] = {}
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            continue
        if artifact.get(MANIFEST_ARTIFACT_TYPE_KEY) != MANIFEST_AGENT_ARTIFACT_TYPE:
            continue
        name = artifact.get(MANIFEST_ARTIFACT_NAME_KEY)
        path = artifact.get(MANIFEST_ARTIFACT_PATH_KEY)
        if isinstance(name, str) and isinstance(path, str):
            agent_paths[name] = path
    return agent_paths


def build_install_manifest(
    source: Path,
    destination: Path,
    adapter: Adapter,
    owned_skill_names: set[str],
) -> dict[str, object]:
    return {
        MANIFEST_SCHEMA_VERSION_KEY: MANIFEST_SCHEMA_VERSION,
        MANIFEST_BUNDLE_ID_KEY: BUNDLE_ID,
        MANIFEST_ADAPTER_KEY: adapter.name,
        MANIFEST_SOURCE_KEY: str(source.expanduser().resolve()),
        MANIFEST_UPDATED_AT_KEY: datetime.now(timezone.utc).isoformat(),
        MANIFEST_ARTIFACTS_KEY: [
            skill_artifact(skill_name, destination) for skill_name in sorted(owned_skill_names)
        ],
    }


def write_install_manifest(
    destination: Path,
    source: Path,
    adapter: Adapter,
    owned_skill_names: set[str],
) -> None:
    _write_install_manifest_data(
        destination,
        build_install_manifest(source, destination, adapter, owned_skill_names),
    )


def prune_obsolete_owned_skills(
    destination: Path,
    previous_manifest: Optional[dict[str, object]],
    current_skill_names: set[str],
    dry_run: bool,
) -> list[str]:
    if previous_manifest is None:
        return [CLEANUP_SKIPPED_NO_MANIFEST_MESSAGE]

    previous_skill_names = manifest_skill_names(previous_manifest)
    obsolete_skill_names = sorted(previous_skill_names - current_skill_names)
    results: list[str] = []
    for skill_name in obsolete_skill_names:
        destination_skill = _artifact_destination_path(destination, skill_name)
        if dry_run:
            results.append(f"would clean up obsolete {skill_name}")
            continue

        if destination_skill.exists() or destination_skill.is_symlink():
            remove_existing_destination(destination_skill)
            results.append(f"cleaned up obsolete {skill_name}")
        else:
            results.append(f"obsolete already absent {skill_name}")

    return results


def copy_skill(
    source_skill: Path,
    destination_skill: Path,
    replace: bool,
    dry_run: bool,
) -> SkillInstallResult:
    if destination_skill.exists() or destination_skill.is_symlink():
        if not replace:
            return SkillInstallResult(f"skipped {source_skill.name}", source_skill.name, False)
        if dry_run:
            return SkillInstallResult(f"would replace {source_skill.name}", source_skill.name, True)
        remove_existing_destination(destination_skill)
        action = "replaced"
    else:
        action = "installed"

    if dry_run:
        return SkillInstallResult(f"would install {source_skill.name}", source_skill.name, True)

    shutil.copytree(
        source_skill,
        destination_skill,
        ignore=shutil.ignore_patterns(
            GENERATED_CACHE_FOLDER_NAME,
            PYTHON_BYTECODE_PATTERN,
            MACOS_METADATA_FILE_NAME,
        ),
    )
    return SkillInstallResult(f"{action} {source_skill.name}", source_skill.name, True)


def _prepare_skill_install(
    source: Path,
    adapter_skills_source: Optional[Path],
    destination: Path,
    adapter: Adapter,
    replace_customized: bool,
) -> _SkillInstallPlan:
    resolved_source = _resolve_source_root(source, "skill")
    skill_sources = [resolved_source]
    if adapter_skills_source is not None:
        skill_sources.append(_resolve_source_root(adapter_skills_source, "adapter skill"))
    destination_root = _resolve_destination_root(destination, "skill")
    for skill_source in skill_sources:
        if _paths_overlap(skill_source, destination_root):
            raise ValueError(
                f"skill source and destination overlap: {skill_source} and {destination_root}"
            )
    source_skills = tuple(
        source_skill
        for skill_source in skill_sources
        for source_skill in iter_skill_directories(skill_source)
    )
    source_skill_names = [source_skill.name for source_skill in source_skills]
    duplicate_names = sorted(
        name for name in set(source_skill_names) if source_skill_names.count(name) > 1
    )
    if duplicate_names:
        raise ValueError(
            "generic and adapter skill sources contain duplicate names: "
            + ", ".join(duplicate_names)
        )

    destination = destination.expanduser()
    previous_manifest = load_install_manifest(
        destination,
        expected_adapter=adapter.name,
        expected_artifact_type=MANIFEST_SKILL_ARTIFACT_TYPE,
    )
    if not replace_customized:
        customized_skills = customized_owned_artifacts(
            destination,
            previous_manifest,
            MANIFEST_SKILL_ARTIFACT_TYPE,
            manifest_skill_paths(previous_manifest),
        )
        if customized_skills:
            raise ValueError(
                "customized owned skills require discrepancy analysis: "
                + ", ".join(customized_skills)
            )
    return _SkillInstallPlan(
        resolved_source=resolved_source,
        source_roots=tuple(skill_sources),
        source_skills=source_skills,
        current_skill_names=set(source_skill_names),
        previous_manifest=previous_manifest,
    )


def install_skills(
    source: Path,
    adapter_skills_source: Optional[Path],
    destination: Path,
    replace: bool,
    dry_run: bool,
    adapter: Adapter,
    cleanup: bool,
    replace_customized: bool,
    *,
    plan: _SkillInstallPlan | None = None,
) -> list[str]:
    if plan is None:
        plan = _prepare_skill_install(
            source,
            adapter_skills_source,
            destination,
            adapter,
            replace_customized,
        )
    resolved_source = plan.resolved_source
    source_skills = plan.source_skills
    current_skill_names = plan.current_skill_names
    destination = destination.expanduser()
    previous_manifest = plan.previous_manifest

    if not dry_run:
        destination.mkdir(parents=True, exist_ok=True)

    results: list[str] = []
    if cleanup:
        results.extend(
            prune_obsolete_owned_skills(
                destination,
                previous_manifest,
                current_skill_names,
                dry_run,
            )
        )

    newly_owned_skill_names: set[str] = set()
    for source_skill in source_skills:
        destination_skill = destination / source_skill.name
        install_result = copy_skill(
            source_skill,
            destination_skill,
            replace,
            dry_run,
        )
        results.append(install_result.message)
        if install_result.owns_destination:
            newly_owned_skill_names.add(install_result.skill_name)

    if not dry_run:
        previously_owned_skills = manifest_skill_names(previous_manifest)
        if cleanup:
            previously_owned_skills &= current_skill_names
        owned_skill_names = previously_owned_skills | newly_owned_skill_names
        write_install_manifest(destination, resolved_source, adapter, owned_skill_names)
        results.append("wrote ownership manifest")

    return results


def iter_agent_files(source: Path, adapter_name: str) -> list[Path]:
    if not source.is_dir():
        raise FileNotFoundError(f"agent source directory does not exist: {source}")
    extension = AGENT_FILE_EXTENSIONS.get(adapter_name)
    if extension is None:
        raise ValueError(f"adapter does not have generated native agents: {adapter_name}")
    all_source_entries = sorted(source.iterdir())
    source_symlinks = [path.name for path in all_source_entries if path.is_symlink()]
    if source_symlinks:
        raise ValueError("agent source contains symlink entries: " + ", ".join(source_symlinks))
    source_entries = [path for path in all_source_entries if not _is_ignored_source_entry(path)]
    unexpected_entries = [
        path.name
        for path in source_entries
        if not path.is_file() or path.suffix != extension
    ]
    if unexpected_entries:
        raise ValueError(
            "agent source contains unexpected top-level entries: "
            + ", ".join(unexpected_entries)
        )
    source_agents = [path for path in source_entries if path.is_file()]
    if not source_agents:
        raise ValueError(f"agent source contains no {extension} definitions: {source}")
    empty_agents = [path.name for path in source_agents if path.stat().st_size == 0]
    if empty_agents:
        raise ValueError("agent source contains empty definitions: " + ", ".join(empty_agents))
    return source_agents


def write_agent_manifest(
    destination: Path,
    source: Path,
    adapter: Adapter,
    owned_agent_paths: dict[str, str],
) -> None:
    manifest = {
        MANIFEST_SCHEMA_VERSION_KEY: MANIFEST_SCHEMA_VERSION,
        MANIFEST_BUNDLE_ID_KEY: BUNDLE_ID,
        MANIFEST_ADAPTER_KEY: adapter.name,
        MANIFEST_SOURCE_KEY: str(source.expanduser().resolve()),
        MANIFEST_UPDATED_AT_KEY: datetime.now(timezone.utc).isoformat(),
        MANIFEST_ARTIFACTS_KEY: [
            agent_artifact(agent_name, agent_path, destination)
            for agent_name, agent_path in sorted(owned_agent_paths.items())
        ],
    }
    _write_install_manifest_data(destination, manifest)


def prune_obsolete_owned_agents(
    destination: Path,
    previous_manifest: Optional[dict[str, object]],
    current_agent_names: set[str],
    dry_run: bool,
) -> list[str]:
    if previous_manifest is None:
        return [CLEANUP_SKIPPED_NO_MANIFEST_MESSAGE]
    previous_agent_paths = manifest_agent_paths(previous_manifest)
    obsolete_agent_names = sorted(set(previous_agent_paths) - current_agent_names)
    results: list[str] = []
    for agent_name in obsolete_agent_names:
        destination_agent = _artifact_destination_path(
            destination,
            previous_agent_paths[agent_name],
        )
        if dry_run:
            results.append(f"would clean up obsolete agent {agent_name}")
            continue
        if destination_agent.exists() or destination_agent.is_symlink():
            remove_existing_destination(destination_agent)
            results.append(f"cleaned up obsolete agent {agent_name}")
        else:
            results.append(f"obsolete agent already absent {agent_name}")
    return results


def _prepare_agent_install(
    source: Path,
    destination: Path,
    adapter: Adapter,
    replace_customized: bool,
) -> _AgentInstallPlan:
    resolved_source = _resolve_source_root(source, "agent")
    destination_root = _resolve_destination_root(destination, "agent")
    if _paths_overlap(resolved_source, destination_root):
        raise ValueError(
            f"agent source and destination overlap: {resolved_source} and {destination_root}"
        )
    source_agents = tuple(iter_agent_files(resolved_source, adapter.name))
    current_agent_names = {source_agent.stem for source_agent in source_agents}
    destination = destination.expanduser()
    previous_manifest = load_install_manifest(
        destination,
        expected_adapter=adapter.name,
        expected_artifact_type=MANIFEST_AGENT_ARTIFACT_TYPE,
    )
    if not replace_customized:
        customized_agents = customized_owned_artifacts(
            destination,
            previous_manifest,
            MANIFEST_AGENT_ARTIFACT_TYPE,
            manifest_agent_paths(previous_manifest),
        )
        if customized_agents:
            raise ValueError(
                "customized owned agents require discrepancy analysis: "
                + ", ".join(customized_agents)
            )
    return _AgentInstallPlan(
        resolved_source=resolved_source,
        source_agents=source_agents,
        current_agent_names=current_agent_names,
        previous_manifest=previous_manifest,
    )


def _validate_combined_install_paths(
    skill_plan: _SkillInstallPlan,
    skills_destination: Path,
    agent_plan: _AgentInstallPlan,
    agents_destination: Path,
) -> None:
    skills_destination_root = _resolve_destination_root(skills_destination, "skill")
    agents_destination_root = _resolve_destination_root(agents_destination, "agent")
    if _paths_overlap(skills_destination_root, agents_destination_root):
        raise ValueError(
            "skill and agent destinations overlap: "
            f"{skills_destination_root} and {agents_destination_root}"
        )
    for skill_source in skill_plan.source_roots:
        if _paths_overlap(skill_source, agents_destination_root):
            raise ValueError(
                "skill source and agent destination overlap: "
                f"{skill_source} and {agents_destination_root}"
            )
    if _paths_overlap(agent_plan.resolved_source, skills_destination_root):
        raise ValueError(
            "agent source and skill destination overlap: "
            f"{agent_plan.resolved_source} and {skills_destination_root}"
        )


def install_agents(
    source: Path,
    destination: Path,
    replace: bool,
    dry_run: bool,
    adapter: Adapter,
    cleanup: bool,
    replace_customized: bool,
    *,
    plan: _AgentInstallPlan | None = None,
) -> list[str]:
    if plan is None:
        plan = _prepare_agent_install(
            source,
            destination,
            adapter,
            replace_customized,
        )
    resolved_source = plan.resolved_source
    source_agents = plan.source_agents
    current_agent_names = plan.current_agent_names
    destination = destination.expanduser()
    previous_manifest = plan.previous_manifest
    if not dry_run:
        destination.mkdir(parents=True, exist_ok=True)

    results: list[str] = []
    if cleanup:
        results.extend(
            prune_obsolete_owned_agents(
                destination,
                previous_manifest,
                current_agent_names,
                dry_run,
            )
        )

    newly_owned_agent_paths: dict[str, str] = {}
    for source_agent in source_agents:
        destination_agent = destination / source_agent.name
        if destination_agent.exists() or destination_agent.is_symlink():
            if not replace:
                results.append(f"skipped agent {source_agent.stem}")
                continue
            if dry_run:
                results.append(f"would replace agent {source_agent.stem}")
                newly_owned_agent_paths[source_agent.stem] = source_agent.name
                continue
            remove_existing_destination(destination_agent)
            action = "replaced"
        else:
            action = "installed"

        if dry_run:
            results.append(f"would install agent {source_agent.stem}")
            newly_owned_agent_paths[source_agent.stem] = source_agent.name
            continue
        shutil.copy2(source_agent, destination_agent)
        newly_owned_agent_paths[source_agent.stem] = source_agent.name
        results.append(f"{action} agent {source_agent.stem}")

    if not dry_run:
        previously_owned_agents = {
            agent_name: agent_path
            for agent_name, agent_path in manifest_agent_paths(previous_manifest).items()
            if not cleanup or agent_name in current_agent_names
        }
        owned_agent_paths = previously_owned_agents | newly_owned_agent_paths
        write_agent_manifest(destination, resolved_source, adapter, owned_agent_paths)
        results.append("wrote agent ownership manifest")
    return results


def _run_install_transaction(
    *,
    source: Path,
    adapter_skills_source: Optional[Path],
    skills_destination: Path,
    skill_plan: _SkillInstallPlan,
    agents_source: Optional[Path],
    agents_destination: Optional[Path],
    agent_plan: Optional[_AgentInstallPlan],
    replace: bool,
    adapter: Adapter,
    cleanup: bool,
    replace_customized: bool,
) -> list[str]:
    staged_destinations: list[_StagedDestination] = []
    committed = False
    preserve_recovery_evidence = False
    try:
        skills_stage = _stage_destination_tree(skills_destination, "skills")
        staged_destinations.append(skills_stage)
        agents_stage = None
        if agent_plan is not None:
            if agents_source is None or agents_destination is None:
                raise ValueError("agent installation transaction is incomplete")
            agents_stage = _stage_destination_tree(agents_destination, "agents")
            staged_destinations.append(agents_stage)

        results = install_skills(
            source,
            adapter_skills_source,
            skills_stage.staged,
            replace,
            False,
            adapter,
            cleanup,
            replace_customized,
            plan=skill_plan,
        )
        if agent_plan is not None and agents_stage is not None:
            results.extend(
                install_agents(
                    agents_source,
                    agents_stage.staged,
                    replace,
                    False,
                    adapter,
                    cleanup,
                    replace_customized,
                    plan=agent_plan,
                )
            )
        _commit_staged_destinations(staged_destinations)
        committed = True
        return results
    except _InstallationRollbackError:
        preserve_recovery_evidence = True
        raise
    finally:
        if not preserve_recovery_evidence:
            _discard_destination_stages(
                staged_destinations,
                remove_created_parents=not committed,
            )


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    adapter = ADAPTERS[args.adapter]
    destination = args.dest
    agents_destination: Optional[Path] = args.agents_dest
    try:
        if args.scope is not None:
            scoped_destination, scoped_agents_destination = default_destinations(adapter, args.scope)
            if destination is None:
                destination = scoped_destination
            if agents_destination is None:
                agents_destination = scoped_agents_destination
        if destination is None:
            raise ValueError("provide --dest or --scope")
        if args.install_agents and agents_destination is None:
            if adapter.agents_directory is None:
                raise ValueError(f"adapter {adapter.name} does not support generated native agents")
            raise ValueError("--install-agents requires --agents-dest or --scope")
        if args.remove_owned and args.install_agents:
            raise ValueError("--remove-owned cannot be combined with --install-agents")
        if args.remove_owned:
            skill_manifest = _prevalidate_owned_removal(
                destination,
                MANIFEST_SKILL_ARTIFACT_TYPE,
                adapter,
            )
            agent_manifest = None
            if agents_destination is not None:
                agent_manifest = _prevalidate_owned_removal(
                    agents_destination,
                    MANIFEST_AGENT_ARTIFACT_TYPE,
                    adapter,
                )
            results = remove_owned_artifacts(
                destination,
                MANIFEST_SKILL_ARTIFACT_TYPE,
                manifest_skill_paths(skill_manifest),
                args.dry_run,
            )
            if agents_destination is not None:
                results.extend(
                    remove_owned_artifacts(
                        agents_destination,
                        MANIFEST_AGENT_ARTIFACT_TYPE,
                        manifest_agent_paths(agent_manifest),
                        args.dry_run,
                    )
                )
        else:
            adapter_skills_source = args.adapter_skills_source
            if (
                adapter_skills_source is None
                and args.source.expanduser().resolve() == default_source().resolve()
            ):
                default_adapter_source = default_adapter_skills_source(args.adapter)
                if default_adapter_source.is_dir():
                    adapter_skills_source = default_adapter_source
            skill_plan = _prepare_skill_install(
                args.source,
                adapter_skills_source,
                destination,
                adapter,
                args.replace_customized,
            )
            agents_source = None
            agent_plan = None
            if args.install_agents:
                agents_source = (
                    args.agents_source
                    if args.agents_source is not None
                    else default_agents_source(args.adapter)
                )
                agent_plan = _prepare_agent_install(
                    agents_source,
                    agents_destination,
                    adapter,
                    args.replace_customized,
                )
                _validate_combined_install_paths(
                    skill_plan,
                    destination,
                    agent_plan,
                    agents_destination,
                )
            if args.dry_run:
                results = install_skills(
                    args.source,
                    adapter_skills_source,
                    destination,
                    args.replace,
                    True,
                    adapter,
                    args.cleanup,
                    args.replace_customized,
                    plan=skill_plan,
                )
                if args.install_agents:
                    results.extend(
                        install_agents(
                            agents_source,
                            agents_destination,
                            args.replace,
                            True,
                            adapter,
                            args.cleanup,
                            args.replace_customized,
                            plan=agent_plan,
                        )
                    )
            else:
                results = _run_install_transaction(
                    source=args.source,
                    adapter_skills_source=adapter_skills_source,
                    skills_destination=destination,
                    skill_plan=skill_plan,
                    agents_source=agents_source,
                    agents_destination=agents_destination,
                    agent_plan=agent_plan,
                    replace=args.replace,
                    adapter=adapter,
                    cleanup=args.cleanup,
                    replace_customized=args.replace_customized,
                )
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return ERROR_EXIT_CODE

    print(f"adapter {adapter.name}")
    print(f"destination {destination.expanduser()}")
    if agents_destination is not None:
        print(f"agents destination {agents_destination.expanduser()}")
    for result in results:
        print(result)

    return SUCCESS_EXIT_CODE


if __name__ == "__main__":
    raise SystemExit(main())
