# Agent-Owned Evaluation Suites

This is the steady-state organization for behavioral evaluation work. Each suite starts from one canonical conceptual agent definition, derives a small set of high-value scenarios, runs the standard generated target agent, and evaluates the result through a hardcoded independent Judge.

Suites are added and maintained in descending order of direct end-user value. The current catalog covers:

1. Dev Coder.
2. Dev Code Reviewer.
3. Dev Runtime Diagnostician.
4. Project Bootstrapper.

The common operating contract is in AGENTS.md. Suite order and concurrency policy are in suite-index.yaml. Shared project skills live under skills. Each named suite contains its own supervisor, Judge, one authoritative scenarios.yaml catalog, and target-specific contract skill.

Codex project-agent names use lowercase letters, digits, and underscores. Suite manifests hardcode the supervisor, target, and Judge runtime names separately from the portable conceptual role ids and generated adapter paths. A Codex run is valid only when retained session evidence proves that every child loaded the staged project-agent definition; task labels and final prose are insufficient.

The root coordinator may launch four supervisors concurrently. Each supervisor has only one active child at a time, so the normal execution ceiling is nine active agents including the root coordinator. A temporary tenth agent is allowed only for one canonical nested dependency declared by the active suite.

Durable governed-result summaries live under results. The initial identity-gated Codex execution is recorded in [the 2026-07-17 agent-suite report](results/2026-07-17-codex-agent-suites.md).

The existing catalogs and runner under evals remain the execution and evidence substrate while cases are migrated into this agent-owned layout. Skill probes become targeted diagnostic controls selected by an agent scenario; they are no longer the unit used to plan exhaustive coverage.
