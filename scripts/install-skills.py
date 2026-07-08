#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import NamedTuple, Optional


SUCCESS_EXIT_CODE = 0
ERROR_EXIT_CODE = 1
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


class Adapter(NamedTuple):
    name: str
    home_environment_variable: Optional[str]
    default_home_folder_name: str
    install_openai_metadata: bool


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


def copy_skill(
    source_skill: Path,
    destination_skill: Path,
    replace: bool,
    dry_run: bool,
    adapter: Adapter,
    adapter_metadata_source: Path,
) -> str:
    if destination_skill.exists():
        if not replace:
            return f"skipped {source_skill.name}"
        if dry_run:
            return f"would replace {source_skill.name}"
        remove_existing_destination(destination_skill)
        action = "replaced"
    else:
        action = "installed"

    if dry_run:
        return f"would install {source_skill.name}"

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
    return f"{action} {source_skill.name}"


def install_skills(
    source: Path,
    destination: Path,
    replace: bool,
    dry_run: bool,
    adapter: Adapter,
) -> list[str]:
    source_skills = iter_skill_directories(source.expanduser().resolve())
    destination = destination.expanduser()
    adapter_metadata_source = default_adapter_metadata_source(source, adapter.name)

    if not dry_run:
        destination.mkdir(parents=True, exist_ok=True)

    results: list[str] = []
    for source_skill in source_skills:
        destination_skill = destination / source_skill.name
        results.append(
            copy_skill(
                source_skill,
                destination_skill,
                replace,
                dry_run,
                adapter,
                adapter_metadata_source,
            )
        )

    return results


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    adapter = ADAPTERS[args.adapter]
    destination = args.dest if args.dest is not None else default_destination(args.adapter)
    try:
        results = install_skills(args.source, destination, args.replace, args.dry_run, adapter)
    except OSError as error:
        print(error, file=sys.stderr)
        return ERROR_EXIT_CODE

    print(f"adapter {adapter.name}")
    print(f"destination {destination.expanduser()}")
    for result in results:
        print(result)

    return SUCCESS_EXIT_CODE


if __name__ == "__main__":
    raise SystemExit(main())
