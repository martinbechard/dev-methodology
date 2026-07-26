# Update Role-Mutation Test For Schema V5

Status: Starting

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/update-role-mutation-test-for-schema-v5.md

Completion: direct-main

Owner: Unowned

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
