# Procedure: Technical Stack Rules

## 1. Purpose and Scope

- **RULE:** This document defines the standard technical stack and associated libraries/tools to be used for development within this project.
  - **BECAUSE:** It ensures consistency across the project's technology choices, simplifying development, deployment, and maintenance.
    - **BECAUSE:** A standardized stack reduces the cognitive load for developers, as they only need to be familiar with a defined set of tools.
      - **BECAUSE:** Consistency facilitates easier onboarding, knowledge sharing, and collaboration.
    - **BECAUSE:** It simplifies dependency management and build processes.

## 2. Core Backend Technologies

- **RULE:** NodeJS **MUST** be used as the primary runtime environment for hosting applications.

  - **BECAUSE:** It provides a widely adopted, event-driven, non-blocking I/O model suitable for building scalable network applications.
    - **BECAUSE:** Leveraging JavaScript/TypeScript across the stack simplifies development.

- **RULE:** Express **MUST** be used if HTTP endpoints need to be exposed by a NodeJS application.

  - **BECAUSE:** Express is a minimal and flexible NodeJS web application framework, providing a robust set of features for web and mobile applications.
    - **BECAUSE:** It is the de facto standard for NodeJS web servers, with extensive community support and middleware available.

- **RULE:** pnpm **MUST** be assumed and used as the package manager for NodeJS projects.
  - **BECAUSE:** pnpm offers efficient disk space usage and faster installation times compared to npm or yarn through its content-addressable store and symlinking strategy.
    - **BECAUSE:** Standardizing on one package manager ensures consistent dependency resolution and lockfile management across the team.

## 3. Common Libraries and Tools

- **RULE:** TypeScript **MUST** be used for all JavaScript development.

  - **BECAUSE:** TypeScript adds static typing to JavaScript, improving code quality, maintainability, and developer productivity by catching errors during development.
    - **BECAUSE:** Static types provide better tooling support (autocompletion, refactoring) and make large codebases easier to manage.

- **RULE:** Axios **MUST** be used for making HTTP requests to external systems or APIs.

  - **BECAUSE:** Axios provides a simple, promise-based API for making HTTP requests from both the browser and NodeJS, with features like request/response interception and automatic JSON data transformation.
    - **BECAUSE:** Standardizing on a single HTTP client simplifies patterns for API interaction.

- **RULE:** Zod **MUST** be used for data validation, particularly for validating API request/response schemas and environment variables.

  - **BECAUSE:** Zod provides a TypeScript-first schema declaration and validation library, ensuring data integrity with clear, composable schemas and excellent type inference.
    - **BECAUSE:** It helps prevent runtime errors caused by invalid data structures.

- **RULE:** Prisma **MUST** be used as the Object-Relational Mapper (ORM) for database access.

  - **BECAUSE:** Prisma offers a type-safe database client, declarative schema migrations, and an intuitive data modeling language, improving developer experience and database interaction safety.
    - **BECAUSE:** It generates a type-safe client based on the database schema, reducing runtime errors related to database operations.

- **RULE:** PostgreSQL **MUST** be used as the relational database system.

  - **BECAUSE:** PostgreSQL is a powerful, open-source object-relational database system with a strong reputation for reliability, feature robustness, and performance.
    - **BECAUSE:** It supports complex queries, transactions, and various data types, making it suitable for a wide range of applications.

- **RULE:** Redis **MUST** be used for caching purposes where applicable.

  - **BECAUSE:** Redis is an in-memory data structure store, often used as a cache, message broker, and database, known for its high performance.
    - **BECAUSE:** Caching frequently accessed data can significantly improve application performance and reduce load on primary data stores.

- **RULE:** dotenv **MUST** be used for managing environment variables in development environments.

  - **BECAUSE:** dotenv loads environment variables from a `.env` file into `process.env`, providing a simple way to manage configuration separately from code, following Twelve-Factor App principles.
    - **BECAUSE:** It prevents sensitive configuration (like API keys) from being hardcoded in the source repository.

- **RULE:** Mermaid **MUST** be used for creating diagrams (e.g., flowcharts, sequence diagrams) within Markdown documentation.

  - **BECAUSE:** Mermaid allows diagrams to be generated from text-based descriptions, making them easy to version control and update alongside documentation.
    - **BECAUSE:** It integrates well with Markdown rendering tools.

- **RULE:** Each top-level Mermaid diagram **MUST** be defined in its own separate `.md` artifact.

  - **BECAUSE:** This promotes modularity and reusability of diagrams.
    - **BECAUSE:** It makes diagrams easier to find, reference, and maintain independently.

- **RULE:** Jest **MUST** be used as the primary testing framework.

  - **BECAUSE:** Jest is a popular JavaScript testing framework with a focus on simplicity, providing features like built-in mocking, code coverage, and parallel test execution.
    - **BECAUSE:** Standardizing on Jest ensures consistent testing practices and tooling across the project.

- **RULE:** Developers **MUST** review `tsconfig.json` and `package.json` to understand Jest-related configurations and import conventions (e.g., path aliases configured for Jest).

  - **BECAUSE:** Jest requires specific configuration (often via `tsconfig.json` for TypeScript projects and `jest.config.js` or `package.json`) to work correctly, especially regarding module resolution and path aliases.
    - **BECAUSE:** Understanding these settings is crucial for writing tests that correctly import project modules.

- **RULE:** The `package.json` file **MUST** include a `build:debug` script that creates a development build including source maps.
  - **EXAMPLE:** `"build:debug": "tsc --sourceMap"` or `"build:debug": "webpack --mode development --devtool source-map"` (adjust command based on build tool)
  - **BECAUSE:** A dedicated debug build script ensures developers can easily generate builds suitable for debugging with proper source mapping.
    - **BECAUSE:** Source maps are essential for debugging transpiled code (like TypeScript) effectively in the browser or NodeJS runtime.

## 4. Review and Updates

- **RULE:** This document **SHOULD** be reviewed periodically and updated as technology choices evolve or new requirements emerge.
  - **BECAUSE:** Keeping the technical stack documentation current ensures it remains an accurate guide for the team.
    - **BECAUSE:** Technology landscapes change, and the project's needs may necessitate adopting new tools or phasing out old ones.
