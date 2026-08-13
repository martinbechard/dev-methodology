# Simplify New-Document Provenance Headers

Status: Starting

Type: Feature

Provider: file

Work Item ID: simplify-new-document-provenance-header

Completion: main-branch

## Summary

Replace verbose internal provenance blocks with concise human-facing provenance, including a visible HTML footnote that shows only useful facts actually known.

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
- For maintained HTML, render provenance as a concise visible footnote in the document rather than relying only on a hidden detailed comment.
- Show only provenance facts useful to a reader and actually supported by authoritative evidence. Omit unknown fields; never invent or reconstruct history.
- Prohibit user-facing placeholders and evidence mechanics such as `historical-unknown`, `migration-assigned`, per-field `*-Evidence` labels, runtime envelope terminology, or internal validation classifications.
- Keep any machine-only correlation or validation data outside the human-facing footnote and minimize hidden document metadata to what deterministic validation strictly requires.
- Replace the UTC-only creation field with a clearly named local creation-time field whose ISO 8601 value includes an explicit numeric UTC offset.
- Resolve local time from authoritative project or runtime-envelope timezone data. Do not ask the document-writing model to infer a timezone.
- Remove Task-ID from the embedded document block. Retain runtime task or execution identity outside the document only where the coordinator, harness, external envelope, or execution record needs it.
- Remove the seven per-field Evidence lines from the canonical new-document block when all embedded values are supplied and validated by one external runtime envelope.
- Keep Artifact-ID as the stable document-to-envelope correlation key so deterministic validation does not depend on an embedded Task-ID.
- Continue to compare every new-document value with authoritative external envelope data. A shorter document block must not permit model-authored or profile-inferred provenance.
- Define a bounded compatibility rule for existing valid headers. Existing documents must remain valid without automatic migration unless a separate authorized change updates them.
- Preserve truthful evidence distinctions in external validation or migration records when required, but never expose internal placeholder or per-field evidence labels in user-facing documentation.
- Update the canonical format contract, template, envelope schema, validator, fixtures, and focused tests together.
- Update design/documentation-templates.html if its displayed provenance guidance or examples describe the old canonical block.
- After the corrected policy and validation contract pass, migrate `design/wiki-skills-and-project-context.html` as the bounded representative historical page: add the concise visible provenance footnote using only known facts, omit unknowns, preserve its accepted semantic baseline, and make no page-wide visual or unrelated content change.
- Avoid adding a replacement metadata line that merely restates that the whole new-document envelope is runtime-supplied unless validation has a concrete need that cannot be satisfied externally.

## Acceptance Criteria

- The canonical new-document example contains no Task-ID line and no per-field Evidence lines.
- The canonical new-document creation time is local and contains an explicit numeric UTC offset.
- The external provenance envelope can retain execution-only metadata without requiring that metadata to be copied into the document.
- The validator correlates a document to its runtime envelope by Artifact-ID and rejects mismatched, missing, inferred, placeholder, malformed, or offset-free new-document values.
- The validator accepts the new compact form and continues to handle existing valid blocks under an explicit compatibility policy.
- Historical validation retains truthful mixed-source evidence behavior without making the new-document header verbose.
- Maintained HTML exposes one concise provenance footnote containing only useful known facts, with no internal placeholder, migration classification, or per-field evidence label.
- Historical HTML with incomplete creation evidence remains truthful by omitting unknown facts rather than displaying or inventing them.
- `design/wiki-skills-and-project-context.html` passes the corrected provenance validator and focused semantic, HTML, navigation, and link checks without visible-content drift beyond the approved footnote.
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
- Which minimum machine-only correlation field, if any, must remain embedded after visible footnote validation is implemented?

## Governed Definition Approval

### Governed Canonical Sources

- skills/document-provenance/SKILL.md
- skills/document-provenance/references/format-contract.md
- skills/document-provenance/references/historical-migration.md
- skills/route-documentation-work/assets/templates/architecture-template.md
- skills/route-documentation-work/assets/templates/functional-spec-template.md
- skills/route-documentation-work/assets/templates/high-level-design-template.md
- skills/route-documentation-work/assets/templates/module-design-template.md
- skills/route-documentation-work/assets/templates/project-wiki-template.md
- skills/route-documentation-work/assets/templates/unit-test-plan-template.md

### Allowed Dependent Artifacts

- skills/document-provenance/assets/provenance-block.md.tmpl
- skills/document-provenance/assets/provenance-envelope.schema.json
- skills/document-provenance/scripts/validate_document_provenance.py
- skills/document-provenance/scripts/test_validate_document_provenance.py
- skills/document-provenance/fixtures/runtime-envelope.json
- design/documentation-templates.html
- design/wiki-skills-and-project-context.html
- Focused bundle-content, HTML, navigation, link, and provenance test files proven necessary by the corrected visible-footnote contract.

Focused fixture files under skills/document-provenance/fixtures may change only as test data needed to prove the approved canonical contract. Supported generated mirrors may change only through their owning source and normal regeneration workflow.

### Approval Resolution

Approved at creation from the user's 2026-08-12 message and expanded by the user's explicit 2026-08-13 correction. Approval covers concise human-facing HTML provenance footnotes, omission of unknown facts and internal evidence labels, the exact governed canonical sources listed above, and the bounded wiki page migration. It does not authorize invented historical content, unrelated page redesign, or changes to other skill definitions.

## Notes

- The work item changes the canonical format for future new documents; it does not itself migrate existing document headers.
- The numeric offset preserves an exact instant while presenting the creation time in local civil time.
- Git remains the default modification-history authority. This item does not add mutable modification metadata to document headers.
- The obsolete `migrate-wiki-skills-and-project-context-historical-provenance` proposal is superseded rather than approved. Its page correction is the final bounded phase of this item, avoiding a duplicate policy owner or cross-folder dependency.

## Starting Handoff Evidence

- Reserved At: 2026-08-13T11:43:11Z.
- Transition: `Ready -> Starting`.
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Coordinator Execution: `/root/backlog_coordinator`.
- Baseline: `e8923f2cb1fe967806a0542359d15af01d94ac19` on primary `main`.
- Capacity: Slot 3 of 5. Independent document-provenance scope; exclude private Backlog Dispatcher, evaluation terminology, Dev Orchestrator routing, and documentation-template parser paths.
- Transition Claims: `start-simplify-new-document-provenance-header-work-item`; event `d0bd6ece-b12a-4174-bbd1-f1fce12a7ef2`. `start-simplify-new-document-provenance-header-provider`; event `450af136-cade-4d7a-9a4d-28d1b64ff762`.
- Runtime Identity: Pending caller-owned visible task creation. Creation does not imply Running.

## Canonical Runtime Assignment

- Assigned At: 2026-08-13T11:46:27Z.
- Codex Task ID: `019ffaf1-7879-7973-9bcb-a34652fbce7f`.
- Conversation ID: `019ffaf1-7879-7973-9bcb-a34652fbce7f`.
- Host: `local`.
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Requested Title: `Starting — Simplify New Document Provenance Headers`.
- Initial Action: Launch one Dev Orchestrator subagent for this authoritative provider record.
- Creation Outcome: Unique success decoded from a complete JSON-string envelope, with no client or pending identity and no retry.
- Lifecycle Boundary: This assignment remains `Starting` until the nested Dev Orchestrator accepts and records `Starting -> Running`.
- Adoption Claims: `adopt-simplify-new-document-provenance-header-visible-task`; event `30fee46c-8126-48fc-bf87-d4e4210820b8`. `adopt-simplify-new-document-provenance-header-provider`; event `d624ab97-c532-443e-b8fd-c11c28473404`.

## Policy Supersession Evidence

- Reconciled At: 2026-08-13T01:28:46Z.
- User Direction: HTML provenance is a concise visible footnote with only useful known facts. Unknown values and internal evidence labels are omitted and history is never invented.
- Ownership Decision: This existing Work Item absorbs the policy correction and bounded wiki-page migration because it already owns the canonical provenance sources, validator, fixtures, and design guidance.
- Transition Claim: `update-concise-visible-provenance-policy-019ff2c3`; outcome `SHARED_CHECKOUT_ACQUIRED`; event `f20f61f9-ad49-4d60-bec9-85b7baaecef8`.

## Running Acceptance Evidence

- Accepted At: 2026-08-13T11:47:52Z.
- Transition: `Starting -> Running`.
- Canonical Codex Task ID: `019ffaf1-7879-7973-9bcb-a34652fbce7f`.
- Accepted By: Dev Orchestrator `/root/simplify_new_document_provenance_header`.
- Work Claim: `simplify-new-document-provenance-header-work`; outcome `SHARED_CHECKOUT_ACQUIRED`; event `ff8a99c5-d9cf-49e6-a94d-43340cff459b`.
- Provider Transition Claim: `run-simplify-new-document-provenance-header-provider`; outcome `SHARED_CHECKOUT_ACQUIRED`; event `1da6ec1b-a055-49b0-8d0c-b364f109c98c`.

## User Action Required

### Question for the User

Do you approve adding these six route-documentation-work template sources to this Work Item's governed canonical scope?

- skills/route-documentation-work/assets/templates/architecture-template.md
- skills/route-documentation-work/assets/templates/functional-spec-template.md
- skills/route-documentation-work/assets/templates/high-level-design-template.md
- skills/route-documentation-work/assets/templates/module-design-template.md
- skills/route-documentation-work/assets/templates/project-wiki-template.md
- skills/route-documentation-work/assets/templates/unit-test-plan-template.md

### Why User Input Is Required

Full acceptance requires changes to these six owning sources, but the previously approved Governed Definition boundary did not authorize them. Dev Architect rejected substitution or partial delivery, so only the user or provider owner can expand the governed canonical scope.

### Options and Tradeoffs

- Approve all six (recommended): update the owning templates with the compact provenance contract and complete the already accepted end-to-end requirement. Newly created architecture, functional specification, high-level design, module design, project wiki, and unit-test-plan documents stop reproducing the legacy verbose block.
- Do not approve: preserve all work and make no changes to those templates. The Work Item cannot satisfy its accepted reusable new-document provenance requirement, and partial or substitute delivery is not authorized.

### Resolution

Approved all six on 2026-08-13 by the user in canonical Codex Task `019ffaf1-7879-7973-9bcb-a34652fbce7f`. This approval adds the six exact `route-documentation-work` owning template paths listed above to this Work Item's governed canonical scope. Preserve the accepted plan and require corrected plan review before source implementation.

### Unattended Work Boundary

Make no source mutation while this question is pending. Preserve the accepted plan, existing Work Item, canonical execution, worktree, claims until the transition boundary, and all current evidence. Read-only evidence inspection may continue.

### Transition Evidence

- Transition: Running -> User Action Required.
- Decision Owner: user/provider owner.
- Exact Blocker: Full acceptance requires changes to the six listed owning templates outside the previously approved governed scope.
- Blocker Reference: simplify-provenance-six-template-scope-approval.
- Unblock Condition: explicit approval of all six named template paths, recorded in this authoritative provider record, followed by corrected plan review.
- Canonical Execution: Codex Task 019ffaf1-7879-7973-9bcb-a34652fbce7f with Dev Orchestrator /root/simplify_new_document_provenance_header.
- Preserved Evidence: accepted JSON and HTML plan, existing Work Item history, claims through the transition boundary, and all current execution evidence.
- Source Mutation: None; source coding had not started.

## User Action Required Recovery Evidence

- Answered At: 2026-08-13 in canonical Codex Task `019ffaf1-7879-7973-9bcb-a34652fbce7f`.
- User Answer: `I approve all six`.
- Resolution: All six exact `route-documentation-work` template sources listed in Governed Canonical Sources are approved.
- Transition: `User Action Required -> Ready`.
- Canonical Execution Preserved: Codex Task `019ffaf1-7879-7973-9bcb-a34652fbce7f` and Dev Orchestrator `/root/simplify_new_document_provenance_header`.
- Next Action: Parent Dev Backlog Coordinator reconciles capacity and records `Ready -> Starting` for this preserved canonical task; the root Dev Orchestrator then separately accepts `Starting -> Running` before source mutation.
- Corrected Gate: Revise the accepted plan for the expanded six-template scope and obtain corrected Dev Architect review before implementation.

## Approved-Scope Resumption Starting Evidence

- Reserved At: 2026-08-13T17:22:20Z.
- Transition: `Ready -> Starting`.
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Coordinator Execution: `/root/backlog_coordinator`.
- Canonical Task and Conversation: `019ffaf1-7879-7973-9bcb-a34652fbce7f` on host `local`.
- Preserved Dev Orchestrator: `/root/simplify_new_document_provenance_header`.
- Baseline: `e143f8a84aded718679a9617911b021c40984cca` on primary `main`.
- Capacity: One of five active slots is reserved. The only other active item is `map-evaluation-contracts-to-inspect-ai`; its exact file scope is disjoint.
- Dependency Decision: The user's approval of all six named templates is durably recorded and no hard dependency remains.
- Scope Boundary: Resume only the existing accepted plan through its required six-template correction and fresh architecture review. Preserve every unrelated untracked plan and temporary artifact.
- Dispatch Result: Resume the same canonical visible task and nested Dev Orchestrator; no new task or replacement execution is authorized.
- Transition Claim: `reserve-simplify-provenance-019ff2c3`; event `cae3ec2b-9a9d-4f10-8fd0-55d474d34325`.
- Next Action: The preserved Dev Orchestrator records `Starting -> Running`, then reacquires the Work Item and exact path claims before any mutation.
