# Dev Backlog Coordinator Requirements Matrix

| Requirement | Canonical source | Deterministic evidence |
| --- | --- | --- |
| Parent identity is Dev Backlog Coordinator | Parent conceptual role and generated identity rule | Generated agent identity tests and harness-agent-identity |
| Persistence-selected managers own inventory and lifecycle | Work-item provider contract and parent role boundaries | test_persistence_routes_cover_supported_providers_without_fallback and provider-selector-boundaries |
| File, GitHub, and GitLab preserve native identifiers | Work-item provider contract | provider-selector-boundaries and provider-selected-workitem-ownership |
| Azure DevOps and Jira placeholders are BLOCKED with zero mutation | Work-item provider contract | test_persistence_routes_cover_supported_providers_without_fallback |
| Provider none has no durable inventory or capacity target | Work-item provider contract | test_persistence_routes_cover_supported_providers_without_fallback |
| UNSET asks whether to select the available file provider; unavailable selected skills stop without fallback | Selector decision rules | test_persistence_routes_cover_supported_providers_without_fallback |
| Successful new-item creation wakes the existing Coordinator for a fresh inventory read without dispatching from the notification path | New work-item notification contract | test_new_item_notification_only_prompts_inventory_reconciliation |
| Running capacity target is ten for durable inventory | Coordination queue target and parent role decisions | test_dispatches_ready_items_until_ten_are_running |
| Blockage entry disables only new secondary-thread dispatch and is safe to repeat | Coordinator role plus set-solo-mode | blockage-entry-disables-secondary-dispatch and test_blockage_entry_and_resumption_change_only_secondary_dispatch |
| Blockage recovery remains usable without a secondary-thread dispatch mechanism | Coordinator role plus resolve-backlog-blockage | blockage-recovery-resumes-secondary-dispatch and NOT_APPLICABLE simulator assertion |
| Dispatch resumes only after every blockage exit condition and is safe to repeat | Coordinator role plus set-multitask-mode | blockage-recovery-resumes-secondary-dispatch and test_blockage_entry_and_resumption_change_only_secondary_dispatch |
| No placeholder work when fewer than ten eligible items exist | Coordination queue target | test_dispatches_every_ready_item_when_queue_has_less_than_ten |
| Canonical execution identity is stored through the provider manager; canonical task id is additional only when coordinate-codex-tasks is active | Coordination execution record and conditional Codex mapping | capacity test plus canonical-id-persistence |
| User Action Required resumption preserves canonical execution; canonical Thread and Agent Task identities remain separate when coordinate-codex-tasks is active | User-decision contract and conditional Codex mapping | test_user_action_resumes_same_task_and_preserves_early_work and replacement rejection tests |
| Resumption requires pre-existing canonical identities plus priority, capacity when applicable, and root acceptance gates | Same-Thread user-decision and dispatch contracts | test_user_action_resumption_requires_recorded_identities and test_user_action_resumption_stops_at_each_dispatch_gate |
| Selected-provider resumption uses direct Coordinator and Orchestrator mutations while provider none stays task-local | Provider-neutral resumption contract | test_selected_provider_resumption_uses_direct_owner_boundaries and test_provider_none_resumption_has_zero_provider_mutation |
| Dirty ownership and premature delivery evidence remain preserved and unaccepted | User-decision recovery contract | test_user_action_resumes_same_task_and_preserves_early_work |
| Placeholder or unavailable providers and different dirty owners stop without provider mutation or ownership release | Provider and recovery boundaries | test_placeholder_provider_resumption_is_blocked_without_mutation, test_unavailable_selected_manager_blocks_resumption_without_mutation, and test_different_dirty_owner_blocks_dispatch_without_release |
| Ambiguous dispatch settles before one possible retry | Coordination dispatch reconciliation | test_settled_dispatch_contains_duplicate_without_retry |
| Delivery and provider-completion contention uses one immediate attempt plus notification-driven retry while named events remain independent | Event Contract contention protocol | test_claim_retry_requires_release_or_recovery_notification, test_release_notification_can_trigger_successful_retry, and test_claim_events_reject_notified_initial_attempt_and_keep_events_independent |
| Parent frees an unresolved durable slot truthfully only after notified recovery remains unavailable | Event Contract recovery handoff and parent role workflow | test_unresolved_notified_claim_frees_capacity_only_after_recovery |
| Exhausted corrections produce exactly one recovery, bounded retry, genuine user decision, or concrete continuing dependency decision for direct Coordinator application | Blocked disposition contract | exhausted-correction-disposition and test_exhausted_corrections_require_exactly_one_concrete_disposition |
| One bounded retry is consumed before a new non-retry reconciliation and cannot repeat | Blocked disposition contract | test_retry_is_consumed_before_a_new_non_retry_disposition |
| User Action Required includes an explanation and genuine user-owned decision | Blocked disposition contract | test_user_action_requires_a_genuine_user_owned_decision |
| Blocked resumption preserves canonical execution, candidate, review, verification, Git, claim, and attempt evidence plus conditional Codex identity | Blocked resumption contract | exhausted-correction-disposition preserved-evidence assertions |
| Effective Commit owns delivery after review and verification | Work-item completion contract and parent role delegation | selected-commit-retry-and-closeout and selected-commit-routing |
| Completion precedes runtime cleanup; Codex title and archival apply only when coordinate-codex-tasks is active | Coordination terminal cleanup and conditional Codex mapping | test_completion_handoff_precedes_parent_cleanup |
| Private-work claims and tiered verification remain scoped | Resource claim and validation tiers | test_private_work_claims_tiered_tests_and_post_facto_audits_are_executable |
| Parent immediately refills durable Running capacity after terminal cleanup | Coordination queue target and delivery handoff | provider-selected-ten-item-dispatch and suite Judge |
| Fifteen-minute review changes scheduling or recovery when needed | Coordination fifteen-minute parent review | provider lifecycle snapshot and fifteen-minute throughput summary outputs |
