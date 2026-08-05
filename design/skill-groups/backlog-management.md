# Backlog Management Skill Group

## Scope

Backlog Management is independent of Resource Coordination and Commit delivery. AGENTS.md selects one creation skill and one management skill for the effective Persistence provider.

The applied-model conventions are defined in [Object-Oriented Skill Group Models](../object-oriented-skill-group-models.md#2-applied-model-legend).

## Design

The design separates blockage recovery from concurrent dispatch mode and gives every Persistence provider the same creation or management procedure vocabulary.

```mermaid
classDiagram
    direction TB

    class DevBacklogSteward {
        <<Agent>>
    }

    class DevBacklogCoordinator {
        <<Agent>>
    }

    class CreateWorkItem["create-*-work-item"] {
        <<AGENTS.md>>
        <<routing>>
        +create-work-item(workItemDescription)
    }

    class ManageWorkItem["manage-*-work-items"] {
        <<AGENTS.md>>
        <<routing>>
        +inventory-work-items(selection)
        +transition-work-item(workItem, transition)
        +reconcile-work-item-completion(workItem, deliveryEvidence)
    }

    namespace BacklogManagement {
        class resolve-backlog-blockage {
            <<SKILL.md>>
            <<Agent Skill>>
        }

        class create-file-work-item {
            <<SKILL.md>>
            <<Injectable Skill>>
            +create-work-item()
            +future-ideas-capture()
            +future-idea-promotion()
            +exact-backlog-creation-transaction()
        }

        class create-github-work-item {
            <<SKILL.md>>
            <<Injectable Skill>>
            +create-work-item()
        }

        class create-gitlab-work-item {
            <<SKILL.md>>
            <<Injectable Skill>>
            +create-work-item()
        }

        class create-azure-devops-work-item {
            <<SKILL.md>>
            <<Injectable Skill>>
            <<Unsupported placeholder>>
            +create-work-item()
        }

        class create-jira-work-item {
            <<SKILL.md>>
            <<Injectable Skill>>
            <<Unsupported placeholder>>
            +create-work-item()
        }

        class manage-file-work-items {
            <<SKILL.md>>
            <<Injectable Skill>>
            +inventory-work-items()
            +transition-work-item()
            +reconcile-work-item-completion()
            +recover-work-item()
            +report-work-items()
        }

        class manage-github-work-items {
            <<SKILL.md>>
            <<Injectable Skill>>
            +inventory-work-items()
            +transition-work-item()
            +reconcile-work-item-completion()
            +recover-work-item()
            +report-work-items()
        }

        class manage-gitlab-work-items {
            <<SKILL.md>>
            <<Injectable Skill>>
            +inventory-work-items()
            +transition-work-item()
            +reconcile-work-item-completion()
            +recover-work-item()
            +report-work-items()
        }

        class manage-azure-devops-work-items {
            <<SKILL.md>>
            <<Injectable Skill>>
            <<Unsupported placeholder>>
            +inventory-work-items()
            +transition-work-item()
            +reconcile-work-item-completion()
            +recover-work-item()
            +report-work-items()
        }

        class manage-jira-work-items {
            <<SKILL.md>>
            <<Injectable Skill>>
            <<Unsupported placeholder>>
            +inventory-work-items()
            +transition-work-item()
            +reconcile-work-item-completion()
            +recover-work-item()
            +report-work-items()
        }
    }

    class set-solo-mode {
        <<SKILL.md>>
        <<Cross-group>>
    }

    class set-multitask-mode {
        <<SKILL.md>>
        <<Cross-group>>
    }

    class ResourceCoordination["resource-coordination"] {
        <<AGENTS.md>>
        <<routing>>
        <<Cross-group>>
        +coordinate-shared-resource(resourceManifest)
    }

    class agent-claim {
        <<SKILL.md>>
        <<Cross-group>>
    }

    DevBacklogSteward --> CreateWorkItem
    DevBacklogSteward --> ManageWorkItem
    DevBacklogCoordinator o..> resolve-backlog-blockage : when a backlog blockage requires sequential recovery
    DevBacklogCoordinator o..> set-solo-mode : when concurrent tasking is enabled and sequential blockage recovery begins
    DevBacklogCoordinator o..> set-multitask-mode : when concurrent tasking is enabled and sequential recovery ends

    CreateWorkItem o--> create-file-work-item
    CreateWorkItem o--> create-github-work-item
    CreateWorkItem o--> create-gitlab-work-item
    CreateWorkItem o--> create-azure-devops-work-item
    CreateWorkItem o--> create-jira-work-item

    ManageWorkItem o--> manage-file-work-items
    ManageWorkItem o--> manage-github-work-items
    ManageWorkItem o--> manage-gitlab-work-items
    ManageWorkItem o--> manage-azure-devops-work-items
    ManageWorkItem o--> manage-jira-work-items

    create-file-work-item ..> ResourceCoordination : when resource coordination is enabled
    create-file-work-item o..> agent-claim : when classifying User Action Required and agent-claim is loaded
    manage-file-work-items ..> ResourceCoordination : when resource coordination is enabled
```

The group keeps blockage analysis and sequential recovery in Backlog Management. set-solo-mode and set-multitask-mode belong to Concurrent Tasking because they disable or enable dispatch to secondary threads.

Dev Backlog Coordinator loads each of the three skills by name when its matching condition occurs. The sibling skills do not name one another, so the Agent definition remains the visible place where the entry, recovery, and exit sequence is assembled.

When Concurrent Tasking is not configured, no secondary-thread dispatch exists to change. resolve-backlog-blockage therefore remains usable without either dispatch-mode skill.

## Skill Responsibilities

Creation and management providers share public procedure names while retaining provider-specific identity, state, recovery, and mutation rules.

| Skill | Public procedures or identity | Responsibility |
| --- | --- | --- |
| resolve-backlog-blockage | Resolve Backlog Blockage | Resolves a declared blockage sequentially without owning dispatch-mode changes. |
| create-file-work-item | Create Work Item; Future Ideas Capture; Future Idea Promotion; Exact Backlog Creation Transaction | Creates file-backed work items and owns the file provider’s lightweight idea workflows. |
| create-github-work-item | Create Work Item | Creates and verifies one authoritative GitHub issue. |
| create-gitlab-work-item | Create Work Item | Creates and verifies one authoritative GitLab issue. |
| create-azure-devops-work-item | Create Work Item | Returns a truthful blocked result because Azure DevOps creation is not implemented. |
| create-jira-work-item | Create Work Item | Returns a truthful blocked result because Jira creation is not implemented. |
| manage-file-work-items | Inventory Work Items; Transition Work Item; Reconcile Work Item Completion; Recover Work Item; Report Work Items | Manages the file-backed lifecycle, dependencies, recovery, completion, reporting, and archival. |
| manage-github-work-items | Inventory Work Items; Transition Work Item; Reconcile Work Item Completion; Recover Work Item; Report Work Items | Maps the shared management procedures to GitHub issue state and evidence. |
| manage-gitlab-work-items | Inventory Work Items; Transition Work Item; Reconcile Work Item Completion; Recover Work Item; Report Work Items | Maps the shared management procedures to GitLab issue state and evidence. |
| manage-azure-devops-work-items | Inventory Work Items; Transition Work Item; Reconcile Work Item Completion; Recover Work Item; Report Work Items | Exposes the shared management interface while returning a truthful unsupported result. |
| manage-jira-work-items | Inventory Work Items; Transition Work Item; Reconcile Work Item Completion; Recover Work Item; Report Work Items | Exposes the shared management interface while returning a truthful unsupported result. |

## Authoritative Inputs

The provider relationships and procedure boundaries are grounded in these Agent and skill definitions.

- [Dev Backlog Steward](../../agents/roles/dev-activities/dev-backlog-steward.role.yaml)
- [Dev Backlog Coordinator](../../agents/roles/dev-activities/dev-backlog-coordinator.role.yaml)
- [Resolve Backlog Blockage](../../skills/resolve-backlog-blockage/SKILL.md)
- [Set Solo Mode](../../skills/set-solo-mode/SKILL.md)
- [Set Multitask Mode](../../skills/set-multitask-mode/SKILL.md)
- [Create File Work Item](../../skills/create-file-work-item/SKILL.md)
- [Create GitHub Work Item](../../skills/create-github-work-item/SKILL.md)
- [Create GitLab Work Item](../../skills/create-gitlab-work-item/SKILL.md)
- [Create Azure DevOps Work Item](../../skills/create-azure-devops-work-item/SKILL.md)
- [Create Jira Work Item](../../skills/create-jira-work-item/SKILL.md)
- [Manage File Work Items](../../skills/manage-file-work-items/SKILL.md)
- [Manage GitHub Work Items](../../skills/manage-github-work-items/SKILL.md)
- [Manage GitLab Work Items](../../skills/manage-gitlab-work-items/SKILL.md)
- [Manage Azure DevOps Work Items](../../skills/manage-azure-devops-work-items/SKILL.md)
- [Manage Jira Work Items](../../skills/manage-jira-work-items/SKILL.md)
- [Agent Claim](../../skills/agent-claim/SKILL.md)
