# Dev Methodology Repository Instructions

## Purpose

This file is the repo-local operating contract for maintaining this repository.

Do not move these directives into a distributed skill unless the rule is reusable outside this repository. The distributed skills under skills are the product this repository ships. This AGENTS.md file describes how to maintain that product.

Keep these instructions simple. If a maintenance rule needs a long explanation, prefer a root procedure file whose name starts with procedure- and link it from here.

## Codex Multi-Item Coordination

When the user explicitly asks one parent task to coordinate multiple user-visible Codex backlog tasks, use the [codex-workitem-coordination skill](skills/codex-workitem-coordination/SKILL.md) through Dev Backlog Coordinator. Keep backlog mutations with Dev Backlog Steward and per-item artifact delivery with Dev Orchestrator. The [orchestrated development lifecycle](design/orchestrated-development-lifecycle.html) owns the communication sequences; do not copy that procedure into repository-local guidance.

## Source Boundaries

- README.md is the human-facing entry point for the bundle.
- AGENTS.md is the agent-facing maintenance contract for this repository.
- skills contains portable Agent Skills distributed to other projects and machines.
- agents contains the customer-independent conceptual agent definition schema and source definitions.
- detection.yaml beside a specialized technology or domain skill is the source for setup-time detection metadata and activation evidence.
- adapters contains runtime-specific metadata for those distributed skills.
- generated/adapters contains generated native agent definitions and must be regenerated from conceptual agent definition sources rather than edited manually.
- backlog contains this repository's primary-worktree-only typed work queue and user-action-required state; isolated agent worktrees omit it.
- .worktrees contains ignored linked agent checkouts rooted at the primary worktree. It is operational state rather than project source, and agents must never resolve it from another linked worktree.
- design contains the HTML explanations of the skill and agent model.
- scripts contains installer, refresh, validation, and regression-test support.

Do not create separate skill files for repo-local maintenance procedures. Keep repo-local procedures in AGENTS.md or in root procedure files.

## Before Editing

- Inspect the live repository state before changing files.
- Read README.md when changing bundle structure, install behavior, skill inventory, adapter behavior, or verification workflow.
- Read the relevant skill files before changing distributed skill content.
- Preserve unrelated local changes and untracked files.
- Keep changes scoped to the requested maintenance work.

## Work-Item Workflow Skill References

Project Configurator owns the independent Persistence and Commit selectors. Persistence routes durable work-item storage; Commit routes delivery. Workflow skills are referenced by name only and technology skill routing remains separate.

- Default persistence file: create with create-file-work-item; manage with manage-file-work-items.
- Default commit direct-main: use complete-work-item-direct-main.

Most-specific matching folder pattern wins independently for Persistence and Commit overrides. A folder override changes only its own selector.

When a selector is UNSET, the pertinent agent asks at the stated operation boundary and does not infer either value from repository or hosting evidence, files, remotes, templates, plugins, or available tools.

## Resource Coordination Skill Reference

Project Configurator selected resource-coordination skill agent-claim. Apply that bundled skill by reference before taking ownership of repository paths or exclusive runtime and integration resources.

The selected skill owns its coordination procedure and evidence. Work-item providers own durable assignment and lifecycle records; they do not own operational resources.

Configured resource deadline policy:

- backlog-mutation: maximum 600 seconds; cleanup grace 120 seconds
- main-integration: maximum 2700 seconds; cleanup grace 600 seconds
- browser-server: maximum 3600 seconds; cleanup grace 600 seconds
- database-port: maximum 1800 seconds; cleanup grace 300 seconds
- live-model-evaluation: maximum 14400 seconds; cleanup grace 1800 seconds

Exact resource-id overrides:

- None.

## Agent Claim Helper

Project Configurator selected and verified the command claim-helper interface. Apply the shared agent-claim semantics and the inlined agent-claim-command adapter for every claim operation.

Invoke this configured adapter directly. Runtime work does not probe or switch claim-helper interfaces. If it is unavailable, report the compatibility outcome CLAIM_TRANSPORT_UNAVAILABLE and request Project Configurator reconfiguration.

----- BEGIN INLINED CLAIM HELPER INTERFACE SKILL: agent-claim-command -----
# Agent Claim Command

Apply this adapter only when Project Configurator selected command in the compatibility field agent_claim_transport and verified this package, Python, and its executable script. That field selects how the claim helper is invoked. Apply agent-claim for scope, ownership, state, recovery, heartbeat, release, and completion semantics.

The command-line implementation flow is Python claim command -> claim helper -> claim registry and journal. The command parser and helper functions are implemented together in scripts/claim.py inside this adapter; the helper writes repository-global registry and journal state under the Git common directory.

## Availability Boundary

Resolve the adapter-bundled script once before the first operation and reuse that exact path for the task. Do not search for MCP tools or change the configured claim-helper interface. Do not assume the target repository contains the adapter package.

Use an explicit path supplied by configured project guidance when present. Otherwise use the scripts/claim.py file beside this loaded SKILL.md. Inside the dev-methodology source checkout, the bundle-owned path is:

```bash
CLAIM_SCRIPT=skills/agent-claim-command/scripts/claim.py
```

For a normal Codex user-level installation, the default is:

```bash
CLAIM_SCRIPT="${HOME}/.agents/skills/agent-claim-command/scripts/claim.py"
```

If the configured script or Python interpreter is absent, unreadable, or cannot start before dispatch, stop with CLAIM_TRANSPORT_UNAVAILABLE and request Project Configurator reconfiguration. Do not switch claim-helper interfaces. An argument, path, root, authorization, input-policy, or other structured rejection returned by the command is not unavailability.

## Command Contract

Invoke the script with Python and one operation:

```bash
python3 "$CLAIM_SCRIPT" --repo /absolute/path/to/project OPERATION [ARGUMENTS]
```

Supported operations are status, acquire, extend, extend-deadline, heartbeat, release, maintain-journal, and report. Each completed invocation writes one JSON document to standard output. Decode it and inspect result.outcome. The top-level exit_code and process exit code are stable automation aids; the structured outcome is authoritative.

Stable process exit codes are:

- 0 for successful execution, including acquired ownership and read-only operations.
- 1 for a structured rejection such as INVALID_SCOPE, INVALID_IDENTIFIER, INVALID_WORKTREE_PATH, WORKTREE_ROOT_NOT_IGNORED, CLAIM_NOT_FOUND, or RELEASE_REJECTED.
- 3 for CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED, SHARED_CHECKOUT_REQUIRED, or SHARED_CHECKOUT_RELEASE_REQUIRED.
- 4 for ISOLATED_CHECKOUT_SETUP_REQUIRED.
- 5 for DIRTY_CHECKOUT_RECOVERY_AUTHORIZATION_REQUIRED.
- 2 for command-line parsing failure before coordination dispatch.

Several outcomes share one exit code. Never branch on the process code alone. A completed structured rejection is a valid coordination result; do not switch claim-helper interfaces or retry it through MCP.

RECONCILIATION_RECOVERY_REQUIRED means a durable pending reconciliation marker still controls transaction recovery. A prepared marker protects the exact original registry and journal snapshots; its RELEASE_PENDING line is not a release. A committed marker makes the exact released registry authoritative and finalizes exactly one RELEASED journal event. Scoped commands and journal maintenance attempt validated deterministic recovery under the registry lock. Report remains read-only and returns this outcome before journal loading when a marker exists.

Release reconciliation requires the claim baseline to precede the exact peer commit and the peer commit to be an ancestor of current HEAD. That peer commit must change exactly the rejected out-of-domain path set, exclude the claimed domain, and match the acquisition-time content for every reconciled path. Later descendant commits may change those paths without invalidating the bounded peer snapshot. The cited rejection must resolve to the same acquisition identity and evidence.

When this outcome appears:

1. Invoke status through this same CLAIM_SCRIPT path.
2. If the outcome persists, preserve the marker, registry, journal, command result, and relevant filesystem evidence.
3. Escalate that evidence. Do not manually edit or remove the marker, registry, journal, or protected claim.

## Command Arguments

Acquire requires claim-id, agent, task, and root-task-id. Ordinary callers pass only the scope selected by Agent Claim's Event Contract: exact backlog files, project-files, or one named resource. The command retains tree, backlog, all-files, branch, base, worktree-path, and compat-file-directories inputs only for schema compatibility or explicitly authorized recovery. Tree, project-files, and all-files require scope-reason. A named resource also requires resource-class, resource-id, expected-duration-seconds, and requested-hard-stop-duration-seconds; the command resolves configured maximum and cleanup grace from PROJECT.yaml. Parent-claim-id and allow-recovery remain optional.

Extend requires claim-id plus net-new scope and uses the same complete timing arguments when adding the claim's one named resource. Extend-deadline requires claim-id, requested-hard-stop-duration-seconds, and extension-evidence. Heartbeat and release require claim-id. Release accepts no-change only for a truthful no-change result. The mutually exclusive reconciliation variant accepts reconcile-out-of-domain-commit with one full 40-character SHA and requires prior-rejected-release-reference for the matching rejected release event. Journal maintenance accepts hot-days, defaulting to 2. Reporting accepts since and format; use JSON output for automation.

## Exact Invocations

Read live ownership:

```bash
python3 "$CLAIM_SCRIPT" --repo . status
```

Update an existing work item:

```bash
python3 "$CLAIM_SCRIPT" --repo . acquire \
  --claim-id update-work-item-123 \
  --agent backlog-steward \
  --task update-work-item-123 \
  --root-task-id work-item-123 \
  --file backlog/feature-backlog/work-item-123.md
```

Perform non-backlog work in the primary worktree:

```bash
python3 "$CLAIM_SCRIPT" --repo . acquire \
  --claim-id task-123 \
  --agent implementation-agent \
  --task task-123 \
  --root-task-id task-123 \
  --project-files \
  --scope-reason "project implementation"
```

Acquire one deadline-bound resource. The project policy, not this command, supplies the configured maximum and cleanup grace:

```bash
python3 "$CLAIM_SCRIPT" --repo . acquire \
  --claim-id browser-check-123 \
  --agent browser-operator \
  --task browser-check-123 \
  --root-task-id task-123 \
  --resource browser-test:primary \
  --resource-class browser-server \
  --resource-id browser-test:primary \
  --expected-duration-seconds 900 \
  --requested-hard-stop-duration-seconds 1800
```

Extend with a newly triggered shared-port event, explicitly extend a resource deadline, heartbeat, and release:

```bash
python3 "$CLAIM_SCRIPT" --repo . extend \
  --claim-id task-123 \
  --resource port:3000 \
  --resource-class database-port \
  --resource-id port:3000 \
  --expected-duration-seconds 600 \
  --requested-hard-stop-duration-seconds 1200

python3 "$CLAIM_SCRIPT" --repo . extend-deadline \
  --claim-id browser-check-123 \
  --requested-hard-stop-duration-seconds 2400 \
  --extension-evidence "one final accessibility case remains"

python3 "$CLAIM_SCRIPT" --repo . heartbeat --claim-id task-123

python3 "$CLAIM_SCRIPT" --repo . release --claim-id task-123
```

Heartbeat is liveness only and never extends a deadline. Extend-deadline succeeds only when the evidence is non-empty, the requested duration increases, and it stays within the immutable configured maximum recorded at acquisition. Status reports overdue and cleanup-grace state without auto-release or delivery inference.

Declare a clean no-change result:

```bash
python3 "$CLAIM_SCRIPT" --repo . release \
  --claim-id task-123 \
  --no-change
```

Reconcile one retained primary scoped claim only after verifying the supplied peer commit and prior rejected release reference:

```bash
python3 "$CLAIM_SCRIPT" --repo . release \
  --claim-id task-123 \
  --reconcile-out-of-domain-commit 0123456789abcdef0123456789abcdef01234567 \
  --prior-rejected-release-reference 12345678-1234-1234-1234-123456789abc
```

Maintain the journal and report contention:

```bash
python3 "$CLAIM_SCRIPT" --repo . maintain-journal --hot-days 2
python3 "$CLAIM_SCRIPT" --repo . report --since 2d --format json
```

## Ambiguous Dispatch

When process control or output capture fails after submitting a mutating command, the dispatch is ambiguous. Do not repeat the mutation or change the claim-helper interface. Invoke status through the same CLAIM_SCRIPT path and reconcile the live registry before continuing.

If the same claim command-line interface cannot provide status, preserve the ambiguous state, report CLAIM_TRANSPORT_UNAVAILABLE, and request Project Configurator reconfiguration or an explicit ownership handoff. Never invoke the MCP adapter to guess whether the command mutation succeeded.

## Behavioral Equivalence

Both configured claim-helper interfaces expose the same helper outcomes and next-action semantics. Their invocation envelopes differ, but this adapter never renames, suppresses, retries, or translates a structured coordination outcome.
----- END INLINED CLAIM HELPER INTERFACE SKILL: agent-claim-command -----

## Skill Definition Approval

Get explicit, scope-specific user approval before changing a skill definition when:

- Testing reveals a defect in the skill and fixing the defect requires changing the skill.
- Changing the skill is necessary to complete other authorized work.

A direct user instruction to change a named skill is approval for that named scope. Do not infer approval from a failing test, a repair assignment, repository access, or general permission to complete related work.

Governed canonical definition surfaces:

- Conceptual agent definitions: agents/roles/**/*.role.yaml.
- Agent definition schemas and model inputs: agents/role-schema.yaml, agents/model-profiles.yaml, adapters/*/model-profiles.yaml.
- Distributed skill definitions: skills/*/SKILL.md.
- Adapter-owned skill definitions: adapters/*/skills/*/SKILL.md.
- Skill definition metadata: skills/*/agents/openai.yaml, adapters/*/skills/*/agents/openai.yaml.

Generated definition mirrors are source-owned and must never be edited directly:

- generated/adapters/**, design/generated/role-definitions.js, design/generated/skill-definitions.js.

Supported source-category to generated-mirror relationships:

- Conceptual agent definitions: generated/adapters/**, design/generated/role-definitions.js.
- Agent definition schemas and model inputs: generated/adapters/**, design/generated/role-definitions.js.
- Distributed skill definitions: generated/adapters/**, design/generated/skill-definitions.js.
- Adapter-owned skill definitions: generated/adapters/**, design/generated/skill-definitions.js.
- Skill definition metadata: generated/adapters/**, design/generated/skill-definitions.js.
- Regenerate a mirror only when it is listed for the approved canonical source category. Cross-family role-to-skill and skill-to-role documentation regeneration is blocked. A supported regeneration does not require a second approval.

When a test fails, investigate whether the test, fixture, assertion, or expected result is incorrect before proposing a definition change. Ordinary authorized implementation changes and corrections to incorrect tests remain allowed when they do not alter a governed definition.

## Technology Skills

Technology detection is owned by Project Configurator. Do not rerun detection during ordinary work.

Before acting on files under a matching folder, every agent must apply each inlined skill completely. These folder skills govern technology-specific implementation, review, diagnosis, verification, security, interface, prompt, and technical documentation work together with the agent's definition-owned skills.

Folder skillsets:

When configured folder patterns overlap, the most-specific matching pattern wins.

- scripts/**: apply the inlined python skill instructions before acting.
  - python evidence: Python source evidence: scripts/build-agent-skill-hierarchy.py and sibling .py files
- skills/project-wiki/scripts/**: apply the inlined python skill instructions before acting.
  - python evidence: Python package evidence: skills/project-wiki/scripts/project_wiki_ops/__init__.py and sibling .py files
- skills/detect-technology-skills/scripts/**: apply the inlined python skill instructions before acting.
  - python evidence: Python source evidence: skills/detect-technology-skills/scripts/detect.py
- evals/projects/python-inventory/**: apply the inlined python skill instructions before acting.
  - python evidence: Python source evidence: evals/projects/python-inventory/src/inventory.py; Owning manifest evidence: evals/projects/python-inventory/pyproject.toml requires Python 3.11 or newer
- evals/projects/fastapi-orders/**: apply the inlined fastapi, python skills instructions before acting.
  - fastapi evidence: Owning manifest dependency: evals/projects/fastapi-orders/pyproject.toml declares fastapi; Framework source evidence: evals/projects/fastapi-orders/app/main.py imports FastAPI and declares an application route
  - python evidence: Python source evidence: evals/projects/fastapi-orders/app/main.py

Inlined folder skill instructions:

### Folder pattern: scripts/**

Apply every inlined technology skill below when working under this folder pattern.

----- BEGIN INLINED TECHNOLOGY SKILL: python -----
# Python

Follow the owning project's Python version, packaging metadata, formatter, linter, type checker, and test runner.

## Implementation

- Keep public functions, classes, exceptions, and module boundaries explicit.
- Prefer standard library types and direct control flow over speculative abstractions.
- Use context managers for resources with deterministic cleanup.
- Preserve exception causes when translating errors at an owning boundary.
- Avoid mutable default arguments and implicit shared state.
- Keep asynchronous and synchronous call paths distinct.
- When a Gang of Four pattern is explicit, combine its generic pattern skill with Python Design Pattern Examples and prefer native functions, protocols, dataclasses, modules, and generators where they preserve the intent.

## Verification

- Add focused tests for changed behavior and failure boundaries.
- Run the narrow project-native test command first, then applicable lint, formatting, and type checks.
- Verify supported Python versions when syntax or library behavior is version-sensitive.
----- END INLINED TECHNOLOGY SKILL: python -----

### Folder pattern: skills/project-wiki/scripts/**

Apply every inlined technology skill below when working under this folder pattern.

----- BEGIN INLINED TECHNOLOGY SKILL: python -----
# Python

Follow the owning project's Python version, packaging metadata, formatter, linter, type checker, and test runner.

## Implementation

- Keep public functions, classes, exceptions, and module boundaries explicit.
- Prefer standard library types and direct control flow over speculative abstractions.
- Use context managers for resources with deterministic cleanup.
- Preserve exception causes when translating errors at an owning boundary.
- Avoid mutable default arguments and implicit shared state.
- Keep asynchronous and synchronous call paths distinct.
- When a Gang of Four pattern is explicit, combine its generic pattern skill with Python Design Pattern Examples and prefer native functions, protocols, dataclasses, modules, and generators where they preserve the intent.

## Verification

- Add focused tests for changed behavior and failure boundaries.
- Run the narrow project-native test command first, then applicable lint, formatting, and type checks.
- Verify supported Python versions when syntax or library behavior is version-sensitive.
----- END INLINED TECHNOLOGY SKILL: python -----

### Folder pattern: skills/detect-technology-skills/scripts/**

Apply every inlined technology skill below when working under this folder pattern.

----- BEGIN INLINED TECHNOLOGY SKILL: python -----
# Python

Follow the owning project's Python version, packaging metadata, formatter, linter, type checker, and test runner.

## Implementation

- Keep public functions, classes, exceptions, and module boundaries explicit.
- Prefer standard library types and direct control flow over speculative abstractions.
- Use context managers for resources with deterministic cleanup.
- Preserve exception causes when translating errors at an owning boundary.
- Avoid mutable default arguments and implicit shared state.
- Keep asynchronous and synchronous call paths distinct.
- When a Gang of Four pattern is explicit, combine its generic pattern skill with Python Design Pattern Examples and prefer native functions, protocols, dataclasses, modules, and generators where they preserve the intent.

## Verification

- Add focused tests for changed behavior and failure boundaries.
- Run the narrow project-native test command first, then applicable lint, formatting, and type checks.
- Verify supported Python versions when syntax or library behavior is version-sensitive.
----- END INLINED TECHNOLOGY SKILL: python -----

### Folder pattern: evals/projects/python-inventory/**

Apply every inlined technology skill below when working under this folder pattern.

----- BEGIN INLINED TECHNOLOGY SKILL: python -----
# Python

Follow the owning project's Python version, packaging metadata, formatter, linter, type checker, and test runner.

## Implementation

- Keep public functions, classes, exceptions, and module boundaries explicit.
- Prefer standard library types and direct control flow over speculative abstractions.
- Use context managers for resources with deterministic cleanup.
- Preserve exception causes when translating errors at an owning boundary.
- Avoid mutable default arguments and implicit shared state.
- Keep asynchronous and synchronous call paths distinct.
- When a Gang of Four pattern is explicit, combine its generic pattern skill with Python Design Pattern Examples and prefer native functions, protocols, dataclasses, modules, and generators where they preserve the intent.

## Verification

- Add focused tests for changed behavior and failure boundaries.
- Run the narrow project-native test command first, then applicable lint, formatting, and type checks.
- Verify supported Python versions when syntax or library behavior is version-sensitive.
----- END INLINED TECHNOLOGY SKILL: python -----

### Folder pattern: evals/projects/fastapi-orders/**

Apply every inlined technology skill below when working under this folder pattern.

----- BEGIN INLINED TECHNOLOGY SKILL: fastapi -----
# FastAPI

Load Python with this skill.

## Application Boundaries

- Keep request and response models explicit and separate persistence or internal domain shapes when their contracts differ.
- Use dependency injection for request-scoped collaborators and cross-cutting policies.
- Translate domain failures to HTTP responses at the API boundary without losing useful causes in logs.
- Keep blocking work out of asynchronous request paths unless it is isolated behind an appropriate executor or synchronous endpoint.
- Put startup and shutdown ownership in lifespan handling.

## Routing And Validation

- Make status codes, response models, validation constraints, authentication requirements, and error bodies observable in the route contract.
- Avoid hidden side effects in dependencies and validators.
- Preserve framework-generated validation behavior unless the API contract intentionally replaces it.

## Verification

- Test routes through the ASGI application boundary with dependency overrides scoped to the test.
- Cover successful responses, invalid input, authorization failure, and translated domain failures.
- Verify asynchronous tests and lifespan behavior with the project's chosen test client and event-loop tooling.
----- END INLINED TECHNOLOGY SKILL: fastapi -----

----- BEGIN INLINED TECHNOLOGY SKILL: python -----
# Python

Follow the owning project's Python version, packaging metadata, formatter, linter, type checker, and test runner.

## Implementation

- Keep public functions, classes, exceptions, and module boundaries explicit.
- Prefer standard library types and direct control flow over speculative abstractions.
- Use context managers for resources with deterministic cleanup.
- Preserve exception causes when translating errors at an owning boundary.
- Avoid mutable default arguments and implicit shared state.
- Keep asynchronous and synchronous call paths distinct.
- When a Gang of Four pattern is explicit, combine its generic pattern skill with Python Design Pattern Examples and prefer native functions, protocols, dataclasses, modules, and generators where they preserve the intent.

## Verification

- Add focused tests for changed behavior and failure boundaries.
- Run the narrow project-native test command first, then applicable lint, formatting, and type checks.
- Verify supported Python versions when syntax or library behavior is version-sensitive.
----- END INLINED TECHNOLOGY SKILL: python -----
## Skill Catalog Maintenance

When adding, renaming, deleting, or materially changing a distributed skill:

- Update the source skill under skills.
- Keep the skill frontmatter name aligned with the skill directory name.
- Keep Codex openai.yaml metadata beside each source SKILL.md when a skill needs Codex app metadata, invocation policy, or tool dependencies.
- Run scripts/openai_metadata.py skills after skill name or description changes so derived Codex interface fields stay aligned while policy and dependencies remain hand-authored.
- Run scripts/build-technology-detection.py after detection metadata or specialized activation criteria change.
- Update README.md when the public skill inventory, setup flow, verification flow, or bundle purpose changes.
- Update the design HTML files that describe skills, conceptual agent definitions, agent maps, skills modularization, agentic configuration, or examples whenever the catalog, conceptual definition model, adapter model, or examples change.
- Update scripts/test_bundle_content.py so the bundle regression tests describe the current catalog.
- Sweep the repository for old skill ids before and after renames or deletions.
- Keep review skill checklists named review-checklist-[review-target].md, and keep completed checklist guidance aligned with artifact-name.review-checklist-[review-target].md.

When adding, renaming, deleting, or materially changing a conceptual agent definition:

- Update the conceptual source under agents/roles.
- Keep its filename field aligned with the conceptual definition source filename.
- Use only bundled skill IDs in the skills list.
- Run scripts/build-skill-docs.py so conceptual agent definition documentation data and native adapters are regenerated together.
- Update README.md and the relevant design HTML when conceptual definition policy, runtime support, installation, or customization behavior changes.
- Never edit design/generated or generated/adapters by hand.

## README And Design HTML

README.md must stay aligned with the distributable bundle:

- Repository shape.
- Install and refresh commands.
- Ownership and prune behavior.
- Bundled skill inventory.
- Applying the bundle to target projects.
- Verification commands.

The design HTML files must stay aligned with the current skills and agent model:

- design/agent-and-skill-definitions.html
- design/agentic-configuration.html
- design/skills-modularization.html
- design/generic-agent-definitions-source.html
- design/agent-skill-specialization-examples.html
- design/orchestrated-development-lifecycle.html
- design/documentation-templates.html

If a change affects the skill catalog, adapter shape, conceptual agent definition naming, dispatch profile examples, or agent specialization story, update the relevant HTML files in the same change.

## Markdown Rules

- Do not use inline Markdown code formatting in Markdown files.
- Use fenced code blocks only when command blocks or multi-line snippets are needed.
- Write steady-state documentation. Do not describe content as enhanced, revised, new, or old unless the document is explicitly a change plan.
- Keep examples generic and portable unless the document is intentionally repo-specific.

## Validation

Select tests from the changed behavior and its actual dependency paths. Run the smallest relevant test first. A tier identifies the affected surface; it never triggers a full repository regression.

| Tier | Change event | Required tests | Explicit exclusions |
| --- | --- | --- | --- |
| 1 | Documentation-only change with no executable contract change | Documentation validation for the changed files; applicable link or markup checks; git diff --check | No unit suites, agent catalog, browser tests, or unrelated documentation checks |
| 2 | Skill, role, configuration, template, or metadata contract change | Targeted contract tests that directly assert the changed statements; validation for each changed source; generated-output freshness for affected outputs; git diff --check | No full repository suite, project-wiki suite, browser tests, or live-model tests |
| 3 | Generated output changes from an approved source change | The source's targeted tests; regenerate only supported outputs; freshness check for that generator; exact source-to-output consistency check; git diff --check | No unrelated generators or broad regression suites |
| 4 | Test fixture, expected result, assertion, or test data change | Tests that consume the changed fixture, result, assertion, or data; one focused negative case when needed to prove that the test detects the intended defect; git diff --check | No unrelated module tests; no production or canonical contract changes merely to satisfy the test |
| 5 | Helper, parser, simulator, runner, installer, or generator implementation change | Targeted unit tests for the changed functions and failure boundaries; a targeted integration test only when the changed function crosses a real component boundary; git diff --check | No full repository suite solely because the file is shared |
| 6 | Product or methodology implementation change | Unit tests for changed behavior; directly affected component tests; a focused regression for the reported defect; git diff --check | No tests for components that do not call, consume, or depend on the changed behavior |
| 7 | Primary-main integration of an already reviewed candidate | Re-run the smallest tests that prove the integrated bytes and affected behavior; verify candidate-to-main content mapping; git diff --check | Do not repeat unchanged pre-integration tests without evidence of integration-sensitive behavior |
| 8 | User-level installation or publication | Targeted installer or publication tests; verify installed bytes or digests against the accepted source; refresh and inspect affected catalog entries | No full repository suite or complete catalog evaluation |
| 9 | Focused testing reveals a distinct cross-component failure | Add only the newly implicated component's targeted tests after recording the concrete failure and dependency path | Do not escalate based only on file size, file location, a shared classification, or hypothetical risk |
| 10 | User explicitly requests broader verification | Run exactly the broader scope requested by the user and state its expected cost before starting | Do not infer permission for additional suites beyond the requested scope |

When a targeted test fails, determine whether the implementation or the test is wrong. If the fixture, assertion, expected result, test data, or other test-support code is incorrect, fix that test-related file within the current change and rerun only the tests that consume it. Do not change correct production behavior or a canonical contract merely to make an incorrect test pass.

Run broader tests only when the user explicitly requests them or a focused failure identifies a concrete affected dependency. A failing focused test may justify additional targeted tests; it does not authorize an automatic full-suite escalation.

Log a distinct defect when testing exposes an unrelated problem. Do not fix that unrelated problem under the current scope and do not keep the current item open solely because of it.

If a build script is introduced later, run the repository build after code, imports, generated artifacts, or project metadata changes.

## Commit Expectations

- Commit coherent verified repository-maintenance work before completion.
- Do not include unrelated untracked files in the commit.
- Include README.md, AGENTS.md, design HTML, tests, Codex metadata, and explicit deployment behavior in the same change when they are part of the same catalog or workflow update.
