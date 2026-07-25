# Reject Nonexistent Lifecycle Handoff Commit OIDs

Status: Ready

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/reject-nonexistent-lifecycle-handoff-commit-oids.md

Completion: direct-main

## Summary

Make lifecycle and provider handoffs derive each commit OID from Git after commit creation and verify the immutable object before reporting it as durable evidence.

## Context

A lifecycle Steward handoff reported commit OID `9cc052194342bddd471425ab9840f35aaf51ddf6`, but the committed lifecycle object is `9cc05219fbb2c10b80ef3300568398dd44f5f8a2`. On 2026-07-25, direct Git reproduction showed `git cat-file -t` rejects the reported OID and identifies the actual OID as a commit. A nonexistent or mistyped OID must not become durable lifecycle evidence.

## Source Evidence

Canonical task `019f9783-31a0-7e91-9704-08cde7886b3a` handoff and the direct Git reproduction on 2026-07-25. Standing user direction requires every confirmed defect to be logged durably.

## Requirements

- Capture the actual commit OID immediately from Git after commit creation.
- Use Git object inspection to verify the reported OID exists and is a commit before reporting it.
- Bind handoff changed-path and content evidence to that exact immutable commit object.
- Reject absent, non-commit, stale, or mismatched reported OIDs with structured error and recovery behavior.
- Preserve exact provider paths, canonical task identity, and claim-event evidence.
- Do not fabricate a correction by prefix matching or substitution.

## Acceptance Criteria

- A normal lifecycle commit reports the OID read back from Git and passes object inspection.
- A mistyped or nonexistent OID is rejected and cannot be persisted as handoff evidence.
- A non-commit or mismatched OID is rejected with the applicable structured recovery outcome.
- Tests cover stale HEAD movement and ambiguous commit dispatch without attributing mutable HEAD to the handoff.
- Terminal and source-move transactions bind their provider paths and content evidence to the verified immutable object.
- No prefix-based guessed correction is accepted.

## Dependencies

None.

## Verification

- Run focused Steward and lifecycle handoff tests.
- Run real disposable-Git tests for normal commit, mistyped OID, stale HEAD, ambiguous dispatch, and terminal/source-move transactions.
- Run relevant handoff schema and evaluation tests.
- Run `git diff --check` and obtain fresh independent review.

## Open Questions

- Which existing handoff schema field should carry the verified object type and immutable changed-path receipt without duplicating Git metadata?

## Notes

This record captures the confirmed defect only. Do not implement unrelated lifecycle corrections or mutate governed definitions without the required exact approval evidence.
