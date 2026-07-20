# Dev Backlog Coordinator Requirements Matrix

| Requirement | Canonical source | Deterministic evidence |
| --- | --- | --- |
| Parent identity is Dev Backlog Coordinator | Parent conceptual role and generated identity rule | Generated agent identity tests and harness-agent-identity |
| Work items are the only durable task records | Codex work-item coordination authority and execution-record sections | file-backed-ten-item-dispatch and simulator construction |
| Running capacity target is ten | Coordination queue target and parent role decisions | test_dispatches_ready_items_until_ten_are_running |
| No placeholder work when fewer than ten eligible items exist | Coordination queue target | test_dispatches_every_ready_item_when_queue_has_less_than_ten |
| Canonical task id is stored in the work item | Coordination execution record and dispatch rules | capacity test plus canonical-id-persistence |
| Ambiguous dispatch settles before one possible retry | Coordination dispatch reconciliation | test_settled_dispatch_contains_duplicate_without_retry |
| Integration and completion claims use separate thirty-minute bounded retry windows | Coordination claim retry window | test_claim_retry_window_is_bounded_to_thirty_minutes, test_successful_retry_stops_the_wait_window, and test_claim_windows_reject_out_of_order_and_separate_completion |
| Parent investigates an exhausted wait and frees an unresolved slot truthfully | Coordination claim retry window and parent role workflow | test_unresolved_wait_frees_capacity_only_after_investigation |
| Private task-owned implementation and review do not require shared project-file claims | Coordination private worktree boundary | test_private_work_claims_tiered_tests_and_post_facto_audits_are_executable |
| Dev Orchestrator owns direct delivery through distinct integration and completion claims | Coordination direct delivery and parent role delegation | bounded-integration-retry-and-closeout scenario and test_completion_handoff_precedes_parent_cleanup |
| Per-item tests are focused and the complete catalog is final-state only | Coordination tiered verification | test_private_work_claims_tiered_tests_and_post_facto_audits_are_executable and suite Judge |
| Work-item completion precedes parent worktree, branch, title, and archive cleanup | Coordination direct delivery and terminal state | test_completion_handoff_precedes_parent_cleanup |
| Parent immediately refills Running capacity after terminal cleanup | Coordination queue target and direct delivery | file-backed-ten-item-dispatch and suite Judge |
| Fifteen-minute review changes scheduling or recovery when needed | Coordination fifteen-minute parent review | file-backed queue snapshot and fifteen-minute throughput summary outputs |
| Scope and broad-test alternatives are post-facto improvements, not gates | Coordination post-facto efficiency audit | test_private_work_claims_tiered_tests_and_post_facto_audits_are_executable and semantic Judge contract |
