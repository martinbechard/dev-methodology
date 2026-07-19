# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Validates the initial and completed direct-path bootstrap states.

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def evidence() -> dict[str, bool]:
    """Return observable configuration and documentation state."""

    project_text = (ROOT / "PROJECT.yaml").read_text()
    manifest_text = (ROOT / "docs" / "coverage-manifest.yaml").read_text()
    return {
        "configurationValid": all(
            marker in project_text
            for marker in ("path: src", "dev-documentation-writer", "dev-verifier")
        ),
        "acceptedConfigurationReview": (
            '"status": "accepted"'
            in (ROOT / "accepted-configuration-review.json").read_text()
        ),
        "moduleDocumentPresent": (ROOT / "docs" / "module-inventory.md").is_file(),
        "manifestAccepted": "status: accepted" in manifest_text,
    }


def main() -> int:
    """Validate the selected fixture phase and print JSON evidence."""

    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("initial", "final"))
    args = parser.parse_args()
    state = evidence()
    print(json.dumps(state, sort_keys=True))
    if not state["configurationValid"] or not state["acceptedConfigurationReview"]:
        return 2
    if args.phase == "initial":
        return 0 if not state["moduleDocumentPresent"] else 3
    return 0 if state["moduleDocumentPresent"] and state["manifestAccepted"] else 4


if __name__ == "__main__":
    raise SystemExit(main())
