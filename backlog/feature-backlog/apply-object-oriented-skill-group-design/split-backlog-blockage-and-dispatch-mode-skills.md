# Split Backlog Blockage And Dispatch-Mode Skills

Status: Blocked

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/apply-object-oriented-skill-group-design/split-backlog-blockage-and-dispatch-mode-skills.md

Completion: direct-main

Series: backlog/feature-backlog/apply-object-oriented-skill-group-design/index.md

## Current Dispatch Reservation

Transition: Ready -> Starting.
Parent Coordination Thread: /root/apply_skill_group_design_backlog.
Launch Reservation: One distinct bounded launch reservation for this provider record.
Normalized Objective: Split backlog blockage and dispatch-mode skills according to the approved object-oriented design and update their individual evaluations.
Dispatch Time: 2026-08-05T03:44:21Z.
Intended Root Dev Orchestrator Role: Dev Orchestrator.
Owner: Unowned pending accepted root.
Current Launch Evidence: Parent Coordinator authorized this exact reservation; exact-file backlog claim reserve-split-backlog-blockage-and-dispatch-mode-skills acquired with outcome SHARED_CHECKOUT_ACQUIRED and event a0c275eb-5663-4ae8-a6f8-652c448390df. Runtime Thread creation and root acceptance have not occurred.
Required Next Lifecycle Transition: The root Dev Orchestrator must separately accept Starting -> Running before repository mutation.
Reconciliation: Accepted by the canonical root Dev Orchestrator below.

## Current Delivery Ownership

Transition: Starting -> Running.
Canonical Work-Item Thread: /root/apply_skill_group_design_backlog/split_backlog_blockage_dispatch_modes.
Canonical Root Agent Task: /root/apply_skill_group_design_backlog/split_backlog_blockage_dispatch_modes.
Root Dev Orchestrator Owner: /root/apply_skill_group_design_backlog/split_backlog_blockage_dispatch_modes.
Branch: codex/split-backlog-blockage-dispatch-modes-019fab.
Worktree: /Users/martinbechard/dev/dev-methodology/.worktrees/split-backlog-blockage-dispatch-modes-019fab.
Phase: Accepted delivery ownership; implementation not started.
Started At: 2026-08-05T03:49:54Z.
Claim Evidence: Private-worktree delivery is claim-free by the configured Event Contract; live claim status was STATUS with empty claims before acceptance. The primary-main provider mutation is protected separately by exact-file claim running-split-backlog-blockage-and-dispatch-mode-skills, acquired with outcome SHARED_CHECKOUT_ACQUIRED and event 97c44759-9614-4eeb-8218-b5d0dd694047.
Accepted Ownership Evidence: The canonical root Dev Orchestrator explicitly accepted this Starting -> Running transition after parent reservation commit 86828daf.

## Summary

Replace backlog-crisis-mode with resolve-backlog-blockage and extract set-solo-mode and set-multitask-mode as complementary Concurrent Tasking skills that disable or enable dispatch to secondary threads.

## Context

The approved design separates backlog-specific blockage analysis from concurrency policy. resolve-backlog-blockage owns declaration, blocked-item recovery, watchdog behavior, and result. set-solo-mode disables secondary-thread dispatch, and set-multitask-mode enables it. Dev Backlog Coordinator assembles the sequence by condition; the three sibling skills do not need to name one another. Backlog blockage recovery must remain usable when Concurrent Tasking is not configured.

## Source Evidence

The user explicitly directed the split earlier in the active design task and on 2026-08-04 requested separate implementation work items and individual evals. The exact approved responsibilities are in design/skill-groups/backlog-management.md, design/skill-groups/concurrent-tasking.md, and the proposal registry at reviewed baseline commit c426c970153948f9d5d2d92f1b7b718613a8d4f7.

## Requirements

- Rename the retained blockage procedure and skill to resolve-backlog-blockage.
- Extract exactly two new skill packages: set-solo-mode and set-multitask-mode.
- Keep dispatch control limited to enabling or disabling dispatch to secondary threads; do not make either skill own backlog diagnosis or lifecycle mutation.
- Update Dev Backlog Coordinator and Dev Backlog Watchdog references and conditions without creating direct sibling-skill dependencies.
- Preserve correct behavior when no secondary-thread dispatch mechanism is configured.
- Add individual evaluations for all three resulting skills and Agent scenarios for entry, continued solo work, recovery, and resumption.

## Acceptance Criteria

- backlog-crisis-mode is no longer a live skill identity.
- resolve-backlog-blockage contains only the retained backlog responsibility.
- set-solo-mode and set-multitask-mode are independently loadable, complementary, and do not overlap blockage diagnosis.
- Agent instructions clearly state when each skill is loaded and do not require dispatch-mode skills when concurrency is absent.
- Focused evaluations distinguish blockage resolution from both dispatch-mode changes and cover safe idempotent handling.
- Generated mirrors, catalogs, and focused suites are fresh and passing.

## Dependencies

None.

## Verification

- Run the supported definition-change precheck for every governed canonical path below.
- Run individual probes for all three resulting skills and focused Dev Backlog Coordinator and Dev Backlog Watchdog suites.
- Run scripts/test_agent_skill_evals.py, scripts/test_eval_coverage_catalog.py, scripts/test_bundle_content.py, and generated-output freshness checks.
- Search maintained sources for stale backlog-crisis-mode references and direct sibling-skill coupling.
- Run git diff --check and obtain independent methodology review and verification.

## Open Questions

Determine the smallest stable result evidence that proves dispatch was disabled or enabled without making the skill depend on one runtime's task API.

## Governed Definition Approval

### Governed Canonical Sources

- skills/backlog-crisis-mode/SKILL.md
- skills/backlog-crisis-mode/agents/openai.yaml
- skills/resolve-backlog-blockage/SKILL.md
- skills/resolve-backlog-blockage/agents/openai.yaml
- skills/set-solo-mode/SKILL.md
- skills/set-solo-mode/agents/openai.yaml
- skills/set-multitask-mode/SKILL.md
- skills/set-multitask-mode/agents/openai.yaml
- agents/roles/dev-activities/dev-backlog-coordinator.role.yaml
- agents/roles/dev-activities/dev-backlog-watchdog.role.yaml

### Allowed Dependent Artifacts

- approval-record-split-backlog-blockage-and-dispatch-mode-skills.yaml
- evals/skill-probes.yaml
- evals/cases.yaml
- evals/workflow-packs.yaml
- evals/agent-tests/dev-backlog-coordinator
- evals/agent-tests/dev-backlog-watchdog
- README.md
- design/agent-and-skill-definitions.html
- design/agent-and-skill-evaluations.html
- design/generated/skill-definitions.js
- design/generated/role-definitions.js
- generated/adapters files regenerated from only the approved canonical sources
- scripts/test_agent_skill_evals.py
- scripts/test_eval_coverage_catalog.py
- scripts/test_bundle_content.py
- Directly related non-governed documentation, fixtures, and focused tests required to keep these approved definitions coherent

### Approval Resolution

Approved at creation on 2026-08-04 by the user's explicit prior split direction and the current request to create implementation work items for the new design and individual evals. The reviewed diagrams show the three exact resulting skill identities and the two exact Agent definitions covered here. Approval is limited to the governed canonical paths listed above. Any additional governed definition requires new explicit user approval recorded in this item.

## Review Defect Evidence

Reviewer: /root/apply_skill_group_design_backlog/split_backlog_blockage_dispatch_modes/review_split_candidate.

Verdict: FAIL.

Delivery Under Review: Candidate 62a32992b0572f7d60dc55dc3eeea470d6c794aa on branch codex/split-backlog-blockage-dispatch-modes-019fab in worktree /Users/martinbechard/dev/dev-methodology/.worktrees/split-backlog-blockage-dispatch-modes-019fab.

Confirmed Finding: The candidate removes the live backlog-crisis-mode identity, but the unchanged generated design/agent-skill-test-coverage-checklist.md blob 47d4dd066a1764538960c842b06ffba973c38b16 still presents backlog-crisis-mode as live or missing-probe at lines 26, 151, and 318. The identical base and candidate checklist is therefore semantically false after the candidate changes the inventory, violating the stale-identity and catalog-freshness acceptance criteria.

Reproduction: python3 scripts/build-support-checklist.py --check and /opt/homebrew/bin/python3.11 -m unittest scripts.test_eval_coverage_catalog fail identically at base 6f45b362 and at the candidate, reporting four unknown dev-document-topic-editor Judge checks. The generated checklist must not be edited by hand.

Scope And Recovery: At the time this review evidence was recorded, Status remained Running and the canonical work-item Thread remained unchanged. The missing dev-document-topic-editor Judge checks and generator infrastructure are outside this item's governed scope. A separately authorized owner must supply those four checks, then refresh the candidate with python3 scripts/build-support-checklist.py on current main, rerun both freshness commands, and obtain fresh review and verification. The unblock condition is a supported generator run that succeeds on current main and removes the stale identity.

## Blocked Handoff

Transition: Running -> Blocked.

Owner: Unowned.

Coordinator Decision Owner: /root/apply_skill_group_design_backlog.

Canonical Thread and Root Agent Task: /root/apply_skill_group_design_backlog/split_backlog_blockage_dispatch_modes.

Preserved Delivery Identity: Branch codex/split-backlog-blockage-dispatch-modes-019fab; worktree /Users/martinbechard/dev/dev-methodology/.worktrees/split-backlog-blockage-dispatch-modes-019fab; candidate 62a32992b0572f7d60dc55dc3eeea470d6c794aa.

Known Technical Blocker: Candidate 62a32992b0572f7d60dc55dc3eeea470d6c794aa correctly changes the live inventory, but the unchanged generated design/agent-skill-test-coverage-checklist.md is semantically stale at lines 26, 151, and 318. The supported generator fails on four unknown dev-document-topic-editor Judge checks: authority-present, semantic-preservation, source-unchanged, and topic-coverage.

Blocker Owner: Missing-check/generator infrastructure outside this item's authority.

Coordinator-Requested Recovery Action: The Coordinator must obtain separately authorized work that registers or corrects those four checks. This item must not modify the generator infrastructure or create a separate defect item because the dependency is technical and has a known recovery owner.

Observable Unblock Condition: The separately authorized work registers or corrects those four checks; current main successfully runs python3 scripts/build-support-checklist.py, python3 scripts/build-support-checklist.py --check, and /opt/homebrew/bin/python3.11 -m unittest scripts.test_eval_coverage_catalog; then the preserved candidate is rebased or refreshed and receives fresh independent review and verification.

Preserved Evidence: Defect evidence commit 38e8875d records review FAIL only for the semantically stale catalog. Verification was FAIL/BLOCKED only for that same catalog dependency; all listed functional and governance gates passed. Preserve the canonical root, branch, worktree, candidate, review, verification, and user-owned primary modification to design/object-oriented-agent-and-skill-model.md byte-for-byte unstaged.

Claim Evidence: Before this lifecycle transaction, claim status returned STATUS with no live claims. Exact-file claim block-split-backlog-blockage-and-dispatch-mode-skills-019fab acquired with outcome SHARED_CHECKOUT_ACQUIRED and event eaa2fdf2-834b-46da-80c5-7e5dd1435375.

Safe Resumption: On the observable unblock condition, the parent Coordinator must restore Ready in a distinct provider transaction, preserving the canonical Thread. The normal Ready -> Starting -> Running sequence then applies. No replacement Thread is permitted while the preserved canonical identity remains valid.
