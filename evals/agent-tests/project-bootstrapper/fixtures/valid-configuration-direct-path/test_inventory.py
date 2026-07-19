# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies the stable source behavior in the direct bootstrap fixture.

from __future__ import annotations

import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

import inventory  # noqa: E402


class InventoryTests(unittest.TestCase):
    def test_available_items_are_filtered_and_sorted(self) -> None:
        self.assertEqual(
            ["bolts", "washers"],
            inventory.available_items({"washers": 4, "nuts": 0, "bolts": 2}),
        )


if __name__ == "__main__":
    unittest.main()
