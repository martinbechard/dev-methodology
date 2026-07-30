# Concurrent Tasking Skill Group

## Scope

Concurrent Tasking encloses Resource Coordination and Feature Branch And Worktrees. codex-workitem-coordination coordinates the enclosing workflow while Persistence remains an independent injected provider.

The shared notation and recommendation boundary are defined in [Object-Oriented Skill Group Models](../object-oriented-skill-group-models.md).

## Current Design

```mermaid
classDiagram
    direction TB

    class DevBacklogCoordinator {
        <<Agent>>
    }

    class DevOrchestrator {
        <<Agent>>
    }

    class DevMergeCoordinator {
        <<Agent>>
    }

    class ConcurrentTasking {
        <<Skill group>>
    }

    class ResourceCoordination {
        <<Skill subgroup>>
    }

    class FeatureBranchAndWorktrees {
        <<Skill subgroup>>
    }

    namespace ConcurrentTaskingSkills {
        class codex-workitem-coordination {
            <<SKILL.md>>
            <<Agent Skill>>
            <<Peer Skill>>
            +resource-coordination()
            +queue-target-and-dispatch()
            +effective-commit-delivery-and-persistence-closure()
        }

        class agent-claim {
            <<SKILL.md>>
            <<Injectable Skill>>
            +claim-events()
            +timed-resource-claims()
            +release-cleanup()
        }

        class agent-claim-command {
            <<SKILL.md>>
            <<Injectable Skill>>
            +command-contract()
            +uncertain-command-outcome()
        }

        class agent-claim-mcp {
            <<SKILL.md>>
            <<Injectable Skill>>
            <<Unavailable implementation>>
            +mcp-operations()
            +uncertain-tool-outcome()
        }

        class agent-work-merge {
            <<SKILL.md>>
            <<Agent Skill>>
            <<Peer Skill>>
            +merge-workflow()
            +verification()
        }

        class complete-work-item-feature-branch {
            <<SKILL.md>>
            <<Injectable Skill>>
            <<Peer Skill>>
            +candidate-publication()
            +review-and-check-loop()
            +merge-and-completion-gate()
        }

        class create-pull-request {
            <<SKILL.md>>
            <<Peer Skill>>
            +workflow()
            +review-order()
        }
    }

    class ManageWorkItem["manage-*-work-items"] {
        <<AGENTS.md>>
        <<Cross-group>>
        +inventory-work-items(selection)
        +transition-work-item(workItem, transition)
        +reconcile-work-item-completion(workItem, deliveryEvidence)
    }

    class ResourceCoordinationBinding["resource-coordination"] {
        <<AGENTS.md>>
        +coordinate-shared-resource(resourceManifest)
    }

    class ClaimHelper["agent-claim-*"] {
        <<AGENTS.md>>
        +read-claim-status()
        +acquire-claim(scope)
        +extend-claim(scope)
        +release-claim()
    }

    class DeliverWorkItem["complete-work-item-*"] {
        <<AGENTS.md>>
        +deliver-work-item(acceptedCommit)
    }

    ConcurrentTasking *-- codex-workitem-coordination
    ConcurrentTasking *-- ResourceCoordination
    ConcurrentTasking *-- FeatureBranchAndWorktrees
    ResourceCoordination *-- agent-claim
    ResourceCoordination *-- agent-claim-command
    ResourceCoordination *-- agent-claim-mcp
    FeatureBranchAndWorktrees *-- agent-work-merge
    FeatureBranchAndWorktrees *-- complete-work-item-feature-branch
    FeatureBranchAndWorktrees *-- create-pull-request

    DevBacklogCoordinator o..> codex-workitem-coordination : when Codex tasks coordinate multiple work items
    DevOrchestrator o..> codex-workitem-coordination : when the task is a coordinated Codex work-item conversation
    DevOrchestrator --> DeliverWorkItem
    DevMergeCoordinator o--> agent-work-merge

    codex-workitem-coordination --> ManageWorkItem
    codex-workitem-coordination --> ResourceCoordinationBinding
    codex-workitem-coordination --> DeliverWorkItem
    codex-workitem-coordination o..> agent-claim : when agent-claim is loaded
    ResourceCoordinationBinding o--> agent-claim
    ResourceCoordinationBinding --> ClaimHelper
    ClaimHelper o--> agent-claim-command
    ClaimHelper o--> agent-claim-mcp
    DeliverWorkItem o--> complete-work-item-feature-branch

    agent-work-merge o--> agent-claim
    complete-work-item-feature-branch o--> agent-claim
    complete-work-item-feature-branch o..> create-pull-request : for GitHub pull-request publication
```

The solid-diamond lines express only containment. Concurrent Tasking contains the coordinating skill and both required subgroups; Resource Coordination and Feature Branch And Worktrees contain their current skills.

The regular arrows expose procedure-name dependencies. codex-workitem-coordination asks for provider management, resource coordination, and delivery through project-selected procedures. AGENTS.md makes those selections by exact skill name and separately selects the claim-helper transport.

The current coordination skill also says “when agent-claim is loaded,” so it is only partly decoupled from the selected Resource Coordination implementation. agent-work-merge and complete-work-item-feature-branch name agent-claim directly, and the feature-branch skill names create-pull-request for GitHub publication. The command helper is the supported current selection; agent-claim-mcp documents an unavailable implementation because it lacks verified deadline parity.

## Skill Recommendations

| Skill | Current source boundary | Recommendation | Reason |
| --- | --- | --- | --- |
| codex-workitem-coordination | Resource Coordination, Queue Target And Dispatch, and Effective Commit Delivery And Persistence Closure coordinate several procedures. | Rename the skill to coordinate-codex-work-items. | The verb-first name states the operation and separates it from a category named coordination. |
| agent-claim | Claim Events is a dispatch table; Claim Scope, Claim Conflicts, Timed Resource Claims, and Release Cleanup define related claim operations and rules. | Keep the skill name. Introduce Coordinate Shared Resource, Acquire Claim, Extend Claim, Extend Claim Deadline, Heartbeat Claim, Read Claim Status, and Release Claim as operation headings. | The headings give callers stable procedure names while Claim Events and the boundary rules remain reference information. |
| agent-claim-command | Command Contract and Command Arguments expose all command operations in one generic section. | Keep the skill name. Add Read Claim Status, Acquire Claim, Extend Claim, Extend Claim Deadline, Heartbeat Claim, Release Claim, Maintain Claim Journal, and Report Claim Contention headings. | These headings can match the MCP implementation exactly while command syntax remains provider-specific detail. |
| agent-claim-mcp | MCP Operations lists the same core operations under one table. | Keep the skill name. Add Read Claim Status, Acquire Claim, Extend Claim, Extend Claim Deadline, Heartbeat Claim, Release Claim, Maintain Claim Journal, and Report Claim Contention headings. | Matching helper headings create one transport-neutral helper interface and make missing MCP capabilities explicit. |
| agent-work-merge | Merge Workflow also supports selected commits, accepted file content, replay, and current-main reconciliation. | Rename the skill to integrate-agent-work. | Integration describes the complete responsibility more accurately than merge and remains appropriate for feature-branch and worktree composition. |
| complete-work-item-feature-branch | Candidate Publication, Review And Check Loop, and Merge And Completion Gate implement Commit delivery but do not mutate Persistence. | Rename the skill to deliver-work-item-feature-branch and introduce Deliver Work Item as its interface heading. | Complete can be confused with provider lifecycle completion. Deliver matches the caller’s procedure while the internal headings preserve feature-branch behavior. |
| create-pull-request | Workflow performs create or update behavior; Review Order and Draft And Ready State constrain it. | Keep the skill name. Rename Workflow to Create Or Update Pull Request. | The new heading identifies the procedure that complete-work-item-feature-branch invokes and covers both new and resumed publication. |

## Authoritative Inputs

- [Dev Backlog Coordinator](../../agents/roles/dev-activities/dev-backlog-coordinator.role.yaml)
- [Dev Orchestrator](../../agents/roles/dev-activities/dev-orchestrator.role.yaml)
- [Dev Merge Coordinator](../../agents/roles/dev-activities/dev-merge-coordinator.role.yaml)
- [Codex Work-Item Coordination](../../skills/codex-workitem-coordination/SKILL.md)
- [Agent Claim](../../skills/agent-claim/SKILL.md)
- [Agent Claim Command](../../skills/agent-claim-command/SKILL.md)
- [Agent Claim MCP](../../skills/agent-claim-mcp/SKILL.md)
- [Agent Work Merge](../../skills/agent-work-merge/SKILL.md)
- [Complete Work Item Feature Branch](../../skills/complete-work-item-feature-branch/SKILL.md)
- [Create Pull Request](../../skills/create-pull-request/SKILL.md)
- [Manage File Work Items](../../skills/manage-file-work-items/SKILL.md)
- [Manage GitHub Work Items](../../skills/manage-github-work-items/SKILL.md)
- [Manage GitLab Work Items](../../skills/manage-gitlab-work-items/SKILL.md)
