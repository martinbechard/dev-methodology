# Orchestrate Template-First Artifact Review Checklists

Status: Ready

Type: Defect

Provider: file

Work Item ID: orchestrate-template-first-artifact-review-checklists

Completion: main-branch

## Summary

Make the Dev Orchestrator establish the applicable review-checklist artifact from its canonical template before artifact writing begins, then explicitly coordinate each writer-and-reviewer correction cycle around that same saved checklist instead of relying on delegated agents to remember the review protocol.

## Context

The current review skills require a completed checklist to precede findings, but the Inspect AI contract-mapping delivery reached three failed artifact reviews without the required adjacent checklist and findings files. The earlier completed Work Item `enforce-methodology-review-checklist-completion` enforced checklist saving for Methodology Artifact Reviewer results only. It did not make the Dev Orchestrator establish the checklist artifact before writing or systematically coordinate the general non-source writer/reviewer loop.

The desired steady-state sequence is:

1. The Dev Orchestrator resolves the applicable generic and artifact-specific checklist templates and exact output paths.
2. Before assigning artifact production, it causes one checklist artifact to be created from those templates with review trace and questions intact but evidence and assessments pending.
3. The artifact writer writes or corrects the artifact against the authoritative inputs and the staged checklist contract.
4. A fresh independent reviewer completes and saves that existing checklist, then derives findings or a pass result from it.
5. On correction, the Orchestrator sends the artifact and checklist-derived findings to the original writer, then assigns a fresh reviewer to update and complete the same checklist artifact for the new candidate. It does not create a new template copy for every cycle.
6. The Orchestrator rejects a review handoff when the required checklist artifact is missing, incomplete, not saved, or not the source of the findings.

## Source Evidence

The user directed this change on 2026-08-13 in canonical Codex Task `019ffbeb-02ee-7d52-9460-d1bfdbdbe20b`: “the orchestrator should first get the check list template created, then do a loop where the artifact writer writes the artifact, then the reviewer completes and saves the checklist but doesn't need to create the template again each time. So the orchestrator needs to help make these steps happen systematically instead of hoping the other agents remember.”

Repository evidence:

- `skills/review-structured-artifact/SKILL.md` requires the completed checklist to precede findings and names the adjacent checklist and findings outputs.
- `skills/review-structured-artifact/references/review-checklist-structured.md` requires the checklist to exist before findings and to trace all material input directives.
- `agents/roles/dev-activities/dev-orchestrator.role.yaml` currently requires independent artifact review and bounded correction loops but does not explicitly stage the checklist before writer assignment or validate the checklist artifact at each loop boundary.
- `backlog/completed-backlog/defects/enforce-methodology-review-checklist-completion.md` is narrower: it enforced saved-checklist results for Methodology Artifact Reviewer without defining this general Orchestrator-owned sequence.

## Requirements

- Update the Dev Orchestrator contract so every required non-source artifact review begins with resolution of the applicable generic checklist template plus any matching artifact-specific supplement.
- Require the Orchestrator to establish one exact checklist output artifact from the resolved template set before assigning the first artifact-writing pass.
- Keep checklist-template creation distinct from checklist completion: the initial artifact preserves template questions and review trace; the independent reviewer supplies evidence, assessments, corrections, authority, impact, and verdict after a candidate exists.
- Require the Orchestrator to pass the authoritative inputs, target path, checklist path, and intended review scope explicitly to the writer and reviewer.
- Require the writer to use the checklist as an observable acceptance contract while retaining ownership of artifact creation and corrections.
- Require each fresh independent reviewer to complete and save the existing checklist before producing findings or a pass verdict.
- Reuse the same checklist artifact across bounded correction cycles. Do not create another template copy merely because a fresh reviewer is assigned.
- Require the Orchestrator to validate that the checklist exists, is complete for the current candidate, and is the source of the returned findings before accepting the review result or advancing to verification.
- Preserve fresh-context reviewer independence, original-writer correction ownership, the existing three-failed-review limit, and all current reviewer zero-write boundaries for the target artifact.
- Clarify that authorized checklist mutation is review-evidence work and does not grant the reviewer ownership to modify the target artifact.
- Update supported generated role projections, focused contract tests, and aligned methodology documentation only where directly required by the canonical contract change.
- Do not redesign or expand the generic checklist questions as part of this defect.

## Acceptance Criteria

- A Dev Orchestrator cannot validly assign the first writing pass for a review-required non-source artifact until the applicable checklist template set and one exact checklist output path are resolved and the checklist artifact is established.
- Writer assignment names the target, authoritative inputs, checklist path, and review scope.
- Reviewer assignment names the same checklist path and requires completion and saving before findings or verdict.
- A correction cycle reuses the existing checklist artifact and assigns the original writer followed by a fresh independent reviewer.
- Orchestrator acceptance rejects a missing, incomplete, unsaved, stale-candidate, or findings-independent checklist.
- Focused tests cover the initial template-first sequence, checklist reuse on correction, invalid review rejection, and preservation of reviewer independence and the three-failure boundary.
- The generic checklist questions remain byte-for-byte unchanged unless a separately authorized Work Item changes them.
- Generated projections and affected documentation remain fresh and consistent with the canonical Dev Orchestrator definition.

## Dependencies

None.

## Verification

- Run focused Dev Orchestrator role-schema and generated-adapter contract tests.
- Run focused review-loop tests proving template-first creation, writer/reviewer handoffs, checklist reuse, and invalid-review rejection.
- Verify the generic checklist question set is unchanged.
- Regenerate supported role projections through the repository-authorized generator and check exact freshness.
- Independently review the changed orchestration contract and run `git diff --check` on the exact accepted scope.

## Open Questions

- Determine the smallest canonical helper or orchestration instruction that can establish the checklist artifact without transferring semantic review ownership to the Orchestrator.

## Governed Definition Approval

### Governed Canonical Sources

- `agents/roles/dev-activities/dev-orchestrator.role.yaml`

### Allowed Dependent Artifacts

- Supported generated Dev Orchestrator adapter projections.
- Focused tests that consume the Dev Orchestrator review-loop contract.
- Directly affected design documentation that describes the orchestrated review loop.

### Approval Resolution

Approved at creation by the user's explicit request on 2026-08-13 in canonical Codex Task `019ffbeb-02ee-7d52-9460-d1bfdbdbe20b` to make the Orchestrator systematically establish and coordinate the checklist-first writer/reviewer loop. This approval covers only the exact canonical role source above and its listed dependent artifacts. It does not authorize changing checklist questions or unrelated agent or skill definitions.
