# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
"""Verify the synthetic worker fixture."""

import unittest

from .main import normalize_event


class WorkerTests(unittest.TestCase):
    """Protect the fixture behavior during routing reconciliation."""

    def test_normalizes_event(self) -> None:
        """Whitespace and case are normalized."""
        self.assertEqual("PARCEL.CREATED", normalize_event(" parcel.created "))


if __name__ == "__main__":
    unittest.main()
