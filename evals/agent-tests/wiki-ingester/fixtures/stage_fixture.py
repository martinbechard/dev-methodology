# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Stages one self-contained Wiki Ingester evaluation repository from tracked fixture inputs.

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


SCENARIOS = ("raw-ingest", "destination-collision", "verifier-failure")
REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
BASE_FIXTURE = REPOSITORY_ROOT / "evals" / "projects" / "wiki-raw-ingest"
OVERLAY_ROOT = Path(__file__).resolve().parent / "scenario-files"
ORDER_SOURCE = Path("raw/2026-07-15-order-cancellation.md")
PROCESSED_ORDER_SOURCE = Path("raw/processed/2026-07-15-order-cancellation.md")
ORDER_PAGE = Path("docs/wiki/orders/order-lifecycle.md")


def stage_fixture(scenario: str, destination: Path) -> None:
    """Copy the common wiki baseline and apply one tracked scenario overlay."""
    if scenario not in SCENARIOS:
        raise ValueError(f"unsupported Wiki Ingester scenario: {scenario}")
    if destination.exists():
        raise FileExistsError(f"fixture destination already exists: {destination}")
    overlay = OVERLAY_ROOT / scenario
    if not BASE_FIXTURE.is_dir() or not overlay.is_dir():
        raise FileNotFoundError(f"fixture inputs are incomplete for {scenario}")

    shutil.copytree(BASE_FIXTURE, destination)
    processed_source = destination / PROCESSED_ORDER_SOURCE
    processed_source.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(destination / ORDER_SOURCE, processed_source)

    order_page = destination / ORDER_PAGE
    page_text = order_page.read_text(encoding="utf-8")
    raw_link = "../../../raw/2026-07-15-order-cancellation.md"
    processed_link = "../../../raw/processed/2026-07-15-order-cancellation.md"
    if raw_link not in page_text:
        raise RuntimeError(f"common fixture lacks the expected raw source link: {ORDER_PAGE}")
    order_page.write_text(page_text.replace(raw_link, processed_link), encoding="utf-8")

    shutil.copytree(overlay, destination, dirs_exist_ok=True)


def parse_args() -> argparse.Namespace:
    """Parse the bounded fixture-builder command line."""
    parser = argparse.ArgumentParser(description="Stage one Wiki Ingester evaluation fixture.")
    parser.add_argument("--scenario", choices=SCENARIOS, required=True)
    parser.add_argument("--destination", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    """Stage the selected fixture and report its resolved path."""
    args = parse_args()
    stage_fixture(args.scenario, args.destination.resolve())
    print(args.destination.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
