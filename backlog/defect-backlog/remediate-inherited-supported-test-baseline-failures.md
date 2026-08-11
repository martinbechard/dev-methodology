# Remediate Inherited Supported-Test Baseline Failures

Status: Starting

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
