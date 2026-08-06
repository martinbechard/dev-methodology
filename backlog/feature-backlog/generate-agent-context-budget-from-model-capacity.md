# Generate Agent Context Budgets From Model Capacity

Status: Ready

Type: Feature

Provider: file

Work Item ID: generate-agent-context-budget-from-model-capacity

Completion: direct-main

## Summary

Define a provider-neutral context percentage in every canonical conceptual agent definition and generate each runtime agent's concrete context budget from that percentage, the selected model's actual context capacity, and the mechanism supported by the target adapter.

## Context

Canonical role sources under agents/roles currently select semantic model profiles through modelProfile and optional modelStages, but they do not state how much of the selected model's context window an agent should use. Adapter model-profile sources currently map semantic profiles to concrete models and may carry an optional context label such as extra-long. The generator validates that label but does not render any context field or context-budget instruction for Codex, Claude Code, Gemini CLI, or Junie CLI.

Without a per-agent allocation, generated agents cannot consistently reserve a deliberate share of their actual model capacity. A portable percentage belongs to the canonical agent definition; concrete model capacity and the available enforcement or instruction mechanism remain adapter-owned because model windows and harness capabilities differ.

## Source Evidence

In the current Codex conversation on 2026-08-06, the user requested: “New work item: implement establishing how much percent context to use per agent. The percentage is in the agent canonical definition and needs to be generated based on actual model capacity and adapter mechanisms”. This message directly authorizes creation of this feature item and the exact governed conceptual-agent, schema, and adapter-profile sources listed below.

## Requirements

- Add one required provider-neutral percentage property to the canonical role schema and every current conceptual agent definition. Validate it as a whole-number percentage greater than zero and no greater than 100.
- Keep the percentage in each agents/roles source. Do not place provider model identifiers, token-window sizes, or harness-native context fields in conceptual role definitions.
- Record the effective context capacity for every concrete model selection in the applicable adapter-owned model-profile source using current authoritative model or harness evidence. Do not infer one model's capacity from another model or retain an undocumented placeholder.
- Define an adapter-owned generation mechanism for each supported runtime. Use a native context-budget or context-window property when the runtime supports one; otherwise generate an explicit, stable adapter-facing instruction or a documented unsupported result. Do not silently accept and discard the percentage.
- Calculate each generated budget deterministically from the role percentage and the effective capacity of the concrete model selected by modelProfile. Document rounding, reserved-capacity treatment, and any adapter-specific limits so the generated value is reproducible.
- Apply the same percentage to each modelStages resolution unless repository evidence establishes that a stage-specific percentage is necessary. Generate a capacity-derived result for every stage profile that the runtime can select.
- Fail generation with an actionable error when a role omits the percentage, a value is outside the accepted range, a concrete model lacks capacity evidence, an adapter mechanism cannot represent the required behavior, or a generated value exceeds the adapter's supported bound.
- Expose the canonical percentage, resolved model capacity, derived context budget, and adapter mechanism in the generated definition or generation manifest sufficiently for review and freshness tests. Keep generated outputs replaceable and do not hand-edit them.
- Update the model-resolution and conceptual-agent documentation to explain which source owns the percentage, model capacity, calculation, adapter mechanism, and unsupported-runtime behavior.
- Preserve every agent's existing model, effort, responsibilities, skills, tools, mutation policy, and delegation behavior unless a directly required context-generation change is independently justified.

## Acceptance Criteria

- Every canonical conceptual agent definition declares an explicit valid context percentage and the schema rejects missing, fractional, zero, negative, or above-100 values.
- For representative roles from every semantic model profile, focused tests prove that percentage multiplied by the authoritative concrete model capacity produces the expected runtime budget under the documented rounding and reserve rules.
- Codex, Claude Code, Gemini CLI, and Junie CLI each have a tested adapter disposition: a generated native setting, a generated enforceable instruction, or an explicit unsupported failure backed by current harness evidence.
- Changing only a role's context percentage changes its generated context allocation without changing its model or effort selection.
- Changing an adapter-owned model capacity updates every affected generated allocation without changing canonical role percentages.
- Roles with modelStages receive correct per-stage derived allocations or a clear validation failure when the adapter cannot represent stage-specific context behavior.
- No supported adapter silently ignores the canonical percentage, and no generated context budget exceeds the selected model or harness capacity.
- Generated native agents, the generation manifest, role documentation data, and maintained design documentation are fresh and consistent with the canonical sources.
- Focused comparison proves that unrelated non-context generated fields remain byte-equivalent or semantically equivalent, as appropriate to the generator format.

## Dependencies

None.

## Verification

- Verify model context capacities and available agent-level context mechanisms against current authoritative vendor documentation, installed runtime schemas, or both; retain source links, versions, or command evidence used for each adapter decision.
- Run the supported definition-change preflight for every governed canonical source before mutation, using the approval provenance recorded in this item.
- Add focused schema and parser tests for the percentage property, including all invalid boundaries.
- Add focused adapter-profile validation tests for model capacity and mechanism metadata.
- Add focused generator tests covering every semantic profile, all four supported adapters, modelStages, deterministic rounding, reserved capacity, unsupported mechanisms, and overflow rejection.
- Regenerate supported agent definitions, documentation data, hierarchy or checklist outputs that consume role fields, and the generation manifest through repository-owned generators.
- Run source-to-generated freshness checks, targeted bundle-content tests, YAML validation for changed sources, and git diff --check.
- Obtain fresh independent review of ownership boundaries, capacity evidence, adapter mappings, generated outputs, and regression coverage.

## Open Questions

- What stable canonical field name best expresses the percentage without implying a provider-specific token limit?
- Does each adapter expose a native per-agent context limit, require a generated instruction, or need to reject unsupported allocation, and how does that mechanism interact with modelStages?
- Should the calculation use the advertised full model window or the usable window after a documented reserve for system instructions, tool results, and output tokens?
- Which deterministic rounding unit is accepted by every supported adapter without exceeding the selected model's effective capacity?

## Governed Definition Approval

### Governed Canonical Sources

- agents/role-schema.yaml
- agents/roles/dev-activities/dev-artifact-reviewer.role.yaml
- agents/roles/dev-activities/dev-backlog-coordinator.role.yaml
- agents/roles/dev-activities/dev-backlog-steward.role.yaml
- agents/roles/dev-activities/dev-backlog-watchdog.role.yaml
- agents/roles/dev-activities/dev-browser-operator.role.yaml
- agents/roles/dev-activities/dev-code-reviewer.role.yaml
- agents/roles/dev-activities/dev-coder.role.yaml
- agents/roles/dev-activities/dev-document-topic-editor.role.yaml
- agents/roles/dev-activities/dev-documentation-writer.role.yaml
- agents/roles/dev-activities/dev-merge-coordinator.role.yaml
- agents/roles/dev-activities/dev-orchestrator.role.yaml
- agents/roles/dev-activities/dev-prompt-reviewer.role.yaml
- agents/roles/dev-activities/dev-runtime-diagnostician.role.yaml
- agents/roles/dev-activities/dev-security-reviewer.role.yaml
- agents/roles/dev-activities/dev-skill-lint-reviewer.role.yaml
- agents/roles/dev-activities/dev-ux-specialist.role.yaml
- agents/roles/dev-activities/dev-verifier.role.yaml
- agents/roles/methodology-maintenance/methodology-artifact-reviewer.role.yaml
- agents/roles/methodology-maintenance/methodology-maintainer.role.yaml
- agents/roles/project-setup/project-bootstrapper.role.yaml
- agents/roles/project-setup/project-configurator.role.yaml
- agents/roles/project-setup/project-organiser.role.yaml
- agents/roles/wiki-activities/wiki-architect.role.yaml
- agents/roles/wiki-activities/wiki-artifact-reviewer.role.yaml
- agents/roles/wiki-activities/wiki-ingester.role.yaml
- agents/roles/wiki-activities/wiki-query-responder.role.yaml
- agents/roles/wiki-activities/wiki-researcher.role.yaml
- agents/roles/wiki-activities/wiki-source-collector.role.yaml
- agents/roles/wiki-activities/wiki-topic-verifier.role.yaml
- agents/roles/wiki-activities/wiki-writer.role.yaml
- adapters/codex/model-profiles.yaml
- adapters/claude/model-profiles.yaml
- adapters/gemini/model-profiles.yaml
- adapters/junie/model-profiles.yaml

### Allowed Dependent Artifacts

- scripts/build-skill-docs.py
- scripts/test_bundle_content.py
- README.md
- design/generic-agent-definitions-source.html
- design/agent-and-skill-definitions.html
- design/generated/role-definitions.js
- design/generated agent hierarchy and support-checklist outputs that consume canonical role fields
- generated/adapters/agent-generation-manifest.json
- generator-owned Codex, Claude Code, Gemini CLI, and Junie CLI native definitions corresponding to the governed role sources above
- Focused test fixtures or documentation files directly required to prove the approved context-generation behavior

### Approval Resolution

Approved at creation. The user's 2026-08-06 message in the current Codex conversation explicitly requests a per-agent percentage in the canonical agent definition and generation based on actual model capacity and adapter mechanisms. That wording authorizes only the exact governed sources listed above and their supported dependent artifacts. Any additional governed skill, agent, schema, model-profile, or adapter-definition source requires separate exact-path approval before mutation.

## Notes

- Existing context labels such as extra-long are implementation evidence to reconcile, not a substitute for the canonical per-agent percentage or a proven concrete model capacity.
- Runtime model capacities and supported configuration mechanisms are drift-prone. Implementation must refresh authoritative evidence rather than relying only on the repository's current prose.
- This item does not authorize changing agent responsibilities or selecting different models merely to make context allocation easier.
