# Report Linked Checkout Topology Accurately For No-Peer Claims

Status: Starting

Type: Defect

Owner: Dev Orchestrator

Provider: file

Provider Reference: backlog/defect-backlog/report-linked-checkout-topology-accurately-for-no-peer-claims.md

Completion: direct-main

## Launch Reservation

- Parent Coordinator Task: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Canonical Task/Thread: 019f977f-8bf5-77a1-b3c8-b55a113736d7
- Reservation: One parent-owned launch reservation.
- Intended Root Role: Dev Orchestrator
- Isolated Checkout: /Users/martinbechard/.codex/worktrees/c3a7/dev-methodology
- Phase: Awaiting root lifecycle acceptance.
- Dispatched At: 2026-07-25T04:19:36Z

## Summary

Make claim result and journal topology labels accurately distinguish the ownership or acquisition policy from the physical checkout used when a no-peer project-file acquisition is invoked from an existing linked private checkout.

## Context

A fresh independent review of canonical task 019f976c-6691-7a83-9df4-e73fc0baae73 found event 5bcd13c9-8d50-4258-ae22-72d4bfc3e4b2 in /Users/martinbechard/dev/dev-methodology/.git/agent-claim-events/hot/2026-07-25.jsonl. The acquisition was invoked from the existing linked private branch codex/durable-defect-creation-coder-019f96cf, but the result and journal labeled mode and worktree_id as primary.

The existing _acquire behavior assigns primary mode for any no-peer current checkout. The resulting diagnostic label can mislead root-cause analysis, even though it did not block private-worktree reuse or mutate primary main.

## Source Evidence

- Fresh independent review of canonical task 019f976c-6691-7a83-9df4-e73fc0baae73 identified the cited journal event and observed linked checkout.
- The no-peer acquisition came from the existing private branch codex/durable-defect-creation-coder-019f96cf, while the structured result and journal reported primary topology labels.
- The separate investigation found canonical private-worktree claim exemption and first-writer shared behavior intentional; this item concerns diagnostic topology accuracy only.

## Requirements

- Accurately report the physical checkout topology for a no-peer project-file acquisition invoked from an existing linked private checkout.
- Distinguish physical checkout reporting from ownership or acquisition policy without changing canonical first-writer shared behavior.
- Preserve private-worktree claim exemption, overlap safeguards, dirty-owner safeguards, primary-main and backlog boundaries, legacy structured-outcome compatibility, and privacy-safe bounded journal fields.
- Do not add explicit transport rebinding as part of this defect.
- Preserve the guarantee that the diagnostic path does not mutate primary main.

## Acceptance Criteria

- Real-Git coverage verifies correct reporting from a primary checkout, a claim-created isolated checkout, and an existing linked private checkout.
- No-peer and active-peer paths report topology accurately while preserving stable structured outcomes and legacy mode semantics.
- Journal assertions verify the bounded topology evidence is accurate and does not widen recorded private data.
- Existing overlap, dirty-owner, private-worktree exemption, primary-main, and backlog protections still pass.
- The implementation does not mutate primary main in the linked-private no-peer path.
- Focused claim-engine and command-transport tests, the applicable full shared-infrastructure regression, git diff --check, and fresh independent review pass.

## Dependencies

None.

## Verification

- Run focused claim-engine and command-transport tests for primary, claim-created isolated, and existing linked private checkouts across no-peer and active-peer paths.
- Assert the relevant journal event fields and stable structured results.
- Exercise real-Git scenarios that confirm no primary mutation.
- Run the full applicable shared-infrastructure regression and git diff --check.
- Obtain fresh independent review of the implementation and verification evidence.

## Open Questions

- Should physical checkout classification use a new bounded field, or should worktree_id be corrected while legacy mode semantics remain unchanged?

## Notes

Any governed-definition changes discovered during delivery require an exact canonical-path approval record before mutation. This work item does not authorize a user-scope installation, runtime catalog refresh, transport rebinding, or project-artifact implementation before dispatch.
