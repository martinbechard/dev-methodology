# Provide Isolated Playwright Harness For Agent Suites

Status: Running

Type: Feature

## Resolution

On 2026-07-20 the user directed the repository to use a UI-level test framework so direct browser access is unnecessary. The selected implementation is an isolated Playwright harness. Playwright is preferred over Selenium and Cypress because the affected scenarios are local synthetic workflows and require per-scenario browser contexts, traces, screenshots, network observations, and deterministic cleanup rather than a desktop-owned browser session.

## Unattended Work Boundary

Do not proxy, spoof, reuse, or otherwise bypass a desktop-owned browser-session identity. Do not use the user's Chrome profile, existing tabs, authenticated state, or non-local destinations. The target agent must exercise the declared interaction through the isolated Playwright surface; a supervisor must not substitute a prewritten test result for the target's work.

## Current Execution

- Canonical Dev Orchestrator task: 019f7e76-c898-7e72-bdef-1c5f6897abd2.
- Branch: codex/isolated-browser-attachment.
- Worktree: /Users/martinbechard/.codex/worktrees/a509/dev-methodology.
- Approval and Ready transition: main commit 0b211b653cdd13612b38376d996deba4289fe940; claim release event a38b9d21-e85b-40eb-8111-73f180bd4618.
- Root-task proof: fresh local tab and Account-flow DOM with empty inventories before and after; claim released at event 5a17988a-8d9c-4283-afa2-d018e360a221.
- Child-target blocker: no in-app backend was provisioned for either nested child identity; no repository change or candidate commit was produced.
- Phase: Running under the canonical Dev Orchestrator task for an isolated Playwright implementation.

## Summary

Provide a governed Playwright execution path that lets isolated agent-suite targets control a fresh headless browser context and collect real interaction evidence while preserving strict cleanup and authority boundaries.

## Context

Five browser-dependent scenarios reached a common infrastructure boundary because their execution was coupled to a desktop-owned in-app browser backend. The fixture services and claims were healthy, but UI interaction, reload persistence, accessibility, network correlation, and browser-visible route assertions could not execute in isolated child targets.

The affected scenarios are Dev UX Specialist complete-responsive-flow and keyboard-and-accessibility-barriers, plus Dev Browser Operator persisted-setting-workflow, upload-boundary-failure, and blocked-route-owned-cleanup. The last scenario must remain semantically BLOCKED for its intentionally absent success route even after browser attachment works.

The classification is recorded in [Classify Agent Suite Blocking Resources](../completed-backlog/analyses/classify-agent-suite-blocking-resources.md), and the authoritative run evidence is preserved in [Complete Agent Suite Results](../../evals/agent-tests/results/2026-07-17-complete-agent-suites.md).

## Requirements

- Provision a fresh Playwright browser and isolated browser context for every browser-capability scenario.
- Use the repository-designated bundled or pinned Playwright and Chromium runtime without relying on a desktop-owned in-app browser backend.
- Preserve a fresh empty context before each scenario and prohibit Chrome, existing tabs, authenticated state, shared profiles, and non-local destinations.
- Bind the Playwright runtime and browser-context identity, local service, selected port, fixture root, and target identity to retained run evidence.
- Require the target to exercise the declared interaction rather than infer behavior from source or static descriptions.
- Retain Playwright traces, screenshots or equivalent visual-state evidence, console output, browser-network evidence when applicable, and explicit page, context, and browser-close receipts.
- Fail browser capability preflight before target execution when the pinned runtime or browser cannot launch, while preserving truthful BLOCKED and cleanup behavior.
- Keep each scenario's local service, browser context, files, ports, processes, and claims isolated from concurrent suites.
- Preserve the intentional missing-route boundary in blocked-route-owned-cleanup and the intentional missing-runtime-evidence Dev UX scenario.

## Acceptance Criteria

- A browser-capability preflight launches the pinned Playwright browser, opens and closes a fresh isolated local-target context and page, and proves no existing user state is available.
- The complete-responsive-flow scenario exercises wide, narrow, keyboard, validation, recovery, and success states with retained observations.
- The keyboard-and-accessibility-barriers scenario reproduces and prioritizes every seeded barrier with governed evidence.
- The persisted-setting-workflow scenario changes the preference, reloads, and observes the persisted visible value.
- The upload-boundary-failure scenario correlates the visible error with the request, status, and service diagnostics without inventing a storage root cause.
- The blocked-route-owned-cleanup scenario observes the browser-visible missing route, remains BLOCKED for the deliberate fixture boundary, and closes every owned resource.
- Each scenario leaves no page, context, browser process, profile, port, claim, credential, fixture, or worktree residue.
- Browser-dependent scenarios are no longer classified as infrastructure BLOCKED solely because a desktop-owned in-app browser backend is unavailable.

## Dependencies

None.

## Verification

- Run the two browser-capability Dev UX Specialist scenarios in isolated fresh Playwright contexts and inspect interaction evidence and cleanup receipts.
- Run all three Dev Browser Operator scenarios and inspect UI, network, service, persistence, missing-route, and cleanup evidence.
- Force Playwright launch preflight failure and confirm no target interaction begins and the existing safe BLOCKED closeout remains intact.
- Run multiple isolated browser batches and prove they do not share ports, contexts, profiles, pages, credentials, or mutable fixture state.
- Run the focused runner capability tests, affected suite tests, applicable bundle validation, and Git diff validation.

## Notes

- Browser automation is an execution capability, not permission to use the user's Chrome session, desktop-owned browser backend, or authenticated state.
- In-app browser coverage remains appropriate only for tests specifically about Codex desktop browser integration; none of the five scenarios in this item require that product-specific surface.
- Do not convert deliberately absent runtime evidence or routes into product defects.
