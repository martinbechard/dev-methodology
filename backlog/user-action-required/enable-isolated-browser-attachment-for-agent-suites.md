# Enable Isolated Browser Attachment For Agent Suites

Status: User Action Required

Type: Feature

## User Action Required

The repository and current Codex host can attach the user-visible root task to a fresh in-app browser session, but cannot provision an isolated in-app backend for the agent-suite child target identity.

## Question for the User

Should this item wait for supported child-thread in-app-browser provisioning, or should scope explicitly authorize a new app-owned root-task suite harness and its identity and evidence contract?

## Why User Input Is Required

The supported root-task path passed, but nested Dev Browser Operator and Dev Runtime Diagnostician tasks had no in-app backend. The current runner stages browser clients for detached Codex execution but cannot provision the desktop-owned backend. Reusing or proxying the parent backend would bypass the host's exact session-isolation boundary, so the repository cannot select that workaround safely without a product or scope decision.

## Resolution

Pending.

## Unattended Work Boundary

Do not proxy, spoof, reuse, or otherwise bypass the parent task's browser-session identity. Resume only after supported child-target provisioning exists or the user explicitly authorizes the app-owned root-task harness alternative.

## Current Execution

- Canonical Dev Orchestrator task: 019f7e76-c898-7e72-bdef-1c5f6897abd2.
- Branch: codex/isolated-browser-attachment.
- Worktree: /Users/martinbechard/.codex/worktrees/a509/dev-methodology.
- Root-task proof: fresh local tab and Account-flow DOM with empty inventories before and after; claim released at event 5a17988a-8d9c-4283-afa2-d018e360a221.
- Child-target blocker: no in-app backend was provisioned for either nested child identity; no repository change or candidate commit was produced.
- Phase: stopped cleanly for the user-owned execution-model decision.

## Summary

Provide a governed browser-automation execution path that lets isolated agent-suite targets attach to a fresh in-app browser session and collect real interaction evidence while preserving strict cleanup and authority boundaries.

## Context

Five browser-dependent scenarios reached a common infrastructure boundary: the staged isolated target reported that the in-app browser was unavailable and had an empty inventory. The fixture services and claims were healthy, but UI interaction, reload persistence, accessibility, network correlation, and browser-visible route assertions could not execute.

The affected scenarios are Dev UX Specialist complete-responsive-flow and keyboard-and-accessibility-barriers, plus Dev Browser Operator persisted-setting-workflow, upload-boundary-failure, and blocked-route-owned-cleanup. The last scenario must remain semantically BLOCKED for its intentionally absent success route even after browser attachment works.

The classification is recorded in [Classify Agent Suite Blocking Resources](../completed-backlog/analyses/classify-agent-suite-blocking-resources.md), and the authoritative run evidence is preserved in [Complete Agent Suite Results](../../evals/agent-tests/results/2026-07-17-complete-agent-suites.md).

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
