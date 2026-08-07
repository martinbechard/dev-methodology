# Review And Verification Skill Group

## Scope

Review And Verification contains evidence review, test selection, end-to-end verification, diagnosis, runtime observation, source tracing, and prompt-contract review. Agent definitions combine these skills with exact-name Baseline Development skills.

The applied-model conventions are defined in [Object-Oriented Skill Group Models](../object-oriented-skill-group-models.md#2-applied-model-legend).

## Design

Review And Verification supplies distinct procedures for code review, verification, runtime diagnosis, and prompt review. The overall view establishes the Agent and Skill Group landscape; the scenario views expand each role’s core and conditional dependencies and the supporting evidence relationships among skills.

### Overall Agent And Skill Group Dependencies

The overall view shows the four principal review and verification Agents, their shared use of Baseline Development, and the optional Resource Coordination dependency used by an end-to-end verification scenario.

```mermaid
classDiagram
    direction LR

    namespace ReviewAndVerificationAgents["Review And Verification Agents"] {
        class DevCodeReviewer {
            <<Agent>>
        }
        class DevVerifier {
            <<Agent>>
        }
        class DevRuntimeDiagnostician {
            <<Agent>>
        }
        class DevPromptReviewer {
            <<Agent>>
        }
    }

    class ReviewAndVerification["Review And Verification"] {
        <<Skill Group>>
    }
    class BaselineDevelopment["Baseline Development"] {
        <<Skill Group>>
    }
    class ResourceCoordination["Resource Coordination"] {
        <<Skill Group>>
    }

    DevCodeReviewer --> ReviewAndVerification
    DevCodeReviewer --> BaselineDevelopment
    DevVerifier --> ReviewAndVerification
    DevVerifier --> BaselineDevelopment
    DevRuntimeDiagnostician --> ReviewAndVerification
    DevRuntimeDiagnostician --> BaselineDevelopment
    DevPromptReviewer --> ReviewAndVerification
    DevPromptReviewer --> BaselineDevelopment
    ReviewAndVerification ..> ResourceCoordination : when end-to-end verification triggers a claim event
```

### Scenario: Reviewing Code

This scenario shows the evidence-review skill and Baseline Development guidance that Dev Code Reviewer loads for every code review, plus file-placement guidance when the review creates a project artifact.

```mermaid
classDiagram
    direction LR

    class DevCodeReviewer {
        <<Agent>>
    }
    class review-code-with-evidence {
        <<SKILL.md>>
        <<Agent Skill>>
        +evidence-packet
        +synthesis-rules
    }
    class careful-coding {
        <<SKILL.md>>
        <<Cross-group>>
        +confirm-work-before-coding()
        +validate-authorized-contract()
        +execute-goal-driven-loop()
    }
    class code-comments {
        <<SKILL.md>>
        <<Cross-group>>
        +review-code-comments()
    }
    class review-structured-artifact {
        <<SKILL.md>>
        <<Cross-group>>
    }

    DevCodeReviewer o--> review-code-with-evidence
    DevCodeReviewer o--> careful-coding
    DevCodeReviewer o--> code-comments
    DevCodeReviewer o--> review-structured-artifact
```

### Scenario: Verifying A Change

This scenario shows the test, review, and explanation skills Dev Verifier always loads and the focused skills it adds when the evidence requires a complete workflow, diagnosis, runtime observation, source tracing, or prompt-contract review.

```mermaid
classDiagram
    direction LR

    class DevVerifier {
        <<Agent>>
    }
    class test-strategy {
        <<SKILL.md>>
        <<Agent Skill>>
        +select-and-run-tests()
        +coverage-principles
    }
    class review-structured-artifact {
        <<SKILL.md>>
        <<Cross-group>>
    }
    class structured-explanation {
        <<SKILL.md>>
        <<Cross-group>>
    }
    class verify-end-to-end-workflow {
        <<SKILL.md>>
        <<Agent Skill>>
        +evidence-handoff-and-commit-authority
    }
    class analyze-root-cause {
        <<SKILL.md>>
        <<Agent Skill>>
    }
    class collect-runtime-evidence {
        <<SKILL.md>>
        <<Agent Skill>>
    }
    class trace-code-execution {
        <<SKILL.md>>
        <<Agent Skill>>
    }
    class review-prompt-contracts {
        <<SKILL.md>>
        <<Agent Skill>>
    }

    DevVerifier o--> test-strategy
    DevVerifier o--> review-structured-artifact
    DevVerifier o--> structured-explanation
    DevVerifier o..> verify-end-to-end-workflow : when confidence depends on a complete real workflow
    DevVerifier o..> analyze-root-cause : when a verification check fails
    DevVerifier o..> collect-runtime-evidence : when static checks cannot establish behavior
    DevVerifier o..> trace-code-execution : when an outcome must be connected to source control flow
    DevVerifier o..> review-prompt-contracts : when verification depends on a model-facing evaluator
```

### Scenario: Diagnosing Runtime Behavior

This scenario shows the discovery, testing, diagnosis, tracing, and explanation skills Dev Runtime Diagnostician uses to establish a mechanism-level cause. Runtime collection and careful coding are loaded only when observation or bounded instrumentation is required.

```mermaid
classDiagram
    direction LR

    class DevRuntimeDiagnostician {
        <<Agent>>
    }
    class code-discovery {
        <<SKILL.md>>
        <<Cross-group>>
        +discover-code-context(requested-work)
        +determine-change-scope(discovered-context)
        +contract-authority-rules
        +discovery-boundaries
    }
    class test-strategy {
        <<SKILL.md>>
        <<Agent Skill>>
        +select-and-run-tests()
        +coverage-principles
    }
    class analyze-root-cause {
        <<SKILL.md>>
        <<Agent Skill>>
    }
    class trace-code-execution {
        <<SKILL.md>>
        <<Agent Skill>>
    }
    class structured-explanation {
        <<SKILL.md>>
        <<Cross-group>>
    }
    class collect-runtime-evidence {
        <<SKILL.md>>
        <<Agent Skill>>
    }
    class careful-coding {
        <<SKILL.md>>
        <<Cross-group>>
        +confirm-work-before-coding()
        +validate-authorized-contract()
        +execute-goal-driven-loop()
    }

    DevRuntimeDiagnostician o--> code-discovery
    DevRuntimeDiagnostician o--> test-strategy
    DevRuntimeDiagnostician o--> analyze-root-cause
    DevRuntimeDiagnostician o--> trace-code-execution
    DevRuntimeDiagnostician o--> structured-explanation
    DevRuntimeDiagnostician o..> collect-runtime-evidence : when source cannot establish runtime state
    DevRuntimeDiagnostician o..> careful-coding : when diagnosis changes instrumentation or code
```

### Scenario: Reviewing A Prompt Contract

This scenario shows the prompt-specific and structured-review skills Dev Prompt Reviewer always loads.

```mermaid
classDiagram
    direction LR

    class DevPromptReviewer {
        <<Agent>>
    }
    class review-prompt-contracts {
        <<SKILL.md>>
        <<Agent Skill>>
    }
    class review-structured-artifact {
        <<SKILL.md>>
        <<Cross-group>>
    }

    DevPromptReviewer o--> review-prompt-contracts
    DevPromptReviewer o--> review-structured-artifact
```

PROJECT.yaml records organise-project-files once in shared_agent_skills, and generated AGENTS.md tells every Agent to load it when the Agent must choose or audit the location of a project file or directory. The scenarios therefore do not repeat that project-wide route as role-specific arrows.

### Scenario: An Investigation Needs More Evidence

This scenario shows how diagnosis and tracing skills add runtime evidence only when source analysis cannot establish the required fact. It also shows project-selected resource coordination for an end-to-end verification that triggers a claim event.

```mermaid
classDiagram
    direction LR

    class analyze-root-cause {
        <<SKILL.md>>
    }
    class trace-code-execution {
        <<SKILL.md>>
    }
    class collect-runtime-evidence {
        <<SKILL.md>>
    }
    class verify-end-to-end-workflow {
        <<SKILL.md>>
    }
    class ProjectSpecificDirectives["Project-specific directives"] {
        <<AGENTS.md>>
        <<routing>>
        +route resource coordination => resource-claim
    }
    class resource-claim {
        <<SKILL.md>>
        <<Cross-group>>
        +coordinate-shared-resource(resourceManifest)
        +acquire-claim(scope)
        +release-claim(claimId)
    }

    analyze-root-cause o..> trace-code-execution : when the cause depends on a source path
    analyze-root-cause o..> collect-runtime-evidence : when runtime facts are missing
    trace-code-execution o..> collect-runtime-evidence : when source cannot identify the actual path
    ProjectSpecificDirectives o..> resource-claim : when resource_coordination is resource-claim
    verify-end-to-end-workflow ..> resource-claim : when verification triggers a claim event
```

Verification returns evidence to the delivery owner. None of these scenarios assigns Commit-provider selection or provider-lifecycle authority to Dev Verifier.

## Skill Responsibilities

The group distinguishes complete review or diagnosis operations from supporting data that callers may need to understand.

| Skill | Public procedures or identity | Responsibility |
| --- | --- | --- |
| review-code-with-evidence | Review Code With Evidence; Evidence Packet; Synthesis Rules | Builds cited review evidence and synthesizes actionable findings. |
| test-strategy | Select And Run Tests; Coverage Principles | Chooses verification from changed behavior, risk, and project-native capabilities. |
| verify-end-to-end-workflow | Verify End To End Workflow; Evidence Handoff And Commit Authority | Verifies a complete real workflow and returns evidence without taking provider lifecycle authority. |
| analyze-root-cause | Analyze Root Cause | Establishes a mechanism-level cause before remediation. |
| collect-runtime-evidence | Collect Runtime Evidence | Collects bounded observations when source alone cannot establish runtime behavior. |
| trace-code-execution | Trace Code Execution | Connects entry points, branches, state changes, errors, and exits through source. |
| review-prompt-contracts | Review Prompt Contracts | Reviews model-facing instructions, tools, state, retries, outputs, and data boundaries. |

## Authoritative Inputs

The relationships and procedure boundaries are grounded in these Agent and skill definitions.

- [Dev Code Reviewer](../../agents/roles/dev-activities/dev-code-reviewer.role.yaml)
- [Dev Verifier](../../agents/roles/dev-activities/dev-verifier.role.yaml)
- [Dev Runtime Diagnostician](../../agents/roles/dev-activities/dev-runtime-diagnostician.role.yaml)
- [Dev Prompt Reviewer](../../agents/roles/dev-activities/dev-prompt-reviewer.role.yaml)
- [Review Code With Evidence](../../skills/review-code-with-evidence/SKILL.md)
- [Test Strategy](../../skills/test-strategy/SKILL.md)
- [Verify End To End Workflow](../../skills/verify-end-to-end-workflow/SKILL.md)
- [Analyze Root Cause](../../skills/analyze-root-cause/SKILL.md)
- [Collect Runtime Evidence](../../skills/collect-runtime-evidence/SKILL.md)
- [Trace Code Execution](../../skills/trace-code-execution/SKILL.md)
- [Review Prompt Contracts](../../skills/review-prompt-contracts/SKILL.md)
- [Careful Coding](../../skills/careful-coding/SKILL.md)
- [Code Comments](../../skills/code-comments/SKILL.md)
- [Code Discovery](../../skills/code-discovery/SKILL.md)
- [Organise Project Files](../../skills/organise-project-files/SKILL.md)
- [Review Structured Artifact](../../skills/review-structured-artifact/SKILL.md)
- [Structured Explanation](../../skills/structured-explanation/SKILL.md)
- [Resource Claim](../../skills/resource-claim/SKILL.md)
