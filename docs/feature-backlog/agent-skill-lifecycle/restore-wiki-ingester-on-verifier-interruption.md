# Restore Wiki Ingester On Verifier Interruption

Status: Ready

Type: Defect

## Summary

Require Wiki Ingester to restore unaccepted wiki drafts, close claims, and return a clean governed result when verification cannot finish.

## Context

In the Wiki Ingester verifier-failure evaluation, the first verifier correctly returned NEEDS_CORRECTION. Shared nested-agent contention then prevented the remaining bounded verification loop. The target left three unaccepted wiki edits, omitted the required evaluation result, retained an active claim, and left a dirty worktree instead of restoring the frozen baseline and returning clean BLOCKED. The suite supervisor had to repair the disposable fixture and release the claim.

The contention was evaluation infrastructure, but the unsafe interruption closeout was target behavior. The complete evaluation did not edit the distributed Wiki Ingester skills.

## Evidence

- evals/agent-tests/wiki-ingester/scenarios.yaml defines the verifier-failure and clean-closeout contract.
- evals/agent-tests/wiki-ingester/fixtures/verifier-failure contains the frozen failure fixture.
- evals/agent-tests/results/2026-07-17-complete-agent-suites.md records the interrupted verifier loop and supervisor cleanup.
- The live checkpoint recorded unaccepted docs/wiki edits, a missing evaluation result, an active claim, and a dirty worktree after verification could not continue.

## Requirements

- Treat unavailable or interrupted required verification as a governed BLOCKED boundary.
- Restore every unaccepted wiki edit to the frozen baseline before returning BLOCKED.
- Preserve accepted work only when its verifier evidence is complete and current.
- Write the required evaluation result with the blocker and restoration evidence.
- Release every claim owned by the task and verify the live registry is clear.
- Verify the worktree is clean before returning the terminal result.
- Add interruption coverage at each point in the bounded verifier loop.

## Acceptance Criteria

- A verifier interruption leaves no unaccepted docs/wiki changes.
- The evaluation result states the blocker and the restoration performed.
- Claims are released and the worktree is clean without supervisor repair.
- Normal verifier correction and acceptance behavior remains unchanged.
- The Wiki Ingester verifier-failure scenario produces a governed terminal result under a forced verifier interruption.
- Repository skill validation, generated-output checks, and unit tests pass.

## Dependencies

None.

## Verification

- Add focused tests that interrupt the verifier before and after each correction attempt.
- Compare the final tree with the frozen baseline after every BLOCKED path.
- Inspect the evaluation result, claim trace, and worktree cleanup evidence.
- Run the Wiki Ingester raw-ingest, destination-collision, and verifier-failure scenarios.
- Run Agent Skill validation, generated-output freshness checks, repository unit tests, and Git diff validation.

## Notes

- The harness contention that triggered the path is separate from the target's obligation to fail cleanly.
