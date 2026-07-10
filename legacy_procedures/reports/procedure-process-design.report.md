# Migration Report: Process Design

## Source

- [Legacy procedure](../procedure-process-design.md)

## Purpose And Scope

The procedure directs an author to create a separate process-design document
from a former serialization example. It favors a top-down decomposition from
one entry function, explicit inputs and outputs, small child functions,
event dispatch, transformational structure, error handling, and detailed
pseudocode explanations.

The current bundle already separates process-level component design from
architecture, and provides the right durable destinations: Structured Design
for an explicit process or function structure; Create Module Design for one
implementation unit; and Create High-Level Design where the process crosses
several components. The module-design template and its review checklist
already require contracts, processing rules, errors, and verification. The
legacy serialization example is not present in the live design directory, so
it cannot remain an authoritative dependency.

## Worthwhile Durable Guidance

- Start a process design with a clear entry process or public operation and
  decompose only as far as a reader needs to implement and test without
  guessing.
- State representative inputs, outputs, validation expectations, side effects,
  and failure outcomes at each public or cross-component boundary.
- Make the main path, meaningful branches, retries, early exits, and recovery
  behavior explicit.
- Keep a transformational step aligned with the structure of the input it
  transforms so ownership and partial-failure behavior are visible.
- Give each stable event-dispatch case a named handler and identify the event
  owner and resulting contract.
- Keep a child operation cohesive: it should normally express a small related
  set of business rules rather than merely moving lines into another name.
- Use pseudocode selectively when prose and a diagram cannot make ordering,
  branching, or recovery behavior unambiguous.

## Mapping And Coverage

| Procedure point | Destination skill(s) or agent(s) | Current coverage | Recommendation |
| --- | --- | --- | --- |
| Create a process design in its own document | Structured Design; Create Module Design; Create High-Level Design | Complete | Route by scope: module for one implementation unit, high-level design for a multi-component process, and structured design for a custom process artifact. Do not require a process-specific filename. |
| Begin with one topmost function and decompose downward | Structured Design; Create Module Design | Partial | Add an optional process-decomposition rule to Structured Design that asks for one named entry process and named child responsibilities when the document is explaining a complex flow. |
| Describe function inputs and outputs with examples and rationale | Create Module Design; module-design template; Structured Design | Partial | The template requires contract inputs and outputs, but not representative values. Add representative examples and their rationale for public, persisted, external, or otherwise ambiguous boundaries; do not require examples for trivial internal helpers. |
| Cover each possible input type or caller-provided variant | Create Module Design; High-Level Design data contracts | Partial | Require documented supported variants, validation, and failure behavior where a union, event family, external payload, or caller contract makes variants material. Avoid an impossible universal enumeration of every runtime value. |
| Structure transformations to mirror input structure | Structured Design; module-design template Processing Rules | Partial | Add a prompt to name transformation stages by the source structure they own, and to state aggregation, ordering, and partial-failure rules where applicable. |
| Dispatch by event with a child handler for every event type | Create Module Design; High-Level Design Interaction Model and Data Shapes And Contracts | Partial | Add guidance to document the dispatch owner, supported events, exhaustive or fallback behavior, and named handler responsibility. Do not prescribe a language-level switch statement. |
| Recursively split functions into one to three business rules | Structured Design; Careful Coding | Partial | Preserve cohesion and business-rule clarity, but not a numeric rule count. Require further decomposition only when it improves a contract, decision boundary, reuse boundary, or testability. |
| Step-by-step pseudocode with reasons, interactions, and errors | Structured Design; module-design template; review-module-design | Partial | Keep source-backed processing rules, interactions, and error handling. Permit concise pseudocode where it adds precision; retain Structured Design assertions as the default format. |

## Obsolete Or Project-Specific Guidance To Omit

- The dependency on design/markdown-serialization-examples.md. That asset is
  absent, and a distributed process-design method should not rely on an
  undocumented serialization notation.
- The prescribed design/<process name>-process.md path and filename.
- The exact PROCEDURE, END PROCEDURE, indentation, capitalization, and nested
  BECAUSE formatting. Structured markdown is the current portable format.
- A mandatory BECAUSE chain after every action. Reasons should accompany
  decisions and non-obvious constraints, not mechanically repeat every step.
- A universal one-to-three-business-rules limit, universal recursive depth, and
  a required child function for every event type. These are implementation
  choices that vary by language, codebase, and actual complexity.
- The malformed example wording and fixed five-level explanation depth.

## Precise Suggested Additions

### Structured Design

Add this paragraph under Component Design Rules:

> When a component design explains a complex process, name the entry process
> and nest the responsibilities or child operations that it invokes. For every
> public, persisted, external, or ambiguous boundary, state the supported
> input or event variants, representative input and output examples where they
> clarify the contract, validation, side effects, and failure outcome. Decompose
> an operation when it exposes a distinct business-rule, decision, ownership,
> recovery, or test boundary; do not impose a fixed depth or size threshold.
> For transformations, identify the source structure, output structure,
> ordering, aggregation, and partial-failure behavior when applicable. For
> event dispatch, identify the dispatch owner, supported events, named handler
> responsibility, and exhaustive or fallback behavior. Use concise pseudocode
> only when it clarifies meaningful order, branches, loops, retries, or error
> recovery beyond ordinary structured assertions.

### Module Design Template

Add one instruction to Public Contracts after the existing contract prompt:

> For a public, persisted, external, or ambiguous contract, give representative
> input and output examples and explain what each example establishes about the
> supported variants, validation, ownership, or failure behavior.

Add one instruction to Processing Rules after the existing flow prompt:

> When the module transforms structured input or dispatches events, name the
> transformation or dispatch owner, the supported variants, the responsible
> stages or handlers, and ordering, fallback, aggregation, or recovery rules
> that affect the resulting contract.

### Create Module Design

Add to its workflow after identifying processing rules:

> For a complex process, identify whether the design needs a named entry
> operation, representative boundary examples, a transformation decomposition,
> or explicit event-dispatch ownership. Include only the detail required to
> make contracts, branches, errors, and verification source-backed and
> implementable without guessing.

No new agent or standalone process-design skill is warranted. This guidance is
part of component and module design, and its scope decision is already handled
by Development Methodology.

## Conclusion

Retire the procedure as a standalone workflow. Keep its top-down process
clarity, meaningful boundary examples, transformation and dispatch ownership,
cohesive decomposition, and explicit failure behavior. Add narrow optional
guidance to Structured Design, the module-design template, and Create Module
Design; leave document paths, pseudocode typography, explanation ladders, and
arbitrary decomposition limits behind.
