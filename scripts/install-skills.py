#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Modified with AI assistance.
# Summary: Installs or removes bundle-owned skills and agents only at explicit deployment destinations.

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from collections.abc import Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import NamedTuple, Optional


SUCCESS_EXIT_CODE = 0
ERROR_EXIT_CODE = 1
MANIFEST_SCHEMA_VERSION = 1
DEFAULT_SKILLS_FOLDER_NAME = "skills"
DEFAULT_ADAPTER_NAME = "generic"
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
PRUNE_SKIPPED_NO_MANIFEST_MESSAGE = "prune skipped; no ownership manifest"


class Adapter(NamedTuple):
    name: str


class SkillInstallResult(NamedTuple):
    message: str
    skill_name: str
    owns_destination: bool


ADAPTERS = {
    adapter_name: Adapter(name=adapter_name)
    for adapter_name in (
        GENERIC_ADAPTER_NAME,
        CODEX_ADAPTER_NAME,
        GEMINI_ADAPTER_NAME,
        CLAUDE_ADAPTER_NAME,
        JUNIE_ADAPTER_NAME,
    )
}


def default_source() -> Path:
    return Path(__file__).resolve().parents[1] / DEFAULT_SKILLS_FOLDER_NAME


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
        required=True,
        help="Explicit deployment or cleanup destination for skills.",
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
        "--prune-owned",
        action="store_true",
        help="Remove obsolete skills previously installed by this bundle.",
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
        help="Explicit deployment or cleanup destination for native agents.",
    )
    parser.add_argument(
        "--remove-owned",
        action="store_true",
        help="Remove only artifacts recorded by this bundle's ownership manifest.",
    )
    return parser.parse_args(argv)


def default_agents_source(adapter_name: str) -> Path:
    return (
        Path(__file__).resolve().parents[1]
        / GENERATED_ADAPTERS_RELATIVE_PATH
        / adapter_name
        / DEFAULT_AGENTS_FOLDER_NAME
    )


def default_adapter_skills_source(adapter_name: str) -> Path:
    return (
        Path(__file__).resolve().parents[1]
        / ADAPTERS_RELATIVE_PATH
        / adapter_name
        / DEFAULT_SKILLS_FOLDER_NAME
    )


def is_skill_directory(path: Path) -> bool:
    return path.is_dir() and (path / SKILL_MANIFEST_FILE_NAME).is_file()


def iter_skill_directories(source: Path) -> list[Path]:
    if not source.is_dir():
        raise FileNotFoundError(f"Skill source directory does not exist: {source}")

    return sorted(path for path in source.iterdir() if is_skill_directory(path))


def remove_existing_destination(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
        return

    shutil.rmtree(path)


def manifest_path(destination: Path) -> Path:
    return destination / INSTALL_MANIFEST_FILE_NAME


def load_install_manifest(destination: Path) -> Optional[dict[str, object]]:
    path = manifest_path(destination)
    if not path.is_file():
        return None

    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Install manifest is not an object: {path}")
    if data.get(MANIFEST_BUNDLE_ID_KEY) != BUNDLE_ID:
        raise ValueError(f"Install manifest belongs to a different bundle: {path}")
    return data


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
        installed_path = destination / artifact_path
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
    previous_manifest = load_install_manifest(destination)
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
        installed_path = destination / artifact_path
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
    manifest_path(destination).write_text(
        json.dumps(
            build_install_manifest(source, destination, adapter, owned_skill_names),
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def prune_obsolete_owned_skills(
    destination: Path,
    previous_manifest: Optional[dict[str, object]],
    current_skill_names: set[str],
    dry_run: bool,
) -> list[str]:
    if previous_manifest is None:
        return [PRUNE_SKIPPED_NO_MANIFEST_MESSAGE]

    previous_skill_names = manifest_skill_names(previous_manifest)
    obsolete_skill_names = sorted(previous_skill_names - current_skill_names)
    results: list[str] = []
    for skill_name in obsolete_skill_names:
        destination_skill = destination / skill_name
        if dry_run:
            results.append(f"would prune obsolete {skill_name}")
            continue

        if destination_skill.exists() or destination_skill.is_symlink():
            remove_existing_destination(destination_skill)
            results.append(f"pruned obsolete {skill_name}")
        else:
            results.append(f"obsolete already absent {skill_name}")

    return results


def copy_skill(
    source_skill: Path,
    destination_skill: Path,
    replace: bool,
    dry_run: bool,
) -> SkillInstallResult:
    if destination_skill.exists():
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


def install_skills(
    source: Path,
    adapter_skills_source: Optional[Path],
    destination: Path,
    replace: bool,
    dry_run: bool,
    adapter: Adapter,
    prune_owned: bool,
    replace_customized: bool,
) -> list[str]:
    resolved_source = source.expanduser().resolve()
    skill_sources = [resolved_source]
    if adapter_skills_source is not None:
        skill_sources.append(adapter_skills_source.expanduser().resolve())
    source_skills = [
        source_skill
        for skill_source in skill_sources
        for source_skill in iter_skill_directories(skill_source)
    ]
    source_skill_names = [source_skill.name for source_skill in source_skills]
    duplicate_names = sorted(
        name for name in set(source_skill_names) if source_skill_names.count(name) > 1
    )
    if duplicate_names:
        raise ValueError(
            "generic and adapter skill sources contain duplicate names: "
            + ", ".join(duplicate_names)
        )
    current_skill_names = {source_skill.name for source_skill in source_skills}
    destination = destination.expanduser()
    previous_manifest = load_install_manifest(destination)
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

    if not dry_run:
        destination.mkdir(parents=True, exist_ok=True)

    results: list[str] = []
    if prune_owned:
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
        previously_owned_current_skills = (
            manifest_skill_names(previous_manifest) & current_skill_names
        )
        owned_skill_names = previously_owned_current_skills | newly_owned_skill_names
        write_install_manifest(destination, resolved_source, adapter, owned_skill_names)
        results.append("wrote ownership manifest")

    return results


def iter_agent_files(source: Path, adapter_name: str) -> list[Path]:
    if not source.is_dir():
        raise FileNotFoundError(f"Agent source directory does not exist: {source}")
    extension = AGENT_FILE_EXTENSIONS.get(adapter_name)
    if extension is None:
        raise ValueError(f"Adapter does not have generated native agents: {adapter_name}")
    return sorted(path for path in source.iterdir() if path.is_file() and path.suffix == extension)


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
    manifest_path(destination).write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def prune_obsolete_owned_agents(
    destination: Path,
    previous_manifest: Optional[dict[str, object]],
    current_agent_names: set[str],
    dry_run: bool,
) -> list[str]:
    if previous_manifest is None:
        return [PRUNE_SKIPPED_NO_MANIFEST_MESSAGE]
    previous_agent_paths = manifest_agent_paths(previous_manifest)
    obsolete_agent_names = sorted(set(previous_agent_paths) - current_agent_names)
    results: list[str] = []
    for agent_name in obsolete_agent_names:
        destination_agent = destination / previous_agent_paths[agent_name]
        if dry_run:
            results.append(f"would prune obsolete agent {agent_name}")
            continue
        if destination_agent.exists() or destination_agent.is_symlink():
            remove_existing_destination(destination_agent)
            results.append(f"pruned obsolete agent {agent_name}")
        else:
            results.append(f"obsolete agent already absent {agent_name}")
    return results


def install_agents(
    source: Path,
    destination: Path,
    replace: bool,
    dry_run: bool,
    adapter: Adapter,
    prune_owned: bool,
    replace_customized: bool,
) -> list[str]:
    resolved_source = source.expanduser().resolve()
    source_agents = iter_agent_files(resolved_source, adapter.name)
    current_agent_names = {source_agent.stem for source_agent in source_agents}
    destination = destination.expanduser()
    previous_manifest = load_install_manifest(destination)
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
    if not dry_run:
        destination.mkdir(parents=True, exist_ok=True)

    results: list[str] = []
    if prune_owned:
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
        previously_owned_current_agents = {
            agent_name: agent_path
            for agent_name, agent_path in manifest_agent_paths(previous_manifest).items()
            if agent_name in current_agent_names
        }
        owned_agent_paths = previously_owned_current_agents | newly_owned_agent_paths
        write_agent_manifest(destination, resolved_source, adapter, owned_agent_paths)
        results.append("wrote agent ownership manifest")
    return results


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    adapter = ADAPTERS[args.adapter]
    destination = args.dest
    agents_destination: Optional[Path] = args.agents_dest
    try:
        if args.install_agents and agents_destination is None:
            raise ValueError("--install-agents requires an explicit --agents-dest")
        if args.remove_owned and args.install_agents:
            raise ValueError("--remove-owned cannot be combined with --install-agents")
        if args.remove_owned:
            skill_manifest = load_install_manifest(destination.expanduser())
            results = remove_owned_artifacts(
                destination,
                MANIFEST_SKILL_ARTIFACT_TYPE,
                manifest_skill_paths(skill_manifest),
                args.dry_run,
            )
            if agents_destination is not None:
                agent_manifest = load_install_manifest(agents_destination.expanduser())
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
            results = install_skills(
                args.source,
                adapter_skills_source,
                destination,
                args.replace,
                args.dry_run,
                adapter,
                args.prune_owned,
                args.replace_customized,
            )
        if args.install_agents:
            agents_source = (
                args.agents_source
                if args.agents_source is not None
                else default_agents_source(args.adapter)
            )
            results.extend(
                install_agents(
                    agents_source,
                    agents_destination,
                    args.replace,
                    args.dry_run,
                    adapter,
                    args.prune_owned,
                    args.replace_customized,
                )
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
