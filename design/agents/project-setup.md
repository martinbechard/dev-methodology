# Project Setup Skill Group

## Scope

Project Setup owns technology detection and project configuration. It uses documentation and placement skills from their primary groups rather than making those skills part of setup.

The applied-model conventions are defined in [Object-Oriented Skill Group Models](../object-oriented-skill-group-models.md#2-applied-model-legend).

## Design

Project Setup supplies the detection and configuration capabilities used to establish project guidance. Its Agents also use Documentation Methodology and Baseline Development skills for documentation structure, verification, and file placement.

### Overall Agent And Skill Group Dependencies

The overall view shows the two Project Setup Agents and the Skill Groups from which they obtain their capabilities.

```mermaid
classDiagram
    direction LR

    namespace ProjectSetupAgents["Project Setup Agents"] {
        class ProjectConfigurator {
            <<Agent>>
        }
        class ProjectBootstrapper {
            <<Agent>>
        }
    }

    class ProjectSetup["Project Setup"] {
        <<Skill Group>>
    }
    class DocumentationMethodology["Documentation Methodology"] {
        <<Skill Group>>
    }
    class BaselineDevelopment["Baseline Development"] {
        <<Skill Group>>
    }

    ProjectConfigurator --> ProjectSetup
    ProjectConfigurator --> DocumentationMethodology
    ProjectConfigurator ..> BaselineDevelopment : when an unfixed project path must be chosen
    ProjectBootstrapper --> DocumentationMethodology
    ProjectBootstrapper ..> BaselineDevelopment : when an unfixed project path must be chosen
```

### Scenario: Configuring A Project

This scenario shows the skills Project Configurator loads to detect applicable technology, write project configuration, route documentation work, and verify the generated guidance.

```mermaid
classDiagram
    direction LR

    class ProjectConfigurator {
        <<Agent>>
    }

    class detect-technology-skills {
        <<SKILL.md>>
        <<Agent Skill>>
        +detect-technology-skills()
    }

    class create-project-configuration {
        <<SKILL.md>>
        <<Agent Skill>>
        +configure-project-agents-and-skills()
        +render-project-guidance()
        +verify-project-configuration()
    }

    class route-documentation-work {
        <<SKILL.md>>
        <<Cross-group>>
    }

    class bootstrap-project-documentation {
        <<SKILL.md>>
        <<Cross-group>>
    }

    class verify-documentation-page {
        <<SKILL.md>>
        <<Cross-group>>
    }

    class organise-project-files {
        <<SKILL.md>>
        <<Cross-group>>
        +choose-project-file-placement()
    }

    ProjectConfigurator o--> detect-technology-skills
    ProjectConfigurator o--> create-project-configuration
    ProjectConfigurator o--> route-documentation-work
    ProjectConfigurator o--> verify-documentation-page
    ProjectConfigurator o..> bootstrap-project-documentation : when documentation or routing structure is missing
    ProjectConfigurator o..> organise-project-files : when an unfixed project path must be chosen
```

create-project-configuration writes the resulting AGENTS.md guidance. That output is not drawn as a loading dependency because the Project Configurator produces the file rather than consuming it through the relationship.

### Scenario: Bootstrapping A Project

This scenario shows how Project Bootstrapper combines documentation routing and bootstrap skills, adding file-placement guidance only when the destination is not already fixed.

```mermaid
classDiagram
    direction LR

    class ProjectBootstrapper {
        <<Agent>>
    }

    class route-documentation-work {
        <<SKILL.md>>
        <<Cross-group>>
    }

    class bootstrap-project-documentation {
        <<SKILL.md>>
        <<Cross-group>>
    }

    class organise-project-files {
        <<SKILL.md>>
        <<Cross-group>>
        +choose-project-file-placement()
    }

    ProjectBootstrapper o--> route-documentation-work
    ProjectBootstrapper o--> bootstrap-project-documentation
    ProjectBootstrapper o..> organise-project-files : when an unfixed project path must be chosen
```

## Skill Responsibilities

The two direct skills separate repository detection from configuration authoring and verification.

| Skill | Public procedures | Responsibility |
| --- | --- | --- |
| detect-technology-skills | Detect Technology Skills | Detects source-backed technology and domain skills for each configured folder. |
| create-project-configuration | Configure Project Agents And Skills; Render Project Guidance; Verify Project Configuration | Creates or updates PROJECT.yaml, renders AGENTS.md guidance, and validates the resulting configuration. |

## Authoritative Inputs

The relationships and procedure boundaries are grounded in these Agent and skill definitions.

- [Project Configurator](../../agents/roles/project-setup/project-configurator.role.yaml)
- [Project Bootstrapper](../../agents/roles/project-setup/project-bootstrapper.role.yaml)
- [Detect Technology Skills](../../skills/detect-technology-skills/SKILL.md)
- [Create Project Configuration](../../skills/create-project-configuration/SKILL.md)
- [Bootstrap Project Documentation](../../skills/bootstrap-project-documentation/SKILL.md)
- [Verify Documentation Page](../../skills/verify-documentation-page/SKILL.md)
- [Organise Project Files](../../skills/organise-project-files/SKILL.md)
- [Route Documentation Work](../../skills/route-documentation-work/SKILL.md)
