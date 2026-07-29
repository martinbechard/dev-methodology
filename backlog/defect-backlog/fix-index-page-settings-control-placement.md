# Fix Index Page Settings Control Placement

Status: Starting

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/fix-index-page-settings-control-placement.md

Completion: direct-main

## Summary

Place the settings cog in the right-hand corner of the AI-Assisted Coding Toolkit index-page header so the index uses the same intuitive header alignment as the documentation detail pages.

## Context

The root index.html loads design/documentation-settings.js and contains the same site-header and site-brand structure used by the documentation detail pages. The shared settings script appends the settings control to that header, but the current index-page layout renders the cog on a separate line below the linked toolkit brand instead of at the far right.

The completed defect backlog/completed-backlog/defects/fix-documentation-header-layout-and-index-navigation.md corrected settings placement and index navigation on documentation detail pages. Its requirements deliberately scoped the placement fix to detail pages, leaving the root index page with the original stacked layout.

## Source Evidence

Direct user request in Codex task 019faec4-1462-7ca2-b964-47706bf1cdc3 on 2026-07-29: "ok but the index page's settings cog needs to also be fixed - create a new item for that." The request included a screenshot of index.html showing the settings cog below the AI-Assisted Coding Toolkit brand instead of in the header's right-hand corner.

## Requirements

- Place the settings trigger at the far right of the site header on index.html.
- Keep the AI-Assisted Coding Toolkit brand and settings trigger aligned as one header row at desktop widths.
- Preserve the settings trigger's accessible name, keyboard behavior, dialog behavior, and saved-setting behavior.
- Preserve the index page's existing toolkit title, document cards, links, and footer content.
- Keep the header readable and operable at narrow viewport widths without overlap, clipping, or unusable controls.
- Reuse or align with the corrected detail-page header convention without regressing either page type.

## Acceptance Criteria

- On index.html, the settings cog appears in the right-hand corner of the site header rather than below the toolkit brand.
- The linked AI-Assisted Coding Toolkit brand remains visible and functional.
- Opening, operating, and closing the settings dialog works with pointer and keyboard input.
- The header remains usable at representative desktop and mobile viewport widths.
- Documentation detail pages retain their corrected settings placement and navigation behavior.
- No index-page document card, link, title, or footer content changes as a side effect.

## Dependencies

None.

## Verification

- Add or update focused documentation tests for the index-page header structure and shared settings-control integration.
- Verify visually at representative desktop and mobile viewport widths that the brand remains left-aligned and the settings trigger is right-aligned.
- Verify keyboard access, focus return, Escape behavior, and the settings dialog's accessible label on index.html.
- Run the directly affected documentation markup and accessibility checks.
- Run git diff validation for the implementation change.

## Open Questions

None.

## Current Dispatch Reservation

Transition: Ready -> Starting.

Parent Coordination Thread: 019faec8-943a-7902-adaa-c2c00a370169.

Launch Reservation: One bounded launch reservation for the canonical work-item conversation; no additional conversation creation is authorized.

Normalized Objective: Place the settings cog in the right-hand corner of the AI-Assisted Coding Toolkit index-page header so the index uses the same intuitive header alignment as the documentation detail pages.

Dispatch Time: 2026-07-29T16:53:43Z.

Intended Root Role: Root Dev Orchestrator.

Canonical Conversation and Root Agent Task: 019faec8-943a-7902-adaa-c2c00a370169.

Direct Conversation-Title Handoff: Fix Index Page Settings Control Placement.

Branch: codex/fix-index-page-settings-control-placement.

Worktree: /Users/martinbechard/.codex/worktrees/1bad/dev-methodology.

Private Baseline: 961af38d (clean HEAD/main observed before recovery baton).

Owner: Unowned pending accepted root.

Runtime Launch Result: Direct conversation-title handoff observed; Root Dev Orchestrator accepted the launch handshake at 2026-07-29T16:51:49.385631Z.

Owner Acceptance: Pending.

Reconciliation: Pending.

## Starting Settlement Evidence

Settlement Window: 2026-07-29T16:53:43Z to 2026-07-29T16:54:43Z (exactly 60 seconds).

Runtime Launch Result: Direct conversation-title handoff observed; Root Dev Orchestrator accepted the launch handshake at 2026-07-29T16:51:49.385631Z.

Canonical Conversation: 019faec8-943a-7902-adaa-c2c00a370169.

Owner Acceptance: Pending.

Reconciliation: Pending.

## Notes

This item is limited to the root index-page settings-control placement. It does not reopen the completed detail-page navigation defect or change the available settings and persistence contract.
