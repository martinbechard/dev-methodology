# Prevent Retired Skill Cache Directories From Breaking Validation

Status: Ready

Type: Defect

Provider: file

Owner: Unowned

Work Item ID: prevent-retired-skill-cache-directories-from-breaking-validation

Completion: main-branch

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
