# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Provides the order-total responsibility for the multi-contribution bootstrap fixture.

from __future__ import annotations


def order_total(unit_price: int, quantity: int) -> int:
    """Return a non-negative integer order total."""

    if unit_price < 0 or quantity < 0:
        raise ValueError("price and quantity must be non-negative")
    return unit_price * quantity
