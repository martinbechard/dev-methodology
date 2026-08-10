# Historical Provenance Migration for Agent and Skill Definitions

Owner: Unowned

Status: User Action Required

Type: Defect

Provider: file

Work Item ID: migrate-agent-and-skill-definitions-historical-provenance

Completion: main-branch

## Summary

Establish authorized historical creation provenance for design/agent-and-skill-definitions.html without inferring or replacing unavailable creation facts.

## Context

The page is a governed maintained HTML document under PROJECT.yaml but has no creation-provenance comment after its doctype. The omission exists in both the pre-review base and the current text-correction candidate. Direct historical provenance validation therefore reports that the creation provenance HTML comment is missing.

The document-provenance skill treats historical migration as an explicit state, never as a fallback for an ordinary edit. It requires retained evidence for historical fields and prohibits deriving creation identity from the current model profile, Git author data, current configuration, or model-authored prose. No authorized historical-migration envelope or retained creation record is available in the current text-review lane.

## Source Evidence

Fresh Methodology Artifact Reviewer evidence in canonical Codex task 019fe928-e316-7833-bd7d-44af8c0bc89d on 2026-08-10 reported the missing comment at design/agent-and-skill-definitions.html:1-2 while reviewing candidate 40e4b07bbcdacc7c4c4c8f1871333502c6278c0a for Work Item review-agent-and-skill-definitions-text.

The ordinary-edits contract in skills/document-provenance/SKILL.md requires creation provenance to remain unchanged during ordinary edits. The historical-migration contract requires explicit authorization and evidence classification before adding a block to an existing document.

## Requirements

- Identify retained historical evidence, if any, for Artifact-ID, Created-UTC, Creating-Agent, Runtime, Dispatched-Model, Reasoning-Effort, and Task-ID.
- Obtain explicit authority for historical migration of this maintained page.
- Use only evidence labels permitted by the document-provenance historical-migration contract; record historical-unknown for facts that authorized evidence cannot establish.
- Add the canonical hidden HTML provenance block immediately after the doctype without changing visible page content.
- Keep ordinary modification history in Git and do not add mutable modification fields to the creation block.
- Do not derive historical values from current runtime configuration, model mappings, Git authorship, or this review task.

## Acceptance Criteria

- The page contains one canonical provenance comment in the required location.
- Every historical creation field has allowed retained evidence or an authorized historical-unknown classification.
- Deterministic historical validation passes with the exact project copyright statement.
- Fresh independent review reports no inferred, unsupported, misplaced, or mutable provenance field.
- Page rendering, accessibility, navigation, and generated catalog behavior remain unchanged.

## Dependencies

None.

## Verification

- Run the document-provenance validator in historical mode against design/agent-and-skill-definitions.html.
- Verify the doctype remains first and the provenance comment is immediately before the html element.
- Run the page's focused HTML, navigation, fragment, and bundle-content checks.
- Run Git diff checks and confirm that visible text is unchanged unless separately authorized.

## Open Questions

- Which retained source, if any, proves the page's original creation identity?
- If one or more creation facts are unavailable, do you authorize the historical-unknown evidence state for those fields?

## User Action Required

Historical migration needs explicit authority and an evidence disposition before implementation.

## Question for the User

Do you authorize historical provenance migration for design/agent-and-skill-definitions.html using retained evidence where available and historical-unknown for creation facts that cannot be established?

Asked At: 2026-08-10T01:50:00Z

Asked In: Parent coordination task 019fb057-1767-7ef2-b5fa-41f4417b20b3

## Why User Input Is Required

The current Work Item authorizes text review and ordinary correction, not reconstruction of historical creation identity. Adding a provenance block without this authority would require invented or unsupported values.

## Options and Tradeoffs

- Authorize migration with historical-unknown: Complete a truthful block even where original creation facts cannot be recovered.
- Authorize migration only with retained evidence: Hold the item until every required historical fact has named evidence.
- Defer: Keep the page's existing missing-provenance state and leave this item in Holding.
- Decline: Archive the item as Abandoned while retaining the validator finding.

## Resolution

Pending.

## Unattended Work Boundary

Do not add, infer, remove, or alter provenance in design/agent-and-skill-definitions.html until the user authorizes a historical evidence strategy. The related text-review Work Item may continue only through ordinary text correction and fresh independent review that accepts this separate pre-existing disposition.

## Notes

- Related Work Item: review-agent-and-skill-definitions-text.
- Separate category-order defect: reconcile-agent-skill-hierarchy-category-order.
