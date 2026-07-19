# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Runs the bounded worker-stall reproduction and emits JSON evidence.

from __future__ import annotations

import asyncio
import json

from worker import reproduce_stall


def main() -> int:
    """Print the observable worker-stall evidence."""

    print(json.dumps(asyncio.run(reproduce_stall()), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
