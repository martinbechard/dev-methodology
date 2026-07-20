# Project Bootstrapper Suite

The required missing-configuration multi-contribution gate uses a scripted dependency protocol in a disposable workspace. It copies the selected Bootstrapper role, generated adapter, applicable skills, suite contracts, and frozen fixture before execution. It does not invoke a live agent pipeline or acquire a repository claim.

Run the deterministic gate:

```bash
python3.11 -m unittest evals/agent-tests/project-bootstrapper/test_scripted_orchestration.py
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
