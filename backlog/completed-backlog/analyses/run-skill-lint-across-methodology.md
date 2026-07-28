# Run Skill Lint Across Methodology Skills

Status: Completed

Type: Analysis

Provider: file

Provider Reference: backlog/completed-backlog/analyses/run-skill-lint-across-methodology.md

Completion: direct-main

## Running Acceptance

- Transition: Starting -> Running.
- Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758.
- Canonical Work-Item Thread: 019fa9be-0083-7542-973f-af35557b2393.
- Canonical Root Agent Task: 019fa9be-0083-7542-973f-af35557b2393.
- Owner: Root Dev Orchestrator.
- Accepted At: 2026-07-28T17:22:38Z.
- Branch: codex/run-skill-lint-across-methodology-019f.
- Worktree: /Users/martinbechard/dev/dev-methodology/.worktrees/run-skill-lint-across-methodology-019f.
- Reserved Base/Main Commit: 6affa81cccc7fca4b8ce8ed4045a5139c18a7654.
- Implementation Claim Evidence: No implementation claim is required; the live registry was empty before this recovery transaction.
- Provider-Mutation Claim Evidence: rehome-skill-lint-provider-019fa9be acquired by dev-backlog-steward for this exact backlog file; claim event b01ace89-b57a-4d10-88af-897fdf3d5a67.
- Recovery History: The prior internal canonical Thread and root Agent Task /root/skill_lint_methodology were replaced during recovery; they remain history only and are not current execution identities.
- Recovery Phase: Recovery reconciliation accepted.
- Current Main Observation: main was clean at c751bd170bb0d09a88d3976e732298b6a743d62d when this transaction began; the reserved base remains 6affa81cccc7fca4b8ce8ed4045a5139c18a7654.

## Summary

Run the official skill lint reviewer across every authoritative methodology skill source and create defect work items for each skill that has confirmed critical findings.

## Context

The repository now includes the dev-skill-lint-reviewer conceptual agent. Its Codex intermediate semantic profile maps to gpt-5.6-luna with high reasoning effort. Earlier comparison runs showed Luna high gave the clearest critical-only review signal for the three longest skills.

This analysis must cover every authoritative skill source in the methodology bundle:

- distributed skills under skills/*/SKILL.md;
- adapter-owned skills under adapters/*/skills/*/SKILL.md.

Generated mirrors, vendored files, build output, evaluation fixtures, archived worktrees, and report artifacts are outside the lint target set unless they are the authoritative source for a distributed or adapter-owned skill.

## Source Evidence

User request on 2026-07-28 in the active Codex task: "Then create a work item where the linter is used to analyze every skill in the methology, and log defects for each that has critical findings".

## Requirements

- Inventory every in-scope authoritative skill source before running reviews.
- Use dev-skill-lint-reviewer with Codex gpt-5.6-luna high reasoning effort for the lint reviews.
- Apply the official criticality criteria from agents/roles/dev-activities/dev-skill-lint-reviewer.role.yaml.
- Report only critical findings that could materially mislead an agent, weaken safety, duplicate authority, or make the skill difficult to maintain.
- Treat bad style or non-STE wording as critical only when it obscures a requirement, condition, permission, prohibition, ownership boundary, command, path, evidence rule, or terminal outcome.
- Treat redundancy as critical only when repeated directives or topics create inconsistent authority, conflicting lifecycle ownership, duplicated maintenance surfaces, or material context bloat.
- Preserve exact skill identifiers, paths, commands, configuration keys, harness distinctions, permissions, and prohibitions in every finding.
- For each skill with one or more confirmed critical findings, create a separate Defect work item that names the skill path, critical finding evidence, smallest correction direction, and verification expectation.
- Do not create defect work items for minor nits, stylistic preferences, uncertain possibilities, or findings that do not meet the criticality threshold.
- Do not fix the identified skill defects under this analysis item unless a separately dispatched defect item authorizes that correction.

## Acceptance Criteria

- The completed analysis records the full in-scope skill inventory and the excluded-source rule used for the run.
- Every in-scope skill has a recorded lint outcome: no critical findings, critical findings logged, or blocked with the exact unreadable source or missing evidence.
- Every confirmed critical-finding skill has exactly one newly created or updated Defect work item in the file provider backlog.
- Each created defect item is independently dispatchable and includes source evidence from the lint result.
- No defect item is created for a finding that is only a minor wording, formatting, tone, grammar, naming, or preference issue.
- The final report lists the lint task identities, model and effort identity, created defect provider references, and any skills reviewed without critical findings.

## Dependencies

None.

## Verification

- Compare the lint inventory against find skills adapters -path '*/SKILL.md' filtered to authoritative distributed and adapter-owned skill sources.
- Validate every created or updated defect item against the file work-item template requirements.
- Run the focused backlog validation or report-generation command used by this repository for file-provider items.
- Run git diff --check before committing the analysis results and defect work items.

## Open Questions

None.

## Notes

The word "methology" in the source request is interpreted as "methodology" and scoped to this repository's authoritative methodology skill sources.

## Analysis Result

The authoritative inventory contains 127 skill sources: 19 raw CRITICAL outcomes and 108 raw NO_CRITICAL outcomes. Independent reconciliation accepted 27 CONFIRMED_CRITICAL outcomes and 100 NO_CRITICAL outcomes. The focused MySQL resolution used Luna with high reasoning effort. The accepted disposition rejected the provisional documentation-bootstrap and Liquibase findings and rejected the narrowed provisional subfindings for manage-file-work-items and project-wiki-create. No skill, agent, schema, or other definition mutation was made under this analysis item.

The accepted results created 27 unique file-provider Defects. Their exact references are:

- backlog/defect-backlog/agent-claim-reset-invalid-json-shapes.md
- backlog/defect-backlog/backlog-crisis-retain-agent-claim.md
- backlog/defect-backlog/align-module-design-mandatory-heading-contract.md
- backlog/defect-backlog/make-technology-detector-fallback-prerequisites-executable.md
- backlog/defect-backlog/end-to-end-verification-commit-authority.md
- backlog/defect-backlog/align-fix-explanation-item-taxonomy.md
- backlog/defect-backlog/bound-jest-failure-ownership-to-current-change.md
- backlog/defect-backlog/separate-distributed-methodology-from-repository-maintenance.md
- backlog/defect-backlog/respect-resource-coordination-none-in-manage-file-work-items.md
- backlog/defect-backlog/bound-mysql-production-verification-to-safe-targets.md
- backlog/defect-backlog/make-project-wiki-template-resolution-install-portable.md
- backlog/defect-backlog/project-wiki-topic-verify-read-only-helper-resolution.md
- backlog/defect-backlog/project-wiki-topic-write-role-owned-verification.md
- backlog/defect-backlog/project-wiki-role-routing-and-operation-paths.md
- backlog/defect-backlog/keep-quarkus-persistence-companion-selection-setup-owned.md
- backlog/defect-backlog/react-server-components-detection-boundary.md
- backlog/defect-backlog/allow-typed-evidence-review-architecture.md
- backlog/defect-backlog/allow-typed-evidence-review-functional-spec.md
- backlog/defect-backlog/allow-typed-evidence-review-high-level-design.md
- backlog/defect-backlog/allow-typed-evidence-review-module-design.md
- backlog/defect-backlog/allow-typed-evidence-review-unit-test-plan.md
- backlog/defect-backlog/replace-structured-design-chain-of-thought-output-contract.md
- backlog/defect-backlog/make-tailwind-companion-guidance-route-aware.md
- backlog/defect-backlog/stop-test-strategy-from-rerunning-technology-routing.md
- backlog/defect-backlog/prevent-sensitive-tool-runtime-log-and-trace-retention.md
- backlog/defect-backlog/detect-typescript-esm-in-bundler-only-projects.md
- backlog/defect-backlog/stop-ux-review-runtime-technology-routing.md

The durable result is [Methodology Skill Lint Review](../../../evals/results/2026-07-28-methodology-skill-lint.md), which records the complete inventory, raw and accepted disposition separation, exact defect evidence, reviewer identities, and final outcome table.

## Completion Evidence

- Terminal lifecycle: Running -> Completed. Terminal owner: Unowned.
- Canonical Work-Item Thread and Canonical Root Agent Task: 019fa9be-0083-7542-973f-af35557b2393. Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758. The running-acceptance branch and worktree evidence above are preserved.
- Accepted report source: 325a9777d51d7ed9121b40a10780e8e007f209f7. Artifact review: GOOD. Verifier: PASS. Provider batch review: GOOD.
- Direct-main integration: 26bb65b3391508feafb3306ba33e5408f8d0e74b. The integrated report blob is b645967027ad1b619c7a1622e87a2ab1cb1b0a10.
- All-skill validation and diff checks passed for the accepted delivery. The direct-main completion contract is satisfied.
- Integration claim: b327eb75-146f-4809-9a16-807d3182c34f acquired; dccba99f-7281-4546-bf07-7c31e76b6a52 released.
- Archive claim: close-skill-lint-analysis-019fa9be acquired for this source and destination record; event 8e6a40b7-53b7-4696-af3a-050c5fece226. The release and terminal provider commit are recorded after this archive transaction.
