# Direct Main Delivery Skill Group

## Scope

Direct Main Delivery is the Commit alternative to feature-branch delivery. Its delivery skill directly names concurrency-owned claim and integration skills.

The applied-model conventions are defined in [Object-Oriented Skill Group Models](../object-oriented-skill-group-models.md#2-applied-model-legend).

## Design

The design exposes the same Deliver Work Item procedure used by feature-branch delivery while keeping direct-main reconciliation and evidence inside its selected implementation.

```mermaid
classDiagram
    direction LR

    class DevOrchestrator {
        <<Agent>>
    }

    class DeliverWorkItem["deliver-work-item-*"] {
        <<AGENTS.md>>
        <<routing>>
        +deliver-work-item(acceptedCommit)
    }

    namespace DirectMainDelivery {
        class deliver-work-item-direct-main {
            <<SKILL.md>>
            <<Injectable Skill>>
            +deliver-work-item()
            +evidence-gate()
            +main-reconciliation()
            +deliberate-integration()
            +integrated-verification-and-main-observation()
        }
    }

    class agent-claim {
        <<SKILL.md>>
        <<Cross-group>>
    }

    class integrate-agent-work {
        <<SKILL.md>>
        <<Cross-group>>
    }

    DevOrchestrator --> DeliverWorkItem
    DeliverWorkItem o--> deliver-work-item-direct-main
    deliver-work-item-direct-main o--> agent-claim
    deliver-work-item-direct-main o..> integrate-agent-work : when the accepted commit is not represented on main
```

## Skill Responsibility

The group contains one selected Commit provider.

| Skill | Public procedures | Responsibility |
| --- | --- | --- |
| deliver-work-item-direct-main | Deliver Work Item; Evidence Gate; Main Reconciliation; Deliberate Integration; Integrated Verification And Main Observation | Integrates an accepted candidate into main, verifies the integrated state, and returns evidence for separate provider lifecycle closure. |

## Authoritative Inputs

The delivery relationship and procedure boundary are grounded in these Agent and skill definitions.

- [Dev Orchestrator](../../agents/roles/dev-activities/dev-orchestrator.role.yaml)
- [Deliver Work Item Direct Main](../../skills/deliver-work-item-direct-main/SKILL.md)
- [Integrate Agent Work](../../skills/integrate-agent-work/SKILL.md)
- [Agent Claim](../../skills/agent-claim/SKILL.md)
