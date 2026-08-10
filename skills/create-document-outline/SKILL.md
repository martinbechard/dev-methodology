---
name: create-document-outline
description: Create a source-traceable JSON document outline and synchronized review HTML before writing a large or complex document.
metadata:
  category: documentation-methodology
---
<!--
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
Artifact-ID: b5945225-b416-49de-ae06-5070721e817f
Created-UTC: 2026-08-10T19:55:24Z
Creating-Agent: Dev Coder
Runtime: Codex
Dispatched-Model: gpt-5.6-sol
Reasoning-Effort: high
Task-ID: /root/create_document_outline
Artifact-ID-Evidence: runtime-supplied
Created-UTC-Evidence: runtime-supplied
Creating-Agent-Evidence: runtime-supplied
Runtime-Evidence: runtime-supplied
Dispatched-Model-Evidence: runtime-supplied
Reasoning-Effort-Evidence: runtime-supplied
Task-ID-Evidence: runtime-supplied
-->

# Create Document Outline

Use this skill to make a large document structure visible before full prose writing. The JSON outline is authoritative. Its sibling HTML file is a synchronized review projection.

The outline is preparation evidence. It is not the final document, verified source truth, a document template, or an artifact-specific review result.

## Activation Gate

Create an outline when at least one condition is true:

- The document uses five or more authorized source artifacts.
- The evidence contains ten or more material facts across at least three topics.
- The expected structure has ten or more material sections or at least three heading levels.
- Conflicts, missing information, or proposed organization can materially change the section order.
- The user requests a visible outline review before prose writing.

Do not create an outline for a short document with one clear source, a bounded edit, or a document whose selected template already makes the small structure obvious.

## Inputs And Authority

Obtain these inputs before synthesis:

- the document purpose and selected document-writing method;
- every authorized source that can affect the document;
- one stable source ID, label, and locator for each source;
- the target project workspace and task identity; and
- any user or project decision about durable outline delivery.

Inventory sources in their original order. Keep credentials, personal information, unauthorized proprietary content, and unnecessary raw payloads out of the outline definition and renderer input. Set authorized and sensitiveDataExcluded to true only after this review is complete.

The helper accepts summarized outline data. It does not accept raw Markdown evidence or send raw source files to the hierarchy renderer.

## Outline Contract

Use the schema and field shape in examples/large-multi-source-outline.json. Keep these rules:

- Use one root at level 1.
- Put ordered sections in children. Each child level is exactly one greater than its parent level.
- Give each section a title, kind classification, concise scope statement, sourceRefs list, and ordered children list.
- Use source_fact, proposed_organization, unknown, conflict, or final_document_decision as the section classification.
- Link source facts, conflicts, and final-document decisions to inventory source IDs.
- Use proposed_organization or unknown when no source supports a structural proposal or known gap.
- Put reviewText only on leaves. A branch cannot also contain review text, and a leaf cannot be empty.
- Keep sibling titles unique.
- Put every unresolved question in unresolvedQuestions with at least one source reference.
- Keep every unresolved question ID in review.remainingQuestionIds until evidence resolves it.

The helper rejects unknown fields. Do not add rawContent, credentials, prompts, or source payload fields to the schema.

## Helper Boundary

Use scripts/outline.py from this skill package. The helper imports and signature-checks the installed mcp_agent_ops.hierarchy.render_hierarchy_html API. It renders the packaged outline theme with numbering, progressive level controls, complete copy support, responsive styling, escaped values, and accessible tree controls.

Do not improvise another parser, renderer wrapper, or HTML writer. Do not install, emulate, or change mcp-agent-ops when the capability is unavailable.

On native Windows, the helper can use python.exe beside the installed mcp-agent-ops.exe console launcher. The helper returns CAPABILITY_UNAVAILABLE when neither the active interpreter nor that installed package interpreter provides the API.

The helper renders to a validated temporary directory. It rejects symbolic links, hard-link aliases, and non-file HTML targets. It atomically replaces the final HTML only after the temporary bytes match the in-memory rendering. A renderer failure leaves the previous HTML unchanged.

Run the capability check first:

```bash
python3 [skill-root]/scripts/outline.py capabilities
```

Continue only after CAPABILITIES_AVAILABLE.

## Temporary Paths

Use the ignored task-owned path by default:

```text
.codex/outlines/<task-id>/
├── <outline-name>.json
└── <outline-name>.html
```

Supply the canonical absolute workspace path, the project-relative output folder, and a safe outline name. Keep the definition JSON inside that workspace.

Create the JSON definition directly at the authoritative path in this pair. The helper accepts only this canonical JSON path. It does not create or retain a staging definition.

Build the synchronized pair:

```bash
python3 [skill-root]/scripts/outline.py \
  --workspace /absolute/project \
  --output-folder .codex/outlines/task-123 \
  --name document-outline \
  build --definition /absolute/project/.codex/outlines/task-123/document-outline.json
```

BUILT means the unchanged canonical JSON and derived HTML bytes are synchronized. The output folder contains no third outline artifact. Decide from the structured outcome, not only the process exit code.

## Evidence Synthesis

1. Read every authorized source before section synthesis.
2. Add each source to the inventory without copying unnecessary payloads.
3. Separate source facts from proposed organization, conflicts, unknowns, and final-document decisions.
4. Create one ordered section hierarchy with concise scope statements.
5. Retain source references on every material branch or apply an explicit non-fact classification.
6. Record unresolved questions with the sources that exposed each gap.
7. Start the review record in draft state with an empty accepted section order.
8. Build the JSON and HTML pair, then inspect the projection.

Inspect without changing either artifact:

```bash
python3 [skill-root]/scripts/outline.py \
  --workspace /absolute/project \
  --output-folder .codex/outlines/task-123 \
  --name document-outline \
  inspect
```

SYNCED means the HTML matches the authoritative JSON. STALE_HTML means the projection is missing or different. Rebuild from the JSON source after STALE_HTML. Never hand-edit the HTML projection.

## Review Loop

Give the reviewer the self-contained HTML and the source inventory. Ask for:

- accepted or corrected section order;
- required section additions, removals, or scope corrections;
- conflicts that need clearer separation; and
- questions and evidence gaps that remain open.

Apply feedback only to the canonical JSON. Do not modify original evidence to make the outline pass review. Rebuild HTML after each correction and run inspect again.

Set review.status to accepted only when:

- acceptedSectionOrder exactly matches the current top-level section order; and
- requiredCorrections is empty.

Accepted outlines can retain explicit unresolved questions. The remainingQuestionIds list must still contain every unresolved question in source order.

## Downstream Writing Boundary

After outline acceptance, give the selected document-writing method both the accepted outline and the original source evidence. The writer must verify claims against the original sources and apply the selected template, provenance rules, terminology, and artifact-specific review.

Do not turn scope statements or review text into final prose without source verification. Do not let the outline replace an artifact template, source links, document provenance, or independent review.

## Retention

Keep a temporary pair while outline review, document writing, or document review can resume. After the final document passes its required review and verification, remove only that exact temporary JSON and HTML pair when project policy does not require retention.

When the user requests the outline as a durable deliverable, choose its location through the target project's placement rules. Retain the JSON and HTML together and identify JSON as authoritative. Apply the target path's provenance and review rules through the owning generator or workflow. Stop when a governed durable HTML location requires metadata that the helper cannot generate without hand-editing the projection.

## Result

Return:

- the activation-gate decision and qualifying condition;
- the source inventory IDs and any excluded input class;
- the JSON and HTML paths, hashes, and helper outcomes;
- the review status, accepted order, required corrections, and remaining questions;
- the selected downstream document-writing method; and
- the temporary cleanup or durable retention decision.
