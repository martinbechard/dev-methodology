---
name: documentation-reverse-engineer
description: Use when deriving a complete source-backed documentation hierarchy from an existing codebase, including exhaustive module coverage, subsystem designs, architecture, functional behavior, and wiki navigation.
metadata:
  category: documentation-methodology
---

# Documentation Reverse Engineer

Use this skill to derive a complete documentation hierarchy from an existing codebase. Work from the smallest implementation responsibilities outward: project configuration, repository inventory, module designs, subsystem high-level designs, architecture, functional specifications, README, and wiki integration.

## Coverage Contract

Whole-repository reverse engineering is exhaustive. Do not replace full coverage with a representative, balanced, minimal, or sampled set unless the user explicitly narrows the repository boundary.

Inventory every tracked path at the frozen baseline plus every meaningful untracked source or configuration path. Assign each path exactly one classification and one owning module or responsibility:

- IN_SCOPE
- GENERATED
- VENDORED
- FIXTURE_ONLY
- SETUP_ARTIFACT
- USER_EXCLUDED

Every classification other than IN_SCOPE needs a concrete generator, owner, fixture purpose, setup contract, or explicit user boundary. Generated or vendored status does not permit an unexplained gap. The path ledger and coverage manifest must reconcile mechanically in both directions.

Higher-level synthesis never substitutes for missing lower-level coverage. A complete run has reviewed artifacts at every level and navigation that exposes them.

## Pass -1: Project Configuration

Before documentation work:

1. Inspect the repository, current Git state, build manifests, existing guidance, documentation, and source/test roots.
2. Create or refresh the single project-root PROJECT.yaml with create-project-configuration.
3. Detect pertinent technology and domain skills once during setup with detect-technology-skills.
4. Record folder routing, unavailable required skills, explicit no-variant scopes, fallback behavior, root and nested AGENTS.md decisions, and validation evidence.
5. Generate or update root and required nested guidance from the accepted project configuration.
6. Independently review configuration and guidance before source-derived writing begins.

Ordinary writers and reviewers consume the accepted routing. They do not rerun technology detection.

### Pass -1 Gate

- Exactly one operational PROJECT.yaml exists at the project root.
- Root and required nested guidance agree with its routes.
- Every detected required skill is available or the run is BLOCKED.
- Explicit no-variant areas remain in scope and use the documented fallback.
- Configuration and guidance pass independent review.

## Source Authority

Use this precedence when facts conflict:

1. executable source, migrations, schemas, and build configuration;
2. tests and retained runtime evidence;
3. generated metadata and public interface definitions;
4. accepted lower-level design artifacts;
5. existing summaries, README prose, and wiki pages.

Treat tests as evidence of intended or exercised behavior, not automatic proof that a current run passed. Preserve explicit uncertainty when the available evidence cannot establish runtime behavior.

## Pass 0: Repository Orientation

1. Freeze the source baseline commit and exact path inventory.
2. Identify source, test, resource, migration, UI, build, CI, deployment, operational, and documentation roots.
3. Record languages, frameworks, persistence, security, external interfaces, generators, wrappers, and supported commands from source evidence.
4. Partition the repository into meaningful runtime or operational responsibilities.
5. Create a coverage manifest row for every responsibility, naming source authority, entrypoints and contracts, related tests, planned module document, and owned-path count.
6. Create the exact path ledger and assign every baseline path one classification, owner, and manifest row.
7. Record explicit user exclusions and unresolved ownership as blockers rather than silently deferring them.

## Code Discovery Tools

Use rg or rg --files for discovery. Use a routed structure-aware search tool when discovery depends on syntax, nesting, imports, exports, callers, route declarations, component shapes, async flow, error handling, or test structure. Confirm an optional search tool is available before using it. If it is unavailable, continue with text search, repository file walking, and direct source reading. Do not treat structural matches as documentation evidence until the matched code has been read.

### Pass 0 Gate

- The ledger path set exactly equals the frozen baseline inventory.
- No path is missing, duplicated, blank, or owned by more than one responsibility.
- Every IN_SCOPE path maps to a manifest row and planned module design.
- Every non-IN_SCOPE path has an evidence-backed classification.
- The manifest covers source, tests, data, security, configuration, build, CI, operations, deployment, assets, and documentation where present.

## Pass 1: Module Designs

Create one module design for every manifest responsibility with create-module-design. A module can be a package, service, API, schema responsibility, UI feature, shared utility, test harness, build toolchain, deployment surface, or other cohesive unit; it need not correspond to one source directory.

Each module design must explain:

- responsibility, scope, and non-goals;
- source authority and owned paths;
- callers, dependencies, interfaces, and contracts;
- data, state, invariants, and lifecycle;
- security, authorization, validation, and failure behavior;
- configuration and operational effects;
- implementation-relevant control or data flow;
- related tests and verification gaps; and
- open questions that source evidence cannot resolve.

Use the folder technology skills selected by PROJECT.yaml while reading each source area. Do not skip an area merely because no specialized technology skill exists.

Have a fresh reviewer use review-module-design for every module artifact. Correct findings and repeat review until the artifact passes or is explicitly blocked.

### Pass 1 Gate

- Every manifest row has exactly one accepted module design.
- Every module design owns at least one ledger path or a justified cross-cutting responsibility.
- Every accepted module design has a completed independent review.
- Ledger counts still reconcile after any module-boundary correction.

## Pass 2: High-Level Designs

Group accepted module designs into coherent subsystems, feature families, platform slices, or operational groupings. Every accepted module belongs to at least one explicit HLD boundary, and overlapping ownership must be explained.

Create each HLD with create-high-level-design. Derive it from accepted module evidence and source only where a cross-module relationship needs confirmation. Explain:

- subsystem scope, non-goals, and parent relationship;
- exact constituent modules and responsibility boundaries;
- interactions, sequencing, data flow, state ownership, and invariants;
- security and trust boundaries;
- configuration and operational ownership;
- error propagation and split outcomes;
- implementation or change ordering; and
- cross-module verification.

Have a fresh reviewer use review-high-level-design for every HLD.

### Pass 2 Gate

- Every accepted module appears in an accepted HLD or has a documented cross-cutting placement.
- Constituent lists reconcile with the module manifest.
- Cross-module interactions are supported by lower-level or direct source evidence.
- Every HLD has an independent passing review.

## Pass 3: Architecture

Create the project-wide architecture with create-architecture from accepted HLDs and confirmed cross-cutting source evidence. Describe system boundaries, tiers, deployment topology, trust and identity, persistence, external interfaces, shared runtime rules, observability, privacy, constraints, and major decisions.

The architecture must preserve important disagreements or gaps found below it. It must not erase module or HLD defects through generalization.

Have a fresh reviewer use review-architecture.

### Pass 3 Gate

- Every HLD is placed in the architecture.
- Cross-cutting security, data, configuration, operations, deployment, and verification constraints reconcile with lower levels.
- The architecture has an independent passing review.

## Pass 4: Functional Specifications

Identify every observable actor and operator workflow supported by source, routes, tests, jobs, scripts, or deployment interfaces. Create functional specifications with create-functional-spec for complete workflow families rather than mirroring implementation files.

Cover applicable:

- actors, permissions, entry conditions, and triggers;
- happy paths, alternate paths, failure and recovery states;
- routes, inputs, outputs, status, visible state, and persistence effects;
- security and privacy behavior;
- asynchronous, operational, and deployment outcomes;
- acceptance criteria and verification evidence; and
- known defects or unproven behavior.

Have a fresh reviewer use review-functional-spec for every specification.

### Pass 4 Gate

- Observable routes, workflows, jobs, operational actions, and deployment behaviors map to accepted functional specifications.
- Functional claims reconcile with accepted design artifacts and source authority.
- Every functional specification has an independent passing review.

## Pass 5: README And Wiki Integration

After the lower levels pass:

1. Update the project README with concise project shape, supported setup, build, test, run, and documentation entry links.
2. Create or update docs/wiki with project-wiki skills.
3. Link architecture, HLDs, modules, functional specifications, coverage manifests, source, tests, known defects, decisions, glossary, and open questions from the appropriate wiki pages.
4. Keep experimental or unaccepted artifacts outside accepted documentation trees.
5. Run wiki status, lint, link, topic, and OKF checks required by the project-wiki contract.
6. Use documentation-page-verify for custom entry documents and the applicable project-wiki reviewers for wiki content.

### Pass 5 Completion Gate

- Passes -1 through 4 are complete.
- README and wiki navigation expose the complete accepted hierarchy.
- No accepted artifact is orphaned.
- Wiki and entry-document verification passes.
- The path ledger, module manifest, HLD membership, architecture placement, and functional coverage still reconcile.

Pass 5 completes whole-repository reverse engineering. Any later experiment that generates code or documents from the accepted hierarchy is a separate project-owned evaluation and must not weaken or redefine this completion gate.

## Parallelization

Parallelize independent module or HLD groups after Pass 0 freezes ownership. Give each writer an explicit scope, accepted inputs, output path, and applicable technology routing. Prevent overlap with repository claims when writers mutate files.

Do not parallelize across an unmet dependency gate. Module review precedes HLD synthesis; HLD review precedes architecture; accepted implementation and design evidence precede functional synthesis; accepted lower levels precede wiki integration.

## Verification

Before reporting completion:

1. Mechanically reconcile the frozen path inventory and ledger.
2. Reconcile manifest rows with accepted module designs.
3. Reconcile module membership with accepted HLDs.
4. Reconcile HLD placement with architecture.
5. Reconcile observable workflow inventory with functional specifications.
6. Confirm every required artifact-specific independent review passes.
7. Run project wiki verification and custom-page verification.
8. Run repository-required lint, schema, link, and generated-document checks.
9. Search for unresolved TODOs, placeholder prose, broken links, and claims unsupported by the named source.

Report READY only when every pass gate succeeds. Otherwise report the exact incomplete coverage, failed review, missing skill, or verification blocker without presenting a higher-level summary as a substitute.
