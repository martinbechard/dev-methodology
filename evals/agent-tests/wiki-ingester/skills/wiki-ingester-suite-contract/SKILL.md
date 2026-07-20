---
name: wiki-ingester-suite-contract
description: Share the canonical Wiki Ingester evaluation contract between its supervisor and Judge.
metadata:
  category: evaluation
---

# Wiki Ingester Suite Contract

Evaluate raw-to-durable ingest with provenance and queue integrity. Require source reading, authoritative reconciliation, granular leaves, coherent hubs and navigation, item-level digest entries, validation, and a fresh Wiki Topic Verifier GOOD before moving a source. After the move, processed links must resolve and changed topic links require a fresh GOOD. Recheck all applicable queues and close the claim cleanly. Destination collisions or exhausted correction gates preserve the raw source and block completion. Judge boundary preservation, content durability, verifier order, link state, and closeout.

For the distinct final evidence-audit scenario, evaluate only the read-only whole-project reverse-engineering route. Require the target to inspect the integrated tree, path ledger, coverage manifest, navigation, links, and ownership; report each exact stale, contradictory, or missing artifact with its authoritative evidence, required work, and existing owner; and record an explicit no-change result. Any repository mutation, ingest claim, queue move, artifact correction, or Wiki Topic Verifier invocation fails this scenario.

Each ingest scenario must start from its own tracked fixtureBuilder output. The final-evidence-audit-read-only scenario instead starts from its dedicated executableCase directory copied into the protected workspace by the runner, with the runner-owned inventory baseline as the mutation authority; do not invoke an ingest fixtureBuilder for that scenario. Treat a missing declared source, destination, wiki baseline, audit evidence, or verifier-control input as test infrastructure and stop before target invocation. Do not borrow files from another suite's disposable state or create source evidence during supervision.

Pass the target's exact verifier child receipts, verdicts, page inventories, and ordered artifact transitions to the Judge. When raw retained-session parent binding is unavailable inside the supervisor, label that identity evidence pending the runner post-audit rather than skipping semantic judging. The runner's retained-session audit remains mandatory and invalidates the batch if a receipt does not bind to the declared Wiki Topic Verifier dependency.
