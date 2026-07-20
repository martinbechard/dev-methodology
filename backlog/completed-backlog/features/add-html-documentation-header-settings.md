# Add Settings Popup To HTML Documentation Headers

Status: Completed

Type: Feature

## Current Execution

- Canonical Dev Orchestrator task: 019f7e76-9f7d-77d0-8a0e-ca2b95065370.
- Worktree: /Users/martinbechard/.codex/worktrees/5a4d/dev-methodology.
- Phase: delivered, verified, reviewed, integrated, and archived; parent cleanup is eligible.

## Summary

Add a settings popup to the header of the HTML documentation so readers can choose their default agent harness and preferred editor. Persist the choices in browser local storage and restore them when documentation pages load.

## Context

The HTML documentation contains views where readers can choose how harness-specific content is displayed and can open Markdown or YAML source files in an editor. The current agent definition viewer selects Codex when a Codex invocation is available, while the skill, agent, and template viewers default editor links to VS Code unless an editor query parameter is supplied. Readers must currently repeat these choices across pages and visits.

The settings must apply only where a documentation view offers the corresponding choice. Pages without harness-specific display or editable Markdown or YAML content do not need additional behavior beyond exposing the shared settings control.

## Requirements

- Add a cog control to the HTML documentation header that opens a settings popup.
- Make the cog control and popup keyboard accessible and provide an accessible Settings label.
- Provide a Default harness setting for documentation views that offer a harness-specific display choice.
- Default the harness setting to Codex when no saved preference exists, preserving the current agent definition viewer behavior.
- Apply the saved harness preference only when the selected harness is available in the current view; otherwise use that view's existing fallback behavior.
- Provide an Editor setting for opening Markdown and YAML source files.
- Offer VS Code and IntelliJ as editor choices.
- Default the editor setting to VS Code when no saved preference exists.
- Use the selected editor for applicable Edit links in the skill, agent, and documentation template viewers.
- Store both settings in browser local storage whenever they change.
- Retrieve and apply both settings when an HTML documentation page loads.
- Handle missing, invalid, or unavailable local-storage values by restoring the documented defaults without breaking the page.
- Keep the settings behavior and storage keys consistent across the HTML documentation pages.

## Acceptance Criteria

- Every HTML documentation header displays a cog control that opens the settings popup.
- The popup exposes one default-harness choice and one editor choice.
- A first-time visitor receives Codex as the default harness and VS Code as the default editor.
- Selecting another available harness changes the initial harness-specific display on applicable views.
- Selecting IntelliJ causes applicable Markdown and YAML Edit links to target IntelliJ instead of VS Code.
- Reloading the current page and navigating to another HTML documentation page restores both saved choices.
- A saved harness that is unavailable on a page does not leave the page blank or prevent other harness content from being displayed.
- Invalid or inaccessible local-storage state does not prevent the documentation page, header, popup, or Edit links from working.
- The cog control and popup can be opened, operated, and closed using a keyboard and expose meaningful accessible names and state.

## Dependencies

None.

## Verification

- Add focused automated coverage for default selection, saving, retrieval, invalid stored values, and unavailable harness fallback.
- Verify VS Code and IntelliJ Edit-link generation for representative Markdown and YAML sources.
- Manually verify persistence across reloads and navigation between documentation pages.
- Manually verify keyboard operation, focus handling, Escape behavior, and accessible labels for the cog control and popup.
- Run the repository documentation checks and git diff validation required for the implementation changes.

## Delivery Evidence

- Accepted candidate: 1f450ad92768bc80bfd60e0b7b56fdc9762e6ec7 on branch codex/add-html-doc-header-settings in the recorded private worktree.
- Independent review: the first reviewer found an invalid IntelliJ URL shape in candidate a1b3caceed3ac9a551a6d9c2e097e8da4b09f70e; correction 1f450ad92768bc80bfd60e0b7b56fdc9762e6ec7 added editor-specific URL generation and final-link tests, and a different fresh reviewer accepted the corrected candidate with no findings.
- Main integration: accepted commits were cherry-picked as 214531b and 52248882adffb7fe9e66a63447d35e4935fd4868.
- Focused post-integration verification: eight documentation settings behavior tests passed, all 88 scripts.test_bundle_content tests passed, syntax checks passed for the four changed browser JavaScript files, and git diff validation passed.
- Browser verification: the shared control appeared on the documentation index and design pages; keyboard opening, Escape close, focus return, first-visit defaults, reload and cross-page persistence, saved harness application, unavailable-view fallback, and VS Code and IntelliJ links for representative role YAML, skill Markdown, and template YAML sources were verified. Browser and port resources were released at claim event 3a6a4856-6b66-4ef1-a1da-065fd6a7582b.
- Integration ownership: exact 14-path main integration claim released at event a84ffaaa-3a98-4f17-8c95-bf11509612d9.
- Completion ownership: exact active and completed backlog paths were acquired at event 61fb8bc6-0c99-4550-8450-51b22d7c76a2 after structured PRIMARY_REQUIRED events cf701402-0eb6-4927-a9ec-80e9f8ae60e4, db13ee88-6841-4fa7-bc55-82af7f410859, and c743a6c4-700f-43a3-b72c-4f4526a915be.
- Open issues: none. The private worktree is clean and the accepted branch is patch-equivalent to main, so parent cleanup may remove both after this terminal commit and claim release.

## Notes

- This item covers the shared settings experience and its integration with existing HTML documentation viewers. It does not require adding harness-specific display choices to pages that do not already have them.
