# Codex Work-Item Coordination Requirements Matrix

This matrix is implementation evidence for the supported skill and conceptual coordinator role. The supported skill is the procedure source of truth. The role assigns that procedure and bounds authority. The suite scenarios and fixtures provide deterministic contract coverage without recreating a competing repository-local skill.

| Requirement | Supported source evidence | Deterministic evaluation evidence |
| --- | --- | --- |
| Five explicit phases | skills/codex-workitem-coordination/SKILL.md phase protocol; agents/roles/dev-activities/dev-backlog-coordinator.role.yaml workflow | lifecycle-batons-and-artifact-scaling; phase-order |
| Exact primary baton and designated successor | Skill primary backlog baton section; role primary baton and wake obligations output | lifecycle-batons-and-artifact-scaling; lifecycle-baton-evidence |
| Parent-only non-polling wake chains | Skill wait and resume protocol; role parent wake ownership | decision-resolution-and-terminal-integrity; parent-only-wake |
| Adaptive active-work concurrency and named resource backoff | Skill adaptive concurrency section; role artifact campaign coordination | lifecycle-batons-and-artifact-scaling; artifact-concurrency-floor, adaptive-scaling, resource-backoff |
| Task-list audit after every measured dispatch batch | Skill dispatch anomaly audit; role canonical task registry | ambiguous-dispatch-and-just-in-time-resume; batch-anomaly-audit |
| Ambiguous dispatch identity reconciliation | Skill dispatch reconciliation fields; role queue and phase ledger and task identity rules | ambiguous-dispatch-and-just-in-time-resume; ambiguous-mutation, task-identity-fields |
| Delayed visibility, bounded settlement, one retry, and duplicate containment | Skill delayed visibility and retry boundary | ambiguous-dispatch-and-just-in-time-resume; delayed-visibility-settlement, retry-limit, duplicate-containment |
| Persistent canonical task id | Skill parent ledger; role canonical task registry output | ambiguous-dispatch-and-just-in-time-resume; canonical-id-persistence |
| Terminal archival eligibility and forbidden early archival | Skill terminal task housekeeping; role task housekeeping outcome | decision-resolution-and-terminal-integrity; archive-eligibility, forbidden-early-archive |
| Archive no-persist outcome is ambiguous | Skill archival tool outcome boundary | decision-resolution-and-terminal-integrity; archive-no-persist |
| User answer resolves the gate, not delivery | Skill decision-resolution lifecycle reference; role lifecycle delegation boundary | decision-resolution-and-terminal-integrity; exact-decision-provenance, no-repeat-question, ready-running-separation, completion-evidence-gate |
| Final full catalog only after accepted fixes integrate | Skill verification and integration routing; role adaptive campaign state | lifecycle-batons-and-artifact-scaling; final-catalog-order |
| Post-interruption live-state reconciliation | Skill interruption recovery; role queue and phase ledger | decision-resolution-and-terminal-integrity; interruption-reconciliation |
| Stable task id with bounded phase titles | Skill task display-state rules; role canonical task registry | ambiguous-dispatch-and-just-in-time-resume; title-stable-id, title-not-authority |
| Just-in-time dispatch across active and archived tasks | Skill just-in-time dispatch; role queue prioritization | ambiguous-dispatch-and-just-in-time-resume; just-in-time-dispatch, no-independent-predecessor-chain, no-active-wait-loop |
| Continuous independent review, verification, and integration | Skill artifact completion routing; role Dev Orchestrator dependency | lifecycle-batons-and-artifact-scaling; dependency-identity-and-order, final-catalog-order |

Review is blocked if any row lacks both an accepted supported source and the named deterministic scenario evidence after integration. A runtime result is verified only when the suite runner captures the configured agent identity and current source and adapter digests.
