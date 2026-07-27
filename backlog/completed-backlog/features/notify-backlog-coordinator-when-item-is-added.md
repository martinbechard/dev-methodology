# Notify the Backlog Coordinator When a Work Item Is Added

Status: Completed

Type: Feature

Owner: Unowned

Provider: file

Provider Reference: backlog/completed-backlog/features/notify-backlog-coordinator-when-item-is-added.md

Completion: direct-main

## Summary

After a new work item is successfully created, wake or notify the configured Dev Backlog Coordinator and provide the new item's provider reference.

## Context

A work item may be created while the Coordinator is inactive. Without a notification, the item may wait until something else restarts the Coordinator.

The notification only tells the Coordinator that the backlog changed. The Coordinator remains responsible for reading the current inventory, checking dependencies and capacity, and deciding whether to start any item.

## Requirements

- Notify the configured Dev Backlog Coordinator only after a new work item is successfully created.
- Include the new item's provider reference in the notification.
- Wake or resume the existing Coordinator context when the runtime supports it.
- Have the Coordinator reread the current backlog before making any dispatch decision.
- Do not reserve capacity, change lifecycle state, create a delivery task, or start implementation from the notification path.
- Do not notify for a failed creation or a duplicate request that created no item.
- If no Coordinator context is currently available, leave the committed item unchanged so the next Coordinator start can discover it normally.
- Use the configured runtime's normal task-notification mechanism. Do not invent a universal cross-provider or cross-runtime event protocol.
- Treat repeated notifications as harmless prompts to reconcile current inventory. Correctness comes from Coordinator reconciliation, not from a complex notification identifier.

## Acceptance Criteria

1. Creating a work item successfully sends its provider reference to the configured Coordinator.
2. An inactive but resumable Coordinator is awakened.
3. The Coordinator rereads the backlog before selecting work.
4. The notification does not change the new item or create a delivery task.
5. Failed or no-op creation sends no notification.
6. Repeated notification cannot cause duplicate delivery because the Coordinator reconciles existing lifecycle and task ownership before dispatch.
7. When no Coordinator is available, the item remains committed and discoverable during the next Coordinator startup.

## Verification

- Test successful creation followed by Coordinator notification.
- Test notification of an inactive but resumable Coordinator.
- Test failed and duplicate no-op creation without notification.
- Test repeated notification followed by one reconciled dispatch decision.
- Test unavailable Coordinator behavior without changing or losing the new item.
- Run git diff --check.

## Dependencies

None.

## Source Evidence

Direct user request: “when adding a new item to the backlog, advise the Backlog coordinator in case it was shut down”.

## Superseded Implementation History

Candidates 2b255e1a, 5cf8d456, and 12e0615b attempted to define a universal provider-neutral event identity and cross-runtime delivery protocol. They remain historical evidence and must not be reused as the implementation plan for this simplified item.

## Completion Evidence

- Implementation commit: 1f8906d8
- A successfully committed file work item sends its provider reference to the existing Coordinator task through the runtime's normal task-message feature.
- Failed creation, duplicate no-op creation, and an unavailable Coordinator send no message.
- The Coordinator rereads provider inventory before any reservation or dispatch decision.
- The notification changes no lifecycle state and creates no delivery task.
- Coordinator simulator tests: 24 passed.
- Focused bundle contract test: 1 passed.
- Skill validation, metadata freshness, generated-output freshness, and Git diff check passed.
- The published skills and Coordinator agent match the committed source bytes.
