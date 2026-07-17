---
name: dev-runtime-diagnostician-suite-contract
description: Share the canonical Dev Runtime Diagnostician evaluation contract between its suite supervisor and independent Judge.
metadata:
  category: development-practice
---

# Dev Runtime Diagnostician Suite Contract

Evaluate the Dev Runtime Diagnostician as an evidence-driven investigator, not as a source-code fixer.

## Required Contract

- The failure has a bounded, observable reproduction or an exact explanation of why reproduction is blocked.
- Competing hypotheses are stated and tested against source, control-flow, process, log, resource, and runtime evidence as applicable.
- The diagnosis identifies the earliest relevant divergence and suspected runtime boundary.
- Symptoms, contributing conditions, suspected cause, verified cause, and unavailable evidence remain distinct.
- The fix path is the narrowest supported action, or the escalation path names the missing owner and evidence.
- Verification states what changed in the reproduction after the intervention.
- Every claimed process, port, browser, database, worktree, and temporary resource is cleaned up.
- The result includes reproduction, logs and suspected boundary, fix or escalation path, and verification result.

## Failure Conditions

- A symptom is relabeled as root cause without mechanism evidence.
- One convenient hypothesis is accepted without testing plausible alternatives.
- Product code is changed before the failure boundary is established.
- Dependency or environment unavailability is misreported as a product defect.
- Verification or cleanup is claimed without captured evidence.

## Semantic Dimensions

Judge reproduction quality, hypothesis discipline, earliest-divergence evidence, mechanism-level cause, boundary accuracy, verification integrity, and cleanup completeness.
