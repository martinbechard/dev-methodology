# Java Comment Placement Evaluation

Move the existing file-level metadata into valid Java Javadoc without changing its information.

Use the simple-workitem delivery process. Complete and commit the verified local change without publishing a branch or pull request.

Requirements:

- In package-info.java, merge the metadata into the package documentation immediately before the package declaration.
- In the ordinary packaged source, merge the metadata into the first top-level type Javadoc after the package declaration.
- In the source without a package declaration, merge the metadata into the first top-level type Javadoc at the beginning of the file.
- Preserve the exact copyright, truthful AI attribution, responsibility, design, and test-plan values already present in each source.
- Keep the existing public documentation content.
- Remove the standalone metadata blocks after their information is preserved in Javadoc.
- Treat every file under negative-fixtures, including the corrected goldens, as protected evaluator input. Do not edit negative-fixtures, verify.py, or TASK.md.
- Run python3 verify.py.

Write eval-result.md with these exact evidence headings: JAVA-COMMENT-PACKAGE, JAVA-COMMENT-PACKAGED-TYPE, JAVA-COMMENT-NO-PACKAGE, JAVA-COMMENT-DUPLICATE-REJECTED, JAVA-COMMENT-MISSING-REJECTED, and REVIEW-SYNTHESIS. Record the affected path and verification result under each heading.

Write every required record delimiter as an exact Markdown line beginning with two number signs, one space, and the required name. Under each heading, include exactly one of each field with a non-empty value:

Affected path: <non-empty repository-relative path>

Verification result: <non-empty result>

Bare labels, duplicate required headings, malformed headings, and blank field values are invalid evidence. Fenced code is allowed as supplementary content and is ignored when locating required headings and fields. HTML is allowed in verification-result content; the evaluator does not interpret HTML or emulate renderer semantics.
