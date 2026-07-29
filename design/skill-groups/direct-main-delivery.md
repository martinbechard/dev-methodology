# Direct Main Delivery Skill Group

## Scope

Direct Main Delivery is the alternative Commit implementation when Concurrent Tasking is not selected. Its current SKILL.md reaches into concurrency-owned integration and resource-coordination skills.

The shared notation and cross-group markers are defined in [Object-Oriented Skill Group Models](../object-oriented-skill-group-models.md).

## Current Design

```mermaid
classDiagram
    direction LR

    class DevOrchestrator {
        <<Agent class>>
    }

    class DeliverWorkitem {
        <<AGENTS.md DII>>
        +deliverWorkitem(acceptedCommit)
    }

    namespace DirectMainDelivery {
        class CompleteWorkitemDirectMain {
            <<SKILL.md>>
            <<Injectable Skill>>
            <<Cross-group responsibility>>
            +skill complete-work-item-direct-main
            +procedure Evidence Gate
            +procedure Main Reconciliation
            +procedure Deliberate Integration
            +procedure Integrated Verification And Main Observation
        }
    }

    class AgentWorkMerge {
        <<SKILL.md>>
        <<Cross-group>>
        <<Peer Skill>>
        +skill agent-work-merge
        +procedure Merge Workflow
    }

    class ResourceCoordination {
        <<AGENTS.md DII>>
        <<Cross-group>>
        +procedure Claim Events
    }

    DevOrchestrator ..> DeliverWorkitem : invokes after accepted gates
    DeliverWorkitem <|.. CompleteWorkitemDirectMain : exported implementation
    CompleteWorkitemDirectMain --> AgentWorkMerge : Deliberate Integration uses Merge Workflow
    CompleteWorkitemDirectMain ..> ResourceCoordination : Main Reconciliation uses Claim Events
```

The caller invokes one Deliver Workitem contract with an accepted commit. AGENTS.md selects complete-work-item-direct-main, whose several titled procedures reconcile main, integrate when necessary, verify the integrated result, and observe main.

agent-work-merge and Resource Coordination retain their primary placement under Concurrent Tasking. Their Cross-group markers expose the current direct-main coupling.

## Authoritative Inputs

- [Dev Orchestrator](../../agents/roles/dev-activities/dev-orchestrator.role.yaml)
- [Complete Work Item Direct Main](../../skills/complete-work-item-direct-main/SKILL.md)
- [Agent Work Merge](../../skills/agent-work-merge/SKILL.md)
- [Agent Claim](../../skills/agent-claim/SKILL.md)
