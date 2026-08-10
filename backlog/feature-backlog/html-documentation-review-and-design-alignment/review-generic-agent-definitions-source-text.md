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

Condition Type: root-execution

Owner: Dev Orchestrator in Codex task /root/review_generic_agent_defs

Evidence: The canonical root execution accepted the reserved item, created isolated branch codex/review-generic-agent-definitions-source-text-orchestrator at main commit 9488c71873e19c99b523927bce14ec64da634158, and acquired the exact file-provider update claim.

Observed At: 2026-08-10T00:50:12Z

Started At: 2026-08-10T00:49:51Z

Deadline or Expires At: 2026-08-10T04:49:51Z

Next Action: Inventory the target page and authoritative sources, then dispatch the bounded source-text correction lane.

Next Reconciliation At: 2026-08-10T00:59:00Z

Codex Task ID: /root/review_generic_agent_defs

Conversation ID: Not exposed by the Codex task runtime

Root Role: Dev Orchestrator

Parent Task ID: 019fb057-1767-7ef2-b5fa-41f4417b20b3

Branch: codex/review-generic-agent-definitions-source-text-orchestrator

Worktree: /Users/martinbechard/dev/dev-methodology/.worktrees/review-generic-agent-definitions-source-text-start-update

Phase: Inventory and implementation dispatch

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
