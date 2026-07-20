---
name: dev-backlog-steward-suite-contract
description: Share the canonical Dev Backlog Steward evaluation contract between its supervisor and Judge.
metadata:
  category: evaluation
---

# Dev Backlog Steward Suite Contract

Evaluate durable typed lifecycle state in the repository's configured backlog backend. Directly requested or explicitly authorized new items start Ready in their typed active queue; independently identified unauthorized ideas retain their underlying Type in User Action Required with one concrete approval question and remain non-dispatchable. Status: Proposed is invalid. New items need source context, requirements, acceptance, dependencies, and verification; claimed or resumed items need visible exclusive ownership. Recovery must reconcile item, claim, logs, results, and verification before completion or archival. A blocked handoff commits Status: Blocked, Owner: Unowned, and Claim: None while retaining the exact blocker, unblock condition, evidence, and acceptance criteria, then releases prior ownership so both item and registry are unowned. Reject an unowned Blocked to Running shortcut even when the unblock condition is satisfied. Resumption records eligible Ready state, successful acquisition of a new claim, the new owner, and only then Running. A failed or absent claim must restore the exact pre-attempt Blocked bytes, keep the item unowned and not Running, and preserve all prior evidence. Reject shadow backlogs, state-implied ownership, unsupported status changes, lost history, or unrecoverable handoffs. Judge item quality, ownership integrity, transition evidence, recovery, evidence preservation, and handoff completeness.
