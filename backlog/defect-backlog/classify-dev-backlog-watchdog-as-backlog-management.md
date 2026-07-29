# Classify Dev Backlog Watchdog As Backlog Management

Status: Running

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/classify-dev-backlog-watchdog-as-backlog-management.md

Completion: direct-main

## Summary

Classify Dev Backlog Watchdog under Backlog Management everywhere the generated conceptual-agent catalog and agent-to-skill hierarchy present agent categories.

## Context

design/role-catalog-groups.yaml defines Backlog Management as a presentation category and currently overrides Dev Backlog Coordinator and Dev Backlog Steward into it. Dev Backlog Watchdog remains assigned to the Dev Activities catalog category even though its entire responsibility is scheduled, read-only observation of backlog coordination.

The catalog grouping is intentionally separate from the conceptual source directory. The Watchdog definition remains agents/roles/dev-activities/dev-backlog-watchdog.role.yaml, while presentation metadata determines the category shown in generated cards and the hierarchy.

## Source Evidence

Direct user request in Codex task 019fae77-d530-7361-b1c6-36f87f3d6e28 on 2026-07-29: "dev-backlog-watchdog should be part of backlog management category".

Repository evidence confirms that design/role-catalog-groups.yaml has Backlog Management overrides for Dev Backlog Coordinator and Dev Backlog Steward but no override for Dev Backlog Watchdog. The generated role data consequently reports the Watchdog catalog group as Dev Activities.

## Requirements

- Add Dev Backlog Watchdog to the Backlog Management presentation category in design/role-catalog-groups.yaml.
- Cite agents/roles/dev-activities/dev-backlog-watchdog.role.yaml as the source and record evidence that the role observes backlog lifecycle, capacity, coordination, stalls, blockers, and crisis conditions.
- Preserve the governed conceptual definition at agents/roles/dev-activities/dev-backlog-watchdog.role.yaml unchanged.
- Regenerate the role catalog data so Dev Backlog Watchdog has catalogGroup backlog-management and the Backlog Management display label.
- Regenerate the agent-to-skill hierarchy so Dev Backlog Watchdog appears in the Backlog Management group.
- Remove Dev Backlog Watchdog from the Dev Activities presentation group without changing its identity, skills, dependencies, model profile, mutation policy, examples, or outputs.
- Keep the cards and hierarchy consistent with the ordered group contract in design/agent-and-skill-definitions.outline.md when that outline is present.
- Update focused tests so the Backlog Management membership contract includes Dev Backlog Coordinator, Dev Backlog Steward, and Dev Backlog Watchdog.
- Add a negative assertion that generated catalog and hierarchy output do not classify Dev Backlog Watchdog under Dev Activities.

## Acceptance Criteria

- The Conceptual Agent Definitions cards show Dev Backlog Watchdog under Agents for Backlog Management.
- Dev Backlog Watchdog does not appear under Agents for Dev Activities.
- The generated agent-to-skill hierarchy places Dev Backlog Watchdog in the Backlog Management group.
- Generated role data reports backlog-management as the Watchdog catalog group while retaining dev-activities as its conceptual source group.
- The Watchdog's governed conceptual definition is byte-for-byte unchanged.
- Generated catalog and hierarchy freshness checks pass.
- Focused regression coverage fails if the Watchdog returns to the Dev Activities presentation category.

## Dependencies

None.

## Verification

- Run focused role-catalog grouping tests for all three Backlog Management agents.
- Run scripts/build-skill-docs.py and scripts/build-agent-skill-hierarchy.py with their freshness checks.
- Run directly affected bundle-content and hierarchy tests.
- Compare the Watchdog's governed conceptual definition before and after implementation and require no change.
- Verify the Watchdog card and hierarchy group in the rendered documentation.
- Run git diff validation for the implementation change.

## Open Questions

None.

## Notes

## Current Dispatch Reservation (Fresh Settlement)

Transition: Ready -> Starting.
Parent Coordination Thread: 019faeef-c808-7a62-a004-15f9986d7b14.
Launch Reservation: One bounded resume reservation for the same canonical conversation.
Normalized Objective: Classify Dev Backlog Watchdog as Backlog Management.
Dispatch Time: 2026-07-29T17:40:10Z.
Intended Root Role: Root Dev Orchestrator.
Canonical Conversation and Root Agent Task: 019faeef-c808-7a62-a004-15f9986d7b14.
Direct Conversation-Title Handoff: Classify Dev Backlog Watchdog As Backlog Management.
Branch: codex/classify-dev-backlog-watchdog-as-backlog-management-019faeef.
Worktree: /Users/martinbechard/.codex/worktrees/5569/dev-methodology.
Owner: Unowned pending accepted root.
Required Next Lifecycle Transition: The same root Dev Orchestrator must separately accept Starting -> Running before repository mutation.
Reconciliation: Pending.

## Starting Settlement Evidence (Fresh Settlement)

Settlement Window: 2026-07-29T17:40:10Z to 2026-07-29T17:41:10Z (exactly 60 seconds).
Runtime Launch Result: Direct conversation-title handoff accepted for resume.
Canonical Conversation: 019faeef-c808-7a62-a004-15f9986d7b14.
Owner Acceptance: Pending.
Reconciliation: Pending.

## Active Execution Evidence (Fresh Settlement)

Transition: Starting -> Running.

Parent Coordinator Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758.

Canonical Thread: 019faeef-c808-7a62-a004-15f9986d7b14.

Root Agent Task: 019faeef-c808-7a62-a004-15f9986d7b14.

Root Role: Dev Orchestrator.

Owner: Root Dev Orchestrator.

Branch: codex/classify-dev-backlog-watchdog-as-backlog-management-019faeef.

Worktree: /Users/martinbechard/.codex/worktrees/5569/dev-methodology.

Current Phase: Running with implementation pending.

Started At: 2026-07-29T17:41:00.844573Z (Root Dev Orchestrator acceptance before the 2026-07-29T17:41:10Z settlement deadline).

Starting Baton: 51614217ca85fe51216e6a9afb9b8cfd1fc472c6 on primary main.

Claim Evidence: starting-running-019faeef acquired as SHARED_CHECKOUT_ACQUIRED at 2026-07-29T17:42:39.244259Z; claim incarnation 86a53498-eba7-472d-ba45-364515f14acf; claim journal event a8a2c4f6-0b56-44af-9a37-fc5b9d2ff3f8.

Reconciliation: Starting -> Running recorded by Dev Backlog Steward on primary main.

## Missed-Settlement Reconciliation

Transition: Starting -> Ready.
Reconciled At: 2026-07-29T17:38:47Z.
Settlement Deadline: 2026-07-29T17:36:38Z.
Canonical Conversation and Root Agent Task: 019faeef-c808-7a62-a004-15f9986d7b14.
Owner: Unowned.
Canonical Acceptance: None observed.
Source Mutation Evidence: None observed.
Required Resumption: Reuse the same canonical task through a new Ready -> Starting -> Running sequence.
Reconciliation: Ready.

## Current Dispatch Reservation

Transition: Ready -> Starting.
Parent Coordination Thread: 019faeef-c808-7a62-a004-15f9986d7b14.
Launch Reservation: One synchronized bounded launch reservation in the adaptive-capacity batch.
Normalized Objective: Classify Dev Backlog Watchdog as Backlog Management.
Dispatch Time: 2026-07-29T17:35:38Z.
Intended Root Role: Root Dev Orchestrator.
Canonical Conversation and Root Agent Task: 019faeef-c808-7a62-a004-15f9986d7b14.
Direct Conversation-Title Handoff: Classify Dev Backlog Watchdog As Backlog Management.
Branch: codex/classify-dev-backlog-watchdog-as-backlog-management-019faeef.
Worktree: /Users/martinbechard/.codex/worktrees/5569/dev-methodology.
Owner: Unowned pending accepted root.
Required Next Lifecycle Transition: The same root Dev Orchestrator must separately accept Starting -> Running before repository mutation.
Reconciliation: Pending.

## Starting Settlement Evidence

Settlement Window: 2026-07-29T17:35:38Z to 2026-07-29T17:36:38Z (exactly 60 seconds; shared adaptive-capacity batch window).
Runtime Launch Result: Direct conversation-title handoff accepted for the synchronized batch.
Canonical Conversation: 019faeef-c808-7a62-a004-15f9986d7b14.
Owner Acceptance: Pending.
Reconciliation: Pending.

Coordinate implementation with backlog/defect-backlog/restore-agent-and-skill-definitions-outline-and-diagram.md because both items update presentation grouping or hierarchy sources. This is a source-overlap consideration, not a delivery dependency.
