# Integrate Inspect AI Reporting And Evidence

Status: Ready

Type: Feature

Provider: file

Work Item ID: integrate-inspect-ai-reporting-evidence

Completion: main-branch

Series: backlog/feature-backlog/inspect-ai-evaluation-adoption/index.md

## Summary

Make Inspect the diagnostic trajectory and score viewer while retaining a compact machine-verifiable governed acceptance projection and immutable evidence bundle.

## Context

Inspect can improve investigation and comparison, but the migration must not establish two competing acceptance authorities or reproduce another large custom report renderer.

Estimated complexity is High. Estimated generation is 160,000–280,000 tokens, or 0.89–1.56 total agent-hours, across 9–15 turns. Estimated non-model runtime is 1–3 hours.

## Source Evidence

The user authorized the phased Inspect-first adoption series on 2026-08-12. This item implements Phase 6 of that proposal.

## Requirements

- Define Inspect logs and viewer as diagnostic presentation, not acceptance authority.
- Project governed status, deterministic dispositions, identity, evidence digests, cleanup, and residual risk into a compact retained result.
- Bind the governed result to the corresponding Inspect log and evaluated source identities.
- Preserve offline or bundle-based viewing where supported.
- Compare the combined output with current HTML reports and retire only demonstrably redundant rendering code.

## Acceptance Criteria

- Users can navigate trajectories, tool activity, scores, timing, tokens, and artifacts through Inspect.
- Machines can independently verify governed status without trusting the UI.
- Missing or changed evidence makes the result non-current or non-passing.
- There is exactly one acceptance authority.
- The implementation removes or deprecates a measurable redundant reporting responsibility.

## Dependencies

prove-inspect-ai-exceptional-runtime-parity. Unblock when the capability routing table establishes every retained evidence source that reporting must represent.

Derived Queue Evidence: Stored lifecycle remains Ready. Series order derives effective Holding behind a healthy predecessor or effective Blocked behind the first genuinely Blocked predecessor; do not rewrite this record for either derived state.

## Verification

- Test log-to-result and result-to-evidence bindings, missing artifacts, digest drift, and mixed-run substitution.
- Perform usability review of representative PASS, BLOCKED, and infrastructure outcomes.
- Obtain independent artifact review.

## Open Questions

- Which current self-contained HTML capabilities remain necessary after adopting Inspect's bundled viewer?
