---
name: agent-role-authoring
description: Create or review portable canonical agent role definitions with clear routing, authority, structured instructions, skill boundaries, agent dependencies, materially distinct examples, output contracts, and generated runtime behavior. Use when adding or materially changing agent role YAML, role schemas, role examples, or generated native agent definitions.
metadata:
  category: documentation-methodology
---

# Agent Role Authoring

Keep each role focused on one stable responsibility and make its executable contract easy for both agents and maintainers to inspect.

## Workflow

1. Read the owning role schema, nearby canonical roles, assigned skills, generated runtime definitions, and relevant validation tests.
2. Define the role's routing purpose, mutation authority, required inputs, state transitions, dependencies, outputs, and terminal outcomes before writing instructions.
3. Keep short single-phase behavior as a concise instruction string. Use structured instructions when the role has branches, delegation, review loops, failure handling, or several completion conditions.
4. Keep stable role behavior in the role. Reference assigned skills for detailed task methods instead of reproducing their procedures.
5. Use canonical role and skill identifiers anywhere the runtime must resolve a dependency.
6. Write examples that demonstrate materially different starting states, workflow branches, authority boundaries, failures, or terminal outcomes.
7. Regenerate every supported runtime definition and inspect the rendered instructions, skill loading, dependencies, outputs, and model settings.
8. Add or update regression coverage for schema validation, rendered structure, important branches, and failure behavior.

## Structured Instructions

Use the owning schema's structured form when available. In this bundle, the supported subproperties are:

- objective: One concise statement of the responsibility and intended outcome.
- boundaries: Scope, authority, safety, idempotency, and prohibited behavior.
- decisions: State-dependent branches whose conditions and outcomes must be unambiguous.
- workflow: Ordered execution phases expressed as observable actions.
- delegation: Canonical agent dependencies, their conditions, and required handoff evidence.
- review: Independent review routing and acceptance requirements.
- failureHandling: Bounded retry, recovery, fallback, blocked, and unavailable-dependency behavior.
- completion: READY, BLOCKED, or other terminal criteria together with required evidence.

Structured instructions require objective, workflow, and completion. Omit optional sections that add no information. Keep each entry atomic enough to test and render it under one clear heading.

## Contract Rules

- Do not treat file presence as validity. Name the validation gate and the behavior for absent, valid, and invalid state when those states change execution.
- Align the description with actual review, verification, and mutation behavior. Do not promise independent review when the workflow only performs same-owner validation.
- Bound correction and verification loops. State who owns each failure, how many retries are allowed, and which condition ends in BLOCKED.
- Include a terminal status in the output contract when instructions can return different terminal outcomes.
- Keep repository mutation policy aligned with agent-claim loading.
- Declare agent dependencies separately from skills. Skills provide methods; agent dependencies provide isolated responsibility or authority boundaries.
- Keep provider model identifiers out of canonical roles and use semantic model profiles.
- Keep customer-independent definitions free of personal, customer, company, or private operational data.

## Examples

Treat examples as behavioral evidence, not paraphrases of the description.

- Give each example a specific purpose, supported runtime invocation, and plausible response.
- Make the distinguishing state or outcome explicit in the purpose and response.
- Do not label minor wording, framework, or document-set variations as materially different behavior.
- Include blocked, partial, repeated, or unavailable-dependency behavior when those paths are important to the role contract.
- Model the output contract in plausible responses, including status and evidence when required.

## Result

Return the canonical role changes, the role-versus-skill boundary decision, generated runtime evidence, regression coverage, and any remaining portability or contract risk.
