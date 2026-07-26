# Bind Project-Files Claims to the Primary Worktree

Status: Ready

Type: Defect

Owner: Unowned

Provider: file

Provider Reference: backlog/defect-backlog/bind-project-files-claims-to-primary-worktree.md

Completion: direct-main

## Summary

Make project-files claim acquisition and release safe for direct-main delivery when the claimant uses a linked worktree.

## Context

The canonical root-AGENTS task 019f9fd6-d7c1-7902-bf33-e10883383b7e delivered accepted candidate 71387a2968d3f879e12d599887bc2981e1bb7144 through non-ancestral primary-main integration 1dded7f556cf4270e2a0bff12178382eac17c3c4. Its live project-files claim, integrate-reconcile-root-agents-019f9fd6, was acquired from linked worktree /Users/martinbechard/.codex/worktrees/9188/dev-methodology. The helper permits that acquisition because project_files is excluded from the primary-worktree scope check, but release validates the claimant worktree HEAD and cannot observe the primary-main integration. The release was rejected as missing_commit_or_no_change.

## Source Evidence

The Parent Coordinator explicitly directed durable Ready logging of this distinct confirmed defect after reviewing the accepted candidate, integration, claim registry, rejected-release event 0abe6b25-19f3-4635-bb38-15769a7861ec, and helper behavior. The defect is separate from the root-AGENTS correction and requires no runtime task at creation.

## Requirements

- Require Event-2 project-files claims to bind to the primary worktree, or return a clear primary-required outcome when requested from a linked worktree.
- Align release validation with that binding so an accepted non-ancestral primary-main integration can be observed safely.
- Preserve the existing claim-event contract and unrelated claim scopes.
- Add a focused public-command regression covering linked acquisition and non-ancestral primary-main integration.

## Acceptance Criteria

- A linked-worktree project-files acquisition either binds safely to primary-main delivery or returns a clear primary-required outcome.
- Release validation recognizes the supported binding and does not falsely require the linked worktree HEAD to contain a non-ancestral primary-main integration.
- The focused public-command regression passes and proves the linked-acquisition and non-ancestral-integration behavior.
- Existing event-contract coverage remains valid.

## Dependencies

None.

## Verification

- Run the focused public-command regression for linked project-files acquisition and non-ancestral primary-main integration.
- Run directly affected helper and event-contract tests.
- Obtain independent review of the claim lifecycle change.

## Open Questions

None.

## Notes

This item is authorized runnable work. It must not use the existing live claim or alter the preserved root-AGENTS delivery evidence except through a separately authorized recovery transaction.
