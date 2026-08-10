# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Defines shell-free command contracts and execution for evaluation fixtures and harnesses.

from __future__ import annotations

import os
import signal
import shlex
import subprocess
import sys
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Mapping, Sequence


_SHELL_CONTROL_TOKENS = frozenset({";", "&&", "||", "|", ">", ">>", "<", "2>", "2>>"})
_DEFAULT_HOST_ENVIRONMENT = ("LANG", "LC_ALL", "PATH", "TEMP", "TMP", "TMPDIR")
_DEFAULT_TIMEOUT_SECONDS = 900.0
_DEFAULT_OUTPUT_BYTES = 10 * 1024 * 1024
_CLEANUP_TIMEOUT_SECONDS = 10.0
_WINDOWS_JOB_WRAPPER = "--windows-job-wrapper"
JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x00002000


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
    process_options: dict[str, object] = {}
    effective_timeout = command.timeout_seconds or _DEFAULT_TIMEOUT_SECONDS
    process_argv = list(command.argv)
    if os.name == "nt":
        process_options["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
        process_argv = [
            sys.executable,
            str(Path(__file__).resolve()),
            _WINDOWS_JOB_WRAPPER,
            str(effective_timeout + _CLEANUP_TIMEOUT_SECONDS),
            *process_argv,
        ]
    else:
        process_options["start_new_session"] = True
    process = subprocess.Popen(
        process_argv,
        cwd=cwd,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=False,
        **process_options,
    )
    buffers: dict[str, bytearray] = {"stdout": bytearray(), "stderr": bytearray()}
    output_exceeded = threading.Event()
    cleanup_lock = threading.Lock()
    cleanup_errors: list[BaseException] = []
    cleanup_complete = False

    def terminate_owned_process_tree() -> None:
        nonlocal cleanup_complete
        with cleanup_lock:
            if cleanup_complete:
                return
            try:
                _terminate_owned_process_tree(process)
                cleanup_complete = True
            except BaseException as error:
                if not cleanup_errors:
                    cleanup_errors.append(error)

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
                    terminate_owned_process_tree()

    threads = [
        threading.Thread(target=drain, args=("stdout", process.stdout), daemon=True),
        threading.Thread(target=drain, args=("stderr", process.stderr), daemon=True),
    ]
    for thread in threads:
        thread.start()
    timed_out = False
    try:
        process.wait(timeout=effective_timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        terminate_owned_process_tree()
    finally:
        # The direct command may exit after spawning children. End the runner-created
        # session before joining capture threads so no ordinary eval process survives.
        terminate_owned_process_tree()
    for thread in threads:
        thread.join(timeout=_CLEANUP_TIMEOUT_SECONDS)
    alive_threads = [thread.name for thread in threads if thread.is_alive()]
    if alive_threads:
        raise RuntimeError(
            "Command output capture did not close after owned-tree cleanup: "
            + ", ".join(alive_threads)
        )
    if cleanup_errors:
        raise RuntimeError("Unable to prove owned process-tree cleanup") from cleanup_errors[0]
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


def _terminate_owned_process_tree(process: subprocess.Popen[bytes]) -> None:
    """Stop one runner-owned tree and prove its root descriptor was reaped."""

    if os.name == "nt":
        if process.poll() is None:
            try:
                process.kill()
            except OSError as error:
                if process.poll() is None:
                    raise RuntimeError("Unable to terminate the Windows Job Object owner") from error
        try:
            process.wait(timeout=_CLEANUP_TIMEOUT_SECONDS)
        except subprocess.TimeoutExpired as error:
            raise RuntimeError("Windows Job Object owner did not terminate") from error
        return
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    except PermissionError as error:
        # A very short root can be reaped before cleanup reaches killpg; on macOS the
        # retired numeric group can then report EPERM. It is unsafe only while our root lives.
        if process.poll() is None:
            raise RuntimeError("Unable to terminate the POSIX process group") from error
    try:
        process.wait(timeout=_CLEANUP_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired as error:
        raise RuntimeError("POSIX process-group root did not terminate") from error


def _run_windows_job_owned_command(command: Sequence[str], timeout_seconds: float) -> int:
    """Run one command assigned before resume to a kill-on-close Windows Job Object."""

    if os.name != "nt":
        raise RuntimeError("Windows Job Object wrapper invoked on a non-Windows host")
    if not command:
        raise ValueError("Windows Job Object wrapper requires a command")

    import ctypes
    from ctypes import wintypes

    class _JobObjectBasicLimitInformation(ctypes.Structure):
        _fields_ = (
            ("PerProcessUserTimeLimit", ctypes.c_int64),
            ("PerJobUserTimeLimit", ctypes.c_int64),
            ("LimitFlags", wintypes.DWORD),
            ("MinimumWorkingSetSize", ctypes.c_size_t),
            ("MaximumWorkingSetSize", ctypes.c_size_t),
            ("ActiveProcessLimit", wintypes.DWORD),
            ("Affinity", ctypes.c_size_t),
            ("PriorityClass", wintypes.DWORD),
            ("SchedulingClass", wintypes.DWORD),
        )

    class _IoCounters(ctypes.Structure):
        _fields_ = tuple((name, ctypes.c_uint64) for name in (
            "ReadOperationCount",
            "WriteOperationCount",
            "OtherOperationCount",
            "ReadTransferCount",
            "WriteTransferCount",
            "OtherTransferCount",
        ))

    class _JobObjectExtendedLimitInformation(ctypes.Structure):
        _fields_ = (
            ("BasicLimitInformation", _JobObjectBasicLimitInformation),
            ("IoInfo", _IoCounters),
            ("ProcessMemoryLimit", ctypes.c_size_t),
            ("JobMemoryLimit", ctypes.c_size_t),
            ("PeakProcessMemoryUsed", ctypes.c_size_t),
            ("PeakJobMemoryUsed", ctypes.c_size_t),
        )

    class _JobObjectBasicAccountingInformation(ctypes.Structure):
        _fields_ = (
            ("TotalUserTime", ctypes.c_int64),
            ("TotalKernelTime", ctypes.c_int64),
            ("ThisPeriodTotalUserTime", ctypes.c_int64),
            ("ThisPeriodTotalKernelTime", ctypes.c_int64),
            ("TotalPageFaultCount", wintypes.DWORD),
            ("TotalProcesses", wintypes.DWORD),
            ("ActiveProcesses", wintypes.DWORD),
            ("TotalTerminatedProcesses", wintypes.DWORD),
        )

    class _StartupInfo(ctypes.Structure):
        _fields_ = (
            ("cb", wintypes.DWORD),
            ("lpReserved", wintypes.LPWSTR),
            ("lpDesktop", wintypes.LPWSTR),
            ("lpTitle", wintypes.LPWSTR),
            ("dwX", wintypes.DWORD),
            ("dwY", wintypes.DWORD),
            ("dwXSize", wintypes.DWORD),
            ("dwYSize", wintypes.DWORD),
            ("dwXCountChars", wintypes.DWORD),
            ("dwYCountChars", wintypes.DWORD),
            ("dwFillAttribute", wintypes.DWORD),
            ("dwFlags", wintypes.DWORD),
            ("wShowWindow", wintypes.WORD),
            ("cbReserved2", wintypes.WORD),
            ("lpReserved2", ctypes.POINTER(wintypes.BYTE)),
            ("hStdInput", wintypes.HANDLE),
            ("hStdOutput", wintypes.HANDLE),
            ("hStdError", wintypes.HANDLE),
        )

    class _ProcessInformation(ctypes.Structure):
        _fields_ = (
            ("hProcess", wintypes.HANDLE),
            ("hThread", wintypes.HANDLE),
            ("dwProcessId", wintypes.DWORD),
            ("dwThreadId", wintypes.DWORD),
        )

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.CreateJobObjectW.argtypes = (ctypes.c_void_p, wintypes.LPCWSTR)
    kernel32.CreateJobObjectW.restype = wintypes.HANDLE
    kernel32.SetInformationJobObject.argtypes = (
        wintypes.HANDLE,
        ctypes.c_int,
        ctypes.c_void_p,
        wintypes.DWORD,
    )
    kernel32.SetInformationJobObject.restype = wintypes.BOOL
    kernel32.QueryInformationJobObject.argtypes = (
        wintypes.HANDLE,
        ctypes.c_int,
        ctypes.c_void_p,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
    )
    kernel32.QueryInformationJobObject.restype = wintypes.BOOL
    kernel32.GetStdHandle.argtypes = (wintypes.DWORD,)
    kernel32.GetStdHandle.restype = wintypes.HANDLE
    kernel32.CreateProcessW.argtypes = (
        wintypes.LPCWSTR,
        wintypes.LPWSTR,
        ctypes.c_void_p,
        ctypes.c_void_p,
        wintypes.BOOL,
        wintypes.DWORD,
        ctypes.c_void_p,
        wintypes.LPCWSTR,
        ctypes.POINTER(_StartupInfo),
        ctypes.POINTER(_ProcessInformation),
    )
    kernel32.CreateProcessW.restype = wintypes.BOOL
    kernel32.AssignProcessToJobObject.argtypes = (wintypes.HANDLE, wintypes.HANDLE)
    kernel32.AssignProcessToJobObject.restype = wintypes.BOOL
    kernel32.ResumeThread.argtypes = (wintypes.HANDLE,)
    kernel32.ResumeThread.restype = wintypes.DWORD
    kernel32.WaitForSingleObject.argtypes = (wintypes.HANDLE, wintypes.DWORD)
    kernel32.WaitForSingleObject.restype = wintypes.DWORD
    kernel32.GetExitCodeProcess.argtypes = (wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD))
    kernel32.GetExitCodeProcess.restype = wintypes.BOOL
    kernel32.TerminateProcess.argtypes = (wintypes.HANDLE, wintypes.UINT)
    kernel32.TerminateProcess.restype = wintypes.BOOL
    kernel32.TerminateJobObject.argtypes = (wintypes.HANDLE, wintypes.UINT)
    kernel32.TerminateJobObject.restype = wintypes.BOOL
    kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
    kernel32.CloseHandle.restype = wintypes.BOOL

    wait_object_0 = 0
    wait_timeout = 258
    create_suspended = 0x00000004
    create_new_process_group = 0x00000200
    STARTF_USESTDHANDLES = 0x00000100
    std_input_handle = 0xFFFFFFF6
    std_output_handle = 0xFFFFFFF5
    std_error_handle = 0xFFFFFFF4
    invalid_handle_value = ctypes.c_void_p(-1).value
    job_object_basic_accounting_information = 1
    job_object_extended_limit_information = 9
    cleanup_timeout_ms = int(_CLEANUP_TIMEOUT_SECONDS * 1000)
    maximum_wait_ms = 0xFFFFFFFE
    command_timeout_ms = min(maximum_wait_ms, max(1, int(timeout_seconds * 1000)))

    def wait_for_empty_job() -> None:
        deadline = time.monotonic() + _CLEANUP_TIMEOUT_SECONDS
        while True:
            accounting = _JobObjectBasicAccountingInformation()
            returned_length = wintypes.DWORD()
            if not kernel32.QueryInformationJobObject(
                job,
                job_object_basic_accounting_information,
                ctypes.byref(accounting),
                ctypes.sizeof(accounting),
                ctypes.byref(returned_length),
            ):
                raise ctypes.WinError(ctypes.get_last_error())
            if accounting.ActiveProcesses == 0:
                return
            if time.monotonic() >= deadline:
                raise RuntimeError("Windows command job did not become empty")
            time.sleep(0.01)

    job = kernel32.CreateJobObjectW(None, None)
    if not job:
        raise ctypes.WinError(ctypes.get_last_error())
    process_information = _ProcessInformation()
    try:
        limits = _JobObjectExtendedLimitInformation()
        limits.BasicLimitInformation.LimitFlags = JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        if not kernel32.SetInformationJobObject(
            job,
            job_object_extended_limit_information,
            ctypes.byref(limits),
            ctypes.sizeof(limits),
        ):
            raise ctypes.WinError(ctypes.get_last_error())

        startup = _StartupInfo()
        startup.cb = ctypes.sizeof(startup)
        startup.dwFlags = STARTF_USESTDHANDLES
        startup.hStdInput = kernel32.GetStdHandle(std_input_handle)
        startup.hStdOutput = kernel32.GetStdHandle(std_output_handle)
        startup.hStdError = kernel32.GetStdHandle(std_error_handle)
        if any(
            handle in (None, invalid_handle_value)
            for handle in (startup.hStdInput, startup.hStdOutput, startup.hStdError)
        ):
            raise ctypes.WinError(ctypes.get_last_error())
        command_line = ctypes.create_unicode_buffer(subprocess.list2cmdline(list(command)))
        if not kernel32.CreateProcessW(
            None,
            command_line,
            None,
            None,
            True,
            create_suspended | create_new_process_group,
            None,
            None,
            ctypes.byref(startup),
            ctypes.byref(process_information),
        ):
            raise ctypes.WinError(ctypes.get_last_error())
        try:
            if not kernel32.AssignProcessToJobObject(job, process_information.hProcess):
                error_code = ctypes.get_last_error()
                if not kernel32.TerminateProcess(process_information.hProcess, 126):
                    raise ctypes.WinError(ctypes.get_last_error())
                if kernel32.WaitForSingleObject(
                    process_information.hProcess,
                    cleanup_timeout_ms,
                ) != wait_object_0:
                    raise RuntimeError("Unassigned suspended Windows command did not terminate")
                raise ctypes.WinError(error_code)
            if kernel32.ResumeThread(process_information.hThread) == 0xFFFFFFFF:
                error_code = ctypes.get_last_error()
                if not kernel32.TerminateJobObject(job, 126):
                    raise ctypes.WinError(ctypes.get_last_error())
                wait_for_empty_job()
                raise ctypes.WinError(error_code)

            wait_result = kernel32.WaitForSingleObject(
                process_information.hProcess,
                command_timeout_ms,
            )
            if wait_result == wait_timeout:
                if not kernel32.TerminateJobObject(job, 124):
                    raise ctypes.WinError(ctypes.get_last_error())
                wait_for_empty_job()
                return 124
            if wait_result != wait_object_0:
                raise ctypes.WinError(ctypes.get_last_error())

            exit_code = wintypes.DWORD()
            if not kernel32.GetExitCodeProcess(
                process_information.hProcess,
                ctypes.byref(exit_code),
            ):
                raise ctypes.WinError(ctypes.get_last_error())
            if not kernel32.TerminateJobObject(job, 1):
                raise ctypes.WinError(ctypes.get_last_error())
            wait_for_empty_job()
            return int(exit_code.value)
        finally:
            close_error = 0
            if process_information.hThread:
                if not kernel32.CloseHandle(process_information.hThread):
                    close_error = ctypes.get_last_error()
            if process_information.hProcess:
                if not kernel32.CloseHandle(process_information.hProcess) and not close_error:
                    close_error = ctypes.get_last_error()
            if close_error:
                raise ctypes.WinError(close_error)
    finally:
        if not kernel32.CloseHandle(job):
            raise ctypes.WinError(ctypes.get_last_error())


def _windows_job_wrapper_main(arguments: Sequence[str]) -> int:
    """Validate private wrapper arguments and surface ownership failures to the parent."""

    if len(arguments) < 2:
        print("Windows Job Object wrapper requires a timeout and command", file=sys.stderr)
        return 126
    try:
        timeout_seconds = float(arguments[0])
        if timeout_seconds <= 0:
            raise ValueError("timeout must be positive")
        return _run_windows_job_owned_command(arguments[1:], timeout_seconds)
    except Exception as error:
        print(f"Windows Job Object ownership failed: {error}", file=sys.stderr)
        return 126


if __name__ == "__main__":
    if sys.argv[1:2] != [_WINDOWS_JOB_WRAPPER]:
        raise SystemExit("This module is not a standalone command")
    raise SystemExit(_windows_job_wrapper_main(sys.argv[2:]))
