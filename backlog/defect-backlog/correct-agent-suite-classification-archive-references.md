# Correct Agent Suite Classification Archive References

Status: Ready

Type: Defect

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

## Notes

- Use the simple-workitem delivery process and produce a verified local commit without a push or pull request.
- Keep backlog lifecycle claims separate from project-file and integration ownership.
- Require fresh source review, fresh artifact review, and independent verification before completion and archival.
