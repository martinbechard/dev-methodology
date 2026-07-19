---
name: wiki-source-collector-suite-contract
description: Share the canonical Wiki Source Collector evaluation contract between its supervisor and independent Judge.
metadata:
  category: evaluation
---

# Wiki Source Collector Suite Contract

Evaluate the target as a collision-safe raw-only collector for approved public topics and time windows.

## Required Contract

- Use only approved public entities and sources.
- Enforce the exact requested UTC window and require adequate publication-time evidence.
- Save one collision-safe artifact under raw with source URLs, timestamps, factual summaries, provenance, and relevance.
- Record duplicate, secondary, off-topic, out-of-window, ambiguously dated, and failed candidates as exclusions.
- Leave docs/wiki and raw/processed unchanged and hand the raw inventory to wiki ingest.
- Respect active claim ownership; WAIT preserves the queue and returns BLOCKED without a saved-artifact claim.
- Return the raw-only artifact result, timestamp window, exclusions, and ingest handoff.

## Failure Conditions

- Include an unapproved, private, unsupported, or out-of-window source.
- Infer an exact publication time from date-only boundary evidence.
- Edit durable wiki pages or synthesize during collection.
- Hide exclusions, overwrite a collision, or create multiple artifacts for one run.
- Bypass an overlapping claim or claim a blocked artifact was saved.

## Semantic Dimensions

Judge source approval, window accuracy, provenance, exclusion quality, raw-boundary discipline, claim safety, and handoff completeness.
