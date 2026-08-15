# Align Generic Agent Definitions Source with the Documentation Design System

Owner: Unowned

Status: Ready

Type: Feature

Provider: file

Work Item ID: align-generic-agent-definitions-source-with-documentation-design-system

Completion: main-branch

Series: backlog/feature-backlog/html-documentation-review-and-design-alignment/index.md

## Summary

Align design/generic-agent-definitions-source.html with the adopted Documentation Design System after its text has been corrected and independently accepted.

## Context

The completed Documentation Design System integration deliberately excluded migration of existing HTML pages. This item performs the page-specific migration for design/generic-agent-definitions-source.html only after Work Item review-generic-agent-definitions-source-text establishes an accepted content baseline.

The design pass must preserve accepted meaning. If it discovers a material text defect, stop the affected design change and return the defect for content reconciliation rather than silently rewriting the page during visual migration.

## Source Evidence

The user requested on 2026-08-09 in canonical task 019fb057-1767-7ef2-b5fa-41f4417b20b3 a separate design-system-alignment work item for each HTML page, dependent on that page's completed text review.

Target page: design/generic-agent-definitions-source.html

## Requirements

- Use the accepted output of Work Item review-generic-agent-definitions-source-text as the semantic baseline.
- Identify the page type and apply the corresponding Documentation Design System checklist together with all applicable cross-cutting checklists.
- Align page shell, header, navigation, typography, spacing, color, content hierarchy, data display, diagrams, actions, responsive behavior, accessibility, settings behavior, and footer treatment as applicable.
- Reuse the adopted design-system assets and components instead of creating page-local variants without evidence.
- Preserve justified page-specific variations and document their rationale, checklist evidence, and review disposition.
- Change authoritative sources or generators for generated content and regenerate the target page. Do not hand-edit generated output.
- Preserve exact accepted wording and semantics except for mechanical markup movement. Route any newly discovered content defect back to content review before continuing.
- Preserve document provenance through the authorized source or generator path.
- Obtain independent Documentation Design System review and browser-based UX and accessibility verification.

## Acceptance Criteria

- design/generic-agent-definitions-source.html passes every applicable Documentation Design System checklist item or records an accepted, source-backed variation.
- The page retains the accepted content baseline with no omitted, duplicated, reordered, or semantically changed material.
- Shared shell, navigation, settings, responsive, accessibility, and footer behaviors match the maintained documentation set.
- Interactive controls work with keyboard and assistive technology, and the page has no console errors, broken links, fragment failures, overflow, inaccessible names, or invalid duplicate identifiers.
- Generated output matches its authoritative source and passes freshness checks.
- Independent design-system review returns ACCEPTED and independent verification passes at required viewport and interaction boundaries.

## Dependencies

- review-generic-agent-definitions-source-text

Blocker owner: Work Item review-generic-agent-definitions-source-text.

Blocked to Ready condition: review-generic-agent-definitions-source-text is Completed with corrected content, fresh independent acceptance, and an immutable content baseline for design/generic-agent-definitions-source.html.

Dependency Resolution: Satisfied by completed Work Item `review-generic-agent-definitions-source-text`, archived in the terminal provider transaction. Accepted content baseline `82c88a17e17ce407ba225f491ba5ba59a2150d3a` was delivered through main integration commit `33728187db5cfd0eb4359ae7acc69d8da598e010` with fresh artifact and code reviews GOOD plus independent verification WARN only for the pre-existing historical provenance migration gap.

## Verification

- Run review-documentation-design-system with the exact page-type and cross-cutting checklists applicable to design/generic-agent-definitions-source.html.
- Run focused page-shell, navigation, settings, markup, link, fragment, provenance, generator-freshness, and bundle tests that consume the page.
- Verify wide and narrow viewports, keyboard operation, accessible names and states, focus behavior, contrast, overflow, diagrams, tables, and browser-console cleanliness as applicable.
- Compare final text-bearing nodes and accessibility attributes against the accepted content baseline.
- Obtain fresh independent artifact, UX, and verification verdicts.
- Run Git diff checks for the exact changed paths.

## Open Questions

- Which Documentation Design System page type and optional variation contract best fit design/generic-agent-definitions-source.html?
- Does the page contain a justified interaction or data-display variation that needs explicit design-system evidence?

## Notes

- This item must not start before its page-specific text review is Completed.
- Creation of this work item does not dispatch it while backlog crisis recovery remains active.

## Starting Handoff Evidence

- Reserved At: 2026-08-13T20:28:08Z.
- Transition: `Ready -> Starting`.
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Coordinator Execution: `/root/backlog_coordinator`.
- Baseline: `ef2addc2b0c626e4111ca25bbc2229535fb54c81` on primary `main`.
- Capacity: Slot 3 of 5; all User Action Required and Blocked items are excluded.
- Dependency Evidence: The page-specific text review is Completed, and the HTML series explicitly permits pages to proceed independently.
- Transition Claim: `reserve-generic-agent-definitions-019ff2c3`; event `43cce56b-a841-41d2-9819-4b66219b1c75`.
- Dispatch Architecture: Create one visible Codex task whose reference-plus-delta prompt starts one Dev Orchestrator collaboration subagent.
- Next Action: Reconcile the unique visible task identity; its nested Dev Orchestrator records `Starting -> Running` before mutation.

## Canonical Runtime Assignment

- Assigned At: 2026-08-13T20:32:03Z.
- Codex Task ID: `019ffcd2-8892-7522-95fd-4811067fd5c4`.
- Conversation ID: `019ffcd2-8892-7522-95fd-4811067fd5c4`.
- Host: `local`.
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Runtime Project: saved `dev-methodology` project at `/Users/martinbechard/dev/dev-methodology`.
- Creation Outcome: Unique direct success with no client or pending identity and no retry.
- Lifecycle Boundary: Provider remains `Starting` until exactly one nested Dev Orchestrator accepts and records `Starting -> Running`.
- Adoption Claim: `adopt-generic-agent-definitions-task-019ff2c3`; event `876d4458-211a-4c1b-814d-705da72ff849`.

## Running Acceptance Evidence

- Accepted At: 2026-08-13T20:33:24Z.
- Transition: `Starting -> Running`.
- Owner: Dev Orchestrator.
- Root Role: Dev Orchestrator.
- Canonical Codex Task ID: `019ffcd2-8892-7522-95fd-4811067fd5c4`.
- Canonical Conversation ID: `019ffcd2-8892-7522-95fd-4811067fd5c4`.
- Runtime Parent Task ID: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Coordinator Task ID: `/root/backlog_coordinator`.
- Branch: `main`.
- Worktree: `/Users/martinbechard/dev/dev-methodology`.
- Phase: Planning.
- Accepted Execution Evidence: The canonical visible task launched this single nested Dev Orchestrator, which accepted the authoritative file-provider assignment before source mutation.
- Transition Claims: `align-generic-agent-running-019ffcd2` and `align-generic-agent-running-file-019ffcd2`.
- Next Action: Produce and review a bounded implementation and TDD plan before source mutation.

## Crisis Serialization Blocker

- Transition: `Running -> Blocked`.
- Recorded At: 2026-08-14T04:48:51Z.
- Crisis Epoch: `blocked-crisis-20260813T223935Z`.
- Exact Blocker: Dev-methodology crisis recovery permits exactly one local work-item execution. The Coordinator selected the stronger accepted Specialization Examples finish lane for the current slot, so this stopped execution cannot truthfully remain Running or mutate concurrently.
- Recovery Owner: Dev Backlog Coordinator.
- Observable Unblock Trigger: The selected Specialization Examples crisis execution reaches terminal cleanup or another truthful non-active disposition, and fresh inventory confirms this preserved item is the next eligible serial recovery.
- Preserved Candidate: `e5a4dd650cd56eccba1085ca06013464c064427f` on branch `codex/align-generic-agent-definitions-019ffcd2` in clean worktree `/Users/martinbechard/dev/dev-methodology/.worktrees/align-generic-agent-definitions-candidate-019ffcd2`.
- Preserved Execution: Canonical Task and Conversation `019ffcd2-8892-7522-95fd-4811067fd5c4` on host `local`, with its existing nested Dev Orchestrator and synchronized plan artifacts.
- Coordination Boundary: No claim operation occurred. Preserve the task unarchived with no source, plan, branch, worktree, or candidate mutation.
- Required Runtime Title: `Blocked — Align Generic Agent Definitions Source With Documentation Design System`.
- Safe Resume: Resume the same task only through `Blocked -> Ready -> Starting -> Running` after the observable trigger.

## Crisis Recovery Ready Evidence

- Transition: `Blocked -> Ready`.
- Recorded At: 2026-08-15T21:34:11Z.
- Crisis Epoch: `blocked-crisis-20260813T223935Z`.
- Resolved Blocker: The selected Specialization Examples crisis execution reached provider `Completed` on configured primary `main`, with accepted delivery, independent review, focused verification, browser cleanup, and a truthful non-active disposition.
- Recovery Decision: This preserved item is the next eligible serial crisis recovery. Ordinary Ready inventory remains excluded while the crisis epoch is active.
- Preserved Candidate: `e5a4dd650cd56eccba1085ca06013464c064427f` on branch `codex/align-generic-agent-definitions-019ffcd2` in clean worktree `/Users/martinbechard/dev/dev-methodology/.worktrees/align-generic-agent-definitions-candidate-019ffcd2`.
- Preserved Canonical Task and Conversation: `019ffcd2-8892-7522-95fd-4811067fd5c4` on host `local`; archived-task reconciliation found no matching archived task, so replacement is prohibited.
- Runtime Parent Task: `01a00756-0c89-7ad0-9468-32da50806a86`.
- Coordinator Task: `/root/backlog_coordinator`.
- Capacity: One available slot of the sole local crisis capacity; this item consumes no slot until `Ready -> Starting` is recorded.
- Coordination Boundary: Claim-free crisis transition. The live claim registry was reset on crisis entry and no claim operation is permitted before crisis exit.
- Next Action: Reserve this Ready item for the same canonical execution, then send the exact resume message to that task so its existing root Dev Orchestrator can accept `Starting -> Running` before mutation.
