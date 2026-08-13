# Work-Item Provider And Completion Contracts

## Purpose

This contract separates two project decisions:

- The Persistence selector chooses where durable work items are created and managed.
- The Commit selector chooses how verified delivery reaches a terminal state.

The Work-item content is the Work-item authority and is stored according to the Persistence provider's specific format.

The selectors compose independently. A repository, remote, template, installed tool, existing queue, or hosting account is evidence about available capabilities, not authority to select either value.

This document is the policy source for the provider, completion, renderer, role, evaluation, migration, and installed-bundle work that implements these contracts. It defines the intended steady state; it does not itself rename skills or implement provider tools.

## Selector Contract

PROJECT.yaml owns both selectors and the file-provider branch authority. The canonical keys are workflow_selection.persistence, workflow_selection.commit, and workflow_selection.canonical_primary_branch. The branch authority is one explicit scalar: main, master, or UNSET. Each selector default and each folder override contains exactly one supported value.

### Persistence selector

| Value | Meaning | Create skill | Manage skill | Operational support |
| --- | --- | --- | --- | --- |
| file | Work-item content is stored in repository files under backlog. | create-work-item-file | manage-work-items-file | Supported |
| github | Work-item content is stored in GitHub issues. | create-work-item-github | manage-work-items-github | Supported when the configured GitHub issue interface is available and authorized |
| gitlab | Work-item content is stored in GitLab issues. | create-work-item-gitlab | manage-work-items-gitlab | Supported when the configured GitLab issue interface is available and authorized |
| azure-devops | Work-item content would be stored in Azure DevOps work items. | create-work-item-azure-devops | manage-work-items-azure-devops | Unsupported placeholder; every create or manage operation returns BLOCKED without mutation |
| jira | Work-item content would be stored in Jira issues. | create-work-item-jira | manage-work-items-jira | Unsupported placeholder; every create or manage operation returns BLOCKED without mutation |
| none | The project has no durable work-item provider. | None | None | Supported for explicitly interactive work only; terminal evidence remains in the task result and durable create or manage operations are invalid |
| UNSET | The project has not selected a provider. | Not resolved | Not resolved | The pertinent agent asks for a user decision before a provider operation |

Management uses one exact manage-work-items Interface Skill and the manage-work-items-* Provider
Skill family. The terminal provider suffix keeps the interface stem intact. Creation remains a
separate one-item operation and does not belong to the management interface.

The create-work-item Interface Skill owns the provider-neutral creation contract. Creation providers use the create-work-item-* family. The create form is singular because one operation creates one independently actionable item. The manage form is plural because inventory, selection, lifecycle, recovery, and reconciliation operate over a provider-backed collection.

Every lifecycle consumer loads manage-work-items for the opaque identity, canonical lifecycle,
result vocabulary, and five public procedures. Project guidance selects exactly one management
provider from Persistence. The selected provider preserves the interface meanings while it owns
native inventory, storage, mutation, recovery, completion, and reporting behavior.

### Commit selector

| Value | Meaning | Completion skill | Operational support |
| --- | --- | --- | --- |
| main-branch | Integrate the final verified commit into main and observe it there before completion. | deliver-work-item-main-branch | Supported |
| feature-branch | Publish a verified feature branch, wait for required review and checks, and observe the configured merge before completion. | deliver-work-item-feature-branch | Supported |
| UNSET | The project has not selected a completion process. | Not resolved | The pertinent agent asks for a user decision before repository mutation or delivery publication |

Completion skill identifiers are action-centered because each skill owns the terminal delivery operation. Pull-request or merge-request creation is a subordinate publication capability, not a completion process.

### Folder overrides

Persistence and Commit folder overrides are resolved independently using the project's existing most-specific matching pattern rule. A Persistence override never changes Commit, and a Commit override never changes Persistence. Each effective value must pass the same validation as its corresponding default. Within one selector, an exact folder pattern may appear only once; validation rejects both a redundant duplicate with the same value and a conflict with different values, naming both indexed rows and selected values.

## Combination Matrix

The matrix distinguishes a valid executable combination, a valid decision boundary, a valid unsupported placeholder, and an invalid operation. A selected unsupported provider remains represented honestly; it is not silently converted into an invalid value or another provider.

| Provider | main-branch | feature-branch | UNSET completion |
| --- | --- | --- | --- |
| file | Valid. Persist under backlog in the primary worktree on the configured canonical primary branch and complete after main observation. | Valid. Persist under backlog in the primary worktree on the configured canonical primary branch, publish the delivery branch, enter AWAITING_REVIEW, and complete after merge observation. | Decision required before implementation or delivery; do not infer completion. |
| github | Valid. Manage the GitHub issue and complete after main observation. | Valid. Manage the GitHub issue, publish a pull request, enter AWAITING_REVIEW, and complete after merge observation. | Decision required before implementation or delivery; do not infer completion. |
| gitlab | Valid. Manage the GitLab issue and complete after main observation. | Valid. Manage the GitLab issue, publish a merge request, enter AWAITING_REVIEW, and complete after merge observation. | Decision required before implementation or delivery; do not infer completion. |
| azure-devops | Valid selector pair but operationally BLOCKED at the provider boundary. No external or local mutation. | Valid selector pair but operationally BLOCKED at the provider boundary. No external or local mutation. | Provider operations are BLOCKED; a later completion operation also requires an explicit decision. |
| jira | Valid selector pair but operationally BLOCKED at the provider boundary. No external or local mutation. | Valid selector pair but operationally BLOCKED at the provider boundary. No external or local mutation. | Provider operations are BLOCKED; a later completion operation also requires an explicit decision. |
| none | Valid only for an explicit interactive work item that needs no durable Work-item lifecycle. Return READY with task-local COMPLETED evidence after main observation. | Valid only for an explicit interactive work item that needs no durable Work-item lifecycle. Publish, record task-local AWAITING_REVIEW, then return READY with task-local COMPLETED evidence after merge observation. | Decision required before implementation or delivery. Durable create and manage operations remain invalid. |
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

## Canonical Work-Item Content

Every provider maps its native storage object to the following logical fields. Providers may store fields in issue bodies, labels, project fields, comments, file sections, or native state, but they must preserve the field's meaning and recovery evidence.

### Identity and creation

| Field | Contract |
| --- | --- |
| work_item_id | Opaque stable identifier owned and resolved by the selected provider. Generic callers pass it unchanged and never parse provider syntax. |
| provider | Effective provider selector value that owns the durable record. |
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
| delivery_reference | Main commit for main-branch, or branch plus pull-request or merge-request reference for feature-branch. |
| review_evidence | Independent review identity, outcome, findings, and correction disposition. |
| check_evidence | Exact commands or provider checks and their outcomes. |
| publication_evidence | Host-observed branch and pull-request or merge-request state when feature-branch is selected. |
| merge_evidence | Host or Git evidence that the configured merge occurred. Publication alone never supplies this field. |
| main_observation | Commit identity plus proof that it is reachable from the configured main branch. |
| terminal_evidence | Work-item lifecycle update, delivery evidence, claim release, and final state needed to prove the terminal outcome. For provider none, the interactive task result owns this evidence and the Persistence-update component is not applicable. |
| completed_at | Time completion was recorded after all terminal evidence existed. |

Sensitive, private, proprietary, credential, or company-internal evidence must remain in an appropriate private evidence store. Public Work-item content may link to a safe reference but must not disclose unsuitable content.

## Exact Work-Item Claim Contract

The claim system exposes one provider-independent scope keyed by the complete opaque work_item_id. The scope does not parse or infer provider type, repository, issue number, path, URL, lifecycle state, or delivery metadata. A live claim excludes every other activity on the same ID while distinct IDs coexist. Activity is exactly work for outcome work or update for provider mutation.

A work-item claim is separate from path and shared-resource claims. Apply each independently when its event occurs. A work-item claim does not grant repository-path or runtime-resource ownership, and those operational claims do not grant work-item ownership.

Before outcome work or provider mutation begins, the owner acquires the exact Work Item ID. At the activity boundary it releases with disposition exactly done, blocked, or handoff. Blocked may include one bounded opaque blocker reference; when present it must be canonical, non-empty, single-line, and at most 200 characters. Done and handoff prohibit that reference. Strict handoff sequencing uses ordinary exclusivity: the current owner releases with handoff before the next owner acquires the same ID. The lifecycle state in the Work-item content remains authoritative throughout this claim sequence.

The live registry and status preserve work_item_id and activity with the existing claim ID, incarnation ID, owner, root task, claim and heartbeat timestamps, checkout fields, and acquisition outcome. Acquisition, conflict, and release journal events preserve the same identity plus event outcome, release disposition, and blocker reference when applicable. Invalid or missing acquisition and release combinations are structured rejections and do not change the live registry. Legacy non-work-item releases remain disposition-free.

Claim reports retain their existing top-level version and add a separately versioned work_items section. It groups deterministic activity segments by Work Item ID with acquired and released times, activity, disposition, owner, duration, open state, and live state. Diagnostics identify missing release, release without acquisition, contradictory events, and historical non-work-item events. Historical records without a Work Item ID remain explicit diagnostics; the report never invents an ID.

## Exact File-Provider Transactions

Every file-provider mutation starts from a complete exact canonical repository-relative
provider-path manifest. commit-file-provider-transaction owns two creation shapes:
ordinary-creation has one absent destination, and future-idea-promotion has one retained source,
one absent destination, and one atomic rationale. manage-work-items-file retains lifecycle update,
move, and archive transactions. An unknown operation, invalid role shape, or missing, inferred,
wildcard, directory, partial, or mismatched manifest is invalid.

The shared creation transaction applies only to canonical file-provider Work-item files under backlog. Its
promotion source must be a retained canonical Future Idea. Created destinations must be absent
and use exclusive-create. Immutable proof covers the complete operation manifest.

The loaded resource-coordination procedure remains independent from file-provider behavior. Apply it before mutation and require its coordination evidence to agree with the exact manifest without copying its policy into the provider manager.

Every mutating Git argument vector names all and only the authorized provider paths after --. Staging must not use git add ., git add -A, directories, wildcards, or inferred paths. Commit creation uses a path-limited form such as git commit --only with the exact manifest paths instead of reusing the implicit full index. Unrelated staged blobs, tracked dirty bytes, and untracked dirty bytes remain exact.

The resulting immutable commit object must have a changed-path set, committed bytes, deletions, destination bytes, and Work Item IDs that match the full provider-owned manifest and every path role. Any mismatch is BLOCKED or failed and never lifecycle success.

## Future Ideas Are Not Work Items

The file provider reserves backlog/future-ideas for explicitly requested lightweight thoughts that are not yet actionable, approved, scheduled, or recognized as work. Durable Future Ideas are file-provider-only. When another Persistence provider applies, capture is BLOCKED unless the user explicitly selects file as the one-item override for that idea; the steward creates neither a provider issue nor a shadow file.

An idea contains a title, Synopsis, and Origin or Rationale. Notes and a free-text Revisit Trigger are optional. It has no lifecycle Status, Type, Owner, Dependencies, Acceptance Criteria, Verification, Provider, Work Item ID, or Completion field and does not enter ordinary provider inventory, runnable counts, dispatch, ownership, lifecycle transitions, or archives.

Only an explicit ideation or promotion operation reads or validates this folder. Idea and promotion target records must resolve to regular files inside their canonical file-provider authority. A symlink or resolved path that escapes the canonical root is rejected without reading external bytes.

Deliberate promotion retains the idea, adds Promoted To with the new Work Item ID, and creates one complete work item in an active, Holding, or User Action Required destination. The promoted item records file as Provider, its immutable filename-stem Work Item ID, exactly main-branch, feature-branch, or UNSET as Completion, and the retained idea path as an exact Source Evidence entry. Holding accepts the underlying dispatchable Type or the Holding Type. User Action Required retains its underlying dispatchable Type.

manage-future-ideas owns capture, explicit inventory, validation, and promotion. It constructs the
retained source, exclusive destination, reciprocal records, and atomic rationale. It then applies
commit-file-provider-transaction for the exact two-path mutation. create-work-item-file supplies
ordinary destination content and uses the same transaction skill for one-path creation.
manage-work-items-file excludes Future Ideas from ordinary lifecycle operations.

## Provider-Owned Work Item IDs

Generic create, inventory, read, transition, reconcile, complete, fail, and report operations accept one opaque Work Item ID. The selected provider owns its representation, uniqueness scope, lookup, storage, concurrency protection, mutation, publication, collision handling, terminal organization, and diagnostic location reporting. Generic lifecycle and Commit logic must not parse paths, URLs, issue numbers, or keys from that ID.

### File

- Authority exists exclusively under backlog in the primary worktree whose attached symbolic branch equals workflow_selection.canonical_primary_branch.
- The configured canonical primary branch must be main or master. UNSET, a missing or unsupported value, an isolated worktree, detached HEAD, or a different current branch blocks before any write, exclusive create, stage, or commit.
- Configuration supplies branch authority. Git is observational evidence only for primary-worktree topology and the current symbolic branch; remotes, tracking state, origin/HEAD, defaults, and the current branch never select the value.
- The Work Item ID is the immutable lowercase filename stem. It is globally unique across active, non-dispatchable, completed, and failed work-item folders. Existing records without an explicit field resolve to their filename stem during migration.
- Unique atomic creation uses no claim. Existing-item and archive claim behavior remains owned by Resource Claim. Every provider mutation still carries its complete exact path manifest and remains a separate verified commit.
- Isolated worktrees may read backlog state but do not author or archive the canonical backlog record.
- A completed item moves to the matching type folder under backlog/completed-backlog. Its Work Item ID remains unchanged; the destination path is diagnostic provider location evidence only.

Example Work Item ID: retry-queued-jobs.

### GitHub

- The configured GitHub issue interface owns creation, search, assignment, labels, project fields, comments, close, reopen, and retrieval.
- The provider-owned Work Item ID is repository identity plus issue number. The issue URL is diagnostic provider location evidence.
- A pull request is a delivery reference. It is never the work-item identifier unless a separate project contract explicitly makes pull requests the provider, which this selector does not.
- No shadow file is created under backlog. An explicitly requested export is a non-authoritative export and must say so.

Example Work Item ID: organization/repository issue 42.

### GitLab

- The configured GitLab issue interface owns creation, search, assignment, labels, milestones or project fields, notes, close, reopen, and retrieval.
- The provider-owned Work Item ID is GitLab instance plus namespace, project, and issue internal identifier. The issue URL is diagnostic provider location evidence.
- A merge request is a delivery reference and retains merge-request terminology. It is not renamed to pull request and is not the work-item identifier.
- No shadow file is created under backlog. An explicitly requested export is a non-authoritative export and must say so.

Example Work Item ID: gitlab.example/namespace/project issue 42.

### Azure DevOps

- The provider-owned Work Item ID is organization, project, and Azure DevOps work-item numeric identifier. Its URL is diagnostic provider location evidence.
- The placeholder create and manage skills report BLOCKED with the selected provider, attempted operation, missing implementation capability, and next action.
- The placeholder performs no Azure DevOps mutation, creates no local queue item, and does not fall back to GitHub, GitLab, file, or none.

Example Work Item ID: organization/project work item 42.

### Jira

- The provider-owned Work Item ID is Jira site plus issue key. The project key and numeric sequence retain Jira issue terminology. The browse URL is diagnostic provider location evidence.
- The placeholder create and manage skills report BLOCKED with the selected provider, attempted operation, missing implementation capability, and next action.
- The placeholder performs no Jira mutation, creates no local queue item, and does not fall back to GitHub, GitLab, file, or none.

Example Work Item ID: jira.example issue PROJ-42.

### None and UNSET

Provider none is an explicit decision that durable Work-item lifecycle is out of scope. It permits an interactive work item normalized in the active task, but it cannot satisfy a request to create, inventory, recover, or close a durable work item.

For provider none, the active task result is the complete non-durable record. It carries the normalized interactive work-item fields, completion disposition, source and integration commits, review and check evidence, main observation, clean claim state, lifecycle status COMPLETED, and completed-at time. Work Item ID, provider-native state, provider ownership mutation, provider terminal update, and provider manager are not applicable. The completion skill performs this task-local finalization after its delivery proof and does not dispatch a nonexistent provider skill.

Provider UNSET preserves the undecided state. At the first operation that requires provider persistence, the pertinent agent asks the user to choose file, github, gitlab, azure-devops, jira, or none. The answer is recorded as project intent before provider mutation. Silence and environmental evidence never resolve UNSET.

## Lifecycle And State Transitions

Two state dimensions remain separate:

- Work-item lifecycle status describes the work item from creation through terminal recording. Its values are listed in the table below. For provider none, the same lifecycle status exists only in the active task result.
- Completion disposition is returned by the selected completion skill. READY means the delivery proof is complete and the Work-item lifecycle update is ready to apply; AWAITING_REVIEW means feature-branch publication is valid but merge proof is incomplete; BLOCKED means the completion process cannot advance safely.

READY as a completion disposition is not the Work-item lifecycle status READY. A provider-backed item with completion disposition READY remains lifecycle RUNNING until its provider manager records terminal evidence and lifecycle COMPLETED. Provider none has no manager, so the completion skill records lifecycle COMPLETED in the task result before returning completion disposition READY.

The canonical Work-item lifecycle vocabulary is provider-neutral while native provider state remains provider-accurate.

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

Azure DevOps and Jira placeholder operations return BLOCKED without creating a remote or file-backed storage object. When no durable Work-item content exists, the task result carries the BLOCKED evidence; it must not pretend that a Work-item lifecycle transition was persisted.

## Completion Contracts

### Provider-neutral interface

The deliver-work-item Interface Skill owns the accepted commit input, Deliver Work Item procedure, READY, AWAITING_REVIEW, and BLOCKED meanings, state-keyed delivery evidence, and prepared Persistence handoff. Dev Orchestrator consumes this interface after independent review and verification accept a commit. AGENTS.md separately selects one provider from the deliver-work-item-* family through the effective Commit value.

The interface does not select a provider, implement integration or publication, mutate Persistence, or dispatch a provider manager. Each provider preserves this public meaning while retaining its own internal procedure and supported result refinements.

### Main branch

The deliver-work-item-main-branch skill owns these stages:

1. Confirm the scoped implementation commit, independent review, and required checks.
2. Acquire the exact shared integration authority.
3. Integrate the accepted commit into the configured main branch.
4. Run the smallest credible post-integration verification for the changed surface.
5. Observe the final verified commit as reachable from main and record the main commit identity.
6. Release integration authority from clean main.
7. Return completion disposition READY with the prepared lifecycle update. When a provider is selected, return that handoff to the caller; Dev Orchestrator directly applies the selected Persistence manager and reconciles the result. When provider is none, record lifecycle COMPLETED and the full terminal evidence in the active task result.

The work is not completed while the accepted commit exists only on an isolated branch, coordination branch, detached worktree, patch, or unmerged pull request or merge request. A clean cherry-pick or merge command is insufficient until the commit is observed on main and focused post-integration verification has passed or a documented completion policy explicitly accepts a scoped omission.

### Feature branch

The deliver-work-item-feature-branch skill owns these stages:

1. Confirm the scoped implementation commit, independent review, and required local checks.
2. Publish the intended feature branch.
3. Create or update the hosting-provider delivery record using provider-accurate terminology and tools: pull request for GitHub and merge request for GitLab.
4. Verify the published base, head, commit, title, body, readiness, checks, and dependency order.
5. Return AWAITING_REVIEW while any required review, check, approval, or configured merge remains incomplete. Dev Orchestrator directly applies the selected Persistence manager once to record that nonterminal lifecycle state and reconciles repeated observations without a duplicate update.
6. Return accepted source correction requests through Dev Orchestrator to the original Dev Coder. Consume the replacement candidate only after fresh independent review and verification, then resume the same branch and publication identity.
7. Observe required review approval, required checks, and the configured merge on the hosting service and in Git.
8. Observe the merged commit as reachable from the configured main branch.
9. Return completion disposition READY with the prepared lifecycle update. When a provider is selected, return that handoff to the caller; Dev Orchestrator directly applies the selected Persistence manager and reconciles the result. When provider is none, record lifecycle COMPLETED and the full terminal evidence in the active task result.

Branch publication, a ready review, an approved review, green checks, a closed delivery record, and a merge button action are each intermediate evidence. Completion requires the configured merge result and main observation. If a project uses a hosting service other than the work-item provider, the delivery reference records that host explicitly without changing the work-item provider.

### Failure and recovery

- A failed publish, review, check, integration, or main observation prevents completion disposition READY and lifecycle COMPLETED.
- After completion disposition READY has been returned, a failed or partially observed provider terminal update preserves READY as the successful delivery handoff but prohibits lifecycle COMPLETED. For feature-branch delivery, preserve lifecycle AWAITING_REVIEW for the same delivery identity. For main-branch delivery, preserve lifecycle RUNNING. Record lifecycle BLOCKED when safe reconciliation cannot continue. Never unconditionally reset lifecycle to RUNNING. A retry does not rerun or invalidate already accepted delivery evidence unless that evidence has become stale or contradictory.
- A correctable review finding preserves durable AWAITING_REVIEW for the same delivery identity while correction work resumes on the same item and branch. It does not transition the Work-item lifecycle back to RUNNING.
- AWAITING_REVIEW never authorizes lifecycle COMPLETED. Its one nonterminal Persistence update is distinct from the one terminal update authorized only by later Commit READY evidence.
- A provider terminal-update failure after merge follows the same delivery-mode recovery lifecycle while preserving delivery disposition READY and its evidence until reconciliation succeeds.
- A missing merge after successful publication remains AWAITING_REVIEW, not BLOCKED, unless a concrete prerequisite or failure prevents review or merge.
- A stale or interrupted execution resumes from the Work-item content, accepted candidate commit, claims, delivery reference, checks, and open issues rather than inferring success from a stopped task.

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
| create-backlog | create-work-item-file | Rename and move file creation, typing, series, user-decision, and short backlog-claim behavior into the file provider create skill. |
| manage-backlog | manage-work-items-file | Rename and move file inventory, lifecycle, recovery, archive, and short backlog-claim behavior into the file provider manage skill. |
| file-based-backlog | create-work-item-file and manage-work-items-file | Absorb routing and authority rules into the symmetric pair, then retire the routing skill. No compatibility alias after the migration gate. |
| github-issues-backlog | create-work-item-github and manage-work-items-github | Split creation from management while preserving GitHub-backed Work-item content authority and no-shadow-file behavior, then retire the combined skill. |
| execute-workitem | deliver-work-item, deliver-work-item-main-branch, and deliver-work-item-feature-branch | Move normalized shared delivery fields into the interface and split completion behavior by selector. Retire process selection from execute-workitem after all callers migrate. |
| execute-workitem terminal READY | Completion disposition READY plus Work-item lifecycle COMPLETED | Preserve READY as the completion skill's successful delivery disposition, not a Work-item lifecycle state. Migrate roles, callers, examples, and evaluations so READY authorizes the required Work-item lifecycle update; only the provider manager, or the provider-none task result, records lifecycle COMPLETED. |
| simple-workitem | main-branch | Replace the prototype process value and reference with the main-branch completion selector and skill. Preserve the stricter main-observation terminal rule. |
| feature-branch-workitem | feature-branch | Replace the prototype process value and reference with the feature-branch completion selector and skill. Extend publication-only AWAITING_REVIEW into observed-merge completion. |
| create-pull-request | deliver-work-item-feature-branch | Retain as a subordinate GitHub publication capability when used by the completion skill. It does not own terminal completion. GitLab uses a merge-request capability and terminology. |
| integrate-agent-work | completion skill selected by PROJECT.yaml | Retain as an integration capability for concurrent branches and worktrees. It supplies merge evidence but does not own Work-item lifecycle. |
| resource-claim | provider and completion skills | Retain as shared mutation-authority infrastructure. File provider operations and completion operations use separate narrow claim scopes. |

Creation providers belong to the create-work-item-* family, and create-work-item publishes their shared contract. Management providers belong to the manage-work-items-* family, and manage-work-items publishes their shared contract. The completion interface is deliver-work-item. Its providers are deliver-work-item-main-branch and deliver-work-item-feature-branch.

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

Applying the effective Commit skill yields the prepared delivery handoff. Commit AWAITING_REVIEW causes Dev Orchestrator to apply the selected Persistence manager once for a nonterminal update, then preserve the same delivery identity. Repeated observation reconciles that update without duplication. Commit READY permits one distinct direct terminal COMPLETED update and verification of the selected manager's result. Provider none retains AWAITING_REVIEW task-locally and returns READY with task-local COMPLETED finalization without provider mutation.

### File plus main branch

The file create skill records a READY item under backlog in the primary worktree on the configured canonical primary branch through atomic no-overwrite creation without a claim. The file manage skill records RUNNING ownership through the provider operation. Implementation, independent review, and verification occur separately in the private worktree. The main-branch Commit skill integrates the accepted commit, observes it on main, and returns Commit READY. Dev Orchestrator then applies the file manager directly for Persistence closure; the manager records terminal evidence and archives the item, and the orchestrator verifies closure.

### File plus feature branch

The file provider owns the backlog record while the feature-branch Commit skill owns publication and returns Commit AWAITING_REVIEW with the branch and delivery reference. Dev Orchestrator directly applies the file manager once to persist nonterminal AWAITING_REVIEW, then preserves that delivery identity. Accepted corrections resume the same item and branch without duplicating the recorded update. After required review, checks, merge, and main observation, the Commit skill returns Commit READY. Dev Orchestrator directly applies the file manager for the distinct terminal closure; the manager records COMPLETED and archives the item, and the orchestrator verifies the result.

### GitHub plus main branch

The GitHub create skill creates one issue and returns its issue URL. The GitHub manage skill records ownership without a shadow backlog file. The main-branch Commit skill integrates and verifies the commit, observes it on main, and returns Commit READY. Dev Orchestrator directly applies the GitHub manager for Persistence closure, then verifies that it recorded evidence and closed the issue according to project convention.

### GitHub plus feature branch

The GitHub issue remains the work-item identifier. The feature-branch Commit skill publishes a GitHub pull request as the delivery reference and returns Commit AWAITING_REVIEW. Dev Orchestrator directly applies the GitHub manager once to persist that nonterminal state. The same Commit delivery resumes through required review, checks, pull-request merge, and main observation without duplicating the update, then returns Commit READY. Dev Orchestrator directly applies the GitHub manager for the distinct terminal COMPLETED update and verifies that it closed the issue.

### GitLab plus main branch

The GitLab create skill creates one issue and returns its issue URL. The GitLab manage skill records ownership without a shadow backlog file. The main-branch Commit skill integrates and verifies the commit, observes it on main, and returns Commit READY. Dev Orchestrator directly applies the GitLab manager for Persistence closure, then verifies that it recorded evidence and closed the issue according to project convention.

### GitLab plus feature branch

The GitLab issue remains the work-item identifier. The feature-branch Commit skill publishes a GitLab merge request as the delivery reference and returns Commit AWAITING_REVIEW. Dev Orchestrator directly applies the GitLab manager once to persist that nonterminal state. The same Commit delivery resumes through required review, checks, merge-request merge, and main observation without duplicating the update, then returns Commit READY. Dev Orchestrator directly applies the GitLab manager for the distinct terminal COMPLETED update and verifies that it closed the issue.

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
- Main-branch main-observation and feature-branch AWAITING_REVIEW-to-merge behavior.
- Recovery from interrupted integration, review, provider update, and terminal recording.
- Exact migration ownership across source, metadata, roles, templates, renderer, generated artifacts, documentation, tests, examples, installer, and installed artifacts.
- A repository-wide and installed-bundle stale-name sweep after migration.

## Source Reconciliation

The provider-neutral creation contract is owned by [create-work-item](../skills/create-work-item/SKILL.md), and the [manage-work-items Interface Skill](../skills/manage-work-items/SKILL.md) owns the shared management vocabulary. File-provider creation and management are owned by [create-work-item-file](../skills/create-work-item-file/SKILL.md) and [manage-work-items-file](../skills/manage-work-items-file/SKILL.md). The migration table above records how create-backlog, manage-backlog, file-based-backlog, github-issues-backlog, and execute-workitem were replaced before their packages and active callers were removed. [create-pull-request](../skills/create-pull-request/SKILL.md) remains a subordinate GitHub publication capability of feature-branch completion, while [integrate-agent-work](../skills/integrate-agent-work/SKILL.md) and [resource-claim](../skills/resource-claim/SKILL.md) retain their independent integration and ownership responsibilities.

The [project configuration template](../skills/route-documentation-work/assets/templates/project-template.yaml), this repository's root PROJECT.yaml, and [render-agents-technology-skills.py](../scripts/render-agents-technology-skills.py) implement workflow_selection.persistence, workflow_selection.commit, and workflow_selection.canonical_primary_branch. Generated workflow guidance references the selected create, manage, and completion skills by name and renders the branch authority without deriving it from Git, while the existing folder technology mechanism remains separately inlined.

The renderer rejects the prototype workitem and backlog keys with deterministic mappings from simple-workitem, feature-branch-workitem, file-based-backlog, github-issues-backlog, none, and UNSET. When prototype and canonical fields coexist, it validates both shapes and reports every redundant or conflicting mapped default and exact-pattern override with both source paths and values. It preserves an explicit configured canonical primary branch through migration and normalizes legacy selector families that omit it to UNSET. A new canonical selector family that omits it is invalid. It preserves canonical maintainer selections, unsupported placeholders, and independent folder overrides without inferring or suggesting overwriting replacements. A combined override diagnostic names the exact rejected field and value, lists the selector-specific vocabulary, and directs the maintainer to split provider and completion overrides. The migration table remains the authority for downstream caller transitions; downstream work must not independently rename, split, alias, or reinterpret these identifiers.
