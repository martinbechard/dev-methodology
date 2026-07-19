# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Covers only the successful synthetic inventory-location normalization path.

from __future__ import annotations

import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from inventory import normalize_location


class InventoryNormalizationTests(unittest.TestCase):
    def test_normalizes_inventory_location(self) -> None:
        self.assertEqual("A-12", normalize_location(" a-12 "))


if __name__ == "__main__":
    unittest.main()
