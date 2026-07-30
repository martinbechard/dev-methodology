# Project Setup Skill Group

## Scope

Project Setup owns technology detection and project configuration. It uses documentation and placement skills from their primary groups rather than making those skills part of setup.

The shared notation and recommendation boundary are defined in [Object-Oriented Skill Group Models](../object-oriented-skill-group-models.md).

## Current Design

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
        }

        class create-project-configuration {
            <<SKILL.md>>
            <<Agent Skill>>
        }
    }

    class development-methodology {
        <<SKILL.md>>
        <<Cross-group>>
    }

    class documentation-bootstrap {
        <<SKILL.md>>
        <<Cross-group>>
    }

    class documentation-page-verify {
        <<SKILL.md>>
        <<Cross-group>>
    }

    class organise-project-files {
        <<SKILL.md>>
        <<Cross-group>>
    }

    class AgentsGuidance {
        <<AGENTS.md>>
    }

    class ConfirmedTechnologySkills {
        <<Selected SKILL.md set>>
    }

    ProjectConfigurator o--> detect-technology-skills
    ProjectConfigurator o--> create-project-configuration
    ProjectConfigurator o--> development-methodology
    ProjectConfigurator o--> documentation-page-verify
    ProjectConfigurator o..> documentation-bootstrap : when documentation or routing structure is missing
    ProjectConfigurator o..> organise-project-files : when an unfixed project path must be chosen

    ProjectBootstrapper o--> development-methodology
    ProjectBootstrapper o--> documentation-bootstrap
    ProjectBootstrapper o..> organise-project-files : when an unfixed project path must be chosen

    AgentsGuidance o--> ConfirmedTechnologySkills
```

Project Configurator and Project Bootstrapper name their skills directly. The generated AGENTS.md also names each confirmed folder technology skill directly. The current definitions do not promise that all technology skills implement one shared procedure, so the selected set is not drawn as an injectable interface.

documentation-bootstrap, documentation-page-verify, and development-methodology belong to Documentation Methodology. organise-project-files belongs to Baseline Development. Their Cross-group nodes expose current setup use without changing primary ownership.

## Skill Recommendations

| Skill | Current source boundary | Recommendation | Reason |
| --- | --- | --- | --- |
| detect-technology-skills | Workflow performs detection; Operation Selection and Evidence Model define dispatch and interpretation rules. | Keep the skill name. Rename Workflow to Detect Technology Skills. | The skill name already states a cohesive operation, and the matching heading gives callers an explicit procedure boundary. |
| create-project-configuration | Setup Contract, Scope, Workflow, and Verification combine configuration decisions, PROJECT.yaml authoring, AGENTS.md rendering, and validation. | Keep the skill name. Introduce Configure Project Agents And Skills, Render Project Guidance, and Verify Project Configuration as operation headings. | The package contains several related operations. Named headings let another skill refer to the required part without treating the complete package as one create call. |

## Authoritative Inputs

- [Project Configurator](../../agents/roles/project-setup/project-configurator.role.yaml)
- [Project Bootstrapper](../../agents/roles/project-setup/project-bootstrapper.role.yaml)
- [Detect Technology Skills](../../skills/detect-technology-skills/SKILL.md)
- [Create Project Configuration](../../skills/create-project-configuration/SKILL.md)
- [Documentation Bootstrap](../../skills/documentation-bootstrap/SKILL.md)
- [Documentation Page Verify](../../skills/documentation-page-verify/SKILL.md)
- [Organise Project Files](../../skills/organise-project-files/SKILL.md)
- [Development Methodology](../../skills/development-methodology/SKILL.md)
