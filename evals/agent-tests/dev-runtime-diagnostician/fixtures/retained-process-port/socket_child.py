# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Holds a loopback port for the retained-child lifecycle fixture.

from __future__ import annotations

import argparse
import json
import os
import signal
import socket
import time
from pathlib import Path


def main() -> int:
    """Bind the requested port until explicitly terminated."""

    parser = argparse.ArgumentParser()
    parser.add_argument("port", type=int)
    parser.add_argument("state_file", type=Path)
    args = parser.parse_args()
    running = True

    def stop(_signum: int, _frame: object) -> None:
        nonlocal running
        running = False

    signal.signal(signal.SIGTERM, stop)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind(("127.0.0.1", args.port))
        listener.listen()
        args.state_file.write_text(
            json.dumps({"childPid": os.getpid(), "port": args.port}) + "\n"
        )
        while running:
            time.sleep(0.02)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
