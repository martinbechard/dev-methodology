<!--
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
-->

# Add Document Provenance Skill

Status: Completed

Type: Feature

Provider: file

Owner: Root Dev Orchestrator

Work Item ID: add-document-provenance-skill

Canonical Conversation: 019fe291-1ba8-7a43-8d21-391a04dfa9a9

Root Agent Task: 019fe291-1ba8-7a43-8d21-391a04dfa9a9

Branch: codex/add-document-provenance-skill

Worktree: /Users/martinbechard/.codex/worktrees/6cb2/dev-methodology

Phase: Completed after verified main-branch delivery and shared catalog refresh

Started At: 2026-08-08T18:11:22Z

Accepted Candidate Commit: 4d3441dec8042c49cfdbb6baf244e53d2c52837d

Integration Commit: d4cd66c6e6b8a8e90314ae0a7f683a740ab5ede2

Completed At: 2026-08-08T19:35:08Z

Completion: main-branch

## Summary

Add a portable document-provenance skill that requires agent-created documents to carry a truthful copyright and creation-provenance header. Make the contract enforceable through format-specific placement rules, runtime-supplied identity, deterministic validation, document-authoring and review routing, templates, generated artifacts, and focused regression coverage.

## Context

The existing code-comments skill owns headers for source code, tests, executable scripts, migrations, and other executable code artifacts. It explicitly excludes documentation, configuration, data, lock files, and manifests. Expanding code-comments to cover documentation would combine distinct artifact contracts and contradict its current code-only boundary.

Agent-created documents currently do not have one portable contract that answers when the document was created, which conceptual agent created it, which runtime dispatched that agent, and which model and reasoning effort were selected. Git can preserve commit history, but it does not independently preserve all dispatch identity. The current conceptual documentation role selects a semantic model profile, and adapter configuration maps that profile to a model and effort, but the current mapping is not reliable evidence for historical execution and may not reflect an explicit runtime override.

Markdown repositories also use YAML front matter for document-specific schemas. In the project-wiki workflow, non-reserved concept pages use OKF front matter, while reserved index.md and log.md pages intentionally remain without concept front matter. Document provenance must not take ownership of those schemas or prevent front matter from being recognized as the first Markdown construct.

The Markdown placement decision is therefore an HTML comment block. When YAML front matter exists, it remains the first construct and the provenance block follows its closing delimiter. When no front matter exists, the provenance block precedes the title or other document content. Exact field labels make the block machine-readable without exposing it in normal rendered output.

The required project copyright statement is:

```text
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
```

Existing documentation templates contain older header forms that do not match this statement and do not preserve complete agent provenance. Generated documents and templates must be corrected through their owning source, not by hand-editing replaceable projections.

## Source Evidence

- On 2026-08-08, the user reported that documents created by agents do not show when they were created, which agent created them, or the model and effort used, and that the documents lack copyright notices.
- The user asked for the correct skill strategy to ensure the requirement is always respected and recalled earlier file-header guidance.
- After reviewing the code-only boundary, the proposed solution was a separate document-provenance skill with runtime-supplied provenance and deterministic enforcement.
- On 2026-08-08, the user stated: "OK let's work on a separate skill as suggested. What about using front matter for markdown? or is HTML-style comment better?"
- The Markdown decision was to use an HTML comment block so existing YAML front matter remains owned by the document format and reserved wiki pages do not acquire concept front matter.
- On 2026-08-08, the user directed: "just create a detailed workitem". This message authorizes creation of this file-backed work item and records the discussed document-provenance outcome for later delivery.

## Requirements

- Add a portable distributed skill whose canonical identifier and directory are document-provenance.
- Keep document-provenance separate from code-comments. Document-provenance owns authored documentation and other explicitly governed non-code document formats; code-comments continues to own executable code artifacts.
- Define exact inclusion and exclusion rules. At minimum, distinguish maintained documents, generated documents, imported or vendor documents, configuration and data files, operational records, and files whose format cannot safely carry comments.
- Require the exact copyright statement supplied by applicable project instructions. Do not invent a holder, address, year, or license statement when project authority is absent or ambiguous.
- Define a structured creation-provenance record with at least these fields:
  - Artifact-ID
  - Created-UTC
  - Creating-Agent
  - Runtime
  - Dispatched-Model
  - Reasoning-Effort
  - Task-ID
- Define Created-UTC as an ISO 8601 UTC timestamp and define Artifact-ID as a durable identifier that survives ordinary file movement or renaming.
- Define Creating-Agent as the conceptual agent identity used for dispatch, not a conversational nickname or inferred Git author.
- Define Runtime as the harness that performed dispatch, such as Codex or another supported adapter runtime.
- Label model information as Dispatched-Model unless the runtime provides separate authoritative evidence for the model that actually executed the request. Do not relabel configured, requested, or inferred values as actual execution evidence.
- Require the coordinator, orchestrator, or harness to supply agent identity, runtime, dispatched model, reasoning effort, task identity, and creation time through a provenance envelope. Do not ask the document-writing model to guess its own runtime metadata.
- Treat missing required runtime evidence as a validation failure for a newly created governed document. Do not silently copy the current adapter model-profile mapping into a document as historical evidence.
- Define an explicit historical migration state for existing documents. Permit git-derived creation time and historical-unknown values only when the header clearly labels their evidence status and no stronger task or rollout evidence exists.
- Preserve immutable creation provenance during ordinary document edits. Define how later corrections to demonstrably false creation metadata are authorized, evidenced, and reviewed.
- Define whether modification provenance is satisfied by Git history or requires a project-configured sidecar or append-only ledger. Do not duplicate mutable facts across a document and ledger without a synchronization and validation rule.
- For Markdown with YAML front matter, require the provenance HTML comment immediately after the closing front-matter delimiter. Preserve YAML front matter as the first construct.
- For Markdown without YAML front matter, require the provenance HTML comment before the first heading or other document content.
- Keep OKF concept metadata in YAML front matter and keep reserved project-wiki index.md and log.md pages free of concept front matter.
- Define a canonical Markdown example using exact, line-oriented labels inside one HTML comment. Reject placeholder values, duplicate fields, malformed timestamps, unsupported evidence labels, and provenance blocks placed before existing YAML front matter.
- Define format-specific placement for maintained HTML documents without breaking the doctype, metadata, accessibility, or rendering contract.
- Define a safe fallback for document formats that do not support comments. Use a project-authorized sidecar or manifest when applicable; otherwise report the unsupported format instead of corrupting the file.
- For generated documentation, require changes to the owning generator, source template, or generation envelope. Do not hand-edit generated projections.
- Add deterministic validation capable of checking one document and a bounded set of governed document paths. Validation must report exact file and field failures and return a failing process result when required provenance is absent or invalid.
- Make validation distinguish new governed documents from historical documents so historical-unknown does not become an unrestricted escape for newly generated content.
- Add positive fixtures for Markdown without front matter, Markdown with OKF front matter, a reserved wiki page, maintained HTML, and a generated document produced from an owning template.
- Add negative fixtures for a missing copyright statement, missing provenance block, comment before YAML front matter, missing or duplicate fields, placeholders, malformed UTC timestamp, unsupported evidence claims, and model or effort values inferred from current profile configuration.
- Integrate document-provenance into the documentation-authoring, wiki-writing, documentation-review, wiki-verification, methodology-maintenance, and project-configuration routes that create or accept governed documents.
- Keep the integration centralized. Prefer a fixed shared provenance gate or definition-owned role assignment over copying the complete field contract into every artifact-specific creation and review skill.
- Update project configuration generation so applicable AGENTS.md guidance states when document-provenance must be loaded, which document paths are governed, the exact copyright statement, and any format or generated-file exclusions.
- Update every maintained documentation template that creates governed documents. Remove stale copyright forms and preserve template placeholders only where the creation workflow deterministically replaces them before acceptance.
- Update conceptual agent definitions, supported generated adapters, metadata, README inventory, skill hierarchy, relevant design pages, support checklists, and evaluation catalogs from their canonical sources.
- Add focused contract tests that fail when the skill is absent from required authoring or verification routes, when generated outputs are stale, or when templates retain contradictory header guidance.
- Add a bounded audit or migration procedure for existing documents. Recover creation facts from immutable Git or retained rollout evidence where possible and record historical-unknown rather than fabricating agent, model, effort, or task identity.
- Do not automatically rewrite vendor documentation, external source captures, lock files, or data artifacts merely because their syntax permits comments.
- Preserve the repository rule that PII or company-internal information is not sent to an LLM unless explicitly authorized. Runtime provenance injection and deterministic validation should not require model access to private coordination logs.

## Acceptance Criteria

- The document-provenance skill exists as a valid portable skill and clearly excludes executable code artifacts owned by code-comments.
- The skill defines one canonical field vocabulary and evidence semantics for copyright, artifact identity, creation time, conceptual agent, runtime, dispatched model, reasoning effort, and task identity.
- The skill requires runtime-supplied provenance and prohibits model-authored guesses or historical inference from current model-profile mappings.
- A conforming Markdown document with YAML front matter keeps that front matter first and places the provenance HTML comment immediately afterward.
- A conforming Markdown document without YAML front matter places the provenance HTML comment before its first heading or other content.
- Reserved project-wiki index.md and log.md pages can carry provenance without acquiring OKF concept front matter.
- Maintained HTML documents have a defined valid placement that does not precede or invalidate a required doctype.
- Newly created governed documents fail deterministic validation when any required copyright or provenance field is missing, duplicated, malformed, placeholder, unsupported, or historically inferred.
- Existing documents can be migrated with explicit evidence status, and the migration workflow never fabricates unknown agent, runtime, model, effort, task, or creation facts.
- Creation metadata remains stable during normal edits, while any correction to false metadata requires named evidence.
- Generated documents receive provenance through their generator, source template, or generation envelope rather than hand edits.
- Documentation creation and verification routes load or execute the shared provenance contract without duplicating its complete rules across artifact-specific skills.
- Project configuration can emit the applicable document-provenance rule and exact copyright statement into generated project guidance.
- Documentation templates no longer use stale or contradictory copyright blocks and cannot be accepted with unresolved provenance placeholders.
- Focused positive and negative validator tests pass, skill validation passes, affected generated outputs are fresh, and Git diff validation passes.
- An independent skill review finds no conflicting authority with code-comments, project-wiki front matter, artifact-specific templates, generated-file ownership, or runtime model-profile configuration.
- Shared skill installations are refreshed and verified after the canonical bundle change is accepted.

## Dependencies

None.

## Starting Handoff Evidence

Starting Recorded At: 2026-08-08T18:08:55Z

Coordinator: Dev Backlog Coordinator task `019fb057-1767-7ef2-b5fa-41f4417b20b3`

Normalized Objective: Add the approved portable `document-provenance` skill and its directly owned package, deterministic validation, focused fixtures, documentation, routing, generated outputs, and installation verification while preserving runtime-supplied evidence truthfulness and existing Markdown front-matter ownership.

Launch Result: Not attempted

Canonical Execution: None

Last Contact At: None

Next Reconciliation At: 2026-08-08T18:23:00Z

Coordination Boundary: Private-worktree discovery and the new skill package may proceed independently. Defer any exact overlapping bundle-content catalog, generated-output, shared review, or main-integration event until `reconcile-bundle-content-suite-drift` clears its active finish lane. Preserve the separately owned untracked `design/agent-owned-evaluation-suites.html` file.

## Active Execution Evidence

Condition Type: delegated-work

Owner: Dev Coder task /root/implement_document_provenance under Root Dev Orchestrator task 019fe291-1ba8-7a43-8d21-391a04dfa9a9

Evidence: Original Dev Coder produced additive clean replacement commit 4d3441dec8042c49cfdbb6baf244e53d2c52837d on immutable source candidate 87d99310abad66be170bafac9c7274a884e2c211, resolving all three findings with focused 14/14 validator, 8/8 OKF, and 2/2 renderer/freshness checks. The same independent methodology reviewer returned VERDICT: GOOD with no residual finding. A parent primary-main-rooted MCP session returned structured skill_validate {ok:true, findings:[]} on the exact clean replacement package and git diff --check passed; the same independent verifier reconciled that immutable evidence with every previously green focused gate and returned VERDICT: PASS. Terminology main d9e12b27087ee3fe34ae38b1eeae477342a4233a was combined without overwriting either feature contract on preserved integration branch codex/integrate-document-provenance-019fe291 as candidate mappings 53c30c00 and f6ffb840; the six declared overlaps and generated outputs are ready for one fresh-current-main delivery reconciliation.

Observed At: 2026-08-08T19:32:15Z

Started At: 2026-08-08T18:11:22Z

Deadline or Expires At: 2026-08-08T22:11:13Z

Next Action: Acquire the exact current-main integration scope, reconcile the preserved f6ffb840 mapping onto fresh main once, run only integration-sensitive checks, deliver to main, then refresh and verify the shared installed skill catalog under its exact exclusive claim.

Next Reconciliation At: 2026-08-08T19:47:00Z

## Candidate Recovery Evidence

Candidate Commit: 87d99310abad66be170bafac9c7274a884e2c211

Candidate Base: 8d0354a930462c97984ee549230cb434411e53b9

Candidate Branch: codex/add-document-provenance-skill

Changed Paths: 46 exact claimed paths

Worktree State: Clean; no generated cache directories

Producer Checks: Renderer and shared routing 14/14; bundle integration and freshness 5/5; probe catalogs valid; skill documentation, support checklist, hierarchy, exact AGENTS rendering, and diff checks current

Package Checks: 11/11 focused validator tests plus skill, metadata, JSON, positive CLI, negative CLI, and whitespace validation passed before the unchanged package was combined with shared outputs

Producer Claim Release: add-document-provenance-package-tree-019fe291 released by event 030f30b0-2b01-4ccf-a2ce-cef18d2d7d9a

Pending Gates: One independent methodology review and one independent verifier result against this immutable commit

## Correction Attempt History

Attempt: 1

Source Candidate: 87d99310abad66be170bafac9c7274a884e2c211

Independent Review: NEEDS_CORRECTION with exactly three findings

Finding 1: Reserved provenance-bearing index.md and log.md fixtures fail the existing OKF H1 gate

Finding 2: Generated skill-browser HTML visibly renders the source provenance comment

Finding 3: Four-space-indented Markdown provenance passes placement validation

Independent Verification: All focused candidate behavior and freshness checks passed; mandatory mcp-agent-ops skill_validate was rejected because the candidate path is outside configured validation roots, and fallback was correctly prohibited

Correction Owner: Original Dev Coder task /root/implement_document_provenance

Correction Claim: add-document-provenance-correction1-019fe291, acquired event 38ead661-fc79-4ad2-a246-92d2e6f847c2 and extended event ed6ed7b6-4a1b-4dab-80a6-77477745b31c

Correction Scope: skills/document-provenance/** plus exact OKF validator/test, skill-doc renderer/test, and generated skill definition paths

Replacement Candidate: 4d3441dec8042c49cfdbb6baf244e53d2c52837d

Correction Result: All three findings resolved by focused regressions; correction claim released by event c4e7a1d7-8fa0-434b-b15d-034e3c7d087b

Replacement Review: VERDICT: GOOD from the same independent methodology reviewer; no residual finding

Replacement Verification: VERDICT: PASS from the same independent verifier after reconciling genuine primary-main-rooted mcp-agent-ops skill_validate {ok:true, findings:[]} on the exact clean 4d3441de package, git diff --check, and the preserved 14/14 validator, 8/8 OKF, and 2/2 renderer/freshness evidence; prior refusals were session-root routing failures, not source findings

## Resource Ownership Reconciliation Evidence

Reconciliation Trigger: Parent-directed immediate reconciliation after producer mutation began before a child path or tree claim existed.

Producer Pause: Dev Coder task /root/implement_document_provenance was interrupted before reconciliation reads and remained paused through the claim attempt.

Out-of-Sequence Path: skills/document-provenance/scripts/test_validate_document_provenance.py

Out-of-Sequence Byte SHA-256: 045e93c8fc4522eae01ce909fb3537d7c7341775e76977500f615fa668fd716d

Out-of-Sequence Diff SHA-256: 9ff148087bf3dc540042e8d98583eb8f3774adcb5e45f70007523cf0a1554763

Out-of-Sequence Diff Fact: New untracked text file, 186 lines; complete unified diff was captured read-only before claim acquisition.

Out-of-Sequence Path: skills/document-provenance/scripts/__pycache__/test_validate_document_provenance.cpython-311.pyc

Out-of-Sequence Byte SHA-256: 2cb6f0dc23c77366fd590f690034c4c0878e081c8b8c80f5cb1f096139ea8f74

Out-of-Sequence Diff SHA-256: fe3b44df5d25441b1f4cc9e827d7e0a14e7501d8b55effffd4dcdf4155f79d2d

Out-of-Sequence Diff Fact: New untracked binary file, 10860 bytes; binary-difference evidence was captured read-only before claim acquisition.

Preservation Disposition: Both paths remained unchanged throughout reconciliation; no out-of-sequence byte was discarded or rewritten.

Claim Attempt Count: 1

Child Tree Claim: add-document-provenance-package-tree-019fe291

Claim Scope: skills/document-provenance/**

Claim Owner: Dev Coder task /root/implement_document_provenance

Parent Claim: add-document-provenance-work-019fe291-r2

Claim Outcome: SHARED_CHECKOUT_ACQUIRED

Claim Event: 9aeaff46-ebb9-489a-ab55-3c3e83b9d4c0

Claimed At: 2026-08-08T18:24:20.750128Z

Resume Disposition: Resume the same producer from the preserved bytes under the acquired child tree claim; no bundle item, shared catalog, generated output, shared review, or integration path is authorized by this reconciliation.

## Finish-Lane Release Evidence

Notification Type: Direct one-time release and recovery notification from parent Dev Backlog Coordinator task 019fb057-1767-7ef2-b5fa-41f4417b20b3

Cleared Work Item: reconcile-bundle-content-suite-drift

Terminal Provider Commit: 8d0354a930462c97984ee549230cb434411e53b9

Accepted Replacement: d4a97090

Recorded Integration: 2dedbfa4061cd5fa128dd429de00e1d55bb1f7e9

Aggregate Verification: 168/168

Claim and Cleanup Evidence: Parent reported every bundle work, path, integration, and provider claim released; detached candidate worktree and task-owned branch residue absent; canonical task archived.

Current-Main Reconciliation: Read exactly once after notification; observed main at 8d0354a930462c97984ee549230cb434411e53b9 with recorded integration and accepted replacement ancestral.

Preservation Boundary: Preserve design/agent-owned-evaluation-suites.html and recorded residual bundle defects; do not rerun completed private package gates solely because main advanced.

## Completion Evidence

- The immutable accepted replacement is 4d3441dec8042c49cfdbb6baf244e53d2c52837d, built additively from candidate 87d99310abad66be170bafac9c7274a884e2c211.
- The independent methodology reviewer returned VERDICT: GOOD with no residual finding.
- The same independent verifier returned VERDICT: PASS after reconciling genuine mcp-agent-ops skill_validate `{ok:true, findings:[]}` on the exact clean candidate with the preserved 14/14 validator, 8/8 OKF, 2/2 renderer/freshness, and git diff evidence.
- Terminology-standard main d9e12b27087ee3fe34ae38b1eeae477342a4233a and the document-provenance replacement were combined without overwriting either contract. Candidate commits map to integration commits 53c30c00 and f6ffb840; current main delivery commit d4cd66c6e6b8a8e90314ae0a7f683a740ab5ede2 contains both mappings.
- Python 3.11 focused coexistence tests passed for both document-provenance and terminology-standard bundle contracts. build-skill-docs, build-agent-skill-hierarchy, and build-support-checklist were byte-current; git diff validation passed.
- The separately owned design/agent-owned-evaluation-suites.html remained unchanged at SHA-256 0e6461d094261ef0e80323d65e77245781aaa40c51976ef5f49b4204f977bdef.
- Under exact shared-install claim add-document-provenance-shared-install-019fe291, the Codex user skill catalog was refreshed after main delivery. The installed package is byte-identical to canonical main, catalog/SKILL digest ed1c5c69e223993b82f103537c188d167f936c474fc0a095f0a3fe3717349ef1, and installed skill validation returned `{ok:true, findings:[]}`.
- Root work claim add-document-provenance-work-019fe291-r2 was released with handoff in event ea5cba12-669d-41a2-9d9a-288cea1c2a3d before exact Work Item update claim add-document-provenance-update-019fe291 and terminal path claim add-document-provenance-terminal-paths-019fe291 were acquired.

## Verification

- Validate the complete document-provenance skill package with the repository-native Agent Skill validator and any available structured skill validator without bypassing a configured-root rejection.
- Run focused bundle-content tests for the new skill identifier, package metadata, catalog membership, role routing, project-configuration output, template ownership, and generated adapter freshness.
- Run focused deterministic validator tests for every positive and negative fixture listed in Requirements.
- Run focused project-wiki checks proving that provenance after YAML front matter remains compatible with OKF validation and that reserved index.md and log.md pages remain valid without concept front matter.
- Run focused maintained-HTML checks proving that provenance placement preserves the doctype and document structure.
- Run the supported generators for affected canonical sources and verify generated files are byte-current rather than hand-edited.
- Run scripts/openai_metadata.py for the new skill package when required by its metadata surface.
- Run the applicable skill-documentation, agent-definition, hierarchy, support-checklist, technology-detection, and evaluation freshness checks implicated by the final dependency graph.
- Run git diff --check.
- Obtain an independent skill review focused on authority boundaries, portability, runtime-evidence truthfulness, Markdown and HTML placement, generated-file ownership, and negative-case completeness.
- Refresh and verify the shared installed skill catalogs only after the source candidate and generated outputs pass focused review and verification.

## Open Questions

- Should the first version use Git as the only modification-history authority, or should projects be able to configure an append-only provenance ledger for document revisions?
- Which non-Markdown document formats should be mandatory in the first portable release beyond maintained HTML?
- Which runtime adapters can supply authoritative dispatched model and reasoning-effort values directly, and what exact evidence label should be used by adapters that expose only requested configuration?
- Should Artifact-ID be project-assigned, derived once from the initial repository path, or generated as a runtime UUID?
- Which operational Markdown records under backlog or other coordination roots should be governed documents, and which should remain explicitly excluded operational records?

## Governed Definition Approval

### Governed Canonical Sources

- skills/document-provenance/SKILL.md
- skills/document-provenance/agents/openai.yaml

### Allowed Dependent Artifacts

- Directly related references, examples, assets, fixtures, and deterministic validation scripts inside the skills/document-provenance package.
- Supported generated mirrors derived from the approved document-provenance skill sources.
- Directly related non-governed tests, evaluation fixtures, README inventory, generated catalogs, design documentation, templates, and project-configuration output required to package, explain, route, and verify the new skill.

Existing skill definitions, unrelated skill metadata, conceptual agent definitions, schemas, and model-profile sources are not included merely because they may later consume document-provenance. If implementation requires another governed canonical source, preserve this approved scope and obtain additional exact-path approval only for the added source before mutating it.

### Approval Resolution

Approved at creation. On 2026-08-08, the user explicitly requested work on "a separate skill as suggested" and then directed creation of "a detailed workitem." In the originating Codex task, document-provenance was the named separate skill and the discussion established its purpose, Markdown placement decision, runtime provenance boundary, and enforcement strategy. This approval is limited to the two exact new canonical skill-package sources listed above and their allowed dependent artifacts; it does not authorize changes to existing governed definitions by implication.

## Notes

- The requested identifier is document-provenance.
- The Markdown HTML comment is source-visible but render-hidden. It is chosen to avoid taking ownership of YAML front-matter schemas.
- The canonical Markdown example should keep the exact copyright statement on its own line, followed by exact field labels. Avoid a redundant Copyright field prefix that changes the required statement.
- The initial skill should describe evidence quality explicitly, such as runtime-supplied, git-derived, or historical-unknown, without permitting historical labels on newly created governed documents.
- The static documentation model profile is configuration evidence, not historical execution evidence. A later profile change must not rewrite or reinterpret existing document headers.
- This item creates a reusable methodology capability. It does not itself authorize a repository-wide historical rewrite before the migration boundary, exclusions, and evidence labels are implemented and reviewed.
