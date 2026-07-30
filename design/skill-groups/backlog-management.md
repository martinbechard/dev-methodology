# Backlog Management Skill Group

## Scope

Backlog Management is independent of Resource Coordination and Commit delivery. AGENTS.md selects one creation skill and one management skill for the effective Persistence provider.

The shared notation and recommendation boundary are defined in [Object-Oriented Skill Group Models](../object-oriented-skill-group-models.md).

## Current Design

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
        <<abstract>>
        +create-work-item(workItemDescription)
    }

    class ManageWorkItem["manage-*-work-items"] {
        <<AGENTS.md>>
        <<abstract>>
        +inventory-work-items(selection)
        +transition-work-item(workItem, transition)
        +reconcile-work-item-completion(workItem, deliveryEvidence)
    }

    namespace BacklogManagement {
        class backlog-crisis-mode {
            <<SKILL.md>>
            <<Agent Skill>>
        }

        class create-file-work-item {
            <<SKILL.md>>
            <<Injectable Skill>>
            +exact-backlog-creation-transaction()
        }

        class create-github-work-item {
            <<SKILL.md>>
            <<Injectable Skill>>
            +creation()
        }

        class create-gitlab-work-item {
            <<SKILL.md>>
            <<Injectable Skill>>
            +workflow()
        }

        class create-azure-devops-work-item {
            <<SKILL.md>>
            <<Injectable Skill>>
            <<Unsupported placeholder>>
            +required-result()
        }

        class create-jira-work-item {
            <<SKILL.md>>
            <<Injectable Skill>>
            <<Unsupported placeholder>>
            +required-result()
        }

        class manage-file-work-items {
            <<SKILL.md>>
            <<Injectable Skill>>
            +inventory-workflow()
            +dispatch-workflow()
            +completion-and-archive-workflow()
        }

        class manage-github-work-items {
            <<SKILL.md>>
            <<Injectable Skill>>
            +inventory-and-selection()
            +lifecycle-management()
            +dependencies-and-recovery()
        }

        class manage-gitlab-work-items {
            <<SKILL.md>>
            <<Injectable Skill>>
            +operations()
            +completion-and-reconciliation()
        }

        class manage-azure-devops-work-items {
            <<SKILL.md>>
            <<Injectable Skill>>
            <<Unsupported placeholder>>
            +required-result()
        }

        class manage-jira-work-items {
            <<SKILL.md>>
            <<Injectable Skill>>
            <<Unsupported placeholder>>
            +required-result()
        }
    }

    class ResourceCoordination["resource-coordination"] {
        <<AGENTS.md>>
        <<Cross-group>>
        +coordinate-shared-resource(resourceManifest)
    }

    class agent-claim {
        <<SKILL.md>>
        <<Cross-group>>
    }

    DevBacklogSteward --> CreateWorkItem
    DevBacklogSteward --> ManageWorkItem
    DevBacklogCoordinator o..> backlog-crisis-mode : when a backlog crisis is declared

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

The AGENTS.md nodes show the procedures that callers need. The concrete nodes show the current headings that contain those procedures. The mismatched names are intentional evidence: for example, create-gitlab-work-item currently exposes only a generic Workflow heading rather than a Create Work Item heading.

Each open-diamond fan-out lists available Persistence implementations. One effective project configuration selects one creation skill and one management skill. Azure DevOps and Jira remain selectable zero-mutation placeholders.

create-file-work-item mostly requests the loaded resource-coordination procedure without selecting its implementation. Its User Action Required classification currently names agent-claim, so the diagram also retains that stronger exact-name dependency.

Crisis mode continues to use the selected Persistence provider while disabling claims and delegated delivery. It therefore remains in Backlog Management without a Resource Coordination relationship.

## Skill Recommendations

| Skill | Current source boundary | Recommendation | Reason |
| --- | --- | --- | --- |
| backlog-crisis-mode | Declaration, Execution, Watchdog Behavior, Exit, and Result define one crisis-resolution procedure. | Rename the skill to resolve-backlog-crisis. | The verb-first name states what the conditional Agent Skill does instead of naming only the mode it enters. |
| create-file-work-item | Exact Backlog Creation Transaction performs the write, while Future Ideas Capture and Future Idea Promotion are separate operations. | Keep the skill name. Introduce Create Work Item, Capture Future Idea, and Promote Future Idea headings; keep Exact Backlog Creation Transaction as their internal transaction procedure. | Create Work Item can match the provider interface without hiding the two file-only procedures inside the same package. |
| create-github-work-item | Creation contains the provider-specific create procedure. | Keep the skill name. Rename Creation to Create Work Item. | The shared heading can match the AGENTS.md procedure used for every creation provider. |
| create-gitlab-work-item | Workflow contains duplicate detection, creation, readback, and partial-mutation handling. | Keep the skill name. Rename Workflow to Create Work Item. | Workflow is too generic to form a stable interface; Create Work Item states the operation. |
| create-azure-devops-work-item | Required Result defines the BLOCKED implementation for creation. | Keep the skill name. Add Create Work Item as the interface heading and place Required Result beneath it. | A blocking implementation still implements the same procedure and should be discoverable through the same heading. |
| create-jira-work-item | Required Result defines the BLOCKED implementation for creation. | Keep the skill name. Add Create Work Item as the interface heading and place Required Result beneath it. | The placeholder can remain truthful while exposing the same procedure name as supported providers. |
| manage-file-work-items | Inventory Workflow, Dispatch Workflow, Completion And Archive Workflow, Recovery Workflow, and Reporting are distinct procedures. | Keep the skill name. Use Inventory Work Items, Transition Work Item, Reconcile Work Item Completion, Recover Work Item, and Report Work Items as operation headings. | The shared procedure names expose provider-neutral operations while the file-specific rules remain inside each section. |
| manage-github-work-items | Inventory And Selection, Lifecycle Management, Dependencies And Recovery, and Result contain the management operations. | Keep the skill name. Use Inventory Work Items, Transition Work Item, Reconcile Work Item Completion, Recover Work Item, and Report Work Items as operation headings. | Matching headings make the GitHub package substitutable without erasing its native issue behavior. |
| manage-gitlab-work-items | Authority And Lookup, Operations, Completion And Reconciliation, and Result contain the management operations. | Keep the skill name. Use Inventory Work Items, Transition Work Item, Reconcile Work Item Completion, Recover Work Item, and Report Work Items as operation headings. | Operations is too broad to identify which management procedure a caller needs. |
| manage-azure-devops-work-items | Required Result handles every management request with one BLOCKED result. | Keep the skill name. Add Inventory Work Items, Transition Work Item, Reconcile Work Item Completion, Recover Work Item, and Report Work Items headings that route to Required Result. | The placeholder should expose the same callable vocabulary as a future supported implementation without pretending that it succeeds. |
| manage-jira-work-items | Required Result handles every management request with one BLOCKED result. | Keep the skill name. Add Inventory Work Items, Transition Work Item, Reconcile Work Item Completion, Recover Work Item, and Report Work Items headings that route to Required Result. | Consistent headings let AGENTS.md select the Jira placeholder through the same management interfaces. |

## Authoritative Inputs

- [Dev Backlog Steward](../../agents/roles/dev-activities/dev-backlog-steward.role.yaml)
- [Dev Backlog Coordinator](../../agents/roles/dev-activities/dev-backlog-coordinator.role.yaml)
- [Backlog Crisis Mode](../../skills/backlog-crisis-mode/SKILL.md)
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
