---
name: documentation-reverse-engineer
description: Use when deriving functional, architecture, high-level design, module design, README, or wiki documentation from an existing codebase.
metadata:
  category: documentation-methodology
---

# Documentation Reverse Engineer

Use this skill to derive a source-backed documentation set from an existing codebase. Work from the smallest implementation units outward: modules, subsystems, architecture, functional behavior, then README and wiki integration.

## Coverage Contract

When the request names a repository, application, or project without a narrower boundary, the entire codebase is in scope. Do not ask the user to choose a documentation breadth and do not offer a representative, sampled, minimal, or tiered documentation set. A narrower run is valid only when the user explicitly names the included boundary. In that case, record the excluded repository areas and do not claim that the project was fully reverse engineered.

Full coverage means documenting every meaningful runtime responsibility, not creating one page per class or file. A meaningful module includes an independently understandable backend responsibility, public contract, persistent aggregate, UI route or feature area, integration, security boundary, background or operational process, or build and deployment capability. Tightly coupled files may share one module document only when their responsibility and lifecycle cannot be understood independently.

The documentation set must preserve enough evidence to recreate the application's observable behavior in another folder. Cover public interfaces, data models and migrations, initial or sample data, configuration behavior, authentication and authorization, user workflows and UI states, validation and error behavior, integrations, operational commands, build and deployment behavior, and the tests that define expected results. Record unsupported or unknowable behavior as a specific open question rather than silently omitting it.

## Pass -1: Project Configuration

Reverse engineering begins with project setup, before documentation inventory or writing.

1. Inspect the repository's manifests, source roots, test roots, runtime boundaries, and verification commands.
2. Inspect the technology skills actually exposed by the target runtime and run setup-time technology detection for representative source scopes.
3. Create or reconcile the single root `PROJECT.yaml` from repository evidence. Record every folder loadout, selected skill, source match, runtime-availability result, missing requirement, conflict, and explicit no-variant result.
4. When no pertinent specialized skill is available for a scope, record `NO_VARIANT` and use general model training for that scope. Do not invent a skill, skip the scope, or call the whole run blocked. A detected required-but-unavailable skill remains `BLOCKED`.
5. Generate or update root and nested `AGENTS.md` files from the accepted configuration. The resulting guidance gives every source area an operational route.
6. Send `PROJECT.yaml` and every generated agent-guidance file for independent review and correction.

Completion gate:

- `PROJECT.yaml` is source-backed, contains no unresolved template instructions, and is independently accepted.
- Every selected technology skill is exposed by the target runtime, and every `NO_VARIANT` scope records its general-model-training fallback.
- Root and nested `AGENTS.md` routing matches the accepted configuration.
- Pass 0 must not start until this gate passes.

Create a documentation coverage manifest under the documentation root before authoring design documents. Use these columns:

| Module or responsibility | Source paths | Entry points and contracts | Related tests | Module document | Review status |
| --- | --- | --- | --- | --- | --- |

Map every in-scope source area to one or more rows. List generated, vendored, fixture-only, and explicitly user-excluded areas separately with their generator, owner, or exclusion reason. An unlisted or deferred source area is a coverage failure.

## Source Authority

Use this authority order when sources disagree:

1. Code and tests describe actual behavior.
2. Functional specifications and requirements describe intended behavior.
3. Project procedures and agent instructions describe workflow obligations.
4. Backlog files describe tracked work and known status.
5. Architecture, high-level design, module design, and plan documents describe design intent.
6. Wiki pages summarize and navigate the sources above.

Do not invent behavior to fill gaps. Record an open question when the repository does not provide enough evidence.

## Pass 0: Repository Orientation

1. Identify source roots, test roots, application entry points, scripts, configuration files, migrations, public routes, command entry points, and generated artifacts.
2. Identify existing documentation roots and note whether they contain functional, architecture, high-level design, module design, or wiki pages.
3. Identify build, test, lint, and documentation commands from project metadata and procedures.
4. Identify current worktree status when the project is a Git repository.
5. Record documentation gaps and conflicts for later passes.
6. Create the documentation coverage manifest and populate its module inventory from the full source, test, configuration, migration, UI, integration, and operational surface.

Completion gate:

- Documentation root is known.
- Source and test roots are known.
- Existing documentation is inventoried.
- Verification commands are known or recorded as not yet identified.
- Every in-scope source area appears in the coverage manifest as a module responsibility or an evidence-backed generated, vendored, or fixture-only exclusion.

## Code Discovery Tools

Use source inventory first, then use structure-aware search where it adds evidence.

- Use rg or repository file walking for source roots, filenames, plain text references, configuration keys, route strings, generated artifacts, and broad source inventory.
- Use grep only as a portability fallback when rg is unavailable.
- Use a routed structure-aware search tool when discovery depends on syntax, nesting, imports, exports, callers, route declarations, component shapes, async flow, error handling, or test structure.
- Confirm an optional search tool is available before using it. If it is unavailable, continue with text search, repository file walking, and direct source reading.
- Do not treat structural matches as documentation evidence until the matched code has been read.
- Use structural search to seed candidate modules, callers, contracts, tests, and relationships; use source reading to decide responsibility, ownership, behavior, and document boundaries.

## Pass 1: Module Designs

1. Walk source roots and identify modules by runtime responsibility.
2. Use the Code Discovery Tools section to seed candidate modules, callers, imports, exports, routes, tests, and structural relationships before reading files deeply.
3. For each meaningful module, read implementation, callers, imports, exported contracts, tests, configuration use, persistence use, and user-visible behavior.
4. Create or update one module design document per meaningful module or tightly coupled module folder.
5. Use the module design template from development-methodology assets.
6. Add a Processing Diagram only when conditional flow, retries, error handling, or state transitions are difficult to understand from prose alone.
7. Link related tests and source files from each module document.
8. Record missing tests, ambiguous ownership, and undocumented side effects as open questions.
9. When an important value crosses module, persistence, serialization, external-system, security, or UI boundaries, trace its source, transformations, validations, ownership, storage, and consumers. Document only lineage that affects correctness, privacy, security, or operability.
10. Update the coverage manifest as each module document passes review.

Prefer one module document for one coherent responsibility. Split only when separate responsibilities can change independently.

Completion gate:

- Every in-scope manifest row has a module document and an accepted module-design review.
- Every module document identifies its source paths, contracts, dependencies, runtime behavior, state, error behavior, configuration, security implications, related tests, and open questions where applicable.
- No in-scope source area is undocumented, implicitly deferred, or represented only by a higher-level document.
- Pass 2 must not start until this gate passes.

## Pass 2: High-Level Designs

1. Review module design documents and identify clusters that collaborate to deliver one subsystem, feature family, workflow engine, integration, UI area, or operational capability.
2. Create or update one high-level design document per subsystem.
3. Use the high-level design template from development-methodology assets.
4. Add diagrams for structural relationships inside the sections they clarify.
5. Link every constituent component document from the subsystem document.
6. Link functional specifications when a subsystem directly serves user-visible workflows.
7. Record overlapping ownership and missing subsystem boundaries as open questions.

Subsystems should be based on runtime collaboration and ownership, not only folder layout.

Completion gate:

- Every accepted module document is linked from at least one high-level design.
- Every high-level design links all of its constituent module documents and has an accepted high-level-design review.
- The full module set is grouped by runtime collaboration without orphaned modules.
- Pass 3 must not start until this gate passes.

## Pass 3: Architecture

1. Review the full set of high-level design documents.
2. Read module documents where subsystem boundaries, dependency direction, state ownership, technology choices, or cross-cutting rules need evidence.
3. Create or update the architecture document using the architecture template.
4. Document system purpose, scope, context, technology stack, file organization, architectural layers, key components, data movement, lifecycle, cross-cutting concerns, design principles, invariants, risks, trade-offs, and verification.
5. Link all high-level design documents from the architecture document.
6. Record architecture-level contradictions as open questions.

Architecture must describe the system that exists. It may call out drift and risk, but it must not silently rewrite behavior.

Completion gate:

- The architecture links every accepted high-level design and explains all cross-subsystem dependencies and cross-cutting responsibilities.
- The architecture has an accepted architecture review.
- Pass 4 must not start until this gate passes.

## Pass 4: Functional Specifications

1. Review architecture, high-level designs, module designs, routes, UI components, command entry points, integration points, tests, and existing product documents.
2. Identify user-visible workflows, admin workflows, operator workflows, external-system workflows, route behavior, permissions, statuses, error states, and acceptance behavior.
3. Create or update functional specifications using the functional specification template.
4. Write workflows from the actor's point of view.
5. Add a Workflow Diagram when actor paths, branching states, permissions, or external handoffs are clearer visually.
6. Link technical documents and modules that implement each workflow.
7. Link tests that verify each workflow, state, edge case, and permission rule.
8. Record mismatches between intended behavior and actual code behavior as open questions or known defects.

Functional specifications describe observable behavior. Technical implementation details belong in related technical documents unless users need that detail to understand behavior.

Completion gate:

- Every user, administrator, operator, and external-system entry point is covered by a functional specification or explicitly identified as having no user-visible workflow.
- Every functional specification links its implementing technical documents and available behavioral tests and has an accepted functional-specification review.
- Pass 5 must not start until this gate passes.

## Pass 5: README And Wiki Integration

Create or update the project README after the documentation set exists. Keep it compact and route readers to deeper pages.

When the project uses docs/wiki:

1. Treat generated functional and technical documents as wiki page subclasses when they live under docs/wiki.
2. Create or update hub and index pages that summarize the documentation set.
3. Ensure durable wiki pages and subclasses include Related Code and Related Tests.
4. Link functional specs, architecture, high-level designs, module designs, source files, tests, procedures, known defects, and open decisions.
5. Record unresolved contradictions in wiki Open Questions.
6. Run wiki lint when available.

Completion gate:

- README and wiki hubs expose the complete architecture, high-level design, module design, and functional specification hierarchy.
- The coverage manifest contains no missing, pending, sampled, or implicitly deferred in-scope module.
- Wiki and documentation verification passes before the run is reported complete.

## Verification

After the passes:

1. Use review-module-design on created or changed module design documents.
2. Use review-high-level-design on created or changed high-level design documents.
3. Use review-architecture on created or changed architecture documents.
4. Use review-functional-spec on created or changed functional specifications.
5. Use project-wiki-review on created or changed project wiki methodology pages.
6. Use documentation-page-verify for mixed, unknown, or custom documentation artifacts.
7. Run the project's build command when documentation work changed code, generated artifacts, or project metadata that can affect the build.
8. Run documentation or wiki lint when available.
9. Search new documentation for unresolved TODO markers that are not intentional.
10. Search new steady-state documentation for stale comparative language such as enhanced, revised, old, and new.
11. Confirm every created document has related source, related test, or Not yet identified entries.
12. Confirm every diagram represents a real sequence, association, aggregation, containment, ownership, dependency, lifecycle, coverage, or data movement relationship.
13. Confirm every open question is specific enough for a human or future agent to answer.

Stop and ask for human input when source conflicts cannot be resolved, business ownership would be guessed, private systems are needed, verification cannot run for environmental reasons, or the work would send private material to an external service without explicit authorization.

## Reconstruction Evaluation Runs

Use this protocol only for a controlled reverse-engineering evaluation, not for routine documentation maintenance.

1. Archive the current documentation and project-routing snapshot before destructive reset work.
2. Delete the documentation folder from the source-under-test before the run starts. When the evaluation includes project-routing reconstruction, also delete `PROJECT.yaml` and the applicable generated `AGENTS.md` files. Commit or otherwise record the exact reset baseline.
3. Run Pass -1 through Pass 5 from the reset baseline. A failed pass stops the run; do not create higher-level artifacts after a failed lower-level gate.
4. After every documentation gate passes, create a new empty reconstruction folder and copy the completed wiki and its linked documentation into that folder before any reconstruction code is written.
5. Give a distinct reconstruction owner only the completed documentation set and declared external toolchain. Run it in an isolated environment whose readable project roots contain the reconstruction folder but not the original repository. Do not allow it to inspect or copy the original application source. If the runtime cannot enforce that filesystem boundary, mark the evaluation `BLOCKED`; an instruction-only or honor-system boundary is not valid evidence.
6. Recreate the application in the reconstruction folder, then run the documented build, tests, routes, workflows, data behavior, security behavior, and operational checks needed to compare observable functionality.
7. Archive the reset baseline, configuration, documentation, completed checklists, reconstruction output, commands, results, timing, and token or cost evidence. Keep the newest three evaluation runs unless the user specifies another retention count.

For checklist-only model evaluation, assign a corpus ID derived from the source baseline, artifact digest, checklist version, and adjudicated defect set. Run the lower-cost candidate and reference reviewer separately in fresh contexts at least three times with identical artifacts, source evidence, and checklist questions, and capture every invocation, verdict, citation, elapsed time, token count, and cost. Compare defect recall, false positives, checklist completeness, quoted source evidence, elapsed time, and token cost.

Promote the candidate only when it completes every checklist question, misses none of the adjudicated blocking defects, produces no more false positives than the reference median, provides source evidence for every verdict, and reduces median elapsed time or token cost by at least 20 percent without increasing the other cost measure. Reject the candidate on any quality regression and retain the reference reviewer. Model cost never justifies sampled coverage or skipped questions.
