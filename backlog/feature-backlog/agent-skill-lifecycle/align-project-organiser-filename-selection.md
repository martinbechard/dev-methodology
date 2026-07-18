# Align Project Organiser Filename Selection

Status: Ready

Type: Defect

## Summary

Remove the generated Project Organiser adapter conflict that simultaneously requires the agent to choose an approved artifact path and prohibits it from choosing filenames.

## Context

The Project Organiser conceptual role owns repository placement decisions. Its contract requires choosing an approved destination, validating the filename against repository guidance, and returning the selected path with placement-audit evidence.

The generated Codex adapter also inlines the structured-design response-only rule that says not to choose filenames. That prohibition is valid for response-only design work, but it contradicts the Project Organiser role when filename and destination selection are the requested output.

The complete conceptual-agent suite rollout confirmed the conflict while freezing the Project Organiser role, generated adapter, and assigned skill rules. The evaluation infrastructure did not edit the subject contract.

## Evidence

- agents/roles/project-setup/project-organiser.role.yaml lines 4 through 7 require repository placement decisions.
- agents/roles/project-setup/project-organiser.role.yaml lines 19 through 23 require filename validation.
- agents/roles/project-setup/project-organiser.role.yaml lines 49 through 54 require the approved path and placement audit in the result.
- generated/adapters/codex/agents/project-organiser.toml lines 624 through 627 contain the conflicting prohibition against choosing filenames.
- evals/agent-tests/project-organiser contains the frozen executable suite that exposed the conflict.

## Requirements

- Preserve response-only structured-design behavior when no artifact authoring or placement decision is requested.
- Permit Project Organiser to choose a filename and destination when its canonical role owns that decision.
- Express the exception in the reusable source contract rather than editing generated adapters by hand.
- Regenerate all native adapters and documentation derived from the changed source.
- Add regression coverage proving that the Project Organiser contract and inlined skills contain no contradictory filename rules.

## Acceptance Criteria

- The canonical Project Organiser role still requires an approved path and placement audit.
- The generated Codex Project Organiser adapter permits required filename selection.
- Response-only structured-design requests continue to avoid unauthorized artifact creation.
- Generated adapters are fresh and repository contract tests pass.
- The Project Organiser executable scenarios can be rerun without freezing contradictory authority.

## Dependencies

None.

## Verification

- Run the focused generated-adapter and bundle-content tests.
- Run Agent Skill validation and every generated-output freshness check.
- Run the Project Organiser suite scenarios and inspect retained identity and Judge evidence.
- Run repository unit tests and Git diff validation.

## Notes

- Do not patch generated/adapters/codex/agents/project-organiser.toml directly.
- Keep the correction scoped to mode-aware filename authority; do not broaden artifact-writing permission.
