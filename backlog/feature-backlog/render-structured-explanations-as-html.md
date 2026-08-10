# Render Structured Explanations as HTML

Owner: Unowned

Status: Ready

Type: Feature

Provider: file

Work Item ID: render-structured-explanations-as-html

Completion: main-branch

## Summary

Extend the structured-explanation skill so a large or review-intensive explanation can produce a source-traceable structured representation and a synchronized, accessible HTML explanation through the create-document-outline workflow and mcp-agent-ops.

## Context

The current structured-explanation skill defines a Markdown reasoning model with QUERY, SUB-QUERY, FACT, HYPOTHESIS, UNKNOWN, and ANSWER items. It requires stable identifiers when review or cross-reference matters and keeps structured-design items subordinate to the explanation flow.

Prior repository work demonstrated that a complete structured explanation can serve as the sole content authority for a derivative HTML page when its item coverage and source blocks are verified. The mcp-agent-ops hierarchy renderer can display nested structured data as self-contained, numbered, collapsible HTML with accessible controls and complete copy support.

Work Item create-html-document-outlines-from-raw-information owns the general source-to-structured-outline methodology, MCP rendering boundary, human-review flow, and writer routing. This item adds only the structured-explanation-specific mapping and must not duplicate or fork that general workflow.

## Source Evidence

The user requested this related work on 2026-08-09 in canonical task 019fb057-1767-7ef2-b5fa-41f4417b20b3:

> Related idea: the structured-explanation skill could use this to create an HTML structured explanation. this is a second work item to create.

Supporting evidence:

- skills/structured-explanation/SKILL.md defines the six explanation item types, their required order, stable identifiers, evidence discipline, and structured-design interoperation.
- /Users/martinbechard/dev/mcp-agent-ops/docs/reference/hierarchy-html-renderer.md documents nested structured inputs, self-contained HTML, numbering, progressive level controls, accessible tree semantics, escaping, and complete copy behavior.
- The prior Agent-Owned Evaluation Suites documentation work retained a complete structured explanation as the sole content authority for derivative HTML and verified QUERY, SUB-QUERY, ANSWER, UNKNOWN, and source-command coverage.

## Requirements

- Extend structured-explanation with a conditional HTML-output route for explanations whose depth, evidence volume, uncertainty, or human-review needs make a visual hierarchy materially useful.
- Keep Markdown as the canonical explanation artifact unless the user explicitly requests another canonical format. Treat JSON as the structured rendering source and HTML as a derived review projection.
- Map QUERY, SUB-QUERY, FACT, HYPOTHESIS, UNKNOWN, ANSWER, and permitted subordinate structured-design items into an ordered hierarchy without inventing new reasoning item types.
- Preserve every stable item identifier, item type, synopsis, source reference, exact command or literal block, parent relationship, and ordering required by the canonical explanation.
- Preserve the distinction between facts, hypotheses, unknowns, and answers in both copied text and visual presentation. Styling must not imply that an UNKNOWN is resolved or a HYPOTHESIS is proven.
- Use create-document-outline to prepare the structured JSON and call the configured mcp-agent-ops server for synchronized HTML generation.
- Allow human review of the HTML while requiring corrections to be made in the canonical explanation and regenerated structured source, never by editing HTML.
- Detect missing items, orphaned answers, parent-child mismatches, duplicate stable identifiers, unsupported item types, and source-block drift before accepting the HTML projection.
- Keep structured-design elements subordinate to the QUERY and ANSWER flow in the rendered hierarchy.
- Define when the HTML artifact is temporary, when it is a requested deliverable, and how it is retained or cleaned up.
- Preserve the existing Markdown-only default for ordinary structured explanations.

## Acceptance Criteria

- A complete multi-query explanation renders as self-contained HTML with visible QUERY, SUB-QUERY, FACT, HYPOTHESIS, UNKNOWN, and ANSWER distinctions and stable identifiers.
- The structured source and HTML contain every canonical explanation item exactly once, in the same parent relationship and semantic order.
- Exact command blocks, file references, and quoted literals remain byte-faithful or are linked without lossy rewriting according to the selected representation contract.
- The rendered hierarchy keeps structured-design items subordinate to their owning explanation item and does not turn the explanation into a design document.
- Copying the HTML hierarchy produces a complete readable explanation that preserves item type, identifier, and unresolved-state meaning.
- Human-review corrections flow back through the canonical explanation and regenerate the JSON and HTML without hand-edited projection drift.
- Ordinary small explanations remain Markdown-only unless the user requests HTML.
- Focused tests reject duplicate IDs, omitted items, orphaned answers, invalid nesting, changed evidence blocks, unsupported item types, and stale HTML.
- Independent methodology review and verification accept the structured-explanation changes and the generated example.

## Dependencies

- create-html-document-outlines-from-raw-information

Blocker owner: Work Item create-html-document-outlines-from-raw-information.

Blocked to Ready condition: the dependency is Completed with an accepted create-document-outline skill and working MCP structured JSON-to-HTML route.

Dependency Resolution: Satisfied on 2026-08-10. Work Item create-html-document-outlines-from-raw-information is Completed with an accepted create-document-outline skill, focused source-traceability validation, and a synchronized JSON-to-HTML route that fails clearly when mcp-agent-ops is unavailable.

Next Action: Dev Backlog Coordinator may reserve this item as the next separate SOLO crisis work-item task after terminal cleanup of the completed dependency.

## Verification

- Validate skills/structured-explanation/SKILL.md through the configured skill validator.
- Build a focused example containing all six explanation item types plus subordinate structured-design items and render it through create-document-outline and MCP.
- Compare canonical and rendered inventories for stable identifier, item type, parent, order, synopsis, source reference, and exact-block parity.
- Verify rejection of duplicate identifiers, missing items, orphaned answers, unsupported types, invalid structured-design placement, changed command blocks, and stale projections.
- Verify the HTML with applicable accessibility, markup, copy, collapse, link, overflow, and browser-console checks.
- Regenerate and check affected skill documentation and supported metadata from canonical sources.
- Run focused bundle assertions and Git diff checks for the exact integrated paths.

## Open Questions

- Should exact multiline command and quotation blocks appear inline in the hierarchy, or remain in the canonical Markdown with stable links from compact HTML nodes?
- Which visual treatment best distinguishes FACT, HYPOTHESIS, UNKNOWN, and ANSWER without relying on color alone?

## Governed Definition Approval

### Governed Canonical Sources

- skills/structured-explanation/SKILL.md

### Allowed Dependent Artifacts

- skills/structured-explanation/agents/openai.yaml
- README.md
- scripts/test_bundle_content.py
- Generated skill documentation produced by repository-authorized generators
- Focused non-governed structured-explanation HTML examples, fixtures, and tests whose exact paths are resolved during implementation

### Approval Resolution

Approved at creation. The user explicitly requested on 2026-08-09 in canonical task 019fb057-1767-7ef2-b5fa-41f4417b20b3 a second work item for structured-explanation to create an HTML structured explanation through the new outline capability. This approval covers exactly skills/structured-explanation/SKILL.md and no other governed definition.

## Notes

- This item does not change the explanation reasoning model or add item types.
- The HTML is derived from the canonical explanation and is not an independent source of truth.
- Creation of this work item does not dispatch it while backlog crisis recovery remains active.
