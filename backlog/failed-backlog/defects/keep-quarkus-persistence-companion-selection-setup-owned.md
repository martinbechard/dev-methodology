# Keep Quarkus persistence companion selection setup-owned

Status: Abandoned

Type: Defect

Provider: file

Provider Reference: backlog/failed-backlog/defects/keep-quarkus-persistence-companion-selection-setup-owned.md

Completion: direct-main

Owner: Unowned

Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758

Parent Agent Task: 019fa9bb-1423-7e80-bcde-3caa765e3758

Launch Reservation: reserve-six-ready-refill-019fa9bb

Normalized Objective: Keep Quarkus persistence companion selection setup-owned.

Dispatch Time: 2026-07-28T20:53:27Z

Intended Root Role: Dev Orchestrator

Runtime Thread: 019faa83-d39e-7020-a285-4d2d3d2d1767

Root Agent Task: 019faa83-d39e-7020-a285-4d2d3d2d1767

Branch: codex/keep-quarkus-persistence-setup-owned-019faa83

Worktree: /Users/martinbechard/.codex/worktrees/562f/dev-methodology

Reservation Commit: 3e0692b60a3694f29f3b8e05f399212c31bc1573

Running Acceptance Commit: 6fc8044a75fe46bf80c9954821ed177b817383dd

User Action Required Commit: 0f7ffee03d9328b001dd1e2af849944646b50d8d

Phase: terminal abandonment

Claim Evidence: Prior recovery evidence: failed claim journal event 46ea90ff-e0e6-4ff1-919f-033cbc589a9f. Running acceptance: SHARED_CHECKOUT_ACQUIRED claim accept-quarkus-persistence-running-019faa83; acquisition journal event 2b164214-b8aa-4a66-9a7f-4fe0fb291b9c; RELEASED journal event fb975c37-1245-44be-a7c1-a64ecd8b8599. User Action Required move: SHARED_CHECKOUT_ACQUIRED claim uar-quarkus-persistence-019faa83; acquisition journal event e345981b-699a-4007-ac6a-3d13d33af316; RELEASED journal event c70c808a-3382-45fd-a922-26f66466fb18. Terminal abandonment: SHARED_CHECKOUT_ACQUIRED claim abandon-quarkus-persistence-019faa83; acquisition journal event 76fa6258-6df5-4806-a38c-962684497d3c. Release evidence follows the committed provider transaction.

## Terminal Abandonment

Disposition Authority: Dev Backlog Coordinator terminal disposition on 2026-07-28.

User Provenance: On 2026-07-28, the user stated: “First of all in general the tech skills are wired into AGENTS.md and by default that's what's loaded, the Dev Coder doesn't have any special instructions for loading technology-specific skills. Second there can be additional skills needed at runtime through the harness skill mechanism - we're not going to override that with a prompt. So this request doesn't really make sense” and “the linter is supposed to judge the writing quality and coherence, not what the prompt seeks to achieve”.

Rationale: The defect incorrectly conflated AGENTS.md setup-configured technology-skill loading with prompt-level selection and ignored harness runtime skill injection. The user declined the requested governed definition change, so no technically coherent authorized delivery remains.

No Artifact Mutation Evidence: No skills/quarkus-persistence definition, references, tests, generated mirrors, candidate, delivery, or integration mutation occurred. The only work for this item is the provider lifecycle record in commits 6fc8044a75fe46bf80c9954821ed177b817383dd, 0f7ffee03d9328b001dd1e2af849944646b50d8d, and this terminal provider commit.

## User Action Required

Exact Question: “Do you explicitly approve changing the governed canonical skill definition skills/quarkus-persistence/SKILL.md so runtime work consumes the setup-supplied persistence companion and reports missing or stale routing instead of selecting a companion from source evidence?”

Why: The supported preflight command returned a governed-definition approval block.

```text
python3 scripts/render-agents-technology-skills.py --project PROJECT.yaml --check-definition-change skills/quarkus-persistence/SKILL.md
{"classification":"governed-definition","outcome":"BLOCKED_APPROVAL_REQUIRED"}
```

Blocker Owner: User

Approval Scope: Approval authorizes no other governed definition. Associated non-definition reference and test work remains bounded by this defect. Only supported generated/adapters/** and design/generated/skill-definitions.js mirrors may be regenerated from the approved distributed-skill source; they must never be hand-edited.

Resumption Requirement: Record dated explicit answer provenance and an approval record naming the exact path. Resume through User Action Required -> Ready -> Starting -> Running in this same canonical task, then pass the supported preflight with that record.

Concrete Example: Before, runtime sees pom.xml with quarkus-hibernate-orm-panache and selects or loads hibernate-orm-panache itself. After, setup supplies quarkus-persistence plus hibernate-orm-panache for the blocking route, runtime consumes that active-scope companion, a reactive route stays distinct, and runtime reports a missing or stale companion instead of inventing one.

Options and Consequences:

- Approve authorizes only this exact governed definition and bounded supported regeneration after normal lifecycle resumption.
- Defer moves the item to Holding with no definition, source, or generated mutation.
- Decline ends the defect as Abandoned with no such mutation.

Unattended Stop: No definition, source, reference, test, generated, candidate, delivery, or integration mutation may continue. Only read-only preservation and lifecycle reconciliation may continue.

## Summary

Keep Quarkus persistence companion selection setup-owned.

## Context

The primary affected skill is skills/quarkus-persistence/SKILL.md. The package repeatedly directs ordinary runtime actors to select a blocking persistence companion from source evidence even though setup-time detection owns that decision and intentionally distinguishes blocking from reactive Panache.

## Source Evidence

The user authorized this independently dispatchable Ready Defect record on 2026-07-28. The accepted methodology skill-lint report at evals/results/2026-07-28-methodology-skill-lint.md, commit 54d860f1978d4cb403e59162cfb209fe45cc06a8, records this finding at 16; skills/quarkus-persistence/references/persistence-guidelines-quarkus.md:20; skills/quarkus-persistence/references/review-checklist-quarkus-persistence.md:4. Independent reviewer /root/confirm_new_routing_findings accepted it as CONFIRMED_CRITICAL.

## Requirements

- Consume only an active-scope companion already supplied by setup and report missing or stale routing.
- Preserve the documented ownership boundary and avoid unrelated provider, source, report, analysis, generated, or lifecycle mutation.

## Acceptance Criteria

- Runtime work never invents a persistence companion.
- Setup-owned blocking and reactive routing remains distinct in the skill, guideline, and direct checklist.
- The correction remains limited to the smallest source-backed scope.

## Dependencies

None

## Verification

- Preserve blocking and reactive detector cases.
- Assert that runtime work never invents a companion.
- Run focused contract validation and git diff --check.
- Obtain independent review of the defect correction.

## Open Questions

None

## Notes

Collision reconciliation before creation found no active item with this provider reference, slug, affected skill, or overlapping accepted outcome.

This record has one primary affected skill identity: skills/quarkus-persistence/SKILL.md. It does not authorize a skill-definition mutation. If correction changes this governed SKILL.md, later implementation requires explicit scope-specific user approval naming that exact definition, a provenance approval record, and the supported pre-mutation definition-change check. Any additionally changed governed SKILL.md requires its own separate exact-path approval and check.
