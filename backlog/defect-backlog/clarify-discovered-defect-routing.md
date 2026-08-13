# Clarify Discovered Defect Routing

Status: Starting

Type: Defect

Provider: file

Work Item ID: clarify-discovered-defect-routing

Completion: main-branch

## Summary

Make the file-provider methodology state the complete positive workflow for a confirmed defect discovered during other work, including durable creation in User Action Required when implementation lacks authorization.

## Context

The current rules are split across two skills. skills/manage-work-items-file/SKILL.md says not to move an independently identified defect into a typed active folder until the user explicitly authorizes the new work. skills/create-work-item-file/SKILL.md separately says to create confirmed independently identified work in backlog/user-action-required and ask whether it should proceed.

An agent can read the prohibition without loading or locating the positive creation rule. During Work Item review-wiki-skills-and-project-context-text, this separation caused a confirmed provenance defect to be recorded only as a residual gap instead of receiving its required durable User Action Required work item.

## Source Evidence

On 2026-08-11 in canonical task 019ff2f9-0863-7133-aac0-ff3cb81dab14, the user identified the ambiguity: "There's confusion - it should be placed in the backlog but with User Action Required." The user then directed: "we need two defects: one we already discussed, second is lack of clarity about what to do when discovering a defect - it's not enough to know what not to do. Please create the defects now."

Repository evidence is the negative rule in skills/manage-work-items-file/SKILL.md and the positive creation rule in skills/create-work-item-file/SKILL.md.

## Requirements

- State the complete positive routing outcome wherever the prohibition on unauthorized active-backlog placement is defined.
- Require a confirmed independently discovered defect to receive one durable file-provider work item in backlog/user-action-required when the user has not authorized implementation.
- Preserve Type: Defect, Status: User Action Required, the exact approval question, source evidence, and unattended-work boundary.
- Distinguish confirmed defects from possibilities, Future Ideas, agent-resolvable technical uncertainty, ordinary blockers, and already authorized work.
- Keep creation authority, lifecycle authority, and implementation authority separate.
- Align the creation and management skills so an agent cannot satisfy the rule by reporting only an ephemeral or residual gap.
- Add focused regression assertions for the positive workflow and cross-skill consistency.

## Acceptance Criteria

- The negative prohibition is immediately paired with an explicit positive destination and action.
- The creation and management skills give the same outcome for a confirmed independently discovered unauthorized defect.
- Examples cover User Action Required creation, later approval to Ready, deferral to Holding, and rejection or abandonment.
- The rules do not create User Action Required records for speculative possibilities or agent-actionable technical problems.
- Focused bundle-content and skill-validation checks pass.
- Fresh methodology and prompt-contract review finds no ambiguous authority or lifecycle path.

## Dependencies

None.

## Verification

- Run focused assertions covering the discovered-defect routing statements in both skills.
- Validate each changed skill package.
- Run affected metadata and generated-output freshness checks if skill descriptions or generated consumers change.
- Run git diff checks for the exact changed paths.

## Open Questions

- Should one skill own the normative rule with the other linking to it, or should both carry the same concise positive requirement?

## Governed Definition Approval

### Governed Canonical Sources

- skills/manage-work-items-file/SKILL.md
- skills/create-work-item-file/SKILL.md

### Allowed Dependent Artifacts

- scripts/test_bundle_content.py
- Generated documentation or adapter outputs only if an approved canonical source change makes regeneration necessary.

### Approval Resolution

Approved on 2026-08-13. The user explicitly approved changing both governed canonical paths, `skills/manage-work-items-file/SKILL.md` and `skills/create-work-item-file/SKILL.md`, with focused tests.

## User Action Required

### Question for the User

Do you approve changing skills/manage-work-items-file/SKILL.md and skills/create-work-item-file/SKILL.md, with focused tests, to make the positive User Action Required routing for confirmed discovered defects explicit and consistent?

### Why User Input Is Required

The defect is confirmed, but the correction changes two governed skill definitions. The user requested the defect record without naming the exact canonical skill paths, so implementation requires path-specific approval.

### Options and Tradeoffs

- Approve both paths: move the defect to the active defect backlog as Ready and correct the complete cross-skill workflow.
- Approve only one named path: narrow the manifest, accepting that the other skill may remain less explicit.
- Defer: move the defect to Holding and retain the current split wording.
- Decline: archive the defect as abandoned and retain the ambiguity as an accepted risk.

### Resolution

Approved on 2026-08-13. The user explicitly approved changing both governed canonical paths, `skills/manage-work-items-file/SKILL.md` and `skills/create-work-item-file/SKILL.md`, with focused tests.

### Unattended Work Boundary

Do not modify either governed skill definition or its focused contract tests until the user approves the exact manifest. Read-only discovery and review of the current workflow may continue.

## User Action Resolution Evidence

- Transition: User Action Required -> Ready.
- Resolution: Both governed paths and focused tests are approved exactly as listed in Governed Definition Approval.
- Approval Provenance: Direct user instruction on 2026-08-13.
- Next Action: Schedule through ordinary priority and capacity after current Starting reservations are reconciled.
- Transition Claim: `resolve-discovered-defect-routing-uar-019ff2c3`; outcome `SHARED_CHECKOUT_ACQUIRED`; event `9d85eaa9-1345-4cec-9fa7-95d94d05a5a8`.

## Starting Handoff Evidence

- Reserved At: 2026-08-13T06:40:07Z.
- Transition: `Ready -> Starting`.
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Coordinator Execution: `/root/backlog_coordinator`.
- Baseline: `6b7ca5546d416ad82fc06bea15b62be2d22c065d` on primary `main`.
- Priority: Oldest eligible independent Ready process-correctness defect. It improves durable defect routing and has no series dependency.
- Overlap: Exact governed sources and focused tests do not overlap the preserved User Action Required candidate. The four untracked plan artifacts remain excluded.
- Dispatch Architecture: Create one user-visible Codex task whose initial reference-plus-delta prompt starts one Dev Orchestrator collaboration subagent for this provider record.
- Transition Claim: `start-clarify-discovered-defect-routing-019ff2c3`; outcome `SHARED_CHECKOUT_ACQUIRED`; event `5d9d0cd7-6333-462f-9c4f-8aa7ab51437c`.
- Next Reconciliation: Adopt the exact visible task identity. Its nested Dev Orchestrator records Starting -> Running before mutation.

## Canonical Runtime Assignment

- Assigned At: 2026-08-13T06:41:05Z.
- Codex Task ID: `019ff9da-3110-7022-86b1-e10cc6f0ece8`.
- Conversation ID: `019ff9da-3110-7022-86b1-e10cc6f0ece8`.
- Host: `local`.
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Requested Title: `Starting — Clarify Discovered Defect Routing`.
- Initial Action: Start one Dev Orchestrator collaboration subagent for this authoritative provider record.
- Creation Outcome: Unique success with no pending client identity and no retry.
- Lifecycle Boundary: This assignment remains Starting until the nested Dev Orchestrator accepts and records Starting -> Running.
