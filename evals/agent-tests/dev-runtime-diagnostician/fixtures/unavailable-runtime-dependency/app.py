# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Provides a synthetic application boundary whose configured storage dependency is intentionally absent.

from __future__ import annotations

import json
import os
import sys
from urllib.error import URLError
from urllib.request import urlopen


def local_health() -> dict[str, str]:
    """Return deterministic evidence that the local application boundary is healthy."""

    return {"application": "healthy", "configuration": "loaded"}


def storage_health() -> dict[str, str]:
    """Query the configured synthetic storage dependency."""

    storage_url = os.environ.get("STORAGE_URL", "http://127.0.0.1:45999/health")
    with urlopen(storage_url, timeout=1) as response:
        return json.load(response)


def main() -> int:
    """Print boundary evidence and return a nonzero status when storage is unavailable."""

    print(json.dumps(local_health(), sort_keys=True))
    try:
        print(json.dumps(storage_health(), sort_keys=True))
    except (TimeoutError, URLError) as error:
        print(f"storage dependency unavailable: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
