# Agent-Owned Evaluation Suites

This is the steady-state organization for behavioral evaluation work. Each suite starts from one canonical conceptual agent definition, derives a small set of high-value scenarios, runs the standard generated target agent, and evaluates the result through a hardcoded independent Judge.

Suites are maintained in descending order of direct end-user value. The catalog contains one executable suite for every conceptual agent definition, from Dev Coder through Methodology Artifact Reviewer.

The common operating contract is in AGENTS.md. Suite order and concurrency policy are in suite-index.yaml. Shared project skills live under skills. Each named suite contains its own supervisor, Judge, one authoritative scenarios.yaml catalog, and target-specific contract skill.

Codex project-agent names use lowercase letters, digits, and underscores. Suite manifests hardcode the supervisor, target, and Judge runtime names separately from the portable conceptual role ids and generated adapter paths. A Codex run is valid only when retained session evidence proves that every child loaded the staged project-agent definition; task labels and final prose are insufficient.

The root coordinator may launch four supervisors concurrently. Each supervisor has only one active child at a time, so the normal execution ceiling is nine active agents including the root coordinator. A temporary tenth agent is allowed only for one canonical nested dependency declared by the active suite.

Durable governed-result summaries live under results. The initial identity-gated Codex execution is recorded in [the 2026-07-17 agent-suite report](results/2026-07-17-codex-agent-suites.md). The completed 26-suite, 78-scenario rollout is recorded in [the complete agent-suite execution report](results/2026-07-17-complete-agent-suites.md).

The existing catalogs and runner under evals remain the execution and evidence substrate while cases are migrated into this agent-owned layout. Skill probes become targeted diagnostic controls selected by an agent scenario; they are no longer the unit used to plan exhaustive coverage.

The bounded suite runner validates the complete catalog, accepts suite and scenario selections, groups at most four ordinary supervisors per coordinator batch, retains partial failures, records UTC and monotonic timing, and removes disposable workspaces and isolated authentication state after each batch.

The reporting command requires an explicit Codex or Junie harness, resolves a worker ceiling from selected suite count, processors, available memory, and the repository ceiling of four, and gives every suite a disjoint run, evidence, checkpoint, and report destination. Codex binds generated TOML agent definitions by digest. Junie stages only Junie Markdown custom agents and requires every retained lifecycle receipt to bind the staged definition marker and digest. A name-only Junie ledger is retained but yields BLOCKED rather than PASS. Full Junie catalog execution additionally requires the explicit allow-full-junie option so smoke defaults cannot spend the complete Junie credit budget accidentally.

Run one suite and update its independent report plus the global report:

```bash
python3 evals/agent-tests/suite_reporting.py run --harness codex --suite dev-coder
```

Run several selected suites with a lower worker cap:

```bash
python3 evals/agent-tests/suite_reporting.py run --harness codex --suite dev-coder --suite dev-code-reviewer --max-workers 2
```

Omit suite selectors to run the complete catalog for Codex:

```bash
python3 evals/agent-tests/suite_reporting.py run --harness codex
```

Junie uses the same selector and report contract. A selected Junie smoke run does not require the full-catalog authorization:

```bash
python3 evals/agent-tests/suite_reporting.py run --harness junie --suite dev-coder
```

The report-only rebuild reads durable suite metadata and never invokes a harness:

```bash
python3 evals/agent-tests/suite_reporting.py rebuild --harness codex
```

Regenerating one selected suite writes only that suite's immutable generation and stable manifest, then deterministically updates aggregate counts and its global entry. The explicit update command rebuilds the global HTML from the same retained metadata without running or rewriting any suite report:

```bash
python3 evals/agent-tests/suite_reporting.py update --harness codex
```

Each suite generation stores self-contained HTML and machine-readable metadata together under one content-addressed immutable generation directory. A single stable suite manifest points to both files with their digests and is replaced atomically only after the complete generation is durable, so interruption cannot expose HTML from one generation with metadata from another. The global HTML follows only those stable manifests and reports deterministic current terminal-status totals beside input-state totals. Missing, stale, malformed, duplicate, incompatible-revision, and mixed-harness inputs remain visible as non-passing input states.

Scenarios declare exceptional runtime facilities through runtimeCapabilities. Offline Node fixtures receive only the selected project dependency tree after its installed TypeScript version matches the tracked lockfile. Offline Maven fixtures receive only checksum-pinned repository files named by the selected project manifest; the isolated home forces Maven offline and the runner proves the fixture tests before model execution. Loopback, descendant-process, and browser scenarios run as isolated single-supervisor batches through a managed permission profile that permits local binding, denies non-local network destinations, and keeps filesystem writes inside the disposable workspace. Browser cases stage the bundled Browser and computer-use runtimes into the isolated Codex home and expose only the in-app backend. A browser PASS requires retained target-session evidence for a fresh local-target tab, interaction, and tab close. When a detached Codex CLI session cannot attach to the desktop in-app browser, the target must initialize browser control, request the in-app backend, confirm the empty inventory, avoid creating a tab, and report BLOCKED. Existing tabs, Chrome, authenticated state, and non-local destinations remain prohibited. The runner preflights each declared facility before starting the model and retains the preflight evidence in the batch result.
