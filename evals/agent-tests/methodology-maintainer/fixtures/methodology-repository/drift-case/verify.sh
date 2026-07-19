#!/bin/sh
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Verifies drift-case source, adapter, documentation, and regression alignment.
set -eu
script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$script_dir"
./regenerate.sh --check
expected=$(cat regression/expected-description.txt)
grep -F "description: $expected" skills/sample/SKILL.md
grep -F "description = \"$expected\"" generated/adapters/sample.toml
grep -F "sample: $expected" README.md
