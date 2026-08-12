# Prefer Durable Recovery Evidence Over Codex Task Identity

Status: Running

Owner: Root Dev Orchestrator task 019ff81d-50ec-7d21-9206-e2a9a7ae4c4d

Type: Feature

Provider: file

Work Item ID: prefer-durable-recovery-evidence-over-codex-task-identity

Completion: main-branch

## Summary

Concisely define Codex task identity as replaceable runtime metadata when an execution is demonstrably unusable and durable recovery evidence remains complete.

## Context

The lifecycle-alignment recovery preserved its provider record, accepted candidate, branch, clean worktree, reviews, final-verifier PASS, and delivery state. Its old Codex task could not access a Git workspace or the configured MCP claim surface, and the only identity-preserving handoff failed. Treating that runtime identity as irreplaceable would strand otherwise accepted work.

The current contract correctly prohibits replacement merely because a task is idle or slow. It needs an equally explicit bounded recovery rule for a demonstrably unusable task.

## Source Evidence

On 2026-08-12, the user clarified that old Codex task identity does not matter when work is durably preserved in provider, branch, worktree, candidate, and verification evidence. The user then explicitly required a guidance update: task identity is replaceable runtime metadata when demonstrably unusable; durable work and delivery evidence are authoritative; Coordinator may authorize exactly one successor with a durable old-to-new identity handoff and duplicate prevention; and the idle-or-slow prohibition must remain.

## Requirements

- Update `skills/coordinate-codex-tasks/SKILL.md` and `.agents/skills/backlog-dispatcher/SKILL.md` concisely.
- Define the evidence threshold for a demonstrably unusable Codex task, including failed required capability and exhausted identity-preserving recovery.
- State that provider/work-item content, accepted commit, branch/worktree, claims, reviews, verifier evidence, and delivery state are authoritative recovery evidence.
- Permit Dev Backlog Coordinator to authorize exactly one successor root execution with a durable old-to-new identity handoff and duplicate prevention.
- Require ambiguous creation reconciliation and prohibit a second successor or concurrent mutation.
- Preserve the prohibition on replacement merely because an execution is idle, slow, quiet, or awaiting an ordinary bounded operation.
- Keep provider lifecycle transitions and new successor Starting -> Running acceptance distinct.
- Add only directly focused tests in this immediate item.
- Assign generated documentation, role, adapter, and broader design effects to `document-external-terminal-cleanup` rather than expanding this source correction.

## Acceptance Criteria

- Both canonical skill sources express the same narrow replacement threshold and evidence precedence.
- A demonstrably unusable task can be superseded once without discarding durable work or weakening provider and claim authority.
- Tests reject idle/slow replacement, multiple successors, identity inference, ambiguous-create retry, and mutation before successor Running acceptance.
- Tests accept one Coordinator-authorized successor after failed same-task recovery with a complete durable evidence handoff.
- Fresh independent skill review and verification accept the exact scope and concise wording.

## Dependencies

None.

## Verification

- Validate both skill packages through configured MCP at the supported primary-root phase.
- Run focused Codex task-control, Dispatcher, provider-transition, and bundle-content tests.
- Prove any generated freshness delta is limited to projections owned by `document-external-terminal-cleanup`.
- Run Git diff whitespace validation.
- Obtain fresh independent skill review and verification.

## Open Questions

None.

## Governed Definition Approval

### Governed Canonical Sources

- skills/coordinate-codex-tasks/SKILL.md
- .agents/skills/backlog-dispatcher/SKILL.md

### Allowed Dependent Artifacts

- Focused test files only when repository discovery proves they directly validate one of the two approved sources.

### Approval Resolution

Approved at creation. On 2026-08-12, the user explicitly required the durable-state-over-task-identity guidance update and named the required successor and duplicate-prevention semantics. Documentation, role definitions, adapters, and generated projections remain outside this immediate governed scope.

## Notes

The separate Watchdog-contract work completed and archived at main commit `c73bd4eb9452ef4df99d1b92442cdbfc2f39f6fb`, and its canonical runtime execution was archived. Reconcile the current integrated skill text as the implementation baseline; do not replay or revert that delivered work.

## Starting Handoff Evidence

- Reserved At: 2026-08-12T22:21:18Z.
- Parent Runtime Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Coordinator Execution: `/root/backlog_coordinator`.
- Normalized Objective: Concisely update the private Backlog Dispatcher and portable Codex task-coordination skill so one demonstrably unusable task may be superseded through complete durable recovery evidence and duplicate prevention, while preserving the prohibition on replacing idle, slow, or quiet tasks.
- Intended Root Role: Dev Orchestrator.
- Baseline: `c73bd4eb9452ef4df99d1b92442cdbfc2f39f6fb` on primary `main`.
- Dispatch Reservation: Exactly one canonical root execution was created and reconciled without retry.
- Canonical Codex Task: `019ff81d-50ec-7d21-9206-e2a9a7ae4c4d`.
- Canonical Conversation: `019ff81d-50ec-7d21-9206-e2a9a7ae4c4d`.
- Runtime Host And Checkout: host `local`; cwd `/Users/martinbechard/dev/dev-methodology`.
- Launch Evidence: Canonical creation at Unix time `1786574098`; runtime status `active`; no client-thread identity and no retry. Creation does not imply Running.
- Conversation Title: Requested `Starting — Prefer Durable Recovery Evidence Over Codex Task Identity`; the read UI displays a normalized truncated rendering.
- Last Contact: 2026-08-12T22:34:58Z.
- Next Reconciliation: The canonical root execution must record Starting -> Running before mutation.
- Create Reconciliation Claim: `reconcile-durable-recovery-create-019ff81d`; outcome `SHARED_CHECKOUT_ACQUIRED`; event `72778701-ad16-4894-b213-f158cf23073a`.
- Transition Claim: `start-durable-recovery-guidance-019ff2c3`; outcome `SHARED_CHECKOUT_ACQUIRED`; event `10a37cf9-4263-4d6c-9f64-64ab2c120dfe`.

## Running Evidence

Started At: 2026-08-12T22:36:10Z

Canonical Conversation: 019ff81d-50ec-7d21-9206-e2a9a7ae4c4d

Root Agent Task: 019ff81d-50ec-7d21-9206-e2a9a7ae4c4d

Parent Coordination: 019ff2c3-1710-7aa1-89c4-9d6066f51fe4

Branch: main

Worktree: /Users/martinbechard/dev/dev-methodology

Phase: planning and baseline reconciliation

Accepted Execution Evidence: This canonical Root Dev Orchestrator accepted the Starting reservation, resolved reservation commit `29b169be8f9ecf44fb955d4e4b4d5fa74169f4e9`, preserved accepted Watchdog baseline `c73bd4eb9452ef4df99d1b92442cdbfc2f39f6fb`, and acquired exact Work Item ID claim `prefer-durable-recovery-019ff81d-work` with activity `work` before this transition.
