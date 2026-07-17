# Agent-Owned Evaluation Suites

This is the primary organization for future behavioral evaluation work. Each suite starts from one canonical conceptual agent definition, derives a small set of high-value scenarios, runs the standard generated target agent, and evaluates the result through a hardcoded independent Judge.

The first wave covers the four roles with the broadest direct end-user value:

1. Dev Coder.
2. Dev Code Reviewer.
3. Dev Runtime Diagnostician.
4. Project Bootstrapper.

The common operating contract is in AGENTS.md. Suite order and concurrency policy are in suite-index.yaml. Shared project skills live under skills. Each named suite contains its own supervisor, Judge, scenarios, and target-specific contract skill.

The root coordinator may launch four supervisors concurrently. Each supervisor has only one active child at a time, so the normal execution ceiling is nine active agents including the root coordinator. A temporary tenth agent is allowed only for one canonical nested dependency declared by the active suite.

The existing catalogs and runner under evals remain the execution and evidence substrate while cases are migrated into this agent-owned layout. Skill probes become targeted diagnostic controls selected by an agent scenario; they are no longer the unit used to plan exhaustive coverage.
