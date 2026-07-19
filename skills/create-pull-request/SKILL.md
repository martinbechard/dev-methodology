---
name: create-pull-request
description: Create, update, recreate, or prepare GitHub pull requests from verified branch state with accurate templates, draft or ready status, explicit dependencies, and clear review and merge order. Use when asked to open, publish, revise, restack, recreate, or mark a pull request ready, or to prepare its title and body.
metadata:
  category: development-practice
---

# Create Pull Request

Publish reviewable changes with truthful state, verified evidence, and an unambiguous dependency order.

## Authority

- When asked only to prepare a title or body, return that content without creating or changing a pull request.
- Create, update, close, recreate, or mark a pull request ready only when the request authorizes that external change.
- Treat pushing the named branch as part of an explicitly authorized pull-request publication workflow. Do not push unrelated branches or commits.

## Template Selection

Use the first applicable template:

1. A template or exact format named by the request.
2. The target repository's pull-request template.
3. The bundled [pull-request template](assets/pull-request-template.md).

Keep repository-required sections. Add Review Order and Review State when a repository template does not already capture them. Remove placeholders before publication.

## Workflow

1. Inspect the live branch, base, commits, diff, worktree state, remote state, existing pull requests, and completed verification.
2. Stop if the branch contains unrelated work, is dirty without an accepted explanation, exposes sensitive data, or lacks the commits intended for review.
3. Decide the smallest coherent pull-request topology before creating branches, commits, or pull requests. Record every scope boundary, base branch, dependency, and required review and merge sequence.
4. Build the title and body from current evidence. Describe the actual diff, exact checks and outcomes, review state, dependency order, and material risk. Do not claim checks that did not run.
5. Push only the intended reviewed branch state, then create or update each pull request with the correct base and head.
6. Verify the published title, body, base, head, draft or ready state, links, and stack relationships from the hosting service.
7. Return pull-request links in required review order, followed by state, checks, and any remaining blocker.

## Scope And Modularity

- Prefer multiple focused pull requests over one avoidably broad pull request when common prerequisites and independent changes can be reviewed and verified separately.
- Put shared foundations in a base pull request and place each independently reviewable feature, agent, component, or migration in its own dependent pull request. For several agent suites, normally create one common protocol and tooling pull request followed by one pull request per agent suite.
- Give each pull request one coherent purpose, its own meaningful verification, and only the dependencies required for that purpose.
- Keep work together when splitting would break an atomic behavior, separate a source generator from required generated outputs, leave a schema without its required consumers, or create trivial coordination overhead without improving reviewability.
- Do not use file count alone to decide the split. Split when a reviewer can understand, validate, and merge each unit in dependency order without unrelated changes obscuring the decision.
- If an avoidably broad pull request has no substantive review history, restack or recreate it as focused pull requests when the split remains safe. Preserve substantive review history and document the preferred future split when recreation would discard valuable evidence.

## Review Order

- Create a standalone pull request against its intended integration base.
- For a stack, create the base dependency first and each dependent pull request afterward. The review and merge sequence must follow the same order.
- Do not use creation order as a substitute for an explicit dependency statement, but keep numbering intuitive when the hosting service assigns numbers by creation time.
- If a newly created stack has reverse or misleading numbering, recreate the pull requests in dependency order before handoff when no substantive human review, comments, external references, or check history would be lost.
- Create and verify replacements before closing obsolete pull requests. Add replacement links to the obsolete pull requests and dependency links to the replacements.
- Preserve pull requests with substantive review history. Make their dependency order prominent and obtain explicit direction before discarding that history solely to improve numbering.

## Draft And Ready State

- Use draft status when the request asks for a draft or when planned changes, required checks, known blockers, or dependency work remains incomplete.
- Mark a pull request ready when its scoped implementation and required verification are complete and it is ready for human review.
- Do not leave a completed pull request in draft merely because it belongs to a stack.
- Do not mark incomplete work ready merely to simplify the handoff.

## Examples

- One verified branch with no dependency becomes one ready pull request against its integration base.
- A two-change stack creates the base pull request first, then the dependent pull request, and reports both links in that order.
- Four independent agent suites that share a protocol become one base pull request for the common protocol and four dependent agent-suite pull requests.
- A just-created stack with reversed numbering and no review history is recreated base-first before handoff.
- A reversed stack with substantive review comments is preserved, clearly cross-linked, and reported with its actual review order.

## Result

Return:

- title and pull-request URL
- base and head branches
- draft or ready state and the reason
- review and merge order
- verification evidence represented in the body
- recreated or superseded pull-request links
- remaining risks, checks, or blockers
