# Use Exact Work-Item Claims For Lifecycle Updates

Status: Starting

Type: Feature

Owner: Dev Orchestrator

## Supplemental Resumption Reservation

- Parent Coordinator Task: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Canonical Task/Thread: 019f9783-31a0-7e91-9704-08cde7886b3a
- Reservation: One parent-owned same-task resumption launch reservation; no replacement task is created.
- Normalized Objective: Use exact work-item claims for lifecycle updates.
- Dispatched At: 2026-07-25T16:04:09Z
- Intended Root Role: Dev Orchestrator
- Canonical Worktree: /Users/martinbechard/.codex/worktrees/8b42/dev-methodology
- Preserved Approval: Original eight governed paths plus only skills/agent-claim-command/SKILL.md and skills/agent-claim-mcp/SKILL.md; no other governed scope.
- Phase: Awaiting root lifecycle acceptance.

## Supplemental Resumption Coordination Evidence

- Backlog Claim: reserve-exact-work-item-claims-supplemental-019f9783 acquired on primary main at 2026-07-25T16:04:09.645990Z; acquisition journal event 096f6363-1325-41d8-a432-ebef900a1bb3.

## Resumption Launch Reservation

- Parent Coordinator Task: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Canonical Task/Thread: 019f9783-31a0-7e91-9704-08cde7886b3a
- Reservation: One parent-owned same-task resumption launch reservation; no replacement task is created.
- Normalized Objective: Use exact work-item claims for lifecycle updates.
- Dispatched At: 2026-07-25T12:30:21Z
- Intended Root Role: Dev Orchestrator
- Preserved Evidence: The exact eight-path approval, existing canonical worktree and branch, and prior lifecycle evidence remain binding.
- Phase: Accepted; lifecycle now Running.

## Resumption Coordination Evidence

- Backlog Claim: resume-exact-work-item-claims-019f9783 acquired on primary main at 2026-07-25T12:30:21.892742Z; acquisition journal event fff40958-7f3a-419f-8ef5-24b695e68d3d.

## Resumption Running Acceptance

- Root Dev Orchestrator: Dev Orchestrator
- Canonical Task/Thread: 019f9783-31a0-7e91-9704-08cde7886b3a
- Delivery Branch: Detached HEAD at bc30647a6de2f1593a1f5a746410c9d6761e2ba5
- Delivery Worktree: /Users/martinbechard/.codex/worktrees/8b42/dev-methodology
- Starting Baseline: c1b20bd399522479ae53bc3f6d81d0c762e33d33
- Started At: 2026-07-25T12:31:30Z
- Phase: approved implementation preparation
- Backlog Claim: 019f9783-resumption-running-steward
- Claim Acquisition Event: 6db6306c-a5f1-4ead-b6d2-ac8dc190636d

## Correction Authority Required

- Question: "Do you approve mutation of exactly skills/agent-claim-command/SKILL.md to align the distributed command adapter with the already-approved runtime rule that a broad backlog claim requires a documented scope reason?"
- Additional Governed Approval Scope: skills/agent-claim-command/SKILL.md only; no other approval expansion.
- Why Approval Is Required: Candidate command runtime now rejects unjustified broad --backlog without --scope-reason, but the governed command adapter still says only tree/project-files/all-files require the reason, so callers receive a documented-invalid command.
- Candidate: 0f3dcab5d539ea1aca197e1fc28fab574e2746b4; clean and claim released.
- Canonical Task/Thread: 019f9783-31a0-7e91-9704-08cde7886b3a
- Delivery Branch: Detached HEAD at bc30647a6de2f1593a1f5a746410c9d6761e2ba5
- Delivery Worktree: /Users/martinbechard/.codex/worktrees/8b42/dev-methodology
- Recorded At: 2026-07-25T13:13:50Z
- Backlog Claim: 019f9783-command-adapter-approval-steward
- Claim Acquisition Event: 5e41129d-f6a1-4078-ae3d-1644edc5b14e
- Unattended Boundary: Preserve candidate and do not mutate the new governed path, approval record, correction artifacts, generated outputs, or dependent docs/tests until the user answers and this same canonical Thread resumes through UAR -> Ready -> Starting -> Running.

### Fresh Independent Review Findings

1. High: command-adapter manifest omission requires the additional approval above.
2. Medium: approved-scope correction for every nonterminal path move to claim exact source plus destination.
3. Medium: approved-scope correction for stale release/ancestry guidance and test.
4. Medium: non-governed regeneration of stale design/agent-and-skill-evaluations.html.
5. Add focused cases for simultaneous different-item processes, broad-versus-exact contention, and baseline_not_ancestor.

## Supplemental Correction Authority Required

- Accepted Candidate: 0f3dcab5d539ea1aca197e1fc28fab574e2746b4
- Candidate Branch: codex/exact-work-item-claims-019f9783; clean.
- Candidate Claim Release Event: 4f2e543a-91e7-4798-b1aa-b9a817fa1d0b
- Source Review Verdict: FAIL.
- Methodology Review Verdict: FAIL.
- Supplemental Question: "Do you approve mutation of exactly skills/agent-claim-command/SKILL.md and skills/agent-claim-mcp/SKILL.md to align both transport contracts with the approved exact-work-item claim policy and the enforced documented-reason requirement for broad backlog scope?"
- Supplemental Governed Approval Scope: Exactly skills/agent-claim-command/SKILL.md and skills/agent-claim-mcp/SKILL.md; no adapter openai.yaml scope is needed if descriptions remain unchanged.
- Prior Prompt Reconciliation: This two-path supplemental question replaces the earlier command-only approval question; all prior lifecycle and eight-path approval evidence remains preserved.
- Next Action Owner at Prompt: User
- Recorded At: 2026-07-25T13:14:40Z
- Backlog Claim: 019f9783-supplemental-approval-steward
- Claim Acquisition Event: 49cfb40c-dc85-4b38-a201-a8fc28f77aa9
- Unattended Boundary: Do not mutate a governed source, approval record, generated mirror, evaluation or documentation artifact, or engine correction until the user answers and this same Thread resumes through UAR -> Ready -> Starting -> Running.

### Source Review Findings Within Existing Approved Non-Governed Engine And Test Scope

1. An exact backlog claim can add prohibited git-index:primary through a resource-only extension.
2. Exact-path extension lacks dirty/recovery and per-path baseline evidence, allowing peer history or interrupted bytes to be misattributed.
3. --no-change can succeed with nonempty committed_scope_paths.

These findings require coder correction after resumption and require no new definition approval.

### Methodology Review Findings

- Executable broad --backlog now requires a documented scope reason, while skills/agent-claim-command/SKILL.md and skills/agent-claim-mcp/SKILL.md retain stale argument and parity contracts.
- Evaluation sources and generated evaluation documentation still reward broad per-item backlog claims.

### Anticipated Non-Governed Dependent Corrections, Not Approval Scope

- AGENTS.md selected inlined command block through supported render
- evals/agent-scenarios.yaml
- evals/skill-probes.yaml
- evals/agent-tests/dev-backlog-steward/skills/dev-backlog-steward-suite-contract/SKILL.md
- evals/agent-tests/dev-backlog-steward/scenarios.yaml
- design/agent-and-skill-evaluations.html through its generator
- Relevant test modules
- The three engine corrections in skills/agent-claim-command/scripts/claim.py and its tests

### Supported Generated Mirrors, Not Supplemental Approval Scope

- design/generated/skill-definitions.js
- generated/adapters/** only where supported by the approved supplemental source categories

## Supplemental Approval Resolution

- User Answer: "I approve"
- Approval Scope: Exactly skills/agent-claim-command/SKILL.md and skills/agent-claim-mcp/SKILL.md; no scope expansion.
- Original Approval: The original eight-path governed approval remains preserved and unchanged.
- Canonical Task/Thread: 019f9783-31a0-7e91-9704-08cde7886b3a
- Phase: Awaiting parent Coordinator Ready -> Starting reservation for this same canonical task.
- Next Action Owner: Parent Coordinator
- Recorded At: 2026-07-25T16:02:50Z
- Backlog Claim: 019f9783-supplemental-ready-steward
- Claim Acquisition Event: 09c38d5d-34ce-404e-ab93-7674dc6f4449
- Unattended Boundary: Do not mutate governed sources, approval records, generated mirrors, evaluation or documentation artifacts, or engine corrections until this same Thread resumes through Ready -> Starting -> Running.

## Launch Reservation

- Parent Coordinator Task: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Canonical Task/Thread: 019f9783-31a0-7e91-9704-08cde7886b3a
- Reservation: One parent-owned launch reservation under the current backlog-wide claim contract.
- Intended Root Role: Dev Orchestrator
- Isolated Checkout: /Users/martinbechard/.codex/worktrees/8b42/dev-methodology
- Phase: Accepted; lifecycle now Running.
- Dispatched At: 2026-07-25T04:24:30Z

## Running Acceptance

- Root Dev Orchestrator: Dev Orchestrator
- Canonical Task/Thread: 019f9783-31a0-7e91-9704-08cde7886b3a
- Delivery Branch: Detached HEAD at bc30647a6de2f1593a1f5a746410c9d6761e2ba5
- Delivery Worktree: /Users/martinbechard/.codex/worktrees/8b42/dev-methodology
- Started At: 2026-07-25T04:26:18Z
- Phase: Running; bounded discovery and approval preparation.
- Backlog Claim: 019f9783-starting-running-steward
- Claim Acquisition Event: 7ef99fde-27a2-4057-afc6-54b989bc20a7

## User Action Required

- Question: "Do you approve mutation of exactly the eight governed canonical definition paths listed below to implement exact work-item claims for file-backed creation, lifecycle, recovery, completion, coordination, and claim semantics?"
- Why Approval Is Required: Repository policy requires an exact scope-specific user answer before any governed canonical definition may be changed.
- Unattended Boundary: Do not mutate any governed source, approval record, generated mirror, or dependent artifact until the user answers and this same canonical Thread resumes through User Action Required -> Ready -> Starting -> Running.
- Next Action Owner at Prompt: User
- Resumption Thread: 019f9783-31a0-7e91-9704-08cde7886b3a
- Recorded At: 2026-07-25T04:31:02Z
- Backlog Claim: 019f9783-user-action-required-steward
- Claim Acquisition Event: f4fc2367-cd1d-421d-931a-ad0535fda68f

## Ready Resumption

- User Answer: "I approve"
- Answer Received: 2026-07-25
- Approval Thread: 019f9783-31a0-7e91-9704-08cde7886b3a
- Approved Scope: Exactly the eight governed canonical definition paths listed below; no scope expansion.
- Phase: Awaiting parent Coordinator Ready -> Starting reservation for this same canonical task.
- Next Action Owner: Parent Coordinator
- Unattended Boundary: Do not mutate governed sources, approval records, generated mirrors, or dependent artifacts until this same canonical Thread is resumed through Ready -> Starting -> Running.

### Governed Canonical Definition Approval Scope

1. skills/agent-claim/SKILL.md
2. skills/codex-workitem-coordination/SKILL.md
3. skills/create-file-work-item/SKILL.md
4. skills/create-file-work-item/agents/openai.yaml
5. skills/manage-file-work-items/SKILL.md
6. skills/manage-file-work-items/agents/openai.yaml
7. agents/roles/dev-activities/dev-backlog-coordinator.role.yaml
8. agents/roles/dev-activities/dev-backlog-steward.role.yaml

### Supported Generated Mirrors, Not Approval Scope

- design/generated/skill-definitions.js
- design/generated/role-definitions.js
- generated/adapters/** only where supported by the approved source categories

### Anticipated Non-Governed Companion Scope, Not Approval Scope

- skills/agent-claim-command/scripts/claim.py
- scripts/test_agent_claim.py
- scripts/test_bundle_content.py
- scripts/test_codex_workitem_coordination.py
- Applicable evaluation fixtures
- README.md
- AGENTS.md only through a supported project-guidance render if required
- design/orchestrated-development-lifecycle.html
- design/work-item-provider-and-completion-contracts.md

### Overlap Reconciliation Evidence

- Canonical durable-defect task 019f96cf-226c-7f62-9d66-7d31cead822e accepted supersession of claim-free creation.
- It stopped before governed, generated, test, or documentation mutation and will not integrate preserved commits 4f47fea91dc6f49b4f36d5c1360bf414fce2d852 and 957c93370c476bb3296151f979b5f1407362e7be.
- agents/roles/dev-activities/dev-orchestrator.role.yaml is excluded from this approval manifest.

## Summary

Make one active work-item file the unit of lifecycle ownership. Starting, Running, milestone, recovery, and terminal updates must claim only the exact work-item paths they mutate instead of claiming the complete backlog. Regenerate every supported dependent definition and publish the verified result to the configured user-level agent and skill destinations.

## Context

The current file-provider and coordination guidance still presents a broad backlog-domain claim as the normal mechanism for a single work-item transaction. That unnecessarily prevents unrelated work-item threads from updating different files.

The intended steady state is:

- One active work item has one lifecycle-writing thread.
- The parent coordinator and watchdog observe a Running item read-only.
- A lifecycle mutation claims the exact active work-item file.
- Terminal completion claims the exact active source and completed destination.
- Recovery claims the exact active item only after the prior thread is confirmed stopped and its ownership is reconciled.
- A broad backlog claim is reserved for a genuine backlog-wide migration or batch operation whose affected files cannot be enumerated safely.

This direction supersedes the no-claim creation proposal recorded in require-durable-defect-logging-and-direct-main-creation.md. Work-item creation and lifecycle mutation retain exact-file coordination rather than becoming claim-free.

Source Evidence: User direction in Codex thread 019f77f4-c4bd-7c91-b197-c987a7beb838: “While a task is running nobody else is accessing the work item so you don't have to block the entire backlog just to update it. So I think just getting a claim on the workitem is good enough.” The user then explicitly requested this implementation work item and required regeneration and publication of affected files.

## Requirements

- Define the active work-item file as the exclusive lifecycle-writing boundary for its assigned thread.
- Require Ready -> Starting to claim only the selected active work-item file.
- Require Starting -> Running and later non-terminal milestone updates to claim only that same active work-item file.
- Require terminal completion or archival to claim exactly the active source path and completed destination path.
- Require recovery or disposition of an interrupted item to claim only that item after confirming the prior thread has stopped, reconciling any live exact-file ownership, and preserving recoverable Git evidence.
- Keep the coordinator and watchdog read-only for a Running item unless they explicitly enter its recovery or disposition procedure.
- Prohibit the broad backlog selector for an individual creation, lifecycle, recovery, or completion transaction.
- Permit the broad backlog selector only for a documented operation that truly owns the backlog as a whole and cannot safely enumerate its paths.
- Preserve safe Git behavior when independent threads update different work-item files. Do not reintroduce queue-wide exclusion through a differently named primary-checkout or integration resource.
- Reconcile require-durable-defect-logging-and-direct-main-creation.md so its no-claim creation proposal does not conflict with the exact-file rule.
- Discover and record the smallest exact governed canonical definition manifest before mutation. Obtain scope-specific user approval and pass every required pre-mutation definition check before changing those sources.
- Regenerate only the supported mirrors and documentation outputs owned by approved canonical sources. Never hand-edit generated definition files.
- Update the human-facing lifecycle HTML so the work-item ownership and exact-file transaction boundaries are understandable without implementation terminology.
- Publish the verified affected skills and generated agent definitions to the configured user-level destinations using the repository installer. Refresh the installed catalog and verify that installed bytes and ownership manifests match the integrated source.

## Acceptance Criteria

- Two independent threads can acquire non-overlapping exact-file ownership for two different work items without either claiming or blocking the complete backlog.
- A second writer for the same work-item file receives the configured conflict outcome and cannot mutate it.
- Starting, Running, milestone, recovery, completion, and archive examples use exact paths; no individual-item example uses the broad backlog selector.
- Completion atomically protects the active source and completed destination without claiming unrelated backlog paths.
- Recovery tests prove that a stopped thread can be reconciled safely without granting concurrent access or discarding its preserved commit.
- Disposable-repository tests cover concurrent different-item updates, same-item contention, source-to-completed movement, interrupted recovery, and rejection of unjustified broad backlog ownership.
- The existing defect-logging/direct-main-creation item and resulting guidance no longer prescribe claim-free work-item creation.
- Applicable focused tests and claim-engine regressions pass, including command-transport behavior and journal/report scope evidence.
- Supported generated mirrors, lifecycle HTML, README or operator guidance, and focused bundle assertions are current.
- An independent methodology review and focused verifier accept the exact source/generated/documentation diff.
- Post-integration verification passes on current main.
- The affected bundle is deployed to the configured user-level skill and agent destinations, the installed catalog is refreshed, and byte or digest checks confirm the installed definitions match the integrated source.

## Dependencies

None.

## Verification

- Run the exact governed-definition approval checks for the discovered canonical source manifest before mutation.
- Run focused file-provider, coordination, claim-engine, command-transport, and disposable-Git contract tests.
- Run only the generator freshness checks supported by the approved canonical source categories.
- Verify design/orchestrated-development-lifecycle.html with the documentation page verifier and an independent readability review.
- Run git diff --check.
- Integrate from fresh current main under exact project-path and integration-resource ownership.
- Deploy with scripts/install-skills.py to the configured user-level runtime destinations, refresh the installed skill catalog, and compare installed ownership-manifest digests with the integrated bundle.

## Notes

- This item changes the scope of coordination, not the requirement to coordinate.
- A worktree is an execution checkout, not a backlog lock.
- A Git commit boundary must not be modeled as ownership of every backlog file.
- Exact governed definition paths remain to be discovered and approved; this Ready item is authority to begin bounded discovery, not authority to mutate an unspecified governed definition.
