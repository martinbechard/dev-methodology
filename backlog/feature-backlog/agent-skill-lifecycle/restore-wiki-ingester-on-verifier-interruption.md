# Restore Wiki Ingester On Verifier Interruption

Status: Blocked

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

## Blocked Outcome

The same HIGH code-review finding remained after two correction attempts, so the correction budget is exhausted. The clean implementation and correction commits 8c28d9b, c677f09, and c75c8b1 remain preserved.

Independent code review never accepted the contribution. Verification and integration therefore did not run.

The unresolved defect is the missing executable boundary to the actual Wiki Ingester or its generated adapter. The current harness injects verifier receipts and then performs restoration, writes the evaluation result, commits the result, and releases the claim itself. Actual Wiki Ingester role regressions can therefore false-pass the interruption tests.

The next action requires an executable target boundary with a nested verifier dependency-injection seam. Injected verifier outcomes must pass through the actual Wiki Ingester execution path so the suite observes the target's restoration, result, commit, receipt, and claim-closeout behavior.

## Notes

- The harness contention that triggered the path is separate from the target's obligation to fail cleanly.
