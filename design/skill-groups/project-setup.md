# Project Setup Skill Group

## Scope

Project Setup owns technology detection and project configuration. It uses documentation and placement skills from their primary groups rather than making those skills part of setup.

The applied-model conventions are defined in [Object-Oriented Skill Group Models](../object-oriented-skill-group-models.md#2-applied-model-legend).

## Design

The design keeps technology detection and project configuration as direct Project Setup skills. Documentation routing, documentation bootstrap, page verification, and file placement remain Cross-group dependencies.

```mermaid
classDiagram
    direction LR

    class ProjectConfigurator {
        <<Agent>>
    }

    class ProjectBootstrapper {
        <<Agent>>
    }

    namespace ProjectSetup {
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

    class AgentsGuidance {
        <<AGENTS.md>>
    }

    ProjectConfigurator o--> detect-technology-skills
    ProjectConfigurator o--> create-project-configuration
    ProjectConfigurator o--> route-documentation-work
    ProjectConfigurator o--> verify-documentation-page
    ProjectConfigurator o..> bootstrap-project-documentation : when documentation or routing structure is missing
    ProjectConfigurator o..> organise-project-files : when an unfixed project path must be chosen

    ProjectBootstrapper o--> route-documentation-work
    ProjectBootstrapper o--> bootstrap-project-documentation
    ProjectBootstrapper o..> organise-project-files : when an unfixed project path must be chosen

    note for AgentsGuidance "AGENTS.md names each confirmed technology skill directly"
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
