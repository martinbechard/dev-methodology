#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
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
AGENTS_HOME_ENVIRONMENT_VARIABLE = "AGENTS_HOME"
CLAUDE_HOME_ENVIRONMENT_VARIABLE = "CLAUDE_HOME"
AGENTS_HOME_FOLDER_NAME = ".agents"
CLAUDE_HOME_FOLDER_NAME = ".claude"
JUNIE_HOME_FOLDER_NAME = ".junie"
SKILL_MANIFEST_FILE_NAME = "SKILL.md"
ADAPTERS_FOLDER_NAME = "adapters"
GENERATED_CACHE_FOLDER_NAME = "__pycache__"
PYTHON_BYTECODE_PATTERN = "*.pyc"
MACOS_METADATA_FILE_NAME = ".DS_Store"
AGENTS_METADATA_FOLDER_NAME = "agents"
OPENAI_METADATA_FILE_NAME = "openai.yaml"
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
MANIFEST_SKILL_ARTIFACT_TYPE = "skill"
PRUNE_SKIPPED_NO_MANIFEST_MESSAGE = "prune skipped; no ownership manifest"


class Adapter(NamedTuple):
    name: str
    home_environment_variable: Optional[str]
    default_home_folder_name: str
    install_openai_metadata: bool


class SkillInstallResult(NamedTuple):
    message: str
    skill_name: str
    owns_destination: bool


ADAPTERS = {
    GENERIC_ADAPTER_NAME: Adapter(
        name=GENERIC_ADAPTER_NAME,
        home_environment_variable=AGENTS_HOME_ENVIRONMENT_VARIABLE,
        default_home_folder_name=AGENTS_HOME_FOLDER_NAME,
        install_openai_metadata=False,
    ),
    CODEX_ADAPTER_NAME: Adapter(
        name=CODEX_ADAPTER_NAME,
        home_environment_variable=AGENTS_HOME_ENVIRONMENT_VARIABLE,
        default_home_folder_name=AGENTS_HOME_FOLDER_NAME,
        install_openai_metadata=True,
    ),
    GEMINI_ADAPTER_NAME: Adapter(
        name=GEMINI_ADAPTER_NAME,
        home_environment_variable=AGENTS_HOME_ENVIRONMENT_VARIABLE,
        default_home_folder_name=AGENTS_HOME_FOLDER_NAME,
        install_openai_metadata=False,
    ),
    CLAUDE_ADAPTER_NAME: Adapter(
        name=CLAUDE_ADAPTER_NAME,
        home_environment_variable=CLAUDE_HOME_ENVIRONMENT_VARIABLE,
        default_home_folder_name=CLAUDE_HOME_FOLDER_NAME,
        install_openai_metadata=False,
    ),
    JUNIE_ADAPTER_NAME: Adapter(
        name=JUNIE_ADAPTER_NAME,
        home_environment_variable=None,
        default_home_folder_name=JUNIE_HOME_FOLDER_NAME,
        install_openai_metadata=False,
    ),
}


def default_source() -> Path:
    return Path(__file__).resolve().parents[1] / DEFAULT_SKILLS_FOLDER_NAME


def default_adapter_metadata_source(source: Path, adapter_name: str) -> Path:
    return source.expanduser().resolve().parent / ADAPTERS_FOLDER_NAME / adapter_name / DEFAULT_SKILLS_FOLDER_NAME


def default_destination(adapter_name: str = DEFAULT_ADAPTER_NAME) -> Path:
    adapter = ADAPTERS[adapter_name]
    configured_home = (
        os.environ.get(adapter.home_environment_variable)
        if adapter.home_environment_variable is not None
        else None
    )
    if configured_home:
        return Path(configured_home).expanduser() / DEFAULT_SKILLS_FOLDER_NAME

    return Path.home() / adapter.default_home_folder_name / DEFAULT_SKILLS_FOLDER_NAME


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
        "--dest",
        type=Path,
        default=None,
        help="Destination skills directory. Defaults to the selected adapter's skills folder.",
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Replace existing destination skill folders with the bundled versions.",
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
    return parser.parse_args(argv)


def is_skill_directory(path: Path) -> bool:
    return path.is_dir() and (path / SKILL_MANIFEST_FILE_NAME).is_file()


def iter_skill_directories(source: Path) -> list[Path]:
    if not source.is_dir():
        raise FileNotFoundError(f"Skill source directory does not exist: {source}")

    return sorted(path for path in source.iterdir() if is_skill_directory(path))


def remove_openai_metadata(skill: Path) -> None:
    metadata = skill / AGENTS_METADATA_FOLDER_NAME / OPENAI_METADATA_FILE_NAME
    if not metadata.exists():
        return

    metadata.unlink()
    agents_directory = metadata.parent
    if not any(agents_directory.iterdir()):
        agents_directory.rmdir()


def copy_openai_metadata(adapter_metadata_source: Path, skill_name: str, destination_skill: Path) -> None:
    metadata_source = (
        adapter_metadata_source / skill_name / AGENTS_METADATA_FOLDER_NAME / OPENAI_METADATA_FILE_NAME
    )
    if not metadata_source.is_file():
        return

    metadata_destination = destination_skill / AGENTS_METADATA_FOLDER_NAME / OPENAI_METADATA_FILE_NAME
    metadata_destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(metadata_source, metadata_destination)


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


def skill_artifact(skill_name: str) -> dict[str, str]:
    return {
        MANIFEST_ARTIFACT_TYPE_KEY: MANIFEST_SKILL_ARTIFACT_TYPE,
        MANIFEST_ARTIFACT_NAME_KEY: skill_name,
        MANIFEST_ARTIFACT_PATH_KEY: skill_name,
    }


def build_install_manifest(
    source: Path,
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
            skill_artifact(skill_name) for skill_name in sorted(owned_skill_names)
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
            build_install_manifest(source, adapter, owned_skill_names),
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
    adapter: Adapter,
    adapter_metadata_source: Path,
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
    remove_openai_metadata(destination_skill)
    if adapter.install_openai_metadata:
        copy_openai_metadata(adapter_metadata_source, source_skill.name, destination_skill)
    return SkillInstallResult(f"{action} {source_skill.name}", source_skill.name, True)


def install_skills(
    source: Path,
    destination: Path,
    replace: bool,
    dry_run: bool,
    adapter: Adapter,
    prune_owned: bool,
) -> list[str]:
    resolved_source = source.expanduser().resolve()
    source_skills = iter_skill_directories(resolved_source)
    current_skill_names = {source_skill.name for source_skill in source_skills}
    destination = destination.expanduser()
    adapter_metadata_source = default_adapter_metadata_source(source, adapter.name)
    previous_manifest = load_install_manifest(destination)

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
            adapter,
            adapter_metadata_source,
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


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    adapter = ADAPTERS[args.adapter]
    destination = args.dest if args.dest is not None else default_destination(args.adapter)
    try:
        results = install_skills(
            args.source,
            destination,
            args.replace,
            args.dry_run,
            adapter,
            args.prune_owned,
        )
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return ERROR_EXIT_CODE

    print(f"adapter {adapter.name}")
    print(f"destination {destination.expanduser()}")
    for result in results:
        print(result)

    return SUCCESS_EXIT_CODE


if __name__ == "__main__":
    raise SystemExit(main())
