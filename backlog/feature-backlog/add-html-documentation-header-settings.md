# Add Settings Popup To HTML Documentation Headers

Status: Proposed

Type: Feature

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

## Notes

- This item covers the shared settings experience and its integration with existing HTML documentation viewers. It does not require adding harness-specific display choices to pages that do not already have them.
