# Establish The STE Technical Documentation Standard

Status: Ready

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/establish-ste-technical-documentation-standard.md

Completion: direct-main

## Summary

Create a portable Simplified Technical English (STE) skill for all technical documentation. Integrate the skill with documentation writing, technical reasoning, communication, review, verification, generated adapters, and public methodology documentation.

## Context

The repository has no distributed STE skill. The current STE rules exist only in the ignored project-local agent at `.codex/agents/ste_writer.toml`. That agent uses `gpt-5.3-codex-spark` and applies a best-effort subset of ASD-STE100 principles.

The conceptual Dev Documentation Writer does not load STE guidance. It uses artifact-specific creation skills to control document structure. The Dev Artifact Reviewer and `documentation-page-verify` do not verify STE usage.

The role schema supplies `effective-communication` to every conceptual agent. That skill currently has no boundary between user or agent messages and durable artifact bodies. The `structured-explanation` skill controls the `QUERY`, `SUB-QUERY`, `FACT`, `HYPOTHESIS`, `UNKNOWN`, and `ANSWER` format. It does not state how STE applies to the prose inside those items.

Tests with the project setup paragraph showed that STE alone preserved descriptive documentation better than STE combined without a boundary with `effective-communication`. The combined prompt incorrectly changed descriptive information into an ordered procedure. The implementation must prevent this semantic change.

Repository STE principles can be mandatory without claiming certified ASD-STE100 compliance. Formal compliance requires the applicable ASD-STE100 issue and controlled dictionary.

## Source Evidence

On 2026-07-27, the user directed: “All technical documentation should comply with STE principles.”

On 2026-07-27, the user then directed: “Create a workitem for all this. In the workitem list the STE principles we want to use during the execution of the work item, as well as in creating the STE skill. include the other changes.”

The current local baseline is `.codex/agents/ste_writer.toml`. The current portable contracts are `skills/effective-communication/SKILL.md`, `skills/structured-explanation/SKILL.md`, `agents/roles/dev-activities/dev-documentation-writer.role.yaml`, `agents/roles/dev-activities/dev-artifact-reviewer.role.yaml`, and `skills/documentation-page-verify/SKILL.md`.

This request authorizes creation of this Ready work item. It does not by itself authorize mutation of an agent or skill definition. Obtain exact, scope-specific approval before each governed definition change.

## STE Principles For This Work Item

Apply these principles to technical prose that is written during execution, including plans, design notes, explanations, documentation, review findings, verification results, and handoffs:

- Preserve the source meaning.
- Preserve each requirement, condition, permission, prohibition, and configuration distinction.
- Preserve exact identifiers, commands, paths, configuration values, code, schema names, fixed labels, and quoted source text.
- Use the same term for the same item or action.
- Use one meaning for each word in a given context.
- Use an approved dictionary term when the applicable ASD-STE100 dictionary is available.
- When the dictionary is not available, use a common and precise word. Do not claim verified dictionary compliance.
- Define a necessary project-specific or technical term at its first use when the context does not define it.
- Prefer active voice when the responsible actor is known.
- Use the imperative form only for an instruction.
- Keep a description descriptive. Do not convert it into a command or procedure.
- Preserve normative force. Do not change `must`, `must not`, `may`, or equivalent requirements without source support.
- Put one action in each procedural step.
- Put one main idea in each sentence.
- Keep an instructional sentence at 20 words or fewer when exact technical content permits it.
- Keep a descriptive sentence at 25 words or fewer when exact technical content permits it.
- Split a sentence instead of deleting or changing technical content to meet a length target.
- Put a condition before the action or result that depends on it.
- Use a numbered list only for an ordered sequence.
- Use a bulleted list for unordered information.
- Keep noun groups short.
- Avoid ambiguous pronouns, hidden references, idioms, wordplay, unnecessary modifiers, and unexplained jargon.
- State the actor, action, object, condition, and result when the reader needs them.
- Use positive instructions when they preserve the required meaning. Use a prohibition when it expresses a real constraint.
- Keep paragraphs short and group related information.
- Use tables only when they make repeated comparisons or mappings clearer.
- Apply STE to the prose in headings, list items, table cells, captions, and structured-explanation synopses.
- Do not rewrite code blocks, machine-readable data, syntax examples, fixed format labels, or verbatim quotations.
- Let the artifact-specific skill control document structure.
- Let `structured-explanation` control its reasoning item types and relationships.
- Let `effective-communication` control the surrounding outcome, evidence, blocker, decision, next action, and handoff.
- Prefer semantic accuracy over a mechanical sentence-length or vocabulary rule.

Use these same principles as the initial content contract for the new portable STE skill. Refine a principle only when source evidence shows that it conflicts with the applicable ASD-STE100 issue or with an established repository contract. Record the reason for each refinement.

## Requirements

### Portable STE Skill

- Create `skills/ste-technical-writing/SKILL.md`.
- Create `skills/ste-technical-writing/agents/openai.yaml`.
- Give the skill a narrow purpose: write, rewrite, and review technical-document prose with the STE principles in this item.
- Make the skill portable across supported harnesses.
- Keep the main workflow concise.
- Put optional issue-specific or dictionary-specific details in directly referenced resources only when they are available and legally distributable.
- State that the repository principles are mandatory for technical-document prose.
- State that verified ASD-STE100 compliance requires the applicable issue and controlled dictionary.
- Require preservation of exact technical content and normative meaning.
- State the boundary for code, commands, identifiers, schemas, fixed labels, and verbatim quotations.
- State that the artifact-specific method controls document structure.
- State that STE controls prose within a structured explanation but does not replace its item model.
- State that STE does not convert descriptions into instructions or unordered rules into procedures.
- Validate the complete skill package with the repository-supported skill validator.

### Documentation Writer

- Add `ste-technical-writing` as an unconditional skill of `agents/roles/dev-activities/dev-documentation-writer.role.yaml`.
- Require the Dev Documentation Writer to apply STE to all technical-document prose.
- Keep `development-methodology` responsible for selecting exactly one artifact route.
- Keep the selected creation skill responsible for artifact structure and required sections.
- Add `structured-explanation` as a conditional skill.
- Use `structured-explanation` only when an artifact or bounded rationale section must expose facts, hypotheses, unknowns, technical causes, decisions, or the reasoning behind a plan.
- Do not require `QUERY`, `FACT`, or `ANSWER` items in ordinary technical documentation.

### Documentation Review And Verification

- Add `ste-technical-writing` as an unconditional review skill of `agents/roles/dev-activities/dev-artifact-reviewer.role.yaml`.
- Update `skills/documentation-page-verify/SKILL.md` to verify applicable STE principles in README files and custom non-wiki technical documents.
- Require review findings for semantic changes caused by mechanical STE application.
- Detect descriptions that were incorrectly changed into instructions.
- Detect unordered information that was incorrectly changed into an ordered procedure.
- Detect changed identifiers, configuration values, modality, or ownership.
- Distinguish repository STE conformance from verified ASD-STE100 compliance.

### Communication And Explanation Boundaries

- Add an artifact boundary to `skills/effective-communication/SKILL.md`.
- Apply `effective-communication` to user and agent messages, including outcomes, evidence, blockers, decisions, next actions, approvals, and handoffs.
- State that an artifact-specific writing method governs the durable artifact body.
- State that `ste-technical-writing` governs technical prose in the artifact body.
- Do not let `effective-communication` convert descriptive artifact content into instructions, procedures, or status reports.
- Add a reciprocal boundary to `skills/structured-explanation/SKILL.md`.
- Keep its item model responsible for structured technical reasoning.
- Apply STE to the prose inside its items.
- Keep `effective-communication` responsible for the surrounding message and handoff.

### Local Agent Migration

- Treat `.codex/agents/ste_writer.toml` as source and evaluation evidence, not as the canonical STE contract.
- After the portable skill is accepted and installed, either make the local agent a thin consumer of `ste-technical-writing` or retire the local agent.
- Remove duplicated STE rule ownership from the local agent if it remains.
- Do not include the ignored local agent in the repository delivery commit.

### Catalog, Generated Output, And Documentation

- Add the portable skill to the public skill inventory in `README.md`.
- Update `design/skills-modularization.html` with the STE ownership and composition boundaries.
- Update `design/agent-and-skill-definitions.html` with the Documentation Writer and Artifact Reviewer skill relationships.
- Update `design/documentation-templates.html` to state that artifact templates control structure while STE controls technical prose.
- Regenerate supported skill-definition, role-definition, explorer, and native-agent artifacts from their canonical sources.
- Do not edit generated files directly.
- Keep installed and generated agent definitions consistent with the conceptual sources.

### Governed Definition Approval Boundary

Before mutation, obtain explicit approval for these exact governed canonical sources:

- `skills/ste-technical-writing/SKILL.md`
- `skills/ste-technical-writing/agents/openai.yaml`
- `skills/effective-communication/SKILL.md`
- `skills/structured-explanation/SKILL.md`
- `skills/documentation-page-verify/SKILL.md`
- `agents/roles/dev-activities/dev-documentation-writer.role.yaml`
- `agents/roles/dev-activities/dev-artifact-reviewer.role.yaml`

Obtain separate explicit approval before changing this local agent definition:

- `.codex/agents/ste_writer.toml`

Record the exact approval wording, date, and user-message provenance. Run the supported pre-mutation definition check for each governed canonical path.

The approved canonical sources may produce updates to these dependent artifacts through supported generators:

- `design/generated/skill-definitions.js`
- `design/generated/role-definitions.js`
- `design/generated/agent-skill-explorer-data.js`
- `generated/adapters/claude/agents/dev-documentation-writer.md`
- `generated/adapters/codex/agents/dev-documentation-writer.toml`
- `generated/adapters/gemini/agents/dev-documentation-writer.md`
- `generated/adapters/junie/agents/dev-documentation-writer.md`
- `generated/adapters/claude/agents/dev-artifact-reviewer.md`
- `generated/adapters/codex/agents/dev-artifact-reviewer.toml`
- `generated/adapters/gemini/agents/dev-artifact-reviewer.md`
- `generated/adapters/junie/agents/dev-artifact-reviewer.md`

Discovery may identify another required governed canonical source. Do not mutate it under this item until the work-item manifest records its exact path and the user gives explicit approval for that path.

## Acceptance Criteria

- A portable `ste-technical-writing` skill exists and passes focused skill validation.
- The portable skill contains the STE principles and semantic-preservation boundaries from this item.
- All technical documentation created by the Dev Documentation Writer uses STE principles.
- The Dev Documentation Writer still selects one artifact-specific structure owner.
- The Dev Documentation Writer uses `structured-explanation` only for an applicable technical reasoning or plan-rationale section.
- The Dev Artifact Reviewer checks STE conformance in every technical document that it reviews.
- The shared page verifier checks STE conformance for README files and custom non-wiki technical documents.
- `effective-communication` governs the surrounding message and does not reshape the artifact body.
- `structured-explanation` governs the reasoning format, and STE governs the prose inside that format.
- Tests reject a rewrite that changes a description into an instruction.
- Tests reject a rewrite that changes unordered rules into an ordered procedure.
- Tests reject changed identifiers, configuration values, ownership, conditions, or normative force.
- Tests accept necessary technical terms, code, commands, schemas, fixed labels, and exact quotations without forced rewriting.
- Documentation says “repository STE principles” or equivalent unless formal compliance is verified against the applicable issue and dictionary.
- README, design pages, generated definitions, native adapters, and installed behavior agree with the canonical sources.
- The local `ste_writer` agent is not the canonical source after delivery.
- Independent review confirms that the new skill does not duplicate artifact structure, communication procedure, or structured-explanation ownership.
- The verified direct-main commit contains only the intended work-item delivery and preserves unrelated worktree state.

## Dependencies

None.

## Verification

- Run the definition-change check for every approved governed canonical path before mutation.
- Validate the new skill package with the preferred skill validator. Use `scripts/validate-agent-skills.py` only when the preferred validator is unavailable under the skill-authoring fallback rules.
- Add focused contract tests for the portable STE skill and its metadata.
- Add focused role tests for unconditional Documentation Writer and Artifact Reviewer STE loading.
- Add focused role tests for conditional Documentation Writer `structured-explanation` loading.
- Add focused boundary tests for `effective-communication`, `structured-explanation`, and `documentation-page-verify`.
- Test descriptive prose, normative requirements, ordered procedures, unordered rules, conditions, code blocks, commands, identifiers, configuration values, fixed labels, quotations, headings, tables, and structured-explanation items.
- Reuse the original project setup paragraph as a regression fixture.
- Compare output meaning against the original source, not against an earlier rewrite.
- Include a negative fixture that invents `resourceCoordination`.
- Include a negative fixture that converts the complete paragraph into one ordered procedure.
- Include a negative fixture that changes `must`, `must not`, or `may`.
- Run `scripts/build-skill-docs.py` after approved canonical role or skill changes.
- Run the focused generated-output freshness and source-to-output consistency checks.
- Run applicable README and design HTML validation.
- Run focused bundle-content assertions for the new skill and role bindings.
- Run `git diff --check`.
- Obtain independent skill and artifact review before direct-main completion.

## Open Questions

- Which ASD-STE100 issue and controlled dictionary can the project legally use for optional formal-compliance verification?
- Should a later work item extend mandatory STE loading to technical wiki-writing roles after this non-wiki documentation integration is proven?

## Notes

- “All technical documentation” applies to explanatory technical prose. It does not authorize changes to executable code, machine-readable syntax, exact identifiers, or quoted evidence.
- This item establishes non-wiki technical-document integration first because the Dev Documentation Writer owns that artifact family. Wiki roles have different source, federation, and ingest contracts. The open question keeps that possible extension explicit without silently expanding this item.
- A sentence-length target must never cause loss of meaning or alteration of a technical token.
- The local Spark agent and prior model experiments are evaluation evidence. They are not proof of formal ASD-STE100 compliance.
