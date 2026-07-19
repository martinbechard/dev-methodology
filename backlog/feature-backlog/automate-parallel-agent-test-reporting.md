# Automate Bounded-Parallel Agent Test Reporting

Status: Proposed

Type: Feature

## Summary

Provide a repository-owned program that runs one, several, or all Agent test suites for a selected Codex or Junie harness with resource-aware bounded parallelism, writes an independent HTML report for every selected suite, and maintains a global HTML report that can be updated incrementally from regenerated suite reports.

## Context

The Agent test suites under evals/agent-tests have independent suite contracts and a shared runner, but operators need one repeatable entry point for selecting suites, using available resources safely, and reviewing results across the catalog. A monolithic report would make a one-suite rerun unnecessarily rebuild or rerun unrelated suites. The reporting contract therefore needs durable per-suite outputs as the aggregation source of truth.

Both Codex and Junie are supported harnesses. Junie credits are limited, so Junie verification must use selected smoke suites and deterministic test doubles rather than requiring or automatically triggering a full-suite Junie run. No Agent suite is run as part of creating this backlog item.

## Requirements

- Add one documented repository-owned command or program for Agent-suite execution and report generation.
- Require an explicit harness selection of Codex or Junie for every execution.
- Support selecting one suite, multiple named suites, or all cataloged suites when no suite selector is supplied.
- Reject unknown, duplicate, or incompatible suite selections with actionable diagnostics before starting harness work.
- Determine a safe default concurrency bound from the selected suite count and available host resources, including processor and memory constraints that can be measured portably.
- Support an explicit maximum-worker override while enforcing a finite upper bound and never starting more workers than selected suites or available resources permit.
- Preserve each suite's existing isolation, claim, checkpoint, evidence, cleanup, and terminal-status contract when suites run concurrently.
- Prevent concurrent suites from sharing mutable fixture, worktree, evidence, checkpoint, port, or report destinations.
- Stop scheduling new work and preserve completed reports when a global safety or resource boundary makes continued execution unsafe.
- Write one independent, self-contained HTML report for each selected Agent suite and harness run.
- Give each suite report a stable suite and harness identity, source revision, run time, terminal status, scenario results, deterministic and model-judge evidence, omissions, and links or references to retained evidence.
- Store enough machine-readable metadata with each suite report for deterministic global aggregation without parsing presentation text.
- Produce a global self-contained HTML report that summarizes all known suite reports, their harnesses, status, freshness, timing, and links.
- Build the global report from existing independent suite reports rather than rerunning Agent suites.
- Allow a regenerated single-suite report to update or replace only that suite's entry in the global report without rerunning or rebuilding every other suite report.
- Preserve unaffected global entries byte-for-byte or semantically unchanged during a one-suite update, apart from deterministic aggregate counts, ordering, freshness, and generation metadata.
- Detect and display missing, stale, malformed, duplicate, incompatible-revision, and mixed-harness suite reports instead of silently treating them as current passing results.
- Make report writes atomic so interruption cannot replace a valid suite or global report with a partial file.
- Keep report ordering, stable identifiers, relative links, accessibility, responsive layout, and offline behavior deterministic.
- Support a full Codex selection while keeping a full Junie selection an explicit operator choice that is never required by normal verification or run automatically by defaults intended for smoke coverage.
- Document commands for one suite, several suites, the default all-suite selection, report-only global rebuilding, and incremental global update from one regenerated suite report.

## Acceptance Criteria

- Selecting one suite starts exactly that suite and produces its independent HTML report plus an updated global report.
- Selecting several suites starts only those suites and never exceeds the resolved worker bound.
- Omitting suite selectors resolves to the complete current suite catalog for the chosen harness.
- Resource discovery and an explicit lower worker cap both reduce concurrency deterministically.
- A suite failure is visible in its report and global summary without erasing reports from other completed suites.
- Replacing one suite report and running the incremental aggregation path updates that global entry and aggregate totals without executing a harness or regenerating unrelated suite reports.
- A report-only rebuild can reconstruct the global report from the complete set of valid per-suite report metadata.
- Stale, missing, malformed, duplicate, incompatible-revision, and mixed-harness inputs remain visible as non-passing report states.
- Codex and Junie use the same selection, isolation, report, and aggregation contracts while retaining harness-specific invocation and identity evidence.
- Normal Junie verification passes with deterministic unit coverage and one or more selected smoke suites; no acceptance criterion requires a full Junie suite run.
- Reports remain usable without network access and meet keyboard, semantic-heading, table, contrast, and narrow-viewport accessibility expectations.

## Dependencies

None.

## Verification

- Add deterministic unit tests for catalog discovery, one/many/default-all selection, invalid selectors, resource calculation, worker overrides, scheduling bounds, cancellation, and partial failure.
- Add fixture-backed tests proving concurrent suites receive disjoint mutable destinations and preserve suite cleanup contracts.
- Add report-schema and rendering tests for passing, failing, blocked, stale, missing, malformed, duplicate, incompatible-revision, and mixed-harness inputs.
- Add incremental aggregation tests that regenerate one suite report, update the global report without harness execution, and prove unrelated suite entries remain unchanged.
- Add report-only rebuild tests using stored per-suite metadata.
- Run selected Codex smoke suites and, when authorized resources permit, one full Codex aggregation acceptance run.
- Run only selected Junie smoke suites for live-harness acceptance. Use fakes or local deterministic fixtures for full-selection scheduling and aggregation coverage; do not require or perform a full Junie run.
- Run Agent Skill validation, generated-output checks when affected, repository script tests, project-wiki tests, and Git diff validation.

## Notes

- Bounded parallelism means measured and configurable concurrency, not one process per catalog entry.
- Per-suite reports are durable aggregation inputs, not temporary fragments of the global HTML.
- Report freshness must be based on governed source and suite identities rather than file modification time alone.
- This item does not change suite semantics, weaken Judge requirements, or authorize external harness spending.
