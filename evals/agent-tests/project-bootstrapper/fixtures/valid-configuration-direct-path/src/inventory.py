# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Provides one stable runtime responsibility for the direct bootstrap fixture.

from __future__ import annotations


def available_items(stock: dict[str, int]) -> list[str]:
    """Return sorted item names whose quantity is positive."""

    return sorted(name for name, quantity in stock.items() if quantity > 0)
