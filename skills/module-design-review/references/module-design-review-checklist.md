# Module Design Review Checklist

## Purpose

Use this Review Checklist to verify a module design artifact created from the methodology templates.

## Shared Contract

- The artifact starts with Current Understanding, Authoritative Sources, Related Code, Related Tests, Related Backlog Items, Related Wiki Pages, Open Questions, and Maintenance Notes.
- Current Understanding describes the module as it exists or is intended now.
- Authoritative Sources include module source, callers, tests, configuration, parent designs, procedures, and related wiki pages.
- Related Code and Related Tests identify evidence or say Not yet identified after a real search.
- Open Questions capture unresolved ownership, contracts, behavior, errors, or verification issues.

## Artifact-Specific Checks

- Purpose And Runtime Path name the module and its project-relative runtime path.
- Parent Context explains the subsystem, architecture, feature, or workflow that owns the module.
- Responsibilities are coherent, bounded, and not a mixed list of unrelated work.
- Callers And Dependencies identify direct callers, imported dependencies, external systems, generated artifacts, and test seams.
- Public Contracts describe exports, inputs, outputs, events, messages, side effects, and expected errors.
- Internal Data And State describe maintained state, caches, derived values, persistence, and ownership rules.
- Processing Rules describe main flow, branches, retries, validation, ordering, idempotency, and concurrency rules when applicable.
- Invariants state rules that must always hold.
- Configuration, External Interfaces, UI Behavior, And Notifications are covered when the module owns them.
- Error Handling names expected failures, propagation, logging, retry, recovery, and user-visible outcomes.
- Verification links unit, integration, end-to-end, lint, validation, or manual evidence for each important responsibility.
- Processing Diagram exists only when it clarifies real branches, state transitions, retries, or error handling.

## Findings

Report findings first. Treat missing runtime path, broad or mixed responsibilities, missing callers, vague contracts, unsourced processing rules, incomplete error handling, and missing verification as review findings.
