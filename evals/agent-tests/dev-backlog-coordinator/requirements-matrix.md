# Codex Work-Item Coordination Requirements Matrix

This matrix is implementation evidence for the supported skill and conceptual coordinator role. The supported skill is the procedure source of truth. The role assigns that procedure and bounds authority. The suite scenarios and fixtures define the agent contract, while coordination_simulator.py and test_coordination_simulator.py execute deterministic state and decision checks without recreating a competing repository-local skill.

| Requirement | Supported source evidence | Deterministic evaluation evidence |
| --- | --- | --- |
| Five explicit phases | skills/codex-workitem-coordination/SKILL.md phase protocol; agents/roles/dev-activities/dev-backlog-coordinator.role.yaml workflow | lifecycle-batons-and-artifact-scaling; phase-order; test_mismatched_isolated_checkout_refuses_lifecycle_and_artifact_go |
| Exact primary baton and designated successor | Skill primary backlog baton section; role primary baton and wake obligations output | lifecycle-batons-and-artifact-scaling; lifecycle-baton-evidence |
| Parent-only non-polling wake chains | Skill wait and resume protocol; role parent wake ownership | decision-resolution-and-terminal-integrity; parent-only-wake; test_contention_wait_release_and_parent_resume_without_successor_polling |
| Adaptive active-work concurrency and named resource backoff | Skill adaptive concurrency section; role artifact campaign coordination | lifecycle-batons-and-artifact-scaling; test_scheduler_starts_three_scales_by_one_and_routes_finished_lane; resource-backoff |
| Task-list audit after every measured dispatch batch | Skill dispatch anomaly audit; role canonical task registry | ambiguous-dispatch-and-just-in-time-resume; batch-anomaly-audit |
| Ambiguous dispatch identity reconciliation | Skill dispatch reconciliation fields; role queue and phase ledger and task identity rules | ambiguous-dispatch-and-just-in-time-resume; ambiguous-mutation, task-identity-fields |
| Delayed visibility, bounded settlement, one retry, and duplicate containment | Skill delayed visibility and retry boundary | ambiguous-dispatch-and-just-in-time-resume; test_settled_matches_prevent_retry_and_contain_duplicate proves expectedRetryCount 0 and containment |
| Persistent canonical task id | Skill parent ledger; role canonical task registry output | ambiguous-dispatch-and-just-in-time-resume; canonical-id-persistence |
| Terminal archival eligibility and forbidden early archival | Skill terminal task housekeeping; role task housekeeping outcome | decision-resolution-and-terminal-integrity; archive-eligibility, forbidden-early-archive |
| Archive no-persist outcome is ambiguous | Skill archival tool outcome boundary | decision-resolution-and-terminal-integrity; archive-no-persist |
| User answer resolves the gate, not delivery | Skill decision-resolution lifecycle reference; role lifecycle delegation boundary | decision-resolution-and-terminal-integrity; exact-decision-provenance, no-repeat-question, ready-running-separation, completion-evidence-gate |
| Final full catalog only after accepted fixes integrate | Skill verification and integration routing; role adaptive campaign state | lifecycle-batons-and-artifact-scaling; final-catalog-order |
| Post-interruption live-state reconciliation | Skill interruption recovery; role queue and phase ledger | decision-resolution-and-terminal-integrity; interruption-reconciliation |
| Stable task id with bounded phase titles | Skill task display-state rules; role canonical task registry | ambiguous-dispatch-and-just-in-time-resume; title-stable-id, title-not-authority; test_success_title_is_exact_done_title |
| Just-in-time dispatch across active and archived tasks | Skill just-in-time dispatch; role queue prioritization | ambiguous-dispatch-and-just-in-time-resume; just-in-time-dispatch, no-independent-predecessor-chain, no-active-wait-loop |
| Continuous independent review, verification, and integration | Skill artifact completion routing; role Dev Orchestrator dependency | lifecycle-batons-and-artifact-scaling; test_scheduler_starts_three_scales_by_one_and_routes_finished_lane; dependency-identity-and-order, final-catalog-order |
| Fifteen-minute parent wake-obligation audit and concrete successor chain | Skill primary baton and wait or resume rules; role parent wake ownership | test_contention_wait_release_and_parent_resume_without_successor_polling persists source, successor, evidence, notification, acknowledgement, release, phase, audit interval, and zero polling; test_concrete_successor_chain_and_wiki_research_obligation fixes the authorized ids |

Review is blocked if any row lacks both an accepted supported source and the named deterministic scenario evidence after integration. A runtime result is verified only when the suite runner captures the configured agent identity and current source and adapter digests.
