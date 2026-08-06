---
name: commit-file-provider-transaction
description: Commit one exact file-provider creation or Future Idea promotion with no-overwrite writes, rollback, immutable proof, and unrelated-state preservation.
metadata:
  category: development-practice
---

# Commit File Provider Transaction

## Commit File Provider Transaction

This skill owns one discriminated transaction for file-provider creation. It accepts only the
ordinary-creation and future-idea-promotion operations. The caller owns record content and
validation. This skill owns path roles, no-overwrite mutation, resource coordination, exact
Git scope, rollback, immutable proof, and unrelated-state preservation.

ordinary-creation is the one-path shape for a complete ordinary work item or a complete
lightweight Future Idea capture. future-idea-promotion is the atomic two-path shape.

## Inputs And Operation Shapes

Resolve one complete exact canonical repository-relative manifest before mutation.

- ordinary-creation contains exactly one absent destination path, its complete validated bytes,
  its record identity, and no current source.
- future-idea-promotion contains exactly one retained current Future Idea path with its saved and
  intended bytes, one absent work-item destination with complete validated bytes, the destination
  Work Item ID, and a nonempty atomic rationale.

Reject unknown operations, multiple destinations, a promotion with a missing endpoint or
rationale, and every missing, inferred, title-derived, partial, wildcard, directory, absolute,
parent-traversing, or mismatched path. A conversation title never supplies a provider path.

Apply ordinary-creation only to one canonical file-provider record under backlog. Apply
future-idea-promotion only to one retained canonical record under backlog/future-ideas and one
canonical file-provider work-item destination under backlog. Do not use this transaction for
arbitrary repository files.

## Snapshot And Coordination

Require the repository's primary worktree on main. Return BLOCKED before mutation when the
worktree or branch does not have file-provider mutation authority.

Before mutation, capture and retain:

- Each manifest path's exact bytes, existence, file type, and resolved authority.
- The exact full Git index file bytes and existence from the worktree's resolved index path.
- The current HEAD object identifier.
- Every unrelated staged blob and its mode.
- Every unrelated tracked dirty byte sequence and untracked dirty byte sequence.

For ordinary-creation, the destination must be absent. For future-idea-promotion, the source
must be a regular file with the caller's exact saved bytes and the destination must be absent.
Reject a symlink, authority escape, identity mismatch, changed source, or target collision before
mutation.

Apply the loaded resource-coordination procedure when its event contract requires protection
for a manifest path. For future-idea-promotion, protect the retained source and destination as
one operation before changing either path. Preserve the resulting coordination evidence. Do not
restate or replace the selected coordination procedure here.

After every applicable source and destination path claim required by that procedure is acquired,
stop before mutation. Re-read and re-resolve every manifest path. When the procedure requires no
claim, perform the same revalidation after that decision and immediately before mutation. Compare
all of these values with the preflight snapshot:

- Current source bytes, file type, canonical containment, and authority.
- Continued destination absence and canonical destination containment and authority.
- The captured HEAD, exact Git index bytes and existence, unrelated staged blobs and modes, and
  unrelated tracked and untracked dirty bytes.

Return zero-mutation BLOCKED on any drift. Do not create a destination, write a source, stage, or
commit. Release acquired coordination only through the selected procedure's zero-mutation
failure boundary and report the mismatched snapshot evidence.

## No-Overwrite Mutation

Create every destination through the platform's exclusive-create operation. The
exclusive-create result is the no-overwrite authority. Do not replace it with a prior existence
check followed by an overwrite-capable write.

Write the complete destination bytes through the exclusive descriptor, synchronize them, and
close the descriptor. For future-idea-promotion, write the intended retained source bytes only
after exclusive destination creation succeeds. Validate both resulting regular files, exact
bytes, identity, destination rules, and reciprocal records before staging.

## Exact Path Commit

Every mutating Git argument vector must name all and only the manifest paths after --. Use the
equivalent of these forms:

```bash
git add -- backlog/type-backlog/item.md
git commit --only -m "Create file work item" -- backlog/type-backlog/item.md

git add -- backlog/future-ideas/idea.md backlog/type-backlog/item.md
git commit --only -m "Promote Future Idea" -- backlog/future-ideas/idea.md backlog/type-backlog/item.md
```

Do not use git add ., git add -A, directory or wildcard pathspecs, or an implicit index-wide
commit. Do not clear, replace, unstage, or commit unrelated index entries.

Capture the new commit object identifier immediately after commit creation. Do not infer success
from command exit alone when the commit result is uncertain. Reconcile HEAD and the exact object
before deciding whether a commit exists.

## Immutable Proof

Read the captured immutable commit object, not mutable worktree or index state. Require all of
these checks:

- Its parent equals the captured pre-transaction HEAD.
- Its changed-path set equals the exact operation manifest.
- Every committed manifest blob equals the validated intended bytes.
- An ordinary destination identity equals its filename stem where the record type requires it.
- A promotion source contains Promoted To with the destination Work Item ID.
- A promotion destination contains reciprocal Source Evidence with the exact source path and a
  Work Item ID equal to its filename stem.
- Every unrelated staged blob and mode, tracked dirty byte sequence, untracked dirty byte
  sequence, and index existence remains identical to the snapshot.

Release applicable coordination only after immutable proof and unrelated-state verification
succeed. Return the operation, exact manifest, commit object identifier, changed-path proof,
committed-byte proof, record identity proof, reciprocal proof when applicable, coordination
evidence, and unrelated-state proof.

## Rollback

If a failure occurs before an immutable commit exists, restore the retained source bytes and
file type, remove only the destination created by this attempt, and restore the exact full Git
index file bytes and existence. Verify every restored manifest path, unrelated worktree byte
sequence, unrelated staged blob and mode, and index byte before releasing coordination.

Never delete or overwrite a pre-existing target. Never use a broad checkout, reset, clean, or
index rewrite as a substitute for the saved exact state.

If an immutable commit exists but proof fails, do not rewrite history or report success. Keep the
commit and coordination evidence, return BLOCKED, and name the recovery owner and exact mismatch.
If rollback cannot restore and verify the exact pre-attempt state, retain coordination ownership
when the selected procedure requires it and return BLOCKED with the preserved snapshots and next
safe recovery action.
