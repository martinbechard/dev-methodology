# Support Existing Isolated Correction Worktree Binding

Status: Running

Type: Defect

Owner: Dev Orchestrator

Provider: file

Provider Reference: backlog/defect-backlog/support-existing-isolated-correction-worktree-binding.md

Completion: direct-main

## Launch Reservation

- Canonical Task/Thread: 019f976c-6691-7a83-9df4-e73fc0baae73
- Reservation: One parent-owned launch reservation.
- Intended Root Role: Dev Orchestrator
- Isolated Checkout: /Users/martinbechard/.codex/worktrees/0311/dev-methodology
- Phase: Awaiting root lifecycle acceptance.
- Dispatched At: 2026-07-25T03:58:59Z

## Lifecycle Start

- Canonical Task/Thread: 019f976c-6691-7a83-9df4-e73fc0baae73
- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Root Role And Owner: Dev Orchestrator
- Isolated Worktree Binding: /Users/martinbechard/.codex/worktrees/0311/dev-methodology
- Canonical Branch State: detached at 3f30d7c7d56dfea4ca23ca2a9afa8df55e9d138e
- Phase: Root lifecycle accepted; delivery proceeds only in the canonical isolated correction worktree.
- Started At: 2026-07-25T04:01:00.487775Z, after the root Dev Orchestrator accepted ownership.
- Coordination Claim: Dev Backlog Steward acquired short primary-main backlog claim support-existing-isolated-correction-worktree-binding-running-019f976c at event 41049fc1-bf18-453e-a663-7f7876efc28e from baseline commit ff63b40b46571f22fd5c5624c79d856ff9b243cf.
- Scope Boundary: This claim owns only the committed Starting-to-Running provider transition and must release immediately; delivery owns separate isolated project-artifact scope.

## Summary

Make the claim transport and topology contract support explicit safe setup or reuse of a canonical correction task’s existing clean isolated worktree and branch even when no peer writer is active.

## Context

The current behavior can depend on an incidental competing claim to reach an isolated-worktree path. With an empty registry, a User Action Required correction received `SHARED_CHECKOUT_ACQUIRED` and released no-change event `0273f787-2f05-44a4-9b87-b96e9ac7858e`; a campaign correction likewise released no-change event `8d47aaf7-6f04-4267-9ced-6e473f8d9df9`. A durable-defect task received isolated setup events `a279c96b-ae93-4ce1-af04-dbaabbdafd63` and `405af7d3-cf11-4fec-9a59-cb00bdd22a1e` while another writer was active, but after the registry emptied, its explicit existing-worktree acquisition returned `SHARED_CHECKOUT_ACQUIRED` event `5bcd13c9-8d50-4258-ae22-72d4bfc3e4b2` and released no-change event `120a4e32-7a33-4b6c-9c59-8e8ae6eb37cb`.

## Source Evidence

Repeated confirmed coordination failure in canonical tasks `019f9722-61cb-7190-8a6d-21c5ab319339` and `019f96cf-226c-7f62-9d66-7d31cead822e`. Standing user direction requires every found defect to be durably logged and never ignored as a warning.

## Requirements

- Support explicit safe isolated-worktree setup or reuse independently of another active writer’s claim.
- Preserve the same canonical task, worktree, branch, and candidate bytes throughout correction setup and reuse.
- Treat supplied branch, base, and worktree intent as binding; do not silently ignore or replace it.
- Produce deterministic first-writer versus explicit-isolation outcomes.
- Keep primary main untouched until accepted delivery is ready for its authorized integration transaction.
- Reject dirty, stale, mismatched, or noncanonical existing worktrees.
- Preserve all existing overlap, primary-main, and dirty-owner safeguards.
- Journal the exact requested binding, resolved binding, and structured outcome.

## Acceptance Criteria

- A no-peer explicit-isolation request creates or binds the intended isolated worktree rather than acquiring the primary checkout.
- An active-peer explicit-isolation request preserves the same safe isolated behavior.
- A clean existing canonical worktree is reused with the exact task, branch, base, and candidate binding intact.
- Dirty, stale, branch-mismatched, base-mismatched, or worktree-mismatched requests are rejected without primary mutation.
- Tests prove exact base/branch binding, no primary mutation before accepted delivery, and overlap/dirty-owner safeguards.
- Registry, journal, and release evidence record the exact binding and outcome for success, rejection, and no-change release.

## Dependencies

None.

## Verification

- Run focused claim-engine and command-transport tests.
- Run focused lifecycle and coordination tests.
- Exercise exact real-Git worktree scenarios for no-peer isolation, active-peer isolation, existing reuse, binding mismatch, dirty state, and stale state.
- Run the full applicable shared-infrastructure regression and `git diff --check`.
- Obtain fresh independent review.

## Open Questions

- Which existing claim command fields and journal schema can express explicit reuse without widening the canonical worktree authority boundary?

## Notes

This record captures the defect only. Any governed-definition changes discovered during delivery require an exact canonical-path approval record before mutation.
