# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Defines shell-free command contracts and execution for evaluation fixtures and harnesses.

from __future__ import annotations

import os
import signal
import shlex
import subprocess
import threading
from dataclasses import dataclass, field
from pathlib import Path
from typing import Mapping, Sequence


_SHELL_CONTROL_TOKENS = frozenset({";", "&&", "||", "|", ">", ">>", "<", "2>", "2>>"})
_DEFAULT_HOST_ENVIRONMENT = ("LANG", "LC_ALL", "PATH", "TEMP", "TMP", "TMPDIR")
_DEFAULT_TIMEOUT_SECONDS = 900.0
_DEFAULT_OUTPUT_BYTES = 10 * 1024 * 1024


@dataclass(frozen=True)
class CommandSpec:
    """Represent one process invocation without a shell interpretation layer."""

    argv: tuple[str, ...]
    environment: Mapping[str, str] = field(default_factory=dict)
    timeout_seconds: float | None = _DEFAULT_TIMEOUT_SECONDS
    maximum_output_bytes: int = _DEFAULT_OUTPUT_BYTES
    inherit_environment: bool = False
    host_environment_allowlist: tuple[str, ...] = _DEFAULT_HOST_ENVIRONMENT

    @property
    def uses_shell(self) -> bool:
        """Return false to make the no-shell execution contract inspectable."""

        return False


@dataclass(frozen=True)
class CommandResult:
    """Capture the observable result of one shell-free process invocation."""

    argv: tuple[str, ...]
    exit_code: int
    stdout: str
    stderr: str

    @property
    def passed(self) -> bool:
        """Return whether the process exited successfully."""

        return self.exit_code == 0


def command_spec(value: object) -> CommandSpec:
    """Normalize a legacy command string or structured command into a safe argument vector.

    Legacy strings remain supported for the existing evaluation cases. They are parsed with
    shlex and rejected when they contain shell control tokens. New catalogs should use an argv
    list or a mapping with argv, env, and timeoutSeconds fields.
    """

    if isinstance(value, CommandSpec):
        return value
    if isinstance(value, str):
        argv = tuple(shlex.split(value))
        environment: Mapping[str, str] = {}
        timeout_seconds = _DEFAULT_TIMEOUT_SECONDS
        maximum_output_bytes = _DEFAULT_OUTPUT_BYTES
        inherit_environment = False
        host_environment_allowlist: tuple[str, ...] = _DEFAULT_HOST_ENVIRONMENT
    elif isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray, str)):
        argv = tuple(_require_argument(item) for item in value)
        environment = {}
        timeout_seconds = _DEFAULT_TIMEOUT_SECONDS
        maximum_output_bytes = _DEFAULT_OUTPUT_BYTES
        inherit_environment = False
        host_environment_allowlist = _DEFAULT_HOST_ENVIRONMENT
    elif isinstance(value, Mapping):
        raw_argv = value.get("argv")
        if not isinstance(raw_argv, Sequence) or isinstance(raw_argv, (bytes, bytearray, str)):
            raise ValueError("command mapping must define argv as a list of strings")
        argv = tuple(_require_argument(item) for item in raw_argv)
        raw_environment = value.get("env", {})
        if not isinstance(raw_environment, Mapping):
            raise ValueError("command env must be a mapping")
        environment = {
            _require_environment_name(key): _require_argument(item)
            for key, item in raw_environment.items()
        }
        raw_timeout = value.get("timeoutSeconds")
        if raw_timeout is not None and (not isinstance(raw_timeout, (int, float)) or raw_timeout <= 0):
            raise ValueError("command timeoutSeconds must be a positive number")
        timeout_seconds = float(raw_timeout) if raw_timeout is not None else _DEFAULT_TIMEOUT_SECONDS
        raw_output_bytes = value.get("maximumOutputBytes", _DEFAULT_OUTPUT_BYTES)
        if not isinstance(raw_output_bytes, int) or isinstance(raw_output_bytes, bool) or raw_output_bytes <= 0:
            raise ValueError("command maximumOutputBytes must be a positive integer")
        maximum_output_bytes = raw_output_bytes
        raw_inherit = value.get("inheritEnvironment", False)
        if not isinstance(raw_inherit, bool):
            raise ValueError("command inheritEnvironment must be a boolean")
        inherit_environment = raw_inherit
        raw_allowlist = value.get("hostEnvironmentAllowlist", list(_DEFAULT_HOST_ENVIRONMENT))
        if not isinstance(raw_allowlist, Sequence) or isinstance(raw_allowlist, (bytes, bytearray, str)):
            raise ValueError("command hostEnvironmentAllowlist must be a list of names")
        host_environment_allowlist = tuple(_require_environment_name(item) for item in raw_allowlist)
    else:
        raise ValueError("command must be a string, argv list, or command mapping")

    if not argv:
        raise ValueError("command argv must not be empty")
    if any(argument in _SHELL_CONTROL_TOKENS for argument in argv):
        raise ValueError("command contains a shell control token; use an argv list and separate commands")
    return CommandSpec(
        argv=argv,
        environment=environment,
        timeout_seconds=timeout_seconds,
        maximum_output_bytes=maximum_output_bytes,
        inherit_environment=inherit_environment,
        host_environment_allowlist=host_environment_allowlist,
    )


def run_command(command: CommandSpec, cwd: Path) -> CommandResult:
    """Execute one command directly and return captured output without invoking a shell."""

    environment = os.environ.copy() if command.inherit_environment else {
        name: os.environ[name]
        for name in command.host_environment_allowlist
        if name in os.environ
    }
    environment.update(command.environment)
    process = subprocess.Popen(
        list(command.argv),
        cwd=cwd,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=False,
        start_new_session=True,
    )
    buffers: dict[str, bytearray] = {"stdout": bytearray(), "stderr": bytearray()}
    output_exceeded = threading.Event()

    def drain(name: str, stream: object) -> None:
        while True:
            chunk = stream.read(65536)
            if not chunk:
                return
            remaining = command.maximum_output_bytes - len(buffers[name])
            if remaining > 0:
                buffers[name].extend(chunk[:remaining])
            if len(chunk) > remaining:
                if not output_exceeded.is_set():
                    output_exceeded.set()
                    _kill_process_group(process.pid)

    threads = [
        threading.Thread(target=drain, args=("stdout", process.stdout), daemon=True),
        threading.Thread(target=drain, args=("stderr", process.stderr), daemon=True),
    ]
    for thread in threads:
        thread.start()
    timed_out = False
    try:
        process.wait(timeout=command.timeout_seconds)
    except subprocess.TimeoutExpired:
        timed_out = True
        _kill_process_group(process.pid)
        process.wait()
    for thread in threads:
        thread.join()
    if process.stdout is not None:
        process.stdout.close()
    if process.stderr is not None:
        process.stderr.close()
    stdout = bytes(buffers["stdout"]).decode("utf-8", errors="replace")
    stderr = bytes(buffers["stderr"]).decode("utf-8", errors="replace")
    if timed_out:
        exit_code = 124
        stderr = f"{stderr}\ncommand timed out after {command.timeout_seconds} seconds".lstrip()
    elif output_exceeded.is_set():
        exit_code = 125
        stderr = f"{stderr}\ncommand output exceeded the configured capture cap".lstrip()
    else:
        exit_code = process.returncode
    return CommandResult(
        argv=command.argv,
        exit_code=exit_code,
        stdout=stdout,
        stderr=stderr,
    )


def _require_argument(value: object) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError("command arguments must be non-empty strings")
    if "\x00" in value:
        raise ValueError("command arguments must not contain NUL bytes")
    return value


def _require_environment_name(value: object) -> str:
    name = _require_argument(value)
    if "=" in name:
        raise ValueError("command environment names must not contain equals signs")
    return name


def _kill_process_group(pid: int) -> None:
    try:
        os.killpg(pid, signal.SIGKILL)
    except (PermissionError, ProcessLookupError):
        pass
