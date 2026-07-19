---
name: agent-evidence-judging
description: Judge one agent-suite run independently from governed evidence after deterministic gates, without editing the candidate or inferring unsupported execution.
metadata:
  category: evaluation
---

# Agent Evidence Judging

Use this project skill only in the hardcoded read-only Judge for an agent-owned suite.

## Evidence Boundary

Accept only the frozen canonical agent definition, applicable assigned-skill rule excerpts, selected scenario, fixture manifest, deterministic results, target and dependency trace, candidate artifacts, final response, and evidence digests supplied by the supervisor. Treat missing governed evidence as missing, even when the candidate prose claims the action occurred. Treat supplied canonical role and assigned-skill instructions as governing contract evidence rather than requiring the product fixture to repeat those rules.

## Workflow

1. Verify that the supplied runtime identities, loaded developer instructions, and digests match the selected suite and scenario. Reject task labels and self-reported names as identity evidence.
2. Confirm that the supplied final result exists for every configured deterministic check. The runner owns ordered runtime traces and process-level execution cardinality; do not require the target or supervisor prose to reproduce evidence unavailable at the Judge boundary.
3. Stop with FAIL when a critical deterministic check failed. Do not perform compensating semantic scoring.
4. Evaluate each semantic dimension against cited governed evidence.
5. Check responsibility boundaries, allowed delegation, output-contract completeness, failure ownership, and terminal-status integrity.
6. Separate confirmed contract failures from missing evidence, environment blockers, stale inputs, and residual uncertainty.
7. Return the verdict and dimension-level evidence without editing any evaluated artifact.

A corrected harness-only retry after an assertion or capture defect is infrastructure evidence, not a target failure or blocker, when the frozen fixture, assertion, candidate artifacts, and target execution did not change. Judge the final complete deterministic result and report the retry as residual infrastructure uncertainty. Re-executing the target, changing the governed assertion, or changing the candidate remains a new evaluation and cannot use this allowance.

## Verdicts

- PASS requires all critical gates and every required semantic threshold.
- FAIL requires evidence of a target-agent contract violation.
- BLOCKED identifies an unavailable dependency, authority, harness capability, or fixture boundary that prevents judgment.
- STALE identifies a governed digest mismatch.

## Result

Return the suite and scenario identifiers, identity checks, deterministic summary, dimension scores when required, cited evidence, critical failures, final verdict, and residual uncertainty.
