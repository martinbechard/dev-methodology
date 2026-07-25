# Align Coordinator UNSET Selection With User Action Required Reconciliation

Status: Ready

Type: Defect

Owner: Unowned

Claim: None

Provider: file

Provider Reference: backlog/defect-backlog/align-coordinator-unset-selection-with-user-action-required-reconciliation.md

Completion: direct-main

## Summary

Align the Dev Backlog Coordinator behavior for an UNSET Persistence selection with the Coordinator to task-local User Action Required reconciliation and same-task user-question protocol.

## Context

A fresh prompt-contract review of User Action Required candidate 331c33eb in canonical task 019f9722-61cb-7190-8a6d-21c5ab319339 found that agents/roles/dev-activities/dev-backlog-coordinator.role.yaml still reports BLOCKED and directly requests provider selection when Persistence is UNSET. That behavior conflicts with the Coordinator to task-local User Action Required reconciliation to same-task question contract.

## Source Evidence

The user's original authorized item requires every additional confirmed distinct defect to be logged durably, never as a warning. The fresh independent-review finding described above is a distinct defect.

## Requirements

- Treat a missing Persistence selection as a genuine user-owned gate.
- Require the Coordinator to record and verify the complete task-local User Action Required request envelope before the canonical work-item task presents it.
- Do not mutate a provider or infer a provider selection while Persistence is UNSET.
- Preserve the same canonical task and record the user answer exactly once.
- Resume the normal lifecycle only after provider selection is recorded.

## Acceptance Criteria

1. Coordinator behavior rejects a direct-ask or BLOCKED bypass when Persistence is UNSET.
2. The canonical work-item task presents the reconciled task-local User Action Required request rather than duplicating or bypassing it.
3. Tests cover an UNSET selection, an unavailable selected manager, provider none, and ambiguous presentation or answer cases.
4. Tests reject duplicate or repeated questions and confirm that the same task and answer are retained exactly once.
5. Provider selection resumes the normal lifecycle only after the recorded user answer resolves the gate.

## Dependencies

- explain-user-action-required-with-examples delivery or its accepted protocol.

## Verification

- Run focused Coordinator prompt and evaluator tests.
- Run generated-definition freshness checks for the approved implementation scope.
- Obtain fresh independent review.

## Open Questions

- The exact governed canonical implementation scope and its supported mirrors require separate explicit user approval at execution time; this creation does not approve them.

## Notes

This file-provider creation records the defect only. It does not authorize artifact mutation, provider mutation, or work-item dispatch.
