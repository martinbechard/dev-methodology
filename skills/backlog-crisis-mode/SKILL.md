---
name: backlog-crisis-mode
description: Resolve a blocked backlog sequentially in one Coordinator task without claims or delegated delivery.
metadata:
  category: development-practice
---

# Backlog Crisis Mode

Use this skill only after the user or Dev Backlog Watchdog declares a backlog crisis.

## Declaration

The Watchdog declares a crisis when any condition is true:

1. Five or more active work items are Blocked.
2. At least one active work item exists and every active work item is Blocked.
3. Three or more Blocked items name the same preventing cause or unmet dependency.
4. The actionable backlog is nonempty and, for 60 minutes, no item completed or was abandoned and no Starting or Running item produced a delivery commit or passing focused verification.

The user may declare a crisis at any time.

User Action Required, Holding, Future Ideas, Completed, Failed, Abandoned, and archived items do not count as active work for these conditions.

The declaration names the triggering condition, time, queue counts, and initial Blocked items. Send it once to the existing Coordinator task. Do not create a separate crisis task.

## Execution

The Coordinator temporarily owns delivery for the crisis set.

1. Stop ordinary dispatch.
2. Stop claim operations.
3. Process one crisis item at a time.
4. Read the current item, current main, relevant sources, preserved candidates, and review findings.
5. Confirm that the recorded blocker still exists.
6. Rewrite unclear objectives, terms, requirements, or blockers before implementation.
7. Remove requirements that do not contribute to the requested outcome.
8. Keep only a short note for superseded candidates or abandoned designs.
9. Implement the smallest complete correction.
10. Run focused tests for the changed behavior and its direct consumers.
11. Commit the current item before starting another item.
12. Finish the item as Completed, Abandoned, or Superseded.

Unrelated modified files do not stop crisis work. Stop only for an overlapping change to a file required by the current item. Adopt interrupted work when its ownership and purpose are clear; otherwise reconcile that exact overlap.

Do not add generalized provider, runtime, receipt, security, or coordination machinery unless the current item requires it.

Add an item to the crisis set when it becomes Blocked during the crisis or when resolving it is necessary to finish an existing crisis item. Do not add unrelated Ready work.

Moving an item to Ready does not resolve it.

## Watchdog Behavior

During a crisis, the Watchdog reports only:

- a new Blocked item that must join the crisis set;
- an exit condition that is not yet satisfied; or
- confirmation that every exit condition is satisfied.

It does not send routine capacity, dispatch, inactivity, or repeated blocker alerts.

## Exit

End the crisis only when:

1. Every crisis item is Completed, Abandoned, or Superseded.
2. No active item remains Blocked.
3. No crisis item is being changed.
4. Every crisis change is committed.
5. Every required combined regression has completed and each failure has a concrete disposition.

The Watchdog sends one crisis-ended notice with the resolved items and final main commit. The Coordinator rereads the backlog and resumes normal dispatch.

The user may end crisis mode. Report any unresolved crisis items before resuming normal dispatch.

## Result

Report the crisis trigger, current crisis item, completed items, unresolved items, focused checks, commits, and whether normal dispatch resumed.
