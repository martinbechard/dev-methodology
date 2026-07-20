# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Models blocked-item resumption outcomes for deterministic evaluation fixtures.
# Governing design: evals/agent-tests/dev-backlog-steward/skills/dev-backlog-steward-suite-contract/SKILL.md
# Governing test plan: evals/agent-tests/dev-backlog-steward/test_contract.py

from __future__ import annotations


_SUCCESSFUL_CLAIM_OUTCOMES = frozenset({"PRIMARY", "ISOLATE", "RECOVER"})
_REQUIRED_ACTIVE_HANDOFF_MARKERS = (
    b"Status: Running",
    b"Owner:",
    b"Claim:",
    b"Blocker:",
    b"Unblock Condition:",
    b"Evidence:",
    b"Acceptance Criteria:",
)
_REQUIRED_BLOCKED_MARKERS = (
    b"Status: Blocked",
    b"Owner: Unowned",
    b"Claim: None",
    b"Blocker:",
    b"Unblock Condition:",
    b"Evidence:",
    b"Acceptance Criteria:",
)


def block_for_handoff(item_before: bytes) -> tuple[bytes, tuple[str, ...]]:
    """Release active ownership while preserving durable blocked-work evidence."""
    if any(marker not in item_before for marker in _REQUIRED_ACTIVE_HANDOFF_MARKERS):
        raise ValueError("blocked handoff fixture lacks required durable evidence")
    if b"Owner: Unowned" in item_before or b"Claim: None" in item_before:
        raise ValueError("blocked handoff fixture must begin with active ownership")

    lines = item_before.splitlines(keepends=True)
    replacements = {
        b"Status:": b"Status: Blocked\n",
        b"Owner:": b"Owner: Unowned\n",
        b"Claim:": b"Claim: None\n",
    }
    item_after = b"".join(
        replacements.get(line.split(maxsplit=1)[0], line) for line in lines
    )
    return item_after, ("running", "blocked", "released")


def attempt_resumption(
    item_before: bytes,
    *,
    unblock_condition_satisfied: bool,
    claim_outcome: str,
    new_owner: str | None = None,
    new_claim: str | None = None,
) -> tuple[bytes, tuple[str, ...]]:
    """Evaluate a blocked item's claimed-resumption transition.

    item_before is the exact durable Blocked item. unblock_condition_satisfied records
    prerequisite eligibility. claim_outcome is a structured claim result such as WAIT or
    PRIMARY. Successful outcomes also require non-empty new_owner and new_claim values.
    The result contains the durable post-attempt bytes and the ordered lifecycle evidence.
    Rejected or failed claims return the original bytes unchanged. Missing evidence or
    successful outcomes without ownership identifiers raise ValueError.
    """
    if any(marker not in item_before for marker in _REQUIRED_BLOCKED_MARKERS):
        raise ValueError("blocked resumption fixture lacks required durable evidence")

    if not unblock_condition_satisfied:
        return item_before, ("blocked",)
    if claim_outcome == "NOT_ATTEMPTED":
        return item_before, ("blocked", "rejected-unowned")
    if claim_outcome not in _SUCCESSFUL_CLAIM_OUTCOMES:
        return item_before, ("blocked", "ready", "claim-failed", "blocked")
    if not new_owner or not new_claim:
        raise ValueError("successful claim outcome requires a new owner and claim")

    item_after = item_before.replace(b"Status: Blocked", b"Status: Running", 1)
    item_after = item_after.replace(b"Owner: Unowned", f"Owner: {new_owner}".encode(), 1)
    item_after = item_after.replace(b"Claim: None", f"Claim: {new_claim}".encode(), 1)
    return item_after, ("blocked", "ready", "claimed", "running")
