# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Reproduces and verifies the retained-child port lifecycle without leaking resources.

from __future__ import annotations

import argparse
import json
import os
import signal
import shutil
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path


FIXTURE_ROOT = Path(__file__).resolve().parent


def available_port() -> int:
    """Reserve and release a loopback port for one bounded probe."""

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        listener.bind(("127.0.0.1", 0))
        return int(listener.getsockname()[1])


def can_bind(port: int) -> bool:
    """Return whether the loopback port is currently available."""

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            listener.bind(("127.0.0.1", port))
        except OSError:
            return False
    return True


def wait_for_state(state_file: Path) -> dict[str, int]:
    """Wait for the socket child to publish its process and port state."""

    deadline = time.monotonic() + 3
    while time.monotonic() < deadline:
        if state_file.exists():
            return json.loads(state_file.read_text())
        time.sleep(0.02)
    raise TimeoutError("socket child did not publish state")


def wait_until_bindable(port: int) -> None:
    """Wait for an explicitly terminated fixture child to release its port."""

    deadline = time.monotonic() + 3
    while time.monotonic() < deadline:
        if can_bind(port):
            return
        time.sleep(0.02)
    raise TimeoutError("fixture child did not release port")


def start_service(port: int, state_file: Path, clean: bool) -> subprocess.Popen[bytes]:
    """Start one fixture service instance."""

    command = [sys.executable, "service.py", str(port), str(state_file)]
    if clean:
        command.append("--clean-shutdown")
    return subprocess.Popen(
        command,
        cwd=FIXTURE_ROOT,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def inspect_retaining_process(port: int, child_pid: int) -> dict[str, object]:
    """Correlate the retained listener with its exact process identity."""

    lsof = shutil.which("lsof")
    if lsof is None:
        raise RuntimeError("lsof is required for retained-process inspection")
    listener = subprocess.run(
        [lsof, "-nP", "-a", "-p", str(child_pid), f"-iTCP:{port}", "-sTCP:LISTEN", "-FpcnT"],
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()
    process = next((line for line in listener.splitlines() if line == f"p{child_pid}"), "")
    verified = bool(process) and "TST=LISTEN" in listener
    return {
        "inspectedPid": child_pid,
        "listenerEvidence": listener,
        "processEvidence": process,
        "processInspectionVerified": verified,
    }


def reproduce() -> dict[str, object]:
    """Prove that the leaky parent shutdown leaves its child holding the port."""

    with tempfile.TemporaryDirectory() as temporary_directory:
        port = available_port()
        state_file = Path(temporary_directory) / "service-state.json"
        parent = start_service(port, state_file, clean=False)
        state = wait_for_state(state_file)
        child_pid = state["childPid"]
        try:
            parent.terminate()
            parent.wait(timeout=3)
            retained = not can_bind(port)
            inspection = inspect_retaining_process(port, child_pid)
        finally:
            if parent.poll() is None:
                parent.kill()
                parent.wait(timeout=3)
            try:
                os.kill(child_pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            wait_until_bindable(port)
        return {
            "parentExited": parent.returncode is not None,
            "childPid": child_pid,
            "port": port,
            "portRetainedAfterParentExit": retained,
            "cleanupVerified": can_bind(port),
            **inspection,
        }


def verify_clean() -> dict[str, object]:
    """Verify three clean start-stop cycles on one selected port."""

    port = available_port()
    child_pids: list[int] = []
    with tempfile.TemporaryDirectory() as temporary_directory:
        for cycle in range(3):
            state_file = Path(temporary_directory) / f"state-{cycle}.json"
            parent = start_service(port, state_file, clean=True)
            state = wait_for_state(state_file)
            child_pids.append(state["childPid"])
            parent.terminate()
            parent.wait(timeout=3)
            wait_until_bindable(port)
    return {
        "cycles": 3,
        "childPids": child_pids,
        "cleanRestartsVerified": can_bind(port),
    }


def main() -> int:
    """Run the requested lifecycle probe and print governed JSON evidence."""

    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("reproduce", "verify-clean"))
    args = parser.parse_args()
    evidence = reproduce() if args.mode == "reproduce" else verify_clean()
    print(json.dumps(evidence, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
