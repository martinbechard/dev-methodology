Read the module code.

Create a document called design/data-lineage-flowchart.md if it doesn't exist. This will contain the data lineage for all modules in the solution, which we are building module by module. The file has to start with a line containing graph LR

1. Identify all of the output variables from this modules. These are variables that are returned to a caller or passed down to a dependency as a parameter, or global varabies exposed as exports
2. For each output variable:
   2.1 Choose a scoped name consisting of `<containing module>_<variable name>` if global, or `<containing module>_<class name>_<member name>` if in a class, or `<containing module>_<function name>_<variable name>` if in a function.
   2.2 If passed as a parameter, add a line indicating `<containing module>_<variable name> --> <destination module>_<function name>_<parameter name>`
   2.3 If assigned to an imported variable , add a line indicating `<containing module>_<variable name> --> <destination import module>_<imported variable>`
   2.4 If returned to a caller, read the calling function code and find the name of the variable it is returned into.

3. Identify all of the input variables from this module. These are variables that are parameters to a function, or exported global variables being assigned to.
   3.1 Choose a scoped name consisting of `<containing module>_<variable name>` if global, or `<containing module>_<class name>_<member name>` if in a class, or `<containing module>_<function name>_<variable name>` if in a function.
   3.2 If received as a parameter, add a line indicating `<calling module>_<variable name> -> <containing module>_<function name>_<parameter name>`
   3.3 If assigned to an exported variable , add a line indicating `<assigning module>_<variable name> --> <containing module>_<exported variable>`

4. Identify all of the intermediate variables in this module. These are variables used to propagate a value from an input variable to an output variable.
   4.1 Choose a scoped name consisting of `<containing module>_<variable name>` if global, or `<containing module>_<class name>_<member name>` if in a class, or `<containing module>_<function name>_<variable name>` if in a function.
   4.2 Add a line for each assignment or each read to and from other variables.

Careful: this is a data lineage exercise, you need to study the callers to know what variables are related to the variables you are documenting.
DO not write type information or other documentation which would be redundant with design documents.
