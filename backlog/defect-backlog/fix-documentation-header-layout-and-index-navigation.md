# Fix Documentation Header Layout And Index Navigation

Status: Running

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/fix-documentation-header-layout-and-index-navigation.md

Completion: direct-main

## Summary

Make the HTML documentation header intuitive by placing the settings control in the right-hand corner and using the linked toolkit title as the single control for returning to the documentation index.

## Context

On design/agent-and-skill-definitions.html, the shared settings script appends the settings control to the site header, but the current header layout leaves the control below the linked toolkit title instead of at the far right. The same page also presents two links to ../index.html: the site-brand title and a separate Back to Documentation Index link in the document navigation.

This duplicates the index action and weakens the visual relationship between the title, settings control, and page navigation. The shared documentation conventions and generated Agent and Skill Evaluations page contain the same brand and redundant index-navigation pattern, so implementation must update owning sources rather than leave inconsistent detail pages or hand-edit generated output.

## Source Evidence

Direct user request in Codex task 019fae77-d530-7361-b1c6-36f87f3d6e28 on 2026-07-29: "The settings icon should be in the righthand corner of the page for intuitiveness. The Back to Documentation Index button is redundant with the link in the title. The title should be the back button: AI-Assisted Coding Toolkit Index." The request included a screenshot of design/agent-and-skill-definitions.html showing the current stacked settings control and redundant index link.

## Requirements

- Place the settings trigger at the far right of the site header on HTML documentation detail pages.
- Preserve the settings trigger's existing accessible name, keyboard behavior, dialog behavior, and saved-setting behavior.
- Keep the site-brand title as the link to the documentation index and change its visible label to exactly AI-Assisted Coding Toolkit Index.
- Remove the separate Back to Documentation Index link from the document navigation.
- Preserve previous, next, and other page-specific navigation controls after removing the redundant index link.
- Apply the corrected shared header and navigation pattern consistently across the HTML documentation detail pages.
- Update authoritative generators or source templates for generated pages instead of hand-editing generated output.
- Preserve a clear, usable header layout at desktop and narrow viewport widths.

## Acceptance Criteria

- On design/agent-and-skill-definitions.html, the settings trigger appears in the right-hand corner of the header rather than below the site-brand link.
- The linked header label reads AI-Assisted Coding Toolkit Index and returns to ../index.html.
- No separate Back to Documentation Index control appears in the page's documentation navigation.
- Previous, next, and page-specific navigation controls remain present and functional.
- Every in-scope HTML documentation detail page uses the same corrected header label, settings placement, and nonredundant index-navigation pattern.
- Generated documentation reproduces the corrected pattern from its authoritative generator without freshness drift.
- The header remains readable and operable with keyboard navigation and at representative desktop and mobile viewport widths.

## Dependencies

None.

## Verification

- Add or update focused documentation tests for the exact linked title label, absence of the redundant index link, preservation of sequence navigation, and shared settings-control integration.
- Regenerate generated HTML documentation and run its freshness checks.
- Run the directly affected documentation markup, link, and accessibility checks.
- Verify the header visually at representative desktop and mobile viewport widths, including keyboard access to the settings dialog and activation of the title link.
- Run git diff validation for the implementation change.

## Open Questions

None.

## Expired Dispatch Reservation

Transition: Ready -> Starting.

Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758.

Launch Reservation: One bounded launch reservation.

Normalized Objective: Make the HTML documentation header intuitive by placing the settings control in the right-hand corner and using the linked toolkit title as the single control for returning to the documentation index.

Dispatch Time: 2026-07-29T15:49:52Z.

Intended Root Role: Root Dev Orchestrator.

Owner: Unowned pending root acceptance.

Runtime Launch Result: Not attempted.

Canonical Conversation: None.

Owner Acceptance: None.

Reconciliation: Pending.

## Startup Reconciliation

Transition: Starting -> Ready.

Reconciled At: 2026-07-29T15:53:00Z.

Settlement Deadline: 2026-07-29T15:50:52Z.

Delayed Canonical Conversation and Root Agent Task: 019fae92-0f9c-73d1-8061-b64d453c503a.

Delayed Owner Acceptance: Observed at 2026-07-29T15:51:19Z, 27 seconds after the settlement deadline; invalid for the expired reservation.

Source Mutation Evidence: None observed. No source mutation was authorized or performed under the expired reservation.

Reservation Disposition: Expired reservation cleared. No replacement launch was created.

Reconciliation: Ready.

## Current Dispatch Reservation (Existing Canonical Conversation)

Transition: Ready -> Starting.

Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758.

Launch Reservation: One bounded resume reservation for the existing canonical conversation; no new conversation creation is authorized.

Normalized Objective: Make the HTML documentation header intuitive by placing the settings control in the right-hand corner and using the linked toolkit title as the single control for returning to the documentation index.

Dispatch Time: 2026-07-29T15:54:20Z.

Intended Root Role: Root Dev Orchestrator.

Canonical Conversation: 019fae92-0f9c-73d1-8061-b64d453c503a.

Canonical Root Agent Task: 019fae92-0f9c-73d1-8061-b64d453c503a.

Worktree: /Users/martinbechard/.codex/worktrees/b423/dev-methodology.

Owner: Unowned pending root acceptance.

Runtime Launch Result: Existing canonical conversation observed and ready for resume.

Owner Acceptance: Pending.

Reconciliation: Pending.

## Starting Settlement Evidence (Existing Canonical Conversation)

Settlement Window: 2026-07-29T15:54:20Z to 2026-07-29T15:55:20Z (exactly 60 seconds).

Runtime Launch Result: Existing canonical conversation observed and ready for resume.

Canonical Conversation: 019fae92-0f9c-73d1-8061-b64d453c503a.

Owner Acceptance: Pending.

Reconciliation: Pending.

## Current Running Acceptance

Transition: Starting -> Running.

Root Dev Orchestrator: Root Dev Orchestrator 019fae92-0f9c-73d1-8061-b64d453c503a.

Canonical Conversation and Root Agent Task: 019fae92-0f9c-73d1-8061-b64d453c503a.

Worktree: /Users/martinbechard/.codex/worktrees/b423/dev-methodology.

Branch: Detached HEAD.

Clean Worktree HEAD: 0fefbb23d1ab19da9aca62098d8e4474264db601.

Accepted At: 2026-07-29T15:55:04Z.

Reconciliation Result: Running.

## Active Execution Evidence

Condition Type: root-execution.

Owner: Root Dev Orchestrator 019fae92-0f9c-73d1-8061-b64d453c503a.

Evidence: Accepted awaiting durable lifecycle.

Observed/Started: 2026-07-29T15:55:04Z.

Deadline: 2026-07-29T16:25:00Z.

Next Action: Attach Codex branch, then focused implementation.

Next Reconciliation: Immediately after lifecycle commit or blocker, and no later than 15 minutes.

## Starting Settlement Evidence

Settlement Window: 2026-07-29T15:49:52Z to 2026-07-29T15:50:52Z (exactly 60 seconds).

Runtime Launch Result: Not attempted.

Canonical Conversation: None.

Owner Acceptance: None.

Reconciliation: Pending.

## Notes

This defect refines the shared experience delivered by backlog/completed-backlog/features/add-html-documentation-header-settings.md. It does not change the settings choices, persistence keys, or popup contents.
