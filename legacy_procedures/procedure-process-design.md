Based on design/markdown-serialization-examples.md, create a design document of the’ process in its own file called design/<process name>-process.md.

DO a top-down decomposition of the process with a single topmost function.
EXPLAIN each function the inputs/outputs and the steps, according to the following directives:

- DESCRIBE the inputs and outputs using examples of values, and a summary explaining the rationale of the example
- Provide examples for every possible types of inputs, according the markdown-serialization-examples.md at the top level or from the calling function.
- For a transformational function, structure the steps in the code to match the structure of the inputs and create child functions for each part
- For a control dispatch function, use a switch based on the event being dispatched and create a child function for each event type
- Break down a function recursively into child functions of 1 to 3 business rules each.
- DESCRIBE step by step what it needs to do using pseudo-code

## Pseudo-code Documentation Rules

FORMAT pseudo-code as:

`PROCEDURE name(params)
	Action1
		BECAUSE main reason
		BECAUSE deeper context (up to 3 more)
	IF/WHILE/FOR condition THEN
		DO Action2
		BECAUSE explanations
		 DO Action12
		BECAUSE explanations
		    etc.
	END IF/WHILE/FOR
END PROCEDURE`

    - Add BECAUSE after each significant action
    - Chain up to 5 BECAUSE statements for complex operations
    - Each BECAUSE should add new information
    - Keep indentation consistent
    - Include error handling
    - EXPLAIN component interactions

EXAMPLE::
`
PROCEDURE processInput(text)
	ValideInput
		BECAUSE we must check format
		BECAUSE invalid input breaks processing
	CreateContext
		BECAUSE we track processing state
		BECAUSE state affects decisions
		BECAUSE we may need to backtrack
		 BECAUSE in case of error, we need to get back to a stable state
		 BECAUSE we won't be able to do anything if we aren't in a stable state
END PROCEDURE`
