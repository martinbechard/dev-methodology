# Governed Wiki Ingester Scenario: Verifier Failure

Attempt to ingest raw/provider-routing.md and stop safely when the independent verifier repeats the federation-ownership finding.

Use a fresh Wiki Topic Verifier context for the initial submission and after each of at most two genuine correction attempts. The governed finding remains federated ownership duplicated for all three submissions. Do not request a third correction or a fourth verdict.

After the third NEEDS_CORRECTION, keep the source in raw, restore every unaccepted wiki edit to the baseline, recheck validation and queues, and return BLOCKED. Record the three verifier identities and verdicts, two correction attempts, latest finding, restoration, source location, explicit no-change result, clean worktree, and released claim in eval-result.md.
