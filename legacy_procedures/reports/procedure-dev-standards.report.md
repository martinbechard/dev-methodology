# Development Standards Migration Report

## Source

Source procedure: [procedure-dev-standards.md](../procedure-dev-standards.md)

## Purpose And Scope

This legacy document is an umbrella policy that routes implementation work to
test, mock, coding, design, review, planning, and procedure-authoring rules.
Its lasting value is a small set of cross-cutting expectations: establish the
applicable project context, make changes intentional and explainable, use the
right design and verification route, and maintain visible task ownership.

It should not become a single distributed development-standards skill. The
current bundle intentionally separates durable capabilities by artifact,
runtime, and responsibility; a universal policy would duplicate their routing
and force unrelated instructions into ordinary coding work.

## Durable Guidance Worth Keeping

- Read the applicable repository instructions, requirements, contracts,
  designs, and procedures before changing behavior; reconcile or escalate a
  conflict rather than silently choosing one source.
- Make each implementation, fix, or refactor traceable to an intended effect,
  its supporting requirement or design, and proportionate verification.
- For design-led work, create the smallest appropriate design artifact before
  implementation and use it to identify meaningful verification scenarios.
- Review designs before implementation when a design artifact is required, and
  use changed-scope code review and verification for implementation work.
- Keep task planning, current status, dependencies, blockers, and handoff
  information visible in a project-selected system.
- Use repository-appropriate code discovery tools and inspect the resulting
  source before relying on a search result as evidence.

## Mapping To The Current Catalog

| Procedure point | Destination | Coverage | Recommendation |
| --- | --- | --- | --- |
| Read all applicable project procedures and standards before acting | [Coding Agent](../../agents/roles/development-use/coding-agent.role.yaml), [careful-coding](../../skills/careful-coding/SKILL.md), and the artifact-creation skills | Partial | Preserve the source-first rule, but scope it to instructions and artifacts relevant to the request. Add a short explicit repository-context check to the general implementation route if it is not already supplied by local AGENTS instructions. Do not require recursive reading of every procedure. |
| Follow TDD, mock consistently, run focused then proportionate broader verification | [jest](../../skills/jest/SKILL.md), [vitest](../../skills/vitest/SKILL.md), [QA And Verification Agent](../../agents/roles/development-use/qa-and-verification-agent.role.yaml), and the TDD migration route | Partial | Retain the behavior-first and boundary-mocking principles. The runner skills cover testing details, while the cross-framework red-green-refactor workflow remains a catalog-level gap already identified by the dedicated TDD procedure review. |
| Apply coding standards | [careful-coding](../../skills/careful-coding/SKILL.md), stack-specific skills, and repository-local AGENTS instructions | Partial by design | Keep portable change-discipline in Careful Coding and technology conventions in their stack skills. Keep language, naming, formatting, directory layout, and tool-specific rules in the target repository rather than creating a generic coding-standards skill. |
| Explain intended effect, desirability, robustness, and alignment with requirements or design | [careful-coding](../../skills/careful-coding/SKILL.md), [fix-explanation](../../skills/fix-explanation/SKILL.md), and [structured-explanation](../../skills/structured-explanation/SKILL.md) | Partial | Strengthen the general implementation handoff so a material change names intended behavior, upstream source when one exists, and verification evidence. Use Fix Explanation only when the user asks for a formal explanation of a fix or patch. |
| Use the approved technical stack | Target-repository AGENTS instructions, project configuration, and [documentation-reverse-engineering](../../skills/documentation-reverse-engineering/SKILL.md) | Correctly project-specific | Do not migrate a fixed stack rule into this reusable bundle. The repository owns permitted dependencies and runtime choices; architecture and source inspection establish those facts. |
| Create a design before code when requirements require one | [development-methodology](../../skills/development-methodology/SKILL.md), [create-functional-spec](../../skills/create-functional-spec/SKILL.md), [create-architecture](../../skills/create-architecture/SKILL.md), [create-high-level-design](../../skills/create-high-level-design/SKILL.md), and [create-module-design](../../skills/create-module-design/SKILL.md) | Covered | Retain current document-type selection. It is more precise than one generic new-design procedure. |
| Derive a unit-test plan from the design | The proposed cross-framework TDD route, Jest or Vitest, and [QA And Verification Agent](../../agents/roles/development-use/qa-and-verification-agent.role.yaml) | Partial | Preserve lightweight scenario planning tied to intended behavior. A formal test-plan artifact is not currently a general methodology type; introduce one only if users repeatedly need a durable, reviewable plan beyond the TDD skill's scenario list. |
| Conduct design reviews | [review-functional-spec](../../skills/review-functional-spec/SKILL.md), [review-architecture](../../skills/review-architecture/SKILL.md), [review-high-level-design](../../skills/review-high-level-design/SKILL.md), [review-module-design](../../skills/review-module-design/SKILL.md), and [Artifact Review Agent](../../agents/roles/development-use/artifact-review-agent.role.yaml) | Covered | Keep artifact-specific review and completed-checklist evidence. Do not restore one generic review procedure as the primary route. |
| Plan work and track status, dependencies, and blockers | [manage-backlog](../../skills/manage-backlog/SKILL.md), [create-backlog](../../skills/create-backlog/SKILL.md), and [Development Orchestrator](../../agents/roles/development-use/development-orchestrator.role.yaml) | Partial | Retain visible, project-selected planning and blocker tracking. Keep file names, status vocabulary, cadence, and escalation thresholds local to each project. |
| Create and maintain procedures consistently | Repository AGENTS instructions and [structured-design](../../skills/structured-design/SKILL.md) | Partial | Keep a repository-maintenance procedure only where the repository owns such documents. A portable procedure-authoring skill is not justified unless procedures are a supported artifact type across target projects. |
| Use root-anchored wiki-style links between Markdown files | Existing Markdown links and project-local documentation conventions | Not portable | Omit. Link syntax, repository root conventions, and documentation tooling are project-specific; the legacy double-bracket syntax is not a distributed-skill rule. |
| Locate TypeScript types, interfaces, and classes with grep after consulting definitions.md | [ast-grep](../../skills/ast-grep/SKILL.md) and [documentation-reverse-engineering](../../skills/documentation-reverse-engineering/SKILL.md) | Superseded | Retain the intent—find definitions efficiently and read the source—but route plain-text queries to rg and structural queries to ast-grep. Do not retain grep-only commands, a src-only assumption, or a required definitions.md registry. |

## Recommendations

- Do not add a Development Standards skill or a dedicated standards agent. The
  document is a router, and the existing Coding Agent, QA And Verification
  Agent, Documentation Architect, and Artifact Review Agent already provide
  the relevant ownership boundaries.
- Make one modest cross-cutting improvement to Careful Coding or the Coding
  Agent: before material implementation, inspect applicable project guidance
  and upstream intent; at handoff, state the intended effect and verification
  evidence. This complements rather than replaces repository-local rules.
- Adopt the separate recommendation for one framework-neutral Test-Driven
  Development skill. It should own the behavior-to-scenario-to-verification
  loop and delegate runner and mock details to Jest, Vitest, Playwright, or
  project-specific skills.
- Keep formal test-plan documents optional. Add a dedicated test-planning
  artifact or skill only after repeated evidence that a lightweight TDD
  scenario list cannot meet review, compliance, or coordination needs.
- Keep technical stack selection, exact task-status mechanics, documentation
  link syntax, and any procedure-authoring template in project-local guidance
  unless a future cross-project use case proves them portable.

## Guidance To Omit Or Narrow

- Omit recursive reading of every mentioned procedure. It creates avoidable
  context loading and ignores relevance; inspect the governing and task-local
  sources instead.
- Omit the instruction tied to a particular read_file tool and its visibility
  model. Tool behavior is runtime-specific.
- Omit the compulsory completion phrase and a list of every file read. Report
  material sources and verification evidence naturally when they matter to the
  request.
- Omit fixed wiki-link syntax, absolute-root assumptions, grep commands, and
  a definitions.md prerequisite. These are former-project conventions.
- Omit periodic-review wording as a distributed operational rule. Repository
  owners may schedule maintenance through their own governance and backlog
  practices.
