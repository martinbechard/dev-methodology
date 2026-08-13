# Avoid Re-Home Terminology and Use Plain Language

Status: Running

Type: Defect

Provider: file

Work Item ID: avoid-re-home-terminology-and-use-plain-language

Completion: main-branch

## Summary

Add re-home to the Terminology Standard's avoided terms and replace it in current methodology with direct descriptions of the actual action.

## Context

Current coordination text uses re-home to mean assigning work, a review, or a task to another compatible task, runtime, or Agent. The term is jargon and does not tell readers which of those actions will occur. It caused a direct user clarification request after the phrase was used to explain recovery from an unavailable reviewer environment.

The active project terminology.md already defines Work item as the preferred concept and uses Avoid sections only for observed misleading substitutions. Current maintained uses include skills/coordinate-codex-tasks/SKILL.md and skills/backlog-dispatcher/SKILL.md. The active Work item remediate-inherited-supported-test-baseline-failures also contains the ambiguous term in its pending review-recovery decision.

## Source Evidence

On 2026-08-11 in Codex task 019ff2f9-0863-7133-aac0-ff141cf16a92, the user stated: "Re-home is jargon, add a workitem to put it on the \"don't use\" terminology list because it is not good and clear english. Then repeat your explanation using undestandable terminology".

## Requirements

- Add re-home and its grammatical variants to the appropriate Avoid entry in terminology.md.
- Explain that re-home is unclear because it hides whether the action assigns a Work item to another task, runs a review in another task or runtime, replaces an Agent, or moves an execution environment.
- Require writers to name the concrete action in plain language, such as assign the work to another task, run the review in another compatible task, use a runtime that can load the required skills, or replace the Agent.
- Replace re-home terminology in current maintained skills, role sources, design documentation, generated Agent configuration, tests, and active Work-item content with the accurate action for each context.
- Preserve exact identifiers, historical quotations, claim identifiers, and archived Work-item evidence when re-home is retained as source-native evidence rather than current guidance.
- Add focused terminology coverage that rejects new current-guidance uses of re-home while allowing explicitly classified historical or source-native evidence.
- Regenerate every generator-owned artifact through its owning generator rather than editing generated output directly.

## Acceptance Criteria

- terminology.md includes an Avoid rule for re-home that gives clear action-specific replacements.
- No current maintained methodology or user-facing language uses re-home as an unexplained action.
- skills/coordinate-codex-tasks/SKILL.md describes the Coordinator's recovery choice in direct language.
- skills/backlog-dispatcher/SKILL.md states the reviewer's prohibited actions without using re-home.
- The active review-recovery decision for remediate-inherited-supported-test-baseline-failures uses understandable language.
- Focused tests fail when re-home is reintroduced into current guidance and pass for classified historical evidence, exact identifiers, and quotations.
- Applicable terminology, skill, role, generated-output freshness, and Git diff checks pass.
- Fresh independent terminology, methodology, source, and verification review accepts the final wording.

## Dependencies

None.

## Verification

- Load the active Terminology Standard and verify the published entry after mutation through the terminology-standard update workflow.
- Search current maintained sources, active Work items, and generated outputs for re-home and its grammatical variants; classify every retained match.
- Run focused terminology-standard, Codex coordination, backlog-dispatcher, bundle-content, and generated-output freshness checks affected by the changes.
- Validate each changed skill or role source and run Git diff checks.
- Obtain fresh independent review and verification of clarity, semantic preservation, and exception handling.

## Open Questions

None.

## Notes

- This defect targets current guidance and user-facing language. It does not rewrite archived Work items or source-native historical evidence solely for terminology modernization.
- The terminology change must preserve the underlying recovery choices and authority boundaries.

## Starting Handoff Evidence

- Reserved At: 2026-08-13T15:43:10Z.
- Transition: `Ready -> Starting`.
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Coordinator Execution: `/root/backlog_coordinator`.
- Baseline: `2e64e8000185dc3b207962ee7f6dbe01cb2aee31` on primary `main`.
- Priority: Oldest eligible process-correctness defect after provider-authority and Index delivery released their shared terminology and bundle-test boundaries.
- Capacity: Runs alongside `reconcile-offline-staging-and-strict-result-schema`; User Action Required, Blocked, and terminal items are excluded.
- Overlap: Offline owns only runner staging, Dev Orchestrator fixture tests, and its plan pair. This task must claim exact terminology, coordination-skill, focused-test, and mechanically required generated paths before mutation. It must not touch Offline paths or unrelated plan artifacts.
- Dispatch Architecture: Create one visible Codex task whose initial prompt launches one Dev Orchestrator subagent and states the visible root title-and-messaging responsibility.
- Transition Claims: Work Item `start-avoid-rehome-terminology-work-item`; event `de86c91d-a756-4225-93c9-ad94d648014c`. Provider `start-avoid-rehome-terminology-provider`; event `da5011ff-50e2-403b-b2a2-9fa4c94b27a5`.
- Canonical Codex Task ID: `019ffbcc-b014-72e0-b6bc-ea5925712b74`.
- Canonical Conversation ID: `019ffbcc-b014-72e0-b6bc-ea5925712b74` (combined runtime identity).
- Runtime Host: `local`.
- Runtime Project: saved `dev-methodology` project at `/Users/martinbechard/dev/dev-methodology`.
- Runtime Created At: `2026-08-13T15:45:23Z` (`1786635923`).
- Requested Title: `Starting — Avoid Re-Home Terminology And Use Plain Language`; the runtime preview is ellipsized only.
- Runtime Creation Outcome: Unique success with no client or pending identity. Creation does not imply Running.

## Running Acceptance Evidence

- Accepted At: 2026-08-13T15:46:55Z.
- Transition: `Starting -> Running`.
- Canonical Codex Task ID: `019ffbcc-b014-72e0-b6bc-ea5925712b74`.
- Canonical Conversation ID: `019ffbcc-b014-72e0-b6bc-ea5925712b74`.
- Executing Agent: `dev-orchestrator:/root/avoid_re_home_terminology`.
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Coordinator Execution: `/root/backlog_coordinator`.
- Work Claim: `avoid-re-home-terminology-work`; event `803910c4-bdbd-4b6f-907c-725f4fb69ab4`.
