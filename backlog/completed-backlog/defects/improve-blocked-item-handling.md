# Improve Blocked Item Handling

Status: Completed

Type: Defect

Owner: Dev Backlog Coordinator SOLO crisis task

Provider: file

Work Item ID: improve-blocked-item-handling

Completion: main-branch

## Summary

Make the Dev Backlog Coordinator actively diagnose and recover each ordinary Blocked item instead of treating the Blocked transition as the end of coordination responsibility.

## Context

Current guidance assigns Blocked recovery to the Coordinator, but the normal role boundary against taking over per-item delivery, the exhausted-correction disposition rules, and the provider resumption rules do not form one executable recovery procedure. Existing deterministic coverage can accept a recovery disposition that changes Blocked directly to Running even though the file-provider contract requires Blocked to Ready to Starting to Running. This ambiguity allowed preserved candidates to remain parked after their blockers became agent-actionable.

The requested behavior is that the Coordinator analyzes the concrete blocker, corrects the work item or other authorized files needed to make progress, and restarts the same canonical execution. The root task independently accepts Starting to Running when it can proceed, or records a new truthful Blocked result when it cannot.

## Source Evidence

On 2026-08-09, the user directed that when an item is Blocked, the Coordinator must analyze the reason, correct the work item or make other appropriate file modifications consistent with the original request and standing directives, restart the item at Starting, and let the same task record Running or Blocked. The user then explicitly requested creation of a separate work item for “improve blocked item handling.”

## Requirements

- Define one mandatory ordinary Blocked-entry recovery procedure owned by Dev Backlog Coordinator.
- Require current evidence review of the blocker, preserved candidate, canonical task, worktree, review and verification findings, dependencies, claims, and acceptance criteria before choosing a disposition.
- Require the Coordinator to correct stale, contradictory, over-scoped, or incomplete work-item content and to perform other authorized supporting-file corrections needed to make the original requested outcome runnable.
- Keep technical investigation and mechanical recovery Coordinator-owned. Do not convert ordinary uncertainty or Coordinator inexperience into a user obligation without first completing bounded diagnosis.
- Move to User Action Required only when diagnosis isolates one concrete user-owned decision, authority grant, action, risk acceptance, or fact. Record the exact question and synchronize the canonical task title to a Waiting for User form.
- Preserve the existing canonical execution, candidate history, review and verification evidence, Git state, and worktree whenever safe resumption is possible.
- Resume through Blocked to Ready to Starting. Prohibit direct Blocked to Running transitions.
- Require the preserved root Dev Orchestrator to independently record Starting to Running when capable of proceeding, or record a new Blocked handoff with current cause and evidence when it cannot.
- Keep the Coordinator responsible for the recovery result until the task has accepted Running, returned a new Blocked result, entered User Action Required, or reached a justified terminal disposition.
- Keep ordinary Blocked recovery distinct from declared backlog crisis recovery.

## Acceptance Criteria

- One coherent state machine defines ordinary Blocked diagnosis, correction, restart, task acceptance, repeated blockage, user escalation, and terminal disposition.
- Agent-actionable blockers result in a concrete correction or recovery action rather than indefinite Blocked storage.
- Technical uncertainty alone cannot produce User Action Required.
- A genuine user-owned decision produces a complete User Action Required record and a synchronized Waiting for User task title.
- A recoverable item follows Blocked to Ready to Starting before the same canonical task can record Running.
- A task that cannot resume records Blocked with a current exact cause, owner, evidence, and observable unblock condition.
- Preserved candidates and accepted gates are reused where valid instead of being discarded or rerun indiscriminately.
- Deterministic tests reject direct Blocked to Running, replacement canonical tasks, vague recovery outcomes, lifecycle-only churn, and false user escalation.

## Dependencies

None.

## Verification

- Add focused Dev Backlog Coordinator scenarios for agent-actionable recovery, work-item correction, same-task restart, genuine user escalation, and failed resumption.
- Extend the coordination simulator and its tests to enforce Blocked to Ready to Starting to Running or Blocked.
- Add bundle assertions for the authoritative skill and role clauses.
- Run the focused Dev Backlog Coordinator suite, file-provider lifecycle tests, role and skill validation, generated-adapter freshness checks, and `git diff --check`.
- Obtain fresh independent skill, role, and prompt-contract review.

## Open Questions

- Determine the smallest durable recovery receipt that proves the Coordinator corrected the blocker without duplicating provider lifecycle evidence.

## Governed Definition Approval

### Governed Canonical Sources

- skills/coordinate-work-items/SKILL.md
- skills/manage-work-items-file/SKILL.md
- agents/roles/dev-activities/dev-backlog-coordinator.role.yaml

### Allowed Dependent Artifacts

- evals/agent-tests/dev-backlog-coordinator/scenarios.yaml
- evals/agent-tests/dev-backlog-coordinator/requirements-matrix.md
- evals/agent-tests/dev-backlog-coordinator/fixtures/cases.yaml
- evals/agent-tests/dev-backlog-coordinator/coordination_simulator.py
- evals/agent-tests/dev-backlog-coordinator/test_coordination_simulator.py
- scripts/test_bundle_content.py
- design/agents/backlog-management.md
- design/agents/work-item-dispatching-and-delivery.md
- design/generated/role-definitions.js
- generated/adapters files regenerated from the approved canonical sources
- Directly related non-governed focused tests and generated projections required to keep these definitions coherent

### Approval Resolution

Approved at creation. User wording on 2026-08-09 required clearer Backlog Coordinator guidance for Blocked analysis, authorized corrective file work, same-task restart through Starting, truthful Running or Blocked acceptance, and exact user escalation when a genuinely user-owned decision remains. Approval is limited to the governed canonical paths listed above; an additional governed definition path requires separately recorded scope-specific approval.

## Completion Evidence

- Delivered on authoritative main in commit `02fc4883`.
- Added the mandatory ordinary Blocked recovery state machine, Coordinator-owned diagnosis and authorized correction, same-task preservation, exact User Action Required boundary, and serialized `Blocked -> Ready -> Starting -> Running|Blocked` resumption.
- Deterministic Coordinator tests passed 28/28; Watchdog tests passed 31/31; bundle tests passed 174/174; four affected skill validators, generated freshness, Python compilation, Ruff, and `git diff --check` passed.
- The two recovery-policy defects were implemented together because they share the Coordinator role and generated projections; this record is archived independently after terminal verification.
