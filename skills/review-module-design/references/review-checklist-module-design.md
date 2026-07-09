# Module Design Review Checklist

## Purpose

Use this Review Checklist to verify a module design artifact created from the methodology templates.

## Completion Format

For every question record:

- Status: pass, fail, question, or n/a.
- Question: copy the objective question being answered.
- Quoted evidence: quote the exact artifact or source text that supports the status.
- Assessment: explain why the quoted evidence passes, fails, is unclear, or is not applicable.

Do not mark pass without quoted evidence.

## Skill Workflow Checks

- Question: Does the review identify runtime path, responsibility, callers, dependencies, contracts, internal state, processing rules, error handling, and verification claims before assessment?
- Question: Does the completed review checklist name this checklist as review-checklist-module-design.md?
- Question: Does the completed review checklist save next to the artifact using artifact-name.review-checklist-module-design.md?
- Question: Does the review use documentation-page-verifier with the artifact, source evidence, and completed review checklist?
- Question: Does the final assessment derive findings or pass status from the completed review checklist rather than memory?
- Question: Does the output lead with findings ordered by severity when problems exist?

## Shared Contract Questions

- Question: Does the artifact start with Current Understanding, Authoritative Sources, Related Code, Related Tests, Related Backlog Items, Related Wiki Pages, Open Questions, and Maintenance Notes?
- Question: Does Current Understanding describe the module as it exists or is intended now?
- Question: Do Authoritative Sources include module source, callers, tests, configuration, parent designs, procedures, and related wiki pages?
- Question: Do Related Code and Related Tests identify evidence or say Not yet identified after a real search?
- Question: Do Open Questions capture unresolved ownership, contracts, behavior, errors, or verification issues?

## Artifact-Specific Questions

- Question: Does Purpose And Runtime Path name the module and its project-relative runtime path?
- Question: Does Parent Context explain the subsystem, architecture, feature, or workflow that owns the module?
- Question: Are Responsibilities coherent, bounded, and not a mixed list of unrelated work?
- Question: Do Callers And Dependencies identify direct callers, imported dependencies, external systems, generated artifacts, and test seams?
- Question: Do Public Contracts describe exports, inputs, outputs, events, messages, side effects, and expected errors?
- Question: Do Internal Data And State describe maintained state, caches, derived values, persistence, and ownership rules?
- Question: Do Processing Rules describe main flow, branches, retries, validation, ordering, idempotency, and concurrency rules when applicable?
- Question: Do Invariants state rules that must always hold?
- Question: Are Configuration, External Interfaces, UI Behavior, And Notifications covered when the module owns them?
- Question: Does Error Handling name expected failures, propagation, logging, retry, recovery, and user-visible outcomes?
- Question: Does Verification link unit, integration, end-to-end, lint, validation, or manual evidence for each important responsibility?
- Question: Does Processing Diagram exist only when it clarifies real branches, state transitions, retries, or error handling?

## Findings

Report findings first. Treat missing runtime path, broad or mixed responsibilities, missing callers, vague contracts, unsourced processing rules, incomplete error handling, and missing verification as review findings.
