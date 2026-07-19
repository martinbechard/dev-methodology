# Correct Agent Suite Classification Archive References

Status: Completed

Type: Defect

## Running Ownership

- Owner: Dev Orchestrator root task 019f77f4-c4bd-7c91-b197-c987a7beb838.
- Lifecycle agent: Dev Backlog Steward.
- Lifecycle claim: correct-agent-suite-classification-archive-references-start.
- Claim evidence: PRIMARY exact-file backlog ownership acquired at 2026-07-19T10:07:47.899884Z from clean baseline commit 979a0bc0771132195b33fbf559c2f9c9c2e981e9.
- Scope boundary: this claim owns only the Running transition and is released after its clean commit. Project artifacts, feature-link corrections, generated outputs, verification, and integration remain gated on a later ARTIFACT GO.

## Summary

Align the bundle-content regression and follow-up backlog links with the completed archive location and terminal status of the agent-suite blocking-resource classification.

## Context

Commit e07e4f23e69ac8e31f70caa3b93da5701e1d5b71 moved backlog/analysis-backlog/classify-agent-suite-blocking-resources.md to backlog/completed-backlog/analyses/classify-agent-suite-blocking-resources.md and changed its status from Running to Completed.

The bundle-content regression in scripts/test_bundle_content.py still resolves the former active path and requires Status: Running. The three Ready follow-up items created from the classification also link to the former active path:

- backlog/feature-backlog/enable-isolated-browser-attachment-for-agent-suites.md
- backlog/feature-backlog/enable-policy-compatible-security-review-agent-suites.md
- backlog/feature-backlog/specify-deterministic-dev-orchestrator-dependency-routing-fixtures.md

The full scripts suite therefore reports one failure from the stale assertion, and the three source links no longer resolve to the durable classification record.

## Requirements

- Resolve the classification from backlog/completed-backlog/analyses/classify-agent-suite-blocking-resources.md in the bundle-content regression.
- Require Status: Completed while preserving the regression coverage for the resolved User Action Required history and analysis type.
- Update each of the three follow-up feature items to link to the completed analysis archive using the correct relative path.
- Preserve the completed classification artifact and its historical resolution without moving or rewriting its lifecycle evidence.
- Keep agent and skill definitions, generated outputs, and unrelated backlog content unchanged.

## Acceptance Criteria

- The focused bundle-content regression reads the archived classification and passes with Status: Completed.
- Every tracked reference from the three follow-up feature items resolves to backlog/completed-backlog/analyses/classify-agent-suite-blocking-resources.md.
- No tracked current reference retains backlog/analysis-backlog/classify-agent-suite-blocking-resources.md.
- The complete scripts unit-test suite passes without the former archived-analysis assertion failure.
- The completed classification remains in the analysis archive with its existing resolution and completion evidence intact.

## Dependencies

None.

## Verification

- Run the focused BundleContentTests test for separation of User Action Required from dispatchable work.
- Sweep tracked files for the former active classification path and confirm no current reference remains.
- Validate that all three corrected Markdown links resolve to the completed analysis file.
- Run the complete scripts unit-test suite.
- Run Git diff validation.

## Completion Evidence

- Source contribution 9e74c89709769e5f786e1091f54de045eba39b1e corrected the bundle-content regression and passed focused Python 3.11 verification and Git diff validation from a clean isolated worktree.
- Fresh source review accepted the contribution with no findings.
- Backlog contribution 3929018b136fb093e9633c2394448f7e122f48b4 corrected only the three authorized feature links and released exact backlog ownership normally at event 25cceafd-6bb6-47b3-96d2-da33c62d00f2.
- Fresh artifact review accepted the three-link contribution with no findings and confirmed every link resolves to the completed analysis archive.
- The source contribution was preserved as provenance-bearing integrated commit 9543d3ba0ef89431ab04bce1bd3a4937b1da65cf without overlap from the separate lifecycle regression work.
- Shared integration c50233b73a9097872cae9760037895e6f404a715 and terminal documentation commit f476be76d01c978a24ea58d47999b659fba24dd4 passed fresh post-integration reviews and complete verification.
- Fresh defect-specific post-integration source and artifact reviews accepted tested main 5864b1908940c5ea39b3345241e437687ed79313 with no findings.
- The focused archive regression passed one test under Python 3.11.
- The complete scripts suite passed all 450 tests under Python 3.11.
- The verifier confirmed both contribution commits are ancestors of tested main, all three links use the completed archive target, the archive records Status: Completed and Type: Analysis, no former active relative link remains in the three feature files, Git diff validation passes, and the checkout is clean.
- Verification resource claim test:bundle-content and test:scripts released no-change at event 00622e74-fa46-4a5d-a905-9eb3dcb9236b.
- Terminal lifecycle claim correct-agent-suite-classification-archive-references-terminal acquired PRIMARY exact-path backlog ownership at event 0cbaf38e-aebe-478a-9889-d325acf21f6b from clean baseline 5864b1908940c5ea39b3345241e437687ed79313.

## Notes

- Use the simple-workitem delivery process and produce a verified local commit without a push or pull request.
- Keep backlog lifecycle claims separate from project-file and integration ownership.
- Require fresh source review, fresh artifact review, and independent verification before completion and archival.
