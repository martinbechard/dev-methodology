# Add Backlog Crisis Mode

Status: Ready

Type: Feature

Owner: Unowned

Provider: file

Provider Reference: backlog/feature-backlog/add-backlog-crisis-mode.md

Completion: direct-main

## Summary

Add a Backlog Crisis Mode in which one Coordinator thread resolves blocking work sequentially without claims or concurrent delivery. The Dev Backlog Watchdog declares and ends automatic crisis mode from explicit queue criteria. The user may also declare crisis mode.

## Context

Normal backlog coordination favors concurrent delivery. That model becomes counterproductive when many items are Blocked, the whole actionable queue is Blocked, or delivery has stopped for an extended period. Additional dispatch, claims, retries, and repeated Watchdog messages can increase confusion instead of restoring progress.

Crisis mode replaces normal coordination temporarily. One thread reviews each blocking item, validates whether its recorded blocker still exists, rewrites unclear or inflated requirements, removes scope creep, implements the smallest correction, runs focused tests, and commits that item before starting the next one.

## Crisis Declaration Criteria

The Dev Backlog Watchdog declares crisis mode when any of these conditions is true:

1. Five or more active work items have Status: Blocked.
2. At least one active typed work item exists and every active typed work item is Blocked.
3. Three or more Blocked items identify the same preventing cause or unmet dependency.
4. The actionable backlog is nonempty, no item reached Completed or Abandoned during the previous 60 minutes, and no Starting or Running item recorded a new delivery commit or passing focused verification during that period.
5. The user explicitly declares crisis mode.

User Action Required, Holding, Future Ideas, and terminal archives do not count as active typed work for these calculations.

## Crisis Declaration

- The Watchdog sends one crisis declaration to the existing Dev Backlog Coordinator.
- The declaration includes the triggering criterion, declaration time, current queue counts, and the exact Blocked items that form the initial crisis set.
- A user declaration identifies the crisis set explicitly or selects all currently Blocked items.
- The Coordinator stops ordinary dispatch and adopts the crisis set in its existing user-visible thread.
- The declaration does not create multiple crisis threads.
- After sending the declaration, the Watchdog stops routine capacity, dispatch, inactivity, and repeated blocker messages to the Coordinator.
- While crisis mode remains active, the Watchdog monitors only the crisis exit conditions and newly Blocked items.

## Crisis Execution Rules

- Use one Coordinator thread for the entire crisis.
- Do not dispatch delivery to other agents or run multiple crisis items concurrently.
- Do not acquire, extend, wait for, or release claims.
- Process one crisis item at a time.
- Before changing an item, read its current record, current main, pertinent skills, relevant source files, preserved candidates, and review findings.
- Confirm whether the recorded blocker still exists. Do not preserve a blocker merely because an older record says it exists.
- Rewrite the item before implementation when its objective, requirements, terminology, or blocker is unclear.
- Remove obsolete lifecycle history from the active plan while retaining a short superseded-history note for rejected candidates or abandoned designs.
- Remove requirements that do not contribute directly to the user's intended outcome.
- Do not introduce generalized cross-provider, cross-runtime, receipt, security, or coordination machinery unless the item actually requires it.
- Leave unrelated modified files untouched. They do not block crisis work.
- Stop only when another modification overlaps a file required by the current item. Inspect that exact overlap and either adopt it as interrupted work or reconcile it before continuing.
- Run only focused tests for the changed behavior and its direct consumers.
- Commit only the current item's intended files.
- Finish the current item's implementation and lifecycle disposition before beginning the next crisis item.
- After all related individual changes are on main, run one combined regression when the integrated behavior requires it.

## Crisis Set

- The initial crisis set contains the exact Blocked items listed in the declaration.
- Add any item that becomes Blocked during crisis mode.
- Add any newly discovered item whose unresolved cause is necessary to complete a crisis-set item.
- Do not add unrelated Ready work merely to keep the crisis thread busy.
- Moving an item from Blocked to Ready does not complete that crisis item.
- A crisis item is resolved only when it is Completed, Abandoned, or Superseded with durable evidence.
- A genuine user-owned or external condition remains part of the crisis set until it is resolved or the user explicitly removes that item from the crisis scope.

## Crisis Exit Criteria

The Watchdog ends crisis mode only when all of these conditions are true:

1. Every item in the crisis set is Completed, Abandoned, or Superseded.
2. No active item remains Blocked.
3. No item is currently being changed by the crisis thread.
4. Every crisis change is committed.
5. Any required combined regression has completed and its failures have concrete dispositions.

When the criteria pass:

- The Watchdog sends one crisis-ended notification to the Coordinator.
- The notification lists the resolved crisis set and the final main commit.
- The Coordinator leaves single-thread mode, rereads the current backlog, and resumes normal concurrent dispatch.
- The Watchdog resumes normal queue monitoring after the Coordinator acknowledges the end.

The user may end crisis mode explicitly. When doing so would leave unresolved crisis items, report those items before resuming normal dispatch.

## Conditional Skill Loading

- Create a Backlog Crisis Mode skill containing the complete declaration, execution, crisis-set, and exit rules.
- The Watchdog reads the skill only after a declaration criterion is met, after the user declares crisis mode, or while an existing crisis remains active.
- The Coordinator reads the skill only after receiving a Watchdog crisis declaration, after the user declares crisis mode, or while an existing crisis remains active.
- Do not load the crisis skill during ordinary backlog operation.
- The Watchdog role retains the declaration criteria needed to decide when the crisis skill must be loaded.
- The Coordinator role retains only the trigger that tells it to load the crisis skill after declaration.

## Expected Definition Scope

The smallest expected canonical definition scope is:

- skills/backlog-crisis-mode/SKILL.md
- skills/backlog-crisis-mode/agents/openai.yaml
- agents/roles/dev-activities/dev-backlog-watchdog.role.yaml
- agents/roles/dev-activities/dev-backlog-coordinator.role.yaml

Focused tests, supported generated mirrors, documentation, and skill inventory updates are dependent artifacts. Confirm the exact governed definition scope before implementation.

## Acceptance Criteria

1. Each automatic declaration criterion has a deterministic focused test.
2. A user can declare crisis mode without satisfying an automatic criterion.
3. One declaration produces one Coordinator crisis thread and stops ordinary concurrent dispatch.
4. No claim operation occurs while crisis mode is active.
5. The Coordinator processes crisis items sequentially and commits one item before starting the next.
6. Unrelated modified files do not block a scoped crisis commit.
7. A stale or incorrect blocker is rewritten from current evidence before implementation.
8. The Watchdog does not send routine Coordinator reminders during crisis mode.
9. Newly Blocked items are added to the crisis set.
10. Moving an item only to Ready does not satisfy crisis completion.
11. Crisis mode ends only after every crisis-set item has a terminal resolved disposition and no Blocked item remains.
12. The Coordinator rereads the backlog and resumes concurrent dispatch after the crisis-ended notification.
13. The Watchdog and Coordinator do not load the crisis skill during ordinary operation.

## Verification

- Run focused Watchdog tests for every declaration and exit criterion.
- Run focused Coordinator tests for single-thread execution, no-claim behavior, sequential commits, and suspended normal dispatch.
- Test unrelated dirty files and one exact overlapping-file case.
- Test stale-blocker reconciliation and item rewriting.
- Test a newly Blocked item joining the active crisis set.
- Test that Ready alone does not remove an item from the crisis set.
- Test user-declared and user-ended crisis mode.
- Test conditional skill loading for both roles.
- Run supported generation and freshness checks for affected definitions and mirrors.
- Run git diff --check.

## Dependencies

None.

## Source Evidence

The user requested a crisis workflow for systemic backlog blockage: one thread, no claims, one item at a time, current-evidence review, clearer rewritten work items, scope-control, focused testing, unrelated-change tolerance, Watchdog declaration and exit, and conditional crisis-skill loading by the Watchdog and Coordinator.

## Open Questions

- Determine the smallest existing runtime signal that lets the Watchdog declare and end crisis mode in the same Coordinator thread without introducing a separate coordination service.
