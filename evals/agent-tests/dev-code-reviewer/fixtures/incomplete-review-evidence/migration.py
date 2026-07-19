# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Provides an inspectable configuration migration with intentionally incomplete upgrade evidence.

from __future__ import annotations

from typing import Any


def normalize_version_two(config: dict[str, Any]) -> dict[str, Any]:
    """Normalize a version-two configuration without claiming version-one support."""

    if config.get("version") != 2:
        raise ValueError("only version two evidence is available")
    endpoint = config.get("endpoint")
    if not isinstance(endpoint, str) or not endpoint:
        raise ValueError("endpoint is required")
    return {"version": 2, "endpoint": endpoint.rstrip("/")}
