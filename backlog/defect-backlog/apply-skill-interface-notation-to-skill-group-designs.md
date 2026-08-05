# Apply Skill Interface Notation To Skill Group Designs

Status: Ready

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/apply-skill-interface-notation-to-skill-group-designs.md

Completion: direct-main

## Summary

Correct the shared applied skill-group model and every affected group design so provider families use the object-oriented Skill interface, Provider Skill, realization, and AGENTS.md factory notation consistently.

## Context

The steady-state skill-group documents were rewritten after the object-oriented method established a distinct public interface contract, direct interface consumption, Provider Skills, implementation realization, and AGENTS.md factory selection. The current applied diagrams retained AGENTS.md routing families but did not preserve the separate interface and implementation relationships. This makes substitution and conformance invisible, especially for Persistence, resource coordination, and Commit delivery.

The review covers design/object-oriented-skill-group-models.md and all seven files under design/skill-groups. The reusable method at design/object-oriented-agent-and-skill-model.md is the notation authority.

## Source Evidence

On 2026-08-05, the user requested: "The skill groups designs don't seem to apply all the conventions of the object-oriented design approach, in particular the Skills Interface notation. Review all designs and correct them where needed". After an explanation of repository coordination, the user directed: "ok continue the audit and corrections".

## Requirements

- Audit the shared applied model and all seven group designs against the complete reusable object-oriented notation.
- Represent every shared provider contract separately from the AGENTS.md factory that selects a provider.
- Show Provider Skills realizing the interface they implement, without turning realization into a loading dependency.
- Preserve exact-name, conditional, cross-group, expanded-group, collapsed-group, public-member, and containment conventions where they remain correct.
- Keep skill identities, public procedures, group membership, and authoritative links aligned with current repository sources.
- Update the adjacent applied-model checklist and findings from the completed audit.

## Acceptance Criteria

- The applied legend defines Skill interface, Interface Skill, Provider Skill, realization, and AGENTS.md factory notation without conflating their meanings.
- Backlog Management depicts its creation and management interfaces, provider realizations, and Persistence factories.
- Concurrent Tasking and Direct Main Delivery depict resource-helper and delivery interfaces consistently with their providers and selection paths.
- Every other group design either applies the relevant interface notation or has no unsupported provider-family abstraction.
- The completed review evidence covers all eight applied design documents and records no unresolved material convention defect.
- Mermaid structure, local links, section openings, focused content assertions, and Git whitespace checks pass.

## Dependencies

None.

## Verification

- Complete the structured review checklist before updating the findings artifact.
- Validate Mermaid fences, class relationships, stereotypes, and interface realization direction for every applied diagram.
- Resolve every local Markdown link in the changed design and review files.
- Run the focused bundle-content assertions that consume the applied skill-group design contract.
- Run Git diff whitespace validation.

## Open Questions

None.
