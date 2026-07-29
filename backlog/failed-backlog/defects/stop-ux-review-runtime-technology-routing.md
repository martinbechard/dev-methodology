# Stop UX review from performing runtime technology routing

Status: Abandoned

Type: Defect

Provider: file

Provider Reference: backlog/failed-backlog/defects/stop-ux-review-runtime-technology-routing.md

Completion: direct-main

Owner: Unowned

Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758

Launch Reservation: reserve-six-ready-defects-019fa9bb

Normalized Objective: Stop UX review from performing runtime technology routing.

Dispatch Time: 2026-07-28T19:19:58Z

Intended Root Role: Dev Orchestrator

Runtime Thread: 019faa2d-2ffa-75c0-80d5-e4192730b94a

Root Agent Task: 019faa2d-2ffa-75c0-80d5-e4192730b94a

Branch: codex/stop-ux-review-runtime-routing-019faa2d

Worktree: /Users/martinbechard/.codex/worktrees/c058/dev-methodology

Phase: Read-only defect analysis pending exact governed-definition approval.

Started At: 2026-07-28T19:27:14.127814Z

Claim Evidence: SHARED_CHECKOUT_ACQUIRED claim starting-to-running-ux-runtime-technology-routing-recovery-019faa2d; acquired 2026-07-28T19:27:14.127814Z; claim journal event d1355d1f-0b69-4a3c-ab00-946d30a0532d; exact file scope backlog/defect-backlog/stop-ux-review-runtime-technology-routing.md; primary-main baseline f0f5c17a6af52fdcf332fc7cf48e7c0b49ee98ef.

Recovery Evidence: The prior acceptance attempt was preserved without mutation after DIRTY_CHECKOUT_RECOVERY_AUTHORIZATION_REQUIRED, claim journal event 15c488a5-e39b-4f79-9e6b-2259c3b8dcff. Dev Backlog Coordinator recovery notification confirmed the unrelated TypeScript ESM acceptance as provider-only commit f0f5c17a6af52fdcf332fc7cf48e7c0b49ee98ef, with claim acquire event 04eb821a-8352-40b8-b37f-81705e60f4bd and release event 1828d51c-d8e3-416a-a26a-22a8ac029a6a; primary main was then reconciled clean.

Next Lifecycle Owner: Root Dev Orchestrator

## User Action Required

Exact Question: Do you approve changing only skills/user-experience-review/SKILL.md so UX reviewers use technology guidance already supplied for the active folder and report a missing route instead of selecting or loading guidance from repository evidence? This approval covers no other skill or agent definition. Focused tests and supported generated mirrors would follow from that approved source change.

Why User Input Is Required: Supported pre-mutation check python3 scripts/render-agents-technology-skills.py --project PROJECT.yaml --check-definition-change skills/user-experience-review/SKILL.md returned {"classification":"governed-definition","outcome":"BLOCKED_APPROVAL_REQUIRED"}; repository policy requires explicit exact user direction and dispatch/repair authority is not approval.

Exact Governed Scope: skills/user-experience-review/SKILL.md, semantically workflow item 2 only.

Exclusions: agents/roles/dev-activities/dev-ux-specialist.role.yaml, skills/user-experience-review/references/review-checklist-user-experience-review.md, skills/user-experience-review/agents/openai.yaml, every other skill/agent definition, design/generated/role-definitions.js, and direct hand edits to all generated mirrors.

Supported Post-Approval Regeneration Only: generated/adapters/** and design/generated/skill-definitions.js from the approved distributed-skill source; regeneration does not broaden approval.

Unattended Stop: Stop governed-definition mutation, test/candidate production that depends on the change, regeneration, delivery, and integration; only read-only preservation/reconciliation may continue.

Evidence: Accepted lint report evals/results/2026-07-28-methodology-skill-lint.md:408-418; source skills/user-experience-review/SKILL.md:15; owning role agents/roles/dev-activities/dev-ux-specialist.role.yaml:6-8,64; bounded read-only reviewer found no code/test-only correction can satisfy acceptance and confirmed exact one-file scope.

## Abandonment Evidence

Abandonment Authority: Explicit user decline in the canonical task on 2026-07-28.

User Decline Provenance: “Declined, skills routing is mostly done by the harness, and agents may be allowed to request more skills to be loaded if it makes sense.”

Rationale: Routing is primarily harness-owned and agents may be permitted to request additional skills when appropriate. This rationale does not authorize any different governed definition, replacement work item, or new feature.

Post-Answer Mutation Evidence: After the answer, this task changed no source, test, generated mirror, governed definition, or provider record before this authorized terminal provider transaction. The only task-state actions were title/update and Coordinator notification.

Delivery Evidence: No implementation candidate or delivery commit exists. Completion direct-main was not attempted because the exact requested definition change was declined. No approval provenance may be inferred or manufactured.

## Summary

Stop UX review from performing runtime technology routing.

## Context

The primary affected skill is skills/user-experience-review/SKILL.md. The skill tells an ordinary UX reviewer to route specialized guidance from repository evidence even though Project Configurator owns setup routing and Dev UX Specialist consumes supplied active-scope guidance.

## Source Evidence

The user authorized this independently dispatchable Ready Defect record on 2026-07-28. The accepted methodology skill-lint report at evals/results/2026-07-28-methodology-skill-lint.md, commit 54d860f1978d4cb403e59162cfb209fe45cc06a8, records this finding at 15; agents/roles/dev-activities/dev-ux-specialist.role.yaml:6,64. Independent reviewer /root/confirm_new_routing_findings accepted it as CONFIRMED_CRITICAL.

## Requirements

- Use only technology guidance already supplied for the active folder and report a routing gap when required guidance is missing.
- Preserve the documented ownership boundary and avoid unrelated provider, source, report, analysis, generated, or lifecycle mutation.

## Acceptance Criteria

- UX review consumes active-scope guidance without ad hoc technology routing.
- A missing required route is reported rather than inferred.
- The correction remains limited to the smallest source-backed scope.

## Dependencies

None

## Verification

- Provide repository evidence for an un-routed skill and require no ad hoc load.
- Run focused contract validation and git diff --check.
- Obtain independent review of the defect correction.

## Open Questions

None

## Notes

Collision reconciliation before creation found no active item with this provider reference, slug, affected skill, or overlapping accepted outcome.

This record has one primary affected skill identity: skills/user-experience-review/SKILL.md. It does not authorize a skill-definition mutation. If correction changes this governed SKILL.md, later implementation requires explicit scope-specific user approval naming that exact definition, a provenance approval record, and the supported pre-mutation definition-change check. Any additionally changed governed SKILL.md requires its own separate exact-path approval and check.
