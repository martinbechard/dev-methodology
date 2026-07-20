#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Selects a fail-closed harness route for bounded synthetic security-review scenarios.
# Governing design: evals/agent-tests/dev-security-reviewer/skills/dev-security-reviewer-suite-contract/SKILL.md
# Governing test plan: evals/agent-tests/dev-security-reviewer/test_route_selection.py

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml


_SUITE_ROOT = Path(__file__).resolve().parent
_REPOSITORY_ROOT = _SUITE_ROOT.parents[2]
_DEFAULT_CATALOG = _SUITE_ROOT / "fixtures" / "policy-compatible-routes.yaml"
_EXPECTED_SCOPE = "bounded-synthetic-security-review"
_MODEL_FAMILY = re.compile(r"^[a-z0-9]+(?:[.-][a-z0-9]+)*$")


@dataclass(frozen=True)
class RouteDecision:
    """Represent the auditable pre-dispatch decision for one active harness route."""

    status: str
    reason: str
    harness: str
    scope: str | None
    native_agent: str | None
    native_agent_sha256: str | None
    model: str | None
    model_family: str | None
    catalog_sha256: str | None

    def to_json(self) -> str:
        """Return a stable JSON receipt suitable for retained deterministic evidence."""

        return json.dumps(asdict(self), sort_keys=True)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _blocked(
    reason: str,
    harness: str,
    catalog_sha256: str | None,
    *,
    scope: str | None = None,
    native_agent: str | None = None,
    native_agent_sha256: str | None = None,
    model: str | None = None,
    model_family: str | None = None,
) -> RouteDecision:
    return RouteDecision(
        status="INFRASTRUCTURE_BLOCKED",
        reason=reason,
        harness=harness,
        scope=scope,
        native_agent=native_agent,
        native_agent_sha256=native_agent_sha256,
        model=model,
        model_family=model_family,
        catalog_sha256=catalog_sha256,
    )


def _load_mapping(path: Path) -> Mapping[str, Any]:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, Mapping):
        raise ValueError("route catalog must be a mapping")
    return loaded


def _model_from_agent(path: Path, harness: str) -> str:
    text = path.read_text(encoding="utf-8")
    if harness == "codex":
        matches = re.findall(r'^model\s*=\s*"([^"]+)"\s*$', text, flags=re.MULTILINE)
        if len(matches) != 1:
            raise ValueError("Codex native agent has no unique model field")
        model = matches[0]
    elif harness == "junie":
        if not text.startswith("---\n") or "\n---\n" not in text[4:]:
            raise ValueError("Junie native agent has no YAML frontmatter")
        frontmatter = text[4:].split("\n---\n", 1)[0]
        loaded = yaml.safe_load(frontmatter)
        if not isinstance(loaded, Mapping):
            raise ValueError("native agent metadata must be a mapping")
        model = loaded.get("model")
    else:
        raise ValueError(f"unsupported harness: {harness}")
    if not isinstance(model, str) or not _MODEL_FAMILY.fullmatch(model.lower()):
        raise ValueError("native agent model is missing or malformed")
    return model


def _model_family(model: str) -> str:
    return re.split(r"[.-]", model.lower())[-1]


def select_route(
    catalog_path: Path,
    repository_root: Path,
    active_harness: str,
    available_harnesses: frozenset[str],
) -> RouteDecision:
    """Validate the active harness against suite policy before cybersecurity dispatch.

    The caller supplies runtime availability separately from the suite-owned catalog. The
    result selects only the active harness; it never silently falls back to another runtime.
    Any unavailable, prohibited, or malformed route returns an infrastructure blocker.
    """

    catalog_sha256: str | None = None
    try:
        catalog_sha256 = _sha256(catalog_path)
        catalog = _load_mapping(catalog_path)
        if catalog.get("schema") != "dev-security-reviewer-policy-routes" or catalog.get("version") != 1:
            raise ValueError("route catalog schema or version is unsupported")
        scope = catalog.get("scope")
        routes = catalog.get("routes")
        if scope != _EXPECTED_SCOPE or not isinstance(routes, Mapping):
            raise ValueError("route catalog scope or routes are malformed")
        route = routes.get(active_harness)
        if not isinstance(route, Mapping):
            raise ValueError("active harness route is missing")
        native_agent = route.get("nativeAgent")
        permitted = route.get("permittedModelFamilies")
        prohibited = route.get("prohibitedModelFamilies")
        if (
            not isinstance(native_agent, str)
            or not native_agent
            or not isinstance(permitted, list)
            or not all(isinstance(value, str) and value for value in permitted)
            or not isinstance(prohibited, list)
            or not all(isinstance(value, str) and value for value in prohibited)
        ):
            raise ValueError("active harness route evidence is malformed")
        agent_path = (repository_root / native_agent).resolve()
        if not agent_path.is_relative_to(repository_root.resolve()) or not agent_path.is_file():
            raise ValueError("native agent path is unavailable or escapes the repository")
        model = _model_from_agent(agent_path, active_harness)
        family = _model_family(model)
        digest = _sha256(agent_path)
    except (OSError, UnicodeError, ValueError, yaml.YAMLError):
        return _blocked("MALFORMED_ROUTE_EVIDENCE", active_harness, catalog_sha256)

    common = {
        "scope": scope,
        "native_agent": native_agent,
        "native_agent_sha256": digest,
        "model": model,
        "model_family": family,
    }
    if active_harness not in available_harnesses:
        return _blocked("ROUTE_UNAVAILABLE", active_harness, catalog_sha256, **common)
    if family in {value.lower() for value in prohibited}:
        return _blocked("MODEL_FAMILY_PROHIBITED", active_harness, catalog_sha256, **common)
    if family not in {value.lower() for value in permitted}:
        return _blocked("MODEL_FAMILY_NOT_PERMITTED", active_harness, catalog_sha256, **common)
    return RouteDecision(
        status="SELECTED",
        reason="POLICY_COMPATIBLE_ROUTE",
        harness=active_harness,
        catalog_sha256=catalog_sha256,
        **common,
    )


def _argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Select the active Dev Security Reviewer suite route.")
    parser.add_argument("--harness", required=True, choices=("codex", "junie"))
    parser.add_argument("--available-harness", action="append", required=True, choices=("codex", "junie"))
    parser.add_argument("--catalog", type=Path, default=_DEFAULT_CATALOG)
    parser.add_argument("--repository-root", type=Path, default=_REPOSITORY_ROOT)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Emit one route receipt and stop dispatch with exit two unless it is selected."""

    arguments = _argument_parser().parse_args(argv)
    decision = select_route(
        arguments.catalog.resolve(),
        arguments.repository_root.resolve(),
        arguments.harness,
        frozenset(arguments.available_harness),
    )
    print(decision.to_json())
    return 0 if decision.status == "SELECTED" else 2


if __name__ == "__main__":
    sys.exit(main())
