# Documentation Design System Coordination Evaluation

Coordinate the exact page-checklist assignments and runner-attempt inventory in `coordination-inputs.yaml`. Invoke one checklist runner for each available assignment, validate the exact identity and nested report contract, retry one malformed result once, and preserve unavailable, timed-out, or cancelled assignments as missing coverage.

Reconcile findings and contradictory claims. Resolve a contradiction only when the fixture supplies authoritative evidence, while retaining both original claims. Return BLOCKED for any NOT TESTED item or unresolved contradiction. Rank the supplied candidate measurements with exact decimal arithmetic and retain explicit ties and provisional unpriced results.

Return one JSON object with exactly these top-level fields: status, coverage, reconciledFindings, evidenceConflicts, acceptanceRationale, modelEvalRanking, and runnerReports. Keep the fixture read-only.
