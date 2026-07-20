# Configure Dev Documentation Writer Models

Status: Ready

Type: Feature

## Summary

Configure Dev Documentation Writer to use GPT-5.6-sol with high reasoning in Codex and Junie, and Fable in Claude, without changing the model selection of unrelated agents.

## Context

The conceptual Dev Documentation Writer currently uses the default semantic model profile. That profile resolves to GPT-5.6-terra with medium effort in Codex, Sonnet with medium effort in Junie, and Sonnet 5 in Claude. The existing advanced Codex mapping already resolves to GPT-5.6-sol with high effort, but changing the shared default or advanced profiles would also change unrelated agents and would not produce the requested Claude Fable mapping.

The model system therefore needs a dedicated semantic mapping or an equivalent source-owned per-agent mechanism. Provider model identifiers must remain in adapter-owned model mappings rather than being embedded directly in the conceptual role definition.

Direct user direction on 2026-07-20 requires:

- Codex Dev Documentation Writer: GPT-5.6-sol with high reasoning.
- Junie Dev Documentation Writer: GPT-5.6-sol with high reasoning.
- Claude Dev Documentation Writer: Fable.
- Add GPT-5.6-sol to the applicable supported model choices when the current Junie model catalog or validator cannot express it.

## Requirements

- Give agents/roles/dev-activities/dev-documentation-writer.role.yaml a semantic model selection that resolves independently from the shared default profile.
- Resolve the selected profile for Codex to model gpt-5.6-sol and effort high.
- Resolve the selected profile for Junie to model gpt-5.6-sol and reasoning level high.
- Resolve the selected profile for Claude to the supported Fable model identifier, currently fable-5.
- Preserve the current effective Gemini selection unless a source-consistent mapping is required to keep every adapter profile complete.
- Extend the Junie model choice catalog, schema, validation, generator, or documentation only where current support does not allow gpt-5.6-sol with high reasoning.
- Do not change the shared default mapping or the resolved models of unrelated conceptual agents.
- Keep provider-specific model identifiers in adapters and generated native definitions, not in the conceptual agent definition.
- Regenerate only the supported role, adapter, documentation, hierarchy, manifest, and checklist outputs owned by the approved canonical sources.
- Update focused tests and model-profile documentation so the new selection and its cross-adapter resolution are explicit and machine checked.
- Before mutating governed role, schema, model-profile, or adapter model-profile sources, record the exact file scope authorized by this user direction and run every required definition-change precheck.

## Acceptance Criteria

- The generated Codex Dev Documentation Writer definition names gpt-5.6-sol and high reasoning effort.
- The generated Junie Dev Documentation Writer definition names gpt-5.6-sol and high reasoning level.
- The generated Claude Dev Documentation Writer definition names the supported Fable model.
- Junie model validation and generation accept gpt-5.6-sol with high reasoning without a manual generated-file edit.
- The conceptual role remains provider neutral and resolves through source-owned model-profile mappings.
- A focused comparison proves that unrelated agents retain their prior model and reasoning resolution.
- Every supported adapter contains a complete mapping for the selected semantic profile.
- Generated definitions and documentation are fresh and contain no hand-edited mirror changes.

## Dependencies

None.

## Verification

- Run the exact governed-definition approval checks for every changed canonical role, model-profile, schema, or adapter model-profile source before mutation.
- Run focused model-profile parser, schema, resolution, and generator tests for Codex, Junie, Claude, and the unchanged Gemini mapping.
- Assert the exact generated Dev Documentation Writer model and reasoning fields for Codex, Junie, and Claude.
- Assert unrelated generated agents retain their previous model and reasoning fields.
- Run the applicable role-generation, skill-documentation, hierarchy, manifest, and support-checklist freshness checks.
- Validate representative generated Codex, Junie, and Claude native definitions.
- Run Git diff validation and obtain a fresh independent review of the canonical and generated diff.
- Use Tier 2 verification for the bounded generated-definition change; do not run the full repository or agent catalog solely for this item unless focused evidence identifies broader impact.

## Notes

- Fable means the canonical Fable identifier supported by the Claude adapter rather than a new provider-neutral model name.
- Adding GPT-5.6-sol to Junie support must not silently replace other Junie model choices.
- This item changes model selection only; it does not change Dev Documentation Writer responsibilities, skills, tools, or repository-mutation authority.
