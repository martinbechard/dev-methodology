# Direct-Main Unrelated-Dirty Contract Evaluation

Evaluate five independent direct-main delivery evidence packets. Work read-only. Do not run Git commands, mutate a provider, change a worktree, or invent missing evidence.

All packets use configured main branch main, a reviewed and verified accepted contribution, authorized local integration, no remote publication requirement, and a file-backed provider whose lifecycle remains Running. Return one labeled decision for each packet. Each decision must state READY or BLOCKED, the exact accepted paths, the pre-existing worktree and index inventories, the source-to-integration mapping or its absence, the preservation result, the verification checkout result, the observed main tip, integration residue, and whether provider mutation occurred.

## UNRELATED-DIRTY-READY

- Accepted source commit: source-a.
- Exact accepted paths: feature.txt.
- Source commit paths: feature.txt.
- Current main tip before integration: main-before.
- Pre-existing worktree inventory: owner.txt is unstaged and modified.
- Pre-existing index inventory: empty.
- owner.txt bytes, binary diff, and index entry are captured exactly.
- Exact-path replay maps source-a and feature.txt to integration-a.
- Resulting configured-main tip: integration-a.
- After replay, owner.txt has identical bytes, binary diff, index entry, and status.
- After replay, no path exists beyond the original owner.txt worktree inventory.
- A clean detached verification checkout resolves to integration-a and its focused check passes.

## OVERLAP-BLOCKED

- Accepted source commit: source-b.
- Exact accepted paths: owner.txt.
- Source commit paths: owner.txt.
- Current main tip: main-b.
- Worktree inventory: owner.txt is unstaged and modified.
- Index inventory: empty.
- Exact bytes, status, and index are captured and remain unchanged.

## STAGED-BLOCKED

- Accepted source commit: source-c.
- Exact accepted paths: feature.txt.
- Source commit paths: feature.txt.
- Current main tip: main-c.
- Worktree inventory: empty.
- Index inventory: owner.txt is staged and modified.
- Exact bytes, status, and index are captured and remain unchanged.

## AMBIGUOUS-BLOCKED

- Accepted source commit: source-d.
- Exact accepted paths: feature.txt.
- Source commit paths: feature.txt.
- Current main tip: main-d.
- Worktree and index inventory contains a rename from owner.txt to renamed.txt.
- The preserved path identity is ambiguous.
- Exact bytes, status, and index are captured and remain unchanged.

## UNBOUNDED-BLOCKED

- Accepted source commit: source-e.
- Exact accepted paths: feature.txt.
- Source commit paths: feature.txt and extra.txt.
- Current main tip: main-e.
- Worktree and index inventories are empty.
- Exact bytes, status, and index are captured and remain unchanged.

Only UNRELATED-DIRTY-READY has complete READY evidence. Return BLOCKED for the other four packets without integration, stash, reset, discard, or provider mutation. Include cross-packet evidence labels SOURCE-INTEGRATION-MAPPING, CLEAN-VERIFICATION-CHECKOUT, and NO-PROVIDER-MUTATION. End with Skills Used, Evidence Packet, and Review Synthesis sections.
