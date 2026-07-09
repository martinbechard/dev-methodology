# Functional Specification Review Checklist

## Purpose

Use this Review Checklist to verify a functional specification artifact created from the methodology templates.

## Shared Contract

- The artifact starts with Current Understanding, Authoritative Sources, Related Code, Related Tests, Related Backlog Items, Related Wiki Pages, Open Questions, and Maintenance Notes.
- Current Understanding describes the behavior as it should be understood now.
- Authoritative Sources distinguish implemented behavior from intended behavior.
- Related Code and Related Tests identify evidence or say Not yet identified after a real search.
- Open Questions capture behavior, ownership, or acceptance conflicts that cannot be resolved from sources.

## Artifact-Specific Checks

- User Or Actor Goal names the actor and the outcome they need.
- Parent Workflow And Entry Points identify where the workflow starts and how users reach it.
- Route Or Surface List covers relevant routes, screens, commands, APIs, notifications, or external surfaces.
- Scope And Non-Goals distinguish included behavior from excluded or deferred behavior.
- Concepts define terms the actor must understand without drifting into module design.
- Workflow Steps are written from the actor's point of view and cover main, alternate, empty, error, and recovery paths.
- States, Rules, Permissions, And Edge Cases identify status values, permission gates, validation rules, limits, and failure behavior.
- Verification blocks name test type, test files, scenario, steps, assertions, and current status.
- Related Documents link architecture, high-level design, module design, tests, and wiki pages that support the workflow.
- Technical implementation detail stays in related technical documents unless users need it to understand behavior.

## Findings

Report findings first. Treat missing actor goal, missing entry points, missing acceptance behavior, missing state or permission coverage, unsourced workflow claims, and missing verification as review findings.
