# Worker Stall Fixture

This synthetic asynchronous worker remains alive and advances a heartbeat after two tasks are cancelled, but the cancellation path retains every connection lease. A later task waits indefinitely for a lease. The bounded probe exposes queue, heartbeat, and pool evidence so queue starvation, CPU saturation, and resource leakage can be compared.

Run the reproduction:

```bash
python3 reproduce.py
```

Run the focused fixture tests:

```bash
python3 -m unittest test_worker.py
```
