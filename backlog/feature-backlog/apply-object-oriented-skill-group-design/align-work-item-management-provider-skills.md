# Align Work-Item Management Provider Skills

Status: Running

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/apply-object-oriented-skill-group-design/align-work-item-management-provider-skills.md

Owner: Dev Orchestrator

Completion: direct-main

Series: backlog/feature-backlog/apply-object-oriented-skill-group-design/index.md

## Current Dispatch Reservation

Transition: Ready -> Starting.
Parent Coordination Thread: /root/apply_skill_group_design_backlog.
Launch Reservation: One distinct bounded launch reservation for this provider record.
Normalized Objective: Align the work-item management provider skills with the approved object-oriented design and update their individual evaluations.
Dispatch Time: 2026-08-05T03:43:54Z.
Intended Root Dev Orchestrator Role: Dev Orchestrator.
Owner: Unowned pending accepted root.
Current Launch Evidence: Parent Coordinator authorized this exact reservation; exact-file backlog claim reserve-align-work-item-management-provider-skills acquired with outcome SHARED_CHECKOUT_ACQUIRED and event d2288904-dc02-4f48-a39c-31f2fff4be8f. Runtime Thread creation and root acceptance have not occurred.
Required Next Lifecycle Transition: The root Dev Orchestrator must separately accept Starting -> Running before repository mutation.
Reconciliation: Root acceptance recorded separately below; the parent reservation remains preserved.

## Current Running Acceptance

Transition: Starting -> Running.
Canonical Thread: /root/apply_skill_group_design_backlog/align_work_item_management_providers.
Root Agent Task: /root/apply_skill_group_design_backlog/align_work_item_management_providers.
Owner: Dev Orchestrator.
Branch: codex/align-work-item-management-providers-019fab.
Worktree: /Users/martinbechard/dev/dev-methodology/.worktrees/align-work-item-management-providers-019fab.
Phase: Implementation acceptance / definition-precheck preparation.
Started At: 2026-08-05T03:48:08Z.
Claim Evidence: The private delivery lane was claim-free immediately before this acceptance. This exact primary-main backlog mutation is protected by exact-file claim running-align-work-item-management-provider-skills-019fab, acquired with outcome SHARED_CHECKOUT_ACQUIRED and event 32f2db9e-61a7-4b0e-a133-d896841fb4bf.
Preserved Coordination: Parent Coordination Thread /root/apply_skill_group_design_backlog and its Ready -> Starting launch reservation remain canonical.

## Summary

Align all five work-item management providers on Inventory Work Items, Transition Work Item, Reconcile Work Item Completion, Recover Work Item, and Report Work Items while preserving provider-specific lifecycle behavior.

## Context

The Backlog Management proposal treats the five management skills as provider implementations selected through project routing. They need the same public procedure vocabulary, but file, GitHub, GitLab, Azure DevOps, and Jira retain distinct authority, lookup, lifecycle, recovery, and availability rules.

## Source Evidence

The user directed in the active Codex task on 2026-08-04: "create separate work items to update skills according to the new design, and update individual evals." The exact provider recommendations are in design/skill-groups/backlog-management.md at reviewed baseline commit c426c970153948f9d5d2d92f1b7b718613a8d4f7.

## Requirements

- Introduce the same five public operation headings in every provider.
- Preserve each provider's native lookup, state, recovery, authority, result, and ambiguous-outcome rules.
- Route unsupported Azure DevOps and Jira operations to their truthful blocked result without pretending successful lifecycle support.
- Align common input and result terms only where provider semantics remain equivalent.
- Add individual evaluation coverage for every provider and every public procedure, using representative cases rather than only name-presence checks.

## Acceptance Criteria

- Every provider exposes the same five procedure names.
- Supported providers retain correct technology-specific lifecycle behavior, and unsupported providers retain truthful blocked behavior.
- AGENTS.md selection can refer to provider-neutral management procedures without requiring one provider to know another.
- Individual evaluations cover inventory, transition, reconciliation, recovery, and reporting across the provider family.
- Generated mirrors, catalogs, and focused tests are fresh and passing.

## Dependencies

None.

## Verification

- Run the supported definition-change precheck for all five governed paths.
- Run every provider's focused probe and provider fixture or contract tests.
- Run scripts/test_agent_skill_evals.py, scripts/test_eval_coverage_catalog.py, scripts/test_bundle_content.py, and generated-output freshness checks.
- Compare all five headings, inputs, results, and unsupported-operation behavior.
- Run git diff --check and obtain independent methodology review and verification.

## Open Questions

Determine which shared data members can be named consistently without weakening a provider's native lifecycle constraints.

## Governed Definition Approval

### Governed Canonical Sources

- skills/manage-file-work-items/SKILL.md
- skills/manage-github-work-items/SKILL.md
- skills/manage-gitlab-work-items/SKILL.md
- skills/manage-azure-devops-work-items/SKILL.md
- skills/manage-jira-work-items/SKILL.md

### Allowed Dependent Artifacts

- approval-record-align-work-item-management-provider-skills.yaml
- evals/skill-probes.yaml
- evals/cases.yaml
- evals/workflow-packs.yaml
- evals/agent-tests/dev-backlog-steward
- evals/agent-tests/dev-backlog-coordinator
- scripts/test_github_work_item_provider_fixture.py
- scripts/test_generate_backlog_report.py
- scripts/test_agent_skill_evals.py
- scripts/test_eval_coverage_catalog.py
- scripts/test_bundle_content.py
- README.md
- design/agent-and-skill-definitions.html
- design/agent-and-skill-evaluations.html
- design/generated/skill-definitions.js
- generated/adapters files regenerated from only the approved canonical sources
- Directly related non-governed documentation, provider fixtures, and focused tests required to keep these approved definitions coherent

### Approval Resolution

Approved at creation on 2026-08-04 by the user statement in the active Codex task: "create separate work items to update skills according to the new design, and update individual evals." Approval is limited to the five governed canonical paths listed above. Any additional governed definition requires new explicit user approval recorded in this item.

### Preserved Approval-Evidence Correction

The prior approval-evidence correction remains in force. The existing approval record and its five-path governed-source manifest remain the sole authority for the bounded correction below; no new governed path or definition authority is inferred.

## Independent Review Defect and Correction Attempt 2

Lifecycle: Running unchanged.

Canonical Thread and Root Agent Task: /root/apply_skill_group_design_backlog/align_work_item_management_providers.

Owner: Dev Orchestrator.

Branch and Worktree: codex/align-work-item-management-providers-019fab at /Users/martinbechard/dev/dev-methodology/.worktrees/align-work-item-management-providers-019fab.

Review Verdict: CHANGES REQUIRED.

Defect Severity: Medium, independently confirmed.

Defect Evidence:

- skills/manage-azure-devops-work-items/SKILL.md line 38 requires an exact canonical operation token, but line 56 uses the contradictory example Requested operation: close.
- skills/manage-jira-work-items/SKILL.md line 38 requires an exact canonical operation token, but line 56 uses the contradictory example Requested operation: transition.

Reproduction:

```text
rg -n '^## (Inventory Work Items|Transition Work Item|Reconcile Work Item Completion|Recover Work Item|Report Work Items)$|Requested operation:' skills/manage-azure-devops-work-items/SKILL.md skills/manage-jira-work-items/SKILL.md
```

Preserved Candidates:

- Superseded candidate: 08542a3eb9e3870ec937a6986e83825ad8160a27.
- Current preserved candidate: c34f2a899411721c48a385e342d57e850b44491c.

Correction Assignment: Original Dev Coder, correction attempt 2 of 2.

Runnable Next Action: Replace the examples with matching canonical tokens, add negative regression assertions, regenerate design/generated/skill-definitions.js, rerun the affected scalar definition and regeneration checks plus focused tests, then obtain fresh review.

## User Action Required

Transition: Running -> User Action Required.

Ownership: The canonical root Dev Orchestrator and its Thread are preserved for same-Thread resumption. No unattended direct-main integration or provider-completion action is authorized while this item is in User Action Required.

Question: Please make design/object-oriented-agent-and-skill-model.md clean in the primary main checkout without us touching your edit, then tell us to resume; alternatively, do you explicitly authorize a scoped preservation/clean/restore procedure for that one edit?

Why Input Is Required: Completion is configured as direct-main, and complete-work-item-direct-main cannot mutate configured main while the primary checkout contains the explicitly protected user-owned modification to design/object-oriented-agent-and-skill-model.md. The user must either make that file clean without agent changes or grant the limited preservation, clean, and restore authority.

Unattended Boundary: No primary-main mutation, main-integration claim, Commit READY, or terminal provider closure is authorized. Other private work may continue.

Resolution: Answered on 2026-08-05 in the parent coordination Thread /root/apply_skill_group_design_backlog. The user authorized committing all remaining document changes. Primary main is clean at 90f68d037d345da896a476dbd43f83dcaa3b3bae, containing the formerly protected design/object-oriented-agent-and-skill-model.md change only, and that project's project-files claim was released.

## User Action Required Resolution

Transition: User Action Required -> Ready.

Recorded Answer and Provenance: Answered on 2026-08-05 in the parent coordination Thread /root/apply_skill_group_design_backlog. The user authorized committing all remaining document changes. Primary main is clean at 90f68d037d345da896a476dbd43f83dcaa3b3bae, containing the formerly protected design/object-oriented-agent-and-skill-model.md change only, and that project's project-files claim was released.

Disposition: The direct-main cleanliness condition is satisfied. This item returns to its typed series folder as Ready with Owner Unowned. The existing canonical Thread /root/apply_skill_group_design_backlog/align_work_item_management_providers and Root Agent Task remain preserved; no Starting reservation or Running acceptance is created by this provider transaction.

## Current Resumption Dispatch Reservation

Transition: Ready -> Starting.
Parent Coordination Thread: /root/apply_skill_group_design_backlog.
Launch Reservation: One distinct bounded resumption reservation for the preserved canonical work-item Thread.
Normalized Objective: Align the work-item management provider skills with the approved object-oriented design and update their individual evaluations.
Dispatch Time: 2026-08-05T14:35:08Z.
Intended Root Dev Orchestrator Role: Dev Orchestrator.
Canonical Thread: /root/apply_skill_group_design_backlog/align_work_item_management_providers.
Canonical Root Agent Task: /root/apply_skill_group_design_backlog/align_work_item_management_providers.
Owner: Unowned pending accepted root.
Current Launch Evidence: Coordinator-authorized resumption reservation recorded under exact-file claim reserve-resumed-management-provider-019fb1, acquired with outcome SHARED_CHECKOUT_ACQUIRED and event 9a77a464-d691-4f0b-8c83-3f00c3c73775.
Required Acknowledgement: The preserved canonical root Dev Orchestrator must acknowledge this exact reservation and separately record Starting -> Running with the same canonical identities before further repository mutation. Do not create a replacement Thread.

## Current Resumption Running Acceptance

Transition: Starting -> Running.
Canonical Thread: /root/apply_skill_group_design_backlog/align_work_item_management_providers.
Root Agent Task: /root/apply_skill_group_design_backlog/align_work_item_management_providers.
Owner: Dev Orchestrator.
Branch: codex/align-work-item-management-providers-019fab.
Worktree: /Users/martinbechard/dev/dev-methodology/.worktrees/align-work-item-management-providers-019fab.
Phase: Resumed direct-main current-main reconciliation.
Started At: 2026-08-05T14:38:53Z.
Claim Evidence: Exact-file primary-main claim running-resumed-management-provider-019fb1 acquired with outcome SHARED_CHECKOUT_ACQUIRED and event ff379abe-4d79-4c56-8aed-a7849f7230c5. Claim status immediately before acquisition reported only unrelated sticky-navigation browser-server and database-port resource claims; neither overlaps this backlog record or the private source and integration lanes.
Preserved Delivery Evidence: Source candidate 1ce2f98cce8d7ee2ca498a7507f422d802ea3166 is clean and independently reviewed PASS and verified PASS. The five exact governed-definition prechecks and five required regeneration checks passed. Exact-path integration commit db58d7130d3e7c06979d7f963bb44b967f15e622 is retained in clean reconciled integration head 230bdba3d6545f7ec0c3c7426f2c77c4c31ca891. Correction history and confirmed defect record remain preserved.
Preserved Coordination: Parent Coordination Thread /root/apply_skill_group_design_backlog and its Ready -> Starting resumption reservation remain canonical. No replacement Thread was created.

## Preserved Delivery Evidence

Canonical Thread and Root Agent Task: /root/apply_skill_group_design_backlog/align_work_item_management_providers.

Accepted Source Candidate: 1ce2f98cce8d7ee2ca498a7507f422d802ea3166.

Independent Review: PASS.

Verification: PASS.

Definition Checks: 5/5 exact governed-definition prechecks passed; 5/5 required regeneration checks passed.

Correction History: Two correction attempts completed.

Exact-Path Integration Commit: db58d7130d3e7c06979d7f963bb44b967f15e622.

Reconciled Clean Head: 230bdba3d6545f7ec0c3c7426f2c77c4c31ca891, with the integration commit and then-current main as ancestors.

Worktree Evidence: The source and integration worktrees are clean.

Claim Evidence: Before this provider transaction, claim status returned STATUS with no live claims. This transition is protected by exact-file claim uar-align-work-item-management-provider-skills-019fab, acquired with outcome SHARED_CHECKOUT_ACQUIRED and event c471fd95-f7c1-4039-a067-212013d506f1.

Safe Resumption: Preserve the canonical Thread, root Agent Task, source candidate, review, verification, integration evidence, and the user-owned primary-main diff. After the user answers, record the answer once and move this item to Ready in its typed active folder. The parent Coordinator must then reserve Ready -> Starting on this same Thread, and its root Dev Orchestrator must accept Starting -> Running before further repository mutation. Do not create a replacement Thread while this canonical identity remains valid.
