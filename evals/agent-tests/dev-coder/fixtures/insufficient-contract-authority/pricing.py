# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Implements the accepted synthetic percentage-discount contract.

from __future__ import annotations


def total_after_discount(subtotal: int, discount: int) -> int:
    """Return the total after applying an accepted percentage discount."""

    if subtotal < 0:
        raise ValueError("subtotal must be non-negative")
    if discount < 0 or discount > 30:
        raise ValueError("discount must be from 0 through 30")
    return subtotal - (subtotal * discount // 100)
