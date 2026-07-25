# Dev Backlog Coordinator Requirements Matrix

| Requirement | Canonical source | Deterministic evidence |
| --- | --- | --- |
| Parent identity is Dev Backlog Coordinator | Parent conceptual role and generated identity rule | Generated agent identity tests and harness-agent-identity |
| Persistence-selected managers own inventory and lifecycle | Work-item provider contract and parent role boundaries | test_persistence_routes_cover_supported_providers_without_fallback and provider-selector-boundaries |
| File, GitHub, and GitLab preserve native identifiers | Work-item provider contract | provider-selector-boundaries and provider-selected-workitem-ownership |
| Azure DevOps and Jira placeholders are BLOCKED with zero mutation | Work-item provider contract | test_persistence_routes_cover_supported_providers_without_fallback |
| Provider none has no durable inventory or capacity target | Work-item provider contract | test_persistence_routes_cover_supported_providers_without_fallback |
| UNSET and unavailable selected skills stop without fallback | Selector decision rules | test_persistence_routes_cover_supported_providers_without_fallback |
| Running capacity target is ten for durable inventory | Coordination queue target and parent role decisions | test_dispatches_ready_items_until_ten_are_running |
| No placeholder work when fewer than ten eligible items exist | Coordination queue target | test_dispatches_every_ready_item_when_queue_has_less_than_ten |
| Canonical task id is stored through the provider manager | Coordination execution record and dispatch rules | capacity test plus canonical-id-persistence |
| User Action Required resumption preserves canonical Thread and Agent Task identities separately | Same-Thread user-decision contract | test_user_action_resumes_same_task_and_preserves_early_work and replacement rejection tests |
| Resumption requires pre-existing canonical identities plus priority, capacity when applicable, and root acceptance gates | Same-Thread user-decision and dispatch contracts | test_user_action_resumption_requires_recorded_identities and test_user_action_resumption_stops_at_each_dispatch_gate |
| Selected-provider resumption uses Steward mutations while provider none stays task-local | Provider-neutral resumption contract | test_selected_provider_resumption_uses_steward_boundaries and test_provider_none_resumption_has_zero_provider_mutation |
| Dirty ownership and premature delivery evidence remain preserved and unaccepted | User-decision recovery contract | test_user_action_resumes_same_task_and_preserves_early_work |
| Placeholder or unavailable providers and different dirty owners stop without provider mutation or ownership release | Provider and recovery boundaries | test_placeholder_provider_resumption_is_blocked_without_mutation, test_unavailable_selected_manager_blocks_resumption_without_mutation, and test_different_dirty_owner_blocks_dispatch_without_release |
| Ambiguous dispatch settles before one possible retry | Coordination dispatch reconciliation | test_settled_dispatch_contains_duplicate_without_retry |
| Delivery and provider-completion waits use the preserved thirty-minute schedule | Coordination claim retry window | test_claim_retry_window_is_bounded_to_thirty_minutes, test_successful_retry_stops_the_wait_window, and test_claim_windows_reject_out_of_order_and_separate_completion |
| Parent investigates an exhausted wait and frees an unresolved durable slot truthfully | Coordination claim retry window and parent role workflow | test_unresolved_wait_frees_capacity_only_after_investigation |
| Effective Commit owns delivery after review and verification | Work-item completion contract and parent role delegation | selected-commit-retry-and-closeout and selected-commit-routing |
| Completion precedes task cleanup | Coordination terminal cleanup | test_completion_handoff_precedes_parent_cleanup |
| Private-work claims and tiered verification remain scoped | Agent claim and validation tiers | test_private_work_claims_tiered_tests_and_post_facto_audits_are_executable |
| Parent immediately refills durable Running capacity after terminal cleanup | Coordination queue target and delivery handoff | provider-selected-ten-item-dispatch and suite Judge |
| Fifteen-minute review changes scheduling or recovery when needed | Coordination fifteen-minute parent review | provider lifecycle snapshot and fifteen-minute throughput summary outputs |
