# Split Backlog Blockage And Dispatch-Mode Skills

Status: Ready

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/apply-object-oriented-skill-group-design/split-backlog-blockage-and-dispatch-mode-skills.md

Completion: direct-main

Series: backlog/feature-backlog/apply-object-oriented-skill-group-design/index.md

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
