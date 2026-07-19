# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Provides the catalog responsibility for the multi-contribution bootstrap fixture.

from __future__ import annotations


def normalize_sku(sku: str) -> str:
    """Normalize a synthetic stock-keeping unit."""

    normalized = sku.strip().upper()
    if not normalized:
        raise ValueError("sku is required")
    return normalized
