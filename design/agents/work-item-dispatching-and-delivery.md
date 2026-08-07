# Work Item Dispatching And Delivery

## Scope

Work Item Dispatching And Delivery is an agent-oriented design topic. It explains how Backlog Management Agents manage a sustained stream of work items and how Dev Delivery Agents deliver one accepted work item. The view brings together the Work Item Dispatching, Resource Coordination, Feature Branch And Worktrees, Main Branch Delivery, Backlog Management, Baseline Development, and Review And Verification Skill Groups without inventing one larger Skill Group around them.

Work Item Dispatching contains coordinate-work-items, coordinate-codex-tasks, set-solo-mode, and set-multitask-mode. Resource Coordination and Feature Branch And Worktrees remain independent Skill Groups rather than nested members of Work Item Dispatching. Persistence remains an independently injected provider.

The applied-model conventions are defined in [Object-Oriented Skill Group Models](../object-oriented-skill-group-models.md#2-applied-model-legend).

## Design

The design starts with the Task Management Agent hierarchy and then shows the relationships between whole Agent Groups and the independent Skill Groups they use. Two expanded diagrams identify the exact Agents and skills inside those Agent Group views. Four scenario diagrams then explain provider routing and other relationships that need more detail.

A solid dependency is fixed by the referencing definition. A dotted dependency applies only under the condition written on the arrow. Project-selected skill loading originates at AGENTS.md. Agent- or skill-owned loading originates at the Agent or skill that makes that decision. Realization arrows show that a provider implements an interface; they do not load a file.

When several provider skills expose the same public procedures, the scenario uses an exact Interface Skill when one exists. The interface gives consumers one shared contract, while AGENTS.md selects the provider skill for the project.

### Agent Hierarchy

The Agent hierarchy separates task management by unit of responsibility. Backlog Management Agents manage a sustained queue and its provider-wide state. Dev Delivery Agents implement, review, verify, integrate, and deliver one accepted work item. Solid arrows identify fixed Agent dependencies, while dotted arrows identify conditional delegation.

```mermaid
classDiagram
    direction TB

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

    namespace DevDeliveryAgents["Dev Delivery Agents"] {
        class DevOrchestrator {
            <<Agent>>
        }
        class DevCoder {
            <<Agent>>
        }
        class DevCodeReviewer {
            <<Agent>>
        }
        class DevVerifier {
            <<Agent>>
        }
        class DevMergeCoordinator {
            <<Agent>>
        }
    }

    DevBacklogCoordinator --> DevOrchestrator
    DevBacklogCoordinator ..> DevBacklogSteward : when provider-wide maintenance is needed
    DevBacklogCoordinator ..> DevBacklogWatchdog : when sustained queue observation is needed
    DevOrchestrator --> DevCoder
    DevOrchestrator --> DevCodeReviewer
    DevOrchestrator --> DevVerifier
    DevOrchestrator ..> DevMergeCoordinator : when multiple contributions need integration
```

### Agent Group And Skill Group Dependencies

The high-level dependency view contains only Agent Groups and independent Skill Groups. An Agent Group arrow summarizes one or more dependencies owned by Agents in that group; it does not mean that every Agent loads every skill in the target group. A solid arrow means at least one member has a fixed dependency. A dotted arrow summarizes a conditional dependency. A Skill Group arrow means that at least one skill in the source group depends on a skill in the target group.

```mermaid
classDiagram
    direction LR

    class BacklogManagementAgents["Backlog Management Agents"] {
        <<Agent Group>>
    }

    class DevDeliveryAgents["Dev Delivery Agents"] {
        <<Agent Group>>
    }

    class BaselineDevelopment["Baseline Development"] {
        <<Skill Group>>
    }
    class BacklogManagement["Backlog Management"] {
        <<Skill Group>>
    }
    class WorkItemDispatching["Work Item Dispatching"] {
        <<Skill Group>>
    }
    class ResourceCoordination["Resource Coordination"] {
        <<Skill Group>>
    }
    class FeatureBranchAndWorktrees["Feature Branch And Worktrees"] {
        <<Skill Group>>
    }
    class MainBranchDelivery["Main Branch Delivery"] {
        <<Skill Group>>
    }
    class ReviewAndVerification["Review And Verification"] {
        <<Skill Group>>
    }

    BacklogManagementAgents --> BaselineDevelopment
    BacklogManagementAgents --> BacklogManagement
    BacklogManagementAgents --> WorkItemDispatching
    DevDeliveryAgents --> BaselineDevelopment
    DevDeliveryAgents --> BacklogManagement
    DevDeliveryAgents ..> WorkItemDispatching : when multiple agents work concurrently
    DevDeliveryAgents --> MainBranchDelivery
    DevDeliveryAgents --> FeatureBranchAndWorktrees
    DevDeliveryAgents --> ReviewAndVerification

    WorkItemDispatching --> ResourceCoordination
    MainBranchDelivery ..> FeatureBranchAndWorktrees : when implementation uses a separate branch or worktree
```

### Backlog Management Agents And Skills

Backlog Management Agents coordinate a sustained queue, maintain provider-wide records, and observe whether the queue needs attention. The diagram expands their exact role-declared skill dependencies. Solid open-diamond arrows are Core Agent Skills. Dotted open-diamond arrows are Optional Agent Skills and state their loading conditions.

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

    namespace BacklogManagementSkills["Backlog Management skills"] {
        class ManageWorkItems["manage-work-items"] {
            <<Interface Skill>>
        }
        class manage-future-ideas {
            <<SKILL.md>>
        }
        class resolve-backlog-blockage {
            <<SKILL.md>>
        }
    }

    namespace WorkItemDispatchingSkills["Work Item Dispatching skills"] {
        class coordinate-work-items {
            <<SKILL.md>>
        }
        class coordinate-codex-tasks {
            <<SKILL.md>>
        }
        class set-solo-mode {
            <<SKILL.md>>
        }
        class set-multitask-mode {
            <<SKILL.md>>
        }
    }

    namespace BaselineDevelopmentSkills["Baseline Development skills"] {
        class structured-explanation {
            <<SKILL.md>>
        }
    }

    DevBacklogCoordinator o--> ManageWorkItems
    DevBacklogCoordinator o--> structured-explanation
    DevBacklogCoordinator o..> coordinate-work-items : when coordinating a sustained queue
    DevBacklogCoordinator o..> coordinate-codex-tasks : when executions use Codex tasks
    DevBacklogCoordinator o..> resolve-backlog-blockage : during declared blockage recovery
    DevBacklogCoordinator o..> set-solo-mode : when secondary dispatch must stop
    DevBacklogCoordinator o..> set-multitask-mode : when secondary dispatch may resume

    DevBacklogSteward o--> ManageWorkItems
    DevBacklogSteward o--> structured-explanation
    DevBacklogSteward o..> coordinate-work-items : when maintenance touches coordinated state
    DevBacklogSteward o..> coordinate-codex-tasks : when inspecting Codex task evidence
    DevBacklogSteward o..> manage-future-ideas : when Future Ideas work is requested

    DevBacklogWatchdog o--> ManageWorkItems
    DevBacklogWatchdog o--> coordinate-work-items
    DevBacklogWatchdog o..> coordinate-codex-tasks : when observing Codex tasks
    DevBacklogWatchdog o..> resolve-backlog-blockage : when blockage criteria apply
```

### Dev Delivery Agents And Skills

Dev Delivery Agents implement, review, verify, integrate, and deliver one accepted work item. This diagram expands their exact role-declared skill dependencies while keeping provider implementations behind their Interface Skills.

```mermaid
classDiagram
    direction LR

    namespace DevDeliveryAgents["Dev Delivery Agents"] {
        class DevOrchestrator {
            <<Agent>>
        }
        class DevCoder {
            <<Agent>>
        }
        class DevCodeReviewer {
            <<Agent>>
        }
        class DevVerifier {
            <<Agent>>
        }
        class DevMergeCoordinator {
            <<Agent>>
        }
    }

    namespace BacklogManagementSkills["Backlog Management skills"] {
        class CreateWorkItem["create-work-item"] {
            <<Interface Skill>>
        }
        class ManageWorkItems["manage-work-items"] {
            <<Interface Skill>>
        }
    }

    namespace WorkItemDispatchingSkills["Work Item Dispatching skills"] {
        class coordinate-work-items {
            <<SKILL.md>>
        }
        class coordinate-codex-tasks {
            <<SKILL.md>>
        }
    }

    namespace MainBranchDeliverySkills["Main Branch Delivery skills"] {
        class DeliverWorkItem["deliver-work-item"] {
            <<Interface Skill>>
        }
    }

    namespace BaselineDevelopmentSkills["Baseline Development skills"] {
        class careful-coding {
            <<SKILL.md>>
        }
        class code-comments {
            <<SKILL.md>>
        }
        class test-driven-development {
            <<SKILL.md>>
        }
        class code-discovery {
            <<SKILL.md>>
        }
        class explain-code-fix {
            <<SKILL.md>>
        }
        class structured-design {
            <<SKILL.md>>
        }
        class structured-explanation {
            <<SKILL.md>>
        }
        class review-structured-artifact {
            <<SKILL.md>>
        }
    }

    namespace ReviewAndVerificationSkills["Review And Verification skills"] {
        class review-code-with-evidence {
            <<SKILL.md>>
        }
        class test-strategy {
            <<SKILL.md>>
        }
        class verify-end-to-end-workflow {
            <<SKILL.md>>
        }
        class analyze-root-cause {
            <<SKILL.md>>
        }
        class collect-runtime-evidence {
            <<SKILL.md>>
        }
        class trace-code-execution {
            <<SKILL.md>>
        }
        class review-prompt-contracts {
            <<SKILL.md>>
        }
    }

    namespace FeatureBranchAndWorktreeSkills["Feature Branch And Worktrees skills"] {
        class integrate-agent-work {
            <<SKILL.md>>
        }
    }

    DevOrchestrator o--> ManageWorkItems
    DevOrchestrator o--> DeliverWorkItem
    DevOrchestrator o--> structured-design
    DevOrchestrator o--> structured-explanation
    DevOrchestrator o..> CreateWorkItem : when an excluded issue needs a work item
    DevOrchestrator o..> coordinate-work-items : when multiple agents work concurrently
    DevOrchestrator o..> coordinate-codex-tasks : when the execution uses a Codex task

    DevCoder o--> careful-coding
    DevCoder o--> code-comments
    DevCoder o--> code-discovery
    DevCoder o--> explain-code-fix
    DevCoder o..> test-driven-development : when executable tests guide implementation

    DevCodeReviewer o--> review-code-with-evidence
    DevCodeReviewer o--> review-structured-artifact
    DevCodeReviewer o--> careful-coding
    DevCodeReviewer o--> code-comments

    DevVerifier o--> test-strategy
    DevVerifier o--> review-structured-artifact
    DevVerifier o--> structured-explanation
    DevVerifier o..> verify-end-to-end-workflow : when an end-to-end workflow must be proven
    DevVerifier o..> analyze-root-cause : when a check fails
    DevVerifier o..> collect-runtime-evidence : when static evidence is insufficient
    DevVerifier o..> trace-code-execution : when an outcome must be traced to source
    DevVerifier o..> review-prompt-contracts : when verification uses a model-facing contract

    DevMergeCoordinator o--> integrate-agent-work
    DevMergeCoordinator o--> review-structured-artifact
    DevMergeCoordinator o--> explain-code-fix
```

The role schema supplies effective-communication and ste-technical-writing to every conceptual Agent. PROJECT.yaml records organise-project-files once in shared_agent_skills, and generated AGENTS.md tells every Agent to load it when the Agent must choose or audit the location of a project file or directory. The diagrams omit that project-wide route instead of repeating it as role-specific arrows.

### Scenario: Creating A Work Item For An Excluded Issue

This scenario applies when Dev Orchestrator deliberately excludes a confirmed issue from the current delivery and must create a durable work item. The create-work-item Interface Skill defines the shared contract. The create-work-item-* family contains the Persistence-selected providers.

```mermaid
classDiagram
    direction TB

    class DevOrchestrator {
        <<Agent>>
    }

    class CreateWorkItem["create-work-item"] {
        <<Interface Skill>>
        +work-item-id
        +create-work-item(workItemDescription)
    }

    class project-specific-directives["Project-specific directives"] {
        <<AGENTS.md>>
        <<routing>>
        +route create-work-item => create-work-item-*
    }

    class create-work-item-file {
        <<Provider Skill>>
        <<Cross-group>>
        +work-item-id
        +create-work-item(workItemDescription)
    }

    class create-work-item-github {
        <<Provider Skill>>
        <<Cross-group>>
        +work-item-id
        +create-work-item(workItemDescription)
    }

    class create-work-item-gitlab {
        <<Provider Skill>>
        <<Cross-group>>
        +work-item-id
        +create-work-item(workItemDescription)
    }

    class create-work-item-azure-devops {
        <<Provider Skill>>
        <<Cross-group>>
        +work-item-id
        +create-work-item(workItemDescription)
    }

    class create-work-item-jira {
        <<Provider Skill>>
        <<Cross-group>>
        +work-item-id
        +create-work-item(workItemDescription)
    }

    DevOrchestrator o..> CreateWorkItem : when a confirmed issue is excluded from current delivery
    project-specific-directives o..> create-work-item-file : when Persistence is file
    project-specific-directives o..> create-work-item-github : when Persistence is github
    project-specific-directives o..> create-work-item-gitlab : when Persistence is gitlab
    project-specific-directives o..> create-work-item-azure-devops : when Persistence is azure-devops
    project-specific-directives o..> create-work-item-jira : when Persistence is jira
    create-work-item-file ..|> CreateWorkItem
    create-work-item-github ..|> CreateWorkItem
    create-work-item-gitlab ..|> CreateWorkItem
    create-work-item-azure-devops ..|> CreateWorkItem
    create-work-item-jira ..|> CreateWorkItem
```

AGENTS.md selects exactly one creation provider from the project Persistence setting. Azure
DevOps and Jira use placeholder provider skills that return their documented unsupported result.
An explicit Future Ideas request conditionally selects manage-future-ideas instead of adding an
operation to the creation or lifecycle interfaces. create-work-item-file and manage-future-ideas
use commit-file-provider-transaction only when their file creation reaches the commit boundary.

### Scenario: Managing Provider Lifecycle

This scenario applies when an Agent inventories or changes durable provider lifecycle. The manage-work-items Interface Skill publishes the shared management contract. Persistence selects one manage-work-items-* provider.

```mermaid
classDiagram
    direction LR

    namespace WorkItemManagementAgents["Work-item management Agents"] {
        class DevBacklogCoordinator {
            <<Agent>>
        }

        class DevOrchestrator {
            <<Agent>>
        }

        class DevBacklogSteward {
            <<Agent>>
        }

        class DevBacklogWatchdog {
            <<Agent>>
        }
    }

    class coordinate-work-items {
        <<SKILL.md>>
        <<Agent Skill>>
        +reconcile-active-execution()
        +coordinate-queue-and-dispatch()
        +coordinate-delivery-and-closure()
        +review-work-item-queue()
    }

    class project-specific-directives["Project-specific directives"] {
        <<AGENTS.md>>
        <<routing>>
        +route manage-work-items => manage-work-items-*
    }

    class ManageWorkItem["manage-work-items"] {
        <<Interface Skill>>
        +work-item-id
        +inventory-work-items(selection)
        +transition-work-item(workItem, transition)
        +reconcile-work-item-completion(workItem, deliveryEvidence)
        +recover-work-item(workItem, recoveryEvidence)
        +report-work-items(selection)
    }

    class manage-work-items-file {
        <<Provider Skill>>
        <<Cross-group>>
        +inventory-work-items(selection)
        +transition-work-item(workItem, transition)
    }

    class manage-work-items-github {
        <<Provider Skill>>
        <<Cross-group>>
        +inventory-work-items(selection)
        +transition-work-item(workItem, transition)
    }

    class manage-work-items-gitlab {
        <<Provider Skill>>
        <<Cross-group>>
        +inventory-work-items(selection)
        +transition-work-item(workItem, transition)
    }

    class manage-work-items-azure-devops {
        <<Provider Skill>>
        <<Cross-group>>
        +inventory-work-items(selection)
        +transition-work-item(workItem, transition)
    }

    class manage-work-items-jira {
        <<Provider Skill>>
        <<Cross-group>>
        +inventory-work-items(selection)
        +transition-work-item(workItem, transition)
    }

    DevBacklogCoordinator o--> ManageWorkItem
    DevOrchestrator o--> ManageWorkItem
    DevBacklogSteward o--> ManageWorkItem
    DevBacklogWatchdog o--> ManageWorkItem
    coordinate-work-items ..> ManageWorkItem : when a Persistence provider is selected
    project-specific-directives o..> manage-work-items-file : when Persistence is file
    project-specific-directives o..> manage-work-items-github : when Persistence is github
    project-specific-directives o..> manage-work-items-gitlab : when Persistence is gitlab
    project-specific-directives o..> manage-work-items-azure-devops : when Persistence is azure-devops
    project-specific-directives o..> manage-work-items-jira : when Persistence is jira
    manage-work-items-file ..|> ManageWorkItem
    manage-work-items-github ..|> ManageWorkItem
    manage-work-items-gitlab ..|> ManageWorkItem
    manage-work-items-azure-devops ..|> ManageWorkItem
    manage-work-items-jira ..|> ManageWorkItem
```

manage-work-items names the shared management contract, and manage-work-items-* names its
provider family. Persistence selects one provider. coordinate-work-items uses the contract
across queue dispatch, active-execution reconciliation, delivery, closure, and periodic review.

### Scenario: A Project Enables Concurrent Agents

This scenario starts with the project goal: enable multiple agents to work concurrently. Concurrent work requires resource coordination, so coordinate-work-items always loads resource-claim. resource-claim always loads the exact resource-claim-helper Interface Skill, which defines the common operation, input, result, and uncertain-outcome contract. Project-specific directives select one verified resource-claim-helper-* Provider Skill. The selected provider remains outside the default context until resource-claim performs a claim operation. resource-claim-helper-command invokes a local command-line helper, while resource-claim-helper-mcp calls tools through the MCP protocol.

```mermaid
classDiagram
    direction LR

    class coordinate-work-items {
        <<SKILL.md>>
        <<Agent Skill>>
        +resource-coordination()
    }

    class integrate-agent-work {
        <<SKILL.md>>
        <<Agent Skill>>
        +merge-workflow()
        +verification()
    }

    class project-specific-directives["Project-specific directives"] {
        <<AGENTS.md>>
        <<routing>>
        +route resource-claim-helper => resource-claim-helper-*
    }

    class resource-claim {
        <<SKILL.md>>
        +coordinate-shared-resource(resourceManifest)
        +acquire-claim(scope)
        +release-claim(claimId)
    }

    class ClaimHelper["resource-claim-helper"] {
        <<Interface Skill>>
        +read-claim-status()
        +acquire-claim(scope)
        +extend-claim(scope)
        +extend-claim-deadline(claimId)
        +heartbeat-claim(claimId)
        +release-claim(claimId)
        +reset-claim-registry()
        +maintain-claim-journal()
        +report-claim-contention()
    }

    class resource-claim-helper-command {
        <<Provider Skill>>
        +read-claim-status()
        +acquire-claim(scope)
        +extend-claim(scope)
        +extend-claim-deadline(claimId)
        +heartbeat-claim(claimId)
        +release-claim(claimId)
        +reset-claim-registry()
        +maintain-claim-journal()
        +report-claim-contention()
    }

    class resource-claim-helper-mcp {
        <<Provider Skill>>
        +read-claim-status()
        +acquire-claim(scope)
        +extend-claim(scope)
        +extend-claim-deadline(claimId)
        +heartbeat-claim(claimId)
        +release-claim(claimId)
        +reset-claim-registry()
        +maintain-claim-journal()
        +report-claim-contention()
    }

    project-specific-directives o..> resource-claim-helper-command : when claim operations use the command-line helper
    project-specific-directives o..> resource-claim-helper-mcp : when claim operations use the verified MCP helper
    coordinate-work-items o--> resource-claim
    integrate-agent-work o--> resource-claim
    resource-claim o--> ClaimHelper
    resource-claim-helper-command ..|> ClaimHelper
    resource-claim-helper-mcp ..|> ClaimHelper
```

Enabling concurrent agents loads coordinate-work-items together with its fixed resource-claim dependency. integrate-agent-work uses the same policy when concurrent contributions reach shared integration. resource-claim then loads resource-claim-helper as a fixed exact-name Interface Skill dependency. The solid open-diamond relationships show these unconditional exact-name loads. Project-specific directives select one helper provider, and the dotted relationship keeps that provider out of the default context until a claim operation needs it. The selected helper skill realizes the interface operations. Solo workflows load neither coordinate-work-items nor resource-claim.

The MCP helper route becomes selectable only after an MCP implementation satisfies resource-claim-helper and the verification boundary in resource-claim-helper-mcp. The current repository selects the command-line helper.

### Scenario: Delivering Accepted Work

This scenario applies after review and verification accept a commit for delivery. The exact deliver-work-item Interface Skill organizes the main-branch and feature-branch providers. The deliver-work-item-* family label remains in routing because AGENTS.md selects the provider named by the project Commit setting.

```mermaid
classDiagram
    direction LR

    class DevOrchestrator {
        <<Agent>>
    }

    class coordinate-work-items {
        <<SKILL.md>>
        <<Agent Skill>>
        +effective-commit-delivery-and-persistence-closure()
    }

    class project-specific-directives["Project-specific directives"] {
        <<AGENTS.md>>
        <<routing>>
        +route deliver-work-item => deliver-work-item-*
    }

    class DeliverWorkItem["deliver-work-item"] {
        <<Interface Skill>>
        +deliver-work-item(acceptedCommit)
    }

    class deliver-work-item-feature-branch {
        <<Provider Skill>>
        +deliver-work-item(acceptedCommit)
        +candidate-publication()
        +review-and-check-loop()
        +merge-and-completion-gate()
    }

    class deliver-work-item-main-branch {
        <<Provider Skill>>
        <<Cross-group>>
        +deliver-work-item(acceptedCommit)
        +main-reconciliation()
        +deliberate-integration()
    }

    class create-pull-request {
        <<SKILL.md>>
    }

    class integrate-agent-work {
        <<SKILL.md>>
        +merge-workflow()
        +verification()
    }

    DevOrchestrator o--> DeliverWorkItem
    coordinate-work-items ..> DeliverWorkItem : when a coordinated item reaches delivery
    project-specific-directives o..> deliver-work-item-feature-branch : when Commit is feature-branch
    project-specific-directives o..> deliver-work-item-main-branch : when Commit is main-branch
    deliver-work-item-feature-branch ..|> DeliverWorkItem
    deliver-work-item-main-branch ..|> DeliverWorkItem
    deliver-work-item-feature-branch o..> create-pull-request : when GitHub pull-request publication is required
    deliver-work-item-main-branch o..> integrate-agent-work : when implementation uses a separate branch or worktree
```

The provider realization arrows show conformance with the exact deliver-work-item contract. Feature-branch delivery loads create-pull-request only for a host that uses a pull request workflow. Main branch describes the final destination, not where implementation occurs. When implementation is isolated on a separate branch or worktree, especially for concurrent or independently delegated work, main-branch delivery uses integrate-agent-work to reconcile the accepted contribution with current main.

## Skill Responsibilities Used By These Agents

The responsibility inventory distinguishes the Work Item Dispatching skills from the independent Resource Coordination and Feature Branch And Worktrees groups used in the same agent workflow.

| Direct group | Skill | Public procedures or identity | Responsibility |
| --- | --- | --- | --- |
| Work Item Dispatching | coordinate-work-items; coordinate-codex-tasks | Resource Coordination; Queue Target And Scheduling; Effective Commit Delivery And Persistence Closure | Separates portable work-item policy from conditional Codex task mapping. |
| Work Item Dispatching | set-solo-mode | Set Solo Mode | Disables dispatch to secondary threads while the current Agent continues sequential work. |
| Work Item Dispatching | set-multitask-mode | Set Multitask Mode | Enables dispatch to secondary threads after the sequential condition ends. |
| Resource Coordination | resource-claim | Coordinate Shared Resource; Acquire Claim; Extend Claim; Extend Claim Deadline; Heartbeat Claim; Read Claim Status; Release Claim | Defines claim events, scope, conflicts, deadlines, and cleanup policy. |
| Resource Coordination | resource-claim-helper | Operation Contract; Read Claim Status; Acquire Claim; Extend Claim; Extend Claim Deadline; Heartbeat Claim; Release Claim; Reset Claim Registry; Maintain Claim Journal; Report Claim Contention; Structured Outcomes; Reconcile an Uncertain Outcome; Provider Realization Contract | Defines one provider-neutral helper interface without selecting a provider or redefining claim policy. |
| Resource Coordination | resource-claim-helper-command | Read Claim Status; Acquire Claim; Extend Claim; Extend Claim Deadline; Heartbeat Claim; Release Claim; Reset Claim Registry; Maintain Claim Journal; Report Claim Contention | Invokes the configured command-line helper without redefining the interface or claim policy. |
| Resource Coordination | resource-claim-helper-mcp | Current Availability; Read Claim Status; Acquire Claim; Extend Claim; Extend Claim Deadline; Heartbeat Claim; Release Claim; Reset Claim Registry; Maintain Claim Journal; Report Claim Contention | Maps the interface to MCP tools and preserves the unavailable-until-parity boundary. |
| Feature Branch And Worktrees | integrate-agent-work | Merge Workflow; Verification | Integrates accepted work from branches, worktrees, or agents and reconciles it with current main. |
| Feature Branch And Worktrees | deliver-work-item-feature-branch | Deliver Work Item; Candidate Publication; Review And Check Loop; Merge And Completion Gate | Publishes, reviews, corrects, and observes feature-branch delivery before lifecycle closure. |
| Feature Branch And Worktrees | create-pull-request | Create Or Update Pull Request; Review Order | Creates or updates a provider-accurate pull request and preserves its review order. |

## Authoritative Inputs

The Task Management Agent hierarchy, Agent Group dependencies, Core and Optional Agent Skills, scenario interfaces, and provider families are grounded in the following files.

### Task Management Agent Groups And Roles

The Agent-group views classify roles by task-management responsibility: backlog management or development delivery. The Agent dependencies and exact skill relationships come from these role sources and the shared role schema.

- [Conceptual Agent Role Schema](../../agents/role-schema.yaml)

- [Dev Backlog Coordinator](../../agents/roles/dev-activities/dev-backlog-coordinator.role.yaml)
- [Dev Backlog Steward](../../agents/roles/dev-activities/dev-backlog-steward.role.yaml)
- [Dev Backlog Watchdog](../../agents/roles/dev-activities/dev-backlog-watchdog.role.yaml)
- [Dev Orchestrator](../../agents/roles/dev-activities/dev-orchestrator.role.yaml)
- [Dev Coder](../../agents/roles/dev-activities/dev-coder.role.yaml)
- [Dev Code Reviewer](../../agents/roles/dev-activities/dev-code-reviewer.role.yaml)
- [Dev Verifier](../../agents/roles/dev-activities/dev-verifier.role.yaml)
- [Dev Merge Coordinator](../../agents/roles/dev-activities/dev-merge-coordinator.role.yaml)

### Core And Optional Agent Skills

The Core and Optional inventory uses the role schema and the complete skill lists in the Agent definitions above, supported by these skill sources.

- [Effective Communication](../../skills/effective-communication/SKILL.md)
- [STE Technical Writing](../../skills/ste-technical-writing/SKILL.md)
- [Structured Explanation](../../skills/structured-explanation/SKILL.md)
- [Structured Design](../../skills/structured-design/SKILL.md)
- [Organise Project Files](../../skills/organise-project-files/SKILL.md)
- [Review Structured Artifact](../../skills/review-structured-artifact/SKILL.md)
- [Explain Code Fix](../../skills/explain-code-fix/SKILL.md)
- [Coordinate Work Items](../../skills/coordinate-work-items/SKILL.md)
- [Coordinate Codex Tasks](../../skills/coordinate-codex-tasks/SKILL.md)
- [Resolve Backlog Blockage](../../skills/resolve-backlog-blockage/SKILL.md)
- [Set Solo Mode](../../skills/set-solo-mode/SKILL.md)
- [Set Multitask Mode](../../skills/set-multitask-mode/SKILL.md)
- [Integrate Agent Work](../../skills/integrate-agent-work/SKILL.md)

### Project Routing And Provider Implementations

The scenario diagrams use these project-routed policy, helper, creation, management, and delivery skill definitions.

- [Resource Claim](../../skills/resource-claim/SKILL.md)
- [Resource Claim Helper](../../skills/resource-claim-helper/SKILL.md)
- [Resource Claim Helper Command](../../skills/resource-claim-helper-command/SKILL.md)
- [Resource Claim Helper MCP](../../skills/resource-claim-helper-mcp/SKILL.md)
- [Deliver Work Item Feature Branch](../../skills/deliver-work-item-feature-branch/SKILL.md)
- [Deliver Work Item Main Branch](../../skills/deliver-work-item-main-branch/SKILL.md)
- [Deliver Work Item](../../skills/deliver-work-item/SKILL.md)
- [Create Pull Request](../../skills/create-pull-request/SKILL.md)
- [Create Work Item](../../skills/create-work-item/SKILL.md)
- [Create File Work Item](../../skills/create-work-item-file/SKILL.md)
- [Manage Future Ideas](../../skills/manage-future-ideas/SKILL.md)
- [Commit File Provider Transaction](../../skills/commit-file-provider-transaction/SKILL.md)
- [Create GitHub Work Item](../../skills/create-work-item-github/SKILL.md)
- [Create GitLab Work Item](../../skills/create-work-item-gitlab/SKILL.md)
- [Create Azure DevOps Work Item](../../skills/create-work-item-azure-devops/SKILL.md)
- [Create Jira Work Item](../../skills/create-work-item-jira/SKILL.md)
- [Manage Work Items](../../skills/manage-work-items/SKILL.md)
- [Manage File Work Items](../../skills/manage-work-items-file/SKILL.md)
- [Manage GitHub Work Items](../../skills/manage-work-items-github/SKILL.md)
- [Manage GitLab Work Items](../../skills/manage-work-items-gitlab/SKILL.md)
- [Manage Azure DevOps Work Items](../../skills/manage-work-items-azure-devops/SKILL.md)
- [Manage Jira Work Items](../../skills/manage-work-items-jira/SKILL.md)
