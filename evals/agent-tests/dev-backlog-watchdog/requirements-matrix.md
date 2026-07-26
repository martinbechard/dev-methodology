# Dev Backlog Watchdog Requirements Matrix

| Requirement | Canonical source | Deterministic evidence |
| --- | --- | --- |
| Runtime identity is Dev Backlog Watchdog | Conceptual role and generated adapter | harness-agent-identity and generated identity tests |
| One standing child remains outside delivery capacity | Coordination dedicated-role contract | healthy-cycle-stays-quiet and active_capacity simulator test |
| Standing and heartbeat prompts render byte-identically | Coordination canonical templates | focused coordination template tests |
| Observation is strictly read-only | Watchdog role authority and coordination boundaries | no-forbidden-mutation and quiet-cycle deep-copy assertion |
| Healthy cycles return one concise no-action result | Watchdog output contract | healthy-cycle-stays-quiet and test_quiet_work_returns_no_action_without_mutation |
| Suspected lack of progress remains distinct from a known blocker | Stalled and Blocked semantics | suspected-stall-alert, test_suspected_stall_alerts_parent_without_setting_stalled, and test_known_preventing_cause_recommends_blocked_not_stalled |
| Every actionable cycle emits exactly one aggregate parent alert with provider identity, exact crossed boundaries and observed values, reason, and smallest Coordinator action | Watchdog output contract | suspected-stall-alert, test_task_state_anomalies_use_status_specific_actions covering mechanical reconciliation for Starting and Running stopped, failed, and missing states, known-cause Blocked preservation, estimate-boundary case, satisfied-exit-condition-alert, and singular alert assertions |
| Stalled and Blocked exit conditions are observed without disposition | Watchdog workflow | satisfied-exit-condition-alert and aggregate exit-condition simulator cases |
| Starting and Running alone consume capacity | Coordinator capacity contract | test_stalled_is_outside_starting_plus_running_capacity |
| Coordinator owns every Stalled disposition | Coordinator role and coordination workflow | test_coordinator_dispositions_are_evidence_gated |
| Stalled remains nonterminal and separate in series state | File provider lifecycle contract | test_series_and_archive_rules_keep_stalled_nonterminal |
| Failed and Abandoned archive only with terminal evidence | File provider lifecycle contract | terminal_archive_destination simulator assertions |
