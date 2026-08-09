# Respect Optional Resource Coordination In Workflow Skills

Status: Running

Owner: Dev Orchestrator task `019fe4e7-95c9-7372-bd9f-aa983c5c7237`

Phase: Running — Private four-definition source lane

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

Evidence: Codex task 019fe4e7-95c9-7372-bd9f-aa983c5c7237 is active in the clean isolated worktree /Users/martinbechard/.codex/worktrees/e01d/dev-methodology on branch codex/respect-optional-resource-coordination-019fe4e7 at Starting baseline ebff99898ae6c297813bc165b1625375b1ea8469. Exact Work Item bootstrap activity=work claim respect-optional-resource-coordination-019fe4e7-bootstrap-work acquired with outcome SHARED_CHECKOUT_ACQUIRED in journal event 0b21b5b5-7fc1-4e4a-885f-8a2970cdba33 and released with disposition handoff in journal event 376145cf-a334-4d45-9e6a-84891a742fd6 after branch establishment. The serialized Starting -> Running provider transaction is protected by exact Work Item activity=update claim respect-optional-resource-coordination-019fe4e7-running-update, journal event f5077de3-3dea-4219-8249-cacfaf98bf43, and exact provider-path claim respect-optional-resource-coordination-019fe4e7-running-path, journal event 6afeea76-921b-4876-8813-6ba4a54c82cc. Current live claim inventory confirms the terminology and tournament owners retain only their recorded scopes; neither owns the four approved canonical definition paths. The private source lane excludes evals/skill-probes.yaml, generated definitions and adapters, shared review or installation, and main integration until direct owner reconciliation. The Blocked documentation-design-system candidate remains untouched.

Observed At: 2026-08-09T05:10:35Z

Started At: 2026-08-09T05:08:03Z

Deadline or Expires At: 2026-08-09T07:10:35Z

Next Action: Commit this atomic Running transition, release its update and provider-path claims, reacquire the exact Work Item activity=work claim, run work-item-native authorization checks for each approved canonical path, and implement only the private four-definition lane with directly affected focused tests

Next Reconciliation At: 2026-08-09T05:25:35Z

## Running Resource Claim Evidence

Bootstrap Work Claim: respect-optional-resource-coordination-019fe4e7-bootstrap-work; Work Item ID respect-optional-resource-coordination-in-workflow-skills; activity work; outcome SHARED_CHECKOUT_ACQUIRED; acquired at 2026-08-09T05:08:03.052960Z; journal event 0b21b5b5-7fc1-4e4a-885f-8a2970cdba33; released with disposition handoff after branch establishment in journal event 376145cf-a334-4d45-9e6a-84891a742fd6

Provider Update Claim: respect-optional-resource-coordination-019fe4e7-running-update; Work Item ID respect-optional-resource-coordination-in-workflow-skills; activity update; outcome SHARED_CHECKOUT_ACQUIRED; acquired at 2026-08-09T05:08:46.990260Z; journal event f5077de3-3dea-4219-8249-cacfaf98bf43; release immediately after the Running provider transaction

Provider Path Claim: respect-optional-resource-coordination-019fe4e7-running-path; path backlog/defect-backlog/respect-optional-resource-coordination-in-workflow-skills.md; outcome SHARED_CHECKOUT_ACQUIRED; acquired at 2026-08-09T05:09:28.189604Z; journal event 6afeea76-921b-4876-8813-6ba4a54c82cc; release immediately after the Running provider transaction
