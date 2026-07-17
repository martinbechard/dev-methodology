# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies healthy work and the deterministic cancelled-lease stall.

from __future__ import annotations

import asyncio
import unittest

from worker import SyntheticWorker, reproduce_stall


class SyntheticWorkerTests(unittest.IsolatedAsyncioTestCase):
    async def test_normal_jobs_release_connections(self) -> None:
        worker = SyntheticWorker()

        await asyncio.gather(worker.handle(0.001), worker.handle(0.001))

        self.assertEqual(2, worker.available_connections)
        self.assertEqual(0, worker.retained_on_cancel)

    async def test_cancelled_jobs_produce_observable_stall(self) -> None:
        evidence = await reproduce_stall()

        self.assertEqual(1, evidence["queuedWorkObserved"])
        self.assertTrue(evidence["heartbeatAdvanced"])
        self.assertEqual(0, evidence["availableConnections"])
        self.assertEqual(2, evidence["retainedCancelledLeases"])
        self.assertFalse(evidence["followupCompleted"])


if __name__ == "__main__":
    unittest.main()
