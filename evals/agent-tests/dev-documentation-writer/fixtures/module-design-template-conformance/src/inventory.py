# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Provides the synthetic inventory-location normalization behavior under documentation.

from __future__ import annotations


def normalize_location(value: str) -> str:
    """Normalize one required inventory location for callers.

    The input is stripped and uppercased. A value that becomes blank raises
    ValueError before a result is returned. The function performs no I/O and
    retains no state.
    """

    normalized = value.strip().upper()
    if not normalized:
        raise ValueError("location is required")
    return normalized
