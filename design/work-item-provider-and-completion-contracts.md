# Work-Item Provider And Completion Contracts

## Purpose

This contract separates two project decisions:

- The Persistence selector chooses where durable work items are created and managed.
- The Commit selector chooses how verified delivery reaches a terminal state.

The selectors compose independently. A repository, remote, template, installed tool, existing queue, or hosting account is evidence about available capabilities, not authority to select either value.

This document is the policy source for the provider, completion, renderer, role, evaluation, migration, and installed-bundle work that implements these contracts. It defines the intended steady state; it does not itself rename skills or implement provider tools.

## Selector Contract

PROJECT.yaml owns both selectors. The canonical keys are workflow_selection.persistence and workflow_selection.commit. Each default and each folder override contains exactly one supported value.

### Persistence selector

| Value | Meaning | Create skill | Manage skill | Operational support |
| --- | --- | --- | --- | --- |
| file | Repository files under backlog are authoritative. | create-file-work-item | manage-file-work-items | Supported |
| github | GitHub issues are authoritative. | create-github-work-item | manage-github-work-items | Supported when the configured GitHub issue interface is available and authorized |
| gitlab | GitLab issues are authoritative. | create-gitlab-work-item | manage-gitlab-work-items | Supported when the configured GitLab issue interface is available and authorized |
| azure-devops | Azure DevOps work items are authoritative in principle. | create-azure-devops-work-item | manage-azure-devops-work-items | Unsupported placeholder; every create or manage operation returns BLOCKED without mutation |
| jira | Jira issues are authoritative in principle. | create-jira-work-item | manage-jira-work-items | Unsupported placeholder; every create or manage operation returns BLOCKED without mutation |
| none | The project has no durable work-item provider. | None | None | Supported for explicitly interactive work only; terminal evidence remains in the task result and durable create or manage operations are invalid |
| UNSET | The project has not selected a provider. | Not resolved | Not resolved | The pertinent agent asks for a user decision before a provider operation |

Provider skill identifiers are symmetric: create-provider-work-item and manage-provider-work-items. The create form is singular because one operation creates one independently actionable item. The manage form is plural because inventory, selection, lifecycle, recovery, and reconciliation operate over a provider-backed collection.

### Commit selector

| Value | Meaning | Completion skill | Operational support |
| --- | --- | --- | --- |
| direct-main | Integrate the final verified commit into main and observe it there before completion. | complete-work-item-direct-main | Supported |
| feature-branch | Publish a verified feature branch, wait for required review and checks, and observe the configured merge before completion. | complete-work-item-feature-branch | Supported |
| UNSET | The project has not selected a completion process. | Not resolved | The pertinent agent asks for a user decision before repository mutation or delivery publication |

Completion skill identifiers are action-centered because each skill owns the terminal delivery operation. Pull-request or merge-request creation is a subordinate publication capability, not a completion process.

### Folder overrides

Persistence and Commit folder overrides are resolved independently using the project's existing most-specific matching pattern rule. A Persistence override never changes Commit, and a Commit override never changes Persistence. Each effective value must pass the same validation as its corresponding default. Within one selector, an exact folder pattern may appear only once; validation rejects both a redundant duplicate with the same value and a conflict with different values, naming both indexed rows and selected values.

## Combination Matrix

The matrix distinguishes a valid executable combination, a valid decision boundary, a valid unsupported placeholder, and an invalid operation. A selected unsupported provider remains represented honestly; it is not silently converted into an invalid value or another provider.

| Provider | direct-main | feature-branch | UNSET completion |
| --- | --- | --- | --- |
| file | Valid. Persist under primary-main backlog and complete after main observation. | Valid. Persist under primary-main backlog, publish the branch, enter AWAITING_REVIEW, and complete after merge observation. | Decision required before implementation or delivery; do not infer completion. |
| github | Valid. Manage the GitHub issue and complete after main observation. | Valid. Manage the GitHub issue, publish a pull request, enter AWAITING_REVIEW, and complete after merge observation. | Decision required before implementation or delivery; do not infer completion. |
| gitlab | Valid. Manage the GitLab issue and complete after main observation. | Valid. Manage the GitLab issue, publish a merge request, enter AWAITING_REVIEW, and complete after merge observation. | Decision required before implementation or delivery; do not infer completion. |
| azure-devops | Valid selector pair but operationally BLOCKED at the provider boundary. No external or local mutation. | Valid selector pair but operationally BLOCKED at the provider boundary. No external or local mutation. | Provider operations are BLOCKED; a later completion operation also requires an explicit decision. |
| jira | Valid selector pair but operationally BLOCKED at the provider boundary. No external or local mutation. | Valid selector pair but operationally BLOCKED at the provider boundary. No external or local mutation. | Provider operations are BLOCKED; a later completion operation also requires an explicit decision. |
| none | Valid only for an explicit interactive work item that needs no durable provider lifecycle. Return READY with task-local COMPLETED evidence after main observation. | Valid only for an explicit interactive work item that needs no durable provider lifecycle. Publish, record task-local AWAITING_REVIEW, then return READY with task-local COMPLETED evidence after merge observation. | Decision required before implementation or delivery. Durable create and manage operations remain invalid. |
| UNSET | Provider decision required before provider persistence; an already explicit interactive item may proceed only if the user also explicitly chooses no durable provider. | Provider decision required before provider persistence; an already explicit interactive item may proceed only if the user also explicitly chooses no durable provider. | Both decisions remain open and must be requested at their respective operation boundaries. |

The following combinations or uses are invalid and fail validation or operation dispatch with an actionable error:

- Any selector value outside the listed vocabulary.
- A provider skill that does not match the effective provider selector.
- A completion skill that does not match the effective completion selector.
- A create, inventory, lifecycle, recovery, or terminal provider operation when provider is none.
- A provider-backed source reference whose provider kind differs from the effective provider selector.
- A GitHub pull request treated as a GitLab merge request, or the reverse.
- A provider issue or work-item reference used as delivery evidence without the completion selector's required commit and merge evidence.
- An override that attempts to encode provider and completion as one combined identifier.

## Canonical Work-Item Record

Every provider maps its native record to the following logical fields. Providers may store fields in issue bodies, labels, project fields, comments, file sections, or native state, but they must preserve the field's meaning and recovery evidence.

### Identity and creation

| Field | Contract |
| --- | --- |
| work_item_id | Stable canonical provider identifier. It is never a branch, pull request, or merge request identifier. |
| provider | Effective provider selector value that owns the durable record. |
| provider_reference | Provider-accurate path, URL, or native reference used to retrieve the item. |
| type | Feature, Defect, Analysis, Investigation, or another project-authorized work type. |
| title | Durable, concise outcome name. |
| summary | Desired outcome and relevant current context. |
| requirements | Concrete behavior or deliverables. |
| acceptance_criteria | Observable completion conditions. |
| dependencies | Provider-accurate references to prerequisites. |
| verification_expectations | Checks and evidence required by the item. |
| source_evidence | Request, finding, decision, or durable source that authorized creation. |
| created_at | Provider-supported creation timestamp or recorded equivalent. |

### Ownership and lifecycle

| Field | Contract |
| --- | --- |
| status | Canonical lifecycle state mapped to, but not confused with, provider-native open or closed state. |
| owner | Current accountable agent, assignee, or provider-supported owner identity. |
| canonical_task_id | Stable execution-task identity when Codex coordinates the work. |
| branch | Delivery branch when one exists. It is not the work-item identifier. |
| worktree | Isolated checkout when one exists. Machine-local values must not be copied into portable project configuration. |
| phase | Current material execution phase. |
| claim_references | Current or released ownership claims required to explain shared mutation authority. |
| started_at | Time the item entered active execution. |
| updated_at | Most recent provider-supported lifecycle update time. |

### Recovery

| Field | Contract |
| --- | --- |
| accepted_candidate_commit | Reviewed candidate commit awaiting or used for integration. |
| wait_started_at | Start of an integration, completion, review, dependency, or user-decision wait. |
| attempt_count | Number of bounded retry attempts for the current wait. |
| last_attempt | Time and outcome of the latest attempt. |
| next_attempt | Next permitted retry time when a bounded schedule applies. |
| blocking_references | Exact claim, dependency, review, check, authority, or decision references. |
| open_issues | Unresolved issues with one owner and next action each. |
| recovery_note | Evidence needed to resume without relying on conversation history. |

### Delivery and evidence

| Field | Contract |
| --- | --- |
| completion | Effective completion selector value. |
| delivery_reference | Main commit for direct-main, or branch plus pull-request or merge-request reference for feature-branch. |
| review_evidence | Independent review identity, outcome, findings, and correction disposition. |
| check_evidence | Exact commands or provider checks and their outcomes. |
| publication_evidence | Host-observed branch and pull-request or merge-request state when feature-branch is selected. |
| merge_evidence | Host or Git evidence that the configured merge occurred. Publication alone never supplies this field. |
| main_observation | Commit identity plus proof that it is reachable from the configured main branch. |
| terminal_evidence | Provider lifecycle update, delivery evidence, claim release, and final state needed to prove the terminal outcome. For provider none, the interactive task result owns this evidence and the provider-update component is not applicable. |
| completed_at | Time completion was recorded after all terminal evidence existed. |

Sensitive, private, proprietary, credential, or company-internal evidence must remain in an appropriate private evidence store. A public provider record may link to a safe reference but must not disclose unsuitable content.

## Future Ideas Are Not Work Items

The file provider reserves backlog/future-ideas for explicitly requested lightweight thoughts that are not yet actionable, approved, scheduled, or recognized as work. Durable Future Ideas are file-provider-only. When another Persistence provider applies, capture is BLOCKED unless the user explicitly selects file as the one-item override for that idea; the steward creates neither a provider issue nor a shadow file.

An idea contains a title, Synopsis, and Origin or Rationale. Notes and a free-text Revisit Trigger are optional. It has no lifecycle Status, Type, Owner, Dependencies, Acceptance Criteria, Verification, Provider, Provider Reference, or Completion field and does not enter ordinary provider inventory, runnable counts, dispatch, ownership, lifecycle transitions, or archives.

Only an explicit ideation or promotion operation reads or validates this folder. Idea and promotion target records must resolve to regular files inside their canonical file-provider authority. A symlink or resolved path that escapes the canonical root is rejected without reading external bytes.

Deliberate promotion retains the idea, adds Promoted To with the canonical work-item reference, and creates one complete work item in an active, Holding, or User Action Required destination. The promoted item records file as Provider, its exact canonical path as Provider Reference, exactly direct-main, feature-branch, or UNSET as Completion, and the retained idea path as an exact Source Evidence entry. Holding accepts the underlying dispatchable Type or the Holding Type. User Action Required retains its underlying dispatchable Type.

Promotion is one failure-atomic primary-main transaction. Before any promotion mutation, the steward snapshots exact idea and target bytes and existence and the exact full Git index file bytes and existence. It stages only the reciprocal pair, uses a path-limited commit, captures the new commit OID, verifies that exact immutable object contains exactly both records and bytes, and leaves unrelated staged state intact. A pre-commit failure restores and verifies the worktree and index snapshots byte-for-byte. When resource coordination selects agent-claim, Event 1 protects the retained Future Idea update through a claim on only its exact current path; the uniquely named promoted target uses atomic no-overwrite creation without a target claim, and an existing target blocks promotion before mutation. Release the source-path claim after success or safe verified rollback, and retain it after unsafe rollback or post-commit reciprocal verification failure. When none is selected, no claim discovery, operation, registry mutation, release, or claim evidence occurs. In either mode, unsafe recovery reports BLOCKED with preserved evidence and the Dev Backlog Steward recovery owner.

## Provider Authority And References

### File

- Authority exists exclusively under backlog in the primary worktree whose branch is main.
- The canonical identifier is the repository-relative backlog path. The stable filename slug may be used as a display shorthand only when it is unambiguous.
- Unique atomic creation uses no claim. Existing-item Running transitions and terminal evidence claim the exact current path, while archive movement also claims the exact destination path; each mutation remains a separate commit.
- Isolated worktrees may read backlog state but do not author or archive the canonical backlog record.
- A completed item moves to the matching type folder under backlog/completed-backlog. The destination path becomes the terminal provider reference.

Example provider reference: backlog/feature-backlog/retry-queued-jobs.md.

### GitHub

- The configured GitHub issue interface owns creation, search, assignment, labels, project fields, comments, close, reopen, and retrieval.
- The canonical identifier is repository identity plus issue number. The canonical reference is the issue URL.
- A pull request is a delivery reference. It is never the work-item identifier unless a separate project contract explicitly makes pull requests the provider, which this selector does not.
- No shadow file is created under backlog. An explicitly requested export is a non-authoritative export and must say so.

Example provider identifier: organization/repository issue 42. Example reference shape: https://github.com/organization/repository/issues/42.

### GitLab

- The configured GitLab issue interface owns creation, search, assignment, labels, milestones or project fields, notes, close, reopen, and retrieval.
- The canonical identifier is GitLab instance plus namespace, project, and issue internal identifier. The canonical reference is the issue URL.
- A merge request is a delivery reference and retains merge-request terminology. It is not renamed to pull request and is not the work-item identifier.
- No shadow file is created under backlog. An explicitly requested export is a non-authoritative export and must say so.

Example provider identifier: gitlab.example/namespace/project issue 42. Example reference shape: https://gitlab.example/namespace/project/-/issues/42.

### Azure DevOps

- The canonical identifier shape is organization, project, and Azure DevOps work-item numeric identifier. The reference shape is the configured organization and project work-item URL.
- The placeholder create and manage skills report BLOCKED with the selected provider, attempted operation, missing implementation capability, and next action.
- The placeholder performs no Azure DevOps mutation, creates no local queue item, and does not fall back to GitHub, GitLab, file, or none.

Example provider identifier: organization/project work item 42. Example reference shape: https://dev.azure.com/organization/project/_workitems/edit/42.

### Jira

- The canonical identifier is Jira site plus issue key. The project key and numeric sequence retain Jira issue terminology. The reference shape is the configured Jira browse URL.
- The placeholder create and manage skills report BLOCKED with the selected provider, attempted operation, missing implementation capability, and next action.
- The placeholder performs no Jira mutation, creates no local queue item, and does not fall back to GitHub, GitLab, file, or none.

Example provider identifier: jira.example issue PROJ-42. Example reference shape: https://jira.example/browse/PROJ-42.

### None and UNSET

Provider none is an explicit decision that durable provider lifecycle is out of scope. It permits an interactive work item normalized in the active task, but it cannot satisfy a request to create, inventory, recover, or close a durable work item.

For provider none, the active task result is the complete non-durable record. It carries the normalized interactive work-item fields, completion disposition, source and integration commits, review and check evidence, main observation, clean claim state, lifecycle status COMPLETED, and completed-at time. Provider reference, provider-native state, provider ownership mutation, provider terminal update, and provider manager are not applicable. The completion skill performs this task-local finalization after its delivery proof and does not dispatch a nonexistent provider skill.

Provider UNSET preserves the undecided state. At the first operation that requires provider persistence, the pertinent agent asks the user to choose file, github, gitlab, azure-devops, jira, or none. The answer is recorded as project intent before provider mutation. Silence and environmental evidence never resolve UNSET.

## Lifecycle And State Transitions

Two state dimensions remain separate:

- Provider lifecycle status describes the work item from creation through terminal recording. Its values are listed in the table below. For provider none, the same lifecycle status exists only in the active task result.
- Completion disposition is returned by the selected completion skill. READY means the delivery proof is complete and the provider lifecycle update is ready to apply; AWAITING_REVIEW means feature-branch publication is valid but merge proof is incomplete; BLOCKED means the completion process cannot advance safely.

READY as a completion disposition is not the provider lifecycle status READY. A provider-backed item with completion disposition READY remains lifecycle RUNNING until its provider manager records terminal evidence and lifecycle COMPLETED. Provider none has no manager, so the completion skill records lifecycle COMPLETED in the task result before returning completion disposition READY.

The canonical provider lifecycle vocabulary is provider-neutral while native provider state remains provider-accurate.

| State | Entry condition | Permitted next states | Required evidence |
| --- | --- | --- | --- |
| READY | The item is authorized, complete enough to dispatch, and has no unmet prerequisite. | RUNNING, HOLDING, USER_ACTION_REQUIRED, ABANDONED | Creation authority, requirements, acceptance criteria, dependencies, verification expectations |
| RUNNING | One accountable owner and execution identity have accepted the item. | BLOCKED, USER_ACTION_REQUIRED, AWAITING_REVIEW, COMPLETED, FAILED, ABANDONED | Owner, canonical task id when applicable, branch or worktree, phase, start evidence |
| BLOCKED | A technical, dependency, capability, claim, or provider prerequisite prevents safe progress. | READY, RUNNING, FAILED, ABANDONED | Exact blocker, owner of next action, recovery evidence |
| USER_ACTION_REQUIRED | A genuine user decision, authority grant, value judgment, or user-held fact is required. | READY, HOLDING, FAILED, ABANDONED | One exact question, why user input is required, prohibited unattended action, recorded resolution when answered |
| HOLDING | The work is intentionally deferred without an immediate user question. | READY, ABANDONED | Deferral decision and resumption condition |
| AWAITING_REVIEW | Feature-branch publication is verified, but required review, checks, or configured merge evidence is incomplete. | RUNNING, BLOCKED, COMPLETED, FAILED, ABANDONED | Branch, commit, pull-request or merge-request reference, publication evidence, completed local verification |
| COMPLETED | The selected completion contract is satisfied and the provider terminal update has succeeded, or provider none has recorded the full terminal result in the active task. | None | Review, checks, main observation, released claims, and provider terminal evidence or the provider-none task result |
| FAILED | Delivery ended without satisfying completion and the outcome is recorded as terminal failure. | None, unless a provider-specific reopen creates READY | Failure evidence, preserved recovery context, provider terminal update |
| ABANDONED | Authorized direction ends the work without delivery. | None, unless a provider-specific reopen creates READY | Abandonment authority and provider terminal update |

Provider-native open, closed, reopened, resolved, done, label, assignee, board, or project-field states map to this vocabulary. They do not redefine it. A native closed state without required completion evidence is inconsistent and must be reconciled, not accepted as proof.

Azure DevOps and Jira placeholder operations return BLOCKED without creating a remote or file-backed record. When no durable record exists, the task result carries the BLOCKED evidence; it must not pretend that a provider lifecycle transition was persisted.

## Completion Contracts

### Direct main

The complete-work-item-direct-main skill owns these stages:

1. Confirm the scoped implementation commit, independent review, and required checks.
2. Acquire the exact shared integration authority.
3. Integrate the accepted commit into the configured main branch.
4. Run the smallest credible post-integration verification for the changed surface.
5. Observe the final verified commit as reachable from main and record the main commit identity.
6. Release integration authority from clean main.
7. Return completion disposition READY with the prepared lifecycle update. When a provider is selected, return that handoff to the caller without dispatching Persistence; Dev Orchestrator owns the later steward dispatch and reconciliation. When provider is none, record lifecycle COMPLETED and the full terminal evidence in the active task result.

The work is not completed while the accepted commit exists only on an isolated branch, coordination branch, detached worktree, patch, or unmerged pull request or merge request. A clean cherry-pick or merge command is insufficient until the commit is observed on main and focused post-integration verification has passed or a documented completion policy explicitly accepts a scoped omission.

### Feature branch

The complete-work-item-feature-branch skill owns these stages:

1. Confirm the scoped implementation commit, independent review, and required local checks.
2. Publish the intended feature branch.
3. Create or update the hosting-provider delivery record using provider-accurate terminology and tools: pull request for GitHub and merge request for GitLab.
4. Verify the published base, head, commit, title, body, readiness, checks, and dependency order.
5. Return AWAITING_REVIEW while any required review, check, approval, or configured merge remains incomplete. Dev Orchestrator asks Dev Backlog Steward exactly once to record that nonterminal lifecycle state for a selected provider and reconciles repeated observations without a duplicate update.
6. Return accepted source correction requests through Dev Orchestrator to the original Dev Coder. Consume the replacement candidate only after fresh independent review and verification, then resume the same branch and publication identity.
7. Observe required review approval, required checks, and the configured merge on the hosting service and in Git.
8. Observe the merged commit as reachable from the configured main branch.
9. Return completion disposition READY with the prepared lifecycle update. When a provider is selected, return that handoff to the caller without dispatching Persistence; Dev Orchestrator owns the later steward dispatch and reconciliation. When provider is none, record lifecycle COMPLETED and the full terminal evidence in the active task result.

Branch publication, a ready review, an approved review, green checks, a closed delivery record, and a merge button action are each intermediate evidence. Completion requires the configured merge result and main observation. If a project uses a hosting service other than the work-item provider, the delivery reference records that host explicitly without changing the work-item provider.

### Failure and recovery

- A failed publish, review, check, integration, or main observation prevents completion disposition READY and lifecycle COMPLETED.
- After completion disposition READY has been returned, a failed or partially observed provider terminal update preserves READY as the successful delivery handoff but prohibits lifecycle COMPLETED. For feature-branch delivery, preserve lifecycle AWAITING_REVIEW for the same delivery identity. For direct-main delivery, preserve lifecycle RUNNING. Record lifecycle BLOCKED when safe reconciliation cannot continue. Never unconditionally reset lifecycle to RUNNING. A retry does not rerun or invalidate already accepted delivery evidence unless that evidence has become stale or contradictory.
- A correctable review finding preserves durable AWAITING_REVIEW for the same delivery identity while correction work resumes on the same item and branch. It does not transition the provider lifecycle back to RUNNING.
- AWAITING_REVIEW never authorizes lifecycle COMPLETED. Its one nonterminal Persistence update is distinct from the one terminal update authorized only by later Commit READY evidence.
- A provider terminal-update failure after merge follows the same delivery-mode recovery lifecycle while preserving delivery disposition READY and its evidence until reconciliation succeeds.
- A missing merge after successful publication remains AWAITING_REVIEW, not BLOCKED, unless a concrete prerequisite or failure prevents review or merge.
- A stale or interrupted execution resumes from the provider record, accepted candidate commit, claims, delivery reference, checks, and open issues rather than inferring success from a stopped task.

## Selector Decision And Validation Rules

- Only explicit user direction or an accepted PROJECT.yaml value selects provider or completion.
- Repository files, remotes, issue templates, pull-request templates, merge-request templates, installed plugins, authenticated tools, existing issues, existing backlog files, and hosting metadata do not select either value.
- UNSET is preserved in templates and existing projects until an explicit decision is recorded.
- The agent asks only when the pertinent operation needs the unresolved selector. A provider decision may remain UNSET during work that needs no provider operation; completion must be resolved before repository mutation or delivery publication.
- Explicit task-level direction may select a value for that task when project guidance permits request-level override. It does not silently rewrite project-wide configuration.
- Unsupported Azure DevOps and Jira values pass vocabulary validation so their placeholder skills can report BLOCKED truthfully.
- Provider none passes vocabulary validation but fails any durable provider operation with an actionable explanation.
- Validation reports the exact key, rejected value or operation, supported values, and required corrective decision.

## Migration Map

The migration is atomic at the accepted steady state. Compatibility behavior exists only where this table assigns it; no hidden aliases are implied.

| Prototype or legacy identifier | Canonical owner | Disposition |
| --- | --- | --- |
| create-backlog | create-file-work-item | Rename and move file creation, typing, series, user-decision, and short backlog-claim behavior into the file provider create skill. |
| manage-backlog | manage-file-work-items | Rename and move file inventory, lifecycle, recovery, archive, and short backlog-claim behavior into the file provider manage skill. |
| file-based-backlog | create-file-work-item and manage-file-work-items | Absorb routing and authority rules into the symmetric pair, then retire the routing skill. No compatibility alias after the migration gate. |
| github-issues-backlog | create-github-work-item and manage-github-work-items | Split creation from management while preserving GitHub issue authority and no-shadow-file behavior, then retire the combined skill. |
| execute-workitem | complete-work-item-direct-main and complete-work-item-feature-branch | Move normalized shared work-item fields into this contract and split completion behavior by selector. Retire process selection from execute-workitem after all callers migrate. |
| execute-workitem terminal READY | Completion disposition READY plus provider lifecycle COMPLETED | Preserve READY as the completion skill's successful delivery disposition, not a provider lifecycle state. Migrate roles, callers, examples, and evaluations so READY authorizes the required provider lifecycle update; only the provider manager, or the provider-none task result, records lifecycle COMPLETED. |
| simple-workitem | direct-main | Replace the prototype process value and reference with the direct-main completion selector and skill. Preserve the stricter main-observation terminal rule. |
| feature-branch-workitem | feature-branch | Replace the prototype process value and reference with the feature-branch completion selector and skill. Extend publication-only AWAITING_REVIEW into observed-merge completion. |
| create-pull-request | complete-work-item-feature-branch | Retain as a subordinate GitHub publication capability when used by the completion skill. It does not own terminal completion. GitLab uses a merge-request capability and terminology. |
| agent-work-merge | completion skill selected by PROJECT.yaml | Retain as an integration capability for concurrent branches and worktrees. It supplies merge evidence but does not own provider lifecycle. |
| agent-claim | provider and completion skills | Retain as shared mutation-authority infrastructure. File provider operations and completion operations use separate narrow claim scopes. |

New provider skills are create-gitlab-work-item, manage-gitlab-work-items, create-azure-devops-work-item, manage-azure-devops-work-items, create-jira-work-item, and manage-jira-work-items. New completion skills are complete-work-item-direct-main and complete-work-item-feature-branch.

## Migration Coverage And Acceptance Gate

Before any implementation item declares the migration accepted, its owned scope must account for every surface below. The final integration item verifies the whole set together.

| Surface | Required steady state |
| --- | --- |
| Source skills | Canonical provider pairs and completion skills exist; retired definitions are removed only after all callers migrate. |
| Skill metadata | Directory names, frontmatter names, Codex metadata, prompts, invocation policy, and dependencies use canonical identifiers. |
| Conceptual roles | Definition-owned skill lists, conditions, examples, decisions, and output contracts use provider and completion independently. |
| PROJECT.yaml template and schema | provider and completion selectors replace prototype workitem and backlog selectors; values and overrides validate independently. |
| Renderer | Generated AGENTS.md names only the effective create, manage, and completion skills without copying procedures. |
| Generated adapters | Regenerated only from approved canonical sources; no generated file is edited directly. |
| Design documentation | Catalog, configuration, specialization, definition, lifecycle, and example pages use the canonical contract and provider-accurate terminology. |
| Evaluations and tests | Provider-completion matrix, unsupported placeholders, UNSET decisions, no inference, authority boundaries, completion-disposition versus lifecycle-state transitions, migration, and stale names have focused coverage. |
| Examples and fixtures | File, GitHub, and GitLab each demonstrate both completion processes; Azure DevOps and Jira demonstrate no-mutation BLOCKED outcomes. |
| Installer and bundle inventory | Canonical files are included, retired files are pruned according to ownership policy, and the installed bundle matches source. |
| Installed artifacts | User-scope refresh and runtime catalog evidence show canonical names only after the repository migration is accepted and deployed. |

Compatibility is transition-bounded:

- During implementation, one migration change may temporarily preserve an old caller while its owning canonical source is being updated in the same accepted sequence.
- The final integration gate rejects old selector keys, old selector values, retired skill identifiers, stale metadata, stale role references, stale generated adapters, stale design examples, stale evaluations, and stale installed bundle artifacts.
- No retired skill remains as a silent alias unless the user explicitly approves a separately documented deprecation period and exact removal condition.
- Generated mirrors change only through their approved source-category generators and must pass freshness checks.

## Contract Walkthroughs

Applying the effective Commit skill yields the prepared delivery handoff; it does not dispatch a provider manager. Commit AWAITING_REVIEW causes Dev Orchestrator to dispatch Dev Backlog Steward exactly once for a nonterminal Persistence update, then preserve the same delivery identity. Repeated observation reconciles that update without duplication. Commit READY permits one distinct steward dispatch for terminal COMPLETED and verification of the selected manager's recorded result. Provider none retains AWAITING_REVIEW task-locally and returns READY with task-local COMPLETED finalization without manager dispatch.

### File plus direct main

The file create skill records a READY item under backlog on primary main through atomic no-overwrite creation without a claim. The file manage skill records RUNNING ownership by claiming the existing item's exact current path for that short transaction. Implementation, independent review, and verification occur separately and claim-free in the private worktree. The direct-main Commit skill claims project-files immediately before integrating the accepted commit, observes it on main, and returns Commit READY after release. Dev Orchestrator then dispatches Dev Backlog Steward exactly once for Persistence closure. The file manager claims the exact current and completed-backlog destination paths, records terminal evidence, moves the item, commits the move, and releases that move claim; the orchestrator verifies closure.

### File plus feature branch

The file provider owns the backlog record while the feature-branch Commit skill owns publication and returns Commit AWAITING_REVIEW with the branch and delivery reference. Dev Orchestrator dispatches Dev Backlog Steward exactly once to persist nonterminal AWAITING_REVIEW, then preserves that delivery identity. Accepted corrections resume the same item and branch without duplicating the recorded update. After required review, checks, merge, and main observation, the Commit skill returns Commit READY. Dev Orchestrator then dispatches Dev Backlog Steward exactly once for the distinct terminal closure; the file manager records COMPLETED and archives the item, and the orchestrator verifies the result.

### GitHub plus direct main

The GitHub create skill creates one issue and returns its issue URL. The GitHub manage skill records ownership without a shadow backlog file. The direct-main Commit skill integrates and verifies the commit, observes it on main, and returns Commit READY. Dev Orchestrator dispatches Dev Backlog Steward exactly once for Persistence closure, then verifies that the GitHub manager recorded evidence and closed the issue according to project convention.

### GitHub plus feature branch

The GitHub issue remains the work-item identifier. The feature-branch Commit skill publishes a GitHub pull request as the delivery reference and returns Commit AWAITING_REVIEW. Dev Orchestrator dispatches Dev Backlog Steward exactly once to persist that nonterminal state. The same Commit delivery resumes through required review, checks, pull-request merge, and main observation without duplicating the update, then returns Commit READY. Dev Orchestrator dispatches Dev Backlog Steward exactly once for the distinct terminal COMPLETED update and verifies that the GitHub manager closed the issue.

### GitLab plus direct main

The GitLab create skill creates one issue and returns its issue URL. The GitLab manage skill records ownership without a shadow backlog file. The direct-main Commit skill integrates and verifies the commit, observes it on main, and returns Commit READY. Dev Orchestrator dispatches Dev Backlog Steward exactly once for Persistence closure, then verifies that the GitLab manager recorded evidence and closed the issue according to project convention.

### GitLab plus feature branch

The GitLab issue remains the work-item identifier. The feature-branch Commit skill publishes a GitLab merge request as the delivery reference and returns Commit AWAITING_REVIEW. Dev Orchestrator dispatches Dev Backlog Steward exactly once to persist that nonterminal state. The same Commit delivery resumes through required review, checks, merge-request merge, and main observation without duplicating the update, then returns Commit READY. Dev Orchestrator dispatches Dev Backlog Steward exactly once for the distinct terminal COMPLETED update and verifies that the GitLab manager closed the issue.

### Azure DevOps and Jira placeholders

For either selected provider and either completion value, the first requested provider operation invokes the matching placeholder. It reports BLOCKED with the operation and capability gap. It does not call an external mutation, create backlog content, or fall back. Completion selection remains recorded but cannot manufacture a work item or bypass the provider blocker.

### UNSET

An unset Persistence selection causes an explicit provider question only when persistence is needed. An unset Commit selection causes an explicit completion question before implementation or publication. The agent does not inspect remotes, files, tools, or templates to decide. Once answered, the selected Persistence and Commit values proceed independently through the applicable walkthrough.

## Verification Obligations

Each downstream implementation must provide focused evidence for its owned part of this contract. The final integration must demonstrate:

- Enumeration and validation of all provider and completion values.
- Independent default and folder-override resolution.
- Every cell in the combination matrix, including invalid operations.
- Symmetric create and manage identifier mapping for every provider.
- Shared-field round trips without provider-inaccurate naming.
- Primary-main-only file authority and absence of provider shadow files.
- No-mutation BLOCKED behavior for Azure DevOps and Jira.
- Direct-main main-observation and feature-branch AWAITING_REVIEW-to-merge behavior.
- Recovery from interrupted integration, review, provider update, and terminal recording.
- Exact migration ownership across source, metadata, roles, templates, renderer, generated artifacts, documentation, tests, examples, installer, and installed artifacts.
- A repository-wide and installed-bundle stale-name sweep after migration.

## Source Reconciliation

The file-provider creation and management procedures are owned by [create-file-work-item](../skills/create-file-work-item/SKILL.md) and [manage-file-work-items](../skills/manage-file-work-items/SKILL.md). The migration table above records how create-backlog, manage-backlog, file-based-backlog, github-issues-backlog, and execute-workitem were replaced before their packages and active callers were removed. [create-pull-request](../skills/create-pull-request/SKILL.md) remains a subordinate GitHub publication capability of feature-branch completion, while [agent-work-merge](../skills/agent-work-merge/SKILL.md) and [agent-claim](../skills/agent-claim/SKILL.md) retain their independent integration and ownership responsibilities.

The [project configuration template](../skills/development-methodology/assets/templates/project-template.yaml), this repository's root PROJECT.yaml, and [render-agents-technology-skills.py](../scripts/render-agents-technology-skills.py) implement workflow_selection.persistence and workflow_selection.commit. Generated workflow guidance references the selected create, manage, and completion skills by name, while the existing folder technology mechanism remains separately inlined.

The renderer rejects the prototype workitem and backlog keys with deterministic mappings from simple-workitem, feature-branch-workitem, file-based-backlog, github-issues-backlog, none, and UNSET. When prototype and canonical fields coexist, it validates both shapes and reports every redundant or conflicting mapped default and exact-pattern override with both source paths and values. It preserves canonical maintainer selections, unsupported placeholders, and independent folder overrides without inferring or suggesting overwriting replacements. A combined override diagnostic names the exact rejected field and value, lists the selector-specific vocabulary, and directs the maintainer to split provider and completion overrides. The migration table remains the authority for downstream caller transitions; downstream work must not independently rename, split, alias, or reinterpret these identifiers.
