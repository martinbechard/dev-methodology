# Respect Optional Resource Coordination In Workflow Skills

Status: Completed

Owner: Unowned

Phase: Completed — Crisis Recovery

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

## Preserved Held-Candidate Evidence

Prior Condition Type: owned-wait

Owner: Dev Orchestrator task 019fe4e7-95c9-7372-bd9f-aa983c5c7237

Evidence: Canonical root task 019fe4e7-95c9-7372-bd9f-aa983c5c7237 remains active on branch codex/respect-optional-resource-coordination-019fe4e7 in worktree /Users/martinbechard/.codex/worktrees/e01d/dev-methodology. Accepted private candidate 28fb65a8b4d1f075e6b2f162c83d24b4e3e739b0 remains clean and unchanged with its exact five-path manifest; methodology ACCEPTED and verifier VERIFIED/PASS evidence remain retained and were not repeated. Terminology task 019fe3d6-2dd6-7322-a507-e8ca961e27d8 has not released the remaining shared event and is actively implementing its authorized projection, so no integration wake is valid. It retains evals/skill-probes.yaml, scripts/test_bundle_content.py, generated definitions and adapters, shared installation, live-model evaluation, and main integration. Release is event-driven: proceed only after a direct terminology-owner or parent Coordinator receipt names the exact released shared event and its applicable path or resource claim boundary. Until then, do not poll, redispatch, enter a retained shared surface, rerun the accepted private review or verification, or mutate candidate bytes. The Blocked documentation-design-system candidate remains untouched. Exact Work Item activity=work claim respect-optional-resource-coordination-019fe4e7-root-work-7 was confirmed live and heartbeated at 2026-08-09T07:17:21.116616Z in journal event 7b0a27b4-e1f8-4543-ad5d-b8c8d79ec5be, then released with disposition handoff solely for this serialized provider update in journal event f23dddcc-5531-44df-9eef-24a4f2202e7d; update claim respect-optional-resource-coordination-019fe4e7-evidence-update-7 and exact provider-path claim respect-optional-resource-coordination-019fe4e7-evidence-path-7 now protect this one provider-only replacement.

Prior Observed At: 2026-08-09T07:18:20Z

Prior Started At: 2026-08-09T07:18:20Z

Prior Deadline or Expires At: 2026-08-09T08:03:20Z

Prior Next Action: Act only on a direct release receipt naming the exact shared event by first acquiring its applicable path or resource claim

Prior Next Reconciliation At: 2026-08-09T07:32:20Z

## Running Resource Claim Evidence

Bootstrap Work Claim: respect-optional-resource-coordination-019fe4e7-bootstrap-work; Work Item ID respect-optional-resource-coordination-in-workflow-skills; activity work; outcome SHARED_CHECKOUT_ACQUIRED; acquired at 2026-08-09T05:08:03.052960Z; journal event 0b21b5b5-7fc1-4e4a-885f-8a2970cdba33; released with disposition handoff after branch establishment in journal event 376145cf-a334-4d45-9e6a-84891a742fd6

Provider Update Claim: respect-optional-resource-coordination-019fe4e7-running-update; Work Item ID respect-optional-resource-coordination-in-workflow-skills; activity update; outcome SHARED_CHECKOUT_ACQUIRED; acquired at 2026-08-09T05:08:46.990260Z; journal event f5077de3-3dea-4219-8249-cacfaf98bf43; released with disposition done in journal event 883af9a2-1ee0-49fe-b6a6-30aab0db1ef3 after Running commit 822abcfb04b5042310d5f0ee701e262a363c35b5

Provider Path Claim: respect-optional-resource-coordination-019fe4e7-running-path; path backlog/defect-backlog/respect-optional-resource-coordination-in-workflow-skills.md; outcome SHARED_CHECKOUT_ACQUIRED; acquired at 2026-08-09T05:09:28.189604Z; journal event 6afeea76-921b-4876-8813-6ba4a54c82cc; released in journal event 6a5fea11-bb2a-4ccb-83d1-47f043ce7cee after Running commit 822abcfb04b5042310d5f0ee701e262a363c35b5

Outcome Work Claim: respect-optional-resource-coordination-019fe4e7-root-work; Work Item ID respect-optional-resource-coordination-in-workflow-skills; activity work; outcome SHARED_CHECKOUT_ACQUIRED; acquired at 2026-08-09T05:13:44.160637Z; journal event 502c9f86-8830-449a-a22c-b18928d9a95c; released with disposition handoff solely for this provider update in journal event 120b2c2e-b302-4c8b-b87e-bcb8d59bdb6b

Evidence Update Claim: respect-optional-resource-coordination-019fe4e7-evidence-update-1; Work Item ID respect-optional-resource-coordination-in-workflow-skills; activity update; outcome SHARED_CHECKOUT_ACQUIRED; acquired at 2026-08-09T05:32:16.333926Z; journal event 1ba0b8eb-788b-440c-9d08-f6f5caaa6590; released with disposition done in journal event 8bfc63e2-b8ea-4ab4-9afc-de01e1c43064 after provider commit 37da1bab8502b7df408b7ceeea491a64c5e07650

Evidence Path Claim: respect-optional-resource-coordination-019fe4e7-evidence-path-1; path backlog/defect-backlog/respect-optional-resource-coordination-in-workflow-skills.md; outcome SHARED_CHECKOUT_ACQUIRED; acquired at 2026-08-09T05:32:33.072845Z; journal event bab3c86d-1809-47ba-ad33-b591d4110623; released in journal event b7bbcad8-c844-4eaa-90d4-227c814d95f7 after provider commit 37da1bab8502b7df408b7ceeea491a64c5e07650

Candidate Work Claim: respect-optional-resource-coordination-019fe4e7-root-work-2; Work Item ID respect-optional-resource-coordination-in-workflow-skills; activity work; outcome SHARED_CHECKOUT_ACQUIRED; acquired at 2026-08-09T05:36:33.659968Z; journal event 7bee54b5-875b-4fba-ab66-9562f87bd30b; released with disposition handoff solely for this provider update in journal event 9995cb7c-ab82-4cbf-b45c-ec2709d99988

Candidate Review Update Claim: respect-optional-resource-coordination-019fe4e7-evidence-update-2; Work Item ID respect-optional-resource-coordination-in-workflow-skills; activity update; outcome SHARED_CHECKOUT_ACQUIRED; acquired at 2026-08-09T05:44:26.831024Z; journal event b742a66c-2ce9-499b-b6ec-ecbf10d72c63; released with disposition done in journal event ab591a88-6596-4884-91c7-cb6f9816054b after provider commit f945d2ededa9d96a440991d959f11190b9a1b5c0

Candidate Review Path Claim: respect-optional-resource-coordination-019fe4e7-evidence-path-2; path backlog/defect-backlog/respect-optional-resource-coordination-in-workflow-skills.md; outcome SHARED_CHECKOUT_ACQUIRED; acquired at 2026-08-09T05:44:59.244916Z; journal event 54e67522-bfb0-4cab-80cd-9d2b93518932; released in journal event 9b7c229c-85a4-4f56-80d2-f668a3c6032a after provider commit f945d2ededa9d96a440991d959f11190b9a1b5c0

Review Work Claim: respect-optional-resource-coordination-019fe4e7-root-work-3; Work Item ID respect-optional-resource-coordination-in-workflow-skills; activity work; outcome SHARED_CHECKOUT_ACQUIRED; acquired at 2026-08-09T05:47:57.478279Z; journal event fd56130d-67fb-4f19-b4a9-e59e09e71d0b; released with disposition handoff solely for this provider update in journal event c4e36db8-c0a5-4969-bf8b-80e1c052e7d8

Correction Update Claim: respect-optional-resource-coordination-019fe4e7-evidence-update-3; Work Item ID respect-optional-resource-coordination-in-workflow-skills; activity update; outcome SHARED_CHECKOUT_ACQUIRED; acquired at 2026-08-09T05:59:12.672504Z; journal event 8a85c93f-50b4-4d06-95e0-d7c611c00afe; released with disposition done in journal event fdb5f3b4-4db7-4b85-820e-58efe99ac1c9 after provider commit 2cddb0fc7dd7b142fcfeec36eec2d3393745b991

Correction Path Claim: respect-optional-resource-coordination-019fe4e7-evidence-path-3; path backlog/defect-backlog/respect-optional-resource-coordination-in-workflow-skills.md; outcome SHARED_CHECKOUT_ACQUIRED; acquired at 2026-08-09T05:59:25.525662Z; journal event ca9ab2de-f5f3-422e-bb8a-0f7a3ce7fd58; released in journal event 854486f5-e7b2-414e-bf75-d2b4fe87913c after provider commit 2cddb0fc7dd7b142fcfeec36eec2d3393745b991

Correction Work Claim: respect-optional-resource-coordination-019fe4e7-root-work-4; Work Item ID respect-optional-resource-coordination-in-workflow-skills; activity work; outcome SHARED_CHECKOUT_ACQUIRED; acquired at 2026-08-09T06:02:35.761338Z; journal event 96c88ece-a179-4b9e-ab66-1d7196780787; released with disposition handoff solely for this provider update in journal event 682f3e2a-bfb1-4a45-aed0-9662fb5a8d60

Correction Evidence Update Claim: respect-optional-resource-coordination-019fe4e7-evidence-update-4; Work Item ID respect-optional-resource-coordination-in-workflow-skills; activity update; outcome SHARED_CHECKOUT_ACQUIRED; acquired at 2026-08-09T06:10:45.559574Z; journal event 3fa0d5e3-0be3-47c8-a945-f21126265caa; released with disposition done in journal event 86f71ec2-2a20-4956-af54-1ce5a82dd10c after provider commit 09ce4cccc96d59c4c0de158a094dfcd13625873a

Correction Evidence Path Claim: respect-optional-resource-coordination-019fe4e7-evidence-path-4; path backlog/defect-backlog/respect-optional-resource-coordination-in-workflow-skills.md; outcome SHARED_CHECKOUT_ACQUIRED; acquired at 2026-08-09T06:10:59.046622Z; journal event 54b7c9f6-fa69-4d8c-b206-f2f4c50cb0ee; released in journal event f6e71fe3-feaf-41a2-8244-3ba1cac63e75 after provider commit 09ce4cccc96d59c4c0de158a094dfcd13625873a

Replacement Candidate Work Claim: respect-optional-resource-coordination-019fe4e7-root-work-5; Work Item ID respect-optional-resource-coordination-in-workflow-skills; activity work; outcome SHARED_CHECKOUT_ACQUIRED; acquired at 2026-08-09T06:15:00.511938Z; journal event 23e2fa2c-1e98-460a-9898-3627e460dc9f; released with disposition handoff solely for this provider update in journal event 1e044570-4abd-46b8-93d5-b5176221b549

Replacement Candidate Update Claim: respect-optional-resource-coordination-019fe4e7-evidence-update-5; Work Item ID respect-optional-resource-coordination-in-workflow-skills; activity update; outcome SHARED_CHECKOUT_ACQUIRED; acquired at 2026-08-09T06:26:27.388088Z; journal event 60af7c8b-5bc5-41fd-99c4-5c716344846d; released with disposition done in journal event a9b553dc-2e49-4908-aca8-011e39acb9e4 after provider commit 23d693a2cbada90e85eed24d4cce40996b5058cd

Replacement Candidate Path Claim: respect-optional-resource-coordination-019fe4e7-evidence-path-5; path backlog/defect-backlog/respect-optional-resource-coordination-in-workflow-skills.md; outcome SHARED_CHECKOUT_ACQUIRED; acquired at 2026-08-09T06:26:48.986492Z; journal event 7e8a3105-efa4-4d2f-837c-ca8652055d8b; released in journal event 444e5daf-3058-44c6-92a9-9979e31527fd after provider commit 23d693a2cbada90e85eed24d4cce40996b5058cd

Accepted Candidate Work Claim: respect-optional-resource-coordination-019fe4e7-root-work-6; Work Item ID respect-optional-resource-coordination-in-workflow-skills; activity work; outcome SHARED_CHECKOUT_ACQUIRED; acquired at 2026-08-09T06:30:04.972453Z; journal event 94481410-02a9-42ff-8180-1c9ff83e98c1; released with disposition handoff solely for this provider update in journal event fa9faf55-15fd-4f38-9536-40254891b5b1

Accepted Candidate Update Claim: respect-optional-resource-coordination-019fe4e7-evidence-update-6; Work Item ID respect-optional-resource-coordination-in-workflow-skills; activity update; outcome SHARED_CHECKOUT_ACQUIRED; acquired at 2026-08-09T06:38:51.261798Z; journal event d170e6b4-7295-42b1-a744-4d4893ceaf9d; released with disposition done in journal event 934de81f-fd2b-4617-b381-db7f674385ee after provider commit 69beebc20fc781d01cc3f8798771c6aad1b5ce45

Accepted Candidate Path Claim: respect-optional-resource-coordination-019fe4e7-evidence-path-6; path backlog/defect-backlog/respect-optional-resource-coordination-in-workflow-skills.md; outcome SHARED_CHECKOUT_ACQUIRED; acquired at 2026-08-09T06:39:03.329630Z; journal event 1a91d8b9-728f-4d54-b866-47f0208e1d5d; released in journal event 1d3b4dc7-964c-4490-9d8f-d01646b12e1a after provider commit 69beebc20fc781d01cc3f8798771c6aad1b5ce45

Owned-Wait Work Claim: respect-optional-resource-coordination-019fe4e7-root-work-7; Work Item ID respect-optional-resource-coordination-in-workflow-skills; activity work; outcome SHARED_CHECKOUT_ACQUIRED; acquired at 2026-08-09T06:42:38.519937Z; journal event c65153a1-4310-422f-8e3a-5e5838d8d361; heartbeat at 2026-08-09T07:17:21.116616Z in journal event 7b0a27b4-e1f8-4543-ad5d-b8c8d79ec5be; released with disposition handoff solely for this provider update in journal event f23dddcc-5531-44df-9eef-24a4f2202e7d

Owned-Wait Update Claim: respect-optional-resource-coordination-019fe4e7-evidence-update-7; Work Item ID respect-optional-resource-coordination-in-workflow-skills; activity update; outcome SHARED_CHECKOUT_ACQUIRED; acquired at 2026-08-09T07:17:44.733022Z; journal event 636d3563-affb-48e3-b1e6-3c7fc73e0b0a; release immediately after this provider-only evidence commit

Owned-Wait Path Claim: respect-optional-resource-coordination-019fe4e7-evidence-path-7; path backlog/defect-backlog/respect-optional-resource-coordination-in-workflow-skills.md; outcome SHARED_CHECKOUT_ACQUIRED; acquired at 2026-08-09T07:17:54.092781Z; journal event 985c1f1c-c570-430a-87ae-9ce469637f61; release immediately after this provider-only evidence commit

## Holding Handoff Evidence

Holding Recorded At: 2026-08-09T07:51:00Z

Coordinator: Dev Backlog Coordinator task `019fb057-1767-7ef2-b5fa-41f4417b20b3`

Reason: Accepted candidate `28fb65a8b4d1f075e6b2f162c83d24b4e3e739b0` is independently accepted and verified, but the terminology predecessor has not released the exact shared catalog, generated, installation, live-model, and main-integration event. Repeated idle owned-wait evidence is no longer an eligible Running condition.

Preserved Execution: Canonical task `019fe4e7-95c9-7372-bd9f-aa983c5c7237`, branch `codex/respect-optional-resource-coordination-019fe4e7`, clean worktree `/Users/martinbechard/.codex/worktrees/e01d/dev-methodology`, exact five-path candidate, methodology ACCEPTED verdict, and verifier VERIFIED/PASS result.

Claim Disposition: Exact activity=work claim `respect-optional-resource-coordination-019fe4e7-root-work-8` was released once with disposition handoff in journal event `f92ee891-6b82-4e79-b1e0-5b3c3160be22`. No claim remains for this work item.

Resumption Condition: Receive one direct terminology completion or shared-event release receipt naming the exact released paths and resource boundary. Then record Holding -> Ready -> Starting for this same canonical task. The task must independently record Starting -> Running with fresh bounded evidence and exact claims before entering shared surfaces or delivery.

Current Boundary: Do not poll, redispatch, reacquire a work claim, repeat accepted gates, mutate candidate bytes, or enter shared catalog, generated, installation, live-model, or integration surfaces while Holding.

## Crisis Completion Evidence

Completed At: 2026-08-09

Coordinator: Dev Backlog Coordinator task `019fb057-1767-7ef2-b5fa-41f4417b20b3` operating in user-directed SOLO crisis mode.

Delivery: Accepted candidate commits `2e408116d3eff8e8f53767fc9c54c9ce84f0aa3b` and `28fb65a8b4d1f075e6b2f162c83d24b4e3e739b0` were replayed to main as `b829227c` and `3844bcd3`. Generated skill documentation was refreshed in `9fff438a`.

Verification: The focused optional-resource-coordination regression ran 3/3, all four changed Agent Skills validated, skill documentation and hierarchy freshness passed, the support checklist was current, the full bundle ran 174/174, and `git diff --check` passed. The previously accepted methodology review and independent verifier PASS remain preserved.

Outcome: Workflow skills now consume the AGENTS.md-selected coordination policy. Projects selecting `none` perform no claim procedure or claim-specific reporting; projects selecting `resource-claim` preserve the complete configured behavior.

Boundaries: No user-level installation, live-model evaluation, remote publication, or unrelated baseline correction occurred.
