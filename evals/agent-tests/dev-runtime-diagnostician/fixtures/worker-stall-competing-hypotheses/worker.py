# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Models a worker whose cancellation path intentionally retains connection leases.

from __future__ import annotations

import asyncio


class SyntheticWorker:
    """Process jobs through a bounded synthetic connection pool."""

    def __init__(self, pool_size: int = 2) -> None:
        self._pool = asyncio.Semaphore(pool_size)
        self.pool_size = pool_size
        self.in_use = 0
        self.retained_on_cancel = 0
        self.heartbeat = 0

    @property
    def available_connections(self) -> int:
        """Return the observable number of unleased connections."""

        return self.pool_size - self.in_use

    async def heartbeat_loop(self) -> None:
        """Advance an independent heartbeat while the worker process remains healthy."""

        while True:
            self.heartbeat += 1
            await asyncio.sleep(0.005)

    async def handle(self, duration: float) -> None:
        """Handle one job, intentionally retaining its lease when cancelled."""

        await self._pool.acquire()
        self.in_use += 1
        try:
            await asyncio.sleep(duration)
        except asyncio.CancelledError:
            self.retained_on_cancel += 1
            raise
        else:
            self.in_use -= 1
            self._pool.release()


async def reproduce_stall() -> dict[str, int | bool]:
    """Return bounded evidence that distinguishes the competing stall hypotheses."""

    worker = SyntheticWorker()
    heartbeat_task = asyncio.create_task(worker.heartbeat_loop())
    cancelled_tasks = [asyncio.create_task(worker.handle(10)) for _ in range(2)]
    while worker.in_use < 2:
        await asyncio.sleep(0.005)
    for task in cancelled_tasks:
        task.cancel()
    await asyncio.gather(*cancelled_tasks, return_exceptions=True)
    heartbeat_before = worker.heartbeat
    await asyncio.sleep(0.03)
    heartbeat_advanced = worker.heartbeat > heartbeat_before
    followup = asyncio.create_task(worker.handle(0.001))
    try:
        await asyncio.wait_for(followup, timeout=0.03)
        followup_completed = True
    except asyncio.TimeoutError:
        followup_completed = False
    heartbeat_task.cancel()
    await asyncio.gather(heartbeat_task, return_exceptions=True)
    return {
        "queuedWorkObserved": 1,
        "heartbeatAdvanced": heartbeat_advanced,
        "availableConnections": worker.available_connections,
        "retainedCancelledLeases": worker.retained_on_cancel,
        "followupCompleted": followup_completed,
    }
