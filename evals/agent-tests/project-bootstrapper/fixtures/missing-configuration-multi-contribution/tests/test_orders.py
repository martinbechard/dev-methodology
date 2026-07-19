# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies the order responsibility in the multi-contribution fixture.

from __future__ import annotations

import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import orders  # noqa: E402


class OrderTests(unittest.TestCase):
    def test_order_total_multiplies_price_and_quantity(self) -> None:
        self.assertEqual(21, orders.order_total(7, 3))


if __name__ == "__main__":
    unittest.main()
