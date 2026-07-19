# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Implements a bounded exponential retry delay for the clean-review fixture.

from __future__ import annotations


def retry_delay(attempt: int, base_delay: int, maximum_delay: int) -> int:
    """Return the accepted bounded delay for a one-based attempt number."""

    if attempt < 1:
        raise ValueError("attempt must be at least one")
    if base_delay < 1 or maximum_delay < base_delay:
        raise ValueError("delay bounds are invalid")
    return min(base_delay * (2 ** (attempt - 1)), maximum_delay)
