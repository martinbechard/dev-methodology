# Prove Inspect AI Mutation And Lifecycle Parity

Status: Holding

Type: Feature

Provider: file

Work Item ID: prove-inspect-ai-mutation-lifecycle-parity

Completion: main-branch

Series: backlog/feature-backlog/inspect-ai-evaluation-adoption/index.md

## Summary

Prove that Inspect preserves repository mutation, test transition, Git commit, resource-claim, cleanup, and safe-refusal contracts for representative governed scenarios.

## Context

Functional success is insufficient when the agent writes outside allowed paths, weakens tests, loses commit evidence, mishandles claims, or invents authority. This phase tests the principal stateful guarantees.

Estimated complexity is High. Estimated generation is 180,000–300,000 tokens, or 1.00–1.67 total agent-hours, across 10–16 turns. Estimated non-model runtime is 2–5 hours.

## Source Evidence

The user authorized the phased Inspect-first adoption series on 2026-08-12. This item implements Phase 4 of that proposal.

## Requirements

- Adapt dev-coder / typescript-behavior-change and insufficient-contract-authority.
- Adapt dev-backlog-steward / creation-and-claim or the closest current representative claim scenario established during discovery.
- Preserve disposable Git repository behavior, allowed-path checks, test-state transitions, required command outcomes, commits, claim lifecycle, and cleanup.
- Distinguish successful mutation, correct refusal, target failure, and infrastructure failure.
- Prevent Inspect scores from overriding governed acceptance.

## Acceptance Criteria

- Every adapted scenario matches current-runner status and deterministic dispositions.
- No scenario gains PASS through weakened mutation, claim, commit, test, or cleanup evidence.
- Retained artifacts permit independent recomputation of the relevant gates.
- The result identifies which lifecycle runner components Inspect replaces and which remain.

## Dependencies

prove-inspect-ai-multi-agent-identity. Unblock when the accepted topology decision defines how target and Judge evidence enter the verifier.

Queued Dependency Evidence: This is a normal predecessor wait, not a current impediment. Resume to Ready after the predecessor completes; propagate Blocked only if that predecessor becomes truly Blocked.

## Verification

- Run frozen dual-harness scenarios.
- Add focused negative tests for forbidden writes, missing commit evidence, invalid claims, and false clean-state reports.
- Obtain independent code and acceptance-parity review.

## Open Questions

- Which claim operations can run inside an Inspect sandbox without weakening primary-worktree authority?
