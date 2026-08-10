---
name: python
description: Implement, refactor, test, or review Python source with explicit module boundaries, type-aware interfaces, predictable resource handling, and project-native tooling. Use for Python files and Python package work.
metadata:
  category: stack-and-domain
---

# Python

Follow the owning project's Python version, packaging metadata, formatter, linter, type checker, and test runner.

## Implementation

- Keep public functions, classes, exceptions, and module boundaries explicit.
- Prefer standard library types and direct control flow over speculative abstractions.
- Use standard-library tempfile APIs for Python-owned temporary files and directories. Do not shell out to mktemp, PowerShell, or another operating-system command.
- Let tempfile select the operating-system temporary root. It can honor TMPDIR, TEMP, or TMP where the platform supports them.
- Normally use TemporaryDirectory, NamedTemporaryFile, or another tempfile API through context managers for deterministic cleanup. Close raw descriptors from mkstemp before later open, replace, or delete operations.
- Use pathlib for paths. Do not assemble separators or assume a POSIX root. Test drive and UNC paths when path semantics are part of the contract.
- Pass shell-free subprocess argument vectors. Use sys.executable for the current Python runtime and shutil.which for supported external executable discovery. Do not hard-code Unix binary paths or Windows executable suffixes.
- Use an explicit operating-system branch only when behavior genuinely differs. Keep the portable path shared and test each supported branch.
- Preserve exception causes when translating errors at an owning boundary.
- Avoid mutable default arguments and implicit shared state.
- Keep asynchronous and synchronous call paths distinct.
- When a Gang of Four pattern is explicit, combine its generic pattern skill with Python Design Pattern Examples and prefer native functions, protocols, dataclasses, modules, and generators where they preserve the intent.

## Verification

- Add focused tests for changed behavior and failure boundaries.
- Run the narrow project-native test command first, then applicable lint, formatting, and type checks.
- Verify supported Python versions when syntax or library behavior is version-sensitive.
