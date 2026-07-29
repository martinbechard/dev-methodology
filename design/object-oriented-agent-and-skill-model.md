# Object-Oriented Analysis Of Agents And Skills

## Scope

This document defines a conceptual vocabulary for object-oriented analysis of Agents and skills.

It covers:

- Agent Skills;
- Injected Skills;
- Peer Skills;
- Skill interfaces and SKILL.md files.

The document explains relationships through examples while defining no schema, migration, or repository change sequence.

## 1. Finality

- **GOAL: GOAL-1** Give callers stable procedure names for invoking skill procedures
  - **SYNOPSIS:** An agent or another skill can use a shared procedure name without knowing which SKILL.md supplies the procedure.
  - **EXAMPLE:** A Backlog Manager uses Create Workitem with a workitem description. The caller does not need to know whether the record will be a file or a GitLab issue.

- **GOAL: GOAL-2** Distinguish Agent Skills, Injected Skills, and Peer Skills
  - **SYNOPSIS:** An Agent Skill is named directly by an Agent. An Injected Skill is selected for an Agent through AGENTS.md. A Peer Skill complements another skill through either a direct reference or skills injection.
  - **EXAMPLE:** Dev Coder names careful-coding, Backlog Manager receives Create Workitem through injection, and complete-work-item-feature-branch invokes create-pull-request as a Peer Skill.

- **GOAL: GOAL-3** Treat a running agent as an object with context and state
  - **SYNOPSIS:** An agent definition is comparable to a class. One running agent or subagent is comparable to an object that combines the definition with a task, loaded skills, and changing state.
  - **EXAMPLE:** A running Backlog Manager has the user’s request, the effective AGENTS.md instructions, the selected workitem SKILL.md, and the current result of creating the item.

## 2. Information Model

| Term | Meaning | Example |
| --- | --- | --- |
| Global Agent space | An execution space in which an Agent can find available SKILL.md files. A skill’s availability in that space does not create a dependency by itself. | careful-coding and test-driven-development can both be available while an Agent execution uses only the applicable skills. |
| Skill interface | A shared procedure name and parameter meaning used by callers and implementing SKILL.md files. | Create Workitem accepts a workitem description. |
| AGENTS.md DII | A diagram prototype for a Skill interface whose implementation is selected through AGENTS.md. | Create Workitem is drawn as AGENTS.md DII. |
| Procedure name | A name shared by an invoker and a SKILL.md to identify the procedure the invoker needs. | Create Workitem. |
| Procedure parameter | Information passed by the invoker to the named procedure. | Workitem description: Add a new Cancel button. |
| Procedure | Instructions in a SKILL.md that explain how to perform the named operation. | Create a GitLab issue, read it back, and return its identity. |
| SKILL.md | A concrete skill definition that contains one or more procedures. This file is the concrete implementation side of the analogy. | create-gitlab-work-item/SKILL.md contains the GitLab workitem-creation procedure. |
| Agent Skill | A SKILL.md referenced by exact name in an Agent definition, either for every execution or under a routing condition. | Dev Coder names careful-coding for every execution and test-driven-development when behavior can be expressed through tests. |
| Conditional routing | A condition on an Agent Skill reference that limits when the Agent uses that exact skill. | Dev Coder uses test-driven-development when executable tests should guide implementation. |
| Injectable Skill | A SKILL.md written to export an implementation under a shared procedure name and parameter meaning so AGENTS.md can select it without changing the invoker. | create-file-work-item and create-gitlab-work-item can export implementations of Create Workitem. |
| Injected Skill | The Injectable Skill selected for a particular Agent through AGENTS.md. | create-gitlab-work-item is the Injected Skill when AGENTS.md binds it to Create Workitem. |
| Skills injection | An AGENTS.md instruction that tells an Agent which SKILL.md supplies the implementation of a procedure invoked by an Agent or Peer Skill. | When you need to Create Workitem, load create-gitlab-work-item. |
| Peer Skill | A SKILL.md intended to complement another SKILL.md. Peer Skills can reference one another directly or use skills injection. | complete-work-item-feature-branch directly invokes create-pull-request for GitHub publication. |
| Agent class | A reusable agent definition containing purpose, instructions, known dependencies, and outputs. | Backlog Manager. |
| Agent object | One task-bound execution of an agent class with context and changing state. | The Backlog Manager processing the Cancel button request. |

## 3. Skills In The Global Agent Space

Skills exist globally in an Agent’s space, much as code modules exist in a process. The space makes a SKILL.md available for loading, but availability alone does not create coupling.

Object-oriented analysis distinguishes three facts:

- whether an invoker knows an exact skill name;
- which procedure name the invoker calls;
- whether another implementation can be selected without changing the invoker.

The procedure name is the common call boundary across these relationships.

- **RULE: RULE-1** A skill is linked to its invoker through a procedure name
  - **SYNOPSIS:** The procedure name identifies the call in the Agent’s global skill space. An exact skill-name reference or an AGENTS.md binding determines how the invoker reaches the implementing SKILL.md.
  - **EXAMPLE:** A Backlog Manager invokes Create Workitem with Add a new Cancel button as its workitem-description parameter.

```mermaid
classDiagram
    direction LR

    class GlobalAgentSpace {
        <<Agent space>>
        +availableSkills
    }

    class Agent {
        <<Agent>>
        +requestProcedure()
    }

    class CreateWorkitem {
        <<AGENTS.md DII>>
        +createWorkitem(workitemDescription)
    }

    class ImplementingSkill {
        <<SKILL.md>>
        +createWorkitem(workitemDescription)
    }

    class CarefulCodingSkill {
        <<SKILL.md>>
        <<Agent Skill>>
        +applyCarefulCoding()
    }

    GlobalAgentSpace o-- Agent : hosts
    GlobalAgentSpace o-- ImplementingSkill : exposes module
    GlobalAgentSpace o-- CarefulCodingSkill : exposes module
    Agent --> CarefulCodingSkill : references by skill name
    Agent ..> CreateWorkitem : invokes by procedure name
    CreateWorkitem <|.. ImplementingSkill : exported implementation
```

Create Workitem is the human-readable procedure name. createWorkitem(workitemDescription) is the diagram notation for the same procedure and its parameter.

The AGENTS.md DII prototype marks the pure-virtual side of the analogy. The SKILL.md contains the procedure that gives the shared procedure name its concrete behavior.

## 4. Agent Skills

An Agent Skill is a SKILL.md that an Agent definition references by exact name. The reference can apply to every execution of that Agent role or only when a routing condition is satisfied.

This section covers only Agent-to-skill references. Skill-to-skill relationships are Peer Skills.

- **RULE: RULE-5** An Agent Skill is referenced by its skill name
  - **SYNOPSIS:** The Agent definition knows the exact SKILL.md identity and follows that skill’s procedure names, parameters, and instructions.
  - **EXAMPLE:** Dev Coder names careful-coding directly in its skill list.

- **RULE: RULE-6** An unconditional Agent Skill applies to every execution of the Agent role
  - **SYNOPSIS:** An Agent definition lists the skill without a condition because that dependency belongs to every execution of the role.
  - **EXAMPLE:** Dev Coder lists careful-coding without a condition so every Dev Coder execution applies it.

- **RULE: RULE-7** A condition routes an Agent to a named Agent Skill
  - **SYNOPSIS:** The Agent definition still knows the exact skill name, but it uses that skill only when the declared condition matches the task.
  - **EXAMPLE:** Dev Coder names test-driven-development under the condition that executable tests should guide the implementation.

```mermaid
classDiagram
    direction LR

    class DevCoder {
        <<Agent>>
        +implementChange()
    }

    class CarefulCodingSkill {
        <<SKILL.md>>
        <<Agent Skill>>
        +applyCarefulCoding()
    }

    class TestDrivenDevelopmentSkill {
        <<SKILL.md>>
        <<Agent Skill>>
        +applyTestDrivenDevelopment()
    }

    DevCoder --> CarefulCodingSkill : references by name every time
    DevCoder --> TestDrivenDevelopmentSkill : references by name when condition matches
```

Both references couple Dev Coder to an exact skill name. The condition changes when the reference applies; it does not turn the reference into skills injection.

## 5. Injected Skills

Injected Skills are Injectable Skills selected for an Agent through AGENTS.md. The Agent invokes a shared procedure name and does not name the implementing SKILL.md.

- **RULE: RULE-2** The Agent, AGENTS.md, and the implementing SKILL.md share the same procedure name
  - **SYNOPSIS:** The procedure name connects the Agent’s intent, the injection instruction, and the concrete procedure.
  - **EXAMPLE:** The Backlog Manager needs Create Workitem. AGENTS.md links Create Workitem to create-gitlab-work-item. That SKILL.md defines the Create Workitem procedure for GitLab.

- **RULE: RULE-3** An Injectable Skill encapsulates selectable technology or procedure details
  - **SYNOPSIS:** The Injectable Skill owns the technology-specific or procedure-specific instructions that the Agent should not repeat.
  - **EXAMPLE:** The GitLab skill owns issue search, issue creation, read-back verification, and GitLab identity. The Backlog Manager supplies only the workitem description.

- **RULE: RULE-4** AGENTS.md selects one of several implementations
  - **SYNOPSIS:** AGENTS.md tells the agent which SKILL.md to load when it needs the procedure.
  - **EXAMPLE:** One project links Create Workitem to create-file-work-item. Another links the same procedure name to create-gitlab-work-item.

```mermaid
classDiagram
    direction LR

    class BacklogManager {
        <<Agent>>
        +createRequestedItem()
    }

    class CreateWorkitem {
        <<AGENTS.md DII>>
        +createWorkitem(workitemDescription)
    }

    class FileWorkitemSkill {
        <<SKILL.md>>
        <<Injectable Skill>>
        +createWorkitem(workitemDescription)
    }

    class GitLabWorkitemSkill {
        <<SKILL.md>>
        <<Injectable Skill>>
        +createWorkitem(workitemDescription)
    }

    BacklogManager ..> CreateWorkitem : invokes
    CreateWorkitem <|.. FileWorkitemSkill : exported implementation
    CreateWorkitem <|.. GitLabWorkitemSkill : exported implementation
```

The two SKILL.md files use the same procedure name and parameter meaning. Their internal procedures and provider evidence remain different.

The two Agent dependency styles differ at the selection boundary:

| Relationship | Agent knows | Selection | Substitution |
| --- | --- | --- | --- |
| Agent Skill | The exact skill name and that skill’s procedures. | The Agent definition references the skill for every execution or under a condition. | Replacement usually requires changing the Agent definition. |
| Injected Skill | The procedure name and parameter meaning. | AGENTS.md selects an implementing SKILL.md. | Another SKILL.md can be selected when it implements the same procedure name and parameter meaning. |

## 6. Peer Skills

A Peer Skill complements another SKILL.md. Peer describes a relationship between complementary skills, not a third implementation-selection mechanism.

- **RULE: RULE-28** Peer Skills provide complementary procedures
  - **SYNOPSIS:** One Peer Skill invokes another when the second skill owns a distinct procedure needed inside the first skill’s workflow.
  - **EXAMPLE:** complete-work-item-feature-branch uses create-pull-request to publish a GitHub pull request.

- **RULE: RULE-29** A direct Peer Skill reference couples two SKILL.md files by name
  - **SYNOPSIS:** The invoking SKILL.md knows the exact Peer Skill and follows that peer’s procedure.
  - **EXAMPLE:** complete-work-item-feature-branch names create-pull-request directly for GitHub publication.

- **RULE: RULE-30** A Peer Skill can be selected through skills injection
  - **SYNOPSIS:** The invoking SKILL.md can use a shared procedure name while AGENTS.md selects the complementary implementation.
  - **EXAMPLE:** A development-workflow SKILL.md can invoke Run Project Tests while AGENTS.md selects JUnit or Jest for the project.

```mermaid
classDiagram
    direction LR

    class FeatureBranchCompletionSkill {
        <<SKILL.md>>
        <<Peer Skill>>
        +publishAcceptedChange()
    }

    class CreatePullRequestSkill {
        <<SKILL.md>>
        <<Peer Skill>>
        +createPullRequest()
    }

    class DevelopmentWorkflowSkill {
        <<SKILL.md>>
        <<Peer Skill>>
        +verifyChange()
    }

    class RunProjectTests {
        <<AGENTS.md DII>>
        +runProjectTests(testScope)
    }

    class JUnitSkill {
        <<SKILL.md>>
        <<Peer Skill>>
        <<Injectable Skill>>
        +runProjectTests(testScope)
    }

    class JestSkill {
        <<SKILL.md>>
        <<Peer Skill>>
        <<Injectable Skill>>
        +runProjectTests(testScope)
    }

    FeatureBranchCompletionSkill --> CreatePullRequestSkill : invokes by skill name
    DevelopmentWorkflowSkill ..> RunProjectTests : invokes by procedure name
    RunProjectTests <|.. JUnitSkill : selectable peer implementation
    RunProjectTests <|.. JestSkill : selectable peer implementation
```

A direct reference is simpler when the invoking skill always needs the same peer. Skills injection preserves the Peer Skill relationship while allowing AGENTS.md to select a different complementary implementation.

## 7. From User Request To Skill Interface

This section separates understanding the user’s request from choosing the implementation.

- **PROCESS: PROCESS-1** Receive a user request
  - **SYNOPSIS:** The agent receives natural language describing the desired backlog change.
  - **EXAMPLE:** The Backlog Manager is told, “Add a new item to create a Cancel button into the backlog.”

- **PROCESS: PROCESS-2** Transform the request into an interface invocation
  - **SYNOPSIS:** The agent identifies the procedure name and constructs the parameter required by the Skill interface.
  - **EXAMPLE:** The agent concludes, “I must Create Workitem with the following workitem description: Add a new Cancel button.”

- **RULE: RULE-8** A procedure parameter carries intent rather than provider details
  - **SYNOPSIS:** The workitem description says what record is needed. The selected SKILL.md decides how its provider represents the record.
  - **EXAMPLE:** Add a new Cancel button does not contain a repository path, GitLab project identifier, label set, or issue URL.

```mermaid
sequenceDiagram
    actor User
    participant Agent as Backlog Manager Agent
    participant Interface as Create Workitem AGENTS.md DII

    User->>Agent: Add a new item to create a Cancel button into the backlog
    Agent->>Agent: Identify the Create Workitem procedure name
    Agent->>Agent: Build workitem description as Add a new Cancel button
    Agent->>Interface: createWorkitem(workitemDescription)
```

At this point, the agent knows what procedure it needs and what information it will pass. It has not chosen file or GitLab behavior itself.

## 8. Skills Injection Through AGENTS.md

AGENTS.md links a procedure name to a concrete SKILL.md.

- **PROCESS: PROCESS-3** Provide the injection instruction
  - **SYNOPSIS:** Effective project guidance tells the agent which skill to load when the procedure is needed.
  - **EXAMPLE:** “When you need to Create Workitem, load create-gitlab-work-item.”

- **RULE: RULE-9** AGENTS.md owns the binding outside the calling agent
  - **SYNOPSIS:** The Backlog Manager retains the Create Workitem procedure name and parameter meaning when project setup chooses another implementation.
  - **EXAMPLE:** Changing the AGENTS.md instruction from create-gitlab-work-item to create-file-work-item does not change the agent’s workitem description.

```mermaid
classDiagram
    direction LR

    class CreateWorkitem {
        <<AGENTS.md DII>>
        +createWorkitem(workitemDescription)
    }

    class AgentsGuidance {
        <<AGENTS.md>>
        +when CreateWorkitem load GitLabWorkitemSkill
    }

    class GitLabWorkitemSkill {
        <<SKILL.md>>
        <<Injectable Skill>>
        +createWorkitem(workitemDescription)
    }

    AgentsGuidance ..> CreateWorkitem : recognizes procedure name
    AgentsGuidance ..> GitLabWorkitemSkill : injects implementation
    CreateWorkitem <|.. GitLabWorkitemSkill : exported implementation
```

Skills injection is an instruction relationship. AGENTS.md makes the selected SKILL.md available by reference; this model does not require a compiled interface object or a software dependency-injection container.

## 9. Loading And Invoking The Selected SKILL.md

The agent follows the injection instruction only when it needs the Skill interface.

- **PROCESS: PROCESS-4** Load the selected skill
  - **SYNOPSIS:** The agent reads the SKILL.md named by AGENTS.md.
  - **EXAMPLE:** The agent concludes, “AGENTS.md says Create Workitem is supplied by create-gitlab-work-item, so I will load that SKILL.md.”

- **PROCESS: PROCESS-5** Find the procedure with the shared name
  - **SYNOPSIS:** The loaded SKILL.md uses the same procedure name and explains the concrete steps.
  - **EXAMPLE:** The agent concludes, “I will follow the Create Workitem procedure found in this SKILL.md.”

- **PROCESS: PROCESS-6** Invoke the selected procedure with the procedure parameter
  - **SYNOPSIS:** The implementing procedure receives the workitem description that the caller constructed.
  - **EXAMPLE:** The GitLab procedure receives Add a new Cancel button, then applies its own duplicate search, issue creation, and read-back rules.

```mermaid
sequenceDiagram
    participant Agent as Backlog Manager Agent
    participant Guidance as AGENTS.md
    participant Skill as create-gitlab-work-item SKILL.md
    participant GitLab

    Agent->>Guidance: Which skill implements Create Workitem
    Guidance-->>Agent: Load create-gitlab-work-item
    Agent->>Skill: Load SKILL.md
    Skill-->>Agent: Create Workitem procedure
    Agent->>Skill: createWorkitem(Add a new Cancel button)
    Skill->>GitLab: Apply the GitLab-specific procedure
    GitLab-->>Skill: Observed issue identity
    Skill-->>Agent: Created workitem result
```

The agent’s request, procedure name, and parameter meaning stay the same when another Injectable Skill is selected. The provider-specific actions come from the loaded SKILL.md.

## 10. One Or More Interfaces In A SKILL.md

The number of Skill interfaces depends on how many independently invocable procedure names the SKILL.md defines.

- **RULE: RULE-10** A simple SKILL.md can export one Skill interface
  - **SYNOPSIS:** One procedure name and its cohesive procedure are enough for a focused skill.
  - **EXAMPLE:** A GitLab workitem-creation SKILL.md exports an implementation of Create Workitem.

- **RULE: RULE-11** A more complex SKILL.md can export several Skill interfaces
  - **SYNOPSIS:** One file can define several procedure names when it contains procedures that callers invoke independently and that do not describe the same cross-cutting concern.
  - **EXAMPLE:** A repository-hosting SKILL.md can export implementations of Create Workitem and Publish Change as separate Skill interfaces.

- **RULE: RULE-12** Multiple interfaces describe the SKILL.md without deciding its structure
  - **SYNOPSIS:** The analysis records each independently invoked procedure name. It does not conclude from that fact alone that the SKILL.md should be split.
  - **EXAMPLE:** Create Workitem and Publish Change remain distinct procedure names even when one SKILL.md implements both.

```mermaid
classDiagram
    direction LR

    class CreateWorkitem {
        <<AGENTS.md DII>>
        +createWorkitem(workitemDescription)
    }

    class PublishChange {
        <<AGENTS.md DII>>
        +publishChange(changeDescription)
    }

    class RepositoryHostingSkill {
        <<SKILL.md>>
        +createWorkitem(workitemDescription)
        +publishChange(changeDescription)
    }

    CreateWorkitem <|.. RepositoryHostingSkill : exported implementation
    PublishChange <|.. RepositoryHostingSkill : exported implementation
```

An Agent Skill or a directly referenced Peer Skill can also contain several procedures. Those procedures do not become interchangeable Skill interfaces merely because they share one file. Interchangeability requires the SKILL.md, its invokers, and alternative implementations to share the same procedure names and parameter meanings.

## 11. A Second Injected Example: Deliver Workitem

The same relationship applies to completion procedures.

- **PROCESS: PROCESS-7** Request delivery after review and testing
  - **SYNOPSIS:** A development workflow invokes Deliver Workitem with the accepted change after its required gates pass.
  - **EXAMPLE:** The caller concludes, “Review and testing passed. I must Deliver Workitem with accepted commit abc123.”

- **RULE: RULE-13** AGENTS.md selects the delivery SKILL.md
  - **SYNOPSIS:** The calling workflow uses the same procedure name while project guidance selects direct-main or feature-branch delivery.
  - **EXAMPLE:** AGENTS.md can link Deliver Workitem to complete-work-item-direct-main or complete-work-item-feature-branch.

```mermaid
classDiagram
    direction LR

    class DevelopmentWorkflow {
        <<Agent or SKILL.md>>
        +deliverAcceptedChange()
    }

    class DeliverWorkitem {
        <<AGENTS.md DII>>
        +deliverWorkitem(acceptedCommit)
    }

    class DirectMainSkill {
        <<SKILL.md>>
        <<Injectable Skill>>
        +deliverWorkitem(acceptedCommit)
    }

    class FeatureBranchSkill {
        <<SKILL.md>>
        <<Injectable Skill>>
        +deliverWorkitem(acceptedCommit)
    }

    DevelopmentWorkflow ..> DeliverWorkitem : invokes
    DeliverWorkitem <|.. DirectMainSkill : exported implementation
    DeliverWorkitem <|.. FeatureBranchSkill : exported implementation
```

The direct-main SKILL.md can integrate and observe the change on main. The feature-branch SKILL.md can publish a branch, wait for review and checks, and observe the merge. Both procedures are reached through the Deliver Workitem procedure name.

## 12. Agent Classes, Objects, And Skill Dependencies

An Agent can use named Agent Skills and Injected Skills together.

- **RULE: RULE-14** The agent class owns reusable purpose and known dependencies
  - **SYNOPSIS:** The Agent definition states its purpose, the Skill interfaces it invokes, and the Agent Skills it names.
  - **EXAMPLE:** A coding-agent class can name careful-coding directly and invoke Deliver Workitem without naming the delivery SKILL.md.

- **RULE: RULE-15** The agent object owns task context and changing state
  - **SYNOPSIS:** One running instance receives the task, effective AGENTS.md, loaded SKILL.md files, and execution evidence.
  - **EXAMPLE:** One coding-agent object holds accepted commit abc123, knows feature-branch is the injected delivery skill, and is waiting for review.

- **RULE: RULE-16** Technology and project skills can be injectable through shared procedure names
  - **SYNOPSIS:** A technology or project SKILL.md is injectable when it implements a procedure name and parameter meaning that the Agent already invokes.
  - **EXAMPLE:** A testing agent can invoke Run Project Tests with a test scope while AGENTS.md selects a JUnit or Jest SKILL.md for the project.

```mermaid
classDiagram
    direction TB

    class CodingAgentClass {
        <<Agent class>>
        +purpose
        +invoke DeliverWorkitem
        +use CarefulCodingSkill
    }

    class RunningCodingAgent {
        <<Agent object>>
        +acceptedCommit abc123
        +state awaitingReview
    }

    class CarefulCodingSkill {
        <<SKILL.md>>
        <<Agent Skill>>
    }

    class FeatureBranchSkill {
        <<SKILL.md>>
        <<Injectable Skill>>
        +deliverWorkitem(acceptedCommit)
    }

    CodingAgentClass <|-- RunningCodingAgent : instance of
    CodingAgentClass --> CarefulCodingSkill : names directly
    FeatureBranchSkill --> RunningCodingAgent : injected through AGENTS.md
```

The class-and-object notation describes the analysis. It does not require the harness to construct a software object at runtime.

## 13. Agent Base Classes And Multiple Inheritance

Shared agent relationships can be shown once when several agent classes use the same procedure dependencies and behavior.

- **RULE: RULE-17** A base class represents genuinely shared agent behavior
  - **SYNOPSIS:** A base agent class can own instructions or Skill interface dependencies that mean the same thing for each inheriting agent.
  - **EXAMPLE:** Reviewing Agent can define Review Artifact once for code, documentation, and methodology reviewers.

- **RULE: RULE-18** Shared SKILL.md use does not imply inheritance
  - **SYNOPSIS:** Two agents can load the same skill while retaining different purposes and class relationships.
  - **EXAMPLE:** A coder and a verifier can both use a testing SKILL.md without becoming subclasses of one Testing Agent class.

- **RULE: RULE-19** An agent class can inherit multiple independent base classes
  - **SYNOPSIS:** One agent class can inherit the procedure dependencies and behavior of more than one base agent class.
  - **EXAMPLE:** Dev Security Reviewer can inherit Reviewing Agent and Security Analysis Agent.

```mermaid
classDiagram
    direction TB

    class ReviewingAgent {
        <<Agent base class>>
        +reviewArtifact()
    }

    class SecurityAnalysisAgent {
        <<Agent base class>>
        +analyzeSecurity()
    }

    class DevSecurityReviewer {
        <<Agent class>>
    }

    ReviewingAgent <|-- DevSecurityReviewer
    SecurityAnalysisAgent <|-- DevSecurityReviewer
```

## 14. Constraints

- **RULE: RULE-20** A loaded skill is not necessarily injectable
  - **SYNOPSIS:** A SKILL.md is injectable only when it and its invokers share a procedure name and parameter meaning that another implementation can also use.
  - **EXAMPLE:** An Agent can load code-discovery by name as an Agent Skill without making code-discovery injectable.

- **RULE: RULE-21** Provider-specific procedure details remain inside SKILL.md
  - **SYNOPSIS:** A shared procedure name stabilizes the invoker. It does not make the file and GitLab procedures identical internally.
  - **EXAMPLE:** Create Workitem can produce a repository-backed record through one SKILL.md and a GitLab issue through another while each procedure preserves provider-accurate evidence.

- **RULE: RULE-22** Skills injection and agent inheritance are separate relationships
  - **SYNOPSIS:** AGENTS.md selects a SKILL.md implementation. Agent inheritance shares agent-class behavior.
  - **EXAMPLE:** Injecting a GitLab workitem skill does not make Backlog Manager a subclass of a GitLab agent.

- **RULE: RULE-23** The model remains conceptual
  - **SYNOPSIS:** The document explains the vocabulary and relationships without prescribing a schema, migration order, or repository change sequence.
  - **EXAMPLE:** The diagrams show Create Workitem with the AGENTS.md DII prototype without specifying a new YAML field for declaring it.

## 15. Definition Of Good

- **RULE: RULE-24** The diagrams distinguish AGENTS.md DII from SKILL.md
  - **SYNOPSIS:** Diagrams label an injected shared contract as AGENTS.md DII and a concrete skill definition as SKILL.md.
  - **EXAMPLE:** CreateWorkitem has the AGENTS.md DII stereotype; GitLabWorkitemSkill has the SKILL.md stereotype.

- **RULE: RULE-25** The complete workitem invocation is traceable
  - **SYNOPSIS:** A reader can follow the request from the user, through the agent’s procedure name and parameter, through AGENTS.md injection, to the selected SKILL.md procedure.
  - **EXAMPLE:** Add a new Cancel button becomes createWorkitem(workitemDescription), AGENTS.md selects create-gitlab-work-item, and that SKILL.md performs the GitLab procedure.

- **RULE: RULE-26** Direct and injected dependency styles have valid uses
  - **SYNOPSIS:** Agent Skills and direct Peer Skill references support exact dependencies. Injected Skills support substitution.
  - **EXAMPLE:** Dev Coder names careful-coding as an Agent Skill, complete-work-item-feature-branch names create-pull-request as a Peer Skill, and Create Workitem uses injection.

- **RULE: RULE-27** Every assertion includes an example
  - **SYNOPSIS:** Each GOAL, RULE, PROCESS, and other structured assertion is followed by an EXAMPLE.
  - **EXAMPLE:** RULE-20 defines the Injectable Skill boundary and illustrates it with code-discovery.

## Authoritative Inputs

- The user-supplied object-oriented analysis and vocabulary corrections for this document.
- [Agentic Configuration](agentic-configuration.html)
- [Work-Item Provider And Completion Contracts](work-item-provider-and-completion-contracts.md)
- [Create File Work Item](../skills/create-file-work-item/SKILL.md)
- [Create GitLab Work Item](../skills/create-gitlab-work-item/SKILL.md)
- [Complete Work Item Direct Main](../skills/complete-work-item-direct-main/SKILL.md)
- [Complete Work Item Feature Branch](../skills/complete-work-item-feature-branch/SKILL.md)
- [Create Pull Request](../skills/create-pull-request/SKILL.md)
- [Code Discovery](../skills/code-discovery/SKILL.md)
- [Careful Coding](../skills/careful-coding/SKILL.md)
- [JUnit](../skills/junit/SKILL.md)
- [Jest](../skills/jest/SKILL.md)
- [Dev Coder](../agents/roles/dev-activities/dev-coder.role.yaml)
- [Dev Orchestrator](../agents/roles/dev-activities/dev-orchestrator.role.yaml)
- [Dev Backlog Coordinator](../agents/roles/dev-activities/dev-backlog-coordinator.role.yaml)
- [Dev Backlog Steward](../agents/roles/dev-activities/dev-backlog-steward.role.yaml)
