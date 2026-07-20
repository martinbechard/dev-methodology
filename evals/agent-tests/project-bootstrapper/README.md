# Project Bootstrapper Suite

The required missing-configuration multi-contribution gate uses a scripted dependency protocol in a disposable workspace. It copies the selected Bootstrapper and Wiki Ingester roles, generated adapters, applicable skills, suite contracts, and frozen fixture before execution. It does not invoke a live agent pipeline or acquire a repository claim. Ordinary setup skips the final evidence audit; reverse-engineering mode transitions stale integrated artifacts to a reviewed steady state through a read-only Wiki Ingester audit and owner-routed corrections.

Run the deterministic gate:

```bash
python3.11 -m unittest evals/agent-tests/project-bootstrapper/test_scripted_orchestration.py
```

Run the whole-project reverse-engineering steady-state case directly:

```bash
python3.11 evals/agent-tests/project-bootstrapper/scripted_orchestration.py --reverse-engineering
```

Run the selected catalog validation without a harness:

```bash
python3.11 evals/agent-tests/runner.py --harness codex --scenario project-bootstrapper:missing-configuration-multi-contribution --validate-only
```

Print the optional live direct-path smoke command:

```bash
python3.11 evals/agent-tests/project-bootstrapper/live_smoke.py
```

Add the execute option only when the live smoke is intentionally authorized. The live smoke is not part of the deterministic gate.
