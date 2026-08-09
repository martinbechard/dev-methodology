# Terminology Standard

This standard defines preferred terms for software-development work. Use the same preferred term for the same concept throughout an Artifact. Preserve source-native language when it is an exact identifier, schema, command, quotation, external product name, or retained Evidence.

## Preferred Terms

### Acceptance criterion

Definition: A measurable condition that an Artifact must satisfy before it can be accepted.

### Agent

Definition: In an AI system, a software component that uses a model, instructions, context, and tools to pursue a goal within delegated authority.

### Agent harness

Definition: Software that supplies the runtime, tools, context, and lifecycle controls needed to run arbitrary Agent Workflows.

### Artifact

Definition: A durable work product that a person or software process creates, changes, reviews, or evaluates.

### Backlog

Definition: A collection of Work items maintained for planning and coordination.

### Business scenario

Definition: A high-level description of a business problem, its context and participants, and the desired business outcome.

### Campaign

Definition: A coordinated, bounded set of Evaluation runs performed for one evaluation objective or release baseline.

Use for:

- Coordinating selected Evaluation runs. The stable collection available for selection is an Evaluation portfolio, not a Campaign.

### Contract validation

Definition: A check that supplied data or an Artifact satisfies explicit input rules such as a schema, format, type, or allowed value.

### Defect

Definition: A reproducible difference between required behavior and observed behavior.

### Evaluation

Definition: In an AI-controlled Workflow, an assessment that applies defined criteria to an Artifact and produces an Evaluation result, normally supported by Evidence. An Evaluation can occur during software testing or during the operation of an agentic Workflow.

### Evaluation case

Definition: One specified input and expected or assessable behavior within an Evaluation, while its target configuration and criteria remain fixed.

### Evaluation decision

Definition: A normalized decision produced by an Evaluation after its required checks and judgments complete.

### Evaluation portfolio

Definition: A governed, stable collection of Evaluation suites available for selection across objectives or releases.

### Evaluation result

Definition: The recorded decision, label, or score produced by an Evaluation, normally with supporting Evidence.

### Evaluation run

Definition: One execution of an Evaluation against a specified target configuration, using selected Evaluation cases.

### Evaluation suite

Definition: A named collection of related Evaluations.

### Evaluator agent

Definition: An Agent that performs an Evaluation.

### Evidence

Definition: Retained information that supports or contradicts a claim about an Artifact, action, or result.

### Provider

Definition: In software design, an implementation of an interface that supplies a concrete service behind an abstraction, commonly selected or constructed through a Factory.

Use for:

- A concrete implementation selected through an interface or Factory, such as a file-backed implementation of a persistence interface.

### Requirement

Definition: A documented capability, behavior, quality, or constraint that an Artifact must satisfy.

### Review

Definition: An examination of an Artifact that identifies findings and recommendations without changing the Artifact.

### Skill

Definition: In an AI system, a reusable instruction package that teaches an Agent how to perform a bounded kind of work.

### Test

Definition: A repeatable check that compares observed behavior with an expected result.

### Test case

Definition: A specification of the preconditions, inputs, actions, expected results, and postconditions for one Test.

### Test condition

Definition: A testable aspect of a system or Artifact used to derive Test cases.

### Test fixture

Definition: Controlled data, files, configuration, or environment state that establishes the starting conditions for a Test.

### Test harness

Definition: Software that prepares and executes Tests in a controlled environment.

### Test report

Definition: A retained summary of the scope, environment, results, Evidence, and limitations of one or more Test runs.

### Test result

Definition: The recorded outcome and supporting Evidence produced by executing one Test case.

### Test run

Definition: One execution of selected Test cases or Test suites in a defined environment.

### Test suite

Definition: A named, stable collection of related Test cases that are selected and executed together.

Avoid:

- Campaign: Do not use for the stable collection of Test cases. A Campaign is the coordinated set of Evaluation runs performed for one objective or release baseline.

### Use case

Definition: A specification of system behavior through interactions with actors that achieve a goal.

### User story

Definition: An informal and evolving expression of a user need used in agile planning.

### Verification

Definition: An Evidence-backed check that a claimed result or behavior satisfies its specified Requirements and Acceptance criteria.

### Work item

Definition: A bounded unit of planned work with an objective, ownership, state, and completion conditions.

Avoid:

- Provider: Do not use for a Work item. A Provider implements an interface; a Work item is the unit being planned, tracked, or delivered.

### Workflow

Definition: A defined sequence of activities, decisions, and handoffs that produces an intended result.
