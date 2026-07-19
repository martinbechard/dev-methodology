# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Defines the observable status contract for the synthetic dependency fixture.
# Governing design: ../fixture-contract.yaml

from __future__ import annotations

import unittest

from src.dependency_status import dependency_status


class DependencyStatusTests(unittest.TestCase):
    """Verify healthy and degraded dependency status responses."""

    def test_all_available_dependencies_are_ok(self) -> None:
        """Available dependencies produce an ok response with no unavailable names."""
        self.assertEqual(
            {"status": "ok", "unavailableDependencies": []},
            dependency_status({"database": True, "queue": True}),
        )

    def test_unavailable_dependencies_are_lexically_sorted(self) -> None:
        """A degraded response sorts unavailable names independently of input order."""
        self.assertEqual(
            {"status": "degraded", "unavailableDependencies": ["cache", "queue"]},
            dependency_status({"queue": False, "database": True, "cache": False}),
        )


if __name__ == "__main__":
    unittest.main()
