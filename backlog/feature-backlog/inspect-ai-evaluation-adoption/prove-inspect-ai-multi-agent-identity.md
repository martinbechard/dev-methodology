# Prove Inspect AI Multi-Agent Identity

Status: Ready

Type: Feature

Provider: file

Work Item ID: prove-inspect-ai-multi-agent-identity

Completion: main-branch

Series: backlog/feature-backlog/inspect-ai-evaluation-adoption/index.md

## Summary

Prove that an Inspect-backed evaluation can retain exact supervisor, target, dependency, and independent Judge identity and topology while preserving a governed BLOCKED outcome.

## Context

This phase is the decisive architectural test. Inspect supports native multi-agent workflows, but the repository requires exact generated-agent identity and parent-child evidence rather than labels or polished prose.

Estimated complexity is Very High. Estimated generation is 180,000–320,000 tokens, or 1.00–1.78 total agent-hours, across 10–18 turns. Estimated non-model runtime is 2–5 hours.

## Source Evidence

The user authorized the phased Inspect-first adoption series on 2026-08-12. This item implements Phase 3 of that proposal.

## Requirements

- Adapt dev-orchestrator / dependency-routing and terminal-status-integrity.
- Retain exact supervisor, target, dependency, and Judge definition identity.
- Retain parent-child relationships and ordered dependency activity.
- Give the Judge a fresh governed context and bind its result to the correct run and evidence.
- Preserve BLOCKED as correct safe behavior rather than a failed reward or infrastructure error.
- Measure how much existing session parsing remains necessary.

## Acceptance Criteria

- Both scenarios match current-runner governed status and deterministic dispositions.
- Identity and topology are proven by retained machine-readable evidence.
- Judge independence and output binding are independently verified.
- The implementation does not reconstruct most of the existing runner's harness parser.
- A written decision selects full Inspect continuation, a topology hybrid, or program stop.

## Dependencies

prove-read-only-inspect-ai-execution. Unblock after the read-only spike is accepted and its exact-agent invocation boundary is stable.

Derived Queue Evidence: Stored lifecycle remains Ready. Series order derives effective Holding behind a healthy predecessor or effective Blocked behind the first genuinely Blocked predecessor; do not rewrite this record for either derived state.

## Verification

- Execute parity runs with frozen scenarios and equivalent model settings.
- Perform adversarial checks for substituted agents, wrong parents, reused Judge context, and flattened BLOCKED results.
- Obtain independent architecture, code, and prompt-contract review.

## Open Questions

- Should Inspect orchestrate the agent stages, or should one external Codex execution remain the topology owner and export structured evidence to Inspect?
