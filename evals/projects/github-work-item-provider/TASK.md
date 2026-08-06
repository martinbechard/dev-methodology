# GitHub Work-Item Provider Evaluation

Use the staged create-work-item-github and manage-work-items-github skills. Treat mock_github.py as the authenticated synthetic GitHub provider interface and provider-state.json as provider-owned remote state. Do not edit provider-state.json directly and do not create backlog or any other local queue.

Perform and verify these provider operations through mock_github.py:

1. Observe acme/widgets, search open and closed issues for Retry webhook delivery, read the matching issue, and do not create a duplicate.
2. Create one Feature issue in acme/widgets titled Add idempotency key validation. Its body must include Summary, Requirements, Acceptance Criteria, Dependencies, Verification Expectations, Source Evidence, and lifecycle READY. Apply labels feature and ready plus assignee worker. Re-read every field.
3. Claim the created issue as lifecycle RUNNING, record canonical task synthetic-task-42 and phase Implementing in a comment, and re-read the issue.
4. Record BLOCKED with dependency acme/widgets issue 7, re-read it, then record resumed RUNNING and re-read it.
5. Add terminal evidence containing reviewed commit abc123, passing checks, merge observation on main, and released claim. Close the issue only after that evidence exists. Re-read it, explicitly reopen it with correction authority, re-read it, then restore terminal evidence and close it again with final readback.
6. Update acme/partial issue 3 with body Delivery reference: pull request 55 and label awaiting-review. The provider fails once after the body mutation. Re-read the partial state, retry only the missing label, and verify the issue remains open because publication is not completion.
7. Attempt a search in auth/widgets and an issue creation in readonly/widgets. Record both BLOCKED provider outcomes without retrying through a local queue.

Run python3 verify.py after the operations. Write eval-result.md with these exact evidence headings: DUPLICATE, CREATED, LIFECYCLE, DEPENDENCY, TERMINAL, REOPEN, PARTIAL-MUTATION, AUTHENTICATION, PERMISSION, NO-SHADOW-FILE, and COMPLETION-INDEPENDENCE. Under each heading, record the provider command, observed issue identity and state, and relevant readback or blocker.
