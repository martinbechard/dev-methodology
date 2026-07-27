# Configure Persistence When Backlog Coordination Is First Requested

Status: Completed

Type: Defect

Owner: Unowned

Claim: None

Provider: file

Provider Reference: backlog/completed-backlog/defects/align-coordinator-unset-selection-with-user-action-required-reconciliation.md

Completion: direct-main

## Summary

Allow Persistence to remain UNSET while a project performs manual work without a backlog. When the Dev Backlog Coordinator is first asked to manage work items, ask the user whether to configure the available file-backed provider, update PROJECT.yaml after approval, and safely regenerate project guidance without overwriting user-modified AGENTS.md content.

## Context

A project may be configured before it needs durable work-item management. Requiring a Persistence provider during initial setup would force an unnecessary decision.

Persistence becomes required when the user asks the Dev Backlog Coordinator to create or manage work items. At that point, the Coordinator must not guess a provider. If the file-backed provider is the only available option, it should ask whether to use that provider for now.

Updating PROJECT.yaml may change generated AGENTS.md guidance. AGENTS.md may also contain user-written project directives, so regeneration must not overwrite it blindly.

## Requirements

- Permit Persistence to remain UNSET while the project is not using managed work items.
- Detect UNSET when the Dev Backlog Coordinator is asked to create or manage work items.
- Ask the user whether to configure the currently available file-backed provider.
- Do not create work items or infer a provider before the user answers.
- After approval, update PROJECT.yaml to select the file provider.
- Generate the proposed AGENTS.md content into a separate candidate file.
- Diff the candidate against the existing AGENTS.md.
- Have the agent review and apply the differences while preserving user-written project directives.
- Move reusable project-specific directives into project-specific configuration or skills when appropriate, then reference them through PROJECT.yaml.
- Regenerate the candidate after relocating directives and confirm that the resulting AGENTS.md preserves the project's behavior.
- Apply the reconciled AGENTS.md only after the review is complete.
- Continue the original Coordinator request after configuration and guidance reconciliation succeed.

## Acceptance Criteria

1. A project can retain Persistence: UNSET while no backlog operation is requested.
2. The first backlog-management request produces one clear provider question instead of guessing or reporting an unexplained failure.
3. Approval updates PROJECT.yaml to select the file-backed provider.
4. Guidance generation writes to a separate candidate file and does not overwrite AGENTS.md.
5. The agent receives a clear diff between the existing AGENTS.md and the generated candidate.
6. User-written project directives remain present after reconciliation.
7. Project-specific directives that should survive future regeneration are represented through project-specific configuration or skills referenced by PROJECT.yaml.
8. The final AGENTS.md is generated and applied only after the agent verifies the reconciliation.
9. The original Coordinator request resumes without requiring the user to repeat the provider decision.
10. An explicit Persistence value of none remains distinct from UNSET and is not silently changed to file.

## Verification

- Test project setup with Persistence left UNSET and no backlog operation.
- Test the first Coordinator backlog request with approval of the file provider.
- Test decline or deferral without changing PROJECT.yaml or AGENTS.md.
- Test candidate-file generation and diff production.
- Test an existing AGENTS.md containing user-written project directives and prove they survive reconciliation.
- Test explicit Persistence: none separately from UNSET.
- Run the focused project-configuration and Coordinator tests affected by the change.
- Run git diff --check.

## Dependencies

None.

## Notes

This work item does not authorize blind regeneration of AGENTS.md. The generated candidate is review input. The agent owns the semantic reconciliation and must preserve project-specific behavior before applying the final file.

## Completion Evidence

- Implementation commit: 527334ed
- Persistence UNSET now produces a direct file-provider question when that provider is available.
- The generated guidance requires a separate AGENTS.md.candidate, comparison with the existing AGENTS.md, preservation of project directives, and resumption of the original request.
- Explicit Persistence none remains unchanged.
- Coordinator simulator tests: 23 passed.
- Focused renderer tests: 2 passed.
- Git diff check passed.
