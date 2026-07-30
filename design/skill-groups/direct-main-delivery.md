# Direct Main Delivery Skill Group

## Scope

Direct Main Delivery is the Commit alternative to feature-branch delivery. Its current skill directly names concurrency-owned claim and integration skills.

The shared notation and recommendation boundary are defined in [Object-Oriented Skill Group Models](../object-oriented-skill-group-models.md).

## Current Design

```mermaid
classDiagram
    direction LR

    class DevOrchestrator {
        <<Agent>>
    }

    class DeliverWorkItem["complete-work-item-*"] {
        <<AGENTS.md>>
        +deliver-work-item(acceptedCommit)
    }

    namespace DirectMainDelivery {
        class complete-work-item-direct-main {
            <<SKILL.md>>
            <<Injectable Skill>>
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

    class agent-work-merge {
        <<SKILL.md>>
        <<Cross-group>>
    }

    DevOrchestrator --> DeliverWorkItem
    DeliverWorkItem o--> complete-work-item-direct-main
    complete-work-item-direct-main o--> agent-claim
    complete-work-item-direct-main o..> agent-work-merge : when the accepted commit is not represented on main
```

Dev Orchestrator knows the Deliver Work Item procedure. AGENTS.md names complete-work-item-direct-main when direct-main is the effective Commit selection.

The concrete node shows the current internal procedure headings. None is named Deliver Work Item, which is the interface mismatch recorded in the recommendation below.

agent-claim and agent-work-merge remain in Concurrent Tasking. The open diamonds show that complete-work-item-direct-main currently names those exact skills instead of reaching them through a procedure-mapped AGENTS.md interface.

## Skill Recommendations

| Skill | Current source boundary | Recommendation | Reason |
| --- | --- | --- | --- |
| complete-work-item-direct-main | Evidence Gate, Main Reconciliation, Deliberate Integration, and Integrated Verification And Main Observation implement delivery; Lifecycle Handoff returns provider evidence without closing the provider record. | Rename the skill to deliver-work-item-direct-main and introduce Deliver Work Item as its interface heading. | Deliver matches the caller’s Commit procedure and avoids implying that the skill itself completes provider lifecycle closure. |

## Authoritative Inputs

- [Dev Orchestrator](../../agents/roles/dev-activities/dev-orchestrator.role.yaml)
- [Complete Work Item Direct Main](../../skills/complete-work-item-direct-main/SKILL.md)
- [Agent Work Merge](../../skills/agent-work-merge/SKILL.md)
- [Agent Claim](../../skills/agent-claim/SKILL.md)
