# Allow Direct-Main Delivery With Unrelated Dirty Primary Files

Status: Running

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/allow-direct-main-delivery-with-unrelated-dirty-primary-files.md

Owner: Root Dev Orchestrator

Completion: direct-main

## Current Dispatch Reservation

Transition: Ready -> Starting.
Parent Coordination Thread: 019fb057-1767-7ef2-b5fa-41f4417b20b3.
Launch Reservation: One distinct bounded launch reservation for this provider record.
Normalized Objective: Allow direct-main delivery with unrelated dirty primary files.
Dispatch Time: 2026-08-05T14:39:34Z.
Intended Root Dev Orchestrator Role: Dev Orchestrator.
Owner: Unowned pending accepted root.
Current Launch Evidence: Parent Coordinator authorized this exact reservation; exact-file backlog claim starting-direct-main-unrelated-dirty-019fb057 acquired with outcome SHARED_CHECKOUT_ACQUIRED and event 793f541f-f05b-4678-b2c6-5d8c70df3ecd. Runtime Thread creation and root acceptance have not occurred.
Required Next Lifecycle Transition: The root Dev Orchestrator must separately accept Starting -> Running before repository mutation.
Reconciliation: Pending.

## Current Running Acceptance

Transition: Starting -> Running.
Canonical Thread: 019fd25f-7adb-7490-bdb8-b73aadc8e79b.
Root Agent Task: 019fd25f-7adb-7490-bdb8-b73aadc8e79b.
Owner: Root Dev Orchestrator.
Branch: main.
Worktree: /Users/martinbechard/dev/dev-methodology.
Phase: Implementation.
Started At: 2026-08-05T14:47:10Z.
Claim Evidence: This exact primary-main backlog mutation is protected by exact-file claim provider-running-direct-main-unrelated-dirty-019fd25f-stage, acquired with outcome SHARED_CHECKOUT_ACQUIRED and event f5778dec-a0d6-4902-9c2e-f9ba4050b2c3.
Preserved Coordination: Parent Coordination Thread 019fb057-1767-7ef2-b5fa-41f4417b20b3 and its Ready -> Starting launch reservation remain canonical.

## Summary

Correct the direct-main delivery contract so an accepted, reviewed contribution can be integrated safely when primary main contains unrelated, non-overlapping dirty working-tree state, without losing the normal clean-main route or weakening delivery evidence.

## Context

The canonical direct-main skill currently requires the intended integration checkout to be clean before shared mutation and requires integrated verification and main observation from a clean integration checkout. The canonical agent-work-merge skill instead supports a fresh branch from current main that applies only accepted files or commits and records source-to-integration mapping. Repository maintenance guidance says unrelated changes do not block a scoped commit and must remain untouched.

Together, these rules create a verified contradiction: unrelated, non-overlapping ownerless dirty state on primary main can indefinitely block direct-main delivery even after independent review and verification accept the contribution. The correction must preserve provider closure as a separate Persistence transaction.

## Source Evidence

The user explicitly requested this defect in canonical task 019faec8-943a-7902-adaa-c2c00a370169 on 2026-08-05: "This is contradictory? It seems like direct-main needs to be fixed", then: "ok create the defect then advise the backlog coordinator that this is high priority and should be taken care of before dispatching or unblocking further tasks".

The contradiction is verified against canonical skills/complete-work-item-direct-main/SKILL.md, which requires a globally clean configured-main checkout; skills/agent-work-merge/SKILL.md, which requires fresh-current-main exact-content reconciliation; and .agents/skills/dev-methodology-repository-maintenance/SKILL.md, which requires unrelated changes to remain untouched and not block scoped commits.

## Requirements

- Preserve a globally clean configured main checkout as the normal direct-main delivery route.
- Add a safe unrelated-dirty route in skills/complete-work-item-direct-main/SKILL.md only.
- Require proof that accepted paths and the Git index do not overlap dirty paths before mutation.
- Capture unrelated dirty diff, bytes, and index state before integration mutation.
- Apply only accepted files or commits and record exact source-to-integration mapping.
- Run post-integration verification from a clean checkout of the resulting main tip when dirty working-tree content could contaminate checks.
- Prove unrelated dirty state remains byte-for-byte and index-for-index preserved after integration.
- Distinguish preserved unrelated dirt from integration residue.
- Reject overlap, ambiguous ownership or state, unsafe staged state, and unbounded commit scope.
- Do not require stash, reset, discard, or provider mutation by the Commit skill.
- Preserve the existing separation between Commit delivery and provider closure.

## Acceptance Criteria

- The clean-main normal route remains explicitly supported without weakened evidence requirements.
- A non-overlapping, unstaged unrelated dirty file can remain byte-for-byte preserved while an exact-path accepted contribution is delivered to main.
- Overlapping dirty paths, unsafe staged state, ambiguous preservation evidence, and unbounded commit scope return BLOCKED without discarding state.
- Direct-main delivery records exact source-to-integration mapping and observes the resulting main tip from a clean verification checkout when needed.
- The delivery result distinguishes unrelated preserved dirt from integration residue and does not perform provider lifecycle mutation.
- Only skills/complete-work-item-direct-main/SKILL.md changes among governed canonical sources.

## Dependencies

None.

## Verification

- Run the supported definition-change precheck for skills/complete-work-item-direct-main/SKILL.md using an approval record that cites this item's exact approval evidence.
- Add or update regression coverage for the clean-main normal path, unrelated unstaged dirty-file preservation during exact-path integration, overlap rejection, unsafe staged or ambiguous-preservation rejection, exact source-to-integration mapping, clean verification checkout and current-main observation, and no provider mutation by the Commit skill.
- Run scripts/test_direct_main_completion_contract.py and the focused direct-main skill probe.
- Run supported regeneration and generated-output freshness checks for this skill source.
- Run git diff --check and obtain independent review and verification.

## Open Questions

Determine the smallest safe Git mechanism and evidence representation that preserve unrelated dirty bytes and index state without weakening current-main reachability.

## Governed Definition Approval

### Governed Canonical Sources

- skills/complete-work-item-direct-main/SKILL.md

### Allowed Dependent Artifacts

- generated/adapters outputs regenerated from skills/complete-work-item-direct-main/SKILL.md.
- design/generated/skill-definitions.js.
- scripts/test_direct_main_completion_contract.py.
- Relevant evaluation fixtures or probes only when consumed by the changed direct-main contract.
- design/work-item-provider-and-completion-contracts.md and design/orchestrated-development-lifecycle.html only when directly needed.

### Approval Resolution

Approved at creation on 2026-08-05 by the user's exact request in canonical task 019faec8-943a-7902-adaa-c2c00a370169: "This is contradictory? It seems like direct-main needs to be fixed", then: "ok create the defect then advise the backlog coordinator that this is high priority and should be taken care of before dispatching or unblocking further tasks". Approval is limited to skills/complete-work-item-direct-main/SKILL.md. It does not authorize skills/agent-work-merge/SKILL.md or any other governed canonical source.

## Notes

Scheduling Priority: High.

Coordinator Directive: Take care of this defect before dispatching or unblocking further tasks. The Dev Backlog Coordinator must reconcile shared-path sequencing with backlog/feature-backlog/apply-object-oriented-skill-group-design/align-integration-and-delivery-skills.md. That related feature owns renames and interfaces while preserving internal direct-main procedures; it is not a duplicate and is not a hard dependency for this defect.

No stash, reset, discard, broad commit, or provider closure is authorized by this item creation.
