# Terminology Standard

This standard defines preferred terms for software development work. Use the same term for the same concept throughout an artifact.

## Preferred Terms

### Acceptance criterion

Definition: A measurable condition that a work product must satisfy before it can be accepted.

> Review note: Acceptance criterion clarity 5/5. Alternatives: acceptance condition 4/5; approval condition 3/5. Decision: Keep acceptance criterion because it directly connects the measurable condition to acceptance.
> User: Agreed

### Agent

Definition: A software participant that performs a defined role through instructions, tools, and delegated authority.

> Review note: Agent clarity 4/5. Alternatives: software actor 4/5; automated worker 3/5. Decision: Keep agent because it is the established name for a role that uses instructions, tools, and delegated authority.
> User: Let's be specific: I don't think software participant is a well-established usage. Let's call it software component
> Assistant: Agreed. Proposed definition: In an AI system, a software component that uses a model, instructions, context, and tools to pursue a goal within delegated authority.
> User: Agreed

### Artifact

Definition: A durable work product that a person or software process creates, changes, reviews, or evaluates.

> Review note: Artifact clarity 4/5. Alternatives: work product 5/5; deliverable 3/5. Decision: Change to work product because it is plain language and includes internal and external outputs.
> User: Agreed
> Assistant: Your later comments use Artifact as the defined concept, which conflicts with this proposed rename. I now recommend keeping Artifact and using it consistently in Requirement and Review. Work product can remain an explanatory alternative rather than the preferred term.
> User: I had Agreed with your proposal, you comment is unclear here out of contxt. I agree again that we keep your proposed definition of Artifact, and deal with the consequences in other sections accordingly
> Assistant: Understood. Keep Artifact as the preferred term with its current definition; do not rename it Work product. The accepted cleanup is to use Artifact consistently in Acceptance criterion, Requirement, and Review. My earlier rename recommendation should be removed when we resolve the comments.
> User: Agreed

### Defect

Definition: A reproducible difference between required behavior and observed behavior.

> Review note: Defect clarity 5/5. Alternatives: bug 4/5; fault 3/5. Decision: Keep defect because it is precise and applies beyond source code.
> User: Agreed

### Evaluation

Definition: A structured assessment that applies defined criteria to a target and produces evidence and a conclusion.

Use for:

- An assessment that can combine deterministic tests, semantic judgment, and human review.

> Review note: Evaluation clarity 5/5. Alternatives: assessment 4/5; appraisal 3/5. Decision: Keep evaluation because it clearly includes criteria, evidence, and a conclusion.
> User: too vague: in the context of AI-controlled workflows, an assessment that applies defined criteria to an artifact and produces a pass/fail result, normally with justifying evidence. An Evaluation can be part of a QA testing activity (ED: not sure of this wording) or it can happen at runtime as part of the software operation of an agentic workflow.
> Assistant: I agree with distinguishing test-time and runtime evaluations. Pass/fail is too narrow because an evaluation can produce a label or score. Proposed definition: In an AI-controlled workflow, an assessment that applies defined criteria to an artifact and produces an Evaluation result, normally supported by evidence. An Evaluation can occur during software testing or during the operation of an agentic workflow. OpenAI similarly defines an evaluation through testing criteria and a data-source configuration, with graders that can return labels or scores: [Evals](https://platform.openai.com/docs/api-reference/evals/deleteRun?lang=python) and [Graders](https://platform.openai.com/docs/api-reference/graders?api-mode=chat).
> User: Agreed

### Evidence

Definition: Retained information that supports or contradicts a claim about an artifact, action, or result.

> Review note: Evidence clarity 5/5. Alternatives: supporting information 4/5; proof 3/5. Decision: Keep evidence because it does not overstate the strength of the support.
> User: Agreed

### Evidence record

Definition: A durable structured artifact that identifies the evaluated claim, supporting evidence, outcome, and integrity information.

> Review note: Evidence record clarity 5/5. Alternatives: evidence package 4/5; receipt 3/5. Decision: Keep evidence record because it states both the content and its durable form without a metaphor.
> User: Misnomer. This is an Evaluation Result or Test Result (when the evaluation is part of a test suite) because the outcome is not evidence is the result of a judgement.
> Assistant: Agreed. Replace Evidence record with Evaluation result: the recorded decision or score produced by an Evaluation, normally with supporting evidence. Test result remains the corresponding term when a Test run executes a Test case. Keep Evidence record only if we later need a separate term for the durable container that stores evidence rather than the decision itself.
> User: Agreed

### Fixture

Definition: Controlled data, files, configuration, or environment state that establishes the starting conditions for a test.

> Review note: Fixture clarity 3/5. Alternatives: test fixture 5/5; test setup 4/5. Decision: Change to test fixture because the qualifier removes the non-testing meanings of fixture.
> User: Agreed

### Harness

Definition: Software that prepares, runs, observes, and closes a test or evaluation in a controlled environment.

> Review note: Harness clarity 3/5. Alternatives: test harness 5/5; test runner 4/5. Decision: Change to test harness because a runner can execute tests without owning preparation, observation, and closeout.
> User: No this is a Test Harness (as opposed to an agentic harness that can run an arbitrary agent workflow)
> Assistant: Agreed. Define Test harness and Agent harness separately. A Test harness prepares and executes tests in a controlled environment. An Agent harness supplies the runtime, tools, context, and lifecycle controls needed to run arbitrary agent workflows. The testing-specific use is consistent with the [ISTQB testing glossary](https://api.glossary.istqb.org/storage/help/R0uz58NqLzUz48LVUuyGSF76NFj4LHQazSs0GlNS.pdf).
> User: Agreed

### Judge

Definition: An evaluator that applies defined criteria to evidence and returns a verdict.

Use for:

- A deterministic evaluator, model evaluator, or human evaluator with an explicit decision role.

> Review note: Judge clarity 3/5. Alternatives: evaluator 5/5; reviewer 4/5. Decision: Change to evaluator because it describes the decision role without a courtroom metaphor.
> User: Humans are never referred to as Judges, they are perhaps QA analysts or other. I feel we should change the defintiion to be: an Agent that performs an evaluation
> Assistant: Agreed for this standard. Rename the term Evaluator agent and define it as an Agent that performs an Evaluation. Human participants remain QA analysts, reviewers, or expert evaluators according to their actual roles.
> User: Agreed

### Requirement

Definition: A documented capability, behavior, quality, or constraint that a work product must satisfy.

> Review note: Requirement clarity 5/5. Alternatives: specification 4/5; need 3/5. Decision: Keep requirement because a specification can contain many requirements, while a need can remain informal.
> User: we defined Artifact, we shouldn't talk about work product here.
> Assistant: Agreed if Artifact remains the preferred term. Proposed definition: A documented capability, behavior, quality, or constraint that an Artifact must satisfy.
> User: Agreed

### Review

Definition: An examination of a work product that identifies findings and recommendations without changing the reviewed target.

> Review note: Review clarity 5/5. Alternatives: inspection 4/5; assessment 4/5. Decision: Keep review because it is familiar and does not imply one specific review method.
> User: we did NOT define target, we should use artifact instead
> Assistant: Agreed. Proposed definition: An examination of an Artifact that identifies findings and recommendations without changing the Artifact.
> User: Agreed

### Scenario

Definition: A bounded situation that defines relevant starting conditions, an action or event, and the expected outcome.

> Review note: Scenario clarity 4/5. Alternatives: behavioral scenario 5/5; use case 3/5. Decision: Keep scenario because the definition supplies the behavioral boundary without restricting the term to user interactions.
> User: Agreed,but should we be using this definition for a Use Case when it describes one of the main usages of a system? User Story is when we loosely describe what a user wants to be ble to do in an agile context. And Scenario is either Test Scenario or Business Scenario - a Business scenario being even higher level than use cases or user stories. Test Scenarios are like realized use cases and more precise. It is probably worth finding clear differentiators for these different terms (without inventing anything i.e. based on common practice)
> Assistant: I recommend removing the unqualified Scenario entry. Define Business scenario as a high-level business problem, context, participants, and desired outcome; Use case as specified system behavior through interactions with actors; User story as an informal and evolving expression of a user need used in agile planning; and Test condition as a testable aspect used to design Test cases. Test scenario is common but less formally consistent, so we should define it only if the project needs a named level between a Use case and its Test cases. Sources: [The Open Group business scenarios](https://www.opengroup.org/architecture/togaf7-doc/arch/p4/bus_scen/bus_scen.htm), [OMG use cases](https://issues.omg.org/issues/UML25-435), [Agile Alliance user stories](https://agilealliance.org/glossary/user-stories/), and the [ISTQB testing glossary](https://api.glossary.istqb.org/storage/help/R0uz58NqLzUz48LVUuyGSF76NFj4LHQazSs0GlNS.pdf).
> User: Agreed

### Skill

Definition: A reusable instruction package that teaches an agent how to perform a bounded kind of work.

> Review note: Skill clarity 4/5. Alternatives: instruction package 4/5; capability 3/5. Decision: Keep skill because it names the reusable package, while capability names what an agent can do.
> User: Agreed, but we should quality: in the context of AI,
> Assistant: Agreed. Proposed definition: In an AI system, a reusable instruction package that teaches an Agent how to perform a bounded kind of work.
> User: Agreed

### Test

Definition: A repeatable check that compares observed behavior with an expected result.

> Review note: Test clarity 5/5. Alternatives: check 4/5; examination 3/5. Decision: Keep test because it clearly requires comparison with an expected result.
> User: Agreed

### Test case

Definition: One executable test with defined preconditions, inputs, actions, and expected results.

> Review note: Test case clarity 5/5. Alternatives: test specification 4/5; test scenario 3/5. Decision: Keep test case because it identifies one executable test, while a specification can define several cases.
> User: No, a Test case is a test specification or scenario - the definition is unclear that it's a spec not a means to run an evaluation i.e. not something executable.
> Assistant: Agreed. Proposed definition: A specification of the preconditions, inputs, actions, expected results, and postconditions for one Test. A Test run executes the Test case and produces a Test result. This distinction follows the [ISTQB testing glossary](https://api.glossary.istqb.org/storage/help/R0uz58NqLzUz48LVUuyGSF76NFj4LHQazSs0GlNS.pdf).
> User: Agreed

### Test report

Definition: A retained summary of the scope, environment, results, evidence, and limitations of one or more test runs.

> Review note: Test report clarity 5/5. Alternatives: results summary 4/5; execution report 4/5. Decision: Keep test report because it includes scope, evidence, and limitations as well as results.
> User: Agreed

### Test result

Definition: The recorded outcome and supporting evidence produced by executing one test case.

> Review note: Test result clarity 5/5. Alternatives: test outcome 4/5; verdict 3/5. Decision: Keep test result because it includes both the outcome and its supporting evidence.
> User: Agreed

### Test run

Definition: One execution of selected test cases or test suites in a defined environment.

> Review note: Test run clarity 5/5. Alternatives: test execution 4/5; test session 3/5. Decision: Keep test run because it identifies one execution without implying an interactive session.
> User: Agreed

### Test suite

Definition: A named collection of related test cases that are selected and evaluated together.

Use for:

- The stable collection, independent of any one execution of that collection.

> Review note: Test suite clarity 5/5. Alternatives: test collection 4/5; test set 3/5. Decision: Keep test suite because it is the established term for a named, stable collection.
> User: Agreed. However, for AI we have the following frequent terminology:
> Eval portfolio
> └── Eval suite
> └── Eval/task
> ├── Dataset
> │ └── Samples/examples/cases
> So the Eval is one type of test and we might say there are several cases to cover which are refererred to as the Dataset - but frankly Dataset is more of a database thing, not sure we need to talk about it too much. In fact in traditional programming we nay have multiple individual tests exercisign the same code with different input conditions so it's not so far. So it seems Eval is a grouping of similar tests for which we only vary the inputs (keeping the agent and skill the same).
> Then We might have a suite - this can match a grouping of related agents e.g. the Dev Suite, the Coordonation Suite. And what we used to call Campaign would be referred to as our Eval Portfolio
> Assistant: I recommend the hierarchy Evaluation portfolio, Evaluation suite, Evaluation, and Evaluation case, followed separately by Evaluation run. An Evaluation keeps one target configuration and set of criteria while its cases vary the inputs. Frameworks may call those cases dataset items or samples, but Evaluation case is clearer in general prose. OpenAI models an evaluation as testing criteria plus a data-source configuration; Inspect models an evaluation task as a dataset, solver, and scorer: [OpenAI Evals](https://platform.openai.com/docs/api-reference/evals/deleteRun?lang=python) and [Inspect tasks](https://inspect.aisi.org.uk/tasks.html). Evaluation portfolio should replace campaign only when campaign means the stable governed collection. When campaign means a completed execution, use Evaluation run or Test run instead.
> User: Agreed, you actually made me understand even better the use of Campaign so it will be good to define it in the terminology and keep all the terms straight.
> Assistant: Agreed. Campaign should become a positive defined term, not an Avoid entry: a coordinated, bounded set of Evaluation runs performed for one evaluation objective or release baseline. The Evaluation portfolio is the stable collection available for selection; an Evaluation suite groups related Evaluations; a Campaign coordinates selected Evaluation runs; and an Evaluation run is one execution against a specified target configuration.
> User: Agreed

### Validation

Definition: A check that supplied data or an artifact satisfies explicit input rules such as a schema, format, type, or allowed value.

> Review note: Validation clarity 3/5. Alternatives: contract validation 5/5; input validation 4/5. Decision: Change to contract validation because it matches the defined check against explicit rules for data or artifacts.
> User: Agreed

### Verdict

Definition: A normalized decision produced by an evaluation after its required checks and judgments complete.

> Review note: Verdict clarity 3/5. Alternatives: evaluation decision 5/5; determination 3/5. Decision: Change to evaluation decision because it names the source and nature of the decision without a courtroom metaphor.
> User: Agreed

### Verification

Definition: An evidence-backed check that a claimed result or behavior satisfies its specified requirements and acceptance criteria.

> Review note: Verification clarity 5/5. Alternatives: acceptance check 4/5; confirmation 3/5. Decision: Keep verification because it requires evidence against requirements and acceptance criteria.
> User: Agreed

### Work item

Definition: A bounded unit of planned work with an objective, ownership, state, and completion conditions.

> Review note: Work item clarity 5/5. Alternatives: task 4/5; ticket 3/5. Decision: Keep work item because it includes ownership, state, and completion conditions across provider types.
> User: Agreed -we should also include Backlog
> Assistant: Agreed. Proposed definition: An ordered collection of Work items that are proposed, ready, active, or otherwise retained for future action. We should decide whether this project includes completed but unarchived Work items before making incomplete part of the definition.
> User: I'm not too crazy about adding the statuses here, remember our goal is to help document writers choose the right names, so having to check the status just to confirm that it's always that name is an unnecessary processing burden. It doesn't matter what status it's in, it's still a work item and not a ticket or task for example. Please confirm.
> Assistant: Confirmed. Status does not change the concept name. Proposed definition: A Backlog is a collection of Work items maintained for planning and coordination. Each member remains a Work item in every lifecycle state; writers do not inspect status before choosing the term.
> User: Agreed

### Workflow

Definition: A defined sequence of activities, decisions, and handoffs that produces an intended result.

> Review note: Workflow clarity 5/5. Alternatives: process 4/5; procedure 3/5. Decision: Keep workflow because it emphasizes activities, decisions, and handoffs that produce a result.
> User: Agreed
