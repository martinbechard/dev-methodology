# Centralize active-capacity and conversation-title coordination policy

Status: Running

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/centralize-active-capacity-and-conversation-title-coordination-policy.md

Completion: direct-main

Owner: Root Dev Orchestrator 019fab2d-b796-7ff0-b7fd-8438b335e4af

Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758

Launch Reservation: ready-starting-three-reservations-019fa9bb-centralize-capacity

Normalized Objective: Centralize the Codex active-execution eligibility, capacity, runtime reconciliation, and portable conversation-title coordination policy so inactive work cannot consume capacity and every lifecycle transition has truthful execution coordination.

Dispatch Time: 2026-07-29T00:06:49.750900Z

Intended Root Role: Dev Orchestrator

Runtime Thread: 019fab2d-b796-7ff0-b7fd-8438b335e4af

Root Agent Task: 019fab2d-b796-7ff0-b7fd-8438b335e4af

Delivery Branch: codex/centralize-active-capacity-conversation-title-019fab2d

Delivery Worktree: /Users/martinbechard/.codex/worktrees/c82a/dev-methodology

Next Lifecycle Owner: Root Dev Orchestrator 019fab2d-b796-7ff0-b7fd-8438b335e4af

Phase: Running; implementation gated on six approval records and supported preflights

Started At: 2026-07-29T00:20:59.422474Z

## User Action Required

Question: “Do you explicitly approve changing the six governed definitions listed below, limited to centralizing the active-execution, capacity, runtime-reconciliation, and portable conversation-title contract described in this work item, with only supported same-category generated mirrors and ordinary documentation/tests updated as companions?”

Why User Input Is Required: Root AGENTS.md and PROJECT.yaml require explicit scope-specific user approval for every governed definition. Backlog creation and repair authority are insufficient.

### Exact Governed Scope

1. skills/codex-workitem-coordination/SKILL.md
2. skills/manage-file-work-items/SKILL.md
3. agents/roles/dev-activities/dev-backlog-coordinator.role.yaml
4. agents/roles/dev-activities/dev-backlog-steward.role.yaml
5. agents/roles/dev-activities/dev-orchestrator.role.yaml
6. agents/roles/dev-activities/dev-backlog-watchdog.role.yaml

### Illustrative Before And After

Before, a provider may remain Starting while its canonical conversation is idle and still inflate active capacity, and its display title may remain “Waiting for Claim” after the claim is gone. After, Starting occupies capacity only during a bounded live launch handshake; otherwise it returns to Ready, and the Steward renames the canonical conversation after the committed lifecycle transition or verifies an exact rename handoff when it lacks UI authority.

### Options And Consequences

- Approve: permits exact approval records, one supported preflight per governed path, the narrow implementation, supported same-category regeneration, ordinary README/design/tests, independent review, and delivery.
- Defer: preserves this item and its evidence in User Action Required without any definition, mirror, companion, or candidate mutation.
- Decline: ends this requested governed-definition change. The earlier work-item creation authorization is not reframed as definition approval.

### Exclusions

No other skill, agent, or metadata definition is in scope. Generated mirrors must not be hand-edited. No skill-to-skill loading is permitted.

Unattended Work Boundary: Stop all definition, mirror, companion implementation, test, documentation, candidate, review, integration, and delivery work until the answer is durably recorded and the same canonical task resumes User Action Required -> Ready -> Starting -> Running with all six exact preflights ALLOWED.

## User Action Required Transition

- Transition: Running -> User Action Required.
- Canonical Work-Item Thread: 019fab2d-b796-7ff0-b7fd-8438b335e4af.
- Canonical Root Agent Task Id: 019fab2d-b796-7ff0-b7fd-8438b335e4af.
- Owner: Root Dev Orchestrator 019fab2d-b796-7ff0-b7fd-8438b335e4af; canonical Thread preserved for the answer and resumption.
- Delivery Branch: codex/centralize-active-capacity-conversation-title-019fab2d.
- Delivery Worktree: /Users/martinbechard/.codex/worktrees/c82a/dev-methodology.
- Running Evidence Preserved: provider-only acceptance commit 24af5ac10ea909a0d5709a85b02742be894c79d9; claim acquired event 1157cbfa-2b2d-41e2-a9e3-85638816b958; claim released event 3cdde1d7-2c99-4514-a370-353c40f54910.
- Lifecycle Claim Evidence: running-uar-centralize-capacity-recovery-019fab2d; claim outcome SHARED_CHECKOUT_ACQUIRED; claim event 9c9bfd66-fef7-4414-9ad5-9baed91a94f9; claimed 2026-07-29T00:34:12.203006Z.

## User Action Resolution And Resumption

- Resolution: Approve.
- Answer: ok I approve.
- Answered At: 2026-07-28.
- Provenance: Direct user message in canonical work-item conversation 019fab2d-b796-7ff0-b7fd-8438b335e4af.
- Authorized Scope: Exactly the six governed paths listed in User Action Required, limited to the recorded centralized active-execution, capacity, runtime-reconciliation, and portable conversation-title contract; supported same-category mirrors and ordinary companions only. The recorded exclusions remain binding.
- Transition: User Action Required -> Ready.
- Owner: Unowned pending the parent Coordinator's distinct Ready -> Starting reservation.
- Canonical Work-Item Thread Preserved: 019fab2d-b796-7ff0-b7fd-8438b335e4af.
- Lifecycle Claim Evidence: uar-ready-centralize-capacity-019fab2d; claim outcome SHARED_CHECKOUT_ACQUIRED; claim event e00f7aea-3dfb-4b91-b0ca-64fb44b06b5a; claimed 2026-07-29T01:09:50.047653Z.

## Resumed Starting Reservation

- Transition: Ready -> Starting.
- Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758.
- Canonical Work-Item Thread: 019fab2d-b796-7ff0-b7fd-8438b335e4af.
- Canonical Root Agent Task Id: 019fab2d-b796-7ff0-b7fd-8438b335e4af.
- Owner: Parent Dev Backlog Coordinator dispatch reservation.
- Launch Reservation: resumed-ready-starting-019fab2d; one live immediate bounded launch handshake.
- Dispatch Time: 2026-07-29T01:11:01.062826Z.
- Normalized Objective: Centralize the Codex active-execution eligibility, capacity, runtime reconciliation, and portable conversation-title coordination policy so inactive work cannot consume capacity and every lifecycle transition has truthful execution coordination.
- Intended Root Role: Dev Orchestrator.
- Delivery Branch: codex/centralize-active-capacity-conversation-title-019fab2d.
- Delivery Worktree: /Users/martinbechard/.codex/worktrees/c82a/dev-methodology.
- Observed Launch Evidence: The parent Coordinator preserved and re-reserved the same canonical Thread immediately after the approved User Action Required -> Ready transition.
- Required Next Transition: The same root Dev Orchestrator must atomically record Starting -> Running before any implementation.
- Lifecycle Claim Evidence: ready-starting-centralize-capacity-019fab2d; claim outcome SHARED_CHECKOUT_ACQUIRED; claim event 06a67744-120d-46ff-88b5-e5385b5c4301; claimed 2026-07-29T01:11:01.062826Z.

## Resumed Running Acceptance

- Transition: Starting -> Running.
- Canonical Work-Item Thread: 019fab2d-b796-7ff0-b7fd-8438b335e4af.
- Canonical Root Agent Task Id: 019fab2d-b796-7ff0-b7fd-8438b335e4af.
- Owner: Root Dev Orchestrator 019fab2d-b796-7ff0-b7fd-8438b335e4af.
- Phase: Running; implementation is gated on an approval record and one supported preflight returning ALLOWED for each of the six approved governed paths.
- Delivery Branch: codex/centralize-active-capacity-conversation-title-019fab2d.
- Delivery Worktree: /Users/martinbechard/.codex/worktrees/c82a/dev-methodology.
- Immediate Acceptance Evidence: The canonical root accepted the parent Coordinator's live resumed Starting reservation at 2026-07-29T01:12:05.042925Z before implementation.
- Preserved Lifecycle Commits: Running acceptance 24af5ac10ea909a0d5709a85b02742be894c79d9; User Action Required 9b28d38fc84f27bb86d36e5e4d5633195e5ae44c; approved Ready resumption 0ef3db18ac71b287679ea47c3b13b7548d9ff68c; resumed Starting reservation f7f3c1bad31055fcdfe883db6162787bb03f3173.
- Preserved Claim Evidence: 1157cbfa-2b2d-41e2-a9e3-85638816b958 acquired and 3cdde1d7-2c99-4514-a370-353c40f54910 released; e00f7aea-3dfb-4b91-b0ca-64fb44b06b5a acquired and 88cbcf96-0fb2-4268-b184-86c8cb97fc33 released; 06a67744-120d-46ff-88b5-e5385b5c4301 acquired and e9d3e8d1-5b4c-41c3-a85b-02a3750709b2 released.
- Required Approval And Preflights: skills/codex-workitem-coordination/SKILL.md; skills/manage-file-work-items/SKILL.md; agents/roles/dev-activities/dev-backlog-coordinator.role.yaml; agents/roles/dev-activities/dev-backlog-steward.role.yaml; agents/roles/dev-activities/dev-orchestrator.role.yaml; agents/roles/dev-activities/dev-backlog-watchdog.role.yaml.
- Lifecycle Claim Evidence: starting-running-centralize-capacity-019fab2d; claim outcome SHARED_CHECKOUT_ACQUIRED; claim event 9526eaa5-33d2-40ad-befe-226415835527; claimed 2026-07-29T01:12:05.042925Z.

## Starting Reservation

- Transition: Ready -> Starting.
- Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758.
- Canonical Work-Item Thread: 019fab2d-b796-7ff0-b7fd-8438b335e4af.
- Canonical Root Agent Task Id: 019fab2d-b796-7ff0-b7fd-8438b335e4af.
- Owner: Parent Dev Backlog Coordinator dispatch reservation.
- Launch Reservation: ready-starting-three-reservations-019fa9bb-centralize-capacity; one live bounded handshake.
- Normalized Objective: Centralize the Codex active-execution eligibility, capacity, runtime reconciliation, and portable conversation-title coordination policy so inactive work cannot consume capacity and every lifecycle transition has truthful execution coordination.
- Intended Root Role: Dev Orchestrator.
- Delivery Branch: codex/centralize-active-capacity-conversation-title-019fab2d.
- Delivery Worktree: /Users/martinbechard/.codex/worktrees/c82a/dev-methodology.
- Conversation Title Handoff: Centralize active-capacity and conversation-title coordination policy — Starting. The canonical conversation owner must synchronize this title before accepting delivery.
- Observed Launch Evidence: Parent Dev Backlog Coordinator reserved this canonical Thread under available Starting-plus-Running capacity and woke its canonical root task.
- Required Next Transition: The same root Dev Orchestrator must atomically record Starting -> Running for this canonical Thread and task before any implementation or governed definition mutation.
- Lifecycle Claim Evidence: ready-starting-three-reservations-019fa9bb; claim outcome SHARED_CHECKOUT_ACQUIRED; claim event ee40be56-9b67-437f-91e6-f70c38fe84f8; claimed 2026-07-29T00:06:49.750900Z.

## Running Acceptance

- Transition: Starting -> Running.
- Canonical Work-Item Thread: 019fab2d-b796-7ff0-b7fd-8438b335e4af.
- Canonical Root Agent Task Id: 019fab2d-b796-7ff0-b7fd-8438b335e4af.
- Owner: Root Dev Orchestrator 019fab2d-b796-7ff0-b7fd-8438b335e4af.
- Phase: Lifecycle acceptance complete; implementation has not started.
- Delivery Branch: codex/centralize-active-capacity-conversation-title-019fab2d.
- Delivery Worktree: /Users/martinbechard/.codex/worktrees/c82a/dev-methodology.
- Started-At Evidence: Root Dev Orchestrator accepted this canonical Starting reservation before repository mutation; 2026-07-29T00:20:59.422474Z.
- Lifecycle Claim Evidence: running-transition-019fab2d; claim outcome SHARED_CHECKOUT_ACQUIRED; claim event 1157cbfa-2b2d-41e2-a9e3-85638816b958; claimed 2026-07-29T00:20:59.422474Z.

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
