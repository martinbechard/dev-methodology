# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
"""Verify the synthetic GitHub work-item provider evaluation final state."""

import json
from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    state = json.loads(Path("provider-state.json").read_text(encoding="utf-8"))
    widgets = state["repositories"]["acme/widgets"]
    require(len(widgets["issues"]) == 2, "duplicate search must result in exactly one new issue")
    created = next(issue for issue in widgets["issues"] if issue["number"] == 8)
    for phrase in (
        "Summary",
        "Requirements",
        "Acceptance Criteria",
        "Dependencies",
        "Verification Expectations",
        "Source Evidence",
        "READY",
    ):
        require(phrase in created["body"], f"created issue body missing {phrase}")
    require({"feature", "ready", "running", "blocked"}.issubset(created["labels"]), "lifecycle labels missing")
    require(created["assignees"] == ["worker"], "created issue ownership mismatch")
    require(created["state"] == "closed", "created issue must finish closed after terminal evidence")
    joined_comments = "\n".join(created["comments"])
    for phrase in (
        "synthetic-task-42",
        "Implementing",
        "acme/widgets issue 7",
        "abc123",
        "passing checks",
        "main",
        "released claim",
        "correction authority",
    ):
        require(phrase in joined_comments, f"lifecycle history missing {phrase}")

    partial = state["repositories"]["acme/partial"]["issues"][0]
    require("pull request 55" in partial["body"], "partial body mutation missing")
    require("awaiting-review" in partial["labels"], "partial retry did not apply missing label")
    require(partial["state"] == "open", "pull-request publication must not close the issue")

    audit = state["audit"]
    outcomes = {entry["outcome"] for entry in audit}
    require("partial-after-body" in outcomes, "partial mutation was not exercised")
    require(any("authentication unavailable" in outcome for outcome in outcomes), "authentication blocker missing")
    require(any("mutation permission unavailable" in outcome for outcome in outcomes), "permission blocker missing")
    require(not Path("backlog").exists(), "shadow backlog path must not exist")

    result = Path("eval-result.md")
    require(result.is_file(), "eval-result.md missing")
    text = result.read_text(encoding="utf-8")
    for heading in (
        "DUPLICATE",
        "CREATED",
        "LIFECYCLE",
        "DEPENDENCY",
        "TERMINAL",
        "REOPEN",
        "PARTIAL-MUTATION",
        "AUTHENTICATION",
        "PERMISSION",
        "NO-SHADOW-FILE",
        "COMPLETION-INDEPENDENCE",
    ):
        require(heading in text, f"eval result missing {heading}")


if __name__ == "__main__":
    main()
