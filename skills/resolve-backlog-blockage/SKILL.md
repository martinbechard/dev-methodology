---
name: resolve-backlog-blockage
description: Resolve a declared backlog blockage sequentially in one Coordinator task without claims or delegated delivery.
metadata:
  category: development-practice
---

# Resolve Backlog Blockage

Use this skill when the Coordinator's inventory reconciliation, the user, or Dev Backlog Watchdog declares a backlog blockage.

This procedure owns backlog diagnosis, recovery, and related lifecycle decisions. It does not change secondary-thread dispatch mode and remains usable when no secondary-thread dispatch mechanism is configured.

## Declaration And Crisis Epoch

The Coordinator evaluates these conditions after every relevant inventory reconciliation and every Blocked transition. The Watchdog declares a blockage when it observes any condition, and an equivalent user alert is sufficient when the triggering criterion and crisis set are observable:

1. Five or more active work items are Blocked.
2. At least one active work item exists and every active work item is Blocked.
3. Three or more Blocked items name the same preventing cause or unmet dependency.
4. The actionable backlog is nonempty and, for 60 minutes, no item completed or was abandoned and no Starting or Running item produced a delivery commit or passing focused verification.

The user may declare a blockage at any time.

User Action Required, Holding, Future Ideas, Completed, Failed, Abandoned, and archived items do not count as active work for these conditions.

The declaration names the triggering condition, time, queue counts, initial Blocked items, Coordinator task, and crisis epoch. Record that marker in the existing provider evidence rather than creating a second registry or a separate blockage task. If the same active blockage is declared again without new evidence, retain the existing epoch and recovery state.

## Entry

Declared crisis recovery supersedes the Coordinator's ordinary no-takeover boundary and the ordinary resource-claim requirement only for the active crisis set and epoch.

1. Stop new dispatch and enter regular SOLO mode.
2. Stop or pause every other mutating execution at a safe preservation boundary. Preserve commits, diffs, candidates, worktrees, review, verification, and blocker evidence.
3. After preservation is verified, invoke the configured claim helper's reset operation exactly once for the new crisis epoch. The reset must leave the live registry empty and preserve claim-event audit history.
4. After that reset, do not perform any claim status, acquire, extend, deadline extension, heartbeat, release, wait, retry, report, maintenance, or additional reset operation while the crisis epoch remains active.

The crisis-epoch marker and the reset event are durable evidence preventing repeated reset. They are not a replacement ownership registry.

## Recovery

The sole Coordinator directly owns delivery for the blockage set in its existing task.

1. Process exactly one blockage item at a time without claims or delegated delivery.
2. Keep all other mutation stopped while the current item is active.
3. Read the current item, current main, relevant sources, preserved candidates, and review findings.
4. Confirm that the recorded blocker still exists.
5. Rewrite unclear objectives, terms, requirements, or blockers before implementation.
6. Remove requirements that do not contribute to the requested outcome.
7. Keep only a short note for superseded candidates or abandoned designs.
8. Implement the smallest complete correction.
9. Run focused tests for the changed behavior and its direct consumers.
10. Commit the current item before starting another item.
11. Finish and archive the item as Completed, Abandoned, or Superseded before starting another item.

Unrelated modified files do not stop blockage recovery. Stop only for an overlapping change to a file required by the current item. Adopt interrupted work when its ownership and purpose are clear; otherwise reconcile that exact overlap.

Do not add generalized provider, runtime, receipt, security, or coordination machinery unless the current item requires it.

Add an item to the blockage set when it becomes Blocked during recovery or when resolving it is necessary to finish an existing blockage item. Include recovery-policy items created specifically to make the current crisis runnable. Do not add unrelated Ready work.

Moving an item to Ready does not resolve it.

When the same blockage state and recovery result are observed again, return the existing result without repeating lifecycle mutation.

## Watchdog Behavior

During blockage recovery, the Watchdog reports only:

- a new Blocked item that must join the blockage set;
- an exit condition that is not yet satisfied; or
- confirmation that every exit condition is satisfied.

It does not send routine capacity, dispatch, inactivity, or repeated blocker alerts.

## Exit

End blockage recovery only when:

1. Every blockage item is Completed, Abandoned, or Superseded.
2. No active item remains Blocked.
3. No blockage item is being changed.
4. Every blockage change is committed.
5. Every required combined regression has completed and each failure has a concrete disposition.

The Watchdog sends one blockage-ended notice with the resolved items and final main commit. The Coordinator rereads the backlog, confirms no mutator remains active, records that recovery is complete, and then enters regular MULTITASK mode. Normal resource-claim policy resumes only after that transition; do not reconstruct crisis-era claims.

The user may end blockage recovery. Report any unresolved blockage items before ending it.

## Result

Report the blockage trigger, current blockage item, completed items, unresolved items, focused checks, commits, and whether every exit condition is satisfied.
