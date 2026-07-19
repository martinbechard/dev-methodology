# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Provides the synthetic dependency availability status used by the routing fixture.
# Governing test plan: tests/test_dependency_status.py

from __future__ import annotations


def dependency_status(dependencies: dict[str, bool]) -> dict[str, object]:
    """Summarize named dependency availability for the synthetic operator contract.

    The dependencies mapping associates each synthetic dependency name with its
    availability. The returned mapping contains ok or degraded status and the
    unavailable dependency names. This function has no I/O or external effects.
    """
    unavailable = [name for name, available in dependencies.items() if not available]
    return {
        "status": "degraded" if unavailable else "ok",
        "unavailableDependencies": unavailable,
    }
