# Enforce Reference-Plus-Delta Dispatch Packets

Status: Running

Type: Defect

Provider: file

Work Item ID: enforce-reference-plus-delta-dispatch-packets

Completion: main-branch

## Summary

Make every Backlog Dispatcher launch prompt a strict reference-plus-delta packet.

## Source Evidence

On 2026-08-12, the user required this correction before any further recovery dispatch: start one Dev Orchestrator subagent, identify the authoritative provider record, and include only dispatch-time facts absent from that record.

## Requirements

- Update `.agents/skills/backlog-dispatcher/SKILL.md` concisely.
- Define a dispatch prompt as one execution action, the authoritative provider locator, and dispatch-time delta only.
- Require stable assignment facts missing from the provider record to be persisted there before launch.
- Prohibit repeating provider requirements, scope, acceptance criteria, or verification expectations.
- Prohibit restating lifecycle, claim, review, verification, delivery, cleanup, or recovery procedures owned by selected skills.
- Require launch as one Dev Orchestrator subagent, not a generic task or a prompt that reconstructs root awareness.
- Add only focused tests that directly enforce this packet boundary.

## Acceptance Criteria

- Focused tests accept a minimal provider-reference-plus-delta packet.
- Focused tests reject copied work-item content, copied selected-skill procedures, generic-task launch wording, and stable facts omitted from the provider record.
- Fresh independent skill review and verification accept the concise source and tests.

## Dependencies

None.

## Verification

- Validate the private skill through the configured supported project-root route.
- Run directly focused dispatcher and bundle-content tests.
- Prove any generated documentation delta is owned by `document-external-terminal-cleanup`.
- Run Git diff whitespace validation.

## Governed Definition Approval

### Governed Canonical Sources

- `.agents/skills/backlog-dispatcher/SKILL.md`

### Allowed Dependent Artifacts

- Focused test files proven to validate this exact dispatch-packet contract.

### Approval Resolution

Approved at creation by the user's explicit 2026-08-12 instruction to incorporate this rule immediately into the private Backlog Dispatcher skill. Documentation, conceptual roles, adapters, and generated projections remain assigned to `document-external-terminal-cleanup`.

## Crisis Recovery Evidence

- Crisis Epoch: `blocked-queue-reference-plus-delta-2026-08-12T23:15:41Z`.
- Trigger: Nine active file-provider work items are Blocked, exceeding the automatic threshold of five.
- Initial Crisis Set: `generate-inspect-ai-evaluation-catalog`, `integrate-inspect-ai-reporting-evidence`, `prove-inspect-ai-exceptional-runtime-parity`, `prove-read-only-inspect-ai-execution`, `prove-inspect-ai-mutation-lifecycle-parity`, `prove-inspect-ai-multi-agent-identity`, `migrate-evaluation-suites-to-inspect-ai`, `align-wiki-skills-and-project-context-with-documentation-design-system`, and `align-skills-modularization-with-documentation-design-system`.
- Recovery-Policy Addition: This item joins the crisis set because its completion is required before any later recovery dispatch can use the corrected launch contract.
- Exclusions: Ready, User Action Required, Completed, archived, series-index, and Future Ideas records are outside the initial Blocked set. The live traceability work is separate active mutation and is not a crisis item.
- Entry Ordering: Freeze new launches; enter SOLO; preserve the live traceability mutator and its untracked `skills/traceability-discipline` bytes; after its claim is released or a truthful preserved handoff is confirmed, perform the one crisis reset while retaining audit history; then dispatch this item first without claims.
- Current Gate: No crisis work-item task may launch and no reset may occur while the traceability mutator remains live and unpreserved.

## Crisis Entry Result

- SOLO Result: `DISABLED`; parallel dispatch is disabled and exactly one separate crisis work-item task is permitted.
- Preserved Mutator: Traceability owner `019ff841-723a-7b80-a3bc-11c4ee9158d5` and parent `019ff5f0-6b8c-7f92-9f32-14caeeefb442` are idle; their tracked and untracked primary-worktree bytes remain preserved at baseline `3a59744810c0522468765093e16881d5bf8ffa0d` without commit, validation, generation, revert, move, deletion, or discard.
- Release Evidence: Project-files claim `revise-traceability-templates` released disposition-free with schema-version-2 outcome `RELEASED`, event `12f06bc7-afff-4c2f-8a8a-1e385563114f`. The earlier disposition-bearing attempt was rejected without mutation as event `8f171bfd-619e-4177-bd1d-c27181a78cb0`.
- Reset Evidence: Exactly one configured MCP reset returned exit code `0`, schema version `2`, outcome `RESET`, registry `.agent-ops/resource-claim/agent-claims.json`, claims `[]`, and event `2e098ae4-b48a-415d-ab4f-3b71e8eed195` in the retained hot journal.
- Claim Suspension: No claim operation is permitted until crisis exit.

## Starting Handoff Evidence

- Reserved At: 2026-08-12T23:19:00Z.
- Parent Runtime Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Coordinator Execution: `/root/backlog_coordinator`.
- Intended Root Role: Dev Orchestrator.
- Baseline: `3a59744810c0522468765093e16881d5bf8ffa0d` on primary `main`, with the separately preserved traceability working-tree bytes listed in Crisis Entry Result.
- Dispatch Reservation: Exactly one new canonical root execution; runtime identity pending caller-owned creation.
- Launch State: Authorized under serialized crisis recovery; successful creation does not imply Running.
- Claim State: Suspended for the crisis epoch; this execution performs no claim operation.
- Next Reconciliation: Reconcile the exact create result immediately; the root execution records Starting -> Running before mutation.

## Running Acceptance Evidence

- Accepted At: 2026-08-12T23:28:20Z.
- Canonical Execution: `/root/enforce_reference_plus_delta`.
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Authorizing Coordinator: `/root/backlog_coordinator`.
- Root Owner: Dev Orchestrator.
- Branch: `main`.
- Worktree: `/Users/martinbechard/dev/dev-methodology`.
- Accepted Baseline: `868dbe34a947efa88cb0ad11c7fd07ac8432f0a6`.
- Accepted Execution: The sole authorized crisis execution accepted the complete provider record and dispatch-time delta on host `local`.
- Runtime Display Handoff: `NOT_APPLICABLE`; this collaboration runtime exposes no separate Codex Task ID, Conversation ID, host, or title-control surface.
- Phase: Implementation planning.
- Claim State: Suspended; no claim operation is permitted or performed.

## Notes

- The completed `prefer-durable-recovery-evidence-over-codex-task-identity` task remains terminal and must not be resumed or reopened.
- Do not combine this immediate private-skill correction with `document-external-terminal-cleanup`.
