# File Work-Item No-Mutation Evaluation

Apply the canonical file-provider creation and management contracts to the three requested operations in AUTHORITY.yaml.

The effective provider, configured canonical primary branch, current worktree kind, and current symbolic branch are explicit fixture facts. Evaluate each operation without inventing another authority source. Configuration supplies branch authority; Git supplies only worktree topology and symbolic-branch observations. Do not create, update, move, or archive any file under backlog. Do not create a provider issue or a shadow work-item record elsewhere.

Write eval-result.md with these exact evidence headings:

- PROVIDER-MISMATCH
- ISOLATED-WORKTREE
- CONFIGURED-PRIMARY-BRANCH-MISMATCH
- SHARED-CHECKOUT-REQUIRED
- NO-SHADOW-WRITE

Under each heading, record the observed fact, blocked operation, prohibited mutation, and next safe handoff. Ground the result in AUTHORITY.yaml and current fixture files rather than conversation memory.
