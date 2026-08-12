# HTML Documentation Review and Design Alignment

## Goal

Review and correct the complete text content of every maintained user-facing HTML documentation page, then align each accepted page with the adopted Documentation Design System without allowing visual migration to conceal or reshape unresolved content defects.

## Scope

This series covers the root toolkit index and the ten top-level design documents linked from the maintained documentation set. It excludes the Documentation Design System reference pages that define the standard, the styled backlog-report example, evaluation fixtures, browser fixtures, document-provenance fixtures, and sample pages.

Generated pages remain generator-owned. A child item must identify and change the authoritative source or generator rather than hand-edit a generated projection.

## Source Evidence

The user requested on 2026-08-09 in canonical task 019fb057-1767-7ef2-b5fa-41f4417b20b3 that all HTML documentation be reviewed and corrected now that the Documentation Design System and terminology-aware writing and review skills exist. The user explicitly required separate text-review items for each page followed by separate design-alignment items, because design adjustment is not useful before the text is correct.

The completed Work Item integrate-documentation-design-system records that existing HTML migration was intentionally excluded and requires separate work. README.md confirms that the existing hand-authored pages were not migrated.

## Workflow

1. Complete each page-specific text review and correction against authoritative repository sources, the Terminology Standard, and applicable writing methodology.
2. Obtain independent acceptance of the corrected content.
3. Move only that page's dependent design-alignment item from Blocked to Ready.
4. Apply the Documentation Design System through the page's authoritative source or generator without changing accepted meaning.
5. Verify page-type conformance, accessibility, responsive behavior, navigation, links, and browser behavior independently.

Pages may proceed independently. A design-alignment item may not start merely because another page's text review completed.

## Text Review Items

- [Review AI-Assisted Coding Toolkit Index Text](../../completed-backlog/features/review-index-page-text.md)
- [Review Conceptual Agent and Skill Definitions Text](../../completed-backlog/features/review-agent-and-skill-definitions-text.md)
- [Review Agent and Skill Evaluations Text](../../completed-backlog/features/review-agent-and-skill-evaluations-text.md)
- [Review Agent-Owned Evaluation Suites Text](../../completed-backlog/features/review-agent-owned-evaluation-suites-text.md)
- [Review Agent and Skill Specialization Examples Text](../../completed-backlog/features/html-documentation-review-and-design-alignment/review-agent-skill-specialization-examples-text.md)
- [Review Coding-Agent Runtime Configuration Text](../../completed-backlog/features/review-agentic-configuration-text.md)
- [Review Documentation Templates Text](../../completed-backlog/features/review-documentation-templates-text.md)
- [Review Generic Agent Definitions Source Text](../../completed-backlog/features/review-generic-agent-definitions-source-text.md)
- [Review Orchestrated Development Lifecycle Text](../../completed-backlog/features/html-documentation-review-and-design-alignment/review-orchestrated-development-lifecycle-text.md)
- [Review Agent Skill Architecture Text](../../completed-backlog/features/html-documentation-review-and-design-alignment/review-skills-modularization-text.md)
- [Review Wiki Skills and Project Context Text](../../completed-backlog/features/html-documentation-review-and-design-alignment/review-wiki-skills-and-project-context-text.md)

## Design Alignment Items

- [Align AI-Assisted Coding Toolkit Index with the Documentation Design System](align-index-page-with-documentation-design-system.md)
- [Align Conceptual Agent and Skill Definitions with the Documentation Design System](align-agent-and-skill-definitions-with-documentation-design-system.md)
- [Align Agent and Skill Evaluations with the Documentation Design System](align-agent-and-skill-evaluations-with-documentation-design-system.md)
- [Align Agent-Owned Evaluation Suites with the Documentation Design System](align-agent-owned-evaluation-suites-with-documentation-design-system.md)
- [Align Agent and Skill Specialization Examples with the Documentation Design System](align-agent-skill-specialization-examples-with-documentation-design-system.md)
- [Align Coding-Agent Runtime Configuration with the Documentation Design System](align-agentic-configuration-with-documentation-design-system.md)
- [Align Documentation Templates with the Documentation Design System](align-documentation-templates-with-documentation-design-system.md)
- [Align Generic Agent Definitions Source with the Documentation Design System](align-generic-agent-definitions-source-with-documentation-design-system.md)
- [Align Orchestrated Development Lifecycle with the Documentation Design System](../../completed-backlog/features/html-documentation-review-and-design-alignment/align-orchestrated-development-lifecycle-with-documentation-design-system.md)
- [Align Agent Skill Architecture with the Documentation Design System](align-skills-modularization-with-documentation-design-system.md)
- [Align Wiki Skills and Project Context with the Documentation Design System](align-wiki-skills-and-project-context-with-documentation-design-system.md)

## Definition of Good

- All visible prose, labels, tables, diagram text, alternate text, accessible names, and navigation wording are accurate, complete, current, source-backed, terminology-aligned, and independently accepted.
- Every page then conforms to the appropriate Documentation Design System page-type and cross-cutting checklists without semantic drift.
- Generated pages are rebuilt from authoritative sources and pass freshness checks.
- The root index and all detail pages retain coherent information ownership, sequence navigation, settings behavior, and source traceability.
- Excluded fixtures, examples, and design-system reference pages remain unchanged unless a focused failure proves a direct dependency and receives separate scope.
