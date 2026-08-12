# Remediate Inherited Supported-Test Baseline Failures

Status: Running

Type: Defect

Provider: file

Work Item ID: remediate-inherited-supported-test-baseline-failures

Completion: main-branch

## Summary

Correct the inherited, OS-independent failures exposed by the complete supported-entry-point comparator so the repository's supported test baseline becomes green without exclusions, weakened assertions, or signature masking.

## Context

Work Item `make-python-skill-and-project-scripts-windows-portable` expanded deterministic discovery to 63 supported test entry points. Full-history current-main reproduction distinguished Windows-specific and missing-capability cases from an inherited baseline of 16 owning paths and 118 exact failure identities. The portability gate records this baseline and fails on every new, changed, or Windows-specific identity; it does not authorize these unrelated contracts to remain broken indefinitely.

History-sensitive tests must be reproduced from a full-history checkout. A prior `git archive` plus synthesized-commit reproduction destroyed Git path history and produced one invalid `setUpClass` identity; that identity was superseded by the two actual `scripts/test_agent_skill_evaluation_docs.py` failures from a full-history clone.

## Source Evidence

The Dev Backlog Coordinator authorized a separate baseline-remediation defect during delivery of `make-python-skill-and-project-scripts-windows-portable` in parent task `019fb057-1767-7ef2-b5fa-41f4417b20b3`. Canonical task `019fe928-e2d8-7f91-91b2-bd27990a7414` supplied the final verified inventory from replacement candidate `7cb7e031` on 2026-08-10.

Authorized baseline inventory:

| Owner | Owning path | Exact identities |
| --- | --- | ---: |
| Dev Artifact Reviewer | `evals/agent-tests/dev-artifact-reviewer/test_checklist_contract.py` | 1 |
| Dev Documentation Writer | `evals/agent-tests/dev-documentation-writer/test_fixtures.py` | 11 |
| Dev Orchestrator | `evals/agent-tests/dev-orchestrator/test_fixtures.py` | 60 |
| Project Configurator | `evals/agent-tests/project-configurator/test_fixtures.py` | 1 |
| Project Bootstrapper | `evals/agent-tests/project-bootstrapper/test_scripted_orchestration.py` | 24 |
| Wiki Ingester | `evals/agent-tests/wiki-ingester/test_contract.py` | 1 |
| Agent-suite runner | `evals/agent-tests/test_runner.py` | 1 |
| Bundle contract | `scripts/test_bundle_content.py` | 0, resolved before handoff |
| Codex task control | `scripts/test_codex_task_control.py` | 8 |
| Evaluation coverage catalog | `scripts/test_eval_coverage_catalog.py` | 1 |
| Agent-skill evaluation docs | `scripts/test_agent_skill_evaluation_docs.py` | 2, with one reported resolved by the portability candidate |
| Resource claim | `scripts/test_resource_claim.py` | 1 |
| Role mutation policy | `scripts/test_role_mutation_policy.py` | 2 |
| STE technical writing | `scripts/test_ste_technical_writing.py` | 1 |
| Technology detection | `scripts/test_technology_detection.py` | 2 |
| Work-item coordination | `scripts/test_work_item_coordination.py` | 2 |

## Requirements

- Reproduce the complete recorded inventory against a clean, full-history checkout of current main before changing any contract.
- Reconcile identities already resolved on current main and retain immutable evidence for every remaining failure signature and owning path.
- Correct each root cause in its authoritative source, fixture, generated artifact, or assertion rather than adding broad exclusions, expected-failure markers, or signature allowlists.
- Preserve supported Linux, macOS, and Windows behavior; do not make a platform-specific shortcut the default contract.
- Regenerate generator-owned artifacts through their owning generators and update focused expectations only when authoritative behavior changes.
- Keep the two separately observed inherited agent-suite command failures outside the 118-identity baseline until their exact ownership and relationship to these defects are independently established.
- Remove each remediated identity from the portability baseline through the owning comparator update without weakening detection of new or changed failures.

## Acceptance Criteria

- Every current-main identity derived from the authorized 16-owner/118-identity inventory is either fixed or shown by immutable evidence to have already been resolved before implementation.
- All 63 supported test entry points complete without an inherited OS-independent failure from this inventory in a complete checkout with declared capabilities present.
- History-sensitive checks use a full-history repository and do not report archive-induced artifacts.
- No failure is hidden by whole-file exclusion, permissive regex, changed signature normalization, expected-failure annotation, or platform-only bypass.
- The portability comparator has no remaining baseline entry for a fixed identity and still rejects every new, changed, or Windows-specific identity.
- Fresh independent code and methodology review plus verification accept the integrated repairs.

## Dependencies

None.

## Verification

- Run the complete 63-entry supported-test workflow in a full-history checkout on current main before and after correction.
- Run every directly owned focused module listed in the final reconciled inventory.
- Run generator freshness, catalog, bundle, role-policy, work-item coordination, and Git diff checks implicated by corrected owners.
- Verify the Windows-portability comparator rejects one injected new identity and one changed inherited signature after baseline removals.
- Run Python compilation and repository cleanliness checks for every changed Python path.

## Open Questions

- Which exact two inherited agent-suite command failures remain outside the authorized 118-identity inventory, and do they duplicate an existing owner after full-history reproduction?

## Notes

- Related Work Item: `make-python-skill-and-project-scripts-windows-portable`.
- This item owns baseline remediation, not Windows portability behavior or the portability workflow itself.

## Starting Handoff Evidence

Starting Recorded At: 2026-08-11T22:32:45Z

Coordinator: Codex task 019ff26f-25d0-7381-88f7-74d52717ff59

Normalized Objective: Reproduce and remediate the authorized inherited supported-test baseline from a clean full-history checkout without exclusions or signature masking, preserve platform behavior, update only authoritative owners and directly affected projections or expectations, then complete fresh independent review, focused verification, main-branch delivery, provider closure, and cleanup.

Intended Root Role: Dev Orchestrator

Launch Result: Requested after this durable reservation

Canonical Execution: None

Last Contact At: 2026-08-11T22:32:45Z

Next Reconciliation At: 2026-08-11T22:47:45Z

## Running Execution Evidence

Accepted At: 2026-08-11T22:39:07Z

Owner: Root Dev Orchestrator

Codex Task ID: 019ff2f9-0863-7133-aac0-ff141cf16a92

Conversation ID: 019ff2f9-0863-7133-aac0-ff141cf16a92

Root Role: Dev Orchestrator

Parent Task ID: 019ff26f-25d0-7381-88f7-74d52717ff59

Branch: codex/remediate-inherited-supported-test-baseline-failures

Worktree: /Users/martinbechard/dev/dev-methodology/.worktrees/remediate-inherited-supported-test-baseline-failures

Phase: Integrating accepted candidate into current main

Accepted Execution Evidence: The exact opaque Work Item ID was acquired with activity work. A clean, non-shallow full-history worktree was created from observed current main f1490b80e856df9cc08d24027acd3252734aac18 before implementation. The dispatch SHA f1490b80d6df33fe92f88905e8b92cacb596967d was not present in the repository; the full observed main identity is retained here without substituting the historical candidate.

## Baseline Reconciliation Evidence

Reconciled At: 2026-08-11T22:55:27Z

Runtime: CPython 3.11.13 in the clean full-history task worktree at f1490b80e856df9cc08d24027acd3252734aac18

Historical Result: 69 of the authorized 118 identities were already resolved before implementation; 49 historical identities remained and are the complete mutation scope.

Already Resolved Owners: All 60 Dev Orchestrator identities, all 8 Codex task-control identities, and 1 of 2 agent-skill evaluation documentation identities.

Separate Current-Main Defects: The supported command stops before its 63-entry loop because scripts/audit-worktree-completion-links.py and scripts/test_audit_worktree_completion_links.py are unclassified. Direct loop execution then stops because stale Playwright exclusions name 13 undiscovered evals/agent-tests/test_runner.py cases. Independent owner execution also found nine new identities outside the authorized baseline: one bundle-content terminology-family case, one role-mutation public-lifecycle case, one STE shared-contract case, and six work-item-coordination Active Execution Evidence or reporting cases. None is authorized for correction by this item.

Implementation Boundary: Correct only the 49 remaining historical identities and their exact authoritative causes. Preserve the separate current-main defects without exclusions, allowlists, normalization changes, or platform bypasses.

## Candidate Evidence

Accepted Candidate Commit: 529112158f6b4454864d5d550db96547d5029371

Candidate Recorded At: 2026-08-11T23:26:59Z

Candidate State: Clean isolated worktree on codex/remediate-inherited-supported-test-baseline-failures

Historical Verification: All 16 owner modules ran through the comparator child entry point, covering 809 tests. All 118 historical identities are absent and all 16 resolved owner rows remain. The nine separately classified current identities remain visible.

Focused Verification: Resource claim 141 of 141 passed; Project Bootstrapper 24 of 24 passed; the core fixture group passed 91 with 4 skips; JSON and text report checks passed; documentation generation check passed; comparator 16-owner, synthetic-new-identity, and cause-drift checks passed.

Known External Gate Failures: The complete supported entry point still stops on the two unclassified audit-worktree paths. The direct supported loop still encounters the stale Playwright exclusion identities. These are preserved as separate current-main defects and were not changed by the candidate.

Overlap Handoff: Reviewer-runtime task 019ff2f9-085e-7202-8099-8f35425278a0 received the exact originally approved scripts/test_role_mutation_policy.py content boundary at commit 84861e84eca27c2dd25ef9238401834fca5418b7 before archival. Final candidate 529112158f6b4454864d5d550db96547d5029371 has the same tree and overlap bytes.

Review Correction Reconciliation: Independent methodology evidence identified one stale role-mutation assertion, but verification proved that correcting it remediated one of the nine newly discovered identities that this item must keep separate. The original coder restored the established boundary. Final candidate 529112158f6b4454864d5d550db96547d5029371 has tree 0b8c8ec3264f587aff614a51734189fe2f61b455, byte-identical to source-approved candidate 84861e84eca27c2dd25ef9238401834fca5418b7. All nine separate current identities remain visible.

Methodology Review Availability: The first methodology-artifact reviewer could not issue a valid verdict because its role requires writing a checklist artifact while this work item explicitly grants reviewers zero write authority. Its substantive stale-assertion finding was classified as one of the nine separate current identities; the temporary correction was reverted. The permitted zero-write replacement failed its required skill load before review.

## Review Recovery Decision

Decision Requested At: 2026-08-11T23:47:31Z

Decision Owner: Parent Dev Backlog Coordinator task 019ff26f-25d0-7381-88f7-74d52717ff59

Current Candidate: 529112158f6b4454864d5d550db96547d5029371, clean and independently source-approved and verified

Review Availability Evidence: The methodology-artifact reviewer could not issue a verdict without violating the explicit zero-write reviewer boundary because its contract mandates a written checklist artifact. The one permitted replacement connected to the configured skill loader but received skill_not_found for dev-methodology-repository-maintenance and stopped before review. This is review availability failure, not a source finding.

Requested Coordinator Decision: Either accept the existing independent source review's explicit methodology-contract, generator-ownership, and comparator-strictness coverage as satisfying the methodology gate, or re-home one zero-write methodology review with a working required-skill load.

Unattended Boundary: Do not begin main integration or provider completion until the Coordinator records one evidence-backed recovery disposition. Preserve the final candidate, source approval, verification, worktree, and released blocked work claim.

Resolution: On 2026-08-12 in the canonical Codex task, the user confirmed that work may continue after clarification that no code approval, scope expansion, reduced verification, or risk acceptance was requested. The selected recovery is to run another strictly read-only methodology review in a compatible task or runtime that can load the required skills. Main integration remains prohibited until that review accepts the candidate.

Methodology Review Result: APPROVED on 2026-08-12 by a fresh strictly read-only reviewer against candidate 529112158f6b4454864d5d550db96547d5029371. The review accepted Project Configurator ownership semantics, selected and none resource-coordination contracts, JSON REPORT behavior, generator ownership and provenance, strict zero-identity comparator behavior, unchanged discovery and normalization, and preservation of all separate current defects. The candidate worktree remained clean.
