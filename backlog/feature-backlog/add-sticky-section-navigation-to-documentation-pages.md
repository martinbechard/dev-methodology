# Add Sticky Section Navigation To Documentation Pages

Status: Starting

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

## Current Dispatch Reservation

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

This item applies to HTML documentation detail pages linked from the toolkit index. It does not add a section menu to the root index page, whose primary purpose is choosing a document rather than navigating a long document body.
