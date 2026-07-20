# Preserve Wiki Research Source Links

Status: Completed

Type: Defect

## Running Ownership

- Owner: Dev Orchestrator root task 019f77f4-c4bd-7c91-b197-c987a7beb838.
- Lifecycle agent: Dev Backlog Steward.
- Lifecycle claim: preserve-wiki-research-source-links-lifecycle.
- Claim evidence: PRIMARY exact-file backlog ownership acquired at 2026-07-20T01:12:15.710366Z from clean baseline commit 9f6f4d41ef185eecd1a37fe3334c082cf85c6bdb.
- Scope boundary: this claim owns only the Running transition and primary index resource and is released after its clean commit. Wiki Researcher suite-local fixtures, scenarios, link validation, tests, review, verification, and integration require a separate canonical isolated claim.

## Completion Evidence

- Accepted source commit: dde9d061c139da880043f57153895faaffd06926; source claim released normally in event 933a2ee3-abe9-4875-97d1-adbf0c6b5f87.
- Current-main reconciliation commit a297b0547ed4f4b69c4fdb573d16c6dbdd44602a preserved the accepted three-file behavior and was independently verified; verifier claim released normally in event c033e7de-f3b4-4423-9fb1-056da343aba3.
- Integrated on main as 3ebf5974a43466936ea9f1e803e34ed199d947e5 with source provenance.
- Focused verification passed: five suite-local source-link tests, global catalog validation, Codex validate-only for the bounded Wiki Researcher source-link scenario with jobs 1, Python compilation, Git diff validation, and clean status.
- Integration claim integrate-wiki-research-source-links released normally in event 6e029910-096e-47af-bac1-591fb29ada65.
- No broad or full agent-catalog run was used for this item; that final-state gate remains campaign-level work.

## Summary

Require Wiki Researcher to resolve every local source link from the saved raw report before committing its handoff.

## Context

The bounded missing-topic research evaluation correctly checked maintained wiki coverage, used only the frozen primary sources, created exactly one collision-safe raw report, preserved docs/wiki, committed its work, and released its claim. The report linked the conflicting-source inventory as ../sources/conflicting-sources.md even though the fixture file was conflicting-sources.md at the repository root. The saved link therefore did not resolve from the report under raw.

The deterministic source-link gate returned FAIL and correctly skipped semantic judging. The complete evaluation did not edit the distributed Wiki Researcher or project-wiki-research skills.

## Evidence

- evals/agent-tests/wiki-researcher/scenarios.yaml defines the bounded missing-topic research and link-resolution contract.
- evals/agent-tests/wiki-researcher/fixtures/wiki-research contains the frozen coverage and source inventory.
- evals/agent-tests/results/2026-07-17-complete-agent-suites.md records the clean recovery-run failure.
- The live report used ../sources/conflicting-sources.md while the authoritative fixture path was conflicting-sources.md at repository root.

## Requirements

- Resolve local source paths from the final raw report location rather than from the working directory used during research.
- Validate every relative Markdown link before committing the report.
- Preserve exact source inventory paths when no relocation occurs.
- Distinguish external URLs from repository-relative source paths during validation.
- Fail cleanly before commit when a required local source link cannot resolve.
- Add focused coverage for root-level, nested, and moved raw report paths.

## Acceptance Criteria

- Every local source link in a saved Wiki Researcher report resolves from the report file.
- Root-level source inventories use the correct relative path from raw.
- Collision-safe report naming does not change link correctness.
- Coverage assessment, exclusions, uncertainty, claim lifecycle, and docs/wiki preservation remain correct.
- The Wiki Researcher bounded missing-topic research scenario passes its source-link gate repeatedly.
- Repository skill validation, generated-output checks, and unit tests pass.

## Dependencies

None.

## Verification

- Add focused link-resolution tests for Wiki Researcher report generation.
- Resolve every Markdown link from the report path in the synthetic fixture.
- Run the bounded missing-topic research scenario and inspect its raw report, commit, claim trace, Judge disposition, and cleanup.
- Run Agent Skill validation, generated-output freshness checks, repository unit tests, and Git diff validation.

## Notes

- Listing the right source name in prose does not compensate for a broken repository-relative link.
