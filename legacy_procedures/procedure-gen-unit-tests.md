CREATE TESTS:

READ THESE INSTRUCTIONS AND PAY CLOSE ATTENTION TO WHAT IS ASKED - DO NOT ADD EXTRANEOUS THINGS NOT REQUESTED.
We are using jest for testing.
We are using CommonJS imports.

LIST all of the files of the form `<module name>.plan.md` under the tests folder, and find which ones don’t have a corresponding test suite of the form `<module name>.test.ts`.

Read File-List.md to know where the original source
FOR EACH missing test suite, CREATE unit tests from the test plans found in that folder.
FOR ANY existing test suite, verify if the full test plan it is based on has been implemented fully and if not then creat the missing tests.

FOR project import paths, ALWAYS USE the ‘@/‘ alias at the start of paths unless relative to the current folder in which case use ‘./‘ at the start.
For example if a file is under src/utils/myUtil.ts, then use the import path:
import { myFunc } from '@/utils/myUtil.js'

Add an import of functions from the file under test example: import { myFunc } from ‘@/markdown-serialization/<process name>/MyComponent’

IMPORTANT: DO NOT TRY TO FIX TYPESCRIPT ERRORS including Import paths. We will fix them later.

Don't make the test file longer than 200 lines, create a new test file if it gets bigger.
You can either name them sequentially or give a suffix if the new file is focused on a particular functionality.
IMPORTANT: NEVER use` replace_in_file`, it doesn't work. always use `write_to_file`
