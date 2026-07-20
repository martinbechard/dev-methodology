# Restore Wiki Ingester On Verifier Interruption

Status: Running

Type: Defect

## User Decision Resolved

- Canonical Dev Orchestrator task: 019f8056-a0f4-7090-8715-65f718d14f76.
- Active branch: codex/restore-wiki-ingester-open-questions.
- Active worktree: /Users/martinbechard/.codex/worktrees/7f71/dev-methodology.
- Superseded archived task: 019f7e86-aece-7a40-96e1-b1e1863dba28; its rollout was unavailable and it is not active ownership.
- Preserved evidence branch: codex/restore-wiki-ingester-verifier-flow.
- Preserved eval-only evidence head: 914bc09, following the bounded executable-boundary correction history on the same branch.
- Resumed direction: implement the approved substantiated-ingest plus page-local Open Questions contract; the rejected rollback/BLOCKED proposal is historical only.
- The eval-only boundary now proves the current canonical Wiki Ingester behavior retains unaccepted docs/wiki drafts after a bound pre-move verifier interruption following one genuine correction.
- No governed role or distributed skill definition was mutated.

The proposed rollback-and-BLOCKED behavior was rejected. The user directed Wiki Ingester to continue ingesting what is substantiated and to flag what is not substantiated as open questions in the appropriate wiki page Open Questions sections.

Approved governed scope: change only agents/roles/wiki-activities/wiki-ingester.role.yaml, its supported generated role mirrors, and directly related focused bundle/evaluation expectations to implement this continuation-and-open-questions behavior. This authorizes no distributed skill-definition change.

Approval evidence: the user's direct clarification in parent thread 019f77f4-c4bd-7c91-b197-c987a7beb838 on 2026-07-20: “Ingest what is substantiated, flag what is not as open questions.”

## Current Execution

- Accepted correction candidate: c8bf42888595fb3a2bf6e8f15b460a819c884f00, superseding 2cb0aea46cff6e9c40e8a656aa862f074d314da9.
- The first reduced pre0 proof stopped after 207.217 seconds when its conclusion bullet used a semicolon/em-dash page-and-source shape instead of the required explicit colon before fact text. Raw-ingest did not start, and the isolated live claim released normally at event 4ba33706-949e-4700-a889-0cda9cfa9dbf.
- The retained sanitized result was replayed offline. The exact failing shape now has deterministic regression coverage, and the corrected role wording requires an explicit colon before fact text.
- Fresh independent methodology review accepted c8bf428, and focused verification passed 21 boundary tests, one bundle test, generated integrity, build-skill-docs freshness, and all four supported mirror hashes from a clean worktree.
- The prior four-case live run completed in 1087.607 seconds. Pre2 passed. Pre0, post0, and raw-ingest reached their required lifecycle, page, source, verifier, and cleanup outcomes but omitted a nonempty Substantiated Conclusions inventory.
- Read-only classification found three target-output defects, zero evaluator defects, and zero infrastructure defects. Pre2 passing the same parser disproved a universal parser defect.
- The next live proof is pre0 only under an eight-minute hard cap. Passing pre2, duplicate post0, raw-ingest, and unrelated cases are excluded. Raw-ingest may be proposed later only for a distinct acceptance criterion that retained evidence and deterministic checks cannot prove; it must not start automatically after pre0.
- Future live evidence retains sanitized terminal results and replays their exact shapes offline before another live run.
- The live claim owns only test:live:wiki-ingester. It must use canonical isolated mode with no project-file or main-integration scope.
- A short primary backlog transaction records this material phase and supplies a legitimate isolation window. It will release immediately after the resource-only claim is acquired.

## Summary

Require Wiki Ingester to preserve and ingest substantiated material while recording unsubstantiated or unresolved material as explicit open questions on the relevant wiki pages.

## Context

In the Wiki Ingester verifier-failure evaluation, the first verifier correctly returned NEEDS_CORRECTION. Shared nested-agent contention then prevented the remaining bounded verification loop. The target left three unaccepted wiki edits, omitted the required evaluation result, retained an active claim, and left a dirty worktree instead of restoring the frozen baseline and returning clean BLOCKED. The suite supervisor had to repair the disposable fixture and release the claim.

The contention was evaluation infrastructure, but the unsafe interruption closeout was target behavior. The complete evaluation did not edit the distributed Wiki Ingester skills.

## Evidence

- evals/agent-tests/wiki-ingester/scenarios.yaml defines the verifier-failure and clean-closeout contract.
- evals/agent-tests/wiki-ingester/fixtures/verifier-failure contains the frozen failure fixture.
- evals/agent-tests/results/2026-07-17-complete-agent-suites.md records the interrupted verifier loop and supervisor cleanup.
- The live checkpoint recorded unaccepted docs/wiki edits, a missing evaluation result, an active claim, and a dirty worktree after verification could not continue.

## Requirements

- Ingest every claim and relationship supported by the available authoritative evidence.
- Do not discard substantiated wiki content merely because another claim remains uncertain or verifier execution is interrupted.
- Put each unsubstantiated, unresolved, or verifier-dependent point into the Open Questions section of the most relevant wiki page.
- Keep open questions specific enough to identify the missing evidence or decision needed for later resolution.
- Preserve source links and provenance for both ingested conclusions and open questions.
- Write the required result describing what was ingested and which open questions were recorded.
- Release every claim owned by the task and verify the worktree and live registry are clean.
- Add interruption coverage at each point in the bounded verifier loop.

## Acceptance Criteria

- A verifier interruption retains all substantiated wiki updates.
- Unsubstantiated or unresolved content appears as explicit open questions on the appropriate wiki pages rather than being silently asserted or discarded.
- The evaluation result distinguishes ingested conclusions from recorded open questions.
- Claims are released and the worktree is clean without supervisor repair.
- Normal verifier correction and acceptance behavior remains unchanged.
- The Wiki Ingester verifier-interruption scenario produces a governed terminal result without rolling back substantiated content.
- Repository role validation, generated-output checks, and focused unit tests pass.

## Dependencies

None.

## Verification

- Add focused tests that interrupt the verifier before and after each correction attempt.
- Compare the final tree with the frozen baseline after every BLOCKED path.
- Inspect the evaluation result, claim trace, and worktree cleanup evidence.
- Run the Wiki Ingester raw-ingest, destination-collision, and verifier-failure scenarios.
- Run Agent Skill validation, generated-output freshness checks, repository unit tests, and Git diff validation.

## Blocked Outcome

Historical outcome, superseded by the current Running resumption above.

The same HIGH code-review finding remained after two correction attempts, so the correction budget is exhausted. The clean implementation and correction commits 8c28d9b, c677f09, and c75c8b1 remain preserved.

Independent code review never accepted the contribution. Verification and integration therefore did not run.

The unresolved defect is the missing executable boundary to the actual Wiki Ingester or its generated adapter. The current harness injects verifier receipts and then performs restoration, writes the evaluation result, commits the result, and releases the claim itself. Actual Wiki Ingester role regressions can therefore false-pass the interruption tests.

The next action requires an executable target boundary with a nested verifier dependency-injection seam. Injected verifier outcomes must pass through the actual Wiki Ingester execution path so the suite observes the target's restoration, result, commit, receipt, and claim-closeout behavior.

## Notes

- The harness contention that triggered the path is separate from the target's obligation to preserve supported knowledge and expose uncertainty honestly.
- A verifier interruption is not authority to erase substantiated knowledge or promote unresolved claims to facts.
