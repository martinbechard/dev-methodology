# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies only the available version-two migration boundary.

from __future__ import annotations

import unittest

import migration


class AvailableMigrationEvidenceTests(unittest.TestCase):
    def test_version_two_endpoint_is_normalized(self) -> None:
        self.assertEqual(
            {"version": 2, "endpoint": "https://fixture.invalid/api"},
            migration.normalize_version_two(
                {"version": 2, "endpoint": "https://fixture.invalid/api/"}
            ),
        )

    def test_version_one_is_not_claimed_as_supported(self) -> None:
        with self.assertRaisesRegex(ValueError, "only version two"):
            migration.normalize_version_two({"version": 1, "url": "legacy"})


if __name__ == "__main__":
    unittest.main()
