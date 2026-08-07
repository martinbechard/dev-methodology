# Prevent Retired Skill Cache Directories From Breaking Validation

Status: Running

Type: Defect

Provider: file

Owner: Dev Orchestrator task 019fda3b-119f-7412-a045-29d5f8998d79

Work Item ID: prevent-retired-skill-cache-directories-from-breaking-validation

Completion: main-branch

Phase: Reviewing

Branch: codex/prevent-retired-skill-cache-validation-019fda3b

Worktree: /Users/martinbechard/.codex/worktrees/f905/dev-methodology

Canonical Conversation: Retained conversation for Codex task 019fda3b-119f-7412-a045-29d5f8998d79; the runtime exposes no separate conversation identifier.

Codex Task ID: 019fda3b-119f-7412-a045-29d5f8998d79

Root Role: Dev Orchestrator

Parent Task ID: 019fb057-1767-7ef2-b5fa-41f4417b20b3

Accepted Candidate Commit: afdfcfbf80583e788f11eec79cf868bfcf552025

## Summary

Keep ignored Python cache artifacts under retired skill paths from being interpreted as incomplete bundled skills or making repository validation scan obsolete skill identities.

## Context

The completed resource-claim rename removed the tracked `agent-claim` and `agent-claim-command` skill definitions. Local ignored `__pycache__` files can nevertheless retain the empty directory shapes `skills/agent-claim` and `skills/agent-claim-command`. Current bundle and installer validation discovers those directory names as skill candidates, reports them as incomplete skills, and scans obsolete paths during the retired-provider identity test.

This makes a supported source checkout fail because of disposable interpreter cache state that is neither a tracked methodology artifact nor a valid skill. A clean clone may pass while an actively used checkout fails, which makes verification non-reproducible.

## Source Evidence

On 2026-08-06, while verifying project-wide conditional Agent skill routing, `/opt/homebrew/bin/python3.11 -m unittest discover scripts` repeatedly reported `skill source contains incomplete skill directories: agent-claim, agent-claim-command`. Inspection found no tracked files under those paths; each directory contained only an ignored `scripts/__pycache__/claim.cpython-311.pyc`. The run later spent several minutes in `test_retired_provider_identities_are_absent_from_maintained_artifacts` while reading maintained paths and was interrupted after unrelated failures had already been emitted. The user then instructed: "don't forget to log defects for corrections."

## Requirements

- Define bundled-skill discovery from valid maintained skill sources rather than the mere presence of an ignored directory.
- Ensure cache-only retired paths cannot be reported as incomplete bundled skills.
- Ensure retired-provider identity validation does not treat disposable ignored cache files as maintained artifacts.
- Preserve detection of genuinely incomplete tracked or intended skill packages.
- Avoid requiring developers to know and manually remove interpreter caches before running repository verification.
- Add a regression fixture containing a retired skill-shaped directory with only ignored Python cache artifacts.

## Acceptance Criteria

- Bundle, installer, and skill validation do not report `agent-claim` or `agent-claim-command` when those paths contain only ignored cache artifacts.
- The retired-provider identity test completes in bounded time and ignores disposable cache-only paths while still detecting retired identities in maintained artifacts.
- A genuinely incomplete intended skill directory remains a validation failure.
- Focused tests pass both in a clean temporary checkout and in a fixture with cache-only retired directories.
- No retired skill identity is restored to the bundled catalog.

## Dependencies

None.

## Verification

- Run the focused skill-source discovery and retired-provider identity tests with cache-only retired directories present.
- Run the corresponding installer dry-run validation.
- Run `/opt/homebrew/bin/python3.11 scripts/validate-agent-skills.py skills`.
- Run `/opt/homebrew/bin/python3.11 -m unittest scripts.test_resource_claim_helper.ResourceClaimHelperTests.test_retired_provider_identities_are_absent_from_maintained_artifacts` or its current owning test class and method.
- Run `git diff --check`.

## Open Questions

- Determine whether one shared maintained-skill discovery helper should own this boundary for the installer, validators, generators, and tests.

## Starting Handoff Evidence

Starting Recorded At: 2026-08-07T03:17:37Z

Parent Coordination Thread: 019fb057-1767-7ef2-b5fa-41f4417b20b3

Launch Reservation: One Root Dev Orchestrator task for this exact work item.

Normalized Objective: Ensure maintained-skill discovery and retired-provider validation ignore cache-only retired skill paths while retaining incomplete intended skill detection and adding focused regression coverage.

Dispatch Time: 2026-08-07T03:17:37Z

Intended Root Role: Dev Orchestrator

Launch Result: Started

Canonical Execution: Codex task 019fda3b-119f-7412-a045-29d5f8998d79

Last Contact: 2026-08-07T03:21:35Z

Next Reconciliation At: 2026-08-07T03:36:35Z

## Running Transition Evidence

Transition: Starting -> Running

Running Recorded At: 2026-08-07T03:21:35Z

Owner: Dev Orchestrator task 019fda3b-119f-7412-a045-29d5f8998d79

Canonical Conversation: Retained conversation for Codex task 019fda3b-119f-7412-a045-29d5f8998d79; the runtime exposes no separate conversation identifier.

Root Agent Task: /root

Branch: codex/prevent-retired-skill-cache-validation-019fda3b

Worktree: /Users/martinbechard/.codex/worktrees/f905/dev-methodology

Phase: Implementing maintained-skill discovery and its directly implicated installer, validator, and focused regression support.

Started At: 2026-08-07T03:21:35Z

Accepted Execution Evidence: The canonical root Dev Orchestrator established a clean isolated candidate branch at main commit 2e415bdd3effe0074539dcf78302fab6c90f3b1d, accepted the bounded defect scope, and is ready to acquire the exact Work Item ID activity=work claim before delegating one source implementation lane.

Next Action: Release this atomic provider transaction, acquire the exact Work Item ID activity=work claim, and dispatch one Dev Coder to produce a focused immutable candidate.

## Active Execution Evidence

Condition Type: delegated-work

Owner: Dev Code Reviewer task /root/review_retired_skill_cache_candidate under Dev Orchestrator task 019fda3b-119f-7412-a045-29d5f8998d79

Evidence: Dev Coder task /root/implement_retired_skill_cache_fix returned clean immutable candidate afdfcfbf80583e788f11eec79cf868bfcf552025 with focused red-green, installer dry-run, validator, exact retired-provider, and diff checks passing. One fresh read-only Dev Code Reviewer now owns the bounded six-path independent review; candidate bytes and branch remain unchanged.

Observed At: 2026-08-07T03:36:43Z

Started At: 2026-08-07T03:36:24Z

Deadline or Expires At: 2026-08-07T04:36:43Z

Next Action: Reacquire the exact activity=work claim after this atomic provider update, accept or route any material review finding once, and dispatch one independent focused verifier only after the immutable candidate receives a GOOD review.

Next Reconciliation At: 2026-08-07T03:50:43Z
