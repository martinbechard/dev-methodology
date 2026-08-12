# Prove Inspect AI Exceptional Runtime Parity

Status: Holding

Type: Feature

Provider: file

Work Item ID: prove-inspect-ai-exceptional-runtime-parity

Completion: main-branch

Series: backlog/feature-backlog/inspect-ai-evaluation-adoption/index.md

## Summary

Evaluate whether Inspect can safely replace current browser, loopback, and child-process runtime infrastructure without losing containment, evidence, or cleanup guarantees.

## Context

Browser brokerage and shared runtime resources are the least portable portion of the current harness. A stable hybrid is acceptable when Inspect cannot replace these lanes proportionately.

Estimated complexity is Very High. Estimated generation is 220,000–400,000 tokens, or 1.22–2.22 total agent-hours, across 14–22 turns. Estimated non-model runtime is 3–8 hours.

## Source Evidence

The user authorized the phased Inspect-first adoption series on 2026-08-12. This item implements Phase 5 of that proposal.

## Requirements

- Adapt dev-browser-operator / persisted-setting-workflow and blocked-route-owned-cleanup.
- Adapt one loopback or child-process diagnostic scenario selected from current catalog evidence.
- Compare Inspect sandbox, tool, network, process, browser, screenshot, trace, and artifact capabilities with the existing broker.
- Preserve exact target authorship, containment, non-local network denial, resource identity, and explicit cleanup evidence.
- Recommend full migration, retained specialized lanes, or no migration for each capability.

## Acceptance Criteria

- Adapted scenarios retain their governed statuses and critical evidence or are explicitly rejected from migration.
- No target can forge tamper-sensitive browser, process, or service evidence.
- Every owned runtime resource has independently verifiable cleanup.
- The outcome defines a stable capability routing table for later generation and migration.

## Dependencies

prove-inspect-ai-mutation-lifecycle-parity. Unblock after ordinary mutation and lifecycle boundaries are accepted.

Queued Dependency Evidence: This is a normal predecessor wait, not a current impediment. Resume to Ready after the predecessor completes; propagate Blocked only if that predecessor becomes truly Blocked.

## Verification

- Run focused containment, forged-evidence, network-denial, and interrupted-cleanup cases.
- Compare current and Inspect traces and retained artifacts.
- Obtain independent runtime and security review.

## Open Questions

- Can Inspect's browser and sandbox extensions replace the authenticated one-shot broker without expanding the target's authority?
