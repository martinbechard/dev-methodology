# Normalize Provider-Family Interface Naming

Status: Starting

Type: Defect

Provider: file

Work Item ID: normalize-provider-family-interface-naming

Completion: direct-main

## Summary

Define and enforce one naming model for Interface Skills, provider-family notation, and Provider Skills so diagrams, skill identities, and project routing describe the same dependency structure.

## Context

The object-oriented analysis distinguishes a public Skill interface from a concrete Interface Skill file, but the applied models currently use incompatible family forms. `create-*-work-item` and `manage-*-work-items` put the wildcard inside the name, while `deliver-work-item-*` and `agent-claim-*` put it at the end. The provider names mirror those inconsistencies, and the documents do not yet state how a wildcard family label maps to an exact loadable SKILL.md identity.

The maintained method also distinguishes `<<Skill interface>>` from `<<Interface Skill>>`, but the applied group diagrams do not consistently prove whether the shown node is an actual skill file or an analysis-only contract. Without one rule, a diagram can appear to show a file dependency that cannot be resolved from the skill catalog.

## Source Evidence

On 2026-08-05, the user requested a further naming and responsibility audit and stated: "the pattern is to have * at the end of the interface, not in the middle. Some provider skills don't have names that match the interface stem." Repository evidence appears in `design/object-oriented-agent-and-skill-model.md`, `design/object-oriented-skill-group-models.md`, `design/skill-groups/backlog-management.md`, `design/skill-groups/concurrent-tasking.md`, and `design/skill-groups/direct-main-delivery.md`.

## Requirements

- Define an exact Interface Skill identity as a loadable kebab-case skill name without wildcard characters.
- Define its provider-family display notation as the exact Interface Skill identity followed by `-*`.
- Require each Provider Skill in that family to use the complete interface stem followed by one provider suffix, such as `create-work-item-file` for `create-work-item-*`.
- Keep a conceptual `Skill interface` distinct from a concrete `Interface Skill`; diagrams must not use the concrete-file stereotype unless an exact SKILL.md exists.
- State how AGENTS.md routing names the exact selected Provider Skill while Agents and using skills depend on the exact Interface Skill or its public procedures.
- Update the reusable examples so the wildcard is terminal and the visible interface, provider stem, procedure vocabulary, and exact file identity are coherent.
- Add deterministic validation that inventories interface-family labels and provider identities and rejects a nonterminal wildcard or a provider name that does not begin with the full interface stem.
- Retain semantic review by a methodology reviewer for interface members, provider behavior, and consumer expectations; deterministic name checks do not replace that review.

## Acceptance Criteria

- The analysis guide gives one unambiguous mapping among an Interface Skill file, its `-*` family label, and its provider names.
- Every maintained provider-family example uses a terminal wildcard.
- Concrete Interface Skill and conceptual Skill interface stereotypes are used according to whether a loadable file exists.
- A focused automated check fails for `create-*-work-item`, `manage-*-work-items`, or a provider whose name does not share the complete interface stem.
- The object-oriented method, applied-model legend, review checklists, and generated documentation remain mutually consistent.
- Independent methodology review confirms that the rule explains the underlying file and dispatch relationships rather than merely prescribing spelling.

## Dependencies

None.

## Verification

- Run the focused provider-family naming validation against all maintained skill-group documents.
- Run the structured documentation checks for both object-oriented model documents.
- Regenerate supported documentation outputs and run their freshness checks.
- Run Markdown link validation and `git diff --check`.
- Obtain fresh independent methodology review.

## Open Questions

None. The exact package uses the interface stem without `*`; the terminal wildcard is family notation rather than a filesystem character.

## Notes

The provider-family rename items may proceed from the exact rule stated here without waiting for this documentation item to merge. Overlap on shared diagrams or validation files is a resource-coordination concern, not a hard lifecycle dependency.

## Current Starting Handoff Evidence

Transition: Ready -> Starting.

Parent Coordination Thread: 019fb057-1767-7ef2-b5fa-41f4417b20b3.

Launch Reservation: One Root Dev Orchestrator task for this exact work item.

Normalized Objective: Normalize provider-family interface naming.

Dispatch Time: 2026-08-06T04:00:57Z.

Intended Root Role: Root Dev Orchestrator.

Launch Result: Not attempted.

Canonical Conversation: None.

Owner: Unowned pending the task's Starting -> Running transition.

Last Contact: 2026-08-06T04:00:57Z; parent Coordinator recorded the reservation.

Next Reconciliation: No later than 2026-08-06T04:15:57Z.

Required Next Lifecycle Transition: The new task must directly record Starting -> Running, establish its exact Work Item ID activity=work claim, and then begin scoped implementation. Final reconciliation follows the provider-name deliveries if their shared diagrams or validation files reach main first.
