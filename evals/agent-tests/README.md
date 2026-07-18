# Agent-Owned Evaluation Suites

This is the steady-state organization for behavioral evaluation work. Each suite starts from one canonical conceptual agent definition, derives a small set of high-value scenarios, runs the standard generated target agent, and evaluates the result through a hardcoded independent Judge.

Suites are maintained in descending order of direct end-user value. The catalog contains one executable suite for every conceptual agent definition, from Dev Coder through Methodology Artifact Reviewer.

The common operating contract is in AGENTS.md. Suite order and concurrency policy are in suite-index.yaml. Shared project skills live under skills. Each named suite contains its own supervisor, Judge, one authoritative scenarios.yaml catalog, and target-specific contract skill.

Codex project-agent names use lowercase letters, digits, and underscores. Suite manifests hardcode the supervisor, target, and Judge runtime names separately from the portable conceptual role ids and generated adapter paths. A Codex run is valid only when retained session evidence proves that every child loaded the staged project-agent definition; task labels and final prose are insufficient.

The root coordinator may launch four supervisors concurrently. Each supervisor has only one active child at a time, so the normal execution ceiling is nine active agents including the root coordinator. A temporary tenth agent is allowed only for one canonical nested dependency declared by the active suite.

Durable governed-result summaries live under results. The initial identity-gated Codex execution is recorded in [the 2026-07-17 agent-suite report](results/2026-07-17-codex-agent-suites.md).

The existing catalogs and runner under evals remain the execution and evidence substrate while cases are migrated into this agent-owned layout. Skill probes become targeted diagnostic controls selected by an agent scenario; they are no longer the unit used to plan exhaustive coverage.

The bounded suite runner validates the complete catalog, accepts suite and scenario selections, groups at most four ordinary supervisors per coordinator batch, retains partial failures, records UTC and monotonic timing, and removes disposable workspaces and isolated authentication state after each batch.

Scenarios declare exceptional runtime facilities through runtimeCapabilities. Offline Node fixtures receive only the selected project dependency tree after its installed TypeScript version matches the tracked lockfile. Loopback, descendant-process, and browser scenarios run as isolated single-supervisor batches through a managed permission profile that permits local binding, denies non-local network destinations, and keeps filesystem writes inside the disposable workspace. Browser cases stage the bundled in-app Browser runtime into the isolated Codex home, open fresh local-target tabs, and prohibit existing tabs or authenticated state. The runner preflights each declared facility before starting the model and retains the preflight evidence in the batch result.
