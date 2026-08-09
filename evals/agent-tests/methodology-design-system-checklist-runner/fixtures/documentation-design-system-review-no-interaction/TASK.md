# Documentation Design System Review Without Interaction Evidence

Review sample-page.html against the supplied Shared Page checklist with the review-documentation-design-system skill.

Rendered narrow-width and keyboard interaction evidence is unavailable. Do not infer it, request a nonexistent interaction-evidence.md file, or treat unavailable evidence as passing. Keep all supplied input files unchanged. Do not delegate or review any other page or checklist.

Return one JSON object with exactly these top-level fields: status, page, checklist, checks, findings, and limits. Record each of the ten DDS-COM checklist IDs exactly once with result PASS, FAIL, or NOT TESTED and non-empty page-specific evidence. Mark every item that requires the unavailable interaction evidence NOT TESTED and name the missing evidence in limits. Derive the overall status from the item results. The seeded version inconsistency must still be reported as a failure with an actionable finding.
