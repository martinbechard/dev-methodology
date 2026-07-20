# Governed Wiki Ingester Scenario: Verifier Failure

Attempt to ingest raw/provider-routing.md and stop safely when the independent verifier repeats the federation-ownership finding.

Use a fresh Wiki Topic Verifier context for the initial submission and after each of at most two genuine correction attempts. The governed finding remains federated ownership duplicated for all three submissions. Do not request a third correction or a fourth verdict.

After the third NEEDS_CORRECTION, keep the source in raw, preserve every substantiated local-routing conclusion, record the unresolved federation ownership in the appropriate page's Open Questions section with the missing decision and raw-source provenance, and recheck validation and queues. Before release, record the three verifier identities and verdicts, two correction attempts, latest finding, retained substantiated content, recorded open question, source location, clean-worktree check, and planned claim closeout in eval-result.md, then commit that governed BLOCKED result. Confirm the worktree is clean, release the claim, and record the actual release receipt in the terminal BLOCKED handoff. Do not mutate the repository after releasing the claim.
