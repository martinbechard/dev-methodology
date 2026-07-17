# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies the accepted contract that conflicts with the requested semantic change.

from __future__ import annotations

import unittest

import pricing


class AcceptedPricingContractTests(unittest.TestCase):
    def test_discount_is_a_percentage(self) -> None:
        self.assertEqual(90, pricing.total_after_discount(100, 10))

    def test_contract_rejects_more_than_thirty_percent(self) -> None:
        with self.assertRaisesRegex(ValueError, "from 0 through 30"):
            pricing.total_after_discount(100, 31)


if __name__ == "__main__":
    unittest.main()
