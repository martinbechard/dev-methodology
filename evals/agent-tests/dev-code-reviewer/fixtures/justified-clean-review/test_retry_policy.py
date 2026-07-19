# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Covers success, cap, and invalid-input behavior for the clean-review fixture.

from __future__ import annotations

import unittest

import retry_policy


class RetryPolicyTests(unittest.TestCase):
    def test_delay_doubles_from_the_first_attempt(self) -> None:
        self.assertEqual(5, retry_policy.retry_delay(1, 5, 30))
        self.assertEqual(10, retry_policy.retry_delay(2, 5, 30))

    def test_delay_is_capped(self) -> None:
        self.assertEqual(30, retry_policy.retry_delay(5, 5, 30))

    def test_invalid_attempt_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "at least one"):
            retry_policy.retry_delay(0, 5, 30)

    def test_invalid_delay_bounds_are_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "bounds are invalid"):
            retry_policy.retry_delay(1, 10, 5)


if __name__ == "__main__":
    unittest.main()
