# Simplify New-Document Provenance Headers

Status: Ready

Type: Feature

Provider: file

Work Item ID: simplify-new-document-provenance-header

Completion: main-branch

## Summary

Simplify the hidden provenance header for newly created governed documents. Record creation time in local time with an explicit UTC offset, omit Task-ID from the document, and remove redundant per-field runtime-supplied evidence lines while preserving deterministic external validation and historical compatibility.

## Context

The current new-document provenance block contains seven creation values followed by seven evidence fields that all repeat runtime-supplied. It also embeds a runtime Task-ID and labels creation time as Created-UTC. In a newly created document, the runtime envelope already supplies and proves all creation values, so repeating the same evidence classification for every field makes the header longer and harder to understand without adding field-level discrimination.

The example reported by the user contains seventeen metadata lines before the closing comment. The desired new-document form is a compact creation record: copyright, durable artifact identity, local offset-bearing creation time, conceptual creating agent, runtime, dispatched model, and reasoning effort. Runtime execution identity and validation evidence may remain in the external envelope or retained execution records without appearing in the document.

Local time must remain an unambiguous instant. For example, the reported value 2026-08-12T12:37:56Z can be represented for America/Toronto on that date as 2026-08-12T08:37:56-04:00. A local timestamp without a numeric offset is not acceptable because it cannot be compared deterministically across daylight-saving transitions or runtimes.

Existing conforming documents and historical migrations may use the current format. This refinement must not require a repository-wide rewrite or discard evidence distinctions when historical fields come from different sources.

## Source Evidence

On 2026-08-12, the user supplied a newly created document header and stated: "The Creation time should be local time not UTC", "There's a lot of lines for Evidence and they all say runtime-supplied this is confusing", and "There's no point in including a Task ID for a document." The user then directed: "Explain if there's any issue with these changes, then either ask me questions or create a work item to improve this." This message authorizes this file-backed improvement item.

The current contract is defined by skills/document-provenance/SKILL.md and skills/document-provenance/references/format-contract.md. The canonical template, external envelope schema, validator, and focused fixtures enforce Created-UTC, Task-ID, and one evidence field per creation value.

## Requirements

- Define a compact canonical provenance block for newly created governed documents.
- Replace the UTC-only creation field with a clearly named local creation-time field whose ISO 8601 value includes an explicit numeric UTC offset.
- Resolve local time from authoritative project or runtime-envelope timezone data. Do not ask the document-writing model to infer a timezone.
- Remove Task-ID from the embedded document block. Retain runtime task or execution identity outside the document only where the coordinator, harness, external envelope, or execution record needs it.
- Remove the seven per-field Evidence lines from the canonical new-document block when all embedded values are supplied and validated by one external runtime envelope.
- Keep Artifact-ID as the stable document-to-envelope correlation key so deterministic validation does not depend on an embedded Task-ID.
- Continue to compare every new-document value with authoritative external envelope data. A shorter document block must not permit model-authored or profile-inferred provenance.
- Define a bounded compatibility rule for existing valid headers. Existing documents must remain valid without automatic migration unless a separate authorized change updates them.
- Preserve field-level evidence distinctions for historical migration only where different fields genuinely have different evidence sources. Do not force the verbose historical representation into newly created documents.
- Update the canonical format contract, template, envelope schema, validator, fixtures, and focused tests together.
- Update design/documentation-templates.html if its displayed provenance guidance or examples describe the old canonical block.
- Avoid adding a replacement metadata line that merely restates that the whole new-document envelope is runtime-supplied unless validation has a concrete need that cannot be satisfied externally.

## Acceptance Criteria

- The canonical new-document example contains no Task-ID line and no per-field Evidence lines.
- The canonical new-document creation time is local and contains an explicit numeric UTC offset.
- The external provenance envelope can retain execution-only metadata without requiring that metadata to be copied into the document.
- The validator correlates a document to its runtime envelope by Artifact-ID and rejects mismatched, missing, inferred, placeholder, malformed, or offset-free new-document values.
- The validator accepts the new compact form and continues to handle existing valid blocks under an explicit compatibility policy.
- Historical validation retains truthful mixed-source evidence behavior without making the new-document header verbose.
- Positive fixtures cover Markdown with and without front matter, reserved wiki pages, maintained HTML, and generated documents using the compact header.
- Negative fixtures cover missing or malformed offsets, envelope mismatches, inferred values, unexpected Task-ID in the new canonical form, and redundant or unsupported evidence metadata as required by the selected compatibility policy.
- Focused document-provenance tests, skill validation, affected generated-output freshness checks, documentation validation, and Git diff checks pass.
- Fresh independent review confirms that the compact form preserves truthful provenance, deterministic validation, placement rules, and generated-document ownership.

## Dependencies

None.

## Verification

- Run skills/document-provenance/scripts/test_validate_document_provenance.py with the configured Python workflow.
- Run positive and negative validator CLI checks against the revised runtime-envelope schema and fixtures.
- Validate the revised document-provenance skill and its OpenAI metadata.
- Run the focused bundle-content and generated-document checks that consume the canonical provenance template or contract.
- Validate design/documentation-templates.html if it changes.
- Run Git diff validation for the exact changed paths.

## Open Questions

- Should the portable contract prefer an explicit project-configured IANA timezone and fall back to authoritative runtime-local timezone data, or require the runtime envelope to always supply both the local offset-bearing timestamp and timezone source?
- Should legacy new-document blocks remain accepted indefinitely or be accepted only as a versioned legacy form while all newly generated documents use the compact form?
- Can historical evidence classifications move entirely to an external migration record, or must mixed-source historical blocks retain compact field-level qualifiers for standalone auditability?

## Governed Definition Approval

### Governed Canonical Sources

- skills/document-provenance/SKILL.md
- skills/document-provenance/references/format-contract.md
- skills/document-provenance/references/historical-migration.md

### Allowed Dependent Artifacts

- skills/document-provenance/assets/provenance-block.md.tmpl
- skills/document-provenance/assets/provenance-envelope.schema.json
- skills/document-provenance/scripts/validate_document_provenance.py
- skills/document-provenance/scripts/test_validate_document_provenance.py
- skills/document-provenance/fixtures/runtime-envelope.json
- design/documentation-templates.html

Focused fixture files under skills/document-provenance/fixtures may change only as test data needed to prove the approved canonical contract. Supported generated mirrors may change only through their owning source and normal regeneration workflow.

### Approval Resolution

Approved at creation from the user's 2026-08-12 message in the current Codex task. Approval covers the exact requested provenance-header behavior and the governed canonical sources listed above. It does not authorize unrelated document metadata, historical content reconstruction, or changes to other skill definitions.

## Notes

- The work item changes the canonical format for future new documents; it does not itself migrate existing document headers.
- The numeric offset preserves an exact instant while presenting the creation time in local civil time.
- Git remains the default modification-history authority. This item does not add mutable modification metadata to document headers.
