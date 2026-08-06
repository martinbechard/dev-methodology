# Backlog Management Skill Group

## Scope

Backlog Management is independent of Resource Coordination and Commit delivery. AGENTS.md selects one creation skill and one management skill for the effective Persistence provider.

The applied-model conventions are defined in [Object-Oriented Skill Group Models](../object-oriented-skill-group-models.md#2-applied-model-legend).

## Design

Backlog Management owns work-item creation, provider lifecycle management, and blockage recovery. The overall view shows the participating Agents and related Skill Groups; the scenario views expand the two provider families, sequential blockage recovery, and optional resource coordination.

### Overall Agent And Skill Group Dependencies

The overall view shows which Agents use Backlog Management and where backlog procedures conditionally use Concurrent Tasking or Resource Coordination. An arrow between Skill Groups means that at least one skill in the source group depends on a skill in the target group under the stated condition.

```mermaid
classDiagram
    direction LR

    namespace BacklogManagementAgents["Backlog Management Agents"] {
        class DevBacklogCoordinator {
            <<Agent>>
        }
        class DevBacklogSteward {
            <<Agent>>
        }
        class DevBacklogWatchdog {
            <<Agent>>
        }
    }

    namespace DevActivitiesAgents["Dev Activities Agents"] {
        class DevOrchestrator {
            <<Agent>>
        }
    }

    class BacklogManagement["Backlog Management"] {
        <<Skill Group>>
    }
    class ConcurrentTasking["Concurrent Tasking"] {
        <<Skill Group>>
    }
    class ResourceCoordination["Resource Coordination"] {
        <<Skill Group>>
    }

    DevBacklogCoordinator --> BacklogManagement
    DevBacklogSteward --> BacklogManagement
    DevBacklogWatchdog ..> BacklogManagement : when a blockage criterion or active recovery applies
    DevOrchestrator --> BacklogManagement
    BacklogManagement ..> ConcurrentTasking : when sequential recovery changes secondary-thread dispatch mode
    BacklogManagement ..> ResourceCoordination : when the selected file provider mutates shared state
```

### Scenario: Creating A Work Item

This scenario applies when an Agent must create one durable work item. The create-work-item Interface Skill states the shared contract. The create-work-item-* family contains its providers, and AGENTS.md selects the provider that matches the project Persistence setting.

```mermaid
classDiagram
    direction LR

    class DevOrchestrator {
        <<Agent>>
    }
    class CreateWorkItem["create-work-item"] {
        <<Interface Skill>>
        +work-item-id
        +create-work-item(workItemDescription)
    }
    class ProjectSpecificDirectives["Project-specific directives"] {
        <<AGENTS.md>>
        <<routing>>
        +route create-work-item => create-work-item-*
    }
    class create-work-item-file {
        <<Provider Skill>>
        +work-item-id
        +create-work-item(workItemDescription)
        +future-ideas-capture()
        +future-idea-promotion()
        +exact-backlog-creation-transaction()
    }
    class create-work-item-github {
        <<Provider Skill>>
        +work-item-id
        +create-work-item(workItemDescription)
    }
    class create-work-item-gitlab {
        <<Provider Skill>>
        +work-item-id
        +create-work-item(workItemDescription)
    }
    class create-work-item-azure-devops {
        <<Provider Skill>>
        +work-item-id
        +create-work-item(workItemDescription)
    }
    class create-work-item-jira {
        <<Provider Skill>>
        +work-item-id
        +create-work-item(workItemDescription)
    }

    DevOrchestrator o..> CreateWorkItem : when an excluded issue needs a durable work item
    ProjectSpecificDirectives o..> create-work-item-file : when Persistence is file
    ProjectSpecificDirectives o..> create-work-item-github : when Persistence is github
    ProjectSpecificDirectives o..> create-work-item-gitlab : when Persistence is gitlab
    ProjectSpecificDirectives o..> create-work-item-azure-devops : when Persistence is azure-devops
    ProjectSpecificDirectives o..> create-work-item-jira : when Persistence is jira
    create-work-item-file ..|> CreateWorkItem
    create-work-item-github ..|> CreateWorkItem
    create-work-item-gitlab ..|> CreateWorkItem
    create-work-item-azure-devops ..|> CreateWorkItem
    create-work-item-jira ..|> CreateWorkItem
```

One effective project selects one creation provider. The Azure DevOps and Jira creation providers preserve the shared interface while returning their documented unsupported result.

### Scenario: Managing Work-Item Lifecycle

This scenario applies when an Agent or coordination skill inventories or changes durable provider lifecycle. The manage-*-work-items interface gives all consumers one vocabulary, while AGENTS.md selects the Persistence-specific implementation.

```mermaid
classDiagram
    direction LR

    namespace WorkItemManagementAgents["Work-item management Agents"] {
        class DevBacklogCoordinator {
            <<Agent>>
        }
        class DevBacklogSteward {
            <<Agent>>
        }
        class DevBacklogWatchdog {
            <<Agent>>
        }
        class DevOrchestrator {
            <<Agent>>
        }
    }

    class coordinate-codex-work-items {
        <<SKILL.md>>
        <<Cross-group>>
        +reconcile-active-execution()
        +coordinate-queue-and-dispatch()
    }
    class ManageWorkItem["manage-*-work-items"] {
        <<Skill interface>>
        +work-item-id
        +inventory-work-items(selection)
        +transition-work-item(workItem, transition)
        +reconcile-work-item-completion(workItem, deliveryEvidence)
        +recover-work-item(workItem, recoveryEvidence)
        +report-work-items(selection)
    }
    class ProjectSpecificDirectives["Project-specific directives"] {
        <<AGENTS.md>>
        <<routing>>
        +route manage-work-items => manage-*-work-items
    }
    class manage-file-work-items {
        <<Provider Skill>>
        +inventory-work-items(selection)
        +transition-work-item(workItem, transition)
    }
    class manage-github-work-items {
        <<Provider Skill>>
        +inventory-work-items(selection)
        +transition-work-item(workItem, transition)
    }
    class manage-gitlab-work-items {
        <<Provider Skill>>
        +inventory-work-items(selection)
        +transition-work-item(workItem, transition)
    }
    class manage-azure-devops-work-items {
        <<Provider Skill>>
        +inventory-work-items(selection)
        +transition-work-item(workItem, transition)
    }
    class manage-jira-work-items {
        <<Provider Skill>>
        +inventory-work-items(selection)
        +transition-work-item(workItem, transition)
    }

    DevBacklogCoordinator ..> ManageWorkItem : when a Persistence provider is selected
    DevBacklogSteward ..> ManageWorkItem : when a Persistence provider is selected
    DevBacklogWatchdog ..> ManageWorkItem : when a Persistence provider is selected
    DevOrchestrator ..> ManageWorkItem : when a Persistence provider is selected
    coordinate-codex-work-items ..> ManageWorkItem : when a Persistence provider is selected

    ProjectSpecificDirectives o..> manage-file-work-items : when Persistence is file
    ProjectSpecificDirectives o..> manage-github-work-items : when Persistence is github
    ProjectSpecificDirectives o..> manage-gitlab-work-items : when Persistence is gitlab
    ProjectSpecificDirectives o..> manage-azure-devops-work-items : when Persistence is azure-devops
    ProjectSpecificDirectives o..> manage-jira-work-items : when Persistence is jira

    manage-file-work-items ..|> ManageWorkItem
    manage-github-work-items ..|> ManageWorkItem
    manage-gitlab-work-items ..|> ManageWorkItem
    manage-azure-devops-work-items ..|> ManageWorkItem
    manage-jira-work-items ..|> ManageWorkItem
```

Persistence names the project selector, while manage-*-work-items names the provider-neutral management contract. Each provider supplies the complete set of lifecycle procedures, even when a provider reports that a requested operation is unsupported.

### Scenario: Recovering From A Backlog Blockage

This scenario applies after the user or Dev Backlog Watchdog declares a backlog blockage. Dev Backlog Coordinator temporarily changes secondary-thread dispatch mode only when concurrent dispatch is configured, then runs the provider-neutral sequential recovery procedure.

```mermaid
classDiagram
    direction LR

    class DevBacklogCoordinator {
        <<Agent>>
    }
    class DevBacklogWatchdog {
        <<Agent>>
    }
    class resolve-backlog-blockage {
        <<SKILL.md>>
        <<Agent Skill>>
    }
    class set-solo-mode {
        <<SKILL.md>>
        <<Cross-group>>
    }
    class set-multitask-mode {
        <<SKILL.md>>
        <<Cross-group>>
    }

    DevBacklogWatchdog o..> resolve-backlog-blockage : when a blockage criterion or active recovery applies
    DevBacklogCoordinator o..> set-solo-mode : when concurrent dispatch is configured and recovery begins
    DevBacklogCoordinator o..> resolve-backlog-blockage : when a backlog blockage is declared
    DevBacklogCoordinator o..> set-multitask-mode : when concurrent dispatch is configured and recovery ends
```

The Agent definition owns this sequence, so the three skills do not need direct references to one another. resolve-backlog-blockage remains usable when no secondary-thread dispatch mechanism is configured.

### Scenario: A File Provider Mutates Shared State

This scenario applies when the file-backed creation or management provider needs the project-selected resource-coordination policy before mutating shared backlog state. AGENTS.md loads agent-claim when the project selects it, and the provider skills depend on its procedures under that condition.

```mermaid
classDiagram
    direction LR

    class create-work-item-file {
        <<Provider Skill>>
    }
    class manage-file-work-items {
        <<Provider Skill>>
    }
    class ProjectSpecificDirectives["Project-specific directives"] {
        <<AGENTS.md>>
        <<routing>>
        +route resource coordination => agent-claim
    }
    class agent-claim {
        <<SKILL.md>>
        <<Cross-group>>
        +coordinate-shared-resource(resourceManifest)
        +acquire-claim(scope)
        +release-claim(claimId)
    }

    ProjectSpecificDirectives o..> agent-claim : when resource_coordination is agent-claim
    create-work-item-file ..> agent-claim : when resource coordination is selected
    manage-file-work-items ..> agent-claim : when resource coordination is selected
```

## Skill Responsibilities

Creation and management providers share public procedure names while retaining provider-specific identity, state, recovery, and mutation rules.

| Skill | Public procedures or identity | Responsibility |
| --- | --- | --- |
| resolve-backlog-blockage | Resolve Backlog Blockage | Resolves a declared blockage sequentially without owning dispatch-mode changes. |
| create-work-item | Work Item Identity; Inputs; Create Work Item; Result | Defines the provider-neutral creation contract consumed by Agents. |
| create-work-item-file | Create Work Item; Future Ideas Capture; Future Idea Promotion; Exact Backlog Creation Transaction | Creates file-backed work items and owns the file provider’s lightweight idea workflows. |
| create-work-item-github | Create Work Item | Creates and verifies one authoritative GitHub issue. |
| create-work-item-gitlab | Create Work Item | Creates and verifies one authoritative GitLab issue. |
| create-work-item-azure-devops | Create Work Item | Returns a truthful blocked result because Azure DevOps creation is not implemented. |
| create-work-item-jira | Create Work Item | Returns a truthful blocked result because Jira creation is not implemented. |
| manage-file-work-items | Inventory Work Items; Transition Work Item; Reconcile Work Item Completion; Recover Work Item; Report Work Items | Manages the file-backed lifecycle, dependencies, recovery, completion, reporting, and archival. |
| manage-github-work-items | Inventory Work Items; Transition Work Item; Reconcile Work Item Completion; Recover Work Item; Report Work Items | Maps the shared management procedures to GitHub issue state and evidence. |
| manage-gitlab-work-items | Inventory Work Items; Transition Work Item; Reconcile Work Item Completion; Recover Work Item; Report Work Items | Maps the shared management procedures to GitLab issue state and evidence. |
| manage-azure-devops-work-items | Inventory Work Items; Transition Work Item; Reconcile Work Item Completion; Recover Work Item; Report Work Items | Exposes the shared management interface while returning a truthful unsupported result. |
| manage-jira-work-items | Inventory Work Items; Transition Work Item; Reconcile Work Item Completion; Recover Work Item; Report Work Items | Exposes the shared management interface while returning a truthful unsupported result. |

## Authoritative Inputs

The provider relationships and procedure boundaries are grounded in these Agent and skill definitions.

- [Dev Backlog Steward](../../agents/roles/dev-activities/dev-backlog-steward.role.yaml)
- [Dev Backlog Coordinator](../../agents/roles/dev-activities/dev-backlog-coordinator.role.yaml)
- [Dev Backlog Watchdog](../../agents/roles/dev-activities/dev-backlog-watchdog.role.yaml)
- [Dev Orchestrator](../../agents/roles/dev-activities/dev-orchestrator.role.yaml)
- [Resolve Backlog Blockage](../../skills/resolve-backlog-blockage/SKILL.md)
- [Set Solo Mode](../../skills/set-solo-mode/SKILL.md)
- [Set Multitask Mode](../../skills/set-multitask-mode/SKILL.md)
- [Create Work Item](../../skills/create-work-item/SKILL.md)
- [Create File Work Item](../../skills/create-work-item-file/SKILL.md)
- [Create GitHub Work Item](../../skills/create-work-item-github/SKILL.md)
- [Create GitLab Work Item](../../skills/create-work-item-gitlab/SKILL.md)
- [Create Azure DevOps Work Item](../../skills/create-work-item-azure-devops/SKILL.md)
- [Create Jira Work Item](../../skills/create-work-item-jira/SKILL.md)
- [Manage File Work Items](../../skills/manage-file-work-items/SKILL.md)
- [Manage GitHub Work Items](../../skills/manage-github-work-items/SKILL.md)
- [Manage GitLab Work Items](../../skills/manage-gitlab-work-items/SKILL.md)
- [Manage Azure DevOps Work Items](../../skills/manage-azure-devops-work-items/SKILL.md)
- [Manage Jira Work Items](../../skills/manage-jira-work-items/SKILL.md)
- [Coordinate Codex Work Items](../../skills/coordinate-codex-work-items/SKILL.md)
- [Agent Claim](../../skills/agent-claim/SKILL.md)
