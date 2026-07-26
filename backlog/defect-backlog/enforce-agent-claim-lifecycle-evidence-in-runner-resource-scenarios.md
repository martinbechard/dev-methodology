# Restrict Coordination Lifecycle Evaluation To Coordination Skills

Status: Ready

Type: Defect

Owner: Unowned

Provider: file

Provider Reference: backlog/defect-backlog/enforce-agent-claim-lifecycle-evidence-in-runner-resource-scenarios.md

Completion: direct-main

## Summary

Evaluate ordinary skills in single-user mode without testing claim acquisition, release, or other coordination behavior. Use coordination scenarios only when evaluating coordination skills.

## Problem

The previous work-item design attempted to make the general evaluation runner prove agent-claim lifecycle behavior whenever a scenario selected agent-claim. That approach puts coordination concerns into evaluations for skills whose behavior does not depend on coordination.

It would also create unnecessary duplicate coverage by making every skill support both coordinated and solo evaluation modes. Ordinary skill evaluations should test the skill's own behavior, not whether an unrelated coordination system was applied.

## Requirements

- Run ordinary skill evaluations in single-user mode with resource coordination set to none.
- Do not require ordinary skill evaluations to acquire claims, release claims, inspect a claim registry, or produce claim lifecycle evidence.
- Use coordination scenarios only for skills whose purpose includes coordination behavior, such as agent-claim, agent-claim-command, agent-claim-mcp, and work-item coordination skills.
- Test claim acquisition, conflict handling, release, and related evidence in the focused suites owned by those coordination skills.
- Do not add coordinated and solo variants to every skill evaluation.
- Do not require every skill to support both coordinated and solo evaluation modes.
- Keep coordination infrastructure available to coordination-focused suites without making it a general skill-evaluation requirement.

## Acceptance Criteria

- An ordinary skill suite runs successfully without claim calls or claim lifecycle evidence.
- An ordinary skill suite is not rejected because an empty shared claim registry or pre-existing claim-event history exists.
- A focused coordination-skill suite can explicitly select coordination mode and test its expected claim behavior.
- Runner tests prove that coordination checks are activated by a coordination-focused suite, not merely by evaluating an arbitrary skill.
- No general requirement is introduced for every skill to have both coordinated and solo scenarios.

## Implementation Guidance

- Identify the explicit suite or scenario metadata that marks a coordination-focused evaluation.
- Default ordinary skill evaluations to single-user mode.
- Keep claim lifecycle assertions within focused coordination tests.
- Remove or revise runner assertions that treat claim evidence as a general evaluation requirement.
- Do not change unrelated skill definitions merely to add coordination variants.

## Verification

- Run targeted runner tests for ordinary single-user skill evaluation.
- Run targeted coordination-skill tests that intentionally exercise claim behavior.
- Add one negative regression proving that an ordinary skill does not need claim evidence.
- Add one positive regression proving that an explicitly coordination-focused suite can still test claim lifecycle behavior.
- Run git diff --check.

## Dependencies

None.

## Superseded Recovery History

The rejected candidates e437702d, 446371ff, 4778fd44, b22704da, and ac579e7c attempted to strengthen general runner validation of claim lifecycle evidence. They remain historical review evidence and must not be integrated or reused as the implementation plan for this revised item.

The previous exhausted-correction and blocker records are superseded because they addressed trusted adapters, release-to-commit binding, journal integrity, and process cleanup under the former general coordination-evaluation model. The revised work must begin from current main and follow the single-user-by-default model above.
