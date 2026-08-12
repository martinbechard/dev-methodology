# Estimate Agent Work In Agent-Hours

Status: Ready

Type: Feature

Provider: file

Work Item ID: estimate-agent-work

Completion: main-branch

## Summary

Create a portable estimate-agent-work skill and assign it to Dev Coder so AI-delivered engineering work is estimated in generated tokens, complexity, turns, agent-hours, non-model runtime, and parallel wall-clock time instead of human person-days.

## Context

Human effort units do not describe the dominant cost and elapsed-time drivers of agentic delivery. The working throughput assumption is 50 generated output tokens per second, including reasoning. Generated-token effort therefore converts to agent-hours at 180,000 generated tokens per agent-hour. Parallelism reduces elapsed wall-clock time through the critical path but does not reduce total agent-hours.

The estimate must keep live evaluation consumption and external tool or test runtime separate from implementation-agent generation. Input and cached tokens may affect monetary cost and context pressure, but they must not be converted through the generated-output throughput rate.

## Source Evidence

The user explicitly requested on 2026-08-12 in Codex task 019ff660-663f-7271-a4da-c30e6c054cf7: "parallelism is a good point - I guess we need to qualify estimates as agent-hours. This would make an interesting skill for our Dev Coder agent - log a backlog item for that skill."

The same conversation established generated tokens, including reasoning, as the throughput basis and supplied the current planning assumption of 50 generated output tokens per second.

## Requirements

- Create the portable estimate-agent-work skill with a clear contract for estimating AI-delivered engineering work.
- Assign the skill to the Dev Coder conceptual agent without moving general work-planning authority away from the roles that own scope and dispatch decisions.
- Define complexity levels in terms of reasoning uncertainty, integration breadth, verification burden, correction risk, and coordination depth.
- Estimate generated tokens, including reasoning, and convert them to agent-hours using an explicit configurable throughput assumption that defaults to 50 generated tokens per second.
- Estimate autonomous turns as checkable work cycles rather than equal-duration time units or user-message counts.
- Report total agent-hours, critical-path agent-hours, expected parallelism, and expected wall-clock duration without claiming that parallelism reduces total model effort.
- Report tool, build, test, browser, live-evaluation, external-service, approval, and other non-model runtime separately.
- Separate implementation-agent generation from tokens consumed by executing live evaluation scenarios.
- State uncertainty, assumptions, range drivers, and confidence; avoid false precision.
- Include compact calculation examples and a reusable estimate output shape.
- Keep monetary token cost optional and distinct from effort unless current provider prices are supplied or verified.
- Regenerate supported native agent adapters and update affected catalog documentation and focused regression coverage through repository-supported generators.

## Acceptance Criteria

- The new skill produces estimates containing complexity, generated-token range, agent-hours, expected turns, non-model runtime, parallelism assumptions, and wall-clock range.
- The conversion is mathematically consistent: agent-hours equal generated tokens divided by the configured generated-token throughput and by 3,600 seconds per hour.
- The default 50-token-per-second assumption yields 180,000 generated tokens per agent-hour and is visibly identified as an assumption rather than a universal measured rate.
- Examples distinguish total agent-hours from critical-path elapsed time and distinguish implementation generation from live-evaluation consumption.
- The Dev Coder conceptual source and every supported generated adapter contain the assigned skill after supported regeneration.
- Focused contract tests cover conversions, parallel and serial examples, uncertainty ranges, excluded runtime, and protection against person-day estimates presented as the primary AI effort measure.
- Relevant skill, agent, generated-output freshness, catalog, documentation, and diff checks pass.
- Independent review finds no ownership confusion between estimation guidance and backlog, architecture, dispatch, or acceptance authority.

## Dependencies

None.

## Verification

- Validate the new skill package and metadata with the repository-supported skill checks.
- Run focused catalog assertions for the skill inventory and Dev Coder assignment.
- Run the supported conceptual-agent generation command and verify exact source-to-adapter consistency.
- Run focused tests for every added conversion or estimate-contract helper.
- Check affected README and design references for catalog consistency.
- Run Git diff whitespace validation.
- Obtain independent skill and generated-artifact review before delivery.

## Open Questions

- Determine whether the skill should prescribe one fixed complexity scale or a small extensible rubric.
- Determine whether measured throughput overrides should be recorded per model, reasoning profile, harness, or execution environment.
- Determine whether a deterministic calculator belongs in the skill package or whether transparent formulas and examples are sufficient.

## Governed Definition Approval

### Governed Canonical Sources

- skills/estimate-agent-work/SKILL.md
- agents/roles/dev-activities/dev-coder.role.yaml

### Allowed Dependent Artifacts

- skills/estimate-agent-work/agents/openai.yaml
- generated/adapters/codex/agents/dev-coder.toml
- generated/adapters/claude/agents/dev-coder.md
- generated/adapters/gemini/agents/dev-coder.md
- generated/adapters/junie/agents/dev-coder.md
- README.md
- design/agent-and-skill-definitions.html
- design/agent-and-skill-evaluations.html
- scripts/test_bundle_content.py
- Additional generator-owned catalog projections and focused test files only when repository discovery proves they consume one of the approved canonical sources.

### Approval Resolution

Approved at creation. On 2026-08-12, in Codex task 019ff660-663f-7271-a4da-c30e6c054cf7, the user explicitly requested a skill for Dev Coder to qualify AI-work estimates as agent-hours and asked that the backlog item be logged. This approval covers only the two exact governed canonical sources listed above. Any additional governed skill or agent-definition source requires separate user approval.

## Notes

This item defines an estimation method, not a promise that generated-token throughput is constant. Implementers must preserve the distinction between an assumed planning rate, an observed rate, and a provider-specific billing rate.
