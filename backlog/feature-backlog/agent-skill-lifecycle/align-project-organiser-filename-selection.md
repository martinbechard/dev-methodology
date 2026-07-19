# Align Project Organiser Filename Selection

Status: Blocked

Type: Defect

## Running Ownership

- Owner: Dev Orchestrator root task 019f77f4-c4bd-7c91-b197-c987a7beb838.
- Lifecycle claim: align-project-organiser-filename-selection-start.
- Claim evidence: dev-backlog-steward acquired PRIMARY ownership of this exact backlog item at 2026-07-19T03:15:20.949615Z before recording the Running transition.
- Scope boundary: the lifecycle claim is released after this committed transition; project-artifact ownership must be acquired separately before implementation.

## Target Merge Pending

- Delivery contribution: commit 2d636dd0f240793820778031ab9d38db6c11ee60 on branch codex/align-project-organiser-filename-selection-impl, based on sibling commit 4a31b337e6baf241de5ec81eb3a3c924096f3c82.
- Review: fresh independent review passed with no findings.
- Verification: focused tests passed 3 of 3; repository validation and freshness checks passed; project-wiki tests passed 17 of 17; all three Project Organiser scenarios retained deterministic and independent Judge PASS evidence.
- Integration boundary: the contribution is not present on main and must be deliberately integrated without overwriting its sibling base change before completion.

## Integration Blocker

- Attempted integration: dev-merge-coordinator acquired PRIMARY ownership of this exact backlog item plus merge:integration:main in event 0143a4da-7519-4e61-aabe-1c5409f56840 and attempted accepted commit 2d636dd0f240793820778031ab9d38db6c11ee60, stable patch id cd87d184bb55153bb0b3a27033fe915adb89c00b, against clean main baseline b0410174ce8127686ce89b3d1e1faefde8b6b112.
- Conflict evidence: cherry-pick produced a content conflict in scripts/test_bundle_content.py, and an independent git apply --check failed at the accepted patch's old line-2203 context.
- Scope boundary: the explicit user direction required stopping on applicability ambiguity rather than adapting the accepted test or absorbing sibling content.
- Restoration evidence: the coordinator aborted the cherry-pick, restored the exact clean baseline, created no integration commit, ran no post-integration tests, and released ownership with no change in event 6082defa-4b29-4cdf-80c8-a87548ac4ec6.
- Excluded content: rejected commits 4a31b337e6baf241de5ec81eb3a3c924096f3c82, 68ea9d4, and 13217749 remain non-ancestors of main; none of their content was integrated by this attempt.
- Next action: a fresh explicit user decision must authorize adapting the accepted regression test to current main, or provide a replacement accepted commit. That authority is not inferred from the failed integration assignment.

## Summary

Remove the generated Project Organiser adapter conflict that simultaneously requires the agent to choose an approved artifact path and prohibits it from choosing filenames.

## Context

The Project Organiser conceptual role owns repository placement decisions. Its contract requires choosing an approved destination, validating the filename against repository guidance, and returning the selected path with placement-audit evidence.

The generated Codex adapter also inlines the structured-design response-only rule that says not to choose filenames. That prohibition is valid for response-only design work, but it contradicts the Project Organiser role when filename and destination selection are the requested output.

The complete conceptual-agent suite rollout confirmed the conflict while freezing the Project Organiser role, generated adapter, and assigned skill rules. The evaluation infrastructure did not edit the subject contract.

## Evidence

- agents/roles/project-setup/project-organiser.role.yaml lines 4 through 7 require repository placement decisions.
- agents/roles/project-setup/project-organiser.role.yaml lines 19 through 23 require filename validation.
- agents/roles/project-setup/project-organiser.role.yaml lines 49 through 54 require the approved path and placement audit in the result.
- generated/adapters/codex/agents/project-organiser.toml lines 624 through 627 contain the conflicting prohibition against choosing filenames.
- evals/agent-tests/project-organiser contains the frozen executable suite that exposed the conflict.

## Requirements

- Preserve response-only structured-design behavior when no artifact authoring or placement decision is requested.
- Permit Project Organiser to choose a filename and destination when its canonical role owns that decision.
- Express the exception in the reusable source contract rather than editing generated adapters by hand.
- Regenerate all native adapters and documentation derived from the changed source.
- Add regression coverage proving that the Project Organiser contract and inlined skills contain no contradictory filename rules.

## Acceptance Criteria

- The canonical Project Organiser role still requires an approved path and placement audit.
- The generated Codex Project Organiser adapter permits required filename selection.
- Response-only structured-design requests continue to avoid unauthorized artifact creation.
- Generated adapters are fresh and repository contract tests pass.
- The Project Organiser executable scenarios can be rerun without freezing contradictory authority.

## Dependencies

None.

## Verification

- Run the focused generated-adapter and bundle-content tests.
- Run Agent Skill validation and every generated-output freshness check.
- Run the Project Organiser suite scenarios and inspect retained identity and Judge evidence.
- Run repository unit tests and Git diff validation.

## Notes

- Do not patch generated/adapters/codex/agents/project-organiser.toml directly.
- Keep the correction scoped to mode-aware filename authority; do not broaden artifact-writing permission.
