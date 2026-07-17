# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies the catalog responsibility in the multi-contribution fixture.

from __future__ import annotations

import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import catalog  # noqa: E402


class CatalogTests(unittest.TestCase):
    def test_sku_is_normalized(self) -> None:
        self.assertEqual("ABC-1", catalog.normalize_sku(" abc-1 "))


if __name__ == "__main__":
    unittest.main()
