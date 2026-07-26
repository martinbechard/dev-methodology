# Notify the Backlog Coordinator When a Work Item Is Added

Status: Starting

Type: Feature

Owner: Unowned

Provider: file

Provider Reference: backlog/feature-backlog/notify-backlog-coordinator-when-item-is-added.md

Completion: direct-main

## Summary

Notify the Dev Backlog Coordinator whenever a new work item is added successfully so an inactive coordinator can resume, reconcile the updated inventory, and manage available capacity.

## Context

New work items can be committed while the Dev Backlog Coordinator is inactive or has finished its current turn. Without an event-driven notification, the coordinator may not observe the new Ready item until another user or agent explicitly resumes it.

The notification must preserve the existing separation between durable backlog creation, coordinator inventory decisions, and per-item delivery. Adding an item does not itself authorize the notification path to reserve capacity, change lifecycle state, or create a work-item Thread.

## Source Evidence

Direct user request in the active task on 2026-07-25: “we want a new work item - when adding a new item to the backlog, advise the Backlog coordinator in case it was shut down”.

## Requirements

- Send one event-driven notification to the applicable Dev Backlog Coordinator after a new work item is created, committed, and verified in the selected durable provider.
- Include the canonical provider reference, lifecycle status, work-item type, completion selection, creation commit, and next runnable action in the notification.
- Wake or resume the existing coordinator context when it is inactive instead of creating a replacement coordinator or duplicate work-item Thread.
- Let the coordinator reconcile current provider inventory and Starting-plus-Running capacity before it decides whether to dispatch the new item.
- Keep notification separate from backlog mutation, lifecycle reservation, delivery ownership, and implementation dispatch.
- Do not notify for failed creation, duplicate reconciliation that creates no item, Future Idea capture, or an uncommitted local draft.
- Make repeated delivery of the same creation event idempotent so it cannot cause duplicate reservation or dispatch.
- Report a precise notification failure when no applicable coordinator can be identified or reached, while preserving the already committed work item for later inventory reconciliation.
- Support every configured durable work-item provider through provider-accurate identity and evidence rather than coupling the behavior to file paths.
- Discover the smallest governed definition scope required for implementation and obtain exact, scope-specific user approval before mutating any governed agent or skill definition.

## Acceptance Criteria

- A successfully committed new Ready work item causes exactly one notification to the applicable existing Dev Backlog Coordinator.
- An inactive coordinator is resumed by the notification and reconciles the provider inventory before making a capacity or dispatch decision.
- The notification carries enough durable evidence to identify the new item and verify its creation without reconstructing the originating conversation.
- Notification does not change the new item's lifecycle state, reserve capacity, grant delivery ownership, or create a work-item Thread.
- Duplicate delivery of the same creation event does not produce duplicate coordinator reservations or work-item Threads.
- Failed creation, duplicate no-op reconciliation, Future Idea capture, and uncommitted drafts do not notify the coordinator.
- An unreachable or unidentified coordinator produces an explicit actionable result without rolling back or hiding the committed item.
- File, GitHub, GitLab, Azure DevOps, and Jira provider contracts remain interchangeable where their configured creation capabilities exist.
- Focused tests cover active, inactive, unreachable, duplicate-event, failed-creation, and unsupported-provider cases.
- Independent review confirms that the behavior is event-driven, provider-neutral, and preserves coordinator, steward, and orchestrator ownership boundaries.

## Dependencies

None.

## Verification

- Run exact governed-definition approval checks for every affected canonical skill or agent definition before mutation.
- Run focused work-item creation, coordinator wake-up, provider-routing, duplicate-delivery, and failure-path tests.
- Regenerate only supported mirrors from approved canonical sources and run their freshness checks.
- Run relevant bundle and coordinator evaluation tests.
- Run git diff --check.
- Obtain independent methodology and prompt-contract review.

## Open Questions

- Determine how the active coordinator identity is resolved for each supported provider and runtime.
- Determine the durable event identity and acknowledgement evidence used to make coordinator notification idempotent.
- Determine whether an unreachable-coordinator result needs a separate recovery queue or can rely on provider inventory reconciliation at the next coordinator start.

## Current Starting Reservation

- Parent Coordination Thread: /root.
- Preserved Canonical Work-Item Thread: /root.
- Canonical Task: 019f9ea6-b3bd-7551-ad1f-5a862f768313.
- Preserved Canonical Root Dev Orchestrator Task: /root.
- Preserved Delivery Branch: main.
- Preserved Delivery Worktree: /Users/martinbechard/.codex/worktrees/e98b/dev-methodology.
- Reservation: One parent-owned Ready -> Starting launch reservation.
- Normalized Objective: Notify the Backlog Coordinator when a work item is added.
- Intended Root Role: Dev Orchestrator.
- Persistence And Completion: file provider; direct-main completion.
- Prior Ready Evidence: commit 2f24e29234d7348f13dcc81827cbf057afb63c81, Status Ready, Owner Unowned, and the exact three-path approval recorded below.
- Dispatched At: 2026-07-26T14:40:19Z.
- Launch Evidence: Parent Coordinator reconciled the current primary main state at a9571e8569fad51b82eb4460316359827d7f101f, found this item Ready and Unowned, found one other Starting-or-Running item against capacity ten, and authorized this exact-item reservation. Runtime acceptance remains pending.
- Backlog Claim Event: 41561b06-848d-4365-86a9-ae07b1631354.
- Next Lifecycle Owner: the preserved root Dev Orchestrator must use its own distinct Dev Backlog Steward transaction to record Starting -> Running before repository mutation. This reservation neither records Running nor creates a replacement Thread.

## Current Running Acceptance

- Canonical Work-Item Thread: /root.
- Canonical Root Dev Orchestrator Task: /root.
- Owner: Dev Orchestrator.
- Delivery Branch: main.
- Delivery Worktree: /Users/martinbechard/.codex/worktrees/e98b/dev-methodology.
- Phase: provider-neutral and governed-source discovery.
- Started At: 2026-07-26T13:51:19Z.
- Backlog Claim Evidence: acquired Event 1 exact-path claim start-running-notify-backlog-coordinator-019f9ea6; event f66b3763-7931-40b0-91f8-f0330f68ac6c.
- Running Lifecycle Commit: defff7a0689f7ded1345e52c4cbb29154a19590d.
- Running Claim Release Evidence: Event 02423e62-c38e-4b3f-afb9-c12a058776c6.

## User Action Required

- Transition: Running -> User Action Required.
- Canonical Work-Item Thread: /root.
- Canonical Root Dev Orchestrator Task: /root.
- Discovery Outcome: the proposed protocol requires changes to governed definitions, so exact scope-specific user approval is required before implementation.

### Exact Governed-Source Manifest

- agents/roles/dev-activities/dev-backlog-steward.role.yaml.
- agents/roles/dev-activities/dev-backlog-coordinator.role.yaml.
- skills/codex-workitem-coordination/SKILL.md.

### Provider Create Skills

Provider create skills need no mutation because their existing successful results already supply provider identity and evidence that the Steward can normalize.

### Dependent Artifacts

- Supported generated role and skill mirrors.
- design/orchestrated-development-lifecycle.html.
- Focused coordination and bundle tests.

### Exact Question

Do you approve changing exactly these three governed definitions so that, after a work item is successfully created and verified, Dev Backlog Steward sends one provider-neutral, idempotent creation notification to the existing Dev Backlog Coordinator, and the Coordinator wakes or resumes, reconciles inventory before dispatch, and reports an explicit unreachable result without changing the new item or creating a duplicate task?

### Options And Tradeoffs

- Approve: implement this exact protocol and supported mirrors/tests.
- Decline: keep current behavior and leave this feature unimplemented.
- Narrow/change: user specifies the permitted paths or behavior and the item remains User Action Required until reconciled.

### Unattended Boundary

No governed source, generated mirror, implementation, integration, publication, reservation, or new runtime task for this item may proceed until the user answers. Read-only reconciliation may continue.

### Resolution

- User Answer: approved.
- Answered At: 2026-07-26.
- Answer Provenance: canonical work-item Thread /root.
- Approved Governed Sources: agents/roles/dev-activities/dev-backlog-steward.role.yaml; agents/roles/dev-activities/dev-backlog-coordinator.role.yaml; skills/codex-workitem-coordination/SKILL.md.
- Approved Dependent Artifacts: supported generated role and skill mirrors; design/orchestrated-development-lifecycle.html; focused coordination and bundle tests.
- Same-Task Resumption Requirement: preserve canonical work-item Thread /root and its root Dev Orchestrator task; this Ready transaction does not reserve Starting, record Running, or create a replacement task.

## Notes

This item authorizes delivery of the coordinator-notification behavior. It does not pre-approve mutation of any governed agent or skill definition; implementation must discover and request the exact required scope.
