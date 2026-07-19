# Enable Isolated Browser Attachment For Agent Suites

Status: Ready

Type: Feature

## Summary

Provide a governed browser-automation execution path that lets isolated agent-suite targets attach to a fresh in-app browser session and collect real interaction evidence while preserving strict cleanup and authority boundaries.

## Context

Five browser-dependent scenarios reached a common infrastructure boundary: the staged isolated target reported that the in-app browser was unavailable and had an empty inventory. The fixture services and claims were healthy, but UI interaction, reload persistence, accessibility, network correlation, and browser-visible route assertions could not execute.

The affected scenarios are Dev UX Specialist complete-responsive-flow and keyboard-and-accessibility-barriers, plus Dev Browser Operator persisted-setting-workflow, upload-boundary-failure, and blocked-route-owned-cleanup. The last scenario must remain semantically BLOCKED for its intentionally absent success route even after browser attachment works.

The classification is recorded in [Classify Agent Suite Blocking Resources](../analysis-backlog/classify-agent-suite-blocking-resources.md), and the authoritative run evidence is preserved in [Complete Agent Suite Results](../../evals/agent-tests/results/2026-07-17-complete-agent-suites.md).

## Requirements

- Run browser-capability scenarios in a Codex execution context that can attach to the isolated in-app browser backend.
- Preserve a fresh empty browser inventory before each scenario and prohibit Chrome, existing tabs, authenticated state, shared profiles, and non-local destinations.
- Bind the browser session, local service, selected port, fixture root, and target identity to retained run evidence.
- Require the target to exercise the declared interaction rather than infer behavior from source or static descriptions.
- Retain governed visual-state or equivalent interaction evidence, browser-network evidence when applicable, and explicit tab-close receipts.
- Fail browser capability preflight before target execution when attachment is unavailable, while preserving the current truthful BLOCKED and cleanup behavior.
- Keep each scenario's local service, browser state, files, ports, processes, and claims isolated from concurrent suites.
- Preserve the intentional missing-route boundary in blocked-route-owned-cleanup and the intentional missing-runtime-evidence Dev UX scenario.

## Acceptance Criteria

- A browser-capability preflight opens and closes a fresh local-target tab through the isolated in-app backend without using existing user state.
- The complete-responsive-flow scenario exercises wide, narrow, keyboard, validation, recovery, and success states with retained observations.
- The keyboard-and-accessibility-barriers scenario reproduces and prioritizes every seeded barrier with governed evidence.
- The persisted-setting-workflow scenario changes the preference, reloads, and observes the persisted visible value.
- The upload-boundary-failure scenario correlates the visible error with the request, status, and service diagnostics without inventing a storage root cause.
- The blocked-route-owned-cleanup scenario observes the browser-visible missing route, remains BLOCKED for the deliberate fixture boundary, and closes every owned resource.
- Each scenario leaves no tab, profile, process, port, claim, credential, fixture, or worktree residue.
- Browser-dependent scenarios are no longer classified as infrastructure BLOCKED solely because isolated attachment is unavailable.

## Dependencies

None.

## Verification

- Run the two browser-capability Dev UX Specialist scenarios in isolated fresh sessions and inspect interaction evidence and cleanup receipts.
- Run all three Dev Browser Operator scenarios and inspect UI, network, service, persistence, missing-route, and cleanup evidence.
- Force attachment preflight failure and confirm no target interaction begins and the existing safe BLOCKED closeout remains intact.
- Run multiple isolated browser batches and prove they do not share ports, profiles, tabs, credentials, or mutable fixture state.
- Run the focused runner capability tests, affected suite tests, applicable bundle validation, and Git diff validation.

## Notes

- Browser availability is an execution capability, not permission to use the user's Chrome session or authenticated state.
- Do not convert deliberately absent runtime evidence or routes into product defects.
