# Mockito Review Checklist

- Question: Does each mock represent an intentional external, nondeterministic, destructive, slow, or isolated collaborator boundary?
- Question: Would a real value, pure collaborator, or lightweight fake express the contract more clearly?
- Question: Is strict stubbing preserved without unused, broad, shadowed, or unjustifiably lenient setup?
- Question: Are stubs limited to behavior required for the scenario and are matchers used consistently?
- Question: Do verifications cover only contractual calls, arguments, counts, ordering, or non-interaction?
- Question: Are state and returned-value assertions used instead of redundant verification where appropriate?
- Question: Are captors reserved for verification of otherwise unobservable values?
- Question: Are spies, partial mocks, static or construction mocks, deep stubs, and resets avoided or explicitly justified?
- Question: Are mocks fresh per test and initialized by the owning test framework's supported integration?
- Question: Does the reported evidence distinguish mocked boundaries from real integrations and identify the commands that ran?
