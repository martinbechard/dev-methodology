# Work-Item Management Provider Operations Evaluation

Evaluate the five public management operations for each provider as 25 independent representative cases. This is a read-only provider-contract exercise. Do not call a provider, inspect external state, mutate a work item, or create a fallback queue.

For file, GitHub, and GitLab, state the provider-specific inputs, authority check, intended provider action, verification readback, failure or ambiguous-outcome handling, and result fields for each case:

1. Inventory a mixed open and terminal selection containing two plausible matches.
2. Transition one observed READY item to RUNNING with an authorized owner and lifecycle evidence.
3. Reconcile completion after delivery disposition READY and all configured terminal evidence are present.
4. Recover after a transition response becomes ambiguous after a partial provider mutation.
5. Report the observed item identity, provider-native state, lifecycle state, evidence, blockers, and next action.

For Azure DevOps and Jira, route each of the same five requests to the provider's Required Result. Every result must be BLOCKED, use the exact public operation token, report no identifier, preserve the selected provider, and state that no provider or fallback mutation was attempted.

Return one labeled evidence block for every provider and operation. Use these exact labels:

- FILE-INVENTORY
- FILE-TRANSITION
- FILE-RECONCILE
- FILE-RECOVER
- FILE-REPORT
- GITHUB-INVENTORY
- GITHUB-TRANSITION
- GITHUB-RECONCILE
- GITHUB-RECOVER
- GITHUB-REPORT
- GITLAB-INVENTORY
- GITLAB-TRANSITION
- GITLAB-RECONCILE
- GITLAB-RECOVER
- GITLAB-REPORT
- AZURE-DEVOPS-INVENTORY
- AZURE-DEVOPS-TRANSITION
- AZURE-DEVOPS-RECONCILE
- AZURE-DEVOPS-RECOVER
- AZURE-DEVOPS-REPORT
- JIRA-INVENTORY
- JIRA-TRANSITION
- JIRA-RECONCILE
- JIRA-RECOVER
- JIRA-REPORT

Do not collapse providers into one generic answer. Preserve file paths and configured canonical-primary-branch authority for file, issue numbers and pull requests for GitHub, issue internal identifiers and merge requests for GitLab, and truthful zero-mutation BLOCKED results for Azure DevOps and Jira.
