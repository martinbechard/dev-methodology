# Claim Work Items By ID And Record Lifecycle Events

Status: Running

Type: Feature

Provider: file

Work Item ID: claim-work-items-by-id-and-record-lifecycle-events

Completion: direct-main

## Current Dispatch Reservation

Transition: Ready -> Starting.
Parent Coordination Thread: /root/apply_skill_group_design_backlog.
Launch Reservation: One distinct bounded launch reservation for this provider record.
Normalized Objective: Add provider-independent exclusive claims keyed by opaque Work Item ID, with structured acquisition, release, and report evidence across command and MCP transports.
Dispatch Time: 2026-08-05T22:38:02Z.
Intended Root Dev Orchestrator Role: Dev Orchestrator.
Effective Commit Selector: complete-work-item-direct-main.
Canonical Runtime Evidence: None at reservation time. The parent Coordinator must reconcile this reservation before creating one canonical work-item Thread.
Current Launch Evidence: Parent Coordinator authorized this exact reservation; exact-file backlog claim reserve-work-item-id-claims-019fb4 acquired with outcome SHARED_CHECKOUT_ACQUIRED and event 342aa843-fc38-466a-b418-a23e1f026391.
Required Next Lifecycle Transition: The canonical root Dev Orchestrator must separately accept Starting -> Running before repository mutation.

## Current Running Acceptance

Transition: Starting -> Running.
Owner: root Dev Orchestrator /root.
Canonical Thread: 019fd414-a82c-75e3-b8e3-988fb862b7ed.
Parent Coordination Thread: /root/apply_skill_group_design_backlog.
Root Agent Task: /root.
Branch: codex/claim-work-items-by-id-and-record-lifecycle-events.
Worktree: /Users/martinbechard/.codex/worktrees/1de0/dev-methodology.
Phase: implementation startup.
Started At: 2026-08-05T22:41:43Z.
Exact Claim Acquisition Evidence: claim record-running-claim-work-items-019fd414 acquired with outcome SHARED_CHECKOUT_ACQUIRED; acquisition event fcc3aa93-33d8-4ac4-9a04-7143ab4dbc67; incarnation 8993a895-857a-4646-8858-e40546f13425.

## Summary

Add a provider-independent claim scope keyed by the opaque Work Item ID. Require coordinators and work-item providers to use that claim while working on or updating an item, and record structured acquire and release metadata so reports can reconstruct active, completed, blocked, and handed-off intervals from command or MCP claim calls.

## Context

The existing claim engine protects repository paths and named shared resources. A file path can identify the current location of a file-provider record, but it cannot provide one stable identity across lifecycle moves, and it cannot identify GitHub, GitLab, Azure DevOps, or Jira items uniformly. The current report therefore infers work-item boundaries from prose, commits, and provider mutations.

Work Item IDs are already opaque, provider-owned, and stable across lifecycle states. A dedicated exact-ID claim can supply an observable execution boundary without treating a provider path, task title, or conversation name as identity.

Claim cleanup must remain separate from provider lifecycle authority. Releasing a work-item claim records the end and disposition of one claimed activity interval; it does not by itself prove that delivery was accepted or that the provider record is terminally complete.

## Source Evidence

On 2026-08-05, in the current Codex conversation analyzing the Dev Methodology dispatcher timeline, the user requested: "let's create an enhancement to have a special claim to acquire exclusivity on a work item, by workitem id rather than file path" and directed that the claim contain enough information to determine when the item started, finished, or became blocked. The user also requested guidance requiring acquisition while updating or working on an item, release when that activity ends, and use of MCP tool calls as the observable event source.

## Requirements

- Add one exact, provider-independent work-item scope identified by an opaque `work_item_id`; two live claims for the same ID must conflict even when their provider paths, repositories, branches, worktrees, tasks, or agents differ.
- Keep work-item identity separate from file, tree, broad-domain, and runtime-resource scopes. A work-item claim must not imply ownership of provider files, source files, Git state, a branch, a worktree, or an external provider mutation capability.
- Record a bounded activity on acquisition. The public contract must distinguish at least `work` from `update` so reporting does not confuse delivery execution with a short provider-lifecycle mutation.
- Record a bounded disposition on release. The public contract must distinguish at least `done`, `blocked`, and `handoff`; `done` means the claimed activity interval ended successfully and does not independently prove provider lifecycle completion.
- Preserve the Work Item ID, activity, disposition, claim and incarnation identifiers, owner agent, root task identifier, timestamps, and MCP or command outcome in the live registry where applicable and in every relevant claim journal event.
- Permit a bounded opaque blocker reference for a `blocked` release without storing prompts, reasoning, arbitrary tool output, personal information, company-sensitive information, or an unrestricted blocker narrative in the claim journal.
- Require a work-item claim before beginning work on an item and before mutating its provider record. Release it immediately when the claimed work or update ends, becomes blocked, or is handed off.
- Preserve strict exclusivity during role changes. The current holder must release with `handoff` before another agent acquires the same Work Item ID; do not create overlapping parent-child exceptions that make the event timeline ambiguous.
- Keep path and resource claims independently applicable. An agent that edits a file-backed provider record or uses an exclusive runtime may need the work-item claim plus the existing path or resource claim required by the applicable event contract.
- Extend both command and MCP claim contracts with equivalent acquire and release inputs, structured validation failures, conflict evidence, status output, and journal evidence.
- Make claim reporting group events by Work Item ID and expose reconstructable activity segments with acquisition time, release time, activity, disposition, owner, duration, live/open state, and incomplete or contradictory-event diagnostics.
- Treat the claim journal timestamps as observed operational boundaries. Provider records remain authoritative for lifecycle status, dependencies, delivery evidence, and terminal completion.
- Preserve backward compatibility for historical claims and events that lack work-item fields; report them as non-work-item claims rather than inventing an ID or disposition.
- Update generated documentation and supported adapters from their canonical sources rather than editing generated files directly.

## Acceptance Criteria

- Acquiring `work_item_id=A` succeeds when no live claim owns A, and a simultaneous request for A returns `CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED` with exact work-item overlap evidence.
- Claims for distinct Work Item IDs can coexist regardless of matching filenames or provider types.
- A successful acquisition event contains the exact Work Item ID and `work` or `update` activity; the matching release event contains the same identity and `done`, `blocked`, or `handoff` disposition.
- A `blocked` release records its timestamp and optional bounded blocker reference, removes only the exact live claim, and remains explicitly separate from any provider transition to Blocked.
- Invalid or missing activity, disposition, Work Item ID, or blocker metadata produces a structured rejection and does not mutate the registry.
- Status output exposes every live work-item claim without conflating it with file or runtime-resource ownership.
- The claim report reconstructs deterministic per-item segments and identifies live claims, missing releases, releases without acquisitions, and historical events without work-item metadata.
- Command and MCP transport fixtures demonstrate equivalent acquire, conflict, status, blocked-release, done-release, handoff, and report behavior.
- Work-item coordination and every management-provider skill require the exact-ID claim at the start of work or provider mutation and require a disposition-bearing release at the corresponding boundary.
- Focused claim-engine, transport, work-item contract, generated-document freshness, skill validation, and repository diff checks pass.

## Dependencies

None.

## Verification

- Add focused command-engine tests to `scripts/test_agent_claim.py` for validation, exact-ID contention, coexistence, registry representation, acquire/release journal fields, blocked and handoff dispositions, historical compatibility, and per-item reporting.
- Add command/MCP parity fixtures to `scripts/test_agent_claim_transport.py`, including visible `claim_acquire` and `claim_release` inputs sufficient for timeline reconstruction.
- Add skill-contract coverage to `scripts/test_bundle_content.py` for acquisition and release guidance across coordination and all configured management providers.
- Run the repository skill validator on every changed skill package.
- Regenerate skill documentation and supported adapters, then run their freshness checks.
- Run `git diff --check` and the focused claim, transport, bundle-contract, and reporting suites.

## Open Questions

- Identify the source and release workflow for the configured `mcp-agent-ops` implementation if it is maintained outside this repository; preserve command/MCP contract parity rather than documenting unsupported fields.
- Decide whether the existing claim report should gain a versioned `work_items` section or whether a separate work-item timeline report is the smaller compatible public surface.

## Governed Definition Approval

### Governed Canonical Sources

- skills/agent-claim/SKILL.md
- skills/agent-claim-command/SKILL.md
- skills/agent-claim-mcp/SKILL.md
- skills/coordinate-codex-work-items/SKILL.md
- skills/manage-file-work-items/SKILL.md
- skills/manage-github-work-items/SKILL.md
- skills/manage-gitlab-work-items/SKILL.md
- skills/manage-azure-devops-work-items/SKILL.md
- skills/manage-jira-work-items/SKILL.md

### Allowed Dependent Artifacts

- skills/agent-claim-command/scripts/claim.py
- scripts/test_agent_claim.py
- scripts/test_agent_claim_transport.py
- scripts/test_bundle_content.py
- design/work-item-provider-and-completion-contracts.md
- design/generated/skill-definitions.js
- generated/adapters/**, only where the repository generator maps an approved canonical skill source to that mirror
- Evaluation catalog or fixture files that directly verify the approved claim and work-item guidance

### Approval Resolution

Approved at creation. The user explicitly requested the exact-ID work-item claim, its acquire/release guidance, blocked and done observability, and MCP-call evidence in the current Codex conversation on 2026-08-05. The governed manifest above is the smallest provider-independent skill-definition scope identified from the live repository. This approval does not authorize conceptual agent-definition changes or unrelated claim, provider, coordination, or reporting behavior.

## Notes

- Creation claim: `create-work-item-claim-events-20260805`; acquisition event `528b90aa-fd6f-47a5-ad5c-5a6c6ab4f8a1` on primary `main`.
- Example work interval: acquire Work Item ID A with activity `work`; release A with disposition `done`.
- Example blocked interval: acquire A with activity `work`; release A with disposition `blocked` and an opaque blocker reference; separately transition the authoritative provider record to Blocked when that provider operation is authorized.
- Example lifecycle update: acquire A with activity `update`; mutate and verify the provider record while holding any separately required provider-path claim; release A with disposition `done`.
- Example handoff: the execution owner releases A with disposition `handoff`; only then may the next owner acquire A for `work` or `update`.
