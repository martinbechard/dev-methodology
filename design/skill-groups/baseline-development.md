# Baseline Development Skill Group

## Scope

Baseline Development contains practices that Agents reference by exact skill name across ordinary implementation, design, review, and explanation work.

The shared notation and cross-group markers are defined in [Object-Oriented Skill Group Models](../object-oriented-skill-group-models.md).

## Current Design

```mermaid
classDiagram
    direction LR

    class DevCoder {
        <<Agent class>>
    }

    class ProjectOrganiser {
        <<Agent class>>
    }

    class DevArtifactReviewer {
        <<Agent class>>
    }

    namespace BaselineDevelopment {
        class CarefulCoding {
            <<SKILL.md>>
            <<Agent Skill>>
            +skill careful-coding
        }

        class CodeComments {
            <<SKILL.md>>
            <<Agent Skill>>
            +skill code-comments
        }

        class CodeDiscovery {
            <<SKILL.md>>
            <<Agent Skill>>
            +skill code-discovery
        }

        class TestDrivenDevelopment {
            <<SKILL.md>>
            <<Agent Skill>>
            +skill test-driven-development
        }

        class StructuredDesign {
            <<SKILL.md>>
            <<Agent Skill>>
            +skill structured-design
        }

        class StructuredExplanation {
            <<SKILL.md>>
            <<Agent Skill>>
            +skill structured-explanation
        }

        class OrganiseProjectFiles {
            <<SKILL.md>>
            <<Agent Skill>>
            +skill organise-project-files
        }

        class ReviewStructuredArtifact {
            <<SKILL.md>>
            <<Agent Skill>>
            +skill review-structured-artifact
        }

        class FixExplanation {
            <<SKILL.md>>
            <<Agent Skill>>
            +skill fix-explanation
        }
    }

    class DocumentationPageVerify {
        <<SKILL.md>>
        <<Cross-group>>
        +skill documentation-page-verify
    }

    DevCoder --> CarefulCoding : references by name
    DevCoder --> CodeComments : references by name
    DevCoder --> CodeDiscovery : references by name
    DevCoder --> TestDrivenDevelopment : conditional name reference
    DevCoder --> OrganiseProjectFiles : references by name
    DevCoder --> FixExplanation : references by name
    ProjectOrganiser --> StructuredDesign : references by name
    ProjectOrganiser --> StructuredExplanation : references by name
    ProjectOrganiser --> OrganiseProjectFiles : references by name
    DevArtifactReviewer --> ReviewStructuredArtifact : references by name
    CodeComments --> StructuredExplanation : invokes by skill name
    FixExplanation --> StructuredExplanation : invokes by skill name
    StructuredExplanation --> StructuredDesign : invokes by skill name when needed
    ReviewStructuredArtifact --> DocumentationPageVerify : invokes by skill name
```

Dev Coder names careful-coding for every execution and test-driven-development under a condition. code-comments and fix-explanation directly invoke structured-explanation as a Peer Skill.

The cross-group documentation-page-verify node makes the current verification dependency visible without moving that skill out of Project Setup.

## Authoritative Inputs

- [Dev Coder](../../agents/roles/dev-activities/dev-coder.role.yaml)
- [Project Organiser](../../agents/roles/project-setup/project-organiser.role.yaml)
- [Careful Coding](../../skills/careful-coding/SKILL.md)
- [Code Comments](../../skills/code-comments/SKILL.md)
- [Code Discovery](../../skills/code-discovery/SKILL.md)
- [Test-Driven Development](../../skills/test-driven-development/SKILL.md)
- [Structured Design](../../skills/structured-design/SKILL.md)
- [Structured Explanation](../../skills/structured-explanation/SKILL.md)
- [Organise Project Files](../../skills/organise-project-files/SKILL.md)
- [Review Structured Artifact](../../skills/review-structured-artifact/SKILL.md)
- [Fix Explanation](../../skills/fix-explanation/SKILL.md)
- [Documentation Page Verify](../../skills/documentation-page-verify/SKILL.md)
