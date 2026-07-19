# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Models a parent service with leaky and clean child-process shutdown paths.

from __future__ import annotations

import argparse
import signal
import subprocess
import sys
import time
from pathlib import Path


def main() -> int:
    """Launch a socket child and stop it only when clean shutdown is selected."""

    parser = argparse.ArgumentParser()
    parser.add_argument("port", type=int)
    parser.add_argument("state_file", type=Path)
    parser.add_argument("--clean-shutdown", action="store_true")
    args = parser.parse_args()
    running = True

    def stop(_signum: int, _frame: object) -> None:
        nonlocal running
        running = False

    signal.signal(signal.SIGTERM, stop)
    child = subprocess.Popen(
        [sys.executable, "socket_child.py", str(args.port), str(args.state_file)],
        cwd=Path(__file__).resolve().parent,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    try:
        while running:
            time.sleep(0.02)
    finally:
        if args.clean_shutdown and child.poll() is None:
            child.terminate()
            child.wait(timeout=3)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
