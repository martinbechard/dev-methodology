# Backlog Lifecycle Evaluation

Reconcile the interrupted retry-policy work from the visible backlog item and the supporting claim, log, and result state.

Determine whether the item is queued, claimed, running, resumable, blocked, crashed, failed, or completed from durable evidence. Do not infer success from a stopped process, an ended log, or the absence of an error. Do not create a duplicate claim or move the item to a completed archive without delivery evidence.

Write backlog-status.md with counts by state, the retry-policy classification, the evidence used, the exact missing completion evidence, and the next safe action. Preserve the active item and recovery evidence. Save eval-result.md with Skills Used, Evidence Packet, and Review Synthesis sections.
