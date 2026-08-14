# Correct Dev Code Reviewer Premise Validation

Status: Ready

Type: Defect

Provider: file

Work Item ID: correct-dev-code-reviewer-premise-validation

Completion: main-branch

## Summary

Require the Dev Code Reviewer to validate every material premise behind a proposed finding so missing authority, ambiguous security boundaries, and unstated attacker capabilities remain open questions instead of confirmed defects. Preserve evidence-backed detection of real security, correctness, compatibility, and verification defects.

## Context

During review of py-json-render, the Dev Code Reviewer interpreted the requirement “external includes cannot escape their configured source root” as requiring protection against hostile concurrent filesystem mutation. No applicable project authority established that attacker capability or threat model. The reviewer promoted the unsupported time-of-check/time-of-use interpretation into a confirmed defect, causing unnecessary native Windows implementation, architecture-review loops, platform-specific tests, and a native-Windows delivery gate.

Existing contracts already establish much of the intended boundary: confirmed findings require applicable authority and contradictory target evidence; missing or ambiguous policy belongs in open questions or residual risk; material assumptions that change implementation boundaries require confirmation; and missing policy must not become a confirmed finding. The runtime role does not state the security-premise rule as explicitly as the evaluation suite contract. The review-code-with-evidence synthesis rule also permits findings from materially unknown checklist items without distinguishing unknown target evidence from absence of authority establishing the requirement.

This item refines the completed prevent-unsupported-review-findings work rather than reopening it. That item addressed generic promotion of missing policy; this item adds explicit premise validation and paired security threat-model regression coverage.

The reviewer remains read-only and evidence-first. The correction must not weaken detection of actual security, correctness, compatibility, or verification defects when applicable authority exists.

## Source Evidence

The user explicitly requested on 2026-08-14 that one authoritative file-backed Work Item be created to correct Dev Code Reviewer premise validation. The request requires every material premise to be identified and validated; security findings to cite an applicable threat model, accepted requirement, repository policy, or demonstrated caller/runtime behavior; unstated attacker capabilities and ambiguous security boundaries to remain open questions; and each confirmed finding to state its premise, authority, contradictory target evidence, and user impact. The user also supplied the py-json-render source-containment review as the regression basis and explicitly prohibited implementation without separate authorization.

Current repository evidence:

- agents/roles/dev-activities/dev-code-reviewer.role.yaml describes evidence extraction and synthesis but does not explicitly require security-premise validation in each confirmed finding.
- skills/review-code-with-evidence/SKILL.md permits findings from contradicted or materially unknown checklist items without separating missing requirement authority from missing target evidence.
- skills/careful-coding/SKILL.md requires confirmation when a material premise changes the requested implementation boundary.
- evals/agent-tests/dev-code-reviewer/skills/dev-code-reviewer-suite-contract/SKILL.md already requires applicable authority plus contradictory target evidence and keeps missing policy outside confirmed findings.
- evals/agent-tests/dev-code-reviewer/scenarios.yaml and the header-policy-authority-boundary fixture provide an existing negative/positive authority-boundary pattern that the new security scenario can follow.

## Requirements

- Require the Dev Code Reviewer to identify and validate every material premise behind each proposed finding before confirming it.
- Require every confirmed finding to state the material premise, applicable authority, contradictory target evidence, and user impact.
- Require a proposed security finding to cite at least one applicable threat model, accepted requirement, repository policy, or demonstrated caller/runtime behavior that establishes the security boundary or attacker capability.
- Treat unstated attacker capabilities and ambiguous security boundaries as open questions rather than confirmed defects.
- Prevent a materially unknown checklist status from becoming a confirmed finding when the missing evidence is the authority that would establish the requirement itself. Preserve materially unknown target or verification evidence in the appropriate evidence-gap classification without manufacturing authority.
- Preserve legitimate findings when applicable authority exists and the target evidence contradicts it.
- Keep the reviewer read-only and evidence-first.
- Preserve detection of actual security, correctness, compatibility, documentation, and verification defects.
- Reconcile the runtime role, review-code-with-evidence, careful-coding, the Dev Code Reviewer suite contract, scenarios, fixtures, evaluator logic, generated adapters, catalogs, and relevant documentation so the terminology and behavior agree.
- Add a negative regression case in which portable canonical-path validation rejects absolute paths, traversal, and existing symbolic-link escapes, while no project authority defines hostile concurrent filesystem mutation as an attacker capability. Permit exactly one clear open question about the possible time-of-check/time-of-use risk; prohibit a confirmed defect, duplicated residual-risk noise, native Windows API demand, platform-specific infrastructure demand, or native-host delivery gate.
- Add a companion positive case with an explicit hostile-concurrent-mutation threat model. Require the same implementation to produce a confirmed security finding with the premise, authority, contradictory target evidence, and user impact.
- Regenerate generated adapters from canonical sources rather than editing generated projections directly.

## Acceptance Criteria

- Runtime instructions and Dev Code Reviewer evaluation expectations use the same premise-validation rule.
- Missing authority cannot be converted into a confirmed finding, including through a materially unknown checklist item.
- The ambiguous source-containment case produces no confirmed defect for missing race-free containment and exactly one clear open question, with no duplicated residual-risk entry.
- The ambiguous case does not demand native Windows APIs, platform-specific infrastructure, or a native-host delivery gate.
- The explicit hostile-concurrent-mutation case produces the expected confirmed security finding for the same candidate implementation.
- Every confirmed finding exposes a premise, applicable authority, contradictory target evidence, and user impact in an auditable form.
- Applicable authority continues to support legitimate security, correctness, compatibility, documentation, and verification findings.
- The reviewer performs no candidate or product mutation.
- Generated adapters match their canonical role and skill sources after supported regeneration.
- Focused Dev Code Reviewer fixture and evaluation checks pass.
- Applicable methodology regression, catalog, documentation, and generated-artifact freshness checks pass.
- Documentation clearly distinguishes observations, premises, authority, findings, open questions, and residual risk.

## Dependencies

None.

## Verification

- Run the deterministic Dev Code Reviewer fixture tests that exercise the authority-boundary evaluator and its negative and positive cases.
- Run the focused Dev Code Reviewer evaluation scenarios and inspect captured synthesis, independent Judge results, and read-only evidence.
- Verify the ambiguous case returns exactly one open question, zero related confirmed findings, and no duplicate residual-risk entry.
- Verify the explicit threat-model case returns the required confirmed security finding with all four evidence dimensions.
- Run the supported agent and skill generation command, then run its freshness check and exact generated-adapter consistency checks.
- Run the focused bundle-content and catalog assertions affected by the Dev Code Reviewer role, skills, suite, fixtures, and documentation.
- Run Markdown and repository validation applicable to changed maintained documents, plus git diff --check.
- Obtain fresh independent review confirming the change preserves evidence-backed defect detection and the reviewer’s read-only boundary.

## Open Questions

- Which existing documentation page or catalog projection is the smallest authoritative place to document the distinction among observations, premises, authority, findings, open questions, and residual risk? Resolve this through source discovery without expanding the governed-definition manifest.
- Should the new paired containment cases extend the existing header-policy-authority-boundary evaluator or use a sibling source-containment-authority-boundary fixture? Choose the smallest structure that keeps evaluator-owned authority and expectations outside the candidate workspace.

## Governed Definition Approval

### Governed Canonical Sources

- skills/review-code-with-evidence/SKILL.md
- skills/careful-coding/SKILL.md

### Allowed Dependent Artifacts

- agents/roles/dev-activities/dev-code-reviewer.role.yaml
- evals/agent-tests/dev-code-reviewer/skills/dev-code-reviewer-suite-contract/SKILL.md
- evals/agent-tests/dev-code-reviewer/scenarios.yaml
- evals/agent-tests/dev-code-reviewer/test_fixtures.py
- evals/agent-tests/dev-code-reviewer/fixtures/header-policy-authority-boundary/README.md
- evals/agent-tests/dev-code-reviewer/fixtures/header-policy-authority-boundary/evaluate_synthesis.py
- evals/agent-tests/dev-code-reviewer/fixtures/header-policy-authority-boundary/expected-results.json
- evals/agent-tests/dev-code-reviewer/fixtures/header-policy-authority-boundary/stage_candidate.py
- generated/adapters/agent-generation-manifest.json
- Supported generated Dev Code Reviewer adapter projections produced by scripts/build-skill-docs.py.
- Focused catalog assertions and the smallest relevant maintained documentation artifact identified during authorized source discovery.

### Approval Resolution

Approved at creation from the user’s 2026-08-14 message: “Inspect and reconcile at least” the named Dev Code Reviewer role, review-code-with-evidence skill, careful-coding skill, suite contract, scenarios, and relevant fixture, evaluator, generated-adapter, catalog, and documentation artifacts. This approves the two exact governed canonical skill paths above and the named dependent reconciliation scope. It does not authorize implementation in this task, unrelated governed definitions, or broader methodology changes. Any additional governed skill-definition path requires separate scope-specific approval.

## Notes

- Do not equate a possible risk with a confirmed defect when the project has not established the premise that makes the risk a requirement violation.
- Do not suppress a confirmed defect when explicit threat-model authority establishes hostile concurrent mutation as in scope.
- Avoid reporting the same ambiguity once as an open question and again as residual risk; the negative regression expects one clear open question.
- Creation of this Work Item records authorized future work but does not authorize implementation during the creation task.
