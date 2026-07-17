# Codex First-Wave Agent Suite Results

Date: 2026-07-17

Runtime: Codex 0.145.0-alpha.20 in disposable synthetic workspaces with isolated user and Codex homes, custom agents staged under the isolated Codex agents directory, multi-agent identity support enabled, and retained session identity evidence.

## Summary

| Suite | Scenario | Suite verdict | Target outcome |
|---|---|---|---|
| Dev Coder | TypeScript order pricing | PASS | Committed verified implementation |
| Dev Code Reviewer | Seeded TypeScript defects | PASS | All seeded defects reported |
| Dev Runtime Diagnostician | Unavailable runtime dependency | PASS | BLOCKED as expected |
| Project Bootstrapper | Valid configuration direct path | PASS | READY |

The initial runs were not accepted because Codex rejected hyphenated agent names or spawned generic task-labelled children without custom-agent identity evidence. Compatibility behavior was not promoted to a valid suite result. Corrected runs required underscore-safe names, explicit custom-agent identity support, isolated Codex agent staging, and session metadata plus developer-instruction fingerprints.

## Dev Coder

The exact supervisor, target, and Judge roles were verified. The target inspected callers and contracts, acquired a narrow claim, added tests before implementation, captured the expected missing-export RED state, implemented the asynchronous coupon boundary, and reached GREEN with seven focused tests. The full test command, separate build, and diff hygiene passed. The target committed exactly the three allowed files, released its claim, spawned no nested agents, and left a clean worktree. The independent Judge accepted every semantic dimension.

An earlier preflight was invalid because the applicable Organise Project Files skill was not staged. It stopped before target mutation and was not counted as an agent result. The scenario and common supervisor protocol now require all scenario-applicable conditional skills to be resolved and staged before target invocation.

Evidence digests:

- Supervisor report: 1e146f0d7edb3e28f3ad886dfdf6b820fcf645c92b83887e03a7926f642a28b1
- Target rollout: 573d1b54aaaef05d75c2b70dc8d36e803ee8dbd559253f87652f7fb727ee3cc6
- Judge rollout: d078725c8e67ed7c0e9e68816b5eb168669a0971c35c32a4008bf16970c4d7cf
- Candidate patch: 7152835630b82ded6cb827e6443d2e50cfc1e14da0badea474d3c772736eda32

## Dev Code Reviewer

The exact supervisor, target, and Judge roles were verified. The target reported the detached provider promise, swallowed provider rejection, and missing zero-through-one-hundred percentage validation with tight source and test evidence. TypeScript compilation passed and all three focused runtime tests reproduced the expected failures. The product tree remained unchanged.

The first Judge packet omitted the frozen Code Comments authority and produced an invalid FAIL. After the packet included the canonical role and assigned-skill rule excerpts, the same Judge amended its verdict and a fresh replacement Judge independently returned PASS. The suite supervision and judging contracts were corrected so assigned-skill authority is always included in governed Judge evidence.

Evidence digests:

- Target final: bee512abed2c3105af527565171469558e839d96348e68dcc21acfc09fd80a18
- Initial incomplete-packet Judge FAIL: 25f75e4466816fc30f4b3d81c316e1f1634ce320642d4cfeb91125704895ef15
- Fresh corrected-packet Judge PASS: 46b6340c822b189b31879d956deb72b22c276d6a5e4804d1d74937c546185977

## Dev Runtime Diagnostician

The exact supervisor, target, and Judge roles were verified. The local health test passed, the application reached the configured storage request, and no listener existed on the configured port. The target correctly kept dependency-side diagnosis BLOCKED, did not label the unavailable dependency as a product defect, proposed no source change, and returned the missing evidence and narrow escalation path. All deterministic gates and semantic dimensions passed.

Evidence digests:

- Target session: 2d7c08ca92c3ca4be4bdb83ed25a87030b6a1c9f08a7ed820d0dcd8a122cc452
- Judge session: d9891a6cbe02b3ceef2217e001b99983f804ab7a9454c00a03b5fc04f94e1a63
- Supervisor session: f1d44af5514cf8c9ffaff8803e96c93c74c33014a8479bb057716f9f5a84d14b

## Project Bootstrapper

The supervisor, target, documentation writer, artifact reviewer, verifier, and Judge identities were verified. Dependencies ran sequentially with one active child at a time. The target reused valid project configuration, skipped configuration detection and merge coordination, created only the missing README, produced one direct commit, passed independent review and verification, released every claim, and left a clean worktree. The independent Judge returned PASS.

Evidence digests:

- Judge verdict: e88898b2827149ed96c6a22a2eae7a9ceee32887b9070e5b93abadb35c2499a1
- Final report: d17ba5952935638c4713543da67ac5ee846d36f8af7f2c3534e47c990b6039df
- Frozen contract: 376c86e8a338438981caa379e36dbd9da3d2d8408631fa9f49fe6eea7f26336e
- Target evidence: 52a24b608e6fc83d175b997df0c724cdc5f24e7dea8c05f329aaca21f14f23c9

## Proven Infrastructure Defects

- Generated Codex names used portable hyphenated role ids that Codex rejected. A separate draft pull request changes only generated Codex name fields to underscores.
- Codex identity validation requires the custom-agent type and loaded developer instructions from retained runtime evidence. Task labels and child paths are insufficient.
- The ordinary workspace-write sandbox did not permit required claim and commit operations under Git metadata. Mutation fixtures need a scoped disposable permission profile covering both worktree files and Git metadata.
- Judge packets must include the canonical role and applicable assigned-skill rule excerpts when a candidate finding relies on those rules.
- Supervisors must resolve every conditional target skill against the frozen scenario and stage each applicable skill before invoking the target. A missing applicable skill is a preflight blocker, not a target failure.
- Supervisor-owned assertion command failures caused by quoting or path construction are infrastructure evidence, not target failures; the same frozen assertion may be corrected once and rerun without weakening it.

## Cleanup

Every run stopped its processes, removed copied authentication and disposable workspaces, released claims, and verified that no owned port, process, claim, worktree, or product mutation remained. Durable evidence contains hashes and governed transcripts without credentials.
