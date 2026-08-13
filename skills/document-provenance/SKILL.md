---
name: document-provenance
description: Apply and validate truthful creation provenance for governed documents without taking ownership of code comments or document-specific metadata.
metadata:
  category: documentation-methodology
---
<!--
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
Artifact-ID: f633e99c-ffc4-4bc9-9c11-75e8dc070914
Created-UTC: 2026-08-08T18:22:49Z
Creating-Agent: Dev Coder
Runtime: Codex
Dispatched-Model: gpt-5.6-sol
Reasoning-Effort: high
Task-ID: 019fe291-1ba8-7a43-8d21-391a04dfa9a9
Artifact-ID-Evidence: runtime-supplied
Created-UTC-Evidence: runtime-supplied
Creating-Agent-Evidence: runtime-supplied
Runtime-Evidence: runtime-supplied
Dispatched-Model-Evidence: runtime-supplied
Reasoning-Effort-Evidence: runtime-supplied
Task-ID-Evidence: runtime-supplied
-->

# Document Provenance

Document provenance records the immutable creation identity of a governed document. Apply this skill when an agent creates, generates, migrates, or accepts a maintained document selected by project guidance.

## Authority Boundary

- Let code-comments own executable source, tests, scripts, migrations, and executable schemas.
- Let document-provenance own only maintained non-code documents that project guidance selects.
- Let the document format continue to own YAML front matter, OKF metadata, titles, metadata elements, accessibility, and content structure.
- Use the exact copyright statement from applicable project instructions. Stop when the statement is absent or ambiguous. Do not invent a holder, address, year, license, or ownership claim.
- Keep correlation and evidence metadata hidden from normal rendering. Compact HTML exposes only the required reader-facing provenance fields in its semantic footer. Do not put document content or mutable status in provenance metadata.

## Inclusion And Exclusion

Apply the contract to maintained Markdown and maintained HTML documents. Apply it to generated documents through the owning generator, source template, or generation envelope.

Do not add the block automatically to these items:

- imported, external, or vendor documents;
- configuration, data, lock, manifest, cache, and binary files;
- operational records whose owning workflow excludes durable document provenance;
- generated projections whose owning source has not been changed;
- formats that cannot safely carry comments.

When a selected format cannot carry comments, use a project-authorized sidecar or manifest. If no such authority exists, report the format as unsupported and leave the file unchanged.

## Runtime Provenance Envelope

The coordinator, orchestrator, or harness supplies one creation record before document acceptance. The document-writing model does not infer or self-report dispatch identity.

For a new document, use a schema-version-2 record with these values:

- Artifact-ID is an opaque durable identifier. Create it once and keep it stable across ordinary moves and renames. Do not derive it from the current path.
- Created-Local is the authoritative creation time in ISO 8601 form with an explicit numeric UTC offset. Do not use `Z` or an offset-free value.
- Created-UTC is the machine-only UTC form of the same instant. Keep it in the external envelope and do not render it in a compact document.
- Creating-Agent is the conceptual Agent identity used for dispatch. It is not a nickname or inferred Git author.
- Runtime is the harness that dispatched the Agent.
- Dispatched-Model is the model selected for dispatch. Do not relabel it as the model that executed the request without separate authoritative runtime evidence.
- Reasoning-Effort is the effort selected for dispatch.
- Task-ID is optional correlation metadata. When supplied, keep it in the external envelope and do not render it in a compact document.

The validator compares the rendered values with the external envelope and proves that Created-Local and Created-UTC represent the same instant. A label in the document is not a substitute for that comparison. Do not create a timezone evidence taxonomy or add an IANA timezone field when the authoritative local timestamp already includes its numeric offset.

Never copy values from the current model profile, an adapter mapping, Git author data, or model-authored prose. Those sources do not prove the historical dispatch.

## Create Or Generate A Document

1. Obtain the exact copyright statement and runtime provenance envelope.
2. Render the compact Markdown block or semantic HTML form from [Format Contract](references/format-contract.md).
3. Replace every template placeholder before acceptance.
4. Put the block at the format-specific location.
5. Run deterministic validation against the runtime envelope.
6. Accept the document only when validation reports no findings.

For generated documentation, change the owning generator, source template, or generation envelope. Validate the generated output. Do not hand-edit a replaceable projection.

## Placement Rules

For Markdown with YAML front matter, keep the front matter as the first construct. Put the provenance HTML comment immediately after its closing delimiter.

For Markdown without YAML front matter, put the provenance HTML comment before the first heading or other content. Reserved project-wiki index.md and log.md pages remain free of OKF concept front matter.

For maintained HTML, keep the HTML doctype first. Put the exact Artifact-ID correlation comment immediately after the doctype and before the html element. Put one visible semantic provenance footnote inside the footer. Do not move metadata, language, accessibility, or rendering content into the comment.

## Historical Documents

Historical migration is an explicit validation route. It is never a fallback for a new or newly generated document. The route accepts an existing verbose historical block or compact historical HTML backed by a schema-version-2 external record.

Use [Historical Migration](references/historical-migration.md) for evidence priority, allowed evidence labels, correction rules, and bounded audit steps. In retained verbose blocks, record historical-unknown for an unavailable creation fact. In compact historical HTML, list the unavailable fact in external Unknown-Facts and omit it from the document. Do not infer the fact from current configuration.

## Ordinary Edits And Corrections

Keep creation provenance unchanged during ordinary edits, reviews, moves, and renames. Git history is the default modification-history authority. Do not add mutable modification fields to the creation block.

A project may select an append-only sidecar or ledger for modification history. The project must define one owner, a synchronization rule, and deterministic validation before use. Do not duplicate mutable facts between a document and a ledger without that contract.

Correct demonstrably false creation metadata only with named retained evidence and explicit project authority. Preserve the correction evidence in the review or project-selected append-only record.

## Deterministic Validation

The bundled validator reads only explicit paths. Use `--new` for compact documents backed by schema version 2. Use `--legacy` with schema version 1 to preserve and validate existing legacy package headers. Use `--historical` only for an authorized verbose legacy migration or compact historical HTML.

```bash
python3 [document-provenance-skill-root]/scripts/validate_document_provenance.py \
  --copyright "Copyright (c) 2026 Example" \
  --envelope /path/to/runtime-envelope.json \
  --new /path/to/new-document.md \
  --historical /path/to/migrated-document.html
```

Use a separate invocation with a schema-version-1 envelope for `--legacy`; one envelope cannot serve both schema versions. A verbose historical document needs no envelope, but compact historical HTML requires schema version 2.

The validator reports the exact path, field, and failure. It returns a failing process result for missing blocks or HTML markers, invalid placement, missing or duplicate fields, placeholders, malformed timestamps or offsets, UTC/local instant mismatches, unsupported evidence, inferred profile values, route/schema mismatches, envelope mismatches, and unsupported formats.

Validate only project-selected governed paths. Passing a path to the validator does not make an excluded file governed.

## Result

Return the governed paths, exact validation route for each path, runtime-envelope evidence where required, validation result, exclusions, and any unsupported format or missing authority.
