# Centralize active-capacity and conversation-title coordination policy

Status: Ready

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/centralize-active-capacity-and-conversation-title-coordination-policy.md

Completion: direct-main

## Summary

Centralize the Codex active-execution eligibility, capacity, runtime reconciliation, and portable conversation-title coordination policy so inactive work cannot consume capacity and every lifecycle transition has truthful execution coordination.

## Context

The user observed that ten Starting-plus-Running provider records did not equal ten running tasks and stated: Provider records should not be in Starting and Running if their tasks are not running. The user requested that backlog coordination keep titles synchronized, clarified that skills do not need to load other skills because the applicable agent definition loads both, authorized creation with ok create the workitem and add it to the queue, and corrected the portable term to conversation title: Another thing - the agents forget to update the task titles. We should make that the backlog steward's responsibility. However, task is the Codex term, I think in general it is known as a conversation. So lets use conversation title in the steward's skill to be more portable.

## Source Evidence

Direct user authorization in the canonical parent conversation on 2026-07-28: ok create the workitem and add it to the queue. The same user direction supplied the quoted observed failure and the conversation-title correction preserved in Context.

## Requirements

- Make skills/codex-workitem-coordination/SKILL.md the single normative authority for Codex active-execution eligibility, short bounded Starting settlement, Running eligibility, capacity counting, runtime and conversation reconciliation, and conversation-title synchronization.
- Use the portable term conversation title in canonical skill, role, and guidance sources. Adapters may map it to a Codex task title or platform UI term.
- Make Dev Backlog Steward accountable after every successful lifecycle transition, including Ready to Starting, Starting to Running, User Action Required, Blocked, Stalled, Awaiting Review when applicable, and terminal outcomes.
- When the runtime can rename the conversation, rename it. Otherwise send the exact required title to the canonical conversation owner or runtime coordinator and verify that handoff before reporting transition coordination complete.
- Keep skills/manage-file-work-items/SKILL.md responsible only for atomic file-provider transitions. It must not own runtime title or capacity policy.
- Keep skills independent: no skill loads another skill. Applicable agent definitions select both skills, and roles retain ownership assignments without copying policy.
- Count Starting only during a live bounded handshake. Restore Ready when that handshake is not live and bounded.
- Require active root execution, live delegated work, or a documented bounded owned wait or progress condition for Running. Otherwise use a truthful non-active state and release capacity.
- Treat these anticipated governed sources as a discovery manifest, not approval: skills/codex-workitem-coordination/SKILL.md; skills/manage-file-work-items/SKILL.md; agents/roles/dev-activities/dev-backlog-coordinator.role.yaml; agents/roles/dev-activities/dev-backlog-steward.role.yaml; agents/roles/dev-activities/dev-orchestrator.role.yaml; agents/roles/dev-activities/dev-backlog-watchdog.role.yaml. Seek exact scope-specific user approval before mutating any governed definition.
- Align applicable human guidance: README.md, design/orchestrated-development-lifecycle.html, and design/agentic-configuration.html. Regenerate mirrors only through supported generators.

## Acceptance Criteria

- One centralized invariant governs active eligibility, capacity, runtime reconciliation, and conversation-title synchronization.
- No skill-to-skill loading exists, and duplicated policy is removed.
- Inactive tasks cannot inflate active capacity.
- Portable conversation titles match the execution phase, with verified handoff when direct rename is unavailable.
- Focused tests and generated-output freshness demonstrate the changed contract.

## Dependencies

None

## Verification

- Run focused tests in scripts/test_codex_workitem_coordination.py and scripts/test_bundle_content.py.
- Run the applicable supported generator freshness check and git diff --check.
- Obtain independent review of the centralized policy, ownership boundaries, and generated effects.

## Open Questions

- What exact bounded Starting settlement duration and trigger should apply?
- What precise representation records a bounded owned wait without falsely treating inactive work as Running?

## Notes

Collision reconciliation before creation searched ordinary active typed folders, backlog/user-action-required, and backlog/holding only. It found no matching canonical path, slug, source reference, or overlapping outcome. Future Ideas were not inspected.

This Ready item authorizes backlog capture only. It does not approve any governed definition mutation, reserve capacity, dispatch execution, or change a lifecycle state.
