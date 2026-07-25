# Migrate Dev Orchestrator Handoff Fixture Scenario Root

Status: Ready

Type: Defect

Owner: Unowned

Provider: file

Provider Reference: backlog/defect-backlog/migrate-dev-orchestrator-handoff-fixture-scenario-root.md

Completion: direct-main

## Summary

Restore the Dev Orchestrator handoff fixture's scenario-root layout so the fixture tests satisfy the runner's current containment validation.

## Context

Commit 8b7db47d introduced `_validate_scenario_roots` through `_audit_handoff_evidence` in `evals/agent-tests/runner.py`. The `_evidence_fixture` helper in `evals/agent-tests/dev-orchestrator/test_fixtures.py` still creates `fixtures/dev-orchestrator/candidate` instead of the selected scenario root at `fixtures/dev-orchestrator/dependency-routing/candidate`. Consequently every handoff test stops before its intended assertion with a missing `dev-orchestrator:dependency-routing` fixture-root RuntimeError.

The current baseline reproducer is:

```bash
PYTHONPATH=evals/agent-tests /Users/martinbechard/.pyenv/versions/3.11.10/bin/python3 -m unittest discover -s evals/agent-tests/dev-orchestrator -p 'test_fixtures.py'
```

It reports 20 failures and 4 errors at the common fixture-root boundary.

## Source Evidence

Fresh review during canonical task `019f981c-4fea-7b83-b8d2-0b254ff45f0c` confirmed this distinct current-baseline defect on 2026-07-25. The coder verified with blame that this fixture mismatch predates its implementation lane and that it did not modify `evals/agent-tests/dev-orchestrator/test_fixtures.py`. The user directed durable capture of every additionally confirmed distinct defect.

## Requirements

- Update the Dev Orchestrator handoff fixture setup to create the `dependency-routing` scenario root expected by the runner.
- Preserve the runner's containment enforcement introduced by commit 8b7db47d.
- Keep fixture paths contained under the disposable fixture root.
- Do not alter unrelated runner behavior or scenario fixtures.

## Acceptance Criteria

- `_evidence_fixture` creates `fixtures/dev-orchestrator/dependency-routing/candidate` for the dependency-routing scenario.
- The focused Dev Orchestrator handoff fixture suite no longer fails because `dev-orchestrator:dependency-routing` is missing.
- The updated fixture remains compatible with `_audit_handoff_evidence` and `_validate_scenario_roots`.
- Focused tests, `git diff --check`, and independent review pass.

## Dependencies

None.

## Verification

- Run the focused Dev Orchestrator fixture suite using the recorded reproducer.
- Run the focused runner handoff and scenario-root containment tests affected by the fixture layout.
- Run `git diff --check`.
- Obtain independent review.

## Open Questions

None.

## Notes

This transaction records the defect only. It does not dispatch a runtime task or authorize runner or fixture changes.
