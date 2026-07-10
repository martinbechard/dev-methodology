# Migration Report: Code Review Checklist

## Source

- [Legacy procedure](../code-review-checklist.md)

## Purpose And Scope

The procedure is a TypeScript-oriented review checklist for implementation
files. It asks a reviewer to inspect every affected file, rate each applicable
item, cite code evidence, record recommendations, and focus on recurring
patterns. Its technical criteria cover organization, imports, duplication,
complexity, coupling, domain modelling, error handling, comments, naming,
cohesion, type safety, and refactoring tests.

The live bundle has a Code Review Agent with a read-only, finding-first output
contract, plus reusable skills for cautious implementation, TypeScript, ESM,
syntax-aware discovery, and Jest or Vitest verification. It does not have a
portable code-review checklist or a Code Review Agent instruction that defines
these review dimensions.

## Worthwhile Durable Guidance

- Review from a fresh read-only context; use concrete file and line evidence.
- Evaluate recurring patterns and material risks, not isolated style nits.
- Check changed code for unnecessary duplication, mixed responsibilities,
  excessive coupling, unclear names, and misleading comments.
- Treat type weakening, unjustified assertions, and optional-value handling as
  correctness risks.
- Inspect error paths for useful context, appropriate propagation, and tests.
- Confirm refactoring preserves behavior and adds focused regression coverage
  for newly extracted behavior.
- Use repository-local architecture, module-design, naming, import, and error
  handling conventions as the authority rather than imposing a universal
  convention.

## Mapping

| Procedure point | Destination skill(s) or agent(s) | Current coverage | Recommendation |
| --- | --- | --- | --- |
| Review every changed file; use ratings, evidence, recommendations, and pattern-level findings | Code Review Agent; new code-review skill | Partial | Keep evidence and pattern discipline in a new portable review skill. Retain the agent's prioritized findings output; do not require an inline questionnaire. |
| File names, locations, co-location, and redundant files | Code Review Agent; Careful Coding; new code-review skill | Partial | Add a repository-convention check that flags deviations only when a project convention or architecture source supports it. |
| File header and design-path registry alignment | Project AGENTS.md and project-specific design/documentation rules | Missing as a portable rule | Do not put the required header or definitions registry in a distributed skill. Let the review skill require checking applicable repository-local design traceability rules. |
| Import paths, aliases, import order, unused imports, and circular dependencies | TypeScript ESM; Ast Grep; Code Review Agent; new code-review skill | Partial | Add review prompts for invalid module-boundary changes, unused imports made by the change, and cycles or layering violations. Leave exact aliases, ordering, and extension rules to the repository. |
| Duplicate algorithms, validation, and error logic; useful abstractions | Careful Coding; Code Review Agent; new code-review skill | Partial | Add a risk-based duplication check: report duplication only when it creates divergent behavior, inconsistent policy, or an unnecessary maintenance burden. |
| Long methods or classes, mixed abstraction levels, and parameter-object threshold | Careful Coding; new code-review skill | Partial | Add a cohesion and complexity prompt. Do not carry numeric line limits or a universal two-parameter-object rule. |
| Tight coupling, implementation-detail knowledge, and missing abstractions | Code Review Agent; Ast Grep; new code-review skill | Partial | Add an architectural-boundary prompt that asks whether dependencies match the documented module or layer boundaries. |
| Feature envy and excessive external getters or setters | New code-review skill | Missing | Fold this into the cohesion and ownership prompt: flag behavior that belongs with the data or component that owns the relevant invariants. |
| Primitive obsession and reusable domain types | TypeScript Strict; Code Review Agent; new code-review skill | Partial | Add explicit prompts to model recurring domain concepts, distinguish optional from nullable or missing, and avoid scattered narrowing or validation. |
| Large conditional chains and repeated type tests | New code-review skill | Missing | Add a prompt to assess whether branching is clear, exhaustive where needed, and centralized when it represents a stable domain variation. Do not prescribe polymorphism by default. |
| Error strategy, contextual messages, logging, and no exceptions for normal flow | Code Review Agent; TypeScript Strict; project-specific error rules; new code-review skill | Partial | Add a generic error-path check for propagation, recovery, actionable context, and observable failures. Keep a tracer API and logging-format requirements project-local. |
| Comment accuracy, rationale, and removal of obsolete comments | Careful Coding; new code-review skill | Partial | Add a comment check that prioritizes stale or contradictory comments, missing rationale for non-obvious decisions, and commented-out code introduced by the change. |
| Clear, consistent, non-misleading names | Code Review Agent; new code-review skill | Partial | Add a naming prompt oriented to domain meaning, public contracts, and ambiguity that affects maintenance or correctness. |
| Class responsibility and method cohesion against design intent | Code Review Agent; project-specific designs; new code-review skill | Partial | Add a responsibility-boundary check based on the applicable design or repository architecture. |
| Optional-to-required assignments, assertions, and canonical type imports | TypeScript Strict; TypeScript ESM; Code Review Agent | Partial | Expand TypeScript Strict with review-specific wording for assertion justification, boundary validation, and semantic optionality. Keep canonical import locations project-local. |
| Design consistency while applying current changes | Code Review Agent; project-wiki-query; QA And Verification Agent | Partial | Add an agent instruction to identify the authoritative change intent before reviewing and report unresolved intent as an open question. |
| Tests for behavior extracted during refactoring, preferably first | Careful Coding; Jest; Vitest; QA And Verification Agent | Partial | Add a review prompt requiring focused tests for extracted or changed behavior and asking whether tests prove the contract rather than the implementation shape. Do not require historical proof that TDD occurred unless a project explicitly records it. |

## Obsolete Or Project-Specific Guidance To Omit

- A mandatory Design header in every TypeScript file and the exact link syntax.
- The definitions document as a universal registry for code paths, types,
  interfaces, and enums.
- Required PascalCase file names for every class or interface, exact standard
  folders, mirrored test folders, and specific alias prefixes.
- A blanket ban on TypeScript or JavaScript file extensions in imports; ESM
  projects may require explicit extensions.
- Universal thresholds of 30 to 40 method lines, 300 class lines, or a
  parameter object whenever there are more than two parameters.
- The named Tracer API and its variable-name logging format.
- A prescribed error-strategy path and the reference to the coding-rules
  procedure.
- The duplicated Testing heading and the expectation that a reviewer can prove
  the order in which tests and refactoring were performed.

## Precise Suggested Additions

### New Portable Skill: Code Review

Create a code-review skill and add it to the Code Review Agent. It should
instruct the reviewer to:

1. Read the diff, changed-file context, applicable tests, and repository-local
   instructions or design sources before reaching conclusions.
2. Report only material findings, ordered by severity, with a tight file
   location, concrete evidence, impact, and actionable correction.
3. Review changed paths for behavior regressions, contract changes, type and
   nullability weakening, error-path behavior, security or trust-boundary
   effects when applicable, dependency or ownership drift, and missing focused
   tests.
4. Use architecture and style conventions only when they are documented in the
   repository; identify absent or contradictory guidance as an open question.
5. Treat duplication, size, conditionals, comments, and naming as findings
   only when they obscure behavior, violate a documented boundary, or create a
   credible maintenance or correctness risk.
6. Finish with open questions and residual risk, matching the existing agent
   output contract.

### TypeScript Strict

Add a review-oriented paragraph: inspect assertions and boundary values; require
validation and narrowing for real unknown input; preserve the semantic
distinction between absent, optional, nullable, and defaulted values; and flag
type changes that weaken public contracts without evidence or tests.

### TypeScript ESM

Add a review-oriented paragraph: verify that changed imports respect the
project's declared module-resolution and extension policy, do not create
cycles or unintended runtime dependencies, and preserve type-only versus
runtime import boundaries.

### Code Review Agent

Add the new code-review skill to the role. Its instructions should explicitly
require the reviewer to identify the authoritative intent and applicable
repository conventions before review, then distinguish confirmed defects from
questions caused by missing project guidance.

## Conclusion

Retire this procedure as a standalone universal checklist. Preserve its
evidence-based, pattern-focused code-quality review method in a new portable
code-review skill, routed through the existing Code Review Agent. Strengthen
TypeScript Strict and TypeScript ESM with narrow review guidance. Keep all
specific design registries, headers, folder layouts, import syntax, tracing
APIs, and numeric thresholds in the target repository's AGENTS.md or local
procedures rather than distributing them across projects.
