# Review and Correct Agent and Skill Evaluations Text

Owner: Unowned

Status: User Action Required

Type: Feature

Provider: file

Work Item ID: review-agent-and-skill-evaluations-text

Completion: main-branch

Series: backlog/feature-backlog/html-documentation-review-and-design-alignment/index.md

Canonical Conversation: 019fe928-e2d9-73d3-a647-7fac38731628

Root Agent Task: 019fe928-e2d9-73d3-a647-7fac38731628

Branch: codex/review-agent-and-skill-evaluations-text-019fb057

Worktree: /Users/martinbechard/dev/dev-methodology/.worktrees/review-agent-skill-evals-text-work-019fb057

Candidate Commit: 5043884e3a2d31ca0c86be33338447a306004578

Phase: Fresh independent rereview and reverification

Started At: 2026-08-10T00:49:58Z

## Prior Active Execution Evidence

Condition Type: root-execution

Owner: Dev Orchestrator 019fe928-e2d9-73d3-a647-7fac38731628

Evidence: Visible Codex task 019fe928-e2d9-73d3-a647-7fac38731628 remains the active canonical root execution. Dev Coder assignment /root/evaluation_text_producer committed clean correction candidate 5043884e3a2d31ca0c86be33338447a306004578 after the fresh reviewer finding. The cumulative candidate remains limited to the same generator, focused test, and generated HTML paths; its 29 directly applicable tests, generator freshness, historical provenance validation, legacy-phrase rejection scan, and exact diff checks pass. The known unrelated Dev Backlog Steward source-contract test remains explicitly excluded without source or test weakening. Exact source claim review-agent-and-skill-evaluations-text-019fe928-source-paths-7 was released at clean candidate boundary. Fresh read-only Methodology Artifact Reviewer /root/evaluation_text_rereview and Dev Verifier /root/evaluation_text_reverify are independently evaluating the cumulative candidate from original baseline 292b55f9578d04438ce5c8d3b34c64b11af0f907, including a required retry of the aggregate terminology-provider load.

Observed At: 2026-08-10T02:04:14Z

Started At: 2026-08-10T00:57:00Z

Deadline or Expires At: 2026-08-10T04:57:00Z

Next Action: Reconcile the fresh rereviewer and reverifier terminal verdicts against candidate 5043884e3a2d31ca0c86be33338447a306004578, then either enter an explicitly bounded correction or begin main-branch delivery only after both acceptance gates are GOOD.

Next Reconciliation At: 2026-08-10T02:19:14Z

## User Action Required

Question: Do you approve running `python3 scripts/install-skills.py --adapter codex --scope user --install-agents --replace` to refresh the repository-owned user-level Codex skills and agents and update `/Users/martinbechard/.codex/config.toml` with the required `MCP_AGENT_OPS_REFERENCE_ROOTS` and `MCP_AGENT_OPS_REFERENCE_NAMES=terminology.md` configuration?

Why User Input Is Required: The active Codex MCP configuration omits both terminology reference settings, causing the mandatory aggregate `reference_load` review to fail with `reference_not_allowed`. The repository-supported installer is the available configuration repair, but its atomic user-scope operation also replaces the bundle-owned installed skills and Agent definitions and installs newly available bundle-owned artifacts. That persistent user-level mutation requires explicit approval.

Preserved Evidence: Clean candidate `5043884e3a2d31ca0c86be33338447a306004578` changes exactly `design/agent-and-skill-evaluations.html`, `scripts/build-agent-skill-evaluation-docs.py`, and `scripts/test_agent_skill_evaluation_docs.py`. Producer checks pass; the replacement reviewer reproduced only the provider configuration failure at catalog revision `bb1c7440506ced28c4ffa8fb00c89d9cb031a1208a80fbac12e4db2bce862ea7` and reported no candidate source defect before the provider gate stopped review.

Prohibited Unattended Action: Do not run the user-scope installer, hand-edit the Codex configuration, bypass the reference provider, or resume review until the user answers this exact question.

Asked At: 2026-08-10T02:12:00Z

Asked In: Parent coordination task 019fb057-1767-7ef2-b5fa-41f4417b20b3

Resolution: Pending

Approval Resolution: Pending

## Starting Handoff Evidence

Parent Coordination Task: 019fb057-1767-7ef2-b5fa-41f4417b20b3

Dispatch Reservation: First normal multitask wave after terminology completion.

Normalized Objective: Review and correct all text in design/agent-and-skill-evaluations.html before design alignment.

Dispatch Requested At: 2026-08-10T00:44:00Z

Intended Root Role: Dev Orchestrator

Launch Result: Reserved; canonical root launch follows this committed transition.

Last Contact: 2026-08-10T00:44:00Z

Next Reconciliation At: 2026-08-10T00:59:00Z

## Summary

Review and correct all textual content in design/agent-and-skill-evaluations.html before any page-wide Documentation Design System migration.

## Context

design/agent-and-skill-evaluations.html is one of the eleven maintained user-facing HTML documentation pages in the repository navigation set. Text quality must be established before visual and structural alignment so design work does not preserve, obscure, or amplify incorrect content.

The review covers visible prose and every text-bearing interface or accessibility surface. If the page is generated or contains generated regions, identify its authoritative source and generator before mutation and regenerate the page instead of hand-editing owned output.

## Source Evidence

The user requested on 2026-08-09 in canonical task 019fb057-1767-7ef2-b5fa-41f4417b20b3 separate text-review work items for every HTML documentation page, followed by separate design-alignment items. The stated reason was that adjusting document design is pointless before the text content is correct.

Target page: design/agent-and-skill-evaluations.html

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
- The accepted commit and source inventory are suitable as the immutable content baseline for Work Item align-agent-and-skill-evaluations-with-documentation-design-system.

## Dependencies

None.

## Verification

- Run the applicable terminology, document-provenance, HTML-markup, local-link, fragment, and source-to-generated freshness checks for design/agent-and-skill-evaluations.html.
- Run only the focused source or generator tests implicated by corrected content.
- Compare the final visible text and text-bearing accessibility attributes with the accepted source inventory.
- Obtain fresh independent documentation or methodology review and record its verdict.
- Run Git diff checks for the exact changed paths.

## Open Questions

- Which authoritative source owns each generated or catalog-derived region of design/agent-and-skill-evaluations.html?
- Which page-specific content checklist is required in addition to general terminology and source-traceability review?

## Notes

- The dependent design item is align-agent-and-skill-evaluations-with-documentation-design-system.
- Creation of this work item does not dispatch it while backlog crisis recovery remains active.
