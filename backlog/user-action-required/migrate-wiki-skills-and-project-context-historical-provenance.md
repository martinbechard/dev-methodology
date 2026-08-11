# Migrate Wiki Skills and Project Context Historical Provenance

Status: User Action Required

Type: Defect

Provider: file

Work Item ID: migrate-wiki-skills-and-project-context-historical-provenance

Completion: main-branch

## Summary

Add truthful historical creation provenance to design/wiki-skills-and-project-context.html so the governed document satisfies the repository's maintained-document provenance contract.

## Context

PROJECT.yaml and generated root guidance govern maintained HTML under design. The document-provenance skill requires a canonical hidden provenance block immediately after the doctype. design/wiki-skills-and-project-context.html has no such block.

The completed Work Item review-wiki-skills-and-project-context-text preserved the absence because its content-only scope supplied neither historical-migration authority nor a provenance envelope. The omission is therefore a confirmed pre-existing defect, not an accepted exception or a text-review correction.

## Source Evidence

During Work Item review-wiki-skills-and-project-context-text, independent source review and verification confirmed that design/wiki-skills-and-project-context.html lacks its required provenance block. The completed provider record preserved this residual gap at backlog/completed-backlog/features/html-documentation-review-and-design-alignment/review-wiki-skills-and-project-context-text.md.

On 2026-08-11 in canonical task 019ff2f9-0863-7133-aac0-ff3cb81dab14, the user stated that the missing provenance requires durable ownership and then directed: "we need two defects: one we already discussed ... Please create the defects now." The user also clarified that an independently discovered defect should be placed in the backlog with User Action Required until implementation is authorized.

## Requirements

- Apply the document-provenance historical-migration procedure to design/wiki-skills-and-project-context.html.
- Use retained evidence for each creation field and use only the procedure's authorized historical-unknown or migration-assigned values when stronger evidence is unavailable.
- Preserve the doctype as the first construct and place the canonical provenance comment immediately after it.
- Preserve the accepted semantic baseline established by delivery commit 97c27b5c8c3c5d2d9a650b1b2c6a2c3f5a657689.
- Do not perform page-wide visual migration or unrelated content changes.

## Acceptance Criteria

- The page contains exactly one canonical provenance block in the required HTML location.
- Every provenance value and evidence label is supported by retained historical-migration evidence or an explicitly authorized unknown state.
- Deterministic document-provenance validation passes in historical mode.
- Focused HTML, navigation, local-link, and accepted-content checks still pass.
- Fresh independent review finds no invented historical identity or semantic drift.

## Dependencies

None.

## Verification

- Run the document-provenance validator in historical mode for design/wiki-skills-and-project-context.html.
- Run the focused HTML documentation contract tests that consume the page.
- Compare visible and accessibility-bearing text with delivery commit 97c27b5c8c3c5d2d9a650b1b2c6a2c3f5a657689.
- Run git diff checks for the exact changed paths.

## Open Questions

- Which retained creation evidence is stronger than historical-unknown for each provenance field?

## User Action Required

### Question for the User

Do you approve proceeding with the historical provenance migration for design/wiki-skills-and-project-context.html under the document-provenance historical-migration rules?

### Why User Input Is Required

The defect is confirmed, but altering historical creation metadata requires explicit migration authority. Proceeding without approval would invent authority to assign or correct historical provenance.

### Options and Tradeoffs

- Approve: move this defect to the active defect backlog as Ready and perform a bounded historical migration using retained evidence and authorized unknown states.
- Defer: move the defect to Holding; the page remains usable but nonconforming.
- Decline: archive the defect as abandoned and retain the provenance exception as an explicit accepted gap.

### Resolution

Pending.

### Unattended Work Boundary

Do not alter the provenance block or creation metadata in design/wiki-skills-and-project-context.html until the user approves. Read-only historical evidence discovery may continue.
