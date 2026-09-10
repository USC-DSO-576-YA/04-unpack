"""Structural checker for Module 4; it intentionally does not print answers."""

from __future__ import annotations

import ast
from pathlib import Path
import subprocess
import sys

import pandas as pd


ROOT = Path(__file__).resolve().parent
HOMEWORK = ROOT / "worldstage_homework.py"


def unfinished_tasks() -> list[int]:
    tree = ast.parse(HOMEWORK.read_text(encoding="utf-8"))
    unfinished: list[int] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Raise) or node.exc is None:
            continue
        if not isinstance(node.exc, ast.Call) or not node.exc.args:
            continue
        message = node.exc.args[0]
        if isinstance(message, ast.Constant) and isinstance(message.value, str):
            if message.value.startswith("Complete Task "):
                unfinished.append(int(message.value.removeprefix("Complete Task ")))
    return sorted(unfinished)


def require(condition: bool, task: int, message: str) -> None:
    if not condition:
        raise AssertionError(f"Task {task}: {message}")


def check_outputs() -> None:
    clean = pd.read_csv(ROOT / "worldstage_shows.csv")
    raw = pd.read_csv(ROOT / "worldstage_shows_raw.csv")
    summary = pd.read_csv(ROOT / "regional_summary.csv")
    cleaned = pd.read_csv(ROOT / "worldstage_cleaned.csv")
    audit = pd.read_csv(ROOT / "cleaning_audit.csv")

    required_summary = [
        "region",
        "total_tickets",
        "avg_sell_through",
        "shows",
        "rated_shows",
        "countries",
        "avg_rating",
        "total_revenue",
    ]
    require(
        list(summary.columns) == required_summary,
        2,
        "summary columns or order differ",
    )
    require(len(summary) == 4, 2, "summary must contain one row per region")
    require(
        set(summary["region"]) == {"Asia", "Europe", "America", "Africa"},
        2,
        "region groups differ",
    )
    require(
        summary["total_tickets"].is_monotonic_decreasing,
        2,
        "total_tickets is not sorted descending",
    )
    require(
        summary["shows"].sum() == len(clean),
        2,
        "show counts do not cover the clean data",
    )
    require(
        summary["total_tickets"].sum() == clean["tickets_sold"].sum(),
        2,
        "ticket totals changed during grouping",
    )
    require(
        summary["rated_shows"].sum() == clean["fan_rating"].count(),
        2,
        "rated-show counts are inconsistent",
    )
    require(
        summary["countries"].sum() == clean["country"].nunique(),
        2,
        "country counts are inconsistent",
    )

    require(len(cleaned) == len(raw), 4, "cleaning must preserve all raw rows")
    require(set(raw.columns).issubset(cleaned.columns), 4, "a raw column was removed")
    require(
        {"country_key", "country", "region"}.issubset(cleaned.columns),
        4,
        "location columns are missing",
    )
    unknown_mask = raw["country_raw"].eq("Atlantis")
    require(
        cleaned.loc[unknown_mask, ["country", "region"]].isna().all().all(),
        4,
        "an unknown country was guessed",
    )

    require(
        {"event_type", "status"}.issubset(cleaned.columns),
        5,
        "clean label columns are missing",
    )
    require(
        set(cleaned["status"].dropna())
        == {"completed", "cancelled", "postponed"},
        5,
        "status labels are not standardized",
    )
    require(
        set(cleaned["event_type"].dropna())
        == {"Arena Show", "Festival", "Club Show", "Stadium Show"},
        5,
        "event labels are not standardized",
    )

    require("ticket_price" in cleaned.columns, 6, "numeric ticket_price is missing")
    raw_price = raw["ticket_price_raw"].astype("string").str.strip().str.lower()
    free_mask = raw_price.eq("free")
    unknown_price = raw_price.isin(["", "tbd"])
    require(
        cleaned.loc[free_mask, "ticket_price"].eq(0).all(),
        6,
        "FREE must become known zero",
    )
    require(
        cleaned.loc[unknown_price, "ticket_price"].isna().all(),
        6,
        "blank and TBD prices must stay unknown",
    )

    expected_measures = {
        "raw_rows",
        "completed_rows",
        "cancelled_rows",
        "postponed_rows",
        "missing_country_before_fill",
        "missing_event_type_before_fill",
        "missing_ticket_price_before_fill",
        "missing_marketing_spend_before_fill",
        "missing_fan_rating_before_fill",
        "missing_tickets_sold_before_fill",
        "attendance_ready_rows",
        "revenue_ready_rows",
        "rating_ready_rows",
    }
    require(
        set(audit["measure"]) == expected_measures,
        7,
        "cleaning audit measures differ",
    )
    require(
        cleaned["marketing_spend"].notna().all(),
        8,
        "marketing_spend still contains missing values",
    )
    require(
        cleaned["fan_rating"].isna().sum() == raw["fan_rating"].isna().sum(),
        8,
        "fan-rating missingness was changed",
    )
    require(
        cleaned["tickets_sold"].isna().sum()
        == raw["tickets_sold"].isna().sum(),
        8,
        "attendance missingness was changed",
    )

    audit_values = audit.set_index("measure")["value"]
    attendance_rows = int(audit_values["attendance_ready_rows"])
    revenue_rows = int(audit_values["revenue_ready_rows"])
    rating_rows = int(audit_values["rating_ready_rows"])
    require(
        attendance_rows == cleaned["tickets_sold"].notna().sum(),
        9,
        "attendance-ready row count differs",
    )
    require(
        revenue_rows
        == cleaned[["tickets_sold", "ticket_price"]].notna().all(axis=1).sum(),
        9,
        "revenue-ready row count differs",
    )
    require(
        rating_rows == cleaned["fan_rating"].notna().sum(),
        9,
        "rating-ready row count differs",
    )

    chart = ROOT / "sell_through_by_region.png"
    require(
        chart.exists() and chart.stat().st_size > 5_000,
        10,
        "chart file is missing or empty",
    )


def main() -> None:
    unfinished = unfinished_tasks()
    if unfinished:
        joined = ", ".join(str(task) for task in unfinished)
        print(f"Unfinished tasks: {joined}")
        print(f"Start with Task {unfinished[0]}. The checker will not show its answer.")
        raise SystemExit(1)

    run = subprocess.run(
        [sys.executable, str(HOMEWORK)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if run.returncode != 0:
        print("The homework script stopped before structural checks could run.")
        print(run.stderr.strip() or run.stdout.strip())
        raise SystemExit(1)

    try:
        check_outputs()
    except AssertionError as error:
        print(error)
        print("Revise that task, then run the checker again.")
        raise SystemExit(1) from error

    print("All 10 code tasks passed the structural checks.")
    print("Inspect the four outputs and complete tour_review.md in your own words.")


if __name__ == "__main__":
    main()
