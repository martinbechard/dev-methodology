# Respect Optional Resource Coordination In Workflow Skills

Status: Running

Owner: Dev Orchestrator task `019fe4e7-95c9-7372-bd9f-aa983c5c7237`

Phase: Running — Candidate exact-manifest review

Type: Defect

Provider: file

Work Item ID: respect-optional-resource-coordination-in-workflow-skills

Completion: main-branch

## Summary

Make integration, delivery, and end-to-end verification skills respect the project-selected resource-coordination setting instead of requiring resource-claim unconditionally.

## Context

PROJECT.yaml supports resource_coordination values none and resource-claim. Project Configurator renders the selected policy through AGENTS.md and requires projects selecting none to load no claim skill or claim procedure. The completed selectable-resource-coordination contract also requires ordinary workflow skills to consume the project-selected policy rather than hard-code resource-claim.

Current source contradicts that boundary:

- skills/integrate-agent-work/SKILL.md says to follow the Claim Events table in resource-claim during integration.
- skills/deliver-work-item-feature-branch/SKILL.md says to follow the Claim Events table in resource-claim during publication.
- skills/deliver-work-item-main-branch/SKILL.md says to follow the Claim Events table in resource-claim during integration.
- skills/verify-end-to-end-workflow/SKILL.md says to apply resource-claim when verification triggers a claim event.

Those exact-name instructions can require an unloaded skill when resource_coordination is none. They also make static dependency diagrams appear to give those workflow skills ownership of a project-specific loading decision that belongs to AGENTS.md.

## Source Evidence

During review of design/agents/work-item-dispatching-and-delivery.md on 2026-08-05, the user directed: "Make the links optional if the skill IS NOT ALWAYS loaded. Add the condition when it is loaded. link it to the shape that loads it. If it's a project-specific decision then show it loaded via AGENTS.md." Source comparison against PROJECT.yaml, skills/create-project-configuration/SKILL.md, and the four workflow skills above confirmed the contract mismatch. The user authorized correction of the documentation model but did not authorize mutation of the four governed skill definitions.

## Requirements

- Replace unconditional resource-claim references with vocabulary that consumes the project-selected resource-coordination policy.
- Perform no claim discovery, acquisition, heartbeat, release, or claim-specific evidence handling when resource_coordination is none.
- Preserve the complete resource-claim behavior when AGENTS.md selects resource-claim.
- Keep AGENTS.md responsible for loading the project-selected coordination skill; do not add resource-claim to conceptual Agent skill lists.
- Keep helper transport selection subordinate to resource-claim and separate from workflow skills.
- Update focused evaluations and generated documentation affected by the corrected public instructions.

## Acceptance Criteria

- All four workflow skills operate coherently with resource_coordination none and agent-claim.
- No workflow skill unconditionally loads or requires agent-claim when project configuration selects none.
- Static dependency diagrams point project-selected resource-coordination loading from AGENTS.md and retain skill-owned conditions only for decisions owned by those skills.
- Focused tests cover both resource-coordination selections for integration, delivery, and end-to-end verification.
- Generated skill documentation is current and all changed definitions pass independent methodology review.

## Dependencies

None.

## Verification

- Run the governed-definition pre-mutation check for each approved canonical source.
- Run focused integration, main-branch delivery, feature-branch delivery, and end-to-end verification tests with resource_coordination none and resource-claim.
- Run affected skill probes and generated-documentation freshness checks.
- Search maintained workflow skills for unconditional exact-name resource-claim references and classify each remaining occurrence.
- Run Markdown link checks and git diff --check.

## Open Questions

Determine the precise shared phrase that tells a workflow skill to apply the selected resource-coordination procedure without inventing an Interface Skill that does not exist.

## Governed Definition Approval

### Governed Canonical Sources

- skills/integrate-agent-work/SKILL.md
- skills/deliver-work-item-feature-branch/SKILL.md
- skills/deliver-work-item-main-branch/SKILL.md
- skills/verify-end-to-end-workflow/SKILL.md

### Allowed Dependent Artifacts

- evals/skill-probes.yaml
- directly affected focused evaluation fixtures and tests identified through source discovery
- design/agents/work-item-dispatching-and-delivery.md
- design/generated/skill-definitions.js
- supported generated adapter files regenerated from only the approved canonical sources

### Approval Resolution

Approved on 2026-08-09. In the Dev Backlog Coordinator task, the user stated: "I'm pretty sure I already approved the respect otional resource coordination - none of the active threads say \"Waiting for user\". Approve it now." This directly approves exactly the four governed skill-definition paths named in the pending question. It authorizes their directly affected focused evaluation fixtures and tests, the listed maintained design source, generator-owned skill projection, and supported generated adapters. It does not authorize another governed definition, unrelated framework work, or baseline absorption.

## User Action Required

### Question for the User

Do you approve updating exactly skills/integrate-agent-work/SKILL.md, skills/deliver-work-item-feature-branch/SKILL.md, skills/deliver-work-item-main-branch/SKILL.md, and skills/verify-end-to-end-workflow/SKILL.md so their workflows use the resource-coordination policy selected through AGENTS.md and perform no claim procedure when the project selects none?

### Why User Input Is Required

The defect is confirmed, but correcting it changes four governed portable skill definitions. The current documentation request does not grant authority to mutate those definitions.

### Options and Tradeoffs

- Approve the four-path correction: preserves resource coordination as an independent project choice and makes the workflow skills consistent with existing setup policy.
- Redesign configuration so integration, delivery, and verification always require resource-claim: removes the optional path but reverses the established selectable-resource-coordination contract and requires broader governed changes.
- Defer the correction: preserves current definitions and their contradiction with resource_coordination none.

### Resolution

Approved. Route this same Work Item through Ready -> Starting -> Running before source mutation.

### Question Reconciliation (2026-08-08)

The retired governed path skills/deliver-work-item-direct-main/SKILL.md was replaced with the current canonical path skills/deliver-work-item-main-branch/SKILL.md. Current-source inspection confirmed unconditional resource-claim instructions remain in all four canonical paths. No parent task or session history available for this reconciliation shows that the exact approval question was previously surfaced. The question remains pending.

### Unattended Work Boundary

Do not mutate the four governed SKILL.md files or their generated mirrors before approval. Read-only source discovery and analysis may continue. The already-authorized correction to design/agents/work-item-dispatching-and-delivery.md remains independent and complete.

## Approval Resumption Evidence

Approval Recorded At: 2026-08-09T05:01:00Z

Approval Provenance: Direct user message in Dev Backlog Coordinator task `019fb057-1767-7ef2-b5fa-41f4417b20b3` on 2026-08-09.

Approved Governed Paths:

- `skills/integrate-agent-work/SKILL.md`
- `skills/deliver-work-item-feature-branch/SKILL.md`
- `skills/deliver-work-item-main-branch/SKILL.md`
- `skills/verify-end-to-end-workflow/SKILL.md`

Approval Boundary: Correct these four definitions so they consume the resource-coordination policy selected through `AGENTS.md`, perform no claim procedure when selection is `none`, and preserve the complete configured `resource-claim` behavior. Only the already listed directly affected non-governed dependents are included. No other governed source or unrelated correction is approved.

Canonical Execution Reconciliation: No current or archived canonical task was found for this Work Item ID. Ready remains unowned until the Coordinator records a new Starting reservation. No source mutation is authorized in Ready.

## Starting Handoff Evidence

Starting Recorded At: 2026-08-09T05:03:00Z

Coordinator: Dev Backlog Coordinator task `019fb057-1767-7ef2-b5fa-41f4417b20b3`

Normalized Objective: Correct exactly four governed workflow skills so they consume the `AGENTS.md`-selected resource-coordination policy, perform no claim procedure when selection is `none`, and preserve complete configured `resource-claim` behavior, together with only directly affected approved tests and generated projections.

Launch Result: Requested after this durable reservation.

Canonical Execution: None

Intended Root Role: Dev Orchestrator

Scheduling Evidence: Two independent provider items are Running. Neither active task owns the four governed workflow skill paths. Begin in one isolated worktree with exact-path authorization checks and the four-definition private source lane. Defer shared mutation involving `evals/skill-probes.yaml`, generated skill definitions or adapters, shared review, installation, or main integration until direct reconciliation with the active terminology and tournament owners. The Blocked documentation-design-system item remains untouched.

Preservation Boundary: Do not create another governed definition or absorb unrelated baselines. No source mutation is authorized until the new canonical Root Dev Orchestrator independently records Starting -> Running with fresh bounded Active Execution Evidence and an exact activity=work claim.

Next Reconciliation At: 2026-08-09T05:18:00Z

## Active Execution Evidence

Condition Type: root-execution

Owner: Dev Orchestrator task 019fe4e7-95c9-7372-bd9f-aa983c5c7237

Evidence: Canonical root task 019fe4e7-95c9-7372-bd9f-aa983c5c7237 remains active on branch codex/respect-optional-resource-coordination-019fe4e7 in worktree /Users/martinbechard/.codex/worktrees/e01d/dev-methodology. Clean Dev Coder candidate 2e408116d3eff8e8f53767fc9c54c9ce84f0aa3b changes exactly the four approved workflow SKILL.md sources and new focused test scripts/test_optional_resource_coordination_workflow_skills.py, with 106 insertions and 4 deletions. Its focused test first failed with 12 expected subtest failures across both configuration selections, then passed 2 of 2 tests before and after commit. All four exact skills passed the repository narrow validator, Git diff validation passed, and the source worktree is clean. Direct terminology-owner and tournament-owner receipts confirm no private path overlap and authorize exact-manifest source review for these five paths. They explicitly withhold evals/skill-probes.yaml, scripts/test_bundle_content.py, generated definitions and adapters, shared installation, live-model evaluation, and main integration until terminology provider completion on clean current main and release of its overlapping claims. The Blocked documentation-design-system candidate remains untouched. Exact Work Item activity=work claim respect-optional-resource-coordination-019fe4e7-root-work-2 remained live through candidate completion and was released with disposition handoff only for this serialized provider update in journal event 9995cb7c-ab82-4cbf-b45c-ec2709d99988.

Observed At: 2026-08-09T05:43:40Z

Started At: 2026-08-09T05:42:45Z

Deadline or Expires At: 2026-08-09T06:28:40Z

Next Action: Commit this provider-only candidate-review evidence replacement, release its update and provider-path claims, reacquire the exact Work Item activity=work claim, dispatch fresh independent methodology review and source verification for candidate 2e408116d3eff8e8f53767fc9c54c9ce84f0aa3b, and route any exact five-path correction to the same Dev Coder without entering any withheld shared surface

Next Reconciliation At: 2026-08-09T05:57:40Z

## Running Resource Claim Evidence

Bootstrap Work Claim: respect-optional-resource-coordination-019fe4e7-bootstrap-work; Work Item ID respect-optional-resource-coordination-in-workflow-skills; activity work; outcome SHARED_CHECKOUT_ACQUIRED; acquired at 2026-08-09T05:08:03.052960Z; journal event 0b21b5b5-7fc1-4e4a-885f-8a2970cdba33; released with disposition handoff after branch establishment in journal event 376145cf-a334-4d45-9e6a-84891a742fd6

Provider Update Claim: respect-optional-resource-coordination-019fe4e7-running-update; Work Item ID respect-optional-resource-coordination-in-workflow-skills; activity update; outcome SHARED_CHECKOUT_ACQUIRED; acquired at 2026-08-09T05:08:46.990260Z; journal event f5077de3-3dea-4219-8249-cacfaf98bf43; released with disposition done in journal event 883af9a2-1ee0-49fe-b6a6-30aab0db1ef3 after Running commit 822abcfb04b5042310d5f0ee701e262a363c35b5

Provider Path Claim: respect-optional-resource-coordination-019fe4e7-running-path; path backlog/defect-backlog/respect-optional-resource-coordination-in-workflow-skills.md; outcome SHARED_CHECKOUT_ACQUIRED; acquired at 2026-08-09T05:09:28.189604Z; journal event 6afeea76-921b-4876-8813-6ba4a54c82cc; released in journal event 6a5fea11-bb2a-4ccb-83d1-47f043ce7cee after Running commit 822abcfb04b5042310d5f0ee701e262a363c35b5

Outcome Work Claim: respect-optional-resource-coordination-019fe4e7-root-work; Work Item ID respect-optional-resource-coordination-in-workflow-skills; activity work; outcome SHARED_CHECKOUT_ACQUIRED; acquired at 2026-08-09T05:13:44.160637Z; journal event 502c9f86-8830-449a-a22c-b18928d9a95c; released with disposition handoff solely for this provider update in journal event 120b2c2e-b302-4c8b-b87e-bcb8d59bdb6b

Evidence Update Claim: respect-optional-resource-coordination-019fe4e7-evidence-update-1; Work Item ID respect-optional-resource-coordination-in-workflow-skills; activity update; outcome SHARED_CHECKOUT_ACQUIRED; acquired at 2026-08-09T05:32:16.333926Z; journal event 1ba0b8eb-788b-440c-9d08-f6f5caaa6590; released with disposition done in journal event 8bfc63e2-b8ea-4ab4-9afc-de01e1c43064 after provider commit 37da1bab8502b7df408b7ceeea491a64c5e07650

Evidence Path Claim: respect-optional-resource-coordination-019fe4e7-evidence-path-1; path backlog/defect-backlog/respect-optional-resource-coordination-in-workflow-skills.md; outcome SHARED_CHECKOUT_ACQUIRED; acquired at 2026-08-09T05:32:33.072845Z; journal event bab3c86d-1809-47ba-ad33-b591d4110623; released in journal event b7bbcad8-c844-4eaa-90d4-227c814d95f7 after provider commit 37da1bab8502b7df408b7ceeea491a64c5e07650

Candidate Work Claim: respect-optional-resource-coordination-019fe4e7-root-work-2; Work Item ID respect-optional-resource-coordination-in-workflow-skills; activity work; outcome SHARED_CHECKOUT_ACQUIRED; acquired at 2026-08-09T05:36:33.659968Z; journal event 7bee54b5-875b-4fba-ab66-9562f87bd30b; released with disposition handoff solely for this provider update in journal event 9995cb7c-ab82-4cbf-b45c-ec2709d99988

Candidate Review Update Claim: respect-optional-resource-coordination-019fe4e7-evidence-update-2; Work Item ID respect-optional-resource-coordination-in-workflow-skills; activity update; outcome SHARED_CHECKOUT_ACQUIRED; acquired at 2026-08-09T05:44:26.831024Z; journal event b742a66c-2ce9-499b-b6ec-ecbf10d72c63; release immediately after this provider-only evidence commit

Candidate Review Path Claim: respect-optional-resource-coordination-019fe4e7-evidence-path-2; path backlog/defect-backlog/respect-optional-resource-coordination-in-workflow-skills.md; outcome SHARED_CHECKOUT_ACQUIRED; acquired at 2026-08-09T05:44:59.244916Z; journal event 54e67522-bfb0-4cab-80cd-9d2b93518932; release immediately after this provider-only evidence commit
