# Align Agent Scenario Output Contract Fields

Status: Ready

Type: Defect

Provider: file

Owner: Unowned

Work Item ID: align-agent-scenario-output-contract-fields

Completion: main-branch

## Summary

Make the Agent scenario catalog outputContractFields for Dev Backlog Watchdog, Dev Backlog Steward, and Dev Orchestrator exactly match their canonical conceptual Agent definitions.

## Context

The catalog validator currently rejects three Agent entries because evals/agent-scenarios.yaml contains stale output field inventories. The conceptual role sources are authoritative for these public output contracts. Leaving the catalog out of sync blocks repository-wide evaluation validation and gives scenario authors an incomplete or obsolete contract.

The observed differences are:

- Dev Backlog Watchdog omits `blocked reconciliation results`.
- Dev Backlog Steward lists obsolete `ownership record` and `completion or blocked summary` fields instead of the canonical `provider maintenance result`, `backlog item, Future Idea, or status update`, and `blocked summary` set.
- Dev Orchestrator omits `confirmed issue dispositions`.

## Source Evidence

On 2026-08-06, while verifying project-wide conditional Agent skill routing, `/opt/homebrew/bin/python3.11 scripts/run-agent-skill-evals.py --validate-catalogs` reported that the outputContractFields for `dev-backlog-watchdog`, `dev-backlog-steward`, and `dev-orchestrator` do not exactly match their conceptual sources. A direct comparison with the three files under `agents/roles/dev-activities` confirmed the differences above. The user then instructed: "don't forget to log defects for corrections."

## Requirements

- Treat each canonical role source outputContract list as authoritative.
- Update only the stale catalog fields and directly affected evaluation expectations or generated artifacts.
- Preserve exact field spelling and ordering from each conceptual role source.
- Do not change a conceptual Agent output contract merely to satisfy the stale catalog.
- Add or strengthen a focused regression check that detects future catalog drift for these entries.

## Acceptance Criteria

- The three evals/agent-scenarios.yaml outputContractFields lists exactly equal their canonical role outputContract member names in the same order.
- The Agent scenario catalog validator reports no mismatch for Dev Backlog Watchdog, Dev Backlog Steward, or Dev Orchestrator.
- Focused tests demonstrate that conceptual role output-contract changes cannot leave the scenario catalog silently stale.
- No unrelated Agent behavior, output contract, scenario, or evaluation rubric changes.

## Dependencies

None.

## Verification

- Run `/opt/homebrew/bin/python3.11 scripts/run-agent-skill-evals.py --validate-catalogs`.
- Run the focused Agent scenario catalog tests.
- Run YAML parsing for evals/agent-scenarios.yaml and the three conceptual role sources.
- Run `git diff --check`.

## Open Questions

None.
