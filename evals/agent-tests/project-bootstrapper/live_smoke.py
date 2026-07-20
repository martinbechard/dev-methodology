#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Launches the optional bounded live Project Bootstrapper direct-path smoke test.

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path


_RUNNER = Path(__file__).resolve().parents[1] / "runner.py"


def _runner_python() -> str:
    if sys.version_info >= (3, 11):
        return sys.executable
    compatible = shutil.which("python3.11")
    if compatible is None:
        raise RuntimeError("the live smoke requires Python 3.11 or newer")
    return compatible


def main(argv: Sequence[str] | None = None) -> int:
    """Print or execute the optional live smoke command.

    Callers must pass execute to start the Codex harness. Timeout minutes must be positive and
    bounds the runner-owned live batch. Without execute, this command has no external side effects.
    The return code is the selected runner's return code when executed, otherwise zero.
    """

    parser = argparse.ArgumentParser(description="Run the optional live Bootstrapper smoke test.")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--timeout-minutes", type=int, default=10)
    arguments = parser.parse_args(argv)
    if arguments.timeout_minutes <= 0:
        parser.error("timeout minutes must be positive")
    command = [
        _runner_python(),
        str(_RUNNER),
        "--harness",
        "codex",
        "--scenario",
        "project-bootstrapper:valid-configuration-direct-path",
        "--jobs",
        "1",
        "--timeout-seconds",
        str(arguments.timeout_minutes * 60),
    ]
    print(" ".join(command))
    if not arguments.execute:
        return 0
    return subprocess.run(command, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
