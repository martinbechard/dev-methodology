# Update Role-Mutation Test For Schema V5

Status: Completed

Type: Defect

Provider: file

Provider Reference: backlog/completed-backlog/defects/update-role-mutation-test-for-schema-v5.md

Completion: direct-main

Owner: Dev Orchestrator

## Summary

Correct the stale schema-version assertion in the role-mutation policy regression so it matches the authoritative role schema version without weakening repositoryMutation coverage.

## Context

The authoritative agents/role-schema.yaml declares version 5. The focused regression scripts.test_role_mutation_policy.RoleMutationPolicyTests.test_role_schema_requires_repository_mutation still asserts schema version 4 at scripts/test_role_mutation_policy.py:288. The command below exits 1 with AssertionError: 4 != 5. The same failure was reproduced from an independent Git archive of frozen baseline 2eb4e7f6934c3e9c95c19a2dd03be032d51695a5, whose tracked tree equals main f58290fac280b58d2ef7aa6a8338b28e5ba5781d. The active durable-defect candidate changes neither agents/role-schema.yaml nor scripts/test_role_mutation_policy.py.

## Source Evidence

The user's standing explicit direction in canonical task 019f96cf-226c-7f62-9d66-7d31cead822e authorizes durable Ready logging of every confirmed defect and forbids downgrading a confirmed defect to a warning. Confirmed reproduction: test id scripts.test_role_mutation_policy.RoleMutationPolicyTests.test_role_schema_requires_repository_mutation; command /opt/homebrew/bin/python3.11 -m unittest scripts.test_role_mutation_policy.RoleMutationPolicyTests.test_role_schema_requires_repository_mutation; failure at scripts/test_role_mutation_policy.py:288, self.assertEqual(4, schema["version"]); observed AssertionError: 4 != 5; exit 1.

## Requirements

- Inspect the accepted schema-v5 migration and identify every coupled version-specific ordinary regression expectation.
- Update stale expectations to version 5 while preserving the repositoryMutation requirement coverage.
- Keep this correction separate from the active durable confirmed-defect logging policy task.

## Acceptance Criteria

- The schema-version assertion aligns with the authoritative schema version 5.
- repositoryMutation coverage remains present and is not weakened by the correction.
- The full scripts.test_role_mutation_policy module and affected role-generation checks pass.
- An independent review accepts the focused change.

## Dependencies

None.

## Verification

- Run /opt/homebrew/bin/python3.11 -m unittest scripts.test_role_mutation_policy.
- Run the affected role-generation checks identified during inspection.
- Obtain independent review of the assertion and any coupled version-specific expectations.

## Open Questions

None.

## Notes

Runnable next action: inspect the accepted schema-v5 migration, update the stale ordinary regression assertion and coupled version-specific expectations, then run the listed verification. Do not implement the correction as part of this creation task.

## Current Starting Reservation

- Transition: Ready -> Starting.
- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a.
- Reservation: One parent-owned launch reservation.
- Normalized Objective: Update the stale role-schema version assertion to version 5 while preserving repositoryMutation coverage.
- Dispatched At: 2026-07-26T17:56:42Z.
- Intended Root Role: Dev Orchestrator.
- Runtime Thread And Task Id: Pending creation.
- Backlog Claim: reserve-schema-v5-test-defect; acquire event bdb2f65b-5831-43fb-a07c-d71bc088cb73.
- Governed-Definition Mutation Authority: None.
- Next Lifecycle Owner: The eventual root Dev Orchestrator must record a distinct Starting -> Running acceptance before implementation or further repository mutation.

## Current Running Acceptance

- Transition: Starting -> Running.
- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a.
- Canonical Work-Item Thread: 019f9f93-bf1a-7d20-9ab1-b184f9c39088.
- Canonical Root Agent Task: 019f9f93-bf1a-7d20-9ab1-b184f9c39088.
- Root Dev Orchestrator: Dev Orchestrator.
- Delivery Branch: codex/schema-v5-role-mutation-test-019f9f93.
- Delivery Worktree: /Users/martinbechard/.codex/worktrees/68d2/dev-methodology.
- Phase: Delivery accepted.
- Started At: 2026-07-26T18:01:34Z.
- Claim Evidence: starting-to-running-schema-v5-019f9f93; acquire outcome SHARED_CHECKOUT_ACQUIRED; claim event a4720a64-af29-4b8c-9bc7-86bfb2d98e6f.
- Next Lifecycle Owner: The root Dev Orchestrator owns delivery. Its Dev Backlog Steward child performs later provider transitions on this canonical item.

## Completion Evidence

- Completed At: 2026-07-26T18:23:19Z.
- Canonical work-item Thread and root Agent Task: 019f9f93-bf1a-7d20-9ab1-b184f9c39088. No replacement task or Thread was created.
- Accepted source candidate: 4d20d431db826212a48c17ef9806e9b67a4540da on branch codex/schema-v5-role-mutation-test-019f9f93. Its only change updates scripts/test_role_mutation_policy.py from schema-version assertion 4 to 5 while preserving repositoryMutation assertions.
- Independent review: GOOD with no findings.
- Source verification: /opt/homebrew/bin/python3.11 -m unittest scripts.test_role_mutation_policy passed 13 tests; BundleContentTests.test_source_roles_generate_current_documentation_and_adapters passed 1 test; Git diff check passed; the source worktree was clean.
- Direct-main integration: 410438f99dd403caca699e7834a2493c09025467. The accepted hunk was already represented on main through 38cfa95989f33769a4cbe745b8e10f52eb397b82, proven by non-ancestral content mapping and reverse-application checking while preserving the newer main role count.
- Post-integration verification: focused mutation-policy test passed 1 test; role-generation check passed 1 test; Git diff checks were clean.
- Main observation: 410438f99dd403caca699e7834a2493c09025467 is reachable from main. Descendant 942bac974d87d7b7c7a11ee724b80c0d91c3d0e6 preserved it, and the terminal transaction started from clean primary main at fb18e79d09faefe7036146aef758f0e212d7917a.
- Lifecycle and integration claims: Starting-to-Running commit 1814e2875c80c9a0e6f5b81073a216066ea56998; claim acquire event a4720a64-af29-4b8c-9bc7-86bfb2d98e6f and release event ccfb2b14-f1b4-41a1-aba4-aa4573429672. Direct-main integration claim direct-main-schema-v5-019f9f93 acquired in event 55f1c8d6-274c-4019-beaa-0d66e8ca745b and released with no-change mapping in event 3698d833-835f-49c5-917c-2e9eb451b435. Terminal archive claim complete-schema-v5-role-mutation-test-019f9f93 acquired in event 7259797d-ccf3-4842-a140-f29c65bdcfa5.
- Publication: no remote publication is configured; no push was attempted.
- Archive path: backlog/completed-backlog/defects/update-role-mutation-test-for-schema-v5.md.
