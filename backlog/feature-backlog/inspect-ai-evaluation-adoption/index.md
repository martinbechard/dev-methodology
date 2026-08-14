# Inspect AI Evaluation Adoption

## Goal

Adopt Inspect AI as the primary candidate execution substrate for the repository's governed agent evaluation suites while preserving exact identity, topology, evidence, lifecycle, mutation, containment, cleanup, and terminal-status guarantees.

## Purpose

The existing evaluation system contains both commodity infrastructure and distinctive governance. Inspect AI may replace task scheduling, sandbox execution, external CLI-agent invocation, transcript storage, scorer execution, and diagnostic viewing. The repository must retain acceptance authority for PASS, FAIL, BLOCKED, STALE, and INFRASTRUCTURE_FAILED until parity evidence proves that an Inspect-backed implementation preserves those meanings.

Harbor is outside this series' critical path. It may be reconsidered later for Terminal-Bench interoperability, published benchmark consumption, or training-rollout workflows.

## Source Evidence

On 2026-08-12 in Codex task 019ff660-663f-7271-a4da-c30e6c054cf7, the user selected an Inspect AI focus after reviewing Harbor and requested a new plan. After receiving the phased Inspect-first plan, the user explicitly requested: "ok create a suite of backlog items for this - maybe one backlog item per phase? all in the same folder".

## Design Anchors

- Current suite and scenario YAML remain canonical during the pilot and generated-adapter phase.
- Inspect owns execution and diagnostic presentation only where parity is demonstrated.
- Repository-owned verification continues to own governed acceptance status and immutable evidence.
- Migration proceeds by capability, not by agent name.
- Dual execution uses frozen scenarios and compares deterministic dispositions, not only aggregate scores.
- Numeric rewards must not flatten BLOCKED, STALE, or infrastructure outcomes.
- Removal of existing runner code follows demonstrated replacement; it never precedes parity.

## Agent-Effort Assumption

Planning estimates use generated output tokens, including reasoning, at an assumed 50 tokens per second. One agent-hour therefore equals 180,000 generated tokens. Estimates report non-model runtime separately and distinguish total agent-hours from critical-path elapsed time.

## Required Order

1. [Map Evaluation Contracts To Inspect AI](../../completed-backlog/analyses/map-evaluation-contracts-to-inspect-ai.md)
2. [Prove Read-Only Inspect AI Execution](prove-read-only-inspect-ai-execution.md)
3. [Prove Inspect AI Multi-Agent Identity](prove-inspect-ai-multi-agent-identity.md)
4. [Prove Inspect AI Mutation And Lifecycle Parity](prove-inspect-ai-mutation-lifecycle-parity.md)
5. [Prove Inspect AI Exceptional Runtime Parity](prove-inspect-ai-exceptional-runtime-parity.md)
6. [Integrate Inspect AI Reporting And Evidence](integrate-inspect-ai-reporting-evidence.md)
7. [Generate The Inspect AI Evaluation Catalog](generate-inspect-ai-evaluation-catalog.md)
8. [Migrate Evaluation Suites To Inspect AI](migrate-evaluation-suites-to-inspect-ai.md)

This order defines dependency scheduling for the series. A healthy nonterminal predecessor makes later children effectively Holding without rewriting their stored lifecycle. A genuinely impeded child alone stores Blocked; later children derive effective Blocked from that first stored blocker. Completed children may move to their canonical archive while retaining their ordered identity here.

## Program Stop Conditions

- Stop full replacement when exact Codex child identity or parent topology would require reconstructing most of the existing harness parser.
- Retain specialized current-runner lanes when Inspect weakens claims, commits, mutation boundaries, browser containment, or cleanup evidence.
- Reject adoption when the combined Inspect adapter and verifier do not remove a material portion of current maintenance.
- Prefer a stable hybrid over forced full migration.

## Definition Of Good

- Inspect provides materially better execution portability and trajectory diagnosis.
- Governed terminal status remains machine-verifiable and independent of presentation.
- Adding or maintaining a scenario consumes fewer agent-hours after migration.
- Existing runner responsibilities are removed only with direct replacement evidence.
- The final architecture has one acceptance authority and no competing truth systems.
