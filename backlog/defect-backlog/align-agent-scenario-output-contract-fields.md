# Align Agent Scenario Output Contract Fields

Status: Running

Type: Defect

Provider: file

Owner: Dev Orchestrator task 019fda3b-119f-7412-a045-29b58108f4e1

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

## Starting Handoff Evidence

Starting Recorded At: 2026-08-07T03:17:03Z

Parent Coordination Thread: 019fb057-1767-7ef2-b5fa-41f4417b20b3

Launch Reservation: One Root Dev Orchestrator task for this exact work item.

Normalized Objective: Align the Dev Backlog Watchdog, Dev Backlog Steward, and Dev Orchestrator scenario output-contract field lists with their canonical conceptual Agent definitions, adding focused drift protection without changing those canonical contracts.

Dispatch Time: 2026-08-07T03:17:03Z

Intended Root Role: Dev Orchestrator

Launch Result: Started

Canonical Execution: 019fda3b-119f-7412-a045-29b58108f4e1

Last Contact: 2026-08-07T03:20:44Z

Next Reconciliation At: 2026-08-07T03:32:03Z

## Running Execution

Codex Task ID: 019fda3b-119f-7412-a045-29b58108f4e1

Conversation ID: 019fda3b-119f-7412-a045-29b58108f4e1

Root Role: Dev Orchestrator

Parent Task ID: 019fb057-1767-7ef2-b5fa-41f4417b20b3

Branch: codex/align-agent-scenario-output-contract-fields

Worktree: /Users/martinbechard/.codex/worktrees/aa61/dev-methodology

Phase: Implementation

## Active Execution Evidence

Condition Type: root-execution

Owner: Dev Orchestrator task 019fda3b-119f-7412-a045-29b58108f4e1

Evidence: The canonical root task is active, the exact work claim align-agent-scenario-output-contract-fields-work is live, and the clean private worktree is on the canonical branch at current main 667328765477ed2b63bc49ced6d66c4ff10cc826.

Observed At: 2026-08-07T03:20:57Z

Started At: 2026-08-07T03:20:44Z

Deadline or Expires At: 2026-08-07T05:20:44Z

Next Action: Dispatch one bounded Dev Coder lane for the catalog correction and focused regression coverage.

Next Reconciliation At: 2026-08-07T03:35:44Z
