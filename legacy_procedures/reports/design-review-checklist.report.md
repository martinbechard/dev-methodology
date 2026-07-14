# Migration Report: Consolidated Design Review Checklist

## Source

- Procedure: [design-review-checklist.md](../design-review-checklist.md)

## Purpose And Scope

The procedure supplies a one-size-fits-many review worksheet for component,
subsystem, feature, and interface designs. It asks reviewers to rate evidence,
separate defect types, justify non-good findings, and assess responsibilities,
interactions, dependencies, extensibility, testability, consistency, errors,
state, boundaries, workflows, and cross-component data.

The live catalog has deliberately split that scope by artifact type. The
primary destinations are review-architecture, review-high-level-design, and
review-module-design, with review-structured as the common review discipline
and documentation-page-verifier as the shared source and format check. The
artifact-review-agent already composes the artifact-specific review
skills and verifier. This split is preferable to a new generic "design review"
skill because it keeps component, subsystem, and architecture criteria at the
right level of abstraction.

## Worthwhile Durable Guidance

- Review from evidence, record the assessment, and make recommendations.
- Keep the completed checklist as the audit trail; derive findings from it.
- Separate the nature of a problem from its priority, especially distinguish a
  design problem from a documentation omission.
- Check responsibility boundaries, interaction contracts, dependency direction,
  error behavior, state ownership, workflows, and verification at the scale
  appropriate to the artifact.
- Treat extension mechanisms as a cost that needs concrete likely variation,
  rather than inventing abstractions for merely possible futures.
- Require interfaces to have a focused consumer-facing purpose and an evidenced
  need, rather than using them by default.

## Mapping

| Procedure point | Destination skill(s) or agent(s) | Current coverage | Recommendation |
| --- | --- | --- | --- |
| Rate each question from evidence, document recommendations, and keep a review record | review-structured; all artifact-specific review skills; artifact-review-agent | Complete | Retain the live pass/fail/question/n/a evidence format. Do not restore emoji ratings or the broad worksheet. |
| Classify a finding as design flaw, documentation gap, architectural inconsistency, or implementation risk | review-structured; artifact-review-agent | Partial | Add an optional finding-type field to review-structured so defect type is distinct from severity. |
| Use a BECAUSE chain for a non-pass finding | review-structured | Partial | The live skill requires an assessment and a single BECAUSE in findings, but not a consequence chain. Add a concise impact statement requirement for material findings. |
| Component purpose, coherent responsibilities, and avoiding overlap | review-module-design; review-high-level-design; review-architecture | Complete | Keep in the artifact-specific checklists: module Responsibilities, HLD Constituent Components, and architecture Major Components And Ownership. |
| Communication, events, dependencies, integration contracts, and data flow | review-high-level-design; review-module-design; review-architecture | Complete | Keep in HLD Interaction Model and Data Contracts, module Public Contracts and Processing Rules, and architecture dependency/data-flow checks. |
| Dependency direction, circularity, implementation-detail coupling, and object creation | review-architecture; review-module-design | Partial | Existing checklists cover dependency direction and dependencies, but do not explicitly ask about circular dependency or dependency-inversion violations. Add focused questions to the architecture and module review checklists. Keep object-instantiation rules source-backed and project-specific. |
| Extensibility, likely variations, and YAGNI | review-module-design; review-high-level-design | Missing | Add a small, conditional extensibility/YAGNI check to both checklists: extension points need a concrete likely variation, otherwise defer the abstraction. |
| Testability, isolatable seams, mocks, and critical-path tests | review-module-design; review-high-level-design; qa-and-verification-agent | Partial | Current verification questions cover test evidence but not whether dependencies can be substituted or critical paths are practically testable. Add conditional test-seam and critical-path questions. |
| Consistency with architecture, principles, naming, and comparable components | review-structured; review-architecture; documentation-page-verifier | Partial | Add a conditional artifact-specific check for conformity with cited project conventions. Do not prescribe naming conventions in a portable skill. |
| Error scenarios, reporting, recovery, and user-visible outcomes | review-module-design; review-architecture | Complete | Keep the module Error Handling question and architecture cross-cutting-concern check; apply at HLD scope through lifecycle and interaction checks. |
| State ownership, transitions, consistency, concurrency, and race conditions | review-module-design; review-high-level-design; review-architecture | Complete | Keep the existing internal-state, lifecycle, data-anchor, data-flow, and invariant questions. |
| Subsystem boundaries, external integrations, end-to-end workflows, and cross-component data consistency | review-high-level-design; review-architecture | Complete | Keep this in HLD Scope And Non-Goals, Interaction Model, Lifecycle, Data Contracts, and Cross-Module Invariants, with architecture boundary and data-flow checks. |
| Interface purpose, consumer-oriented contracts, and only creating interfaces for real variation | review-module-design; review-high-level-design | Partial | Add a conditional contract/abstraction question: an interface must have named consumers and a concrete current or likely variation; otherwise prefer the direct concrete dependency. |
| Findings summary, critical actions, improvements, and strengths | review-structured; artifact-review-agent | Partial | Preserve findings-first and severity ordering. Do not require separate strengths or duplicated next-steps sections; recommendations belong with each finding. |

## Obsolete Or Project-Specific Guidance To Omit

- References to Object-Instantiation-Design-Directives.md and refactoring-plan.md are repository-specific and unavailable in a portable skill. A project can supply equivalent directives as review inputs.
- Mandatory event-emitter patterns, event payloads, and dependency-injection wording assume a particular architecture. Retain only the technology-neutral contract, dependency, and ownership checks.
- The component/subsystem/interface labels should not drive a single generic review workflow; live artifact-specific skills already choose a more precise review shape.
- Emoji ratings and per-section duplicated tables add form without improving the live checklist evidence model.
- A blanket requirement to list strengths and a separate next-steps list repeats the findings and recommendations already required by the current workflow.

## Precise Suggested Additions

### review-structured/SKILL.md

In the findings format, add optional fields for material findings:

- Finding type: design flaw, documentation gap, architectural inconsistency, implementation risk, or other.
- Impact: the concrete consequence if the finding remains unresolved.

State that finding type describes the problem while severity describes urgency.

### review-architecture/references/review-checklist-architecture.md

Add these artifact-specific questions:

- Does Major Layers And Dependency Direction identify and reject circular dependencies or dependencies that invert the intended layer direction?
- When abstractions or interfaces cross a major boundary, is each justified by named consumers and a concrete current or likely variation?

### review-high-level-design/references/review-checklist-high-level-design.md

Add these conditional questions:

- Where extensibility is proposed, does the design name a concrete likely variation and the narrow extension point that supports it; otherwise is the abstraction deferred?
- Do constituent-component seams and the verification plan make critical collaboration paths testable without relying on uncontrolled external dependencies?
- Does the subsystem conform to the relevant cited project architecture and interaction conventions?

### review-module-design/references/review-checklist-module-design.md

Add these conditional questions:

- Do Callers And Dependencies avoid circular dependencies and implementation-detail coupling that conflicts with the stated dependency direction?
- Where an interface or extension point is introduced, are its consumers and a concrete current or likely variation named; otherwise is a simpler concrete dependency preferred?
- Can important dependencies be substituted at a test seam, and does Verification cover the module's critical paths?
- Does the module conform to the relevant cited project conventions for names, patterns, and contracts?

## Conclusion

Do not create a replacement generic design-review skill or a new
agent. Retire the legacy worksheet in favor of the existing review stack and
artifact-review-agent. The only durable catalog improvements are a small
finding-type/impact convention in review-structured and conditional review
questions for dependency cycles, justified extensibility, interface purpose,
test seams, and cited-project consistency. All framework-specific directives
should remain local project inputs, not distributed-skill policy.
