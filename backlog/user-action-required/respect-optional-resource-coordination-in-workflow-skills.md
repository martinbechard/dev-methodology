# Respect Optional Resource Coordination In Workflow Skills

Status: User Action Required

Type: Defect

Provider: file

Work Item ID: respect-optional-resource-coordination-in-workflow-skills

Completion: direct-main

## Summary

Make integration, delivery, and end-to-end verification skills respect the project-selected resource-coordination setting instead of naming agent-claim unconditionally.

## Context

PROJECT.yaml supports resource_coordination values none and agent-claim. Project Configurator renders the selected policy through AGENTS.md and requires projects selecting none to load no claim skill or claim procedure. The completed selectable-resource-coordination contract also requires ordinary workflow skills to consume the project-selected policy rather than hard-code agent-claim.

Current source contradicts that boundary:

- skills/integrate-agent-work/SKILL.md says to follow the Claim Events table in agent-claim during integration.
- skills/deliver-work-item-feature-branch/SKILL.md says to follow the Claim Events table in agent-claim during publication.
- skills/deliver-work-item-direct-main/SKILL.md says to follow the Claim Events table in agent-claim during integration.
- skills/verify-end-to-end-workflow/SKILL.md says to apply agent-claim when verification triggers a claim event.

Those exact-name instructions can require an unloaded skill when resource_coordination is none. They also make static dependency diagrams appear to give those workflow skills ownership of a project-specific loading decision that belongs to AGENTS.md.

## Source Evidence

During review of design/skill-groups/concurrent-tasking.md on 2026-08-05, the user directed: "Make the links optional if the skill IS NOT ALWAYS loaded. Add the condition when it is loaded. link it to the shape that loads it. If it's a project-specific decision then show it loaded via AGENTS.md." Source comparison against PROJECT.yaml, skills/create-project-configuration/SKILL.md, and the four workflow skills above confirmed the contract mismatch. The user authorized correction of the documentation model but did not authorize mutation of the four governed skill definitions.

## Requirements

- Replace unconditional agent-claim references with vocabulary that consumes the project-selected resource-coordination policy.
- Perform no claim discovery, acquisition, heartbeat, release, or claim-specific evidence handling when resource_coordination is none.
- Preserve the complete agent-claim behavior when AGENTS.md selects agent-claim.
- Keep AGENTS.md responsible for loading the project-selected coordination skill; do not add agent-claim to conceptual Agent skill lists.
- Keep helper transport selection subordinate to agent-claim and separate from workflow skills.
- Update focused evaluations and generated documentation affected by the corrected public instructions.

## Acceptance Criteria

- All four workflow skills operate coherently with resource_coordination none and agent-claim.
- No workflow skill unconditionally loads or requires agent-claim when project configuration selects none.
- Static dependency diagrams point project-selected resource-coordination loading from AGENTS.md and retain skill-owned conditions only for decisions owned by those skills.
- Focused tests cover both resource-coordination selections for integration, delivery, and end-to-end verification.
- Generated skill documentation is current and all changed definitions pass independent methodology review.

## Dependencies

None.

## Verification

- Run the governed-definition pre-mutation check for each approved canonical source.
- Run focused integration, direct-main delivery, feature-branch delivery, and end-to-end verification tests with resource_coordination none and agent-claim.
- Run affected skill probes and generated-documentation freshness checks.
- Search maintained workflow skills for unconditional exact-name agent-claim references and classify each remaining occurrence.
- Run Markdown link checks and git diff --check.

## Open Questions

Determine the precise shared phrase that tells a workflow skill to apply the selected resource-coordination procedure without inventing an Interface Skill that does not exist.

## Governed Definition Approval

### Governed Canonical Sources

- skills/integrate-agent-work/SKILL.md
- skills/deliver-work-item-feature-branch/SKILL.md
- skills/deliver-work-item-direct-main/SKILL.md
- skills/verify-end-to-end-workflow/SKILL.md

### Allowed Dependent Artifacts

- evals/skill-probes.yaml
- directly affected focused evaluation fixtures and tests identified through source discovery
- design/skill-groups/concurrent-tasking.md
- design/generated/skill-definitions.js
- supported generated adapter files regenerated from only the approved canonical sources

### Approval Resolution

Pending. The user authorized the static documentation correction on 2026-08-05 but did not authorize mutation of these four governed skill-definition paths.

## User Action Required

### Question for the User

Do you approve updating exactly the four governed SKILL.md files listed above so their workflows use the resource-coordination policy selected through AGENTS.md and perform no claim procedure when the project selects none?

### Why User Input Is Required

The defect is confirmed, but correcting it changes four governed portable skill definitions. The current documentation request does not grant authority to mutate those definitions.

### Options and Tradeoffs

- Approve the four-path correction: preserves resource coordination as an independent project choice and makes the workflow skills consistent with existing setup policy.
- Redesign configuration so integration, delivery, and verification always require agent-claim: removes the optional path but reverses the established selectable-resource-coordination contract and requires broader governed changes.
- Defer the correction: preserves current definitions and their contradiction with resource_coordination none.

### Resolution

Pending.

### Unattended Work Boundary

Do not mutate the four governed SKILL.md files or their generated mirrors before approval. Read-only source discovery and analysis may continue. The already-authorized correction to design/skill-groups/concurrent-tasking.md remains independent and complete.
