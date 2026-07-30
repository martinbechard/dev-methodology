# Object-Oriented Skill Group Models

## Scope

This index applies the reusable [Object-Oriented Analysis Of Agents And Skills](object-oriented-agent-and-skill-model.md) to the established methodology skill groups.

Each group has its own document. Every group document contains:

- a current-state class diagram of the Agent, AGENTS.md, and SKILL.md relationships;
- a proposed-state class diagram that applies the recommendations while retaining the same relationship view;
- the current SKILL.md headings that act as procedure boundaries in that view; and
- one recommendation for every skill whose primary home is that group.

The seven group documents cover forty-one current skills. Each skill has one primary group. A repeated skill outside its primary group is marked Cross-group.

The current diagrams describe the current definitions. The proposed diagrams visualize the possible definition improvements described by the recommendations. Neither a proposed diagram nor a recommendation changes a skill or claims that the recommended interface already exists.

Each recommendation uses one or both of the requested improvement forms: a clearer operation-shaped skill name, or procedure headings that give invokers and alternative implementations consistent interface vocabulary. “Keep the skill name” means that only heading changes are recommended.

## Diagram Notation

The applied diagrams use the relationship conventions from the analysis method:

- A SKILL.md node in a Current Design displays the exact current kebab-case skill name.
- An empty SKILL.md node means that the relationship loads the whole skill.
- A method-like member in a Current Design represents a procedure found under the named current heading. Generic members such as workflow() are intentionally preserved when the source heading is generic.
- A regular arrow points from an invoker to a procedure it knows without naming the implementing skill.
- An open-diamond arrow points from a definition or SKILL.md that knows the exact referenced skill name.
- A dotted arrow is conditional. Its label states the condition.
- A solid arrow is unconditional and carries no label.
- A solid-diamond line is used only for skill-group and subgroup containment. It is not a loading relationship.
- An AGENTS.md node exposes the procedure wording that project guidance maps to a selected skill.

Mermaid sometimes needs an internal identifier when a visible name contains a wildcard. The visible class label remains the analysis identity. For example, the CreateWorkItem node is displayed as create-*-work-item.

Each Proposed Design applies the recommendations with a second visual convention:

- A gold SKILL.md node has a proposed skill-name change.
- Its renamed-from member records the current exact name, so the change remains identifiable without relying on color.
- A neutral SKILL.md node keeps its current skill name. Its method-like members show proposed procedure headings.
- A repeated gold Cross-group node represents the same proposed rename shown in the skill’s primary group, not a second recommendation.
- AGENTS.md procedure-family labels and relationship endpoints use the proposed vocabulary needed to reference the proposed skills.

## Group Designs

- [Baseline Development](skill-groups/baseline-development.md)
- [Project Setup](skill-groups/project-setup.md)
- [Documentation Methodology](skill-groups/documentation-methodology.md)
- [Backlog Management](skill-groups/backlog-management.md)
- [Concurrent Tasking](skill-groups/concurrent-tasking.md)
- [Direct Main Delivery](skill-groups/direct-main-delivery.md)
- [Review And Verification](skill-groups/review-and-verification.md)

## Definition Of Good

- **RULE: RULE-1** Each established skill group has independent current and proposed designs
  - **SYNOPSIS:** A reader can inspect one responsibility boundary and compare its current and recommended organization without loading the other six groups.
  - **EXAMPLE:** Concurrent Tasking contains paired diagrams for resource coordination and feature-branch delivery without repeating the Backlog Management provider matrix.

- **RULE: RULE-2** Every primary skill receives one source-backed improvement recommendation
  - **SYNOPSIS:** A recommendation either improves the skill name or introduces procedure headings that can become stable interface vocabulary.
  - **EXAMPLE:** create-gitlab-work-item keeps its current name but receives a proposed Create Work Item heading because its current entry procedure is only named Workflow.

- **RULE: RULE-3** Current and recommended vocabulary remain visibly separate
  - **SYNOPSIS:** Current Design shows current names and headings, while Proposed Design shows the vocabulary recommended by the table.
  - **EXAMPLE:** The Backlog Management current diagram shows workflow() for create-gitlab-work-item, while its proposed diagram shows create-work-item().

- **RULE: RULE-4** Every proposed skill-name change is identifiable by color and text
  - **SYNOPSIS:** A gold node distinguishes a proposed name from unchanged names, and renamed-from preserves the current identity for readers who do not rely on color.
  - **EXAMPLE:** The proposed Concurrent Tasking diagram highlights integrate-agent-work and records renamed-from agent-work-merge inside the same node.

## Authoritative Inputs

- The retained user directions for the established skill groups and their object-oriented representation.
- The forty-one SKILL.md files linked from the seven group documents.
- The conceptual Agent definitions linked from the seven group documents.
- [Bundled Skill Inventory](../README.md)
- [Agentic Configuration](agentic-configuration.html)
- [Work-Item Provider And Completion Contracts](work-item-provider-and-completion-contracts.md)
