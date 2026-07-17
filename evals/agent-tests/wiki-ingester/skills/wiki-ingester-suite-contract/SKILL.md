---
name: wiki-ingester-suite-contract
description: Share the canonical Wiki Ingester evaluation contract between its supervisor and Judge.
metadata:
  category: evaluation
---

# Wiki Ingester Suite Contract

Evaluate raw-to-durable ingest with provenance and queue integrity. Require source reading, authoritative reconciliation, granular leaves, coherent hubs and navigation, item-level digest entries, validation, and a fresh Wiki Topic Verifier GOOD before moving a source. After the move, processed links must resolve and changed topic links require a fresh GOOD. Recheck all applicable queues and close the claim cleanly. Destination collisions or exhausted correction gates preserve the raw source and block completion. Judge boundary preservation, content durability, verifier order, link state, and closeout.
