# Object-Oriented Skill Group Models

## Scope

This index applies the reusable [Object-Oriented Analysis Of Agents And Skills](object-oriented-agent-and-skill-model.md) to the established methodology skill groups.

Each group has its own document so a reader can inspect one responsibility boundary without loading the complete set. The groups are analytical views of responsibility. They do not replace the catalog categories stored in skill metadata.

Each SKILL.md from the established directory tree stays in its primary group. A Cross-group node appears when a current Agent definition or SKILL.md reaches across that boundary. A Cross-group responsibility marker means that a skill remains in its primary group while part of its current procedure records or invokes another group’s concern. Both markers expose current coupling without deciding that the skill should be split.

AGENTS.md DII appears only where project guidance selects a procedure implementation. A project-selected list of technology skills is shown as a selected SKILL.md set because the current definitions name those skills directly and do not promise one shared procedure name.

The skill nodes are complete for the established groups. Agent arrows show representative current invokers rather than every Agent that names each skill.

## Diagram Notation

Every concrete SKILL.md node uses +skill followed by the skill name. This identifies the skill and is not a procedure call.

A function-style member names a procedure and its parameters. An AGENTS.md DII can use this notation for a callable contract. A concrete SKILL.md node uses it only when the whole skill is one cohesive procedure.

When a skill defines several related procedures, +procedure identifies the relevant part. The member uses the exact SKILL.md section title when one exists. Otherwise, concise keywords clarify the part being used. When a relationship applies the whole named skill, the node needs no procedure member.

For example:

- +skill agent-claim identifies agent-claim/SKILL.md;
- +procedure Claim Events identifies the titled part of agent-claim used for acquiring or releasing a claim;
- +deliverWorkitem(acceptedCommit) identifies the single Deliver Workitem contract represented by an AGENTS.md DII.

## Group Designs

- [Baseline Development](skill-groups/baseline-development.md)
- [Project Setup](skill-groups/project-setup.md)
- [Documentation Methodology](skill-groups/documentation-methodology.md)
- [Backlog Management](skill-groups/backlog-management.md)
- [Concurrent Tasking](skill-groups/concurrent-tasking.md)
- [Direct Main Delivery](skill-groups/direct-main-delivery.md)
- [Review And Verification](skill-groups/review-and-verification.md)

## Definition Of Good

- **RULE: RULE-1** Each established skill group has an independent design document
  - **SYNOPSIS:** Baseline Development, Project Setup, Documentation Methodology, Backlog Management, Concurrent Tasking, Direct Main Delivery, and Review And Verification can be read and maintained separately while sharing this notation.
  - **EXAMPLE:** A reader investigating claims and feature branches can open Concurrent Tasking without processing the Backlog Management provider matrix.

- **RULE: RULE-2** Concrete skill notation identifies the skill before its relevant procedure
  - **SYNOPSIS:** Every concrete skill node uses +skill, while function style is reserved for a whole-skill procedure and +procedure identifies a titled or keyword-selected part of a multi-procedure skill.
  - **EXAMPLE:** Concurrent Tasking shows +skill agent-claim with +procedure Claim Events instead of presenting all of agent-claim as coordinateResource(claimEvent, scope).

## Authoritative Inputs

- The retained user directions for the established skill groups and their object-oriented representation.
- [Bundled Skill Inventory](../README.md)
- [Agentic Configuration](agentic-configuration.html)
- [Work-Item Provider And Completion Contracts](work-item-provider-and-completion-contracts.md)
