---
name: methodology-design-system-checklist-runner-suite-contract
description: Share the strict Documentation Design System checklist-runner evaluation contract between its supervisor and Judge.
metadata:
  category: evaluation
---

# Methodology Design System Checklist Runner Suite Contract

Evaluate one exact page-checklist assignment. The coordinator-owned inventory must identify a non-empty page, checklist, and unique checklist IDs. Require exact identity, exactly-once check coverage, non-empty evidence, actionable findings for every FAIL, and missing-evidence limits for every NOT TESTED. Any NOT TESTED item takes status precedence over FAIL because incomplete evidence blocks integrated acceptance. Unavailable or ambiguous input must retain every expected ID as NOT TESTED. Reject malformed, null, empty, wrong-identity, duplicate, missing, or extra output without mutation, delegation, or integrated acceptance.
