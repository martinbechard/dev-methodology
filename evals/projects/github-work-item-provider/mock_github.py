# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
"""Deterministic synthetic GitHub issue provider for the work-item skill fixture."""

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional


class ProviderError(RuntimeError):
    """Report one provider boundary failure with a stable process status."""

    def __init__(self, message: str, exit_code: int) -> None:
        super().__init__(message)
        self.exit_code = exit_code


def load_state(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(path: Path, state: Dict[str, Any]) -> None:
    path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def repository(state: Dict[str, Any], name: str, mutation: bool = False) -> Dict[str, Any]:
    try:
        repo = state["repositories"][name]
    except KeyError as error:
        raise ProviderError(f"repository not found: {name}", 2) from error
    if not repo.get("authenticated", False):
        raise ProviderError(f"authentication unavailable for {name}", 3)
    if mutation and not repo.get("can_mutate", False):
        raise ProviderError(f"mutation permission unavailable for {name}", 4)
    return repo


def audit(
    state: Dict[str, Any], command: str, repo: str, outcome: str, number: Optional[int] = None
) -> None:
    entry: Dict[str, Any] = {"command": command, "repository": repo, "outcome": outcome}
    if number is not None:
        entry["number"] = number
    state.setdefault("audit", []).append(entry)


def issue_by_number(repo: Dict[str, Any], number: int) -> Dict[str, Any]:
    for issue in repo["issues"]:
        if issue["number"] == number:
            return issue
    raise ProviderError(f"issue not found: {number}", 2)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", type=Path, required=True)
    subparsers = parser.add_subparsers(dest="command", required=True)

    for name in ("repository", "search"):
        command = subparsers.add_parser(name)
        command.add_argument("--repository", required=True)
        if name == "search":
            command.add_argument("--query", required=True)

    get_command = subparsers.add_parser("get")
    get_command.add_argument("--repository", required=True)
    get_command.add_argument("--number", type=int, required=True)

    create = subparsers.add_parser("create")
    create.add_argument("--repository", required=True)
    create.add_argument("--title", required=True)
    create.add_argument("--body", required=True)
    create.add_argument("--label", action="append", default=[])
    create.add_argument("--assignee", action="append", default=[])

    update = subparsers.add_parser("update")
    update.add_argument("--repository", required=True)
    update.add_argument("--number", type=int, required=True)
    update.add_argument("--body")
    update.add_argument("--add-label", action="append", default=[])
    update.add_argument("--assignee", action="append", default=[])
    update.add_argument("--comment")
    update.add_argument("--issue-state", choices=("open", "closed"))
    return parser.parse_args()


def perform(args: argparse.Namespace, state: Dict[str, Any]) -> Dict[str, Any]:
    repo_name = args.repository
    if args.command == "repository":
        repo = repository(state, repo_name)
        return {"repository": repo_name, "authenticated": True, "can_mutate": repo["can_mutate"]}
    if args.command == "search":
        repo = repository(state, repo_name)
        query = args.query.casefold()
        return {
            "repository": repo_name,
            "issues": [
                issue
                for issue in repo["issues"]
                if query in issue["title"].casefold() or query in issue["body"].casefold()
            ],
        }
    if args.command == "get":
        repo = repository(state, repo_name)
        return {"repository": repo_name, "issue": issue_by_number(repo, args.number)}
    if args.command == "create":
        repo = repository(state, repo_name, mutation=True)
        number = repo["next_number"]
        repo["next_number"] += 1
        issue = {
            "number": number,
            "url": f"https://github.example/{repo_name}/issues/{number}",
            "title": args.title,
            "body": args.body,
            "state": "open",
            "labels": sorted(set(args.label)),
            "assignees": sorted(set(args.assignee)),
            "comments": [],
        }
        repo["issues"].append(issue)
        audit(state, "create", repo_name, "created", number)
        return {"repository": repo_name, "issue": issue}
    if args.command == "update":
        repo = repository(state, repo_name, mutation=True)
        issue = issue_by_number(repo, args.number)
        failure_key = f"update:{args.number}"
        if args.body is not None:
            issue["body"] = args.body
        if repo.get("fail_once", {}).pop(failure_key, None) == "after_body":
            audit(state, "update", repo_name, "partial-after-body", args.number)
            raise ProviderError(f"ambiguous partial update for {repo_name} issue {args.number}", 5)
        issue["labels"] = sorted(set(issue["labels"] + args.add_label))
        if args.assignee:
            issue["assignees"] = sorted(set(args.assignee))
        if args.comment:
            issue["comments"].append(args.comment)
        if args.issue_state:
            issue["state"] = args.issue_state
        audit(state, "update", repo_name, "updated", args.number)
        return {"repository": repo_name, "issue": issue}
    raise ProviderError(f"unsupported command: {args.command}", 2)


def main() -> int:
    args = parse_args()
    state = load_state(args.state)
    try:
        result = perform(args, state)
    except ProviderError as error:
        audit(state, args.command, args.repository, f"blocked:{error}", getattr(args, "number", None))
        save_state(args.state, state)
        print(json.dumps({"outcome": "BLOCKED", "message": str(error)}, sort_keys=True))
        return error.exit_code
    save_state(args.state, state)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
