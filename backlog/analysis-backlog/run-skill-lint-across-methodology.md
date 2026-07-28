# Run Skill Lint Across Methodology Skills

Status: Ready

Type: Analysis

Provider: file

Provider Reference: backlog/analysis-backlog/run-skill-lint-across-methodology.md

Completion: direct-main

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
