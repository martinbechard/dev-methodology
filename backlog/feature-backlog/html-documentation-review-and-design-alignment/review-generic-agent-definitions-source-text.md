# Review and Correct Generic Agent Definitions Source Text

Owner: Dev Orchestrator

Status: Running

Type: Feature

Provider: file

Work Item ID: review-generic-agent-definitions-source-text

Completion: main-branch

Series: backlog/feature-backlog/html-documentation-review-and-design-alignment/index.md

## Starting Handoff Evidence

Parent Coordination Task: 019fb057-1767-7ef2-b5fa-41f4417b20b3

Dispatch Reservation: First normal multitask wave after terminology completion.

Normalized Objective: Review and correct all text in design/generic-agent-definitions-source.html before design alignment.

Dispatch Requested At: 2026-08-10T00:44:00Z

Intended Root Role: Dev Orchestrator

Launch Result: Reserved; canonical root launch follows this committed transition.

Last Contact: 2026-08-10T00:44:00Z

Next Reconciliation At: 2026-08-10T00:59:00Z

## Active Execution Evidence

Condition Type: delegated-work

Owner: Dev Orchestrator task 019fe929-3695-7d20-93dc-63852ced1020 coordinating original Dev Coder task /root/fix_generic_agent_test_contract

Evidence: Fresh code review returned GOOD. Fresh artifact review confirmed all three prior findings resolved in the HTML but returned NEEDS CORRECTION because test_context_budget_ownership_and_runtime_evidence_are_documented still requires the retired July 2026 Junie wording. The original Dev Coder is applying only that source-backed test-contract correction on immutable combined candidate e40a50fae05f8e26264269b7a6970512abf416e4.

Observed At: 2026-08-10T01:32:15Z

Started At: 2026-08-10T01:32:15Z

Deadline or Expires At: 2026-08-10T01:47:00Z

Next Action: Collect the one-path test correction, combine it into a new immutable candidate, and repeat fresh artifact and code review before independent verification.

Next Reconciliation At: 2026-08-10T01:43:00Z

Codex Task ID: 019fe929-3695-7d20-93dc-63852ced1020

Conversation ID: 019fe929-3695-7d20-93dc-63852ced1020

Root Role: Dev Orchestrator

Parent Task ID: 019fb057-1767-7ef2-b5fa-41f4417b20b3

Branch: codex/review-generic-agent-definitions-test-contract-round2-019fe929

Worktree: /private/tmp/review-generic-agent-definitions-test-contract-round2-019fe929

Phase: Correction round 2

## Summary

Review and correct all textual content in design/generic-agent-definitions-source.html before any page-wide Documentation Design System migration.

## Context

design/generic-agent-definitions-source.html is one of the eleven maintained user-facing HTML documentation pages in the repository navigation set. Text quality must be established before visual and structural alignment so design work does not preserve, obscure, or amplify incorrect content.

The review covers visible prose and every text-bearing interface or accessibility surface. If the page is generated or contains generated regions, identify its authoritative source and generator before mutation and regenerate the page instead of hand-editing owned output.

## Source Evidence

The user requested on 2026-08-09 in canonical task 019fb057-1767-7ef2-b5fa-41f4417b20b3 separate text-review work items for every HTML documentation page, followed by separate design-alignment items. The stated reason was that adjusting document design is pointless before the text content is correct.

Target page: design/generic-agent-definitions-source.html

## Requirements

- Inventory the page's information owners, authoritative repository sources, generated regions, navigation role, and intended audience before editing.
- Review the title, headings, summaries, body prose, callouts, tables, lists, captions, diagram text, labels, alternate text, accessible names, navigation wording, and footer text.
- Verify material claims against current canonical skills, conceptual Agent definitions, schemas, configuration, procedures, evaluation evidence, and generators as applicable.
- Apply the project Terminology Standard and applicable writing and review skills without changing exact identifiers, commands, file paths, schema fields, quotations, or source-native evidence.
- Correct stale facts, contradictions, missing context, ambiguous references, duplicated explanations, weak topic order, unsupported conclusions, and terminology drift.
- Preserve explicit unknowns and limitations when the sources do not justify a definitive statement.
- Change authoritative sources or generators for generated content, then regenerate the target page through supported commands.
- Preserve document provenance and update it only through the authorized runtime envelope.
- Obtain fresh independent documentation and methodology review of the corrected text.
- Do not perform page-wide visual migration or design-system component replacement in this item.

## Acceptance Criteria

- Every material statement is supported by current authoritative evidence or clearly labeled as an unknown, limitation, proposal, or example.
- The page uses preferred terminology consistently while preserving exact technical literals.
- Heading and topic order let the intended audience understand purpose, concepts, workflow, boundaries, and verification without reconstructing missing context.
- All text-bearing accessibility surfaces accurately describe their targets and do not duplicate or contradict visible content.
- Generated regions and pages match their authoritative sources and pass applicable freshness checks.
- Fresh independent review reports no unresolved material content, terminology, structure, or source-traceability finding.
- The accepted commit and source inventory are suitable as the immutable content baseline for Work Item align-generic-agent-definitions-source-with-documentation-design-system.

## Dependencies

None.

## Verification

- Run the applicable terminology, document-provenance, HTML-markup, local-link, fragment, and source-to-generated freshness checks for design/generic-agent-definitions-source.html.
- Run only the focused source or generator tests implicated by corrected content.
- Compare the final visible text and text-bearing accessibility attributes with the accepted source inventory.
- Obtain fresh independent documentation or methodology review and record its verdict.
- Run Git diff checks for the exact changed paths.

## Open Questions

- Which authoritative source owns each generated or catalog-derived region of design/generic-agent-definitions-source.html?
- Which page-specific content checklist is required in addition to general terminology and source-traceability review?

## Notes

- The dependent design item is align-generic-agent-definitions-source-with-documentation-design-system.
- Creation of this work item does not dispatch it while backlog crisis recovery remains active.
