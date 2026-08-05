# Baseline Development Skill Group

## Scope

Baseline Development contains practices that Agent definitions load by exact skill name across implementation, design, review, placement, and explanation work.

The applied-model conventions are defined in [Object-Oriented Skill Group Models](../object-oriented-skill-group-models.md#2-applied-model-legend).

## Design

The design keeps nine baseline responsibilities together. Multi-operation skills expose the procedure headings that Agents or other skills can reference, while single-operation skills use their skill identity as the operation.

```mermaid
classDiagram
    direction LR

    class DevCoder {
        <<Agent>>
    }

    class ProjectOrganiser {
        <<Agent>>
    }

    class StructuredArtifactReviewers {
        <<Agent superclass stand-in>>
    }

    namespace BaselineDevelopment {
        class careful-coding {
            <<SKILL.md>>
            <<Agent Skill>>
            +confirm-work-before-coding()
            +validate-authorized-contract()
            +execute-goal-driven-loop()
        }

        class code-comments {
            <<SKILL.md>>
            <<Agent Skill>>
            +write-structured-comments()
            +add-code-artifact-header()
            +document-public-constructs()
            +review-code-comments()
        }

        class code-discovery {
            <<SKILL.md>>
            <<Agent Skill>>
            +discover-code-context(requested-work)
            +determine-change-scope(discovered-context)
            +contract-authority-rules
            +discovery-boundaries
        }

        class test-driven-development {
            <<SKILL.md>>
            <<Agent Skill>>
            +run-red-green-refactor-loop()
        }

        class structured-design {
            <<SKILL.md>>
            <<Agent Skill>>
            +create-structured-design()
            +self-review-structured-design()
        }

        class structured-explanation {
            <<SKILL.md>>
            <<Agent Skill>>
            +create-structured-explanation()
        }

        class organise-project-files {
            <<SKILL.md>>
            <<Agent Skill>>
            +choose-project-file-placement()
        }

        class review-structured-artifact {
            <<SKILL.md>>
            <<Agent Skill>>
            +review-structured-artifact()
        }

        class explain-code-fix {
            <<SKILL.md>>
            <<Agent Skill>>
        }
    }

    class verify-documentation-page {
        <<SKILL.md>>
        <<Cross-group>>
    }

    class analyze-root-cause {
        <<SKILL.md>>
        <<Cross-group>>
    }

    DevCoder o--> careful-coding
    DevCoder o--> code-comments
    DevCoder o--> code-discovery
    DevCoder o--> explain-code-fix
    DevCoder o..> organise-project-files : when implementation creates a project file or directory
    DevCoder o..> test-driven-development : when executable tests should guide implementation

    ProjectOrganiser o--> organise-project-files
    ProjectOrganiser o--> structured-design
    ProjectOrganiser o--> structured-explanation

    StructuredArtifactReviewers o--> review-structured-artifact

    code-comments o..> structured-explanation : when writing a non-trivial comment block
    explain-code-fix o--> structured-explanation
    structured-explanation o..> structured-design : when an explanation needs system structure
    review-structured-artifact o--> verify-documentation-page
    test-driven-development o..> analyze-root-cause : when a test fails unexpectedly
```

## Skill Responsibilities

The group combines exact-name Agent Skills with explicit procedure boundaries for skills that contain several related operations.

| Skill | Public procedures or identity | Responsibility |
| --- | --- | --- |
| careful-coding | Confirm Work Before Coding; Validate Authorized Contract; Execute Goal-Driven Loop | Keeps implementation assumptions, contracts, scope, and verification explicit. |
| code-comments | Write Structured Comments; Add Code Artifact Header; Document Public Constructs; Review Code Comments | Creates and reviews code comments, required headers, and public API documentation. |
| code-discovery | Discover Code Context; Determine Change Scope | Gathers repository evidence and turns it into the smallest justified change or review boundary. Contract Authority and Boundaries remain shared data for both procedures. |
| test-driven-development | Run Red-Green-Refactor Loop | Guides implementation through executable failing and passing behavior. |
| structured-design | Create Structured Design; Self-Review Structured Design | Creates structured design artifacts and checks them against the same design contract. |
| structured-explanation | Create Structured Explanation | Organizes technical reasoning into evidence-backed explanations. |
| organise-project-files | Choose Project File Placement | Chooses and audits repository destinations from project guidance and taxonomy. |
| review-structured-artifact | Review Structured Artifact | Reviews structured artifacts through checklist-backed evidence and findings. |
| explain-code-fix | Explain Code Fix | Explains a completed code change and classifies the nature of the fix. |

## Authoritative Inputs

The relationships and procedure boundaries are grounded in these Agent and skill definitions.

- [Dev Coder](../../agents/roles/dev-activities/dev-coder.role.yaml)
- [Project Organiser](../../agents/roles/project-setup/project-organiser.role.yaml)
- [Dev Artifact Reviewer](../../agents/roles/dev-activities/dev-artifact-reviewer.role.yaml)
- [Dev Code Reviewer](../../agents/roles/dev-activities/dev-code-reviewer.role.yaml)
- [Dev Verifier](../../agents/roles/dev-activities/dev-verifier.role.yaml)
- [Dev Prompt Reviewer](../../agents/roles/dev-activities/dev-prompt-reviewer.role.yaml)
- [Dev Merge Coordinator](../../agents/roles/dev-activities/dev-merge-coordinator.role.yaml)
- [Careful Coding](../../skills/careful-coding/SKILL.md)
- [Code Comments](../../skills/code-comments/SKILL.md)
- [Code Discovery](../../skills/code-discovery/SKILL.md)
- [Test-Driven Development](../../skills/test-driven-development/SKILL.md)
- [Structured Design](../../skills/structured-design/SKILL.md)
- [Structured Explanation](../../skills/structured-explanation/SKILL.md)
- [Organise Project Files](../../skills/organise-project-files/SKILL.md)
- [Review Structured Artifact](../../skills/review-structured-artifact/SKILL.md)
- [Explain Code Fix](../../skills/explain-code-fix/SKILL.md)
- [Verify Documentation Page](../../skills/verify-documentation-page/SKILL.md)
- [Analyze Root Cause](../../skills/analyze-root-cause/SKILL.md)
