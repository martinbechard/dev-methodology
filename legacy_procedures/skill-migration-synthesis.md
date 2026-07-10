# Legacy Procedure Migration Synthesis

## Scope And Method

This page consolidates one independent migration report for each of the 27
legacy procedures. Each report compared its procedure with the live portable
skill catalog and canonical roles, then separated reusable guidance from
former-project conventions. The legacy procedures remain source material; this
page makes recommendations only and does not change the distributed skills.

## Decision Summary

Retire the procedures as standalone portable workflows. Most of their useful
content fits as small, evidence-based additions to existing skills. Create a
small number of focused skills only where the catalog has no coherent current
home:

| Priority | Recommendation | Intended role routing | Evidence |
| --- | --- | --- | --- |
| High | Create Code Review for evidence-based, risk-focused code review. | Code Review Agent | [report](reports/code-review-checklist.report.md) |
| High | Create Test-Driven Development for framework-neutral red-green-refactor work. | Coding Agent and QA And Verification Agent | [report](reports/procedure-TDD-rules.report.md) |
| High | Create Code Execution Tracing for source-level path, branch, nesting, and state tracing. | Coding Agent and QA And Verification Agent | [report](reports/procedure-code-tracing.report.md) |
| High | Create Root Cause Analysis, including test-failure diagnosis before patching. | QA And Verification Agent and Runtime Diagnostician; selectively Coding Agent | [old procedure report](reports/procedure-root-cause-analysis-old.report.md), [current procedure report](reports/procedure-root-cause-analysis.report.md) |
| Medium | Create Runtime Trace Instrumentation for opt-in, safe, bounded runtime evidence collection. Keep it distinct from execution tracing. | Runtime Diagnostician, Coding Agent, and QA And Verification Agent | [report](reports/procedure-tracer.report.md) |
| Medium | Create Unit Test Plan, with a small template, for durable design- or code-derived test-plan artifacts. | Development Methodology route; Coding, QA, and Code Review roles | [design-derived report](reports/procedure-unit-test-plan-from-design.report.md), [code-derived report](reports/procedure-unit-test-plan-from-code.report.md) |

No new canonical agent is recommended. The existing role model already has
appropriate owners; new skills should be routed to those roles rather than
creating narrowly named agents.

## Targeted Improvements To Existing Skills

- Careful Coding: project-intent checks, refactoring evidence and rollback
  discipline, parameter-object and conditional-complexity choices, comment
  hygiene, and portable error-handling guidance.
- Review Structured: explicit correction and authority for each finding,
  impact-based severity, finding type, review-of-review handling, and selected
  design checks for circularity, test seams, and justified extensibility.
- Jest and Vitest: integration-scenario evidence, deterministic stateful
  dependency cleanup, mock-selection and complex-double guidance, test-plan
  reconciliation, and configuration-derived import guidance.
- Create Functional Spec and Review Functional Spec: optional scenario coverage,
  cross-representation consistency, and project-aware approval traceability.
- Documentation Reverse Engineering: conditional source-backed data lineage
  across important module, persistence, serialization, external, security, or
  UI boundaries.
- Structured Design, Create Module Design, and the module-design template:
  process-boundary and transform/dispatch ownership, optional context diagrams,
  and explicit test seams, fixtures, and boundary doubles.
- Manage Backlog: child-to-series status rollup guidance.
- Maintain Methodology Documentation and the architecture template: review
  catalog alignment plus portable stack-decision and configuration-validation
  prompts.

## What Stays Project-Local

Do not transfer fixed paths, filenames, directory trees, approved technology
lists, product-domain models, mandatory tool commands, global Tracer/log files,
numeric thresholds, legal headers, status-file mechanics, or blanket rules
about timers and test order. Preserve those in the owning repository's
AGENTS.md, architecture/design documents, and local procedures when still
needed.

## Procedure Reports

| Legacy procedure | Independent analysis report | Consolidated disposition |
| --- | --- | --- |
| [Code review checklist](code-review-checklist.md) | [Report](reports/code-review-checklist.report.md) | New Code Review skill |
| [Design review checklist](design-review-checklist.md) | [Report](reports/design-review-checklist.report.md) | Improve Review Structured |
| [Design review feedback guidelines](design-review-feedback-guidelines.md) | [Report](reports/design-review-feedback-guidelines.report.md) | Improve Review Structured |
| [TDD rules](procedure-TDD-rules.md) | [Report](reports/procedure-TDD-rules.report.md) | New Test-Driven Development skill |
| [Apply refactoring plan](procedure-apply-refactoring-plan.md) | [Report](reports/procedure-apply-refactoring-plan.report.md) | Improve existing coding, QA, and role guidance |
| [Code tracing](procedure-code-tracing.md) | [Report](reports/procedure-code-tracing.report.md) | New Code Execution Tracing skill |
| [Coding rules](procedure-coding-rules.md) | [Report](reports/procedure-coding-rules.report.md) | Improve Careful Coding |
| [Create trading-workflow integration tests](procedure-create-integration-tests-for-trading-workflow.md) | [Report](reports/procedure-create-integration-tests-for-trading-workflow.report.md) | Improve Jest, Vitest, and QA guidance |
| [Create procedure](procedure-create-procedure.md) | [Report](reports/procedure-create-procedure.report.md) | Improve Structured Design |
| [Create requirements](procedure-create-requirements.md) | [Report](reports/procedure-create-requirements.report.md) | Already covered; no change |
| [Create usage scenarios](procedure-create-usage-scenarios.md) | [Report](reports/procedure-create-usage-scenarios.report.md) | Improve functional-spec creation and review |
| [Data lineage](procedure-data-lineage.md) | [Report](reports/procedure-data-lineage.report.md) | Improve Documentation Reverse Engineering |
| [Design review](procedure-design-review.md) | [Report](reports/procedure-design-review.report.md) | Improve review maintenance and feedback guidance |
| [Development standards](procedure-dev-standards.md) | [Report](reports/procedure-dev-standards.report.md) | Existing roles plus TDD skill |
| [Document code design](procedure-document-code-design.md) | [Report](reports/procedure-document-code-design.report.md) | Improve module-design materials |
| [Document new design](procedure-document-new-design.md) | [Report](reports/procedure-document-new-design.report.md) | Improve module-design materials |
| [Generate unit tests](procedure-gen-unit-tests.md) | [Report](reports/procedure-gen-unit-tests.report.md) | Improve Jest and role guidance |
| [Generate workflow integration tests](procedure-gen-workflow-int-test.md) | [Report](reports/procedure-gen-workflow-int-test.report.md) | Improve Jest, Vitest, and QA guidance |
| [Mocking rules](procedure-mocking-rules.md) | [Report](reports/procedure-mocking-rules.report.md) | Improve Jest, Vitest, and review guidance |
| [Process design](procedure-process-design.md) | [Report](reports/procedure-process-design.report.md) | Improve structured and module design |
| [Root-cause analysis, old](procedure-root-cause-analysis-old.md) | [Report](reports/procedure-root-cause-analysis-old.report.md) | New Root Cause Analysis skill |
| [Root-cause analysis](procedure-root-cause-analysis.md) | [Report](reports/procedure-root-cause-analysis.report.md) | New Root Cause Analysis skill |
| [Status-tracking rules](procedure-status-tracking-rules.md) | [Report](reports/procedure-status-tracking-rules.report.md) | Improve Manage Backlog |
| [Technical-stack rules](procedure-technical-stack-rules.md) | [Report](reports/procedure-technical-stack-rules.report.md) | Improve Jest and architecture template |
| [Tracer](procedure-tracer.md) | [Report](reports/procedure-tracer.report.md) | New Runtime Trace Instrumentation skill |
| [Unit-test plan from code](procedure-unit-test-plan-from-code.md) | [Report](reports/procedure-unit-test-plan-from-code.report.md) | New Unit Test Plan skill when artifact is needed |
| [Unit-test plan from design](procedure-unit-test-plan-from-design.md) | [Report](reports/procedure-unit-test-plan-from-design.report.md) | New Unit Test Plan skill and template |

## Recommended Implementation Order

1. Decide the six proposed skill names and boundaries, especially the three
   distinct diagnostic skills: Root Cause Analysis, Code Execution Tracing, and
   Runtime Trace Instrumentation.
2. Add the six skills, their Codex metadata, role routing, catalog tests,
   generated adapters, README inventory, and affected design HTML together.
3. Apply the targeted additions to existing skills and templates in one
   follow-up change, avoiding duplicated rules between the new skills and
   runner-specific material.
4. Refresh shared installs and run the repository's complete bundle validation
   suite before retiring or archiving the legacy procedures.
