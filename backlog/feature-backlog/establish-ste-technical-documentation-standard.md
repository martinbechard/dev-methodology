# Establish The STE Technical Documentation Standard

Status: Ready

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/establish-ste-technical-documentation-standard.md

Completion: direct-main

## Summary

Create a portable Simplified Technical English (STE) skill for all technical documentation. Integrate the skill with documentation writing, technical reasoning, communication, review, verification, generated adapters, and public methodology documentation. Use GPT-5.5 with medium reasoning effort for dedicated Codex documentation authors and the Dev Artifact Reviewer.

## Context

The repository has no distributed STE skill. It also has no canonical portable contract that applies STE principles to technical-document prose.

The conceptual Dev Documentation Writer does not load STE guidance. It uses artifact-specific creation skills to control document structure. The Dev Artifact Reviewer and `documentation-page-verify` do not verify STE usage.

The role schema supplies `effective-communication` to every conceptual agent. That skill currently has no boundary between user or agent messages and durable artifact bodies. The `structured-explanation` skill controls the `QUERY`, `SUB-QUERY`, `FACT`, `HYPOTHESIS`, `UNKNOWN`, and `ANSWER` format. It does not state how STE applies to the prose inside those items.

Tests with the project setup paragraph showed that STE alone preserved descriptive documentation better than STE combined without a boundary with `effective-communication`. The combined prompt incorrectly changed descriptive information into an ordered procedure. The implementation must prevent this semantic change.

The purpose is clearer technical documentation. Formal ASD-STE100 verification, certification, issue validation, and controlled-dictionary validation are out of scope.

## Source Evidence

On 2026-07-27, the user directed: “All technical documentation should comply with STE principles.”

On 2026-07-27, the user then directed: “Create a workitem for all this. In the workitem list the STE principles we want to use during the execution of the work item, as well as in creating the STE skill. include the other changes.”

On 2026-07-27, the user granted definition-change approval with this direction: “I give approval for modifying the skills currently listed in the work item, not need to indicate getting approvals for them, only for additional skills or agents beyond them.”

On 2026-07-27, the user resolved both open questions with this direction: “We are not getting formal-compliance verification, this is only to try to create clearer artifacts and documentation. The wiki writer agents should also use STE - basically any agents creating technical documentation.”

On 2026-07-27, the user set the documentation-authoring model with this direction: “We should change all Documentation writing agents to use GPT-5.5 medium - add that to the work item.”

On 2026-07-27, the user set the documentation reviewer model with this direction: “Add in the workitem to also have a 5.5 reviewer agent.”

The current portable contracts are `skills/effective-communication/SKILL.md`, `skills/structured-explanation/SKILL.md`, `agents/role-schema.yaml`, `agents/roles/dev-activities/dev-documentation-writer.role.yaml`, and `skills/documentation-page-verify/SKILL.md`.

The approval covers every exact skill and agent definition in the governed-definition scope below. It does not cover a later addition to that scope.

The direction to cover any agent that creates technical documentation authorizes `agents/role-schema.yaml` as the exact shared-skill binding source.

The GPT-5.5 directions authorize `adapters/codex/model-profiles.yaml`, the exact documentation-authoring role paths, and `agents/roles/dev-activities/dev-artifact-reviewer.role.yaml` in the governed-definition scope below.

## STE Principles For This Work Item

Apply these principles to technical prose that is written during execution, including plans, design notes, explanations, documentation, review findings, verification results, and handoffs:

- Preserve the source meaning.
- Preserve each requirement, condition, permission, prohibition, and configuration distinction.
- Preserve exact identifiers, commands, paths, configuration values, code, schema names, fixed labels, and quoted source text.
- Use the same term for the same item or action.
- Use one meaning for each word in a given context.
- Use common and precise words.
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

Use these same principles as the initial content contract for the new portable STE skill. Refine a principle only when source evidence shows that it conflicts with an established repository contract. Record the reason for each refinement.

## Requirements

### Portable STE Skill

- Create `skills/ste-technical-writing/SKILL.md`.
- Create `skills/ste-technical-writing/agents/openai.yaml`.
- Give the skill a narrow purpose: write, rewrite, and review technical-document prose with the STE principles in this item.
- Make the skill portable across supported harnesses.
- Keep the main workflow concise.
- State that the repository principles are mandatory for technical-document prose.
- State that the skill improves clarity but does not verify or certify formal ASD-STE100 compliance.
- Require preservation of exact technical content and normative meaning.
- State the boundary for code, commands, identifiers, schemas, fixed labels, and verbatim quotations.
- State that the artifact-specific method controls document structure.
- State that STE controls prose within a structured explanation but does not replace its item model.
- State that STE does not convert descriptions into instructions or unordered rules into procedures.
- Validate the complete skill package with the repository-supported skill validator.

### Agent Coverage

- Add `ste-technical-writing` to the unconditional shared skills in `agents/role-schema.yaml`.
- Give every conceptual agent access to the same STE contract.
- Apply the contract only when an agent writes, rewrites, or reviews technical-document prose.
- Apply the contract to durable wiki pages, hubs, digests, architecture, maintenance guidance, technical reports, specifications, designs, plans, README files, and custom technical documents.
- Include wiki writers, wiki ingesters, wiki architects, methodology maintainers, and other agents when their current work creates or changes technical documentation.
- Do not apply STE rules to executable code, machine-readable data, exact technical tokens, verbatim quotations, or ordinary communication envelopes.
- Keep `effective-communication` responsible for ordinary user and agent messages.

### Documentation Authoring And Review Model

- Use the existing semantic `documentation` model profile for dedicated documentation-authoring roles and the Dev Artifact Reviewer.
- Map the Codex `documentation` profile to model `gpt-5.5`.
- Set the Codex reasoning effort for that profile to `medium`.
- Keep other harness mappings native to their supported model catalogs.
- Do not invent a GPT model mapping for a harness that does not support that model.
- Keep `modelProfile: documentation` on the Dev Documentation Writer.
- Set `modelProfile: documentation` on the Wiki Architect.
- Set `modelProfile: documentation` on the Wiki Ingester.
- Set `modelProfile: documentation` on the Wiki Researcher.
- Set `modelProfile: documentation` on the Wiki Source Collector.
- Set `modelProfile: documentation` on the Wiki Writer.
- Set `modelProfile: documentation` on the Dev Artifact Reviewer.
- Keep other review-only, verification-only, query-response, and general implementation roles on their existing profiles unless their own approved scope changes.

### Documentation Writer

- Supply `ste-technical-writing` to the Dev Documentation Writer through the shared role schema.
- Require the Dev Documentation Writer to apply STE to all technical-document prose.
- Keep `development-methodology` responsible for selecting exactly one artifact route.
- Keep the selected creation skill responsible for artifact structure and required sections.
- Add `structured-explanation` as a conditional skill.
- Use `structured-explanation` only when an artifact or bounded rationale section must expose facts, hypotheses, unknowns, technical causes, decisions, or the reasoning behind a plan.
- Do not require `QUERY`, `FACT`, or `ANSWER` items in ordinary technical documentation.

### Documentation Review And Verification

- Supply `ste-technical-writing` to the Dev Artifact Reviewer and wiki review roles through the shared role schema.
- Use the existing Dev Artifact Reviewer as the GPT-5.5 medium reviewer for technical documentation.
- Update `skills/documentation-page-verify/SKILL.md` to verify applicable STE principles in README files and custom non-wiki technical documents.
- Require review findings for semantic changes caused by mechanical STE application.
- Detect descriptions that were incorrectly changed into instructions.
- Detect unordered information that was incorrectly changed into an ordered procedure.
- Detect changed identifiers, configuration values, modality, or ownership.
- Do not report formal ASD-STE100 verification or certification.

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

### Catalog, Generated Output, And Documentation

- Add the portable skill to the public skill inventory in `README.md`.
- Update `design/skills-modularization.html` with the STE ownership and composition boundaries.
- Update `design/agent-and-skill-definitions.html` with the shared STE relationship and its technical-document boundary.
- Update `design/documentation-templates.html` to state that artifact templates control structure while STE controls technical prose.
- Regenerate supported skill-definition, role-definition, explorer, and native-agent artifacts from their canonical sources.
- Do not edit generated files directly.
- Keep installed and generated agent definitions consistent with the conceptual sources.

### Governed Definition Approval Scope

Approval is granted for these exact governed canonical sources:

- `skills/ste-technical-writing/SKILL.md`
- `skills/ste-technical-writing/agents/openai.yaml`
- `skills/effective-communication/SKILL.md`
- `skills/structured-explanation/SKILL.md`
- `skills/documentation-page-verify/SKILL.md`
- `agents/role-schema.yaml`
- `adapters/codex/model-profiles.yaml`
- `agents/roles/dev-activities/dev-documentation-writer.role.yaml`
- `agents/roles/dev-activities/dev-artifact-reviewer.role.yaml`
- `agents/roles/wiki-activities/wiki-architect.role.yaml`
- `agents/roles/wiki-activities/wiki-ingester.role.yaml`
- `agents/roles/wiki-activities/wiki-researcher.role.yaml`
- `agents/roles/wiki-activities/wiki-source-collector.role.yaml`
- `agents/roles/wiki-activities/wiki-writer.role.yaml`

No additional approval request is necessary for these exact paths. Use the approval evidence in Source Evidence for each required pre-mutation definition check.

The approved canonical sources may produce updates to these dependent artifacts through supported generators:

- `design/generated/skill-definitions.js`
- `design/generated/role-definitions.js`
- `design/generated/agent-skill-explorer-data.js`
- Generated role adapters under `generated/adapters/claude/agents`.
- Generated role adapters under `generated/adapters/codex/agents`.
- Generated role adapters under `generated/adapters/gemini/agents`.
- Generated role adapters under `generated/adapters/junie/agents`.

Discovery may identify another required skill or agent definition. Do not mutate it under this item until the work-item manifest records its exact path and the user gives explicit approval for that path.

## Acceptance Criteria

- A portable `ste-technical-writing` skill exists and passes focused skill validation.
- The portable skill contains the STE principles and semantic-preservation boundaries from this item.
- Every conceptual agent receives the shared STE skill.
- Agents apply STE only when they write, rewrite, or review technical-document prose.
- The Codex `documentation` profile uses `gpt-5.5` with `medium` reasoning effort.
- Every dedicated documentation-authoring role uses the semantic `documentation` profile.
- The Dev Artifact Reviewer uses the semantic `documentation` profile and resolves to GPT-5.5 with medium reasoning effort in Codex.
- Non-Codex harnesses retain supported native model mappings.
- All technical documentation created by the Dev Documentation Writer uses STE principles.
- Durable technical wiki content created by wiki agents uses STE principles.
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
- No output claims formal ASD-STE100 verification or certification.
- README, design pages, generated definitions, native adapters, and installed behavior agree with the canonical sources.
- Independent review confirms that the new skill does not duplicate artifact structure, communication procedure, or structured-explanation ownership.
- The verified direct-main commit contains only the intended work-item delivery and preserves unrelated worktree state.

## Dependencies

None.

## Verification

- Run the definition-change check for every approved governed canonical path before mutation.
- Validate the new skill package with the preferred skill validator. Use `scripts/validate-agent-skills.py` only when the preferred validator is unavailable under the skill-authoring fallback rules.
- Add focused contract tests for the portable STE skill and its metadata.
- Add focused role-schema tests that prove every conceptual agent receives `ste-technical-writing`.
- Add focused boundary tests that prove STE applies to technical documentation but not to ordinary communication or non-document artifacts.
- Add focused model-profile tests for the exact Codex `gpt-5.5` and `medium` mapping.
- Add focused role tests for the Documentation Writer, Wiki Architect, Wiki Ingester, Wiki Researcher, Wiki Source Collector, and Wiki Writer.
- Verify that each dedicated documentation-authoring role resolves to the Codex `documentation` profile.
- Add a focused role test that proves the Dev Artifact Reviewer resolves to the Codex `documentation` profile.
- Verify that non-Codex adapters retain valid native mappings.
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

None.

## Notes

- “All technical documentation” applies to explanatory technical prose. It does not authorize changes to executable code, machine-readable syntax, exact identifiers, or quoted evidence.
- Wiki roles retain their source, federation, ingest, and verification contracts. STE changes the clarity of their technical prose, not those ownership boundaries.
- GPT-5.5 with medium effort is the Codex mapping for documentation-authoring roles. Other harnesses use their supported native model mappings.
- The existing Dev Artifact Reviewer is the GPT-5.5 medium reviewer. This item does not create a second documentation-review role.
- Formal ASD-STE100 compliance and certification are non-goals.
- A sentence-length target must never cause loss of meaning or alteration of a technical token.
