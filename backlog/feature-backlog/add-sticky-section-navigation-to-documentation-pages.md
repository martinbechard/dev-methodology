# Add Sticky Section Navigation To Documentation Pages

Status: Running

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/add-sticky-section-navigation-to-documentation-pages.md

Completion: direct-main

## Summary

Apply the evaluation page's floating page-section navigation pattern to the other HTML documentation detail pages so readers can move directly to any major part of a long page.

## Context

design/agent-and-skill-evaluations.html presents its page structure in a sticky, horizontally arranged navigation menu labeled Page sections. Each entry links to a major section anchor, the menu remains available while scrolling at desktop widths, and the page provides scroll offsets so linked headings are not hidden behind the menu.

The HTML detail pages linked from index.html generally contain multiple top-level sections with stable headings, but most do not expose an equivalent page-section menu. design/orchestrated-development-lifecycle.html already has a chapter navigator, so implementation must align or preserve that useful existing behavior rather than add a duplicate control.

## Source Evidence

Direct user request in Codex task 019faec4-1462-7ca2-b964-47706bf1cdc3 on 2026-07-29: "The structure of the agent-and-skills-evaulation.html page is presented as a floating menu on that page. That makes it easy to navigate to any part of the page. This is very useful. Create an item to apply the same patter on the other documentation pages." The request included a screenshot of the sticky Page sections menu on design/agent-and-skill-evaluations.html while viewing the Campaign receipt and results section.

## Requirements

- Add one page-section navigation menu to every HTML documentation detail page linked from index.html, excluding design/agent-and-skill-evaluations.html because it already owns the reference implementation.
- Populate each menu from that page's major top-level content sections using concise labels that accurately match the visible headings.
- Link every menu entry to a unique, stable section anchor on the same page.
- Keep the section menu available while scrolling at representative desktop widths, following the evaluation page's floating or sticky interaction pattern.
- Ensure anchored headings remain visible below the sticky menu after direct navigation.
- Preserve or align an existing page-owned chapter navigator, including the one in design/orchestrated-development-lifecycle.html, instead of rendering a second competing menu.
- Preserve the separate previous and next documentation navigation controls.
- Support keyboard navigation, visible focus, meaningful navigation labeling, and correct link semantics.
- Provide usable narrow-viewport behavior without clipped or unreachable entries.
- Hide or simplify the page-section navigation for print so it does not obscure document content.
- Update authoritative generators or source templates when an in-scope page is generated; do not hand-edit generated output.
- Keep the navigation presentation and interaction conventions consistent while allowing each page to retain its own section labels and information structure.

## Acceptance Criteria

- Every HTML documentation detail page linked from index.html has exactly one page-section or chapter-navigation menu.
- Each menu provides a working link for every major top-level section on its page and does not link to missing or duplicate anchors.
- design/agent-and-skill-evaluations.html retains its existing Page sections behavior as the reference experience.
- design/orchestrated-development-lifecycle.html retains one coherent chapter navigator rather than gaining a duplicate.
- Activating a section link places the corresponding heading visibly below the sticky navigation at desktop widths.
- All menu entries are reachable and operable using a keyboard and expose a meaningful navigation landmark label.
- The menus remain usable at representative desktop and mobile viewport widths and do not cover page content.
- Previous and next document navigation continues to work on every page.
- Generated pages reproduce the accepted menus and anchors from their authoritative sources without freshness drift.

## Dependencies

None.

## Verification

- Add focused tests that inventory every index-linked HTML detail page and require exactly one page-section or chapter-navigation landmark.
- Verify that menu links resolve to unique anchors and correspond to the page's major top-level sections.
- Verify generated-page source ownership and freshness for every generated page affected by the implementation.
- Run directly affected documentation markup, link, and accessibility checks.
- Verify keyboard operation, focus visibility, sticky scroll behavior, anchor offsets, and previous or next navigation in a browser.
- Verify representative desktop and mobile viewport layouts and print rendering.
- Run git diff validation for the implementation change.

## Open Questions

None.

## Notes

## Missed-Settlement Reconciliation

Transition: Starting -> Ready.
Reconciled At: 2026-07-29T17:38:47Z.
Settlement Deadline: 2026-07-29T17:36:38Z.
Canonical Conversation and Root Agent Task: 019faef0-2663-7e50-a6ab-0de973661fbf.
Owner: Unowned.
Canonical Acceptance: None observed.
Source Mutation Evidence: None observed.
Required Resumption: Reuse the same canonical task through a new Ready -> Starting -> Running sequence.
Reconciliation: Ready.

## Historical Dispatch Reservation

Transition: Ready -> Starting.
Parent Coordination Thread: 019faef0-2663-7e50-a6ab-0de973661fbf.
Launch Reservation: One synchronized bounded launch reservation in the adaptive-capacity batch.
Normalized Objective: Add sticky section navigation to documentation pages.
Dispatch Time: 2026-07-29T17:35:38Z.
Intended Root Role: Root Dev Orchestrator.
Canonical Conversation and Root Agent Task: 019faef0-2663-7e50-a6ab-0de973661fbf.
Direct Conversation-Title Handoff: Add Sticky Section Navigation To Documentation Pages.
Branch: codex/add-sticky-section-navigation-to-documentation-pages.
Worktree: /Users/martinbechard/.codex/worktrees/cf9b/dev-methodology.
Owner: Unowned pending accepted root.
Required Next Lifecycle Transition: The same root Dev Orchestrator must separately accept Starting -> Running before repository mutation.
Reconciliation: Pending.

## Starting Settlement Evidence

Settlement Window: 2026-07-29T17:35:38Z to 2026-07-29T17:36:38Z (exactly 60 seconds; shared adaptive-capacity batch window).
Runtime Launch Result: Direct conversation-title handoff accepted for the synchronized batch.
Canonical Conversation: 019faef0-2663-7e50-a6ab-0de973661fbf.
Owner Acceptance: Pending.
Reconciliation: Pending.

## Current Dispatch Reservation

Transition: Ready -> Starting.

Parent Coordination Thread: 019fb057-1767-7ef2-b5fa-41f4417b20b3.

Launch Reservation: One parent-coordinator launch reservation; no runtime work-item Thread has been created by this reservation.

Normalized Objective: Add sticky documentation section navigation.

Dispatch Time: 2026-08-05T14:16:41.530718Z.

Intended Root Dev Orchestrator: Dev Orchestrator.

Runtime Launch Evidence: None. This provider transaction reserves capacity only and does not create or accept a runtime task.

Owner: Unowned.

Reconciliation: Starting reservation recorded by the parent Coordinator's Dev Backlog Steward.

## Running Acceptance

Transition: Starting -> Running.

Parent Coordination Thread: 019fb057-1767-7ef2-b5fa-41f4417b20b3.

Canonical Work-Item Thread and Root Agent Task: 019faef0-2663-7e50-a6ab-0de973661fbf.

Root Dev Orchestrator: Dev Orchestrator.

Owner: Root Dev Orchestrator 019faef0-2663-7e50-a6ab-0de973661fbf.

Branch: codex/add-sticky-section-navigation-to-documentation-pages.

Worktree: /Users/martinbechard/.codex/worktrees/cf9b/dev-methodology.

Phase: Provider acceptance complete; implementation may begin.

Accepted At: 2026-08-05T14:21:37.470068Z.

Claim Evidence: Shared-checkout exact-file claim starting-running-sticky-section-navigation-019faef0 acquired as journal event b49086b8-dd27-41dc-a330-3ea774b90234.

Reconciliation: Running acceptance recorded by the canonical root Dev Orchestrator's Dev Backlog Steward.

## Confirmed In-Scope Defect

Observed At: 2026-08-05T14:37:18.079111Z.

Scope: Print media for design/orchestrated-development-lifecycle.html.

Evidence: Its single nav[aria-label="Lifecycle chapters"] remains visible in print because the existing print CSS does not include .chapter-nav. The computed display under emulated print media was flex.

Expected: The lifecycle chapter navigator has computed display none in print, matching the print-hidden section and chapter menus on the other index-linked documentation pages.

Reproduction: Serve the current candidate, open design/orchestrated-development-lifecycle.html, emulate print media, and inspect the computed display of nav[aria-label="Lifecycle chapters"].

Runnable Next Action: Add .chapter-nav to that page's existing print-hide rule, without changing its chapter links, sticky desktop behavior, or previous and next controls; rerun focused inventory and browser print checks.

## Confirmed In-Scope Defect: Parser Verification Gap

Evidence Source: Fresh independent source review.

Scope: The focused nine-page documentation navigation inventory test.

Evidence: DocumentationNavigationParser records declared aria-labelledby section targets and navigation fragments but does not inventory actual element IDs or previous and next link destinations. Its current assertions can therefore accept missing or duplicate section anchors and broken or missing adjacent-document hrefs.

Reproduction: A malformed fixture with section aria-labelledby="missing-heading", h2 id="different-heading", section-nav href="#missing-heading", and document-nav href="missing-page.html" satisfies the current assertions.

Expected: The focused test rejects that fixture and every equivalent mismatch.

Runnable Next Action: Extend the focused parser and test to inventory all element IDs, reject duplicates, require every section-nav fragment to resolve to an actual unique ID, and require every previous and next href to resolve to the expected adjacent index-linked detail page. Keep the nine-page scope and do not run a broad suite.

This item applies to HTML documentation detail pages linked from the toolkit index. It does not add a section menu to the root index page, whose primary purpose is choosing a document rather than navigating a long document body.
