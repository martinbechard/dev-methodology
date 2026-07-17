# Retained Process Port Fixture

This synthetic service launches a child socket process. The normal leaky shutdown path exits the parent but leaves the child holding the configured port. The reproduction command captures the parent and child process evidence, proves the bind failure, terminates only the fixture child, and confirms that the port is released. A separate clean-mode command performs three start-stop cycles using the narrow lifecycle intervention.

Run the bounded reproduction:

```bash
python3 lifecycle_probe.py reproduce
```

Verify repeated clean restarts:

```bash
python3 lifecycle_probe.py verify-clean
```

Both commands own and clean up their synthetic processes. They choose an available loopback port at runtime.
