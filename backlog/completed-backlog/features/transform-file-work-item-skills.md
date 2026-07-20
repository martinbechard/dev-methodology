# Transform File Work-Item Skills

Status: Completed

Type: Feature

## Current Execution

- Canonical Dev Orchestrator task: 019f7f7e-78df-7790-a845-928e9f2a03b9.
- Branch: codex/transform-file-work-item-skills.
- Worktree: /Users/martinbechard/.codex/worktrees/c90f/dev-methodology.
- Started from approved Ready commit 7ab9e985c6ef7f26462bde7878d28fb1c0307d40.
- Scope remains limited to the approved five skill packages, their metadata, supported generated mirrors, and directly related non-governed tests and documentation.

## Completion Evidence

- Phase: Completed.
- Accepted candidate: 0a948c8d820fd947c2dda13803ebe2074415805b on codex/transform-file-work-item-skills, following producer commit 0c6b009c5987fb90334dc107f5c4ef8d9d5ba26b and the independent review correction pass.
- Governed checks: all ten exact authorized SKILL.md and agents/openai.yaml paths returned ALLOWED_APPROVED_DEFINITION_CHANGE before mutation, using the approval records sourced from thread 019f77f4-c4bd-7c91-b197-c987a7beb838 message item-2078.
- Independent methodology review: ACCEPTED after correction of the frozen Dev Backlog Steward suite alignment, migration-bridge probe coverage, executable negative fixture, mature isolation and current-state reporting rules, and generated hierarchy and support views.
- Independent verifier: PASS for the accepted candidate and corrected main state. Catalog validation, five-package Agent Skill validation, exact metadata checks, skill documentation, hierarchy and support-checklist freshness, generated attribution, YAML and TOML parsing, and diff hygiene passed.
- Focused deterministic tests: 16 evaluation-catalog tests and 13 focused BundleContentTests passed on integrated main. The file-work-item-no-mutation fixture prepared successfully and covers provider mismatch, isolated or non-main authority, PRIMARY_REQUIRED, unchanged protected backlog content, and no shadow backlog writes.
- Live creation verification: a disposable primary-main repository created one typed item under claim live-create-feature-019f7f7e, rejected a duplicate without mutation, created a linked two-child series under claim live-create-series-019f7f7e, rejected a GitHub provider mismatch without file or issue mutation, released all claims, and ended clean on main.
- Live management verification: a disposable primary-main repository exercised Ready to Running to Blocked to resumed Running to Completed for a feature and Ready to Running to Failed for a defect. Implementation and backlog claims remained separate, completed and failed archive paths were correct, all claims released, and the repository ended clean on main.
- Integration contention: initial exact project integration acquisition returned WAIT at event 77ab6417-3c65-49a6-bc79-162aeb72352b on direct-main-completion-integration-019f7f8c. The successor handoff acquired file-work-item-skills-integration-019f7f7e PRIMARY at event 701a88ef-8501-4185-8128-fb7aea4acba0 on clean main baseline 8e10117b0d695f12e5acc54576825566e2a3879b.
- Semantic integration mapping: 0c6b009c5987fb90334dc107f5c4ef8d9d5ba26b mapped to 60dbbd2, 0a948c8d820fd947c2dda13803ebe2074415805b mapped to a12b01b, and focused current-main reconciliation completed at 5f84d5b8625df6a93661b92827b33877c49cada8.
- Current-main reconciliation preserved the already integrated GitHub, GitLab, Azure DevOps, Jira, and direct-main catalog entries. Two missing non-governed GitLab probe declarations were added solely to reproduce the combined support checklist; no GitLab governed definition changed.
- Integration release: file-work-item-skills-integration-019f7f7e released normally from clean main at event 1f4372cc-0420-46cc-a8d4-97647f59c3df. Delivery commit 5f84d5b8625df6a93661b92827b33877c49cada8 remains reachable from current main.
- Terminal backlog claim: file-work-item-skills-terminal-019f7f7e acquired PRIMARY for only this active path and the completed destination at event 97932f46-0ad4-4800-859b-7786b13f5a2c. Its normal clean release follows this committed archive transaction.
- Retirement boundary: create-file-work-item and manage-file-work-items now own the complete file-provider procedures. create-backlog, manage-backlog, and file-based-backlog are migration-only bridges with no independent behavior. Physical deletion waits only for the separately governed caller migration owned by integrate-work-item-contracts-across-bundle.
- Cleanup eligibility: the private worktree is clean at accepted commit 0a948c8d820fd947c2dda13803ebe2074415805b. The ten governed package files are byte-identical to integrated main. The branch is semantically integrated through the mapping above rather than ancestry-merged, so the parent may remove the clean worktree and delete the branch using this patch-equivalence evidence.
- Open issues: none for this work item. The full scripts, project-wiki, and agent catalog suites remain the final campaign or release gate and were intentionally not run for this bounded transformation.

## Approval Resolution

The user approved the exact governed definition scope, conditional on equivalent replacement skills existing before retirement.

## Approved Scope

Do you approve changing or retiring skills/create-backlog/SKILL.md, skills/manage-backlog/SKILL.md, and skills/file-based-backlog/SKILL.md and their agents/openai.yaml metadata, and creating skills/create-file-work-item/SKILL.md and skills/manage-file-work-items/SKILL.md with their agents/openai.yaml metadata, together with only their supported generated mirrors and directly related non-governed tests and documentation?

## Approval Evidence

- Basis: explicit-user-direction.
- Exact answer: “I want to have equivalent skills so retire them as long as you have replacements”.
- Provenance: thread 019f77f4-c4bd-7c91-b197-c987a7beb838, message item-2078.
- Condition: create-file-work-item and manage-file-work-items must provide equivalent replacement behavior before create-backlog, manage-backlog, or file-based-backlog is retired.

The decision gate is resolved. Delivery completion still requires implementation, the governed pre-mutation checks for every exact canonical definition, supported regeneration, independent review, focused verification, integration, and terminal backlog evidence.

## Summary

Replace the generic create-backlog and manage-backlog names with symmetric file-provider skills, absorb the redundant file-based-backlog wrapper, and preserve backlog on main as the only authoritative file-backed queue.

## Context

This item is a provider lane in the [Work-Item Provider And Completion Contracts series](../../feature-backlog/work-item-provider-and-completion/index.md). The current create-backlog and manage-backlog skills contain the mature typed-item and lifecycle procedures. The newer file-based-backlog skill mostly selects those procedures. The transformation should preserve the mature behavior under provider-specific names rather than layer another wrapper around it.

## Requirements

- Create the canonical create-file-work-item and manage-file-work-items skill packages from the existing create-backlog and manage-backlog contracts.
- Keep each skill's frontmatter name, directory name, Codex metadata, descriptions, examples, and evaluation identifiers aligned.
- Preserve typed item placement, related-series indexes, unique slugs, user-action boundaries, lifecycle transitions, recovery evidence, archive behavior, and dispatchability rules.
- Make backlog under the primary main worktree the only authoritative file-provider storage root.
- Prohibit file-backed work-item creation or lifecycle mutation from isolated worktrees and non-main authorities.
- Use agent-claim's backlog scope for each file mutation and preserve PRIMARY_REQUIRED behavior when the primary worktree is unavailable.
- Keep implementation claims separate from short backlog transition claims.
- Require durable source, dependency, ownership, delivery, verification, completion, blocked, and archival evidence appropriate to each transition.
- Absorb the provider-selection content of file-based-backlog into the two canonical skills.
- Retire file-based-backlog after all source and generated references move to the canonical create and manage identifiers.
- Provide migration guidance for repositories and PROJECT.yaml files that still name create-backlog, manage-backlog, or file-based-backlog.
- Do not create provider issues or mirror file items into GitHub, GitLab, Azure DevOps, or Jira.

## Acceptance Criteria

- New file-backed work-item creation routes through create-file-work-item.
- Existing file-backed item state changes route through manage-file-work-items.
- Every file-backed item remains under backlog on the primary main worktree.
- An isolated or non-primary mutation request blocks without writing a shadow queue.
- The transformed skills preserve the complete existing typed-item, series, user-action, recovery, and archive contracts.
- file-based-backlog has no remaining independent behavior and can be removed without losing a procedure.
- Migration guidance maps every retired identifier to one canonical replacement.
- Provider-backed projects never load the file skills unless the file provider is selected or explicitly requested for one item.

## Dependencies

define-provider-and-completion-selector-contracts.

## Verification

- Add focused tests for file creation, duplicate detection, series placement, claim acquisition, lifecycle transitions, recovery, completion, failure, archive, and invalid primary-worktree state.
- Add negative tests proving isolated worktrees and provider-backed projects do not create backlog files.
- Compare transformed skill behavior with the complete create-backlog and manage-backlog regression inventory.
- Sweep source, metadata, generated output, templates, evals, and documentation for stale file-based-backlog and ambiguous backlog identifiers.
- Run Agent Skill validation, metadata alignment, generated-output checks, focused backlog tests, full repository tests, project-wiki tests, and Git diff validation.

## Notes

- This is a behavior-preserving provider qualification, not a new backlog taxonomy.
- Cross-bundle role and documentation migration is finalized by integrate-work-item-contracts-across-bundle.
