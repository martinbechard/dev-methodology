# Model Directly Invoked Skills As Static Classes

Status: Completed

Type: Feature

Provider: file

Work Item ID: model-directly-invoked-skills-as-static-classes

Completion: main-branch

## Summary

Extend the object-oriented Agent and Skill model with Static Classes for skills that callers invoke directly outside Agent definitions. Use the private Backlog Dispatcher skill and its invocation of the Dev Backlog Coordinator as the primary example, and align the dispatch-process documentation with the current Codex root-task launch constraint.

## Starting Handoff Evidence

- Starting Recorded At: 2026-08-12T18:22:03Z.
- Coordinator: Backlog Dispatcher Codex task `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`, acting through canonical Dev Backlog Coordinator subagent `/root/backlog_coordinator`.
- Dispatch Reservation: `reserve-starting-model-static-classes-019ff2c3`.
- Normalized Objective: Define Static Classes for directly invoked skills, document the private Backlog Dispatcher to Dev Backlog Coordinator example and root-owned Codex task-launch boundary, and verify OpenAI-attributed statements against official sources.
- Intended Root Role: Dev Orchestrator.
- Launch Result: Started. Caller creation succeeded after pending worktree resolution without retry.
- Runtime Parent Task ID: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Dev Backlog Coordinator Task Identity: `/root/backlog_coordinator`.
- Canonical Execution: Codex task `019ff737-8b68-7010-8342-ca3cc356053e` on host `local`.
- Canonical Codex Task ID: `019ff737-8b68-7010-8342-ca3cc356053e`.
- Canonical Conversation ID: `019ff737-8b68-7010-8342-ca3cc356053e`; this runtime exposes one combined identity.
- Pending Client Identity: `client-new-thread:6cc87bc3-e1d1-4ec4-9692-dd2944a21d6c`, resolved uniquely to the canonical task above.
- Runtime Worktree: `/Users/martinbechard/.codex/worktrees/d7b9/dev-methodology`.
- Runtime Creation Time: 2026-08-12T18:24:04Z (`1786559044`).
- Runtime State: Active. This proves a successful launch only and does not prove Running acceptance.
- Conversation Title: `Starting — Model Directly Invoked Skills As Static Classes`, explicitly synchronized and confirmed.
- Baseline Commit: `aac210514eadad32ce0678fbf0860c4724ebee4b`.
- Provider Claim: `reserve-starting-model-static-classes-019ff2c3`; outcome `SHARED_CHECKOUT_ACQUIRED`; event `52ce6fa6-f1b6-4308-a1e0-138a1faa3757`.
- Identity Reconciliation Claim: `reconcile-starting-model-static-classes-019ff737`; outcome `SHARED_CHECKOUT_ACQUIRED`; event `40e7bfec-088d-420d-81c1-e02893507156`.
- Last Contact: 2026-08-12T18:24:04Z, caller returned the successful canonical task identity and active runtime state.
- Next Reconciliation: Accept the canonical task's distinct Starting -> Running provider transition or reconcile a concrete failed, stopped, missing, or blocked handoff. Do not create a replacement automatically.
- Next Lifecycle Owner: The new root Dev Orchestrator must claim this exact Work Item ID with activity `update` and record the distinct Starting -> Running acceptance before implementation or documentation mutation.

## Scheduling Evidence

- Mode: MULTITASK enabled and verified after crisis exit.
- Active Eligibility Before Reservation: zero Starting and zero Running items.
- Effective Scheduling Limit: one new launch in this scheduling pass. The selected item is independent of active delivery because no active delivery or finish-lane candidate exists.
- Capacity Result: one of one pass-local launch slots reserved; this item now consumes the slot as Starting.
- Dependencies: None.
- Overlap Result: no canonical execution, provider duplicate, active claim, active work-item path owner, or finish-lane delivery overlaps this item. Documentation paths remain unclaimed until the root Dev Orchestrator accepts Running and acquires its outcome-work claim.

## Running Acceptance Evidence

- Running Recorded At: 2026-08-12T18:26:22Z.
- Owner: Root Dev Orchestrator.
- Canonical Codex Task ID: `019ff737-8b68-7010-8342-ca3cc356053e`.
- Canonical Conversation ID: `019ff737-8b68-7010-8342-ca3cc356053e`; the current Codex runtime exposes one combined identity through the task surface, so the distinct provider fields retain the same runtime-supplied value.
- Runtime Parent Task ID: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Dev Backlog Coordinator Task Identity: `/root/backlog_coordinator`.
- Root Role: Dev Orchestrator.
- Branch: `codex/model-direct-skills-static-classes`.
- Worktree: `/Users/martinbechard/.codex/worktrees/d7b9/dev-methodology`.
- Phase: Documentation design and source reconciliation.
- Accepted Baseline: `84e8ceec51974eb9302890b11eb6d1c3921351f3`, verified as the private worktree HEAD before work began.
- Accepted Execution Evidence: the canonical root task is active in the reserved private worktree, accepted the exact Work Item ID, created its dedicated branch at the accepted baseline, and acquired the distinct activity `update` work-item claim plus the exact provider-path claim before this transition.
- Provider Update Claim: `running-model-static-classes-019ff737`; outcome `SHARED_CHECKOUT_ACQUIRED`; event `db9f27fc-9e90-4eee-b556-4842264f9c14`.
- Provider Path Claim: `running-provider-path-model-static-019ff737`; outcome `SHARED_CHECKOUT_ACQUIRED`; event `6033c8fd-247b-4c9b-8e86-16d9f09cfa80`.
- Next Action: commit this distinct Starting -> Running provider mutation, release both update claims with disposition `handoff` where required, then acquire activity `work` and the exact documentation path ownership before source mutation.

## Completion Evidence

- Completed At: 2026-08-12T19:00:10Z.
- Outcome: Defined directly invoked Skills as Static Classes, documented Backlog Dispatcher as the project-private worked example that invokes Dev Backlog Coordinator, and aligned the canonical dispatch process with the conditional Coordinator-direct versus caller-owned runtime-operation boundary.
- Accepted Baseline: `84e8ceec51974eb9302890b11eb6d1c3921351f3`.
- Candidate Branch: `codex/model-direct-skills-static-classes`.
- Candidate Commits: `9767a68bb9f2aa510e29f88768b9a8a05813e994`, `aa811d3ff1c8aa80d12982c44c685b9e1c12b903`, and `61df16407378540800045f16479691338a34cd78`.
- Main Integration Commits: `c2925941`, `9dd60b79`, and `653f20f9`.
- Main Observation: `653f20f963e26d69c448c4b8db6abc1df3f3f4d8` is the verified current-main documentation result before this provider completion transaction.
- Changed Maintained Documents: `design/object-oriented-agent-and-skill-model.md` and `design/agents/work-item-dispatching-and-delivery.md`; no generated projection is owned by either document.
- Independent Reviews: initial topic review found four corrections; an independent methodology/source review found one stale claim-helper selection; all findings were corrected. Final fresh source review accepted candidate `61df16407378540800045f16479691338a34cd78` with no material findings.
- Independent Verification: accepted candidate `61df16407378540800045f16479691338a34cd78`; exact two-file scope, historical provenance, links and anchors, navigation, citations, Mermaid notation and fences, source ownership, provider-family tests, focused resource-coordination tests, and Git whitespace checks passed.
- Primary-Root Verification: configured `verify_markdown_links` checked both changed documents after integration and returned `ok: true` with zero findings. `python3 -m unittest scripts.test_provider_family_naming scripts.test_project_document_provenance` ran 11 tests successfully. Python 3.11 focused bundle-content selectors for claim-rule ownership and Codex collaboration references both passed. `git diff --check 61736b2a..653f20f9` passed.
- Source Truthfulness: official OpenAI documentation supports reusable Skill packages, explicit or implicit Skill invocation, distinct outcome chats, and saved-chat resumption. The stronger caller-owned root task-control boundary remains labeled observed current Codex runtime and harness behavior plus a project coordination constraint, not an OpenAI general guarantee.
- Residual Environment Notes: the isolated-worktree MCP link check was structurally unavailable, so it was rerun successfully after integration at the configured primary root. Mermaid CLI and markdownlint were unavailable; independent structural checks and focused regression tests found no candidate defect. One broad unchanged resource-claim-helper fixture test has an unrelated untracked-directory failure; focused candidate-relevant tests passed.
- Integration Claim: `integrate-model-static-classes-019ff737`; acquired event `1a15ce89-f738-463d-b8eb-2019172fd85e`; released event `8d4f96af-97cd-4e54-b020-83409c661e02`.
- Outcome-Work Claim: `work-model-static-classes-019ff737`; released with disposition `handoff` in event `d23aef45-3802-4fb0-bf91-fb80a7b7f955` before the terminal provider update.
- Completion Update Claim: `complete-model-static-classes-019ff737`; acquired event `decb4f9b-9f65-4ffb-bdf9-bb95b147e410`.
- Completion Path Claim: `complete-provider-paths-model-static-019ff737`; acquired event `080a3290-0f6c-413f-a14e-df01c7846f38`.
- Canonical Codex Task ID: `019ff737-8b68-7010-8342-ca3cc356053e`.
- Canonical Conversation ID: `019ff737-8b68-7010-8342-ca3cc356053e`; the runtime exposes one combined identity while the provider preserves distinct fields.

## Context

The design currently models Agents, Skills, Skill Groups, and related definition relationships. It does not give directly invoked operational skills a distinct object-oriented representation when those skills are not dependencies of an Agent definition.

The project-private `.agents/skills/backlog-dispatcher/SKILL.md` is such an entry point. It coordinates caller-owned runtime operations and invokes the Dev Backlog Coordinator Role, but it is not itself a portable Agent definition. Current Codex coordination also requires the caller-owned root task to perform work-item task creation. This runtime constraint explains why Backlog Dispatcher remains a Skill rather than an Agent.

Official OpenAI documentation supports only the broader public claims that Codex work can run as separate tasks or threads and that Skills package reusable instructions and workflows. Unless stronger official evidence is found, the root-only task-launch constraint must be described as current observed Codex runtime or harness behavior, not as a general OpenAI platform guarantee.

## Source Evidence

On 2026-08-12, after restarting Codex and completing the resource-claim repair, the user requested: add Static Classes to `design/object-oriented-agent-and-skill-model.md` for directly invoked skills outside Agent definitions; use the private Backlog Dispatcher as an example that invokes the Dev Backlog Coordinator; update the dispatch-process documentation to explain that Codex tasks can start other tasks only from root and therefore Backlog Dispatcher is a Skill rather than an Agent; and verify the claim in official OpenAI documentation.

Relevant repository sources are `design/object-oriented-agent-and-skill-model.md`, `design/agents/work-item-dispatching-and-delivery.md`, `.agents/skills/backlog-dispatcher/SKILL.md`, `skills/coordinate-codex-tasks/SKILL.md`, and the applicable conceptual Agent role definitions. Relevant official sources include OpenAI's Codex product documentation about multiple tasks or threads and Skills as reusable workflow packages.

## Requirements

- Define Static Class semantics and notation for a Skill that callers invoke directly without instantiating or attaching it to an Agent definition.
- Distinguish Static Classes from Agent dependencies, request-triggered skill loading, `AGENTS.md` provider selection, Interface Skills, Provider Skills, and Skill Groups.
- Use private Backlog Dispatcher as the primary worked example. Show that it invokes the Dev Backlog Coordinator Role while leaving caller-owned root task creation with the authorized runtime dispatcher.
- Explain why Backlog Dispatcher is modeled and placed as a project-private Skill rather than as an Agent.
- Preserve the boundary between project-private `.agents/skills` content and portable distributable skills or Agent definitions.
- Update `design/object-oriented-agent-and-skill-model.md` and the canonical dispatch-process documentation, including diagrams, terminology, navigation, examples, and cross-links that those documents own.
- Inspect `design/agents` and the complete `design/orchestrated-development-lifecycle.html` before choosing the final model and wording.
- Verify every OpenAI-platform statement against current official OpenAI documentation.
- Attribute only source-supported public behavior to OpenAI. Label the root-only task-launch constraint as observed current Codex runtime or harness behavior unless an official OpenAI source states that exact constraint.
- Update generated projections only through their canonical source and supported generator when repository discovery proves that a changed canonical source owns them.
- Apply the configured document-provenance contract to every changed maintained document.

## Acceptance Criteria

- The object-oriented model defines Static Class in a way that is consistent with the existing Agent, Skill, Interface Skill, Provider Skill, and Skill Group model.
- The model contains a clear Backlog Dispatcher example that invokes Dev Backlog Coordinator without representing Backlog Dispatcher as an Agent.
- The dispatch-process documentation explains the caller-owned root task boundary and the resulting Skill-versus-Agent design choice.
- Statements attributed to OpenAI have direct citations to current official OpenAI documentation; runtime-specific observations are clearly identified and are not overstated as public guarantees.
- Private placement and portable publication boundaries remain consistent with `.agents/skills/backlog-dispatcher/SKILL.md` and current project guidance.
- All affected navigation, links, diagrams, terminology, generated artifacts, and provenance are consistent and current.
- Fresh independent review finds no loss of lifecycle authority, runtime ownership, or object-model distinctions.

## Dependencies

None.

## Verification

- Run the repository-supported checks for changed design Markdown and HTML artifacts, links, navigation, provenance, and generated freshness.
- Verify any regenerated output by exact source-to-projection comparison through its supported generator.
- Check every external citation against the current official OpenAI source and confirm that the cited text supports the associated claim.
- Run focused regression tests for any changed design generator, catalog, or documentation projection.
- Run Git diff whitespace validation.
- Obtain fresh independent document-topic review, methodology-artifact review, and documentation verification before delivery.

## Open Questions

None. The implementer must resolve notation and exact document ownership from repository design authority without changing the requested semantics.

## Notes

The official OpenAI sources presently identified support separate Codex task or thread execution and reusable Skills. They do not presently establish the stronger root-only task-launch rule. Treat that distinction as a required truthfulness boundary during delivery.
