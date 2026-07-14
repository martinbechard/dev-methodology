---
name: documentation-reverse-engineer
description: Use when deriving a complete source-backed documentation and reconstruction package from an existing codebase and proving reconstruction readiness against the original baseline.
metadata:
  category: documentation-methodology
---

# Documentation Reverse Engineer

Use this skill to derive and evaluate a source-backed reconstruction package from an existing codebase. Work from the smallest implementation units outward: modules, subsystems, architecture, functional behavior, README and wiki integration, then independent reconstruction and parity evaluation.

## Coverage Contract

When the request names a repository, application, or project without a narrower boundary, the entire codebase is in scope. Do not ask the user to choose a documentation breadth and do not offer a representative, sampled, minimal, or tiered documentation set. A narrower run is valid only when the user explicitly names the included boundary. In that case, record the excluded repository areas and do not claim that the project was fully reverse engineered.

Full coverage means documenting every meaningful runtime responsibility, not creating one page per class or file. A meaningful module includes an independently understandable backend responsibility, public contract, persistent aggregate, UI route or feature area, integration, security boundary, background or operational process, or build and deployment capability. Tightly coupled files may share one module document only when their responsibility and lifecycle cannot be understood independently.

The documentation set must preserve enough evidence to recreate the application's observable behavior in another folder. Cover public interfaces, data models and migrations, initial or sample data, configuration behavior, authentication and authorization, user workflows and UI states, validation and error behavior, integrations, operational commands, build and deployment behavior, and the tests that define expected results. Record unsupported or unknowable behavior as a specific open question rather than silently omitting it.

Every exact baseline path also needs one reconstruction disposition. MUST_DOCUMENT means the package contains the construction facts, contracts, data, configuration, and behavior needed to recreate the responsibility. PUBLIC_GENERATOR means a generator obtainable without original-source access can recreate the path from locked public inputs and an explicit invocation. PARITY_TEST_ONLY means the path does not need construction detail but its observable responsibility is covered by one or more executable parity cases. Every path gets exactly one of these dispositions. A generated classification is not sufficient and does not exempt the path from disposition, generator-differential, or parity evidence.

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

Create a machine-checkable path coverage ledger beside the manifest. Capture the exact source-baseline commit and inventory every tracked path plus every meaningful untracked source or configuration path present at that baseline. For each path record its classification, owning module or responsibility, manifest row, one of IN_SCOPE, GENERATED, VENDORED, FIXTURE_ONLY, SETUP_ARTIFACT, or USER_EXCLUDED, and exactly one reconstruction disposition: MUST_DOCUMENT, PUBLIC_GENERATOR, or PARITY_TEST_ONLY. Any non-IN_SCOPE classification requires a concrete generator, owner, fixture use, setup contract, or explicit user boundary; directory-level labels without path entries are insufficient. A generated classification is not sufficient reconstruction evidence.

Compare the ledger mechanically with the baseline inventory. The set difference in both directions must be empty, duplicate path entries are invalid, and the ledger must contain zero `UNCLASSIFIED`, blank-owner, or implicitly deferred paths. Hidden files, root manifests, build scripts, migrations, assets, test support, CI, and operational configuration are part of the inventory; do not limit the ledger to conventional source extensions.

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
7. Create the path coverage ledger from the exact source baseline and mechanically prove that every inventoried path maps to a manifest row or a justified non-source classification.
8. Assign every path exactly one reconstruction disposition and link each disposition to its document evidence, public-generator contract, or parity case IDs.

Completion gate:

- Documentation root is known.
- Source and test roots are known.
- Existing documentation is inventoried.
- Verification commands are known or recorded as not yet identified.
- Every in-scope source area appears in the coverage manifest as a module responsibility or an evidence-backed generated, vendored, or fixture-only exclusion.
- The path coverage ledger matches the baseline inventory exactly, has no duplicate or unclassified path, maps every IN_SCOPE path to a manifest row, and assigns every path exactly one allowed reconstruction disposition.

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
10. Treat the path ledger as an ownership contract, not an evidence boundary. Link the direct caller, dependency, schema, configuration, security, error-adapter, and test sources needed to support claims even when another manifest row owns those files.
11. Close the evidence chain before review: every caller, dependency, public contract, processing rule, invariant, error behavior, and verification claim must link direct source evidence or be labeled as an inference, unverified behavior, or open question.
12. Distinguish executable verification from test-shaped source. Confirm the method is discovered and runs: check framework annotations/registration, disabled or ignored state, dependency injection, fixtures, assertions, and the invoked branch. Do not report an unannotated helper, dormant fixture, prospective command, or requested test as executed coverage.
13. Trace failure behavior through the actual branch, including wrapper fallback, swallowed subprocess errors, nested exception causes, validation differences by HTTP method, retry/recovery, logging, and transaction rollback. Describe the implementation as it is; record stronger desired behavior as a gap, not an invariant.
14. For build and contributor modules, verify wrapper semantics, default versus opt-in lifecycle goals, source-mutating tasks, runtime selection, and README commands against the committed scripts and configuration.
15. Update the coverage manifest as each module document passes review.

Prefer one module document for one coherent responsibility. Split only when separate responsibilities can change independently.

Completion gate:

- Every in-scope manifest row has a module document and an accepted module-design review.
- Every module document identifies its source paths, contracts, dependencies, runtime behavior, state, error behavior, configuration, security implications, related tests, and open questions where applicable.
- The module's explicit project-relative runtime path is present; execution prose is not a substitute for the path.
- Every cross-module claim closes to direct evidence outside the owned path set when necessary; no page uses ownership as a reason to omit caller, schema, configuration, security, or test authority.
- Verification claims distinguish executed tests from unannotated helpers, dormant fixtures, requested checks, and other prospective evidence.
- Error and build-tool claims match implemented fallback, validation, nested-cause, retry, rollback, wrapper, and lifecycle behavior rather than a safer intended contract.
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
8. When the parent architecture is intentionally created in Pass 3, record its expected project-relative path as a provisional target, state the currently inherited constraints from accepted modules and project configuration, and do not create a broken Markdown link. This ordered-workflow exception is not permission to omit the parent permanently.

Subsystems should be based on runtime collaboration and ownership, not only folder layout.

Completion gate:

- Every accepted module document is linked from at least one high-level design.
- Every high-level design links all of its constituent module documents and has an accepted high-level-design review.
- Every high-level design either links an accepted existing parent architecture or records the Pass 3 parent target and inherited constraints explicitly.
- The full module set is grouped by runtime collaboration without orphaned modules.
- Pass 3 must not start until this gate passes.

## Pass 3: Architecture

1. Review the full set of high-level design documents.
2. Read module documents where subsystem boundaries, dependency direction, state ownership, technology choices, or cross-cutting rules need evidence.
3. Create or update the architecture document using the architecture template.
4. Document system purpose, scope, context, technology stack, file organization, architectural layers, key components, data movement, lifecycle, cross-cutting concerns, design principles, invariants, risks, trade-offs, and verification.
5. Link all high-level design documents from the architecture document.
6. Record architecture-level contradictions as open questions.
7. Replace each provisional high-level-design parent target with a resolving link to the accepted architecture, reconcile inherited constraints against the architecture, and independently re-review every changed high-level design before closing Pass 3.

Architecture must describe the system that exists. It may call out drift and risk, but it must not silently rewrite behavior.

Completion gate:

- The architecture links every accepted high-level design and explains all cross-subsystem dependencies and cross-cutting responsibilities.
- The architecture has an accepted architecture review.
- Every accepted high-level design links back to the accepted parent architecture; no provisional Pass 2 parent target remains.
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
- Wiki and documentation verification passes.
- Pass 6 must not start until this gate passes, and the run must not be reported as complete reverse engineering before Pass 6 passes.

## Pass 6: Reconstruction Readiness And Parity Evaluation

Pass 6 is mandatory for every whole-project run reported as complete reverse engineering. A run that stops after Pass 5 may report that its documentation gates passed, but it must not claim reconstruction readiness or complete reverse engineering.

1. Reconcile the exact baseline inventory against the reconstruction-disposition ledger mechanically in both directions. Reject missing, duplicate, blank, extra, or unknown dispositions.
2. For each MUST_DOCUMENT path, verify that accepted documents contain the construction facts needed by an independent builder. Original-source links remain traceability evidence; they are not a substitute for self-contained construction instructions.
3. For each PUBLIC_GENERATOR path, package the generator identity, locked version or digest, public inputs, invocation, output contract, comparison policy, and dependency provenance. The generator must be obtainable without access to the original repository.
4. For each PARITY_TEST_ONLY path, link at least one executable parity case that observes the responsibility. No path may use this disposition only to avoid documentation work.
5. Create the reconstruction root as a brand-new empty destination outside the source project. Copy the complete docs/wiki tree first by value, then copy the remainder of the complete docs tree, linked root documentation, PROJECT.yaml, every applicable AGENTS.md and CLAUDE.md, declared public-generator inputs, and declared parity contracts. Do not write reconstruction code before the copied seed validates inside that destination.
6. Preserve project-relative links from documentation to application source as non-seed evidence references in the seed manifest and reconcile them against the path ledger. Do not copy the referenced application source. Every documentation or configuration dependency must resolve inside the seed; source-evidence references may remain unresolved inside the destination only when they are explicitly recorded and no construction claim depends on reading them.
7. Use the portable reconstruction-run helper under this skill's scripts directory to hash every copied input, record wiki-first copy phases and run metadata, validate exact file and hash equality inside the destination, and reject symbolic links, hard links, absolute original-source paths, workstation-specific user-home paths, source-root escapes, and undeclared seed files. Store repository evidence paths project-relative. Use portable variables or declared container roots for genuine external runtime paths instead of embedding a checkout, worktree, cache, or temporary-directory path.
8. Capture the original baseline oracle before the builder receives access to its environment. Record the exact commands, inputs, fixtures, environment, exit statuses, observable outputs, normalized results, and digests for build, test, route, workflow, data, security, integration, configuration, operational, and deployment behavior that exists in the project. Bind each result to an immutable source tree, built artifact, process or container identity, command, and run ID derived by the verifier rather than supplied as an unchecked label. The oracle may expose only the behavior needed for comparison; it must not contain original application source, source excerpts, absolute original-source paths, source-derived caches, or undeclared artifacts that could serve as reconstruction inputs.
9. Create a machine-readable parity case catalog. Each case needs a unique stable ID, owning behavior or disposition, preconditions, inputs, original command, reconstruction command, comparison policy, required probe kind, required evidence, and mandatory execution strength. Seal the evaluator implementation, governing contract, accepted case inventory, probe inventory, and immutable oracle under one digest. The evaluator must reject unknown, duplicate, missing, unattempted, wrong-kind, weak, or provenance-unbound evidence and must recompute every case status, alias, disposition, count, and final verdict from sealed fragments; caller-supplied READY labels are never evidence.
10. Run every PUBLIC_GENERATOR against the original baseline and the reconstructed project. Reconcile the expected and actual generated file sets exactly in a machine-readable delta ledger. Each row records generator ID, path, original result or digest, reconstructed result or digest, comparison policy, status, evidence, and resolution. Explicitly normalize source-backed nondeterministic fields; do not ignore them informally.
11. Give a distinct builder only the validated seed and declared external toolchain. Enforce the boundary with an operating-system sandbox or container whose readable mounts exclude the original repository, its parent workspace, source-derived caches, and undeclared temporary paths. Before the real run, use the exact image, mounts, environment, user, and nested sandbox policy against a disposable repository to prove both a content-reading source-denial probe and the required acquire/release agent-claim lifecycle. Grant only the narrow reconstruction metadata write surface needed by the claim mechanism when the nested sandbox would otherwise make `.git` read-only. An instruction-only boundary, working-directory convention, permission predicate, or honor-system promise is not valid.
12. Give a distinct verifier in a fresh operating-system sandbox or container only the reconstructed application, immutable oracle package, parity and generator contracts, and declared external toolchain. The verifier must not receive the original source, builder-private workspace, or builder working context.
13. From inside both environments, run and record denied-access probes against the original repository's canonical path, alternate path, parent traversal, symlink, hardlink, cache, temporary-file, and environment-variable channels. Each denial probe must attempt an actual content open and byte read with at least two independent readers; shell metadata or `test -r` predicates are insufficient because they can disagree with real access. Record mounts, environment, working directory, caches, credentials, network access, dependency provenance, commands, outcomes, and evidence digests in a machine-readable contamination ledger.
14. Build the full project in the reconstruction root. The independent verifier then runs every parity case and generator differential against the immutable original baseline oracle. Native build, lint, unit, integration, browser, performance, packaging, container, TLS, operations, and deployment gates that exist in the contract must execute at their real boundary; source inspection or an `OWNED_SMOKE` label cannot satisfy a required runtime gate. Importers must prove the complete expected suite identity and reject unmatched failures, skips, partial suites, synthetic fixtures, or artifacts not bound to the recorded command and target. Reconcile case IDs and result sets exactly in both directions; no missing, unexpected, duplicate, skipped, silently unrun, UNRUNNABLE, or failed required case may pass.
15. Send the complete package to review-reconstruction-readiness. Correct blocking findings and repeat the independent review in a fresh context. Do not let the builder review or verify its own reconstruction.
16. Archive every attempted run, including failed and blocked runs, with exact content hashes and status evidence. Capture a full pre/post Git metadata inventory for every generator and reconcile all changes, including the transient claim registry, rather than checking only `.git/config`. Keep immutable input manifests separate from post-run evidence: compute final claims from the final bytes and write their attestation outside the attested set so a mutable or self-referential manifest cannot retain a stale digest. Seal and validate the new archive before pruning; then retain the newest three valid run archives unless the user explicitly selects another count.

Completion gate:

- Every baseline path has exactly one accepted reconstruction disposition and its required evidence.
- The copied seed is self-contained for construction, was validated inside a new destination, records all source-evidence references, and contains no original application source or unresolved contamination.
- Every PUBLIC_GENERATOR output reconciles with zero missing, unexpected, failed, or unresolved delta.
- Every parity case has one immutable original oracle result and one independently verified reconstructed result, and all required cases pass.
- Builder and verifier isolation is enforced by the operating system or container runtime and confirmed by denied-access probes; prompt compliance is never sufficient.
- The reconstructed application passes the documented build, test, route, workflow, data, security, integration, configuration, operational, and deployment parity contract.
- The reconstruction-readiness review passes and the exact run archive validates before newest-three retention is applied.

## Verification

After the passes:

1. Use review-module-design on created or changed module design documents.
2. Use review-high-level-design on created or changed high-level design documents.
3. Use review-architecture on created or changed architecture documents.
4. Use review-functional-spec on created or changed functional specifications.
5. Use project-wiki-review on created or changed project wiki methodology pages.
6. Use review-reconstruction-readiness on the complete Pass 6 package.
7. Use documentation-page-verify for mixed, unknown, or custom documentation artifacts.
8. Run the project's build command when documentation work changed code, generated artifacts, or project metadata that can affect the build.
9. Run documentation or wiki lint when available.
10. Search new documentation for unresolved TODO markers that are not intentional.
11. Search new steady-state documentation for stale comparative language such as enhanced, revised, old, and new.
12. Confirm every created document has related source, related test, or Not yet identified entries.
13. Confirm every diagram represents a real sequence, association, aggregation, containment, ownership, dependency, lifecycle, coverage, or data movement relationship.
14. Confirm every open question is specific enough for a human or future agent to answer.

Stop and ask for human input when source conflicts cannot be resolved, business ownership would be guessed, private systems are needed, verification cannot run for environmental reasons, or the work would send private material to an external service without explicit authorization.

## Reconstruction Evaluation Runs

Use this protocol only for a controlled reverse-engineering evaluation, not for routine documentation maintenance.

1. Archive the current documentation and project-routing snapshot before destructive reset work.
2. Delete the documentation folder from the source-under-test before the run starts. When the evaluation includes project-routing reconstruction, also delete PROJECT.yaml and the applicable generated AGENTS.md files. Commit or otherwise record the exact reset baseline.
3. Run Pass -1 through Pass 5 from the reset baseline. A failed pass stops the run; do not create higher-level artifacts after a failed lower-level gate. Archive that failed attempt before another run begins.
4. Run executable Pass 6. Create a new empty reconstruction folder and copy the completed wiki into that folder first, then the complete documentation and configuration seed, before any reconstruction code is written.
5. Give a distinct builder only the validated seed and declared external toolchain, then give a distinct verifier only the reconstructed application and immutable oracle package. Enforce both boundaries with operating-system sandbox or container policy. Do not allow either step to inspect or copy the original application source. If the runtime cannot enforce and prove those filesystem boundaries, mark the evaluation BLOCKED; an instruction-only or honor-system boundary is not valid evidence.
6. Recreate the application in the reconstruction folder, then reconcile all generator outputs and parity cases against the original baseline oracle.
7. Archive the exact content set below for every successful, failed, or blocked attempt:

- RUN.json with status, source baseline, documentation baseline, owners, commands, timestamps, and environment identity.
- reset/source-baseline.json with the reset commit or digest and exact path inventory.
- configuration/PROJECT.yaml and configuration/AGENTS.md, plus nested routing files in the same configuration tree.
- documentation/docs/wiki and the full accepted documentation corpus.
- reviews/reconstruction-readiness.review-checklist-reconstruction-readiness.md and every lower-level completed review checklist.
- seed/seed-manifest.json and copied-seed validation results.
- oracle/original-baseline.json and its immutable hash manifest.
- reconstruction with the reconstructed source, configuration, migrations, assets, tests, and scripts, excluding fetched dependency caches.
- parity/cases.json and parity/reconciliation.json.
- generators/delta-ledger.json and generator command results.
- contamination/ledger.json with sandbox definitions, mount inventories, denied-access probes, and resolutions.
- execution/commands.jsonl and execution/results.json.
- metrics/usage.json with elapsed time and available token or cost evidence by activity; unavailable measurements are recorded as unavailable rather than estimated.
- archive-manifest.json with the exact archive file set, sizes, and SHA-256 digests.

Every required archive entry must exist for failed and blocked attempts too. When a stage never started, store a non-empty machine-readable NOT_RUN record naming the unmet gate and failure evidence instead of omitting the entry or fabricating a result.

8. Validate the newly sealed archive by reproducing its exact file set and every digest. Only after that validation may retention delete older runs. Keep the newest three evaluation runs unless the user specifies another retention count.

Initialize a run and seal its archive with the portable helper:

```bash
python3 skills/documentation-reverse-engineer/scripts/reconstruction_run.py initialize --source-project /source/project --build-root /new/reconstruction-root --run-id run-001 --source-baseline BASELINE
python3 skills/documentation-reverse-engineer/scripts/reconstruction_run.py validate-seed --build-root /new/reconstruction-root --exact
python3 skills/documentation-reverse-engineer/scripts/reconstruction_run.py seal-archive --new-archive /archives/run-001 --archive-root /archives --retain 3
```

For checklist-only model evaluation, assign a corpus ID derived from the source baseline, artifact digest, checklist version, and adjudicated defect set. Run the lower-cost candidate and reference reviewer separately in fresh contexts at least three times with identical artifacts, source evidence, and checklist questions, and capture every invocation, verdict, citation, elapsed time, token count, and cost. Compare defect recall, false positives, checklist completeness, quoted source evidence, elapsed time, and token cost.

Promote the candidate only when it completes every checklist question, misses none of the adjudicated blocking defects, produces no more false positives than the reference median, provides source evidence for every verdict, and reduces median elapsed time or token cost by at least 20 percent without increasing the other cost measure. Reject the candidate on any quality regression and retain the reference reviewer. Model cost never justifies sampled coverage or skipped questions.
