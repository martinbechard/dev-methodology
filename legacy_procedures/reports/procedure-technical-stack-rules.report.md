# Migration Report: Technical Stack Rules

## Source

- Legacy procedure: [procedure-technical-stack-rules.md](../procedure-technical-stack-rules.md)

## Purpose And Scope

This procedure fixes one application's implementation stack: NodeJS, Express,
pnpm, TypeScript, Axios, Zod, Prisma, PostgreSQL, Redis, dotenv, Mermaid, and
Jest. It also requires a debug build script and periodic maintenance of that
decision. Its durable value is not the named dependency list. It is the
discipline of recording technology decisions, using the chosen toolchain
consistently, validating data at trust boundaries, and verifying the actual
build and test configuration before changing it.

The live bundle deliberately keeps framework and persistence skills separate
and routes project-wide technology choices to an architecture artifact and
repository-local instructions. The closest live destinations are
[create-architecture](../../skills/create-architecture/SKILL.md), its
[architecture template](../../skills/development-methodology/assets/templates/architecture-template.md),
[typescript-strict](../../skills/typescript-strict/SKILL.md),
[typescript-esm](../../skills/typescript-esm/SKILL.md),
[api-routes](../../skills/api-routes/SKILL.md), [jest](../../skills/jest/SKILL.md),
and [node-cli](../../skills/node-cli/SKILL.md). PostgreSQL support is currently
intentionally specific to Drizzle rather than Prisma.

## Worthwhile Durable Guidance

- Make project-wide technology choices explicit, source-backed architectural
  decisions; name both required and disallowed technologies when that
  constraint matters.
- Treat the runtime, language, package manager and lockfile, build scripts,
  test configuration, module configuration, persistence, and deployment
  configuration as a compatible system rather than independent preferences.
- Validate and narrow data at HTTP, configuration, persistence, and other
  real trust boundaries before relying on it in typed code.
- Keep secrets and deployment-specific values out of source; document the
  repository's development configuration and validation path without making a
  particular dotenv package universal.
- Review actual package metadata and compiler/test configuration before
  changing imports, aliases, transforms, build behavior, or test execution.
- Keep editable diagram source under version control and use a diagram only
  when it materially clarifies a relationship.
- Revisit stack choices when source evidence shows a changed runtime,
  dependency, security, deployment, or operational requirement.

## Mapping

| Procedure point | Destination skill(s) or agent(s) | Current coverage | Recommendation |
| --- | --- | --- | --- |
| One standard stack, maintained for consistency, onboarding, dependencies, and builds | Architecture artifact; target-repository AGENTS.md; create-architecture | Partial | Keep the decision-recording principle in the architecture route. Put the approved stack itself, compatibility range, and ownership in the target repository. |
| NodeJS is the application runtime | Target-repository architecture and AGENTS.md; Node CLI when the work is a CLI | Correctly project-specific | Do not add a general Node application-runtime rule; CLI guidance is not server-runtime selection guidance. |
| Express exposes Node HTTP endpoints | Target-repository architecture and AGENTS.md; API Routes | Correctly project-specific | API Routes owns portable HTTP-boundary behavior, not framework selection. Do not add Express to it. |
| pnpm is the package manager | Target-repository architecture, package metadata, lockfile, and AGENTS.md | Missing by design | Record the selected package manager, lockfile, install command, and any workspace constraints locally. Do not make pnpm a bundle default. |
| TypeScript is mandatory for JavaScript work | TypeScript Strict; TypeScript ESM; target-repository architecture | Partial | The two TypeScript skills cover strict typing and module behavior. Keep language adoption policy local because supported targets include non-TypeScript stacks. |
| Axios is the external HTTP client | Target-repository architecture and integration conventions; API Routes for server boundaries | Missing by design | Do not create an Axios skill or mandate a client. A project may choose fetch, a generated client, or another transport library. |
| Zod validates request, response, and environment schemas | TypeScript Strict; API Routes; target-repository validation conventions | Partial | Keep validation and narrowing at real unknown-data boundaries. Do not prescribe Zod; a concrete validator and schema ownership belong to the project. |
| Prisma is the ORM and PostgreSQL the relational store | Target-repository architecture; Postgres Drizzle when the project uses Drizzle | Correctly project-specific | Do not add Prisma to Postgres Drizzle or create a Prisma agent from this single legacy rule. Add a focused persistence skill only when repeated Prisma work establishes a distinct reusable workflow. |
| Redis is used for applicable caching | Target-repository architecture and performance/caching design | Missing by design | Preserve the decision rule: cache only for an evidenced workload and record invalidation, ownership, and failure behavior locally. Do not impose Redis or caching globally. |
| dotenv manages development environment variables | Node CLI; target-repository configuration and secret-handling guidance | Partial | Node CLI already routes environment-variable work. Add no package rule; project guidance must specify secret storage, .env handling, and deployment configuration. |
| Mermaid is used for Markdown diagrams | Architecture/template authoring; documentation-page-verifier | Complete | Keep Mermaid as the default editable source where diagrams are useful. The template and verifier already preserve editable source and diagram-purpose rules. |
| Each top-level Mermaid diagram has a separate Markdown artifact | Architecture/template authoring; project-local documentation conventions | Not portable and conflicts with live templates | Omit. The live templates place a diagram immediately after the section it clarifies; separate artifacts are only appropriate when a repository's publishing or reuse needs justify them. |
| Jest is the primary test framework | Jest; target-repository architecture and package metadata | Correctly project-specific | Jest skill owns Jest work once selected. Do not displace Vitest or create a universal runner default. |
| Inspect tsconfig.json and package.json for Jest import and alias behavior | Jest; TypeScript ESM | Partial | Add a concise configuration-discovery rule to Jest for config-sensitive test changes. Exact config filenames, aliases, and transformers remain local. |
| A build:debug script emits source maps | Target-repository package metadata, build configuration, and architecture | Missing by design | Keep only when the project's debugger, artifact, and deployment flow require it. The script name and build command are local conventions. |
| Periodically review stack choices | Target-repository architecture maintenance or backlog governance | Correctly project-specific | Record review triggers or cadence locally; do not impose a recurring review schedule on all bundle consumers. |

## Obsolete Or Project-Specific Guidance To Omit

- The mandatory NodeJS, Express, pnpm, TypeScript, Axios, Zod, Prisma,
  PostgreSQL, Redis, dotenv, Mermaid, and Jest selections. These are a product
  architecture decision, not a reusable methodology decision.
- Claims that Express, Axios, Prisma, Jest, or a specific package manager is
  universally the standard or best choice. They are time-sensitive and vary by
  runtime, team, compliance profile, and generated-client strategy.
- The fixed requirement for a separate Markdown file per top-level Mermaid
  diagram. It conflicts with the current templates' local-diagram rule and
  creates needless navigation overhead for many designs.
- The exact build:debug script name and TypeScript or webpack command. Debug
  artifact generation, source-map policy, bundler, and production exposure are
  repository-specific.
- A generic periodic-review mandate. The responsible project should choose
  review triggers, owner, evidence, and cadence.

## Precise Suggested Additions

### Jest

Under Guidance, add:

> Before changing tests whose execution, transforms, module resolution, path
> aliases, environment, or coverage behavior may be configuration-sensitive,
> inspect the repository's package scripts, Jest configuration, TypeScript
> compiler settings, and relevant resolver or transformer configuration.
> Treat those files as one execution boundary and verify with a focused test
> command after the change.

This is a narrow missing point: the Jest skill currently gives strong test
design and verification guidance but does not tell an agent to discover the
configuration that determines whether a test can execute.

### Create Architecture And Architecture Template

Under Create Architecture workflow step 2, add:

> For each required technology choice, identify its architectural role, source
> of configuration or version authority, compatibility boundary, and
> verification command. Record prohibited or approval-required alternatives
> only when repository evidence establishes them.

In the architecture template's Technology Stack section, add a TODO asking for
the package manager and lockfile, configuration owners, supported runtime or
toolchain versions where known, and the command or check that verifies the
stack is usable. This turns a dependency list into an actionable project
contract without naming a universal stack.

### No New Skill Or Agent

Do not add a technical-stack-rules skill, a stack-selection agent, or
library-specific Axios, Zod, Prisma, Redis, dotenv, or Express skills from
this procedure. The legacy rules provide one project profile, not a repeated,
customer-independent workflow. Existing stack skills should continue to
trigger only when the target project's evidence selects their technology.

## Conclusion

Retire this procedure as a distributed rule set. Transfer its approved-stack
list, package-manager policy, configuration examples, caching policy, and
debug-build convention into the former project's architecture documentation
and AGENTS.md. Preserve the portable core through two small improvements:
Jest should explicitly inspect the test execution configuration, and the
architecture route should record each project-selected technology's authority,
compatibility boundary, and verification. No new agent or fixed-stack skill is
recommended.
