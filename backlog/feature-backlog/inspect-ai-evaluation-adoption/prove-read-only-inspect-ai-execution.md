# Prove Read-Only Inspect AI Execution

Status: Blocked

Type: Feature

Provider: file

Work Item ID: prove-read-only-inspect-ai-execution

Completion: main-branch

Series: backlog/feature-backlog/inspect-ai-evaluation-adoption/index.md

## Summary

Implement the smallest Inspect-backed Codex evaluation path and prove parity for the read-only dev-code-reviewer justified-clean-review scenario.

## Context

The first executable spike must isolate basic task translation, exact generated-agent configuration, read-only workspace enforcement, deterministic scoring, independent judging, and diagnostic log quality before adding mutation or complex topology.

Estimated complexity is Medium. Estimated generation is 90,000–160,000 tokens, or 0.50–0.89 total agent-hours, across 6–10 turns. Estimated non-model runtime is 1–3 hours.

## Source Evidence

The user authorized the phased Inspect-first adoption series on 2026-08-12. This item implements Phase 2 of that proposal.

## Requirements

- Pin and install Inspect through a repository-supported isolated development path.
- Adapt dev-code-reviewer / justified-clean-review without changing its frozen behavior contract.
- Invoke Codex CLI with the exact generated target configuration.
- Preserve a read-only fixture and capture complete mutation evidence.
- Run deterministic checks before a fresh independent Judge.
- Retain Inspect logs, transcript, scorer output, target output, and governed result evidence.
- Compare diagnostic usability with the current report.

## Acceptance Criteria

- Inspect and the current runner produce the same governed status and deterministic dispositions.
- Exact target configuration evidence is retained.
- The fixture remains unchanged and that fact is independently verified.
- Judge inputs exclude unauthorized context.
- The Inspect viewer exposes a materially useful trajectory and scoring record.
- The result states whether Phase 3 may proceed.

## Dependencies

map-evaluation-contracts-to-inspect-ai. Unblock when its accepted mapping explicitly authorizes the Phase 2 execution design.

## Verification

- Run the frozen scenario once through each harness under equivalent model settings.
- Validate retained artifacts and hashes.
- Obtain independent code review and parity verification.

## Open Questions

- Does Inspect's external Codex integration expose the exact configuration identity directly, or is a narrow adapter required?
