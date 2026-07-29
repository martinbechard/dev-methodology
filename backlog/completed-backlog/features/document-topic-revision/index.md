# Integrate Document Topic Editing and Revise the Methodology Documents

## Goal

Integrate one conceptual document-topic editor and two distributed topic skills into the methodology bundle, then use that capability to analyze and revise every current top-level design HTML document.

## Purpose

Separate read-only topic analysis from source mutation. The analysis phase must reconstruct and score a document's topic hierarchy from source evidence. The revision phase must apply accepted structural changes without losing content, breaking navigation, or hand-editing generated mirrors.

## Current Anchors

- .agents/skills/create-document-outline/SKILL.md contains the current project-local topic analysis and scoring procedure.
- .agents/skills/improve-document-outline/SKILL.md contains the current project-local improvement procedure.
- /private/tmp/agentic-configuration-topic-outline-source-grounded-v13.md records the most recent independent source-grounded test result.
- design contains ten current top-level HTML documents.
- PROJECT.yaml and AGENTS.md require exact approval evidence before governed agent or skill definitions change.

## Non-Goals

- Do not perform document revisions as part of backlog creation.
- Do not treat a generated HTML mirror as an independently authored source.
- Do not combine all document revisions into one implementation transaction.
- Do not increase alignment scores by creating artificial parents, suppressing topics, or inventing sequence relationships.

## Definition of Good

- The bundle provides a clearly named read-only analyze-document-topics skill and a mutation-capable revise-document-topics skill.
- A dedicated conceptual document-topic editor loads both skills and uses the documentation model profile at high Codex reasoning effort.
- Each design document has an independently dispatchable revision item.
- Every revision starts from a source-grounded scored outline, preserves complete topic coverage, and records why each structural change improves the document.
- Generated surfaces are revised through their owning source and generator.
- Documentation, generated adapters, catalogs, evaluations, tests, and links remain current.

## Recommended Order

1. [Incorporate the Document Topic Editor and Topic Skills](../incorporate-document-topic-agent-and-skills.md)
2. Revise the catalog and generated-view documents:
   - [Core Agent and Skills](revise-agent-and-skill-definitions-topics.md)
   - [Agent and Skill Evaluations](../revise-agent-and-skill-evaluations-topics.md)
   - [Agent and Skill Wiring Map](../revise-agent-skill-explorer-topics.md)
3. Revise the explanatory methodology documents:
   - [Examples](revise-agent-skill-specialization-examples-topics.md)
   - [Agentic Configuration](../revise-agentic-configuration-topics.md)
   - [Documentation Templates](../revise-documentation-templates-topics.md)
   - [Generic Agent Definitions Source](revise-generic-agent-definitions-source-topics.md)
   - [Orchestrated Development Lifecycle](revise-orchestrated-development-lifecycle-topics.md)
   - [Technology Skills](revise-skills-modularization-topics.md)
   - [Wiki Skills and Project Context](revise-wiki-skills-and-project-context-topics.md)

## Coordination

Every document-revision child depends on the integration item so it runs with the final distributed skills and conceptual agent. The evaluation-page child also depends on the existing generator-baseline defect. The lifecycle and agentic-configuration children also depend on the active coordination-policy defect because that work changes both documents.
