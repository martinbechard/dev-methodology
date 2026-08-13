# Align Wiki Skills and Project Context with the Documentation Design System

Owner: Unowned

Status: Blocked

Type: Feature

Provider: file

Work Item ID: align-wiki-skills-and-project-context-with-documentation-design-system

Completion: main-branch

Series: backlog/feature-backlog/html-documentation-review-and-design-alignment/index.md

## Summary

Align design/wiki-skills-and-project-context.html with the adopted Documentation Design System after its text has been corrected and independently accepted.

## Context

The completed Documentation Design System integration deliberately excluded migration of existing HTML pages. This item performs the page-specific migration for design/wiki-skills-and-project-context.html only after Work Item review-wiki-skills-and-project-context-text establishes an accepted content baseline.

The design pass must preserve accepted meaning. If it discovers a material text defect, stop the affected design change and return the defect for content reconciliation rather than silently rewriting the page during visual migration.

## Source Evidence

The user requested on 2026-08-09 in canonical task 019fb057-1767-7ef2-b5fa-41f4417b20b3 a separate design-system-alignment work item for each HTML page, dependent on that page's completed text review.

Target page: design/wiki-skills-and-project-context.html

## Requirements

- Use the accepted output of Work Item review-wiki-skills-and-project-context-text as the semantic baseline.
- Identify the page type and apply the corresponding Documentation Design System checklist together with all applicable cross-cutting checklists.
- Align page shell, header, navigation, typography, spacing, color, content hierarchy, data display, diagrams, actions, responsive behavior, accessibility, settings behavior, and footer treatment as applicable.
- Reuse the adopted design-system assets and components instead of creating page-local variants without evidence.
- Preserve justified page-specific variations and document their rationale, checklist evidence, and review disposition.
- Change authoritative sources or generators for generated content and regenerate the target page. Do not hand-edit generated output.
- Preserve exact accepted wording and semantics except for mechanical markup movement. Route any newly discovered content defect back to content review before continuing.
- Preserve document provenance through the authorized source or generator path.
- Obtain independent Documentation Design System review and browser-based UX and accessibility verification.

## Acceptance Criteria

- design/wiki-skills-and-project-context.html passes every applicable Documentation Design System checklist item or records an accepted, source-backed variation.
- The page retains the accepted content baseline with no omitted, duplicated, reordered, or semantically changed material.
- Shared shell, navigation, settings, responsive, accessibility, and footer behaviors match the maintained documentation set.
- Interactive controls work with keyboard and assistive technology, and the page has no console errors, broken links, fragment failures, overflow, inaccessible names, or invalid duplicate identifiers.
- Generated output matches its authoritative source and passes freshness checks.
- Independent design-system review returns ACCEPTED and independent verification passes at required viewport and interaction boundaries.

## Dependencies

- review-wiki-skills-and-project-context-text

Blocker owner: Work Item review-wiki-skills-and-project-context-text.

Blocked to Ready condition: review-wiki-skills-and-project-context-text is Completed with corrected content, fresh independent acceptance, and an immutable content baseline for design/wiki-skills-and-project-context.html.

Dependency Reconciliation: Satisfied by completed Work Item `review-wiki-skills-and-project-context-text`; its archived provider record and accepted immutable content baseline remain authoritative. No current impediment remains.

## Verification

- Run review-documentation-design-system with the exact page-type and cross-cutting checklists applicable to design/wiki-skills-and-project-context.html.
- Run focused page-shell, navigation, settings, markup, link, fragment, provenance, generator-freshness, and bundle tests that consume the page.
- Verify wide and narrow viewports, keyboard operation, accessible names and states, focus behavior, contrast, overflow, diagrams, tables, and browser-console cleanliness as applicable.
- Compare final text-bearing nodes and accessibility attributes against the accepted content baseline.
- Obtain fresh independent artifact, UX, and verification verdicts.
- Run Git diff checks for the exact changed paths.

## Open Questions

- Which Documentation Design System page type and optional variation contract best fit design/wiki-skills-and-project-context.html?
- Does the page contain a justified interaction or data-display variation that needs explicit design-system evidence?

## Notes

- This item must not start before its page-specific text review is Completed.
- Creation of this work item does not dispatch it while backlog crisis recovery remains active.

## Starting Handoff Evidence

- Reserved At: 2026-08-13T20:29:11Z.
- Transition: `Ready -> Starting`.
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Coordinator Execution: `/root/backlog_coordinator`.
- Baseline: `e65b32ed1957bc4e9dcac9e4b7f4635c483de887` on primary `main`.
- Capacity: Slot 5 of 5; all User Action Required and Blocked items are excluded.
- Dependency Evidence: The page-specific text review is Completed, and the HTML series explicitly permits pages to proceed independently.
- Transition Claim: `reserve-wiki-skills-context-019ff2c3`; event `f209fd16-bfa9-473e-9849-aa3518812cdf`.
- Dispatch Architecture: Create one visible Codex task whose reference-plus-delta prompt starts one Dev Orchestrator collaboration subagent.
- Next Action: Reconcile the unique visible task identity; its nested Dev Orchestrator records `Starting -> Running` before mutation.

## Canonical Runtime Assignment

- Assigned At: 2026-08-13T20:32:03Z.
- Codex Task ID: `019ffcd2-a09c-7c91-a09c-d61bc1c04a64`.
- Conversation ID: `019ffcd2-a09c-7c91-a09c-d61bc1c04a64`.
- Host: `local`.
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Runtime Project: saved `dev-methodology` project at `/Users/martinbechard/dev/dev-methodology`.
- Creation Outcome: Unique direct success with no client or pending identity and no retry.
- Lifecycle Boundary: Provider remains `Starting` until exactly one nested Dev Orchestrator accepts and records `Starting -> Running`.
- Adoption Claim: `adopt-wiki-skills-context-task-019ff2c3`; event `a46dba3b-6343-49d8-82f8-736bf9d3fe2b`.

## Running Acceptance Evidence

- Accepted At: 2026-08-13T20:33:05Z.
- Transition: `Starting -> Running`.
- Owner: Dev Orchestrator.
- Canonical Conversation: `019ffcd2-a09c-7c91-a09c-d61bc1c04a64`.
- Canonical Task: `019ffcd2-a09c-7c91-a09c-d61bc1c04a64`.
- Branch: `main`.
- Worktree: `/Users/martinbechard/dev/dev-methodology`.
- Phase: implementation planning and design-system scope discovery.
- Accepted Execution Evidence: The canonical Dev Orchestrator accepted the reserved assignment after confirming the provider record, satisfied dependency, primary `main` checkout, and empty claim registry.
- Next Action: Produce and independently review a bounded implementation and TDD plan before source mutation.

## Blocked Evidence

- Recorded At: 2026-08-13T20:42:05Z.
- Transition: `Running -> Blocked`.
- Canonical Task and Conversation: `019ffcd2-a09c-7c91-a09c-d61bc1c04a64` on host `local`.
- Preserved Dev Orchestrator: the same nested execution launched by the canonical visible task.
- Source State: No source mutation or candidate exists.
- Exact Blocker: Configured `mcp-agent-ops` resolves `review-documentation-design-system` version `0.1.0`, while this repository requires version `1.0.0`.
- Recovery Owner: Project Configurator and the configured MCP skill-catalog owner.
- Unblock Condition: Refresh the configured MCP skill catalog and prove a revision-matched load resolves `review-documentation-design-system` version `1.0.0`.
- Work Claim Release: `align-wiki-skills-context-work-019ffcd2`; disposition `blocked`; event `990c8b3f-8257-4b6f-a489-9ac5fc6edd9d`.
- Provider Transition Claim: `block-wiki-skill-version-019ff2c3`; event `f592cb31-755b-4648-93fa-3835d40a6507`.
- Required Runtime Title: `Blocked — Align Wiki Skills And Project Context With Documentation Design System`.
- Safe Resume: After the unblock condition, preserve the same canonical task and resume only through `Blocked -> Ready -> Starting -> Running`.

## Recovery Resolution

- Resolved At: 2026-08-13T21:12:06Z.
- Transition: `Blocked -> Ready`.
- Recovery Result: Configured `mcp-agent-ops` now resolves `review-documentation-design-system` version `1.0.0`.
- Revision-Matched Proof: Refresh, skill load, and all 11 applicable checklist loads share revision `cff1fd094bd840c97adb17b079cc118d1d1d4d0621cdc3a6785b61fed1d2591e`.
- Byte Verification: Installed checklist bytes match the repository, and focused catalog, skill, installer, and diff checks pass.
- Source State: No repository, page, or provider mutation was required by the supporting recovery.
- Preserved Canonical Task and Conversation: `019ffcd2-a09c-7c91-a09c-d61bc1c04a64`.
- Provider Transition Claim: `unblock-wiki-skill-version-019ff2c3`; event `0ca0a1f7-43c6-4ba9-a799-64e471a954bd`.
- Required Runtime Title: `Ready — Align Wiki Skills And Project Context With Documentation Design System`.

## Recovered Starting Evidence

- Reserved At: 2026-08-13T21:12:06Z.
- Transition: `Ready -> Starting`.
- Capacity: Slot 5 of 5.
- Preserved Canonical Task and Conversation: `019ffcd2-a09c-7c91-a09c-d61bc1c04a64`.
- Preserved Dev Orchestrator: the same nested execution.
- Recovery Baseline: `037e093d`.
- Transition Claim: `unblock-wiki-skill-version-019ff2c3`; event `0ca0a1f7-43c6-4ba9-a799-64e471a954bd`.
- Required Runtime Title: `Starting — Align Wiki Skills And Project Context With Documentation Design System`.
- Next Action: The same nested Dev Orchestrator records `Starting -> Running`, reacquires its Work Item claim, and resumes planning with the revision-matched v1.0.0 review skill and checklists.

## Provenance Catalog Blocked Evidence

- Recorded At: 2026-08-13T21:31:18Z.
- Transition: `Running -> Blocked`.
- Canonical Task and Conversation: `019ffcd2-a09c-7c91-a09c-d61bc1c04a64`.
- Preserved Execution: The same nested Dev Orchestrator and accepted implementation plan.
- Source State: No source mutation or candidate exists.
- Exact Blocker: Catalog revision `cff1fd094bd840c97adb17b079cc118d1d1d4d0621cdc3a6785b61fed1d2591e` resolves `document-provenance` digest `ed1c5c69…`, while repository compact-v2 authority requires digest `2f50ecb30a023fd4c74ca8f57773dea475bb122b7537c3958639404672914563`.
- Recovery Owner: Project Configurator and configured MCP skill-catalog owner.
- Unblock Condition: A revision-matched configured `skill_load` returns `document-provenance` digest `2f50ecb30a023fd4c74ca8f57773dea475bb122b7537c3958639404672914563`.
- Path Claim Release: `paths-wiki-skills-context-019ffcd2`; event `edbd11a2-259c-4b7b-8959-363243f12acf`. The preceding disposition-bearing release was rejected and made no change.
- Work Claim Release: `resume-wiki-skills-context-work-019ffcd2`; disposition `blocked`; event `e40e7133-472b-472a-bfc7-44955f2bd215`.
- Provider Transition Claim: `block-wiki-provenance-digest-019ff2c3`; event `7d647467-41c4-4015-ab5e-38ece34772ca`.
- Required Runtime Title: `Blocked — Align Wiki Skills And Project Context With Documentation Design System`.
- Safe Resume: Preserve the same task and plan, then resume only through `Blocked -> Ready -> Starting -> Running` after the exact digest proof.

## Recovered Running Acceptance Evidence

- Accepted At: 2026-08-13T21:14:20Z.
- Transition: `Starting -> Running`.
- Owner: Dev Orchestrator.
- Canonical Conversation: `019ffcd2-a09c-7c91-a09c-d61bc1c04a64`.
- Canonical Task: `019ffcd2-a09c-7c91-a09c-d61bc1c04a64`.
- Branch: `main`.
- Worktree: `/Users/martinbechard/dev/dev-methodology`.
- Phase: resumed implementation planning and design-system scope discovery.
- Accepted Execution Evidence: The preserved canonical Dev Orchestrator accepted the recovered reservation after the configured MCP catalog refreshed to revision `cff1fd094bd840c97adb17b079cc118d1d1d4d0621cdc3a6785b61fed1d2591e` and resolved `review-documentation-design-system` version `1.0.0`.
- Next Action: Resume the bounded implementation and TDD plan, then route it through independent technical review before source mutation.
