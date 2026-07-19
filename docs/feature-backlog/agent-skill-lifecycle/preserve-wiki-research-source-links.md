# Preserve Wiki Research Source Links

Status: Ready

Type: Defect

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
