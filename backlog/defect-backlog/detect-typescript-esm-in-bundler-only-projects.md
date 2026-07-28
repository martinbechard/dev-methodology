# Detect TypeScript ESM in bundler-only projects

Status: Ready

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/detect-typescript-esm-in-bundler-only-projects.md

Completion: direct-main

## Summary

Detect TypeScript ESM in bundler-only projects.

## Context

The primary affected skill is skills/typescript-esm/SKILL.md. The skill claims bundler ESM coverage, but activation requires package module mode or NodeNext and misses module: ESNext or moduleResolution: bundler projects.

## Source Evidence

The user authorized this independently dispatchable Ready Defect record on 2026-07-28. The accepted methodology skill-lint report at evals/results/2026-07-28-methodology-skill-lint.md, commit 54d860f1978d4cb403e59162cfb209fe45cc06a8, records this finding at 3; skills/typescript-esm/detection.yaml:9-18. Independent reviewer /root/confirm_critical_e accepted it as CONFIRMED_CRITICAL.

## Requirements

- Add a detection.yaml branch for bundler and ESNext TypeScript configurations.
- Preserve the documented ownership boundary and avoid unrelated provider, source, report, analysis, generated, or lifecycle mutation.

## Acceptance Criteria

- Bundler-only TypeScript projects activate the TypeScript ESM skill.
- The correction remains detection.yaml-only unless later scope evidence requires another path.
- The correction remains limited to the smallest source-backed scope.

## Dependencies

None

## Verification

- Require both typescript-esm and typescript for a bundler-only detector fixture.
- Run focused contract validation and git diff --check.
- Obtain independent review of the defect correction.

## Open Questions

None

## Notes

Collision reconciliation before creation found no active item with this provider reference, slug, affected skill, or overlapping accepted outcome.

This record has one primary affected skill identity: skills/typescript-esm/SKILL.md. It does not authorize a skill-definition mutation. The accepted smallest correction is detection.yaml-only and does not currently require governed-definition approval. If a later change reaches SKILL.md or governed metadata, it requires separate exact-path approval, provenance, and pre-mutation checking.
