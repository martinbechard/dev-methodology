# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies the healthy local boundary independently from the intentionally absent storage service.

from __future__ import annotations

import unittest

import app


class LocalHealthTests(unittest.TestCase):
    def test_local_health_is_available_without_storage(self) -> None:
        self.assertEqual(
            {"application": "healthy", "configuration": "loaded"},
            app.local_health(),
        )


if __name__ == "__main__":
    unittest.main()
