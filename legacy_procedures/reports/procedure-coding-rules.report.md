# Procedure Analysis: Coding Rules

## Source

- Procedure: [procedure-coding-rules.md](../procedure-coding-rules.md)
- Scope reviewed: sections 0 through 8, against the live distributed skills and development-use roles.

## Durable Guidance

The procedure contains a useful portable core: make narrow changes, keep contracts explicit, preserve type safety, test behavior, and seek design clarification before a material unapproved redesign. That core should remain concise and must not carry the procedure's former project topology or named registries into every consumer project.

The bundle should continue to route project-specific standards through AGENTS.md and, when a setup decision needs a reviewable record, PROJECT.yaml. A generic skill cannot truthfully require a particular header, design directory, definition registry, tracer, source tree, test tree, import alias, line count, or test runner.

## Mapping

| Procedure point | Destination | Coverage | Recommendation |
| --- | --- | --- | --- |
| Consult the relevant design before changing behavior; pause for approval before a major redesign | careful-coding; Coding Agent | Partial | Add one project-guidance discovery rule to careful-coding. Keep approval thresholds in the target project's AGENTS.md. |
| Verify changes and complete a review after tests pass | careful-coding; Jest; Vitest; QA And Verification Agent; Code Review Agent | Covered | Retain the current focused-then-broader verification and independent read-only review model. Do not create a global mandatory checklist. |
| Clear naming, small cohesive methods, minimal necessary change, avoid premature abstraction | careful-coding; Coding Agent | Covered | No addition. The current principles intentionally avoid prescriptive casing and line limits. |
| Prefer named domain types; distinguish optional, null, and missing; avoid any and broad casts | typescript-strict | Covered | No addition. The current skill is more portable and semantically precise than the legacy interface-versus-type placement rules. |
| Use a parameter object for a long positional argument list | typescript-strict | Missing, minor | Add a conditional guideline: prefer a named options or parameter object when a public signature has several related optional or same-typed positional parameters and it improves call-site clarity. Do not impose a two-parameter threshold. |
| Use explicit imports and exports; account for module-boundary behavior | typescript-esm | Covered | No addition. Alias policy, index-barrel policy, and file extensions must remain project-specific. |
| Test observable behavior, isolate external boundaries, use focused tests first, and preserve regression coverage | Jest; Vitest; Coding Agent; QA And Verification Agent | Covered | No addition. Keep framework selection and test placement in project guidance. |
| Avoid swallowed errors; provide contextual diagnostics; do not use exceptions as routine branching | careful-coding; stack- or runtime-specific skills | Missing, targeted | Add a short error-handling rule to careful-coding: preserve and surface actionable failures at real boundaries; do not silently swallow errors; follow the project's logging, error-shape, and recovery conventions. |
| Explain why in comments, keep comments accurate, remove commented-out code | careful-coding | Missing, minor | Add a concise documentation hygiene rule: write comments for non-obvious rationale or constraints, update them with the code, and do not leave obsolete commented-out code. |
| Replace unwieldy condition chains with an appropriate data-driven or polymorphic design | careful-coding | Partial | Add a preference, not a ban: when branching encodes stable variants and keeps growing, consider a discriminated union, dispatch map, or dedicated strategy after confirming that it simplifies the code. |
| Standard headers, AI-credit text, copyright/license metadata, JSON underscore metadata | Target project AGENTS.md or local repository procedure | Not portable | Omit from distributed skills. Apply only where a project's legal, generated-file, or tooling contract requires it. |
| Design comment links, design/modules location, definitions.md registry, canonical Design Code Path | Target project AGENTS.md, PROJECT.yaml, project wiki/design documents | Not portable | Omit from distributed skills. Existing methodology artifacts support source links without prescribing this legacy schema. |
| src/interfaces, src/types, src/constants, test mirroring, integration-test-plan location, index.ts-only barrels, fixed line limits | Target project AGENTS.md and architecture/module design | Not portable | Omit from distributed skills. These are repository topology decisions and vary by framework and codebase. |
| Tracer API, formatting of trace messages, named error strategy document | Target project AGENTS.md plus runtime-specific skill when applicable | Not portable | Omit from distributed skills. Preserve only as local operational guidance. |
| Require JSDoc on every export and remove every TODO attribution | Target project AGENTS.md | Not portable | Omit from distributed skills. These are team style choices with legitimate exceptions. |

## Precise Additions

Make the following small additions to careful-coding only; they preserve portability and fit its role as the shared implementation guardrail.

1. Under Think Before Coding, add: Before changing behavior, locate and follow the project-owned source of intent, such as AGENTS.md, a design document, acceptance criteria, or a tracked issue. If the evidence conflicts or a material redesign is required, surface the conflict before proceeding.
2. Under Surgical Changes, add: Preserve actionable error information at real boundaries. Do not silently swallow failures; use the project's established error, logging, and recovery conventions.
3. Under Simplicity First, add: When a public signature accumulates several related optional or same-typed positional parameters, prefer a named options or parameter object if it makes calls and evolution clearer.
4. Under Surgical Changes, add: Keep comments limited to non-obvious rationale, constraints, and workarounds. Update or remove comments and commented-out code that no longer describe the implementation.
5. Under Simplicity First, add: If a growing conditional represents stable variants, consider a discriminated union, dispatch map, or dedicated strategy only when it reduces total complexity.

No changes are recommended to typescript-strict, typescript-esm, Jest, Vitest, roles, or generated adapters. The Coding Agent and Code Review Agent already compose careful-coding with focused verification and read-only evidence-based review.

## Omit List

- Personal copyright, email address, AI-credit, license phrase, witty remark, and file-path header requirements.
- Every-file JSDoc mandate and blanket prohibition on TODO or attribution comments.
- Fixed source/test/design folder layout, 200/300/40-line limits, naming/casing matrix, and barrel-only index.ts requirement.
- definitions.md, Design Code Path, design/modules, design/error-strategy.md, Tracer, project aliases, and legacy tool commands.
- Mandatory test-directory mirroring, integration-test-plan location, and one prescribed incremental test-splitting workflow.
- Absolute prohibitions on switch or if chains, static helper placement, interface placement, and interface-versus-type choice beyond the existing semantic TypeScript guidance.

## Conclusion

Do not revive Coding Rules as a distributed skill and do not add a specialized agent. The portable value is a small set of implementation guardrails, best placed in careful-coding. The remaining rules describe one former TypeScript project's legal metadata, information architecture, observability API, and style decisions; they belong in that project's AGENTS.md and design material, not in a reusable bundle.
