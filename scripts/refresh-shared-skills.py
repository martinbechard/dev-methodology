#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import NamedTuple, Optional


SUCCESS_EXIT_CODE = 0
ERROR_EXIT_CODE = 1
REPOSITORY_PARENT_INDEX = 1
INSTALLER_SCRIPT_NAME = "install-skills.py"
CODEX_ADAPTER_NAME = "codex"
CLAUDE_ADAPTER_NAME = "claude"
TARGET_AGENTS_CODEX = "agents-codex"
TARGET_CODEX_HOME = "codex-home"
TARGET_CLAUDE = "claude"
CODEX_HOME_SKILLS_PATH = Path.home() / ".codex" / "skills"


class RefreshTarget(NamedTuple):
    name: str
    adapter: str
    destination: Optional[Path]
    description: str


REFRESH_TARGETS = (
    RefreshTarget(
        name=TARGET_AGENTS_CODEX,
        adapter=CODEX_ADAPTER_NAME,
        destination=None,
        description="AGENTS_HOME or ~/.agents shared skills with Codex metadata",
    ),
    RefreshTarget(
        name=TARGET_CODEX_HOME,
        adapter=CODEX_ADAPTER_NAME,
        destination=CODEX_HOME_SKILLS_PATH,
        description="direct ~/.codex shared skills with Codex metadata",
    ),
    RefreshTarget(
        name=TARGET_CLAUDE,
        adapter=CLAUDE_ADAPTER_NAME,
        destination=None,
        description="CLAUDE_HOME or ~/.claude shared skills",
    ),
)
REFRESH_TARGETS_BY_NAME = {target.name: target for target in REFRESH_TARGETS}
DEFAULT_TARGET_NAMES = tuple(target.name for target in REFRESH_TARGETS)


def repository_root() -> Path:
    return Path(__file__).resolve().parents[REPOSITORY_PARENT_INDEX]


def installer_script() -> Path:
    return repository_root() / "scripts" / INSTALLER_SCRIPT_NAME


def build_install_command(target: RefreshTarget, dry_run: bool) -> list[str]:
    command = [
        sys.executable,
        str(installer_script()),
        "--adapter",
        target.adapter,
        "--replace",
        "--prune-owned",
    ]
    if target.destination is not None:
        command.extend(["--dest", str(target.destination)])
    if dry_run:
        command.append("--dry-run")
    return command


def parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Refresh shared skill installs from this repository.")
    parser.add_argument(
        "--target",
        action="append",
        choices=DEFAULT_TARGET_NAMES,
        help="Shared skill target to refresh. Repeat for multiple targets. Defaults to all targets.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Show installer actions without replacing files.")
    return parser.parse_args(argv)


def selected_targets(target_names: list[str] | None) -> list[RefreshTarget]:
    names = target_names or list(DEFAULT_TARGET_NAMES)
    return [REFRESH_TARGETS_BY_NAME[name] for name in names]


def run_command(command: list[str]) -> int:
    return subprocess.run(command, check=False).returncode


def main(
    argv: Sequence[str] | None = None,
    runner: Callable[[list[str]], int] = run_command,
) -> int:
    args = parse_args(argv)
    for target in selected_targets(args.target):
        print(f"refreshing {target.name}: {target.description}", flush=True)
        exit_code = runner(build_install_command(target, args.dry_run))
        if exit_code != SUCCESS_EXIT_CODE:
            return exit_code or ERROR_EXIT_CODE
    return SUCCESS_EXIT_CODE


if __name__ == "__main__":
    raise SystemExit(main())
